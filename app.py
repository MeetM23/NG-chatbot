"""
Funding Scheme Assistant - Flask Backend
Answers questions strictly based on the 'Funding Opportunity - Industry Sector Wise' document.
Optimized for high speed, sectioned knowledge routing, and streaming responses on Groq free tier.
"""

import os
import re
import time
from flask import Flask, request, jsonify, render_template, Response, stream_with_context, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq, RateLimitError, NotFoundError

# Load environment variables from .env
load_dotenv()

# Model configuration: default to llama-3.1-8b-instant (overridable via .env GROQ_MODEL)
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
FALLBACK_MODEL = "openai/gpt-oss-20b"  # Active fast fallback if primary is not available in catalog or quota-limited

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment or .env file.")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# 1. SECTIONED KNOWLEDGE: Load knowledge.md into sections dict at startup
KNOWLEDGE_PATH = os.path.join(os.path.dirname(__file__), "knowledge.md")
KNOWLEDGE_SECTIONS = {}

def load_sections(filepath: str) -> dict[str, str]:
    """Parses knowledge.md into a dictionary keyed by '## ' section titles."""
    sections = {}
    current_title = None
    lines_acc = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("## "):
                if current_title:
                    sections[current_title] = "".join(lines_acc).strip()
                current_title = line[3:].strip()
                lines_acc = []
            elif current_title:
                lines_acc.append(line)
        if current_title:
            sections[current_title] = "".join(lines_acc).strip()
    return sections

KNOWLEDGE_SECTIONS = load_sections(KNOWLEDGE_PATH)
print(f"[Startup] Loaded {len(KNOWLEDGE_SECTIONS)} knowledge sections: {list(KNOWLEDGE_SECTIONS.keys())}", flush=True)

# 2. KEYWORD ROUTING MAP
KEYWORD_SECTION_MAP = {
    # Sectors
    "Agri-Tech": ["agri", "agritech", "farm", "farmer", "agriculture", "crop", "farming", "krishi"],
    "Food": ["food", "beverage", "processing", "fpo", "pmfme", "agro"],
    "Animal": ["animal", "veterinary", "dairy", "poultry", "livestock", "fisheries", "aquaculture", "fish", "fidf", "ahidf"],
    "Healthcare": ["health", "healthcare", "med", "medical", "pharma", "biotech", "hospital", "clinic", "rdi", "medicine"],
    "EdTech": ["edtech", "education", "school", "college", "learning", "skill", "training"],
    "Waste Management": ["waste", "recycling", "garbage", "circular", "plastic", "scrap", "pollution"],
    "AI/IoT/Robotic": ["ai", "iot", "robot", "robotic", "robotics", "machine learning", "hardware", "deeptech", "automation", "sensor"],
    "Green Energy": ["green", "clean energy", "solar", "energy", "ev", "electric vehicle", "renewable", "battery", "wind"],
    "Semiconductors": ["semiconductor", "semiconductors", "chip", "chips", "fab", "microchip"],
    "Logistic/Mobility": ["logistic", "logistics", "mobility", "transport", "freight", "fleet", "delivery", "supply chain"],
    "IT/E-Commerce": ["it", "e-commerce", "ecommerce", "software", "saas", "app", "tech", "platform"],
    "Cybersecurity": ["cyber", "cybersecurity", "security", "firewall", "infosec", "hacker"],
    "Textile": ["textile", "fabric", "garment", "apparel", "clothing", "handloom", "weaver", "cotton"],
    "Fintech": ["fintech", "finance", "banking", "payment", "nbfc", "lending", "credit"],
    "Defence": ["defence", "defense", "military", "aerospace", "army", "navy", "airforce", "drdo"],
    "Construction": ["construction", "infra", "infrastructure", "real estate", "cement", "building"],

    # States
    "Tamil Nadu": ["tamil nadu", "tamilnadu", "chennai", "tn", "coimbatore", "madurai"],
    "Kerala": ["kerala", "cochin", "kochi", "thiruvananthapuram", "trivandrum"],
    "Karnataka": ["karnataka", "bangalore", "bengaluru", "mysore"],
    "Telangana": ["telangana", "hyderabad", "tg"],
    "Maharashtra": ["maharashtra", "mumbai", "pune", "nagpur", "mh"],
    "Gujarat": ["gujarat", "ahmedabad", "gandhinagar", "surat", "vadodara", "rajkot", "srujan"],
    "UP": ["up", "uttar pradesh", "lucknow", "noida", "kanpur", "varanasi"],
    "MP": ["mp", "madhya pradesh", "bhopal", "indore"],
    "Bihar": ["bihar", "patna"],
    "Haryana": ["haryana", "gurgaon", "gurugram", "faridabad"],

    # Special categories
    "SC/ST/OBC": ["sc", "st", "obc", "caste", "tribal", "dalit", "scheduled caste", "scheduled tribe", "backward class"],
    "Young Entrepreneur": ["young", "youth", "student", "age", "under 25", "under 35", "teen"],
    "NGO": ["ngo", "non-profit", "nonprofit", "not-for-profit", "trust", "society", "charity"],
    "SIDBI": ["sidbi", "machinery", "working capital", "equipment", "msme unit", "plant"],
}


