---
tags: [funnel]
---

# Prüfung aller AC-Formulare — 23.10.2026

Anlass: Das Formular „0€ doTERRA Energie-Kickstart“ war eine Kopie von Freischaufeln
(falscher Tag, falsche Liste, AC-Standard-Bestätigungsmail, keine Seite nach der Bestätigung).
Danach alle 21 Formulare über die Schnittstelle ausgelesen: Tag · Liste · Automation ·
Bestätigungsmail · Danke-Seite nach dem Absenden · Seite nach dem Bestätigungsklick.

**Erledigt am 23.10.:** Energie-Kickstart (Formular 64) komplett — Tag `energie-kickstart`,
Liste „doTERRA Interessenten“, eigene Bestätigungsmail, Absenderadresse, Seite nach Bestätigung
`/energie-kickstart-bestaetigt/` (WP 4382). Einmal echt anmelden steht noch aus (reCAPTCHA).

**Ebenfalls am 23.10.:** Neue Bestätigungsmails für die neun laufenden Mentoring-Formulare
(49 · 51 · 53 · 45 · 41 · 47 · 66 · 71 · 1), gebaut mit `scripts/mails/bestaetigung-bauen.py`,
in AC eingesetzt und zurückgelesen. Ansicht: `outputs/funnels/bestaetigungsmails/`, alte Fassungen
in `_alt/`. Offen bleiben die Altformulare 37 · 39 · 43 · 55 · 57 (weiter „Grenzen setzen“).

## Die Formulare

| # | Formular | Tag → Automation | Liste | Bestätigungsmail | nach Bestätigung |
|---|---|---|---|---|---|
| 64 | doTERRA Energie-Kickstart | energie-kickstart → 0€ doTERRA Energiekick | doTERRA Interessenten | ✅ eigene | ✅ /energie-kickstart-bestaetigt/ |
| 47 | Bio Check | 0€ Bio-Check → 0€ Bio-Check | Newsletter | Text gestaltet, **Betreff Standard** | /anmeldung-danke/ (Angebote drauf) |
| 66 | Ideen-Finder | 0€ Idee → 0€ Idee | Newsletter | Text gestaltet, **Betreff „Sie“ + Listenname** | /produkt-ideen-finder-los/ (Pitch 39) |
| 71 | Stimmcheck | 0€ Stimmcheck → 0€ Stimmcheck | Newsletter | Text gestaltet, **Betreff „Sie“ + Listenname** | /stimm-check-los/ (Pitch) |
| 69 | Anmeldung KI Webinar | 0€ KI Webinar → 0€ KI Webinar | Newsletter | Text gestaltet, **nennt 8. Oktober**, Betreff „Sie“ | 🚨 /ki-masterclass-danke/ ist **privat** |
| 73 | Anmeldung KI Webinar (Kopie) | wie 69 | Newsletter | wie 69 | 🚨 wie 69 |
| 49 | Businessfahrplan | 0€ Businessfahrplan → 0€ Businessfahrplan | **keine** | 🚨 „Grenzen setzen“ | /anmeldung-erfolgreich/ |
| 51 | Lead-Challenge | 0€ Lead-Challenge → 0€ Lead Challenge | **keine** | 🚨 „Grenzen setzen“ | /anmeldung-erfolgreich/ |
| 53 | Starterguide | 0€ Starterguide → 0€ Instagram-Starterguide | **keine** | 🚨 „Grenzen setzen“ | /anmeldung-erfolgreich/ |
| 45 | Story-Challenge | Formular → 0€ Story Challenge | Newsletter | 🚨 „Grenzen setzen“ (2024) | /anmeldung-erfolgreich/ |
| 41 | Von 0 auf echt | Formular → 0€ Von 0 auf echt | **keine** | 🚨 „Grenzen setzen“ (2024) | /anmeldung-erfolgreich/ |
| 1 | Newsletter | Newsletter → Willkommens-Sequenz | Newsletter | alter Text (2023) | /anmeldung-erfolgreich |
| 62 | Freischaufeln | Freischaufeln Lead → 0€ Freischaufeln | Newsletter | **keine** — Danke-Seite sagt trotzdem „Mail bestätigen“ | — |
| 25 | Guide doTERRA Business | → Guide doTERRA Business | doTERRA Interessenten | eigener Text (2024) | /anmeldung-erfolgreich/ |
| 37 | Mini-Notfallapotheke | Formular → Automation 39 | doTERRA Interessenten | 🚨 „Grenzen setzen“ | /anmeldung-erfolgreich/ |
| 39 | Öl-Reise | Formular → Automation 41 | doTERRA Interessenten | 🚨 „Grenzen setzen“ | /anmeldung-erfolgreich/ |
| 43 | Webinar Businessaufbau | Formular → Automation 43 | Newsletter | 🚨 „Grenzen setzen“ | /anmeldung-erfolgreich/ |
| 60 | Mama Business Bootcamp | Formular → Automation 68 | Newsletter | keine | — |
| 55 | Webinar Mama CEO | 0€ Webinar Mama-CEO 2 → **keine Automation** | keine | 🚨 „Grenzen setzen“ | /anmeldung-erfolgreich/ |
| 57 | MBA Warteliste | mba-warteliste → **keine Automation** | keine | 🚨 „Grenzen setzen“ | /anmeldung-erfolgreich/ |
| 59 | MBA-Webinar 24.6. | mba-webinar-anmeldung → **keine Automation** | keine | — | Standardtext |

