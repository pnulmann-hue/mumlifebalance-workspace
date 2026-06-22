/**
 * Meta Token Guard
 * ================
 * Prüft, ob der Meta-Access-Token noch lebt — und (wenn App-Secret vorhanden)
 * wie viele Tage er noch gültig ist. Wirft NICHT beim Import (anders als
 * meta-api.js), damit der GitHub-Workflow auch bei totem Token sauber laufen
 * und eine Telegram-Warnung schicken kann.
 *
 * Hintergrund: Am 16.05.2026 ist der Token still abgelaufen — 5 Wochen lang hat
 * niemand gemerkt, dass Cockpit-Ads-Lesung + Claude-Zugriff tot waren. Dieser
 * Wächter sorgt dafür, dass das nie wieder unbemerkt passiert.
 *
 * Aufruf:
 *   node --env-file=.env token-guard.js        (lokal)
 *   node token-guard.js                          (CI, Env kommt aus Secrets)
 *
 * Exit-Codes:
 *   0  = gesund (lebt, und falls messbar: > WARN_DAYS Tage Restlaufzeit)
 *   1  = tot / fehlt / abgelaufen
 *   2  = läuft bald ab (innerhalb WARN_DAYS)
 *
 * Optionale Env für Restlaufzeit-Messung: META_APP_ID + META_APP_SECRET
 * Optional: WARN_DAYS (Default 10)
 */

const API_VERSION = 'v21.0';
const BASE = `https://graph.facebook.com/${API_VERSION}`;

const TOKEN = process.env.META_ACCESS_TOKEN;
const APP_ID = process.env.META_APP_ID;
const APP_SECRET = process.env.META_APP_SECRET;
const WARN_DAYS = parseInt(process.env.WARN_DAYS || '10', 10);

function out(status, message) {
  // Erste Zeile maschinenlesbar für den Workflow, danach menschenlesbar.
  console.log(`STATUS=${status}`);
  console.log(message);
}

// Setzt process.exitCode (statt process.exit), damit der Event-Loop sauber
// ausläuft. process.exit() während noch ein fetch-Socket schliesst löst auf
// Windows eine libuv-Assertion aus und liefert Exit-Code 127 statt des
// gewünschten Codes.
async function main() {
  if (!TOKEN) {
    out('DEAD', '❌ Meta-Token FEHLT (META_ACCESS_TOKEN ist leer). Bitte neuen Token hinterlegen.');
    return 1;
  }

  // 1. Liveness: lebt der Token überhaupt?
  let me;
  try {
    const res = await fetch(`${BASE}/me?fields=id,name&access_token=${TOKEN}`);
    const body = await res.json();
    if (!res.ok) {
      const msg = body?.error?.message || JSON.stringify(body);
      out('DEAD', `❌ Meta-Token TOT — Zugriff auf Werbekonto futsch.\n\nMeta sagt: ${msg}\n\n→ Neuen Token erstellen (Anleitung: scripts/meta-ads/TOKEN-SETUP.md) und GitHub-Secret META_ACCESS_TOKEN aktualisieren.`);
      return 1;
    }
    me = body;
  } catch (e) {
    out('DEAD', `❌ Meta-API nicht erreichbar: ${e.message}`);
    return 1;
  }

  // 2. Restlaufzeit (nur wenn App-Secret da ist — debug_token braucht App-Token)
  if (APP_ID && APP_SECRET) {
    try {
      const appToken = `${APP_ID}|${APP_SECRET}`;
      const res = await fetch(`${BASE}/debug_token?input_token=${TOKEN}&access_token=${appToken}`);
      const body = await res.json();
      const expiresAt = body?.data?.expires_at; // Unix-Sekunden; 0 = nie
      if (res.ok && typeof expiresAt === 'number') {
        if (expiresAt === 0) {
          out('OK', `✅ Meta-Token gesund (${me.name}). Läuft NIE ab (System-User-Token). Perfekt.`);
          return 0;
        }
        const msLeft = expiresAt * 1000 - Date.now();
        const daysLeft = Math.floor(msLeft / 86400000);
        const dateStr = new Date(expiresAt * 1000).toISOString().slice(0, 10);
        if (daysLeft <= WARN_DAYS) {
          out('WARN', `⚠️ Meta-Token läuft in ${daysLeft} Tagen ab (am ${dateStr}).\n\nJetzt erneuern, bevor Cockpit-Ads + Claude-Zugriff wieder still sterben.\nAnleitung: scripts/meta-ads/TOKEN-SETUP.md`);
          return 2;
        }
        out('OK', `✅ Meta-Token gesund (${me.name}). Noch ${daysLeft} Tage gültig (bis ${dateStr}).`);
        return 0;
      }
    } catch {
      // debug_token fehlgeschlagen — Liveness reichte, kein harter Fehler.
    }
  }

  // 3. Lebt, aber Restlaufzeit nicht messbar (kein App-Secret hinterlegt).
  out('OK', `✅ Meta-Token lebt (${me.name}). Restlaufzeit nicht messbar — für Frühwarnung META_APP_SECRET hinterlegen.`);
  return 0;
}

main().then((code) => { process.exitCode = code; });
