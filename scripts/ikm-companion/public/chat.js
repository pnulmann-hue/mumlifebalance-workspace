/* =============================================================
   Instagram-Kundenmaschine-Companion — Frontend Chat Logic
   =============================================================
   Wiederverwendete Logik aus Bio-Check-Bot. Generisch — alle
   Bot-spezifischen Strings und PITCHES werden vom /assistent-
   Skill in dieser Datei und in index.html injiziert.

   Der Bot laeuft in 3 Screens:
   - landing:  Einstiegs-Screen mit „Los geht's"-Button
   - chat:     Chat-UI mit Bot + User-Messages
   - done:     Abschluss mit Pitch-Links

   Backend-Endpoints:
   - POST /api/chat   → Claude-Proxy
   - POST /api/tag    → AC-Tag bei Pitch-Click (optional)

   Inline-Marker im Bot-Output (vom System-Prompt gesetzt):
   - [[BUTTON: Label | value]]         → rendert Click-Button
   - [[PITCH: key]]                    → rendert Pitch-Card (key aus PITCHES)
   - [[DONE]]                          → schliesst Chat ab, zeigt Done-Screen
   ============================================================= */

const API = {
  chat: '/api/chat',
  tag: '/api/tag',
};

// =============================================================
// === IKM-Telegramgruppen-Einladungs-Link (von Patricia, 2026-04-28) ====
const TELEGRAM_GROUP_URL = 'https://t.me/+s6yEn-RiXZw3Nzg8';
// === Ende ============================================================

const INSTA_URL = 'https://instagram.com/mumlifebalance_patricia_ulmann';

// =============================================================
// PITCHES — Inhalt der Pitch-Cards.
// Format: key → { title, price, url, tag }
// `tag` wird an /api/tag uebergeben und triggert AC-Automation.
// =============================================================

const PITCHES = {
  // Mitgliedschaft — Pitch-Text liefert Patricia spaeter nach.
  // Solange leitet der Link auf Insta-DM. Tag wird trotzdem in AC gesetzt.
  mitgliedschaft: {
    title: 'Umsetzerinnen-Mitgliedschaft',
    price: 'Patricia erzaehlt dir mehr — kontaktiere sie',
    url: INSTA_URL,
    tag: 'mitgliedschaft',
  },
  // Telegramgruppe — Bestandteil des IKM-Kurses, primaerer Fragen-Kanal.
  // Patricia beantwortet jeden Dienstag und Donnerstag.
  telegram: TELEGRAM_GROUP_URL
    ? {
        title: 'IKM-Telegramgruppe',
        price: 'Patricia antwortet Di + Do · andere Teilnehmerinnen lesen mit',
        url: TELEGRAM_GROUP_URL,
        tag: 'telegram',
      }
    : {
        // Fallback: Patricia hat den Link noch nicht eingetragen.
        title: 'IKM-Telegramgruppe — Link bei Patricia anfragen',
        price: 'Schreib ihr kurz auf Insta, sie schickt dir den Einladungs-Link',
        url: INSTA_URL,
        tag: 'telegram',
      },
  insta: {
    title: 'Schreib Patricia auf Instagram',
    price: 'kostenlos · persoenliche Antwort',
    url: INSTA_URL,
    tag: 'insta',
  },
};

// =============================================================
// State
// =============================================================

const state = {
  user: { name: '', email: '' },
  messages: [],
  isThinking: false,
  completed: false,
  // Vision-Feature: anhaengende Bild-Daten vor dem Senden
  // Format: { dataUrl: 'data:image/jpeg;base64,...', mediaType: 'image/jpeg' }
  pendingAttachment: null,
};

// Vision-Feature: maximale Bild-Groesse (Anthropic-Limit ~5 MB nach Base64)
const MAX_IMAGE_DIMENSION = 1568; // Pixel — Claude-Empfehlung fuer optimale Token-Effizienz
const MAX_IMAGE_BYTES = 4 * 1024 * 1024; // 4 MB nach Base64, sicherheitshalber unter 5 MB

// =============================================================
// DOM refs
// =============================================================

