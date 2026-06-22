# Meta-Token dauerhaft einrichten

> **Warum diese Datei existiert:** Am 16.05.2026 ist ein kurzlebiger Token (aus dem Graph-API-Explorer) noch am selben Tag abgelaufen. 5 Wochen lang waren dadurch der Cockpit-Ads-Teil und Claudes Zugriff aufs Werbekonto unbemerkt tot. Diese Anleitung führt zum **dauerhaften** Token, der nicht still stirbt — plus dem Wächter, der ab jetzt warnt, falls doch mal was abläuft.

---

## Der richtige Token-Typ: System-User-Token (läuft nie ab)

Graph-Explorer-Tokens sind kurzlebig (1–2 Stunden) oder maximal 60 Tage. Für Automatisierung ist der **System-User-Token** aus den Business-Einstellungen der richtige — der kann auf **„Läuft nie ab"** gestellt werden.

### Schritt 1 — System-User anlegen (einmalig)

1. Öffne die [Meta Business-Einstellungen](https://business.facebook.com/settings/) → **Benutzer → Systembenutzer**.
2. **Hinzufügen** → Name z.B. `mumlifebalance-automation`, Rolle **Admin**.
3. Beim Systembenutzer auf **Assets zuweisen** → dein **Werbekonto** (`act_592366665547345`) → Vollzugriff/Verwalten aktivieren. (Falls du Page-Ads liest: auch die Facebook-Seite zuweisen.)

### Schritt 2 — Token generieren

1. Beim Systembenutzer **„Token generieren"** klicken.
2. **App auswählen:** deine bestehende Meta-App (die `META_APP_ID` aus der `.env`).
3. **Ablauf:** **„Niemals"** wählen.
4. **Berechtigungen ankreuzen:** `ads_read`, `ads_management`, `business_management`, `pages_read_engagement`.
5. **Token generieren** → einmal kopieren (wird nur einmal angezeigt).

---

## Den Token hinterlegen (zwei Orte)

### A) GitHub-Secret (für Cockpit-Bot + alle Workflows)

Repo → **Settings → Secrets and variables → Actions** → `META_ACCESS_TOKEN` **aktualisieren** (oder neu anlegen) → Token einfügen.

> Optional, für die Restlaufzeit-Frühwarnung bei 60-Tage-Tokens: zusätzlich `META_APP_ID` und `META_APP_SECRET` als Secrets hinterlegen. Bei einem „Niemals"-System-User-Token nicht nötig.

### B) Lokale `.env` (für Claude Code / lokale Aufrufe)

In `scripts/meta-ads/.env` die Zeile `META_ACCESS_TOKEN=...` ersetzen.

> ⚠️ Die `.env` ist gitignored und persistiert nicht in der Web-Sandbox. In Claude Code auf deinem Rechner bleibt sie aber liegen.

---

## Prüfen, ob's läuft

```bash
cd scripts/meta-ads
node --env-file=.env meta-api.js whoami      # sollte deinen Namen + Konto zeigen
node --env-file=.env token-guard.js          # sollte "✅ Meta-Token ... Läuft NIE ab" o.ä. zeigen
```

---

## Der Wächter (läuft automatisch)

`.github/workflows/meta-token-guard.yml` prüft **täglich 07:00 CH-Zeit** den Token und schickt dir **nur bei Problem** eine Telegram-Nachricht (gesund = still, kein Spam):

- **Token tot/fehlt** → ❌-Warnung sofort.
- **Läuft in ≤ 10 Tagen ab** (nur messbar mit `META_APP_SECRET`) → ⚠️-Vorwarnung.

Manuell auslösen: Repo → **Actions → Meta-Token-Guard → Run workflow**.

So stirbt der Zugriff nie wieder 5 Wochen lang unbemerkt.
