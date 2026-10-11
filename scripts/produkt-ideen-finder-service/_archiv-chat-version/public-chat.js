/* =============================================================
   Produkt-Ideen-Finder — Frontend Chat Logic
   =============================================================
   3 Screens: landing → chat → done
   Backend: POST /api/chat (Claude-Proxy) · POST /api/lead (AC-Capture)

   Inline-Marker im Bot-Output (vom System-Prompt gesetzt):
   - [[BUTTON: Label | value]]  → Click-Button
   - [[PITCH: minikurs]]        → Pitch-Karte 39er
   - [[DONE]]                   → schliesst Tool ab, zeigt Done-Screen
   ============================================================= */

/* ⬇️⬇️⬇️  PATRICIA: HIER den echten ThriveCart-Link des 39er-Kurses eintragen  ⬇️⬇️⬇️ */
const MINIKURS_URL = 'https://mumlifebalance.thrivecart.com/eigene-produkterstellung/';
/* ⬆️⬆️⬆️  ------------------------------------------------------------------  ⬆️⬆️⬆️ */

const API = { chat: '/api/chat', lead: '/api/lead' };

const PITCHES = {
  minikurs: {
    title: '💸 Vom Network-Wissen zum eigenen Produkt',
    price: '39 CHF',
    url: MINIKURS_URL,
    tag: 'minikurs',
  },
};

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// ============================================================
// State
// ============================================================

const state = {
  user: { name: '', email: '' },
  messages: [],
  isThinking: false,
  completed: false,
  leadSent: false,
};

// ============================================================
// DOM refs
// ============================================================

const $landing = document.getElementById('screen-landing');
const $chatScreen = document.getElementById('screen-chat');
const $doneScreen = document.getElementById('screen-done');
const $messages = document.getElementById('chat-messages');
const $typing = document.getElementById('chat-typing');
const $form = document.getElementById('chat-form');
const $input = document.getElementById('chat-input');
const $send = document.getElementById('chat-send');
const $btnStart = document.getElementById('btn-start');
const $doneMinikurs = document.getElementById('done-minikurs');

// ============================================================
// localStorage — Chat-Verlauf persistieren
// ============================================================

const STORAGE_KEY = 'produktIdeenFinder:state';
const STORAGE_VERSION = 1;
const STORAGE_MAX_AGE = 1000 * 60 * 60 * 24 * 30; // 30 Tage

function storageKeyFor(email) {
  return email ? `${STORAGE_KEY}:${email.toLowerCase()}` : STORAGE_KEY;
}

function saveState() {
  if (state.completed) {
    try { localStorage.removeItem(storageKeyFor(state.user.email)); } catch {}
    return;
  }
  try {
    localStorage.setItem(storageKeyFor(state.user.email), JSON.stringify({
      v: STORAGE_VERSION, savedAt: Date.now(),
      user: state.user, messages: state.messages, leadSent: state.leadSent,
    }));
  } catch (err) { console.warn('localStorage save failed:', err); }
}

function loadState() {
  try {
    const key = storageKeyFor(state.user.email);
    const raw = localStorage.getItem(key);
    if (!raw) return false;
    const data = JSON.parse(raw);
    if (data.v !== STORAGE_VERSION) { localStorage.removeItem(key); return false; }
    if (Date.now() - data.savedAt > STORAGE_MAX_AGE) { localStorage.removeItem(key); return false; }
    if (!Array.isArray(data.messages) || data.messages.length === 0) return false;
    state.user = { ...state.user, ...data.user };
    state.messages = data.messages;
    state.leadSent = !!data.leadSent;
    return true;
  } catch { return false; }
}

// ============================================================
// Init
// ============================================================

function init() {
  const params = new URLSearchParams(window.location.search);
  state.user.email = params.get('e') || params.get('email') || '';
  state.user.name = params.get('n') || params.get('name') || '';

  if ($doneMinikurs) $doneMinikurs.href = MINIKURS_URL;

  $btnStart.addEventListener('click', startChat);
  $form.addEventListener('submit', handleSubmit);
  $input.addEventListener('input', autosizeInput);
  $input.addEventListener('keydown', handleInputKeydown);

  const hasSavedState = loadState();
  if (hasSavedState) {
    $landing.hidden = true;
    $chatScreen.hidden = false;
    renderSavedMessages();
    setTimeout(() => $input.focus(), 300);
  }
}