const $landing = document.getElementById('screen-landing');
const $chatScreen = document.getElementById('screen-chat');
const $doneScreen = document.getElementById('screen-done');
const $messages = document.getElementById('chat-messages');
const $typing = document.getElementById('chat-typing');
const $form = document.getElementById('chat-form');
const $input = document.getElementById('chat-input');
const $send = document.getElementById('chat-send');
const $btnStart = document.getElementById('btn-start');
// Vision-Feature DOM-Refs
const $fileInput = document.getElementById('chat-file-input');
const $attachBtn = document.getElementById('chat-attach');
const $attachmentPreview = document.getElementById('chat-attachment-preview');
const $attachmentThumb = document.getElementById('chat-attachment-thumb');
const $attachmentRemove = document.getElementById('chat-attachment-remove');

// =============================================================
// localStorage — Chat-Verlauf persistieren
// =============================================================

const STORAGE_KEY = 'instagram-kundenmaschine-bot:state';
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
    // Vision-Feature: Bilder NICHT im localStorage speichern (zu gross),
    // stattdessen Platzhalter-Text. Bei Resume sieht User „[Profil-Screenshot]"
    // statt das Bild — Anthropic-Conversation-Kontext geht verloren, das ist OK.
    const messagesForStorage = state.messages.map((m) => {
      if (Array.isArray(m.content)) {
        const textBlock = m.content.find((b) => b.type === 'text');
        return { role: m.role, content: '[Profil-Screenshot] ' + (textBlock?.text || '') };
      }
      return m;
    });

    const data = {
      v: STORAGE_VERSION,
      savedAt: Date.now(),
      user: state.user,
      messages: messagesForStorage,
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

// =============================================================
// Init
// =============================================================

function init() {
  const params = new URLSearchParams(window.location.search);
  state.user.email = params.get('e') || params.get('email') || '';
  state.user.name = params.get('n') || params.get('name') || '';

  $btnStart.addEventListener('click', startChat);
  $form.addEventListener('submit', handleSubmit);
  $input.addEventListener('input', autosizeInput);
  $input.addEventListener('keydown', handleInputKeydown);

  // Vision-Feature: File-Upload-Events
  $attachBtn.addEventListener('click', () => $fileInput.click());
  $fileInput.addEventListener('change', handleFileSelect);
  $attachmentRemove.addEventListener('click', clearAttachment);

  const hasSavedState = loadState();
  if (hasSavedState) {
    $landing.hidden = true;
    $chatScreen.hidden = false;
    renderSavedMessages();
    setTimeout(() => $input.focus(), 300);
  }

  // Pitch-Links auf Done-Screen mit Tag-Tracking
  document.querySelectorAll('.done__link').forEach((link) => {
    link.addEventListener('click', () => {
      const pitchType = link.dataset.pitch;
      if (pitchType) fireTagEvent(pitchType);
    });
  });
}

function renderSavedMessages() {
  if (new URLSearchParams(window.location.search).has('reset')) {
    try { localStorage.removeItem(storageKeyFor(state.user.email)); } catch {}
    window.location.href = window.location.pathname + (state.user.email ? `?e=${encodeURIComponent(state.user.email)}&n=${encodeURIComponent(state.user.name)}` : '');
    return;
  }

  state.messages.forEach((msg) => {
    const el = document.createElement('div');
    el.className = `msg msg--${msg.role === 'user' ? 'user' : 'bot'}`;
    if (msg.role === 'assistant') {
      el.innerHTML = renderBotContent(msg.content);
      attachInlineHandlers(el);
    } else if (Array.isArray(msg.content)) {
      // Multimodal user-message (sollte selten in localStorage sein, weil
      // Bilder rausgestripped werden — nur als Safety-Net)
      renderUserMessageBlocks(el, msg.content);
    } else {
      el.textContent = msg.content;
    }
    $messages.appendChild(el);
  });
  scrollToBottom();

  const lastMsg = state.messages[state.messages.length - 1];
  if (lastMsg?.role === 'user') {
    setTimeout(() => sendToBotWithRetry(), 600);
    return;
  }

  const resumeEl = document.createElement('div');
  resumeEl.className = 'msg msg--bot';
  resumeEl.style.opacity = '0.7';
  resumeEl.style.fontSize = '14px';
  resumeEl.innerHTML = '<em>Willkommen zurueck — wir machen hier weiter. Wenn du von vorne starten willst, lade die Seite mit <code>?reset</code> am Ende der URL neu.</em>';
  $messages.appendChild(resumeEl);
}

// =============================================================
// Screen-Wechsel
// =============================================================

function startChat() {
  $landing.hidden = true;
  $chatScreen.hidden = false;
  sendInitialBotMessage();
  setTimeout(() => $input.focus(), 300);
}

function showDoneScreen() {
  state.completed = true;
  saveState();
  setTimeout(() => {
    $chatScreen.hidden = true;
    $doneScreen.hidden = false;
  }, 1200);
}

// =============================================================
// Initial Bot-Message
// =============================================================

async function sendInitialBotMessage() {
  setThinking(true);
  try {
    const reply = await callChatAPI([
      {
        role: 'user',
        content: `__INIT__ User heisst: ${state.user.name || '(unbekannt)'}. E-Mail: ${state.user.email || '(unbekannt)'}. Bitte begruesse sie herzlich nach deiner Persona.`,
      },
    ]);
    addMessage('assistant', reply);
  } catch (err) {
    addMessage('assistant', 'Hey! Ich hab gerade Schluckauf technischer Natur. Probier bitte in ein paar Sekunden nochmal oder lade die Seite neu.');
    console.error(err);
  } finally {
    setThinking(false);
  }
}

// =============================================================
// User sendet Message
// =============================================================

async function handleSubmit(e) {
  e.preventDefault();
  if (state.isThinking || state.completed) return;

  const text = $input.value.trim();
  const attachment = state.pendingAttachment;

  // Mind. Text ODER Bild noetig
  if (!text && !attachment) return;

  $input.value = '';
  autosizeInput();

  if (attachment) {
    // Multimodal: content als Array mit image-block + text-block
    const userText = text || 'Hier ist mein Profil — schau dir mein Schaufenster an und sag mir die drei groessten Hebel.';
    const base64Data = attachment.dataUrl.split(',')[1]; // strip „data:image/...;base64,"
    addMessage('user', [
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: attachment.mediaType,
          data: base64Data,
        },
      },
      { type: 'text', text: userText },
    ]);
    clearAttachment();
  } else {
    addMessage('user', text);
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
      console.log('Auto-Retry in 1.5s …');
      await new Promise((r) => setTimeout(r, 1500));
      return sendToBotWithRetry(true);
    }

    addRetryMessage();
  } finally {
    setThinking(false);
  }
}