## Was das heisst

1. **Zehn Formulare verschicken als erste Mail einen Text der alten Positionierung:**
   *„Toll, dass du lernen willst, erfolgreich Grenzen zu setzen! … Damit ich dir den Link zum
   Webinar senden … darf“*. Darunter Businessfahrplan, Lead-Challenge, Starterguide,
   Story-Challenge und Von 0 auf echt — also laufende Funnels.
2. **Kein einziger Betreff ist eigener Text** (ausser Kickstart): entweder „Bitte bestätigen Sie
   Ihr Abonnement für %LISTNAME%“ oder „Bitte bestätige deine Anmeldung %LISTNAME%“. Bei sechs
   Formularen ohne Liste ist %LISTNAME% leer, bei den anderen steht der interne Listenname da.
3. **Die Seite nach der Bestätigung ist bei elf Formularen `/anmeldung-erfolgreich/`** — mit der
   alten Work-Life-Balance-Positionierung und einem Instagram-Hinweis, ohne Angebot.
4. **Die Danke-Seite nach dem Absenden ist überall „Fast geschafft“** (`/fast-geschafft/` oder
   `-2/`) — ohne Angebot. Julias erste und stärkste Verkaufsstelle ist damit überall leer.
5. **`/ki-masterclass-danke/` ist privat**, Formulare 69 und 73 leiten nach der Bestätigung dorthin.
   Die Masterclass ist vorbei — Formulare stilllegen oder umleiten.
6. **Drei Formulare ohne Automation** (Webinar Mama CEO, MBA-Warteliste, MBA-Webinar 24.6.) —
   vermutlich Altbestand; wer sich dort noch einträgt, bekommt nichts.

## Julias Regel für die Danke-Seite

Aus „Bonus Deine Danke Seite“ und dem Update 2026 (Leadgewinnung leicht gemacht): Nach dem
Absenden kurz „das hat geklappt“, dann *„aber halt, stopp, ich hab da noch was für dich“* — ein
Produkt, das es **nirgends sonst** zu diesem Preis gibt, stark rabattiert (bei ihr 17 statt 199),
mit Name, Preis, Mockup und Inhaltsliste. Die Knappheit ist die Stelle, nicht eine Uhr:
**„nur hier“**, nicht „nur heute“. Im Update 2026 zwei Optionen nebeneinander, die teurere
gelegentlich ausverkauft — aber nur, wenn sie es wirklich ist.

→ Dafür braucht jeder Funnel eine **eigene** Danke-Seite (heute teilen sich alle zwei).

**Patricias Entscheid (23.10.):** Auf der Danke-Seite der **grosse Kurs für 199 statt 333**, Satz
*„diesen Preis gibt es nur hier, direkt nach deiner Anmeldung“*, ohne Uhr. Der Upsell nach
Storyideen und Startklar bleibt bei **97** (Käuferinnen-Preis). Minikurse bleiben 39.
ThriveCart heute: Kundenmaschine 333 · Upsell 7 = 97 · Bump an der Digitalen Produktwelt = 199 ·
ungenutzte Upsell-Kopie 8 = 199.

**Kassenlinks zu 199 (angelegt 23.10., getestet: Kasse zeigt 333 − 134 = 199):**
ThriveCart kann keine Preisoption verstecken, deshalb Gutscheine — fester Betrag 134, nur das
eine Produkt, nur Einmalzahlung, ohne Ablauf und ohne Begrenzung.

