/* =============================================================
   Bio-Check für Network-Mamas — Frontend Chat Logic
   =============================================================
   Der Bot läuft in 3 Screens:
   - landing:  Einstiegs-Screen mit „Los geht's"-Button
   - chat:     Chat-UI mit Bot + User-Messages
   - done:     Abschluss mit Pitch-Links + PDF-Trigger

   Backend-Endpoints (via netlify.toml gemappt):
   - POST /api/chat   → Claude-Proxy (sendet messages, kriegt Bot-Antwort)
   - POST /api/tag    → setzt AC-Tag beim Pitch-Click
   - POST /api/pdf    → generiert PDF + triggert AC-Mail-Automation

   Inline-Marker im Bot-Output (vom System-Prompt gesetzt):
   - [[BUTTON: Label | value]]         → rendert Click-Button
   - [[PITCH: thema|expertin|kundenmaschine]] → rendert Pitch-Card
   - [[DONE]]                           → schliesst Chat ab, zeigt Done-Screen
   ============================================================= */

const API = {
  chat: '/api/chat',
  tag: '/api/tag',
  pdf: '/api/pdf',
};

const PITCHES = {
  thema: {
    title: '🎯 Finde dein Thema als Network-Mama',
    price: '39 CHF',
    url: 'https://mumlifebalance.thrivecart.com/thema-finden/',
    tag: 'thema',
  },
  expertin: {
    title: '⭐ Expertin statt Verkäuferin',
    price: '97 CHF',
    url: 'https://mumlifebalance.thrivecart.com/expertin/',
    tag: 'expertin',
  },
  kundenmaschine: {
    title: '🚀 Instagram-Kundenmaschine',
    price: '333 CHF',
    url: 'https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/',
    tag: 'kundenmaschine',
  },
  insta: {
    title: '💬 Schreib Patricia auf Instagram',
    price: 'kostenlos · persönliche Antwort',
    url: 'https://instagram.com/mumlifebalance_patricia_ulmann',
    tag: 'insta',
  },
};

// ============================================================
// State
// ============================================================

const state = {
  user: { name: '', email: '' },
  messages: [], // {role: 'user'|'assistant', content: string}
  isThinking: false,
  completed: false,
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

// ============================================================
// localStorage — Chat-Verlauf persistieren
// User kann pausieren + im selben Browser spaeter weitermachen
// ============================================================

const STORAGE_KEY = 'bioCheckBot:state';
const STORAGE_VERSION = 1;
const STORAGE_MAX_AGE = 1000 * 60 * 60 * 24 * 30; // 30 Tage

function storageKeyFor(email) {
  return email ? `${STORAGE_KEY}:${email.toLowerCase()}` : STORAGE_KEY;
}

function saveState() {
  if (state.completed) {
    // Nach Abschluss: nicht mehr speichern, State aufraeumen
    try { localStorage.removeItem(storageKeyFor(state.user.email)); } catch {}
    return;
  }
  try {
    const data = {
      v: STORAGE_VERSION,
      savedAt: Date.now(),
      user: state.user,
      messages: state.messages,
    };
    localStorage.setItem(storageKeyFor(state.user.email), JSON.stringify(data));
  } catch (err) {
    console.warn('localStorage save failed:', err);
  }
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
    return true;
  } catch {
    return false;
  }
}

// ============================================================
// Init — lese Token/Email aus URL + State aus localStorage
// ============================================================

function init() {
  const params = new URLSearchParams(window.location.search);
  state.user.email = params.get('e') || params.get('email') || '';
  state.user.name = params.get('n') || params.get('name') || '';

  $btnStart.addEventListener('click', startChat);
  $form.addEventListener('submit', handleSubmit);
  $input.addEventListener('input', autosizeInput);
  $input.addEventListener('keydown', handleInputKeydown);

  // Gespeicherten Chat-Verlauf pruefen
  const hasSavedState = loadState();
  if (hasSavedState) {
    // Direkt in Chat-Screen springen + alte Messages rendern
    $landing.hidden = true;
    $chatScreen.hidden = false;
    renderSavedMessages();
    setTimeout(() => $input.focus(), 300);
  }

  // Pitch-Links auf Done-Screen mit Tag-Tracking
  document.querySelectorAll('.done__link').forEach((link) => {
    link.addEventListener('click', (e) => {
      const pitchType = link.dataset.pitch;
      if (pitchType) fireTagEvent(pitchType);
    });
  });
}

