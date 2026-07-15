---
tags: [funnel, doterra]
---

# 🌿 Öl-Begleiter — Anmeldung via AC-Formular → Biolinks → Bot

**Ziel:** Menschen tragen sich mit E-Mail ein (= Lead in ActiveCampaign), werden dann
zum Telegram-Öl-Begleiter weitergeleitet. Der Anmelde-Link kommt in deine **Biolinks**.

**Der Flow:**

```
Biolinks  →  "Öl-Pröbchen testen"-Button  →  Anmelde-Landing (AC-Formular)
     ↓                                              ↓ Vorname + E-Mail
     └────────────────────────────────  Lead in AC-Liste 18 + Tag
                                                    ↓ Weiterleitung
                                          Telegram-Öl-Begleiter  →  7 Tage
```

Damit hast du beides: die **E-Mail als Lead** (für parallele Mails) UND die Testerin
**im Bot** (für die 7-Tage-Begleitung).

---

## Die Dateien in diesem Ordner

| Datei | Zweck |
|-------|-------|
| `anmeldung.html` | Vollständige Anmelde-Landing (Ziel für den Biolink). Als WP-Seite veröffentlichen. |
| `ac-form-embed.html` | Nur der Formular-Block (falls du ihn in eine bestehende Seite einbetten willst). |
| `biolink-button.html` | Fertiger Button für deine Link-in-Bio-Seite. |

---

## Schritt 1 — Telegram-Bot anlegen (falls noch nicht)

Bei **@BotFather** einen neuen Bot erstellen → du bekommst den **Token**
(`OEL_BOT_TOKEN` für `scripts/oel-begleiter/`) und den festen Link `https://t.me/DeinBot`.
Diesen Link brauchst du unten als `{{BOT_LINK}}`.

## Schritt 2 — AC-Formular anlegen

In ActiveCampaign → **Formulare → Neu**:

1. **Typ:** Inline-Formular. Felder: **Vorname** (`fullname`) + **E-Mail** + Datenschutz-
   Checkbox (Custom Field `datenschutz`, wie beim Bio-Check).
2. **Aktionen:**
   - **Zu Liste hinzufügen:** `18 · doTERRA Interessenten`
   - **Tag hinzufügen:** neuer Tag **`oel-sample-lead`** (empfohlen, damit du Sample-
     Testerinnen von der 3-Tage-Energie-Challenge unterscheidest). Alternativ vorhandenen
     Tag `energie_kickstart` (84) nutzen.
   - **Nach dem Absenden weiterleiten zu URL:** `{{BOT_LINK}}` (dein Telegram-Bot!)
3. Formular speichern → **„Integrieren" → Code kopieren.** Darin stehen die zwei Werte,
   die du unten brauchst:
   - die **Formular-Nummer** (`u`/`f`, z.B. 71) → `{{AC_FORM_ID}}`
   - der **`or`-Token** (langer UUID-String) → `{{AC_ORG_TOKEN}}`

> 💡 Schneller Weg: In AC das bestehende ENERGIE-Formular (64) **duplizieren**, umbenennen
> in „Öl-Begleiter", nur die Weiterleitung auf `{{BOT_LINK}}` ändern und den `oel-sample-lead`-
> Tag ergänzen. Dann sind Liste + Consent schon korrekt gesetzt.

## Schritt 3 — Platzhalter in den Dateien ersetzen

In `anmeldung.html` **und** `ac-form-embed.html` diese drei Werte ersetzen:

| Platzhalter | Wert |
|-------------|------|
| `{{AC_FORM_ID}}` | Formular-Nummer aus AC |
| `{{AC_ORG_TOKEN}}` | `or`-Token aus dem AC-Embed-Code |
| `{{BOT_LINK}}` | `https://t.me/DeinBot` |

> Schick mir den AC-Embed-Code deines neuen Formulars, dann setz ich die Werte für dich
> ein und geb dir die finale paste-fertige Version zurück.

## Schritt 4 — Landing veröffentlichen

`anmeldung.html` als WordPress-Seite anlegen (z.B. `mumlifebalance.ch/oel-begleiter`).
Am einfachsten über den `/wp`-Skill als **Draft** — dann prüfst du sie und publizierst selbst.

## Schritt 5 — In die Biolinks setzen

In `biolink-button.html` `{{LANDING_URL}}` auf deine neue Seite setzen
(`https://mumlifebalance.ch/oel-begleiter`) und den Button in deine Link-in-Bio-Seite
einfügen. Fertig.

---

## Wichtig / Grenzen

- **Consent bleibt Pflicht** (Datenschutz-Checkbox, wie bei allen deinen Formularen).
- **Sandbox:** `mumlifebalance.activehosted.com` ist aus der Web-Claude-Sandbox geblockt
  (403) — darum sind das paste-fertige Assets statt Live-Push. Das AC-Formular selbst
  legst du in der AC-Oberfläche an (Nummer + Token entstehen erst dort).
- **Doppel-Opt-in-Reibung:** Erst Formular, dann Telegram ist ein Schritt mehr als „direkt
  zum Bot". Dafür bekommst du die E-Mail. Wenn du lieber reibungslos direkt zum Bot willst
  (ohne AC-Lead), zeigt der Biolink-Button einfach auf `{{BOT_LINK}}` statt auf die Landing.

## 🔗 Verwandte Notizen

- [[../../scripts/oel-begleiter/README|Öl-Begleiter Bot (Code)]]
- [[../active-funnels|Aktive Funnels]]
- [[_MOCs/MOC-doTERRA|doTERRA Map of Content]]
