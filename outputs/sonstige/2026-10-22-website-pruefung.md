---
tags: [misc, website, salespage]
---

# Website-Prüfung mumlifebalance.ch — 22.10.2026

Alle **73 veröffentlichten Seiten** geprüft: Ansicht am Computer (1440 px) und am Handy (375 px),
Links zu ThriveCart mit Status und Preis an der Kasse, Datumsangaben, übrige Links, und die
**34 Seiten der heutigen Ausrichtung** mit dem Copywriting-Skill (BRAND-VOICE, ZIELGRUPPE,
Blackliste). Werkzeug: `scripts/wordpress/seiten-pruefen.mjs` (wiederholbar).

Patricias feste Entscheide, die nicht bemängelt werden: Ergebnis-Zahlen bleiben · keine
Geld-zurück-Garantie · echte Kundinnen-Zitate bleiben wörtlich.

---

## ✅ Schon behoben (22.10.)

- **Einzug am Computer** auf 14 Seiten weg: bio-check, content-box, dankesseite-potenzial-quiz,
  fahrplan, instagram-starterguide, lead-challenge, mama-ceo, mba, mba-warteliste,
  potenzial-test, story-challenge, von-0-auf-echt, anmeldung-danke, freischaufeln — dazu der
  Hintergrund von hormone und energie-kickstart. Ursache: ein Elementor-Container „boxed“
  (max. 1140 px, 10 px Rand) bzw. die Theme-Breite. Lösung im Customizer („Zusätzliches CSS“,
  Block `VOLLBREITE GESTALTETE SEITEN`, Quelle `scripts/wordpress/vollbreite-customizer.css`),
  weil die Firewall das Speichern der Seiten selbst blockt.
- **Handy:** keine der 73 Seiten scrollt seitlich.

---

## 🔴 Dringend — Geld, Termine, Compliance

| Seite | Fund | Was tun |
|---|---|---|
| /ki-kurs/ | „Die Kasse ist bis Freitag, 23. Oktober, offen“ — morgen vorbei. Dazu „Kapitel 1 AB 2.11.“ gegen „So 1. November: Kapitel 1 bis 3“ | ab 24.10. Kassen-Text tauschen; einen Starttag festlegen |
| /ki-kurs/ ↔ MBA-Upsell | „Dann rechne ich dir den vollen Betrag an“ — beim Upsell steht bewusst keine Anrechnung | Regel vereinheitlichen |
| /stimm-check-los/ | Danke-Seite lädt zur Masterclass „Donnerstag, 8. Oktober, 9 Uhr“ ein — jede neue Anmeldung landet dort | auf Aufzeichnung oder KI-Kurs umstellen |
| /ki-masterclass/ + /ki-masterclass-danke/ | ganzer Inhalt hängt am 8. Oktober, Formular noch offen | stilllegen oder auf Aufzeichnung umbauen |
| /mba/ | „Programmstart Mitte August“, „Nach den Sommerferien starten wir live“; „drei Kurse … CHF 999“ ohne Easy KI | Termine raus, Easy KI in Aufzählung + Wert-Stack |
| /mba-warteliste/ | „PIONEER-PHASE STARTET NÄCHSTEN MONAT“ — die MBA läuft längst; 30-Min-Call, der auf /mba fehlt | auf /mba/ umleiten oder abschalten |
| /mba-webinar-replay/ | „Pioneer-Preis“ und „Fenster nur 48 Stunden offen“ | nur stehen lassen, wenn die Frist technisch läuft; „Pioneer“ streichen |
| /mama-wird-hausapothekerin/ | „weniger Medikamente“, Algifor-Szene, „ohne direkt zur Apotheke oder zum Arzt zu rennen“, „Öl-Anwendung, die wirkt“ bei Bauchweh, „SOS-Notfälle: Fieber … Ohrenschmerzen“ | **Compliance** — umformulieren, Programm ist aktiv |
| /mini-notfallapotheke-fuer-mamas/ | „3 einfache Hausmittel, die sofort helfen“, „Körper … selbst zu heilen“ | **Compliance** |
| /startersets/ | Immun- und Wirkaussagen bei Kindern („Stronger … Immunabwehr“, „Brave … Angst“), „EUR 80“ | **Compliance** — abschalten oder auf Bestell-Link kürzen |
| /doterra/ | „On Guard stärkt das Immunsystem“, „Air befreit die Atemwege“, „Deep Blue lindert“ | **Compliance** — abschalten, auf /energieroutine/ leiten |
| /mama-energise/ | ThetaHealing „Fr. 120.00 / Fr. 400.00“, „Heilung fördern“ | abschalten, auf /energieroutine/ leiten |
| „Körper hat alles, um sich selbst zu heilen“ | Patricias Satz auf vier doTERRA-Seiten | überall raus |