function renderSavedMessages() {
  // Reset-Option zuerst checken (verhindert dass alte Messages noch gerendert werden)
  if (new URLSearchParams(window.location.search).has('reset')) {
    try { localStorage.removeItem(storageKeyFor(state.user.email)); } catch {}
    window.location.href = window.location.pathname + (state.user.email ? `?e=${encodeURIComponent(state.user.email)}&n=${encodeURIComponent(state.user.name)}` : '');
    return;
  }

  // Saved messages direkt rendern (ohne neu zum Bot zu schicken)
  state.messages.forEach((msg) => {
    const el = document.createElement('div');
    el.className = `msg msg--${msg.role === 'user' ? 'user' : 'bot'}`;
    if (msg.role === 'assistant') {
      el.innerHTML = renderBotContent(msg.content);
      attachInlineHandlers(el);
    } else {
      el.textContent = msg.content;
    }
    $messages.appendChild(el);
  });
  scrollToBottom();

  // Edge-Case: Letzte Message ist von User → der Bot war beim Reload mitten im Antworten.
  // Automatisch wieder zum Bot schicken, damit User nicht hängt.
  const lastMsg = state.messages[state.messages.length - 1];
  if (lastMsg?.role === 'user') {
    setTimeout(() => sendToBotWithRetry(), 600);
    return; // Resume-Hinweis-Message überspringen, weil Bot direkt weitermacht
  }

  // Info-Message dass wir weitermachen
  const resumeEl = document.createElement('div');
  resumeEl.className = 'msg msg--bot';
  resumeEl.style.opacity = '0.7';
  resumeEl.style.fontSize = '14px';
  resumeEl.innerHTML = '<em>🌿 Willkommen zurück — wir machen hier weiter. Wenn du von vorne starten willst, lade die Seite mit <code>?reset</code> am Ende der URL neu.</em>';
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
  saveState(); // loescht localStorage da completed=true
  setTimeout(() => {
    $chatScreen.hidden = true;
    $doneScreen.hidden = false;
    triggerPdfSend();
  }, 1200);
}

// ============================================================
// Initial Bot-Message (Start-Nachricht vom Bot holen)
// ============================================================

async function sendInitialBotMessage() {
  setThinking(true);
  try {
    const reply = await callChatAPI([
      {
        role: 'user',
        content: `__INIT__ User heisst: ${state.user.name || '(unbekannt)'}. E-Mail: ${state.user.email || '(unbekannt)'}. Bitte begrüsse sie herzlich, erkläre kurz was kommt (5-10 Min, Schaufenster-Metapher eingebaut), und frag ob sie schon eine Bio hat (🅰) oder bei 0 startet (🅱).`,
      },
    ]);
    addMessage('assistant', reply);
  } catch (err) {
    addMessage('assistant', '🌿 Hey! Ich hab gerade Schluckauf technischer Natur. Probier bitte in ein paar Sekunden nochmal oder lade die Seite neu.');
    console.error(err);
  } finally {
    setThinking(false);
  }
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

  await sendToBotWithRetry();
}

/**
 * Schickt state.messages zum Bot. Bei Fehler:
 * - Auto-Retry 1x nach 1.5s (transient errors)
 * - Bei zweitem Fehler: Retry-Button statt unhilfreichem „Ups"
 *   → User verliert NICHTS, kann mit einem Klick nochmal probieren
 *   → State + alle Messages bleiben erhalten (im localStorage)
 */
async function sendToBotWithRetry(autoRetried = false) {
  setThinking(true);
  try {
    const reply = await callChatAPI(state.messages);
    addMessage('assistant', reply);

    if (reply.includes('[[DONE]]')) showDoneScreen();
  } catch (err) {
    console.error('Bot-Fehler:', err);

    // Auto-Retry einmal bei transientem Fehler
    if (!autoRetried && err.retryable !== false) {
      console.log('Auto-Retry in 1.5s …');
      await new Promise((r) => setTimeout(r, 1500));
      return sendToBotWithRetry(true);
    }

    // Bei finalem Fehler: Retry-Button statt verlorener Lead
    addRetryMessage();
  } finally {
    setThinking(false);
  }
}

function addRetryMessage() {
  const el = document.createElement('div');
  el.className = 'msg msg--bot msg--retry';
  el.innerHTML = `
    <p>🌿 Mein Bot hat kurz den Faden verloren — passiert manchmal. Deine Antwort ist gespeichert, du musst nichts neu tippen.</p>
    <div class="msg__buttons">
      <button class="msg__button" data-action="retry">🔄 Nochmal probieren</button>
    </div>
  `;
  el.querySelector('button[data-action="retry"]').addEventListener('click', () => {
    el.remove();
    sendToBotWithRetry();
  });
  $messages.appendChild(el);
  scrollToBottom();
}

function handleInputKeydown(e) {
  // Enter sendet, Shift+Enter = Zeilenumbruch
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    $form.requestSubmit();
  }
}

// ============================================================
// Button-Click (aus [[BUTTON: ...]])
// ============================================================

function handleButtonClick(value) {
  if (state.isThinking || state.completed) return;
  addMessage('user', value);
  sendToBotWithRetry();
}

