/**
 * Funding Scheme Assistant - Floating Chat Widget
 * Self-contained, zero-dependency widget with Shadow DOM isolation.
 * Productive, distraction-free UI without decorative gradients.
 */
(function () {
  "use strict";

  // Prevent double-initialization
  if (window.FundingChatbot && window.FundingChatbot.initialized) {
    return;
  }

  // Detect script element and configuration attributes
  const currentScript =
    document.currentScript ||
    document.querySelector('script[src*="widget.js"]') ||
    document.querySelector("script[data-api-url]");

  let apiUrl = "";
  let widgetTitle = "Funding Scheme Assistant";
  let widgetSubtitle = "Official Startup Schemes, Grants & Subsidies";
  let primaryColor = "#0f172a";
  let position = "right"; // 'right' or 'left'

  if (currentScript) {
    const customApiUrl = currentScript.getAttribute("data-api-url");
    if (customApiUrl) {
      apiUrl = customApiUrl;
    } else if (currentScript.src) {
      try {
        const parsedUrl = new URL(currentScript.src);
        apiUrl = `${parsedUrl.origin}/chat`;
      } catch (e) {
        apiUrl = "/chat";
      }
    }

    if (currentScript.getAttribute("data-title")) {
      widgetTitle = currentScript.getAttribute("data-title");
    }
    if (currentScript.getAttribute("data-color")) {
      primaryColor = currentScript.getAttribute("data-color");
    }
    if (currentScript.getAttribute("data-position")) {
      position = currentScript.getAttribute("data-position").toLowerCase();
    }
  }

  if (!apiUrl) {
    apiUrl = "/chat";
  }

  // Define global namespace
  window.FundingChatbot = {
    initialized: true,
    apiUrl: apiUrl,
    history: [],
    isOpen: false,
    toggle: null,
    open: null,
    close: null,
    reset: null
  };

  // Create Host Container for Shadow DOM
  const host = document.createElement("div");
  host.id = "funding-chatbot-host";
  host.style.position = "fixed";
  host.style.zIndex = "2147483647";
  host.style.bottom = "0";
  if (position === "left") {
    host.style.left = "0";
  } else {
    host.style.right = "0";
  }
  host.style.width = "0";
  host.style.height = "0";
  host.style.overflow = "visible";

  const shadow = host.attachShadow({ mode: "open" });

  // Widget Styles - Clean, productive, typography-first, no decorative gradients
  const style = document.createElement("style");
  style.textContent = `
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
    }

    :host {
      --fcb-primary: ${primaryColor};
      --fcb-primary-hover: #1e293b;
      --fcb-bg: #ffffff;
      --fcb-surface: #f8fafc;
      --fcb-border: #e2e8f0;
      --fcb-border-focus: #0f172a;
      --fcb-text-main: #0f172a;
      --fcb-text-muted: #64748b;
      --fcb-bot-bubble: #ffffff;
      --fcb-user-bubble: #0f172a;
    }

    /* Floating Launcher Button - Clean, professional, productive */
    .fcb-launcher {
      position: fixed;
      bottom: 22px;
      ${position === "left" ? "left: 22px;" : "right: 22px;"}
      height: 44px;
      padding: 0 16px;
      border-radius: 8px;
      background: var(--fcb-primary);
      color: #ffffff;
      border: 1px solid #1e293b;
      box-shadow: 0 4px 14px rgba(15, 23, 42, 0.16);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 500;
      transition: background 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
      z-index: 2147483647;
      outline: none;
    }

    .fcb-launcher:hover {
      background: var(--fcb-primary-hover);
      box-shadow: 0 6px 18px rgba(15, 23, 42, 0.22);
      transform: translateY(-1px);
    }

    .fcb-launcher:active {
      transform: translateY(0);
    }

    .fcb-launcher svg {
      width: 17px;
      height: 17px;
      fill: none;
      stroke: currentColor;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
      flex-shrink: 0;
    }

    .fcb-launcher.open .icon-chat,
    .fcb-launcher.open .launcher-label {
      display: none;
    }
    .fcb-launcher.open .icon-close,
    .fcb-launcher.open .launcher-close-label {
      display: inline-block;
    }

    .fcb-launcher:not(.open) .icon-chat,
    .fcb-launcher:not(.open) .launcher-label {
      display: inline-block;
    }
    .fcb-launcher:not(.open) .icon-close,
    .fcb-launcher:not(.open) .launcher-close-label {
      display: none;
    }

    /* Chat Window Container */
    .fcb-window {
      position: fixed;
      bottom: 78px;
      ${position === "left" ? "left: 22px;" : "right: 22px;"}
      width: 390px;
      max-width: calc(100vw - 28px);
      height: 560px;
      max-height: calc(100vh - 96px);
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.18), 0 4px 10px -2px rgba(15, 23, 42, 0.08);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      z-index: 2147483646;
      opacity: 0;
      transform: translateY(8px);
      pointer-events: none;
      transition: opacity 0.15s ease, transform 0.15s ease;
    }

    .fcb-window.active {
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }

    /* Header */
    .fcb-header {
      padding: 12px 14px;
      background: #0f172a;
      border-bottom: 1px solid #1e293b;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      flex-shrink: 0;
    }

    .fcb-header-info {
      display: flex;
      align-items: center;
      gap: 10px;
      overflow: hidden;
    }

    .fcb-avatar {
      width: 30px;
      height: 30px;
      border-radius: 6px;
      background: #1e293b;
      border: 1px solid #334155;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #f8fafc;
      flex-shrink: 0;
    }

    .fcb-avatar svg {
      width: 16px;
      height: 16px;
      fill: none;
      stroke: currentColor;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    .fcb-header-text h3 {
      font-size: 0.88rem;
      font-weight: 600;
      color: #ffffff;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .fcb-status-dot {
      display: inline-block;
      width: 6px;
      height: 6px;
      background: #10b981;
      border-radius: 50%;
    }

    .fcb-header-text p {
      font-size: 0.72rem;
      color: #94a3b8;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .fcb-header-actions {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .fcb-header-btn {
      background: transparent;
      border: 1px solid transparent;
      color: #94a3b8;
      cursor: pointer;
      padding: 5px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s ease;
    }

    .fcb-header-btn:hover {
      background: #1e293b;
      color: #ffffff;
      border-color: #334155;
    }

    /* Message Area */
    .fcb-messages {
      flex: 1;
      padding: 14px;
      background: #f8fafc;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .fcb-messages::-webkit-scrollbar {
      width: 4px;
    }
    .fcb-messages::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 2px;
    }

    .fcb-msg-row {
      display: flex;
      width: 100%;
    }

    .fcb-msg-row.user {
      justify-content: flex-end;
    }

    .fcb-msg-row.bot {
      justify-content: flex-start;
    }

    .fcb-bubble {
      max-width: 88%;
      padding: 10px 13px;
      border-radius: 8px;
      font-size: 0.85rem;
      line-height: 1.5;
      word-break: break-word;
    }

    .fcb-msg-row.user .fcb-bubble {
      background: #0f172a;
      color: #ffffff;
      border: 1px solid #1e293b;
    }

    .fcb-msg-row.bot .fcb-bubble {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      color: #0f172a;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }

    .fcb-bubble p {
      margin-bottom: 6px;
    }
    .fcb-bubble p:last-child {
      margin-bottom: 0;
    }
    .fcb-bubble ul {
      margin: 6px 0 6px 18px;
    }
    .fcb-bubble li {
      margin-bottom: 4px;
    }
    .fcb-msg-row.user .fcb-bubble strong {
      color: #ffffff;
    }
    .fcb-msg-row.bot .fcb-bubble strong {
      color: #0f172a;
      font-weight: 600;
    }

    /* Suggestion Chips - Clean functional search buttons */
    .fcb-chips-container {
      margin-top: 8px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .fcb-chip {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      color: #334155;
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 500;
      text-align: left;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }

    .fcb-chip:hover {
      background: #f1f5f9;
      border-color: #94a3b8;
      color: #0f172a;
    }

    .fcb-chip svg {
      width: 13px;
      height: 13px;
      fill: none;
      stroke: currentColor;
      stroke-width: 2;
      flex-shrink: 0;
      color: #64748b;
    }

    /* Typing Indicator */
    .fcb-typing {
      display: none;
      align-items: center;
      gap: 4px;
      padding: 8px 12px;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      width: fit-content;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    }

    .fcb-typing span {
      font-size: 0.76rem;
      color: #64748b;
      margin-right: 4px;
    }

    .fcb-dot {
      width: 5px;
      height: 5px;
      background: #94a3b8;
      border-radius: 50%;
      animation: fcbBlink 1.2s infinite both;
    }
    .fcb-dot:nth-child(2) { animation-delay: 0.2s; }
    .fcb-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes fcbBlink {
      0%, 80%, 100% { opacity: 0.3; }
      40% { opacity: 1; }
    }

    /* Input Footer */
    .fcb-footer {
      padding: 10px 12px;
      background: #ffffff;
      border-top: 1px solid #e2e8f0;
      flex-shrink: 0;
    }

    .fcb-form {
      display: flex;
      gap: 6px;
    }

    .fcb-input {
      flex: 1;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 8px 12px;
      font-size: 0.85rem;
      color: #0f172a;
      outline: none;
      transition: border-color 0.15s, background 0.15s;
    }

    .fcb-input:focus {
      background: #ffffff;
      border-color: #0f172a;
    }

    .fcb-input::placeholder {
      color: #94a3b8;
    }

    .fcb-send-btn {
      background: #0f172a;
      border: 1px solid #0f172a;
      color: #ffffff;
      width: 36px;
      height: 36px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: background 0.15s, border-color 0.15s;
      flex-shrink: 0;
    }

    .fcb-send-btn:hover:not(:disabled) {
      background: #1e293b;
      border-color: #1e293b;
    }

    .fcb-send-btn:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }

    .fcb-send-btn svg {
      width: 15px;
      height: 15px;
      fill: none;
      stroke: currentColor;
      stroke-width: 2.2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    .fcb-footer-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 6px;
      padding: 0 2px;
      font-size: 0.69rem;
      color: #94a3b8;
    }

    .fcb-hint {
      font-size: 0.72rem;
      color: #b45309;
      font-weight: 500;
    }

    /* Responsive */
    @media (max-width: 480px) {
      .fcb-window {
        width: calc(100vw - 20px);
        height: calc(100vh - 90px);
        bottom: 74px;
        right: 10px;
        left: 10px;
        max-width: none;
        max-height: none;
      }
      .fcb-launcher {
        bottom: 16px;
        ${position === "left" ? "left: 16px;" : "right: 16px;"}
      }
    }
  `;

  shadow.appendChild(style);

  // Widget Markup - Productive, semantic, clean
  const container = document.createElement("div");
  container.innerHTML = `
    <!-- Launcher Button -->
    <button class="fcb-launcher" id="fcb-launcher" aria-label="Toggle Funding Scheme Assistant">
      <svg class="icon-chat" viewBox="0 0 24 24">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
      </svg>
      <span class="launcher-label">Ask Schemes</span>
      <svg class="icon-close" viewBox="0 0 24 24">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
      </svg>
      <span class="launcher-close-label">Close</span>
    </button>

    <!-- Chat Window -->
    <div class="fcb-window" id="fcb-window">
      <div class="fcb-header">
        <div class="fcb-header-info">
          <div class="fcb-avatar" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
          </div>
          <div class="fcb-header-text">
            <h3>
              <span>${widgetTitle}</span>
              <span class="fcb-status-dot" title="Active"></span>
            </h3>
            <p>${widgetSubtitle}</p>
          </div>
        </div>
        <div class="fcb-header-actions">
          <button class="fcb-header-btn" id="fcb-reset-btn" title="New conversation / Clear chat" aria-label="Clear chat">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="1 4 1 10 7 10"></polyline>
              <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path>
            </svg>
          </button>
          <button class="fcb-header-btn" id="fcb-close-btn" title="Close" aria-label="Close Chat">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>

      <div class="fcb-messages" id="fcb-messages">
        <!-- Default Bot Welcome Message -->
        <div class="fcb-msg-row bot">
          <div class="fcb-bubble">
            <p>Welcome. Ask about Indian startup funding schemes, grants, subsidies, and state-wise opportunities from the official document.</p>
            <div class="fcb-chips-container" id="fcb-chips">
              <button class="fcb-chip" data-query="Schemes for Agri-Tech startups">
                <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                Schemes for Agri-Tech startups
              </button>
              <button class="fcb-chip" data-query="Funding available in Gujarat">
                <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                Funding available in Gujarat
              </button>
              <button class="fcb-chip" data-query="Loans for SC/ST entrepreneurs">
                <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                Loans for SC/ST entrepreneurs
              </button>
            </div>
          </div>
        </div>

        <!-- Typing Indicator Row -->
        <div class="fcb-msg-row bot" id="fcb-typing-row" style="display: none;">
          <div class="fcb-typing" style="display: flex;">
            <span>Consulting document</span>
            <div class="fcb-dot"></div>
            <div class="fcb-dot"></div>
            <div class="fcb-dot"></div>
          </div>
        </div>
      </div>

      <div class="fcb-footer">
        <form class="fcb-form" id="fcb-form">
          <input 
            type="text" 
            class="fcb-input" 
            id="fcb-input" 
            placeholder="Ask about schemes, grants, sectors or states..." 
            autocomplete="off"
          />
          <button type="submit" class="fcb-send-btn" id="fcb-send-btn" aria-label="Send Message" title="Send (Enter)">
            <svg viewBox="0 0 24 24">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </form>
        <div class="fcb-footer-meta">
          <span>Official Scheme Documentation</span>
          <span class="fcb-hint" id="fcb-hint" style="display: none;">Please wait...</span>
        </div>
      </div>
    </div>
  `;

  shadow.appendChild(container);

  // Append Host to Document
  function mount() {
    if (document.body) {
      document.body.appendChild(host);
    } else {
      document.addEventListener("DOMContentLoaded", () => {
        document.body.appendChild(host);
      });
    }
  }
  mount();

  // Element Selectors in Shadow DOM
  const launcher = shadow.getElementById("fcb-launcher");
  const chatWindow = shadow.getElementById("fcb-window");
  const closeBtn = shadow.getElementById("fcb-close-btn");
  const resetBtn = shadow.getElementById("fcb-reset-btn");
  const messagesBox = shadow.getElementById("fcb-messages");
  const form = shadow.getElementById("fcb-form");
  const input = shadow.getElementById("fcb-input");
  const sendBtn = shadow.getElementById("fcb-send-btn");
  const typingRow = shadow.getElementById("fcb-typing-row");
  const chipsContainer = shadow.getElementById("fcb-chips");
  const hintEl = shadow.getElementById("fcb-hint");

  let isRateLimited = false;

  // Toggle Functionality
  function toggleWidget() {
    window.FundingChatbot.isOpen = !window.FundingChatbot.isOpen;
    if (window.FundingChatbot.isOpen) {
      chatWindow.classList.add("active");
      launcher.classList.add("open");
      setTimeout(() => {
        if (!isRateLimited) input.focus();
      }, 150);
    } else {
      chatWindow.classList.remove("active");
      launcher.classList.remove("open");
    }
  }

  function openWidget() {
    if (!window.FundingChatbot.isOpen) toggleWidget();
  }

  function closeWidget() {
    if (window.FundingChatbot.isOpen) toggleWidget();
  }

  function resetChat() {
    window.FundingChatbot.history = [];
    // Clear messages except welcome bubble and typing row
    const userRows = messagesBox.querySelectorAll(".fcb-msg-row:not(:first-child):not(#fcb-typing-row)");
    userRows.forEach(row => row.remove());
    if (chipsContainer) {
      chipsContainer.style.display = "flex";
    }
    input.value = "";
    input.focus();
  }

  window.FundingChatbot.toggle = toggleWidget;
  window.FundingChatbot.open = openWidget;
  window.FundingChatbot.close = closeWidget;
  window.FundingChatbot.reset = resetChat;

  launcher.addEventListener("click", toggleWidget);
  closeBtn.addEventListener("click", closeWidget);
  if (resetBtn) resetBtn.addEventListener("click", resetChat);

  // Markdown renderer for bot messages
  function renderMarkdown(text) {
    let safe = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    const lines = safe.split("\n");
    let inList = false;
    const formatted = [];

    for (let line of lines) {
      const trimmed = line.trim();
      if (trimmed.startsWith("* ") || trimmed.startsWith("- ") || trimmed.startsWith("• ")) {
        if (!inList) {
          formatted.push("<ul>");
          inList = true;
        }
        const item = trimmed.replace(/^(\*|-|•)\s+/, "");
        formatted.push(`<li>${item}</li>`);
      } else {
        if (inList) {
          formatted.push("</ul>");
          inList = false;
        }
        if (trimmed.length > 0) {
          formatted.push(`<p>${line}</p>`);
        } else {
          formatted.push("<br>");
        }
      }
    }

    if (inList) formatted.push("</ul>");
    return formatted.join("");
  }

  function scrollToBottom() {
    messagesBox.scrollTop = messagesBox.scrollHeight;
  }

  function appendMessage(role, text) {
    const row = document.createElement("div");
    row.className = `fcb-msg-row ${role}`;

    const bubble = document.createElement("div");
    bubble.className = "fcb-bubble";

    if (role === "bot") {
      bubble.innerHTML = renderMarkdown(text);
    } else {
      bubble.textContent = text;
    }

    row.appendChild(bubble);
    messagesBox.insertBefore(row, typingRow);
    scrollToBottom();
  }

  function createBotBubble() {
    const row = document.createElement("div");
    row.className = "fcb-msg-row bot";

    const bubble = document.createElement("div");
    bubble.className = "fcb-bubble";

    row.appendChild(bubble);
    messagesBox.insertBefore(row, typingRow);
    scrollToBottom();
    return bubble;
  }

  function triggerRateLimitCooldown(seconds = 10) {
    isRateLimited = true;
    sendBtn.disabled = true;
    input.disabled = true;
    hintEl.style.display = "inline";
    hintEl.textContent = `Rate limited (${seconds}s)...`;

    let remaining = seconds;
    const cooldownTimer = setInterval(() => {
      remaining--;
      if (remaining > 0) {
        hintEl.textContent = `Wait (${remaining}s)...`;
      } else {
        clearInterval(cooldownTimer);
        isRateLimited = false;
        hintEl.style.display = "none";
        sendBtn.disabled = false;
        input.disabled = false;
        input.focus();
      }
    }, 1000);
  }

  // Handle Send with Streaming Response
  async function sendMessage(text) {
    const trimmed = text.trim();
    if (!trimmed || isRateLimited) return;

    if (chipsContainer) {
      chipsContainer.style.display = "none";
    }

    appendMessage("user", trimmed);

    input.value = "";
    input.disabled = true;
    sendBtn.disabled = true;
    typingRow.style.display = "flex";
    scrollToBottom();

    // Send last 6 messages of history (both user and bot messages)
    const recentHistory = window.FundingChatbot.history.slice(-6);

    try {
      const res = await fetch(window.FundingChatbot.apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: trimmed,
          history: recentHistory
        })
      });

      if (res.status === 429) {
        // Rate limit hit
        let reply = "I'm a bit busy right now, please try again in a minute.";
        try {
          const data = await res.json();
          if (data && data.reply) reply = data.reply;
        } catch (e) {}
        typingRow.style.display = "none";
        appendMessage("bot", reply);
        triggerRateLimitCooldown(10);
        return;
      }

      if (!res.ok) {
        let errorReply = "Something went wrong, please try again.";
        try {
          const data = await res.json();
          if (data && data.reply) errorReply = data.reply;
        } catch (e) {}
        typingRow.style.display = "none";
        appendMessage("bot", errorReply);
        return;
      }

      // Stream response using getReader()
      if (res.body && res.body.getReader) {
        const reader = res.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let fullReply = "";
        let bubbleCreated = false;
        let botBubbleEl = null;

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value, { stream: true });
          if (chunk) {
            if (!bubbleCreated) {
              // Hide typing indicator when first chunk arrives
              typingRow.style.display = "none";
              botBubbleEl = createBotBubble();
              bubbleCreated = true;
            }
            fullReply += chunk;
            botBubbleEl.innerHTML = renderMarkdown(fullReply);
            scrollToBottom();
          }
        }

        if (!bubbleCreated) {
          typingRow.style.display = "none";
          appendMessage("bot", "No response received.");
        } else {
          window.FundingChatbot.history.push({ role: "user", content: trimmed });
          window.FundingChatbot.history.push({ role: "assistant", content: fullReply });
        }
      } else {
        // Fallback for non-streaming environments
        const reply = await res.text();
        typingRow.style.display = "none";
        appendMessage("bot", reply);
        window.FundingChatbot.history.push({ role: "user", content: trimmed });
        window.FundingChatbot.history.push({ role: "assistant", content: reply });
      }

    } catch (err) {
      typingRow.style.display = "none";
      appendMessage("bot", "Something went wrong connecting to the assistant. Please try again.");
    } finally {
      if (!isRateLimited) {
        input.disabled = false;
        sendBtn.disabled = false;
        input.focus();
      }
      scrollToBottom();
    }
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    sendMessage(input.value);
  });

  // Example Chips Click
  shadow.addEventListener("click", (e) => {
    const chipBtn = e.target.closest(".fcb-chip");
    if (chipBtn) {
      const query = chipBtn.getAttribute("data-query");
      if (query && !isRateLimited) {
        sendMessage(query);
      }
    }
  });

})();