## 🟠 Preise und Kassen

| Wo | Fund |
|---|---|
| /bio/ | „Vom Networkwissen zum Produkt · Mini-Kurs · 37 CHF“ (zweimal) — Kasse 39 |
| /dankesseite-potenzial-quiz/ | „Finde dein Thema · CHF 37“ (dreimal) — Kasse 39 |
| /bio/ | verlinkt „Dein starkes Mama-Business“ → Kasse steht auf **test** (bucht nichts ab) |
| /mama-zeit/, /easy-mumlife-academy/ | verlinken die Kasse `mama-zeit` — **abgeschaltet** |
| /ordnung-im-familienchaos/, /grenzen-setzen/, /selbstbewusst-als-mama/, /easy-mumlife-academy/ | verlinken abgeschaltete Kassen |
| /anmeldung-danke/ | „Nur einmalig. Dieses Angebot kommt nicht zurück.“ — Expertin 97 steht offen auf /bio |
| ThriveCart „Aus Nebenbei wird Business“ (VIP) | „Beta-Platz · April 2026“, „Noch 3 Plätze“ — auf der Kasse selbst |
| ThriveCart Digitale Produktwelt, Bump | „Dieser Kurs: CHF 249.–“ — der Kurs kostet 333 |
| MBA-Preis | /mba zeigt 1347, Replay 997 — bewusst so? (Webinar-Preis) |

Geprüft und richtig: Instagram-Kundenmaschine, Mama-CEO, Magnet-Ich, Digitale Produktwelt je 333 ·
MBA 1347 · Expertin 97 (statt 149) · Startklar 39 · Storyideen 19 · Easy KI 333 · VIP 777.

## 🟠 Kaputte Links

- /mama-ceo/ → `mumlifebalance.ch/instagram-kundenmaschine` gibt **404** (keine Seite dieses Namens)
- Fusszeile von doterra, grenzen-setzen, mama-wird-hausapothekerin, mini-notfallapotheke, oelreise,
  quiz, selbsttest, startersets u.a.: „Privatsphäre-Einstellungen“ ist ein nicht ausgeführter
  Shortcode `[rcb-consent …]` und führt nirgends hin
- /datenschutzerklaerung/ → ActiveCampaign-SCC-Link gibt 404
- /workshop-2/ → /anmeldung-erfolgreich-2/ gibt 404

## 🟡 Seiten mit abgelaufenem Datum (alte Ausrichtung / vergangene Events)

/bootcamp/ und /bootcamp-willkommen/ (29.6.–3.7.2026) · /ki-webinar/ (26. Mai 2026) ·
/webinar-business/ (19.1.2026) · /webinar-mama/ (21.2.25) · /webinar/ (27.9.24) ·
/doterra-webinar/ (23. August 2024) · /workshop-2/ (30.10.–3.11.2023).
Dazu ohne Datum, aber alte Ausrichtung: 3-schritte, 5-tage-challenge, grenzen-setzen(+_anmeldung),
mama-zeit, selbstbewusst-als-mama, selbsttest, quiz, werteliste(-2), ebook, easy-mumlife-academy,
ordnung-im-familienchaos, mama-unternehmen, energise-begleitung, anmeldung-erfolgreich*, fast-geschafft(-2).
→ **Kandidaten zum Abschalten** (auf „privat“ stellen, nichts löschen).

Unkritisch: Jahreszahlen in Patricias Geschichte (2023, Mai 2025) und „© 2026“ in der Fusszeile.

---

## ✍️ Texte — Copywriting-Prüfung je Seite