function addRetryMessage() {
  const el = document.createElement('div');
  el.className = 'msg msg--bot msg--retry';
  el.innerHTML = `
    <p>Mein Bot hat kurz den Faden verloren — passiert manchmal. Deine Antwort ist gespeichert, du musst nichts neu tippen.</p>
    <div class="msg__buttons">
      <button class="msg__button" data-action="retry">Nochmal probieren</button>
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
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    $form.requestSubmit();
  }
}

function handleButtonClick(value) {
  if (state.isThinking || state.completed) return;
  addMessage('user', value);
  sendToBotWithRetry();
}

// =============================================================
// API calls
// =============================================================

async function callChatAPI(messages) {
  // Bei String-Content: [[DONE]] entfernen. Bei Array-Content (multimodal): durchreichen.
  const cleanMessages = messages.map((m) => {
    if (typeof m.content === 'string') {
      return { role: m.role, content: m.content.replace(/\[\[DONE\]\]/g, '').trim() };
    }
    return { role: m.role, content: m.content };
  });

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
    err.retryable = payload?.retryable !== false;
    throw err;
  }
  const data = await res.json();
  return data.text || data.message || '';
}

async function fireTagEvent(pitchType) {
  if (!state.user.email) return;
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

// =============================================================
// Message-Rendering
// =============================================================

function addMessage(role, content) {
  state.messages.push({ role, content });
  saveState();

  const el = document.createElement('div');
  el.className = `msg msg--${role === 'user' ? 'user' : 'bot'}`;

  if (role === 'assistant') {
    el.innerHTML = renderBotContent(content);
    attachInlineHandlers(el);
  } else if (Array.isArray(content)) {
    // Multimodal user-message: image-block + text-block
    renderUserMessageBlocks(el, content);
  } else {
    el.textContent = content;
  }

  $messages.appendChild(el);
  scrollToBottom();
}

// Vision-Feature: rendert eine User-Message mit image+text-Blocks
function renderUserMessageBlocks(el, content) {
  content.forEach((block) => {
    if (block.type === 'image') {
      const img = document.createElement('img');
      img.className = 'msg__image';
      img.src = `data:${block.source.media_type};base64,${block.source.data}`;
      img.alt = 'Profil-Screenshot';
      el.appendChild(img);
    } else if (block.type === 'text') {
      const p = document.createElement('div');
      p.textContent = block.text;
      el.appendChild(p);
    }
  });
}

function renderBotContent(raw) {
  let text = raw.replace(/\[\[DONE\]\]/g, '').trim();

  const pitches = [];
  text = text.replace(/\[\[PITCH:\s*([a-z_]+)\s*\]\]/gi, (_, key) => {
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
    const items = block
      .split(/\n|<br\/>/)
      .map((l) => l.replace(/^\s*[•·-]\s+/, '').trim())
      .filter(Boolean);
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
    btn.addEventListener('click', () => {
      const value = btn.dataset.value;
      btn.disabled = true;
      handleButtonClick(value);
    });
  });

  el.querySelectorAll('.msg__pitch-link').forEach((link) => {
    link.addEventListener('click', () => {
      const pitch = link.dataset.pitch;
      if (pitch) fireTagEvent(pitch);
    });
  });
}

// =============================================================
// Helpers
// =============================================================

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

// =============================================================
// Vision-Feature: File-Upload-Handler
// =============================================================

async function handleFileSelect(e) {
  const file = e.target.files?.[0];
  if (!file) return;

  // Validierung: nur Bilder
  if (!file.type.startsWith('image/')) {
    alert('Bitte ein Bild hochladen (JPG, PNG, WebP oder GIF).');
    $fileInput.value = '';
    return;
  }

  try {
    // Bild verkleinern auf max 1568px lange Kante (Anthropic-Empfehlung)
    const { dataUrl, mediaType } = await resizeImageToDataUrl(file);

    // Final-Check: nicht zu gross nach Resize
    if (dataUrl.length > MAX_IMAGE_BYTES) {
      alert('Das Bild ist zu gross — versuch einen Screenshot mit weniger Inhalt oder schicke es in zwei Teilen.');
      $fileInput.value = '';
      return;
    }

    state.pendingAttachment = { dataUrl, mediaType };
    $attachmentThumb.src = dataUrl;
    $attachmentPreview.hidden = false;
    $input.placeholder = 'Sag kurz, was ich anschauen soll (oder leer lassen — ich machs auch so) …';
    $input.focus();
  } catch (err) {
    console.error('File-Upload-Fehler:', err);
    alert('Das Bild konnte nicht geladen werden. Versuch es nochmal.');
  } finally {
    $fileInput.value = ''; // damit das gleiche Bild nochmal gewaehlt werden kann
  }
}

function clearAttachment() {
  state.pendingAttachment = null;
  $attachmentThumb.src = '';
  $attachmentPreview.hidden = true;
  $input.placeholder = 'Schreib hier …';
}

// Bild verkleinern via Canvas → liefert data-URL (base64) + mediaType
function resizeImageToDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(reader.error);
    reader.onload = () => {
      const img = new Image();
      img.onerror = () => reject(new Error('Bild laesst sich nicht dekodieren'));
      img.onload = () => {
        // Berechne Skalierungs-Faktor
        const maxDim = MAX_IMAGE_DIMENSION;
        let { width, height } = img;
        if (width > maxDim || height > maxDim) {
          if (width > height) {
            height = Math.round(height * (maxDim / width));
            width = maxDim;
          } else {
            width = Math.round(width * (maxDim / height));
            height = maxDim;
          }
        }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);

        // Anthropic erwartet jpeg/png/gif/webp. Bei jpg/jpeg konvertieren wir zu jpeg
        // (komprimiert besser), bei png/gif/webp behalten wir das Original.
        const isPhoto = file.type === 'image/jpeg' || file.type === 'image/jpg';
        const targetType = isPhoto ? 'image/jpeg' : 'image/png';
        const quality = isPhoto ? 0.85 : undefined;
        const dataUrl = canvas.toDataURL(targetType, quality);

        resolve({ dataUrl, mediaType: targetType });
      };
      img.src = reader.result;
    };
    reader.readAsDataURL(file);
  });
}

init();