function renderSavedMessages() {
  if (new URLSearchParams(window.location.search).has('reset')) {
    try { localStorage.removeItem(storageKeyFor(state.user.email)); } catch {}
    window.location.href = window.location.pathname;
    return;
  }
  state.messages.forEach((msg) => {
    const el = document.createElement('div');
    el.className = `msg msg--${msg.role === 'user' ? 'user' : 'bot'}`;
    if (msg.role === 'assistant') { el.innerHTML = renderBotContent(msg.content); attachInlineHandlers(el); }
    else { el.textContent = msg.content; }
    $messages.appendChild(el);
  });
  scrollToBottom();

  const lastMsg = state.messages[state.messages.length - 1];
  if (lastMsg?.role === 'user') { setTimeout(() => sendToBotWithRetry(), 600); return; }

  const resumeEl = document.createElement('div');
  resumeEl.className = 'msg msg--bot';
  resumeEl.style.opacity = '0.7';
  resumeEl.style.fontSize = '14px';
  resumeEl.innerHTML = '<em>💡 Willkommen zurück — wir machen hier weiter. Wenn du von vorne starten willst, lade die Seite mit <code>?reset</code> am Ende der URL neu.</em>';
  $messages.appendChild(resumeEl);
}

// ============================================================
// Screen-Wechsel
// ============================================================

function startChat() {
  $landing.hidden = true;
  $chatScreen.hidden = false;
  sendInitialBotMessage();
  setTimeout(() => $input.focus(), 300);
}

function showDoneScreen() {
  state.completed = true;
  if (state.user.email) fireLead(); // Safety: falls E-Mail per URL kam
  saveState();
  setTimeout(() => {
    $chatScreen.hidden = true;
    $doneScreen.hidden = false;
    scrollToBottom();
  }, 1200);
}

// ============================================================
// Initial Bot-Message
// ============================================================

async function sendInitialBotMessage() {
  setThinking(true);
  try {
    const reply = await callChatAPI([{
      role: 'user',
      content: `__INIT__ User heisst: ${state.user.name || '(unbekannt)'}. E-Mail: ${state.user.email || '(unbekannt)'}. Bitte begrüsse sie herzlich, erklär in 1–2 Sätzen was kommt (ca. 5 Min, am Ende hält sie ihre erste eigene Produktidee in der Hand) und starte mit dem ersten Schritt (ihr Network).`,
    }]);
    addMessage('assistant', reply);
    if (reply.includes('[[DONE]]')) showDoneScreen();
  } catch (err) {
    addMessage('assistant', '💡 Hey! Ich hab gerade einen kleinen technischen Schluckauf. Probier bitte in ein paar Sekunden nochmal oder lade die Seite neu.');
    console.error(err);
  } finally { setThinking(false); }
}

// ============================================================
// User sendet Message
// ============================================================

async function handleSubmit(e) {
  e.preventDefault();
  if (state.isThinking || state.completed) return;
  const text = $input.value.trim();
  if (!text) return;

  $input.value = '';
  autosizeInput();
  addMessage('user', text);

  // E-Mail erkennen → Lead-Capture (einmalig)
  if (!state.user.email && EMAIL_RE.test(text)) {
    state.user.email = text;
    saveState();
    fireLead();
  }

  await sendToBotWithRetry();
}

async function sendToBotWithRetry(autoRetried = false) {
  setThinking(true);
  try {
    const reply = await callChatAPI(state.messages);
    addMessage('assistant', reply);
    if (reply.includes('[[DONE]]')) showDoneScreen();
  } catch (err) {
    console.error('Bot-Fehler:', err);
    if (!autoRetried && err.retryable !== false) {
      await new Promise((r) => setTimeout(r, 1500));
      return sendToBotWithRetry(true);
    }
    addRetryMessage();
  } finally { setThinking(false); }
}

function addRetryMessage() {
  const el = document.createElement('div');
  el.className = 'msg msg--bot msg--retry';
  el.innerHTML = `
    <p>💡 Mein Bot hat kurz den Faden verloren — passiert manchmal. Deine Antwort ist gespeichert, du musst nichts neu tippen.</p>
    <div class="msg__buttons">
      <button class="msg__button" data-action="retry">🔄 Nochmal probieren</button>
    </div>`;
  el.querySelector('button[data-action="retry"]').addEventListener('click', () => {
    el.remove();
    sendToBotWithRetry();
  });
  $messages.appendChild(el);
  scrollToBottom();
}

function handleInputKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); $form.requestSubmit(); }
}

function handleButtonClick(value) {
  if (state.isThinking || state.completed) return;
  addMessage('user', value);
  sendToBotWithRetry();
}

// ============================================================
// API calls
// ============================================================