def find_matching_sections(text: str) -> list[str]:
    """Finds sections matching words in `text` (lowercase, word-level matching)."""
    text_lower = text.lower()
    matched = []
    for section, keywords in KEYWORD_SECTION_MAP.items():
        for kw in keywords:
            if " " in kw or "/" in kw:
                if kw in text_lower:
                    matched.append(section)
                    break
            else:
                if re.search(r"\b" + re.escape(kw) + r"\b", text_lower):
                    matched.append(section)
                    break
    return matched


def get_routed_sections(user_message: str, history: list) -> tuple[list[str], str]:
    """
    Selects relevant sections using keyword routing on current message and last 2 messages.
    Always includes 'General schemes (all sectors)'. Sends at most 3 matched sections.
    If nothing matches, sends General section + list of all section names.
    Returns (selected_section_names, knowledge_snippet).
    """
    # 1. Match current user message
    current_matches = find_matching_sections(user_message)

    # 2. Match previous 2 messages in history for follow-ups
    history_matches = []
    if isinstance(history, list) and len(history) > 0:
        history_snippet = " ".join([str(item.get("content", "")) for item in history[-2:] if isinstance(item, dict)])
        history_matches = find_matching_sections(history_snippet)

    # Combine unique matches (current message matches take priority)
    combined = []
    for sec in current_matches:
        if sec not in combined:
            combined.append(sec)
    for sec in history_matches:
        if sec not in combined:
            combined.append(sec)

    # Limit to at most 3 matched sections
    matched_sections = combined[:3]

    # Always include General schemes
    general_key = "General schemes (all sectors)"
    selected_sections = [general_key] + matched_sections

    # Build knowledge snippet
    if not matched_sections:
        # If nothing matches: send General section + list of all section names
        all_section_names = ", ".join([s for s in KNOWLEDGE_SECTIONS.keys() if s != general_key])
        general_content = KNOWLEDGE_SECTIONS.get(general_key, "")
        knowledge_snippet = (
            f"## {general_key}\n{general_content}\n\n"
            f"Available sections: {all_section_names}"
        )
    else:
        snippets = []
        for s in selected_sections:
            if s in KNOWLEDGE_SECTIONS:
                snippets.append(f"## {s}\n{KNOWLEDGE_SECTIONS[s]}")
        knowledge_snippet = "\n\n".join(snippets)

    return selected_sections, knowledge_snippet


