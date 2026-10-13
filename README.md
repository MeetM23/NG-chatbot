# Funding Scheme Assistant Chatbot & Floating Widget

A minimal, high-performance AI chatbot widget that answers questions exclusively from the document **"Funding Opportunity - Industry Sector Wise"**.

Built using **Python 3 + Flask** with **CORS**, **Groq API** (`llama-3.1-8b-instant` / `openai/gpt-oss-20b`), and a zero-dependency **Shadow DOM Floating Chat Widget** (`public/widget.js`) that can be embedded into any website.

---

## Project Structure

```text
NG-ChatBot/
  app.py                     # Flask backend with CORS, routing, and Groq streaming logic
  knowledge.md               # Sectioned knowledge base bundled with serverless function
  prepare_knowledge.py       # One-time extraction script using pypdf
  requirements.txt           # Runtime dependencies (flask, flask-cors, groq, python-dotenv)
  vercel.json                # Vercel deployment configuration
  .env                       # Local environment settings (GROQ_API_KEY, GROQ_MODEL)
  .gitignore                 # Git ignore file (.env, __pycache__/, venv/, .vercel/)
  README.md                  # Documentation and deployment instructions
  public/
    widget.js                # Self-contained floating chat widget (served at /widget.js)
  templates/
    index.html               # Host page embedding the widget
  data/
    Funding Opportunity - Industry Sector Wise.pdf
```

---

## Local Installation & Setup

1. **Install Python 3.10+**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Key**:
   In `.env`:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=llama-3.1-8b-instant
   ```
   *(The Groq API key is kept securely on the server and is never exposed to the client).*

4. **Verify Knowledge Base (Optional)**:
   If updating the PDF, place it in `data/` and run:
   ```bash
   python prepare_knowledge.py
   ```

5. **Start Local Flask Server**:
   ```bash
   python app.py
   ```
   The server runs at `http://127.0.0.1:5000`. Test endpoints:
   - Health check: `http://127.0.0.1:5000/status` (returns `{"status": "ok"}`)
   - Widget script: `http://127.0.0.1:5000/widget.js`
   - Test portal: `http://127.0.0.1:5000/`

---

## Deploy to Vercel

The application is pre-configured for seamless serverless deployment using `vercel.json`.

### Steps:

1. **Push your code to GitHub / GitLab / Bitbucket**:
   Ensure `.env`, `venv/`, and `.vercel/` are excluded by `.gitignore`.

2. **Import Project to Vercel**:
   - Go to [vercel.com](https://vercel.com) and click **"Add New Project"**.
   - Select your Git repository.
   - Framework Preset: Leave as **Other** (Vercel automatically detects `vercel.json` and Python).

3. **Add Environment Variables**:
   In the Vercel project configuration screen (under **Environment Variables**), add:
   - `GROQ_API_KEY`: Your secret Groq API key (Required).
   - `GROQ_MODEL`: `llama-3.1-8b-instant` (Optional, defaults to `llama-3.1-8b-instant`).

4. **Deploy**:
   - Click **Deploy**.
   - Vercel will bundle `knowledge.md` alongside `app.py` and serve static files from `public/` (including `/widget.js`) at the root domain.

5. **Serverless Behavior Note**:
   The in-memory cache and per-IP rate limiter are preserved in `app.py`. Note that on serverless platforms like Vercel, in-memory states reset whenever serverless function instances spin down or scale across regions.

---

## How to add the chatbot to any website

You can embed this chatbot as a floating widget in the bottom-right corner of any website (regardless of framework, tech stack, port, or whether it runs on VS Code Live Server on port 5500, Next.js, WordPress, or plain HTML).

### 1. Paste the script tag before `</body>`

#### For Local Testing:
```html
<script src="http://127.0.0.1:5000/widget.js" data-api-url="http://127.0.0.1:5000/chat"></script>
```

#### For Production (Vercel):
```html
<script src="https://your-app.vercel.app/widget.js" data-api-url="https://your-app.vercel.app/chat"></script>
```

*(If the widget is embedded on the same domain as the Vercel deployment, you can omit `data-api-url` and it will automatically default to `/chat`).*

---

## Widget Customization Options

The widget supports optional data attributes on its script tag:

| Attribute | Default | Description |
|---|---|---|
| `data-api-url` | Script origin + `/chat` | The endpoint URL to send chat messages to |
| `data-title` | `"Funding Scheme Assistant"` | Header title displayed in the chat window |
| `data-color` | `"#0f172a"` (slate-900) | Primary brand color for launcher button & user bubbles |
| `data-position` | `"right"` | Corner position (`"right"` or `"left"`) |

Example with custom settings:
```html
<script 
  src="https://your-app.vercel.app/widget.js" 
  data-api-url="https://your-app.vercel.app/chat"
  data-title="Gov Funding Bot"
  data-color="#1e293b"
  data-position="right">
</script>
```