async function callChatAPI(messages) {
  const cleanMessages = messages.map((m) => ({
    role: m.role,
    content: m.content.replace(/\[\[DONE\]\]/g, '').trim(),
  }));

  const res = await fetch(API.chat, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages: cleanMessages, user: state.user }),
  });

  if (!res.ok) {
    let payload = null;
    try { payload = await res.json(); } catch {}
    const err = new Error(payload?.error || `Chat API ${res.status}`);
    err.status = res.status;
    err.retryable = payload?.retryable !== false;
    throw err;
  }
  const data = await res.json();
  return data.text || data.message || '';
}

async function fireLead() {
  if (state.leadSent || !state.user.email) return;
  state.leadSent = true;
  saveState();
  try {
    await fetch(API.lead, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: state.user.email, name: state.user.name }),
    });
  } catch (err) {
    console.warn('Lead-Capture fehlgeschlagen (nicht kritisch):', err);
  }
}

// ============================================================
// Message-Rendering
// ============================================================

function addMessage(role, content) {
  state.messages.push({ role, content });
  saveState();

  const el = document.createElement('div');
  el.className = `msg msg--${role === 'user' ? 'user' : 'bot'}`;
  if (role === 'assistant') { el.innerHTML = renderBotContent(content); attachInlineHandlers(el); }
  else { el.textContent = content; }
  $messages.appendChild(el);
  scrollToBottom();
}

function renderBotContent(raw) {
  let text = raw.replace(/\[\[DONE\]\]/g, '').trim();

  const pitches = [];
  text = text.replace(/\[\[PITCH:\s*([a-z]+)\s*\]\]/gi, (_, key) => {
    const pitch = PITCHES[key.toLowerCase()];
    if (!pitch) return '';
    pitches.push(pitch);
    return `__PITCH_PLACEHOLDER_${pitches.length - 1}__`;
  });

  const buttons = [];
  text = text.replace(/\[\[BUTTON:\s*([^|\]]+?)\s*\|\s*([^\]]+?)\s*\]\]/gi, (_, label, value) => {
    buttons.push({ label: label.trim(), value: value.trim() });
    return `__BUTTON_PLACEHOLDER_${buttons.length - 1}__`;
  });

  let html = escapeHTML(text)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(?<!\*)\*([^*\n]+?)\*(?!\*)/g, '<em>$1</em>')
    .replace(/\n\n+/g, '</p><p>')
    .replace(/\n/g, '<br/>');
  html = `<p>${html}</p>`;

  html = html.replace(/<p>(\s*[•·-]\s+.+?)<\/p>/gs, (_, block) => {
    const items = block.split(/\n|<br\/>/).map((l) => l.replace(/^\s*[•·-]\s+/, '').trim()).filter(Boolean);
    return '<ul>' + items.map((i) => `<li>${i}</li>`).join('') + '</ul>';
  });

  buttons.forEach((btn, i) => {
    const btnHtml = `<button class="msg__button" data-value="${escapeAttr(btn.value)}">${escapeHTML(btn.label)}</button>`;
    html = html.replace(`__BUTTON_PLACEHOLDER_${i}__`, btnHtml);
  });
  if (buttons.length > 0 && !html.includes('msg__buttons')) {
    const btnRegex = /(<button class="msg__button"[^>]*>[^<]*<\/button>\s*)+/g;
    html = html.replace(btnRegex, (match) => `<div class="msg__buttons">${match}</div>`);
  }

  pitches.forEach((pitch, i) => {
    const pitchHtml = `
      <div class="msg__pitch">
        <div class="msg__pitch-title">${pitch.title}</div>
        <div class="msg__pitch-price">${pitch.price}</div>
        <a href="${pitch.url}" target="_blank" rel="noopener" class="msg__pitch-link" data-pitch="${pitch.tag}">Jetzt ansehen →</a>
      </div>`;
    html = html.replace(`__PITCH_PLACEHOLDER_${i}__`, pitchHtml);
  });

  return html;
}

function attachInlineHandlers(el) {
  el.querySelectorAll('.msg__button').forEach((btn) => {
    btn.addEventListener('click', () => { const value = btn.dataset.value; btn.disabled = true; handleButtonClick(value); });
  });
}

// ============================================================
// Helpers
// ============================================================

function escapeHTML(str) { const div = document.createElement('div'); div.textContent = str; return div.innerHTML; }
function escapeAttr(str) { return str.replace(/"/g, '&quot;'); }

function setThinking(on) {
  state.isThinking = on;
  $typing.hidden = !on;
  $send.disabled = on;
  $input.disabled = on;
  if (on) scrollToBottom();
}

function autosizeInput() {
  $input.style.height = 'auto';
  $input.style.height = Math.min($input.scrollHeight, 140) + 'px';
}

function scrollToBottom() {
  requestAnimationFrame(() => {
    $messages.scrollTop = $messages.scrollHeight;
    window.scrollTo(0, document.body.scrollHeight);
  });
}

init();