Ampel: 🟢 nur Feinschliff · 🟡 überarbeiten · 🔴 dringend

### Mentoring — Verkauf

**Startseite 🔴** — alte Mama-Balance-Ausrichtung („Mindset, Alltagsmanagement und Selbstfürsorge“),
drei „nicht …, sondern“-Sätze, Floskeln („passiert Magie“, „Hamsterrad“), Werte-Block doppelt,
„Erfüllung und Erfolg entsteht“ → „entstehen“.

**Über mich 🟡/🔴** — „androhen“ → „andrehen“ · Reihe „X statt Y“ · Satz bricht ab („zur klaren
Unternehmerin mit Haltung…“) · Netzwerkaufbau-Tipps („Systematik hinter Empfehlungsmarketing“) ·
KI-Assistenten, Mai 2025 und 18 Stunden fehlen · „Theta-Heilerin“: passt das noch?

**Angebote 🟡** — „unabhängig vom Network / von deinem Unternehmen“ klingt gegen das Network
(Magnet-Ich sagt das Gegenteil) → „neben deinem Network ein zweites Einkommen, das dir allein gehört“ ·
„Manchmal braucht es mehr als To-do-Listen … nämlich jemanden“ · Jargon „smarte Monetarisierung“,
„Network Marketing 2.0“, „Herzensbusiness“ · VIP hat zwei Kassen (Produkt 29 + 30).

**MBA 🔴** — siehe oben (Termine, Easy KI) · Antithesen „Keine Modul-Listen — sondern …“,
„Umsetzung statt Theorie“, „Klarheit statt Chaos“.

**Mama-CEO 🔴** — „Kein Monat ohne Verkauf seit Mai 2025“, „vierstellig pro Monat“ (gestrichen) →
„Seit Mai 2025 gibt es keinen Monat mehr ohne Einkommen aus meiner Selbständigkeit, mit 18 Stunden
in der Woche.“ · „schon erste Kundinnen hattest“, „Produkte, Kundinnen, Finanzen“ → Kundschaft-Ebene ·
„Mega puff“, „Mama-Logistik-Discos“ · „Patricias eigene Tools“ (dritte Person) · „1.500 CHF“ → „1'500 CHF“ ·
toter Link (siehe oben).

**KI-Kurs 🟡** — siehe oben (Frist, Starttag, Anrechnung) · „Du stellst dir keine Software hin. Du stellst jemanden ein“.

**Magnet-Ich 🟡/🟢** — „Fremde Frauen schreiben dir“ → „Leute, die dich noch gar nicht kennen“ ·
Überschrift „STELL DIR VOR“ → „ANGENOMMEN, ES IST DREI WOCHEN SPÄTER“ · viele Grossbuchstaben im Einstieg.

**MBA-Replay 🟡 · MBA-Warteliste 🔴** — siehe oben.

### Mentoring — Produkte und Funnel

**Startklar 🟡** — „verkaufe seit über einem Jahr jeden einzelnen Monat“ (veraltet) · Ebene: „deiner
Wunschkundin“, „Frauen, die du nicht persönlich kennst“, „Bringt mir das Kundinnen?“ → Kundschaft ·
„In einer Woche steht dein Profil“ gegen „Nach einem Nachmittag“, „5 fertige Beiträge“ gegen „drei
Beiträge“ · Antithesen „Dir fehlt keine Strategie. Dir fehlen die Handgriffe.“

**Storyideen 🟡** — „Es liegt nicht daran … — sondern …“, „Dir fehlt keine Disziplin. Dir fehlt ein
Vorrat“, „statt dass du hinterherschreibst“ · „sichtbar werden“ (Blackliste).

**Stimm-Check 🟢** — „Dir fehlt kein besserer Prompt. Deiner KI fehlt, wer du bist.“ ·
„Dieselbe KI. Derselbe Auftrag.“ (Stakkato).

**Stimm-Check-los 🔴 · KI-Masterclass 🔴 · Masterclass-Danke 🔴 · KI-Webinar 🔴** — vergangene Termine
(siehe oben). KI-Webinar zusätzlich: „Content liegt liegen“, „frägst“, „Mompreneurin“, „keinen Bock“.