// ============================================================
// API calls
// ============================================================

async function callChatAPI(messages) {
  // Entferne [[DONE]] Marker aus Messages, damit Claude nicht verwirrt wird
  const cleanMessages = messages.map((m) => ({
    role: m.role,
    content: m.content.replace(/\[\[DONE\]\]/g, '').trim(),
  }));

  const res = await fetch(API.chat, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages: cleanMessages,
      user: state.user,
    }),
  });

  if (!res.ok) {
    let payload = null;
    try { payload = await res.json(); } catch {}
    const err = new Error(payload?.error || `Chat API ${res.status}`);
    err.status = res.status;
    err.retryable = payload?.retryable !== false; // default: ja, Retry erlauben
    throw err;
  }
  const data = await res.json();
  return data.text || data.message || '';
}

async function fireTagEvent(pitchType) {
  if (!state.user.email) return; // Ohne E-Mail kein Tag
  try {
    await fetch(API.tag, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: state.user.email,
        pitch: pitchType,
      }),
    });
  } catch (err) {
    console.warn('Tag-Event fehlgeschlagen (nicht kritisch):', err);
  }
}

async function triggerPdfSend() {
  if (!state.user.email) return;
  try {
    await fetch(API.pdf, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: state.user.email,
        name: state.user.name,
        messages: state.messages,
      }),
    });
  } catch (err) {
    console.error('PDF-Versand fehlgeschlagen:', err);
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

  if (role === 'assistant') {
    el.innerHTML = renderBotContent(content);
    attachInlineHandlers(el);
  } else {
    el.textContent = content;
  }

  $messages.appendChild(el);
  scrollToBottom();
}

function renderBotContent(raw) {
  // 1. [[DONE]] Marker entfernen (wird separat behandelt)
  let text = raw.replace(/\[\[DONE\]\]/g, '').trim();

  // 2. [[PITCH: key]] extrahieren und durch Placeholder ersetzen
  const pitches = [];
  text = text.replace(/\[\[PITCH:\s*([a-z]+)\s*\]\]/gi, (_, key) => {
    const pitch = PITCHES[key.toLowerCase()];
    if (!pitch) return '';
    pitches.push(pitch);
    return `__PITCH_PLACEHOLDER_${pitches.length - 1}__`;
  });

  // 3. [[BUTTON: Label | value]] extrahieren und durch Placeholder ersetzen
  const buttons = [];
  text = text.replace(/\[\[BUTTON:\s*([^|\]]+?)\s*\|\s*([^\]]+?)\s*\]\]/gi, (_, label, value) => {
    buttons.push({ label: label.trim(), value: value.trim() });
    return `__BUTTON_PLACEHOLDER_${buttons.length - 1}__`;
  });

  // 4. Markdown-Light: **bold**, *italic*, Line-breaks, Bullet-Listen
  let html = escapeHTML(text)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(?<!\*)\*([^*\n]+?)\*(?!\*)/g, '<em>$1</em>')
    .replace(/\n\n+/g, '</p><p>')
    .replace(/\n/g, '<br/>');

  html = `<p>${html}</p>`;

  // Bullet-Listen (einfach)
  html = html.replace(/<p>(\s*[•·-]\s+.+?)<\/p>/gs, (_, block) => {
    const items = block
      .split(/\n|<br\/>/)
      .map((l) => l.replace(/^\s*[•·-]\s+/, '').trim())
      .filter(Boolean);
    return '<ul>' + items.map((i) => `<li>${i}</li>`).join('') + '</ul>';
  });

  // 5. Placeholder zurück-ersetzen mit echten HTML-Elementen
  buttons.forEach((btn, i) => {
    const btnHtml = `<button class="msg__button" data-value="${escapeAttr(btn.value)}">${escapeHTML(btn.label)}</button>`;
    html = html.replace(`__BUTTON_PLACEHOLDER_${i}__`, btnHtml);
  });

  if (buttons.length > 0 && !html.includes('msg__buttons')) {
    // Buttons in einen Wrapper packen am Ende, falls sie im Text verteilt stehen
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
  // Button-Clicks
  el.querySelectorAll('.msg__button').forEach((btn) => {
    btn.addEventListener('click', () => {
      const value = btn.dataset.value;
      btn.disabled = true;
      handleButtonClick(value);
    });
  });

  // Pitch-Link-Clicks (Tag-Tracking)
  el.querySelectorAll('.msg__pitch-link').forEach((link) => {
    link.addEventListener('click', () => {
      const pitch = link.dataset.pitch;
      if (pitch) fireTagEvent(pitch);
    });
  });
}

// ============================================================
// Helpers
// ============================================================

function escapeHTML(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function escapeAttr(str) {
  return str.replace(/"/g, '&quot;');
}

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

// ============================================================
// Go
// ============================================================

init();
