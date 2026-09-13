---
tags: [plan, automation, content]
---

# Content-Maschine — vollautomatisches Wochen-Content-System

**Erstellt:** 2026-09-13 · **Auftrag:** Patricia will ein System, das sie **so gut wie keine Zeit kostet** und trotzdem **richtig guten, konvertierenden Content** liefert. Claude hat alles Wissen (PIE, Content-Regeln, Compliance, Voice, Funnels).

## Entscheidungen (von Patricia bestätigt)
- **Profile:** beide (@mumlifebalance Mentoring **+** doTERRA, sauber getrennt nach Compliance/Themen).
- **Menge Mentoring:** 2 Karussells + 3 Reels/Woche werden GEPOSTET (Di+Do Karussell, Mo/Mi/Fr Reels; Mix B-Roll + Talking-Head).
- **ABER Pack = Überangebot:** Claude legt **~5 Karussells + ~5 Reels** als Vorschläge ins Cockpit. Patricia gibt die besten frei; **nicht gewählte wandern in den Vorrat** (`wochenpack`-Backlog) für die Folgewoche. Kein Ideen-Verschleiss.
- **Qualitätslatte hoch:** jeder Vorschlag stark konvertierend — Expertise + Julia-Trost-Methodik (PIE, Reels-to-Cash, Stories-die-verkaufen), nicht Füllmaterial.
- **Produktions-Tag: jeden FREITAG automatisch** — Claude produziert das komplette Paket für die **nächste** Woche und legt es fixfertig ins Artefakt/Cockpit. (Ersetzt die frühere „Montag früh"-Idee.)
- **Wochenthema-Check:** Das Paket richtet sich nach dem **definierten aktuellen Wochenthema**. Ist keins definiert/klar → Claude schickt Patricia **von selbst eine Nachricht** „Wochenthema fehlt, lass uns das kurz festlegen", ohne dass sie sonst etwas tun muss. Kein Blind-Produzieren.
- **Blotato-Slot:** Karussells abends **19:00–20:15**.
- **Neuer strategischer Fokus (13.9.):** GroImpact bringt bereits zielgruppengenaue Follower → **kalte Reichweite zweitrangig**, Content muss **tief gehen & verkaufen** (warme Zielgruppe heiss machen). Ideen-Motor entsprechend trimmen.

## Nutzt bereits Bestehendes (kein Neubau)
- **Konkurrenz/Markt:** `apify-scrape.yml` (täglich Watchlist), `apify-discover.yml` (monatlich Top-Creator), `apify-telegram-digest.yml` (So 19:00 Digest). → Marktrecherche-Input.
- **Ideen-Motor:** `/freitag-hooks` (Fr 08:00 voll-auto: Marktanalyse→Hooks→Pick→Build) — wird zum vollen Pack-Generator ausgebaut.
- **Freigabe/Posting:** Cockpit-Artifact (`eeee48d5-…`) + `scripts/cockpit/freigabe-zu-blotato.mjs` (WordPress→Blotato-Media→Post).
- **Video:** `/videoschnitt` (`textebene.py` + HyperFrames: Auto-Zoom, Untertitel, eingeschobene Bilder) + `/handy` (`hol-content.py`).
- **Cover:** Titelbild-Editor `outputs/reels/_titelbild-editor/` (Artifact `21e66e0e-…`) + Render-Pipeline `scripts/karussell-render/`.
- **Scheduler:** GitHub Actions (Secrets liegen: ANTHROPIC_API_KEY, BLOTATO_API_KEY, NOTION_TOKEN, TELEGRAM_*, APIFY_API_TOKEN).

## Wochen-Ablauf (Ziel-Spezifikation, von Patricia 2026-09-13)
| Wann | Automatisch (Claude) | Patricias Aufwand |
|---|---|---|
| So abend | Konkurrenz-Scrape + Markt-Digest | – |
| **FR** | Wochenthema prüfen. Unklar/fehlt → **Nachricht an Patricia** „lass uns das Wochenthema festlegen" (sonst nichts). Sonst: **5 Reels + 5 Karussells fürs nächste Woche** fixfertig ins Artefakt/Cockpit (Texte, Reel-Cover, Karussell-Slides), passend zum Wochenthema, beide Profile | – |
| FR/SA | Im Artefakt durchsehen: Texte, Cover, Karussells — **Datum je Post setzen** → **Knopf „Veröffentlichen"** | ~10–15 Min |
| nach „Veröffentlichen" | **Sprechreels + Karussells** postet Claude automatisch (Blotato, zu den gesetzten Daten). **B-Roll-Reels + Reel-Cover** → **Telegram** an Patricia → sie plant sie selbst ein | B-Roll selbst einplanen |

**Posting-Split (verbindlich):**
- **Sprechreels (mit Stimme) → Claude postet automatisch** (kein Trending-Sound nötig).
- **Karussells → Claude postet automatisch.**
- **B-Roll-Reels + Cover → Telegram an Patricia**, sie plant sie selbst (wegen Trending-Sound in der App).

**Harte Grenze (ehrlich):** Sprechreels brauchen **gefilmtes Material**. Für den automatischen Freitag-Lauf muss ein **Vorrat an Sprech-Clips** da sein (Wissens-Dump in `DCIM/Sprechreels`) — daraus schneidet Claude. Vorrat leer → für die Sprechreel-Slots kommen **Sprechtexte zum Ablesen** statt fertiger Videos. Karussells + B-Roll brauchen kein Filmen.

## Bau-Phasen
### Phase 1 — „A"-Automatik (Freigabe→Auto-Output)
- Titelbild-Editor ↔ Cockpit: Cover-Einstellungen (Bild/Farbe/Hook/Slide-Texte) werden gespeichert (`Artifact write_db`), Claude liest sie (`read_db`) und rendert serverseitig — **kein Download für Patricia**.
- Karussell-GO → render Slides+Cover → `freigabe-zu-blotato.mjs` (Slot 19–20:15).
- Reel fertig → Telegram (Video+Cover).
- **Status:** in Arbeit.

### Phase 2 — Wochen-Ideen-Pack-Generator (Mo früh)
- GitHub Action ruft Claude (API) mit allen Kontext-Dateien (Monatsplan, `active-funnels.json`, PIE/hook-framework, Content-Radar, apify-Digest, Compliance-Memorys, Energie-Story für doTERRA).
- Erzeugt pro Profil ein **Überangebot** (~5 Karussells + ~5 Reels: Slide-Texte, B-Roll-Hooks+Captions, Talking-Head-Sprechtexte, Cover-Vorschläge) → schreibt in Cockpit-DB als Entwürfe. Patricia wählt; Rest bleibt als Vorrat (`wochenpack`-Backlog) für Folgewochen.
- Regeln: PIE-Mix, Feed-Aesthetic ABAB, Caption-Standard-Schluss, keine erfundenen Zahlen, doTERRA-Compliance, **stark konvertierend** (Julia-Trost-Methodik + Patricia-Expertise) statt kalt-reichweitig.

### Phase 3 — Sprechreel-/Talking-Head-Auto-Loop
- **Eigenes Handy-Album `DCIM/Sprechreels`** (getrennt von Content-Inbox). Abholung:
  `python scripts/handy/hol-content.py --album Sprechreels --ziel-video video/sprechreels`
  (`--ziel-video` am 2026-09-13 zu hol-content.py hinzugefügt; `video/sprechreels/` ist gitignored).
- **Zwei Aufnahme-Arten:** (1) **Wissens-Dump** — Patricia spricht 10–20 Min frei ihr Wissen/ihre Strategie ein → Claude transkribiert, fischt die stärksten Nuggets, schneidet **viele** Reels + nutzt das Transkript als Treibstoff für den Ideen-Motor (authentische, konvertierende Inhalte in ihrer Stimme). (2) **Geplante Sprechreels** — Sprechtext aus dem Wochen-Pack ablesen.
- Trigger: täglicher Abhol-Check (wenn PC läuft; Zeit noch festzulegen) **oder** Patricia sagt „Sprechreels sind drin".
- Auto: abholen → `textebene.py` mit **auto-generiertem finish.json** (Untertitel, Auto-Zoom, Hook-Overlay immer; Spezial-Inserts wie Backoffice-Mockup wenn im Briefing vorgesehen) → Render → Telegram + Cockpit.
- **Dreh-Anleitung** (Position, Kamera, in-die-Linse, Abwechslung): `context/sprechreels-drehanleitung.md`.

## Offene Technik-Fragen (beim Bauen klären)
- Rendering (HyperFrames/ffmpeg) läuft heute **lokal** (Patricias PC). Für Voll-Auto entweder: (a) Render-Schritt bleibt lokal/in-Session wenn Clips da sind, oder (b) GitHub-Action-Runner mit ffmpeg+Chromium. Karussell-PNG-Render ist leichter → eher automatisierbar als Video.
- Blotato-Account-IDs für beide Profile prüfen.
- Cockpit-DB-Schema für „Entwürfe pro Woche" festlegen (Sammlung `wochenpack`?).

## SSOT-Hinweis
Dieses System darf **nie nur in einem Chat leben**. Jeder gebaute Teil kommt ins Repo (Skripte in `scripts/`, Editor in `outputs/reels/_titelbild-editor/`, Workflows in `.github/workflows/`). Dieser Plan ist die Landkarte.