**Produkt-Ideen-Finder-los 🟡** (Live-Danke-Seite STANDBEIN — nur Text ändern) — „wie du’s an die
Frau bringst“ → „unter die Leute bringst“ · „der Rest ergibt sich fast von selbst“.

**Content-Box 🟢** — „heb sie dir gut ab“ → „auf“ · „Häng solange bei mir auf Instagram rein“ ·
„Instagram-Kundenmaschine“ ohne Link.

### Gratis-Angebote

Querschnitt: Anführungszeichen gemischt („…" statt „…“, teils «»).

**Bio-Check 🟡** — „bleibt sie stehen“ (Kundschaft-Ebene) · Hero steht doppelt · „Keine Copy-Paste-Texte –
sondern …“ · „Keine Kosten. Kein Abo. Keine versteckte Agenda.“

**Fahrplan 🟡** — „kommen die Kundinnen von selbst“ → „melden sich die richtigen Leute“ · Format und Dauer fehlen.

**Lead-Challenge 🟡** — „keine Kundinnen“, „deiner Wunschkundin“, „Interessentinnen“ → Kundschaft-Ebene ·
„Ich begleite dich täglich im Telegram-Kanal“ — läuft das noch live?

**Story-Challenge 🟡** — drei Antithesen in Folge · Nummerierung 1·2·3 neben „7 Tage“ verwirrt.

**Potenzial-Test 🟢/🟡** — „keine Kundinnen“ → „kauft niemand“ · „keinen grösseren Plan – den richtigen Hebel“.

**Dankesseite Potenzial-Quiz 🔴** — Preis 37 statt 39 (dreimal) · „Partnerunternehmen“ vs. „Network“.

**Von 0 auf echt 🟡** — „5 Schritte“ (Formular) gegen „6 Schritte“ (Text) · „Networkbusiness 2.0“ ·
„Du darfst. Du kannst.“ (Stakkato).

**Instagram-Starterguide 🔴** — Ebenenfehler in der Headline: „ein Profil, das deine Wunschkundin
anzieht“ → „das die richtigen Leute anzieht“ · „Stell dir eine Person vor“ · „keine Kundinnen“.

**Freischaufeln 🟡** — „wie einen Termin mit einer Kundin“ · „Das liegt nicht an zu wenig Disziplin.“ ·
„Znüni“ (Mundart).

**Bio 🔴** — Preis 37 statt 39 · Bio-Check „5 Min“ gegen „10 Minuten“ · Mama-Business-Kasse auf test ·
„Made with  in der Schweiz“ (Herz-Icon fehlt).

**Anmeldung-Danke 🔴** — falsche Knappheit · „Du verkaufst nicht mehr – du wirst empfohlen“ ·
„Du brauchst gerade nichts kaufen“ → „musst“.

### doTERRA

**Energieroutine 🟢** — „nicht weniger — nur anders“, „Und fast nie weniger essen“ · „gut ein Jahr“
gegen „3–4 Monate“ auf /energie-kickstart · „kommt einfach nicht mehr“ klingt nach Zusicherung.

**Energie-Kickstart 🟡** — „Kein Druck, kein Verkauf“ gegen Mail-Einwilligung · „Abend-Ritual, das alles ändert“.

**Hormone 🟡** — Energie-Routine ist nirgends verlinkt (Hauptangebot!) · „ins Gleichgewicht bringen“
klingt nach Gesundheitszusage · „Haare im Bürstenkamm“ · „Schreib mir“ Instagram statt WhatsApp.

**Frühstücke 🟢** — zwei zerschnittene Sätze bei den Protein-Pancakes · „Alle 30 Frühstücke“, die Seite zeigt zwölf.

**Hausapotheke 🔴 · Mini-Notfallapotheke 🔴 · doterra 🔴 · startersets 🔴 · mama-energise 🔴** — siehe oben.

**Ölreise 🟡** — erst klären, ob sie noch läuft · „Beschwerden lindern“ · Überschrift „FAQ zum Home Essential Kit“ falsch kopiert.

---

## 🔗 Verwandte Notizen

- [[2026-06-09-claude-tipps-insta-analyse]]