- Kundenmaschine: `https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/?coupon=DANKE199IKM`
- Mama-CEO: `https://mumlifebalance.thrivecart.com/mama-ceo/?coupon=DANKE199CEO`
- Digitale Produktwelt: `https://mumlifebalance.thrivecart.com/digitale-produktwelt/?coupon=DANKE199DPW`
  (für Ideen-Finder und Businessfahrplan, Patricias Entscheid 23.10.)

✅ Kasse der Kundenmaschine am 23.10. auf **Selbstlernkurs** umgestellt (Patricia: alle Module
sofort offen, Telegram-Antworten Di/Do, Call-Aufzeichnungen der ersten Runde in der Gruppe):
Unterzeile, Einleitung, „Begleitung & Support in der Telegram-Gruppe“, drei Listenpunkte und
die FAQ 2–6. Live geprüft: kein Datum, kein „Gruppenprogramm“ mehr. Die Hero-Zeile „Baue dir in
8 Wochen …“ bleibt (Ergebniszeit, kein Programmablauf).

## Danke-Seiten mit 199er-Angebot (gebaut 23.10., Entwürfe)

`scripts/wordpress/deploy-danke-seiten.mjs` (lokal ansehen mit `--vorschau` →
`outputs/funnels/danke-seiten/`). Aufbau: Postfach-Schritte mit dem Betreff der
Bestätigungsmail → „Halt, eins noch“ mit Brückensatz und Produktbild → Preisblock 199 statt
333 „nur hier, direkt nach deiner Anmeldung“ → ruhiger Ausweg. Gestaltung: `.enr`-CSS.

| Seite | WP | Formular | Kurs |
|---|---|---|---|
| /danke-story-challenge/ | 4386 | 45 | Kundenmaschine |
| /danke-starterguide/ | 4388 | 53 | Kundenmaschine |
| /danke-bio-check/ | 4390 | 47 | Kundenmaschine |
| /danke-lead-challenge/ | 4392 | 51 | Kundenmaschine |
| /danke-businessfahrplan/ | 4394 | 49 | Kundenmaschine |
| /danke-ideen-finder/ | 4396 | 66 | Kundenmaschine |
| /danke-von-0-auf-echt/ | 4398 | 41 | Kundenmaschine |
| /danke-freischaufeln/ | 4400 | 62 | Mama-CEO (ohne Bestätigungsmail) |

Nach dem Veröffentlichen: je Formular „Bei Absendung → URL öffnen“ auf die eigene Seite.
Seit 23.10. abends führen **Businessfahrplan und Ideen-Finder auf die Digitale Produktwelt**
(`DANKE199DPW`), die übrigen sechs Mentoring-Seiten auf die Kundenmaschine, Freischaufeln auf Mama-CEO.

**Kassen aufgeräumt (23.10., live geprüft):**
- Digitale Produktwelt: „Jemand kauft deinen Kurs“ statt „Eine Frau …“, „Sofort verfügbar.“ statt
  „ab 4. April“, Tippfehler Modul 3, Call-Zeile gelöscht (Kurs lief nie live, keine Aufzeichnungen),
  Telegram „ich antworte dienstags und donnerstags“, FAQ „Gibt es Live-Calls? Nein …“.
- Mama-CEO: Selbstlernkurs mit Telegram-Gruppe; „4 Live-Termine“ + Beschreibung gelöscht, „8 Wochen“
  bei Programm/Telegram/Zugang raus, FAQ ohne Live-Termine (Calls geschlossen, keine Aufzeichnungen),
  „über 13“, „mit der Selbständigkeit“, „Mein erstes.“ entfernt.
- Die „Enter your bullet points here..“ und „Ut Repellat Officiis“ stehen in **ausgeblendeten
  Spalten** — nicht sichtbar, deshalb nicht gelöscht (ein Löschversuch hätte den Modul-Titel mitgenommen).

⚠️ Offen: Zusatzangebot an der DPW-Kasse rechnet falsch (249 + 333 = 582 → 448), Preisentscheid
zum Bundle (DPW 199 + Kundenmaschine 199 = 398) steht bei Patricia.

## Reihenfolge zum Abarbeiten (Vorschlag)

1. Bestätigungsmails der laufenden Funnels in eigener Stimme (wie Kickstart, Muster
   `outputs/produkte/doterra-mama-energie/mails/kickstart-mail-0.html`).
2. Je Funnel eine Seite nach der Bestätigung statt `/anmeldung-erfolgreich/`.
3. Je Funnel eine Danke-Seite mit „nur hier“-Angebot — dafür entscheidet Patricia das Angebot.
4. Altbestand (55, 57, 59, 69, 73) stilllegen.