# Base System Rules Template
SYSTEM_RULES_TEMPLATE = """You are a friendly funding-scheme assistant. You answer ONLY using the
KNOWLEDGE below, which comes from the document 'Funding Opportunity -
Industry Sector Wise'.

Rules:
1. Answer only from the KNOWLEDGE. Never use outside information and never
   guess or invent scheme names, amounts or eligibility.
2. Default assumption: every user message is about the funding schemes
   in the KNOWLEDGE, unless it is clearly about something else. Words
   like 'scheme', 'schema', 'skim', 'yojana', 'grant', 'loan', 'fund',
   'subsidy' and similar typos or spellings all refer to funding
   schemes. Never decline because of a typo.
3. Short or vague messages ('what is schema?', 'what is this?', 'help',
   'what can you do?', 'tell me more') are about this chatbot and its
   document. Answer briefly: explain that you help people find startup
   funding schemes, grants, loans and subsidies in India by sector,
   state, or eligibility, and give 2 or 3 example questions they can
   ask.
4. Follow-up questions ('why?', 'how?', 'and for Gujarat?', 'what about
   loans?', 'explain', 'who can apply?') must be answered using the
   previous messages in the conversation. Look at the last user and bot
   messages to understand what the user is referring to, then answer
   from the KNOWLEDGE. If the previous message was a refusal and the
   user asks 'why?', explain that you can only answer questions about
   the funding schemes in your document, and invite them to ask about
   one.
5. Simple questions about the concepts in the document are allowed and
   should be answered in 1 to 2 simple sentences, for example 'what is
   DPIIT?', 'what is a grant?', 'what is equity funding?', 'what is
   CGTMSE?', 'what does Pvt Ltd or LLP mean?', 'what is 1 Cr / 1 L?'.
   Answer these only in the context of startup funding.
6. Decline ONLY when the question is clearly unrelated to startup
   funding or this document (for example sports, politics, coding,
   recipes, medical advice, general trivia). Then reply politely: 'Sorry,
   I can only help with questions about startup funding schemes in my
   document. You can ask me about grants, loans and funds by sector,
   state, or eligibility.' Do not answer the unrelated question at all.
7. If the question is about funding schemes but the answer is not in the
   KNOWLEDGE, say: 'I couldn't find that in my document.'
8. If the question is unclear and you cannot guess the topic, ask ONE
   short clarifying question about their sector, state, entity type or
   age.
9. Greetings and small talk are fine. Reply warmly in one line and invite
   the user to ask about funding schemes.
10. When a user asks for schemes for a sector, state or entity type, list the
   matching schemes with amount and eligibility. Keep answers short and
   easy to read, using bullet points when listing several schemes.
11. Always reply in the same language the user writes in.
12. Mention that users should verify the final details with the official
   scheme provider before applying.

KNOWLEDGE:
{knowledge}"""

# 5. CACHE: In-memory dictionary for first messages (empty history)
# Note: On serverless environments (like Vercel), in-memory cache resets when function instances spin down or scale.
response_cache = {}
MAX_CACHE_ENTRIES = 200

# Initialize Flask app
# Exposes the Flask instance as a module-level variable named `app` for WSGI/Vercel
app = Flask(__name__, static_folder="public", static_url_path="")
CORS(app)

# In-memory per-IP rate limiter
# Note: On serverless environments (like Vercel), in-memory rate limits reset when function instances spin down or scale.
ip_request_history = {}


def is_ip_rate_limited(ip_address: str, limit: int = 10, window: float = 60.0) -> bool:
    """Checks if the IP has sent more than `limit` messages in `window` seconds."""
    now = time.time()
    history = ip_request_history.get(ip_address, [])
    valid_timestamps = [t for t in history if now - t < window]
    if len(valid_timestamps) >= limit:
        ip_request_history[ip_address] = valid_timestamps
        return True
    valid_timestamps.append(now)
    ip_request_history[ip_address] = valid_timestamps
    return False


def extract_retry_after(error: Exception) -> float:
    """Extracts wait time in seconds from Groq rate limit error headers or message text."""
    if hasattr(error, "response") and error.response is not None:
        headers = getattr(error.response, "headers", {})
        retry_header = headers.get("retry-after")
        if retry_header:
            try:
                return float(retry_header)
            except ValueError:
                pass

    err_str = str(error)
    match = re.search(r"try again in ([0-9]+(?:\.[0-9]+)?)s", err_str, re.IGNORECASE)
    if match:
        return float(match.group(1))

    match_sec = re.search(r"in ([0-9]+(?:\.[0-9]+)?)s", err_str, re.IGNORECASE)
    if match_sec:
        return float(match_sec.group(1))

    return 1.5


@app.route("/")
def index():
    """Serves the test host page containing the embedded widget."""
    return render_template("index.html")


@app.route("/widget.js")
def widget_js():
    """Serves the widget script at site root (matching Vercel public/ folder behavior)."""
    return send_from_directory(os.path.join(os.path.dirname(__file__), "public"), "widget.js", mimetype="application/javascript")


@app.route("/status", methods=["GET"])
def status():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def chat():
    """
    Handles chat messages with keyword routing, caching, and streaming.
    Expects JSON: {"message": "...", "history": [...]}
    Returns text/plain stream of response chunks, or 429 JSON on rate limit.
    """
    start_time = time.time()

    # 1. Check in-memory per-IP limiter
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr or "127.0.0.1").split(",")[0].strip()
    if is_ip_rate_limited(client_ip, limit=10, window=60.0):
        print(f"[IP Limiter] Exceeded limit for IP: {client_ip}", flush=True)
        return jsonify({"reply": "You're sending messages too fast. Please wait a minute and try again."}), 429

    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({"reply": "Please enter a message to begin."}), 400

    cleaned_msg = user_message.lower().strip()
    is_first_message = (not history or len(history) == 0)

    # 5. CACHE: Check cache for first messages
    if is_first_message and cleaned_msg in response_cache:
        cached_reply = response_cache[cleaned_msg]
        total_time = time.time() - start_time
        # 7. TIMING LOGS
        print(f"[Request] Cache HIT for '{cleaned_msg}' | Total time: {total_time:.4f}s", flush=True)
        return Response(cached_reply, mimetype="text/plain")

    # 2. KEYWORD ROUTING: Pick relevant sections
    selected_sections, knowledge_snippet = get_routed_sections(user_message, history)
    system_prompt = SYSTEM_RULES_TEMPLATE.format(knowledge=knowledge_snippet)
    approx_tokens = len(system_prompt) // 4

    # Build Groq message payload
    messages = [{"role": "system", "content": system_prompt}]
    if isinstance(history, list) and len(history) > 0:
        recent_history = history[-6:]
        for item in recent_history:
            if isinstance(item, dict) and "role" in item and "content" in item:
                role = "assistant" if item["role"] == "assistant" else "user"
                messages.append({"role": role, "content": str(item["content"])})
    messages.append({"role": "user", "content": user_message})

    # 4. FEWER RETRIES: 1 retry, wait max 3s
    MAX_RETRIES = 1
    stream_response = None

    for attempt in range(MAX_RETRIES + 1):
        try:
            try:
                stream_response = groq_client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=400,
                    stream=True,
                )
            except (NotFoundError, RateLimitError):
                # Fallback to fast 20b model if primary is not available or hits limit
                stream_response = groq_client.chat.completions.create(
                    model=FALLBACK_MODEL,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=400,
                    stream=True,
                )
            break
        except RateLimitError as e:
            print(f"[Groq RateLimitError] Attempt {attempt + 1}/{MAX_RETRIES + 1}: {e}", flush=True)
            if attempt < MAX_RETRIES:
                wait_time = min(extract_retry_after(e), 3.0)
                print(f"[Retry] Sleeping {wait_time:.2f}s before retry...", flush=True)
                time.sleep(wait_time)
            else:
                return jsonify({"reply": "I'm a bit busy right now, please try again in a minute."}), 429
        except Exception as e:
            print(f"[Groq Error] {e}", flush=True)
            return jsonify({"reply": "I couldn't process your request right now. Please try again."}), 500

    # 6. STREAMING: Stream response chunks via generator
    def generate():
        full_reply_parts = []
        try:
            for chunk in stream_response:
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    full_reply_parts.append(delta)
                    yield delta
        except Exception as err:
            print(f"[Streaming Chunk Error] {err}", flush=True)
            yield "\n[Error while streaming response]"

        # Complete response accounting
        full_reply = "".join(full_reply_parts).strip()
        total_time = time.time() - start_time

        # 7. TIMING LOGS
        print(f"[Request] Sections: {selected_sections} | Approx prompt tokens: {approx_tokens} | Total time: {total_time:.2f}s", flush=True)

        # 5. CACHE: Store first messages
        if is_first_message and full_reply:
            if len(response_cache) >= MAX_CACHE_ENTRIES:
                del response_cache[next(iter(response_cache))]
            response_cache[cleaned_msg] = full_reply

    return Response(stream_with_context(generate()), mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
