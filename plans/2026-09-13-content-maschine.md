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
- **Pack-Tag:** **Montag früh** liegt das fertige Wochen-Pack im Cockpit.
- **Blotato-Slot:** Karussells abends **19:00–20:15**.
- **Neuer strategischer Fokus (13.9.):** GroImpact bringt bereits zielgruppengenaue Follower → **kalte Reichweite zweitrangig**, Content muss **tief gehen & verkaufen** (warme Zielgruppe heiss machen). Ideen-Motor entsprechend trimmen.

## Nutzt bereits Bestehendes (kein Neubau)
- **Konkurrenz/Markt:** `apify-scrape.yml` (täglich Watchlist), `apify-discover.yml` (monatlich Top-Creator), `apify-telegram-digest.yml` (So 19:00 Digest). → Marktrecherche-Input.
- **Ideen-Motor:** `/freitag-hooks` (Fr 08:00 voll-auto: Marktanalyse→Hooks→Pick→Build) — wird zum vollen Pack-Generator ausgebaut.
- **Freigabe/Posting:** Cockpit-Artifact (`eeee48d5-…`) + `scripts/cockpit/freigabe-zu-blotato.mjs` (WordPress→Blotato-Media→Post).
- **Video:** `/videoschnitt` (`textebene.py` + HyperFrames: Auto-Zoom, Untertitel, eingeschobene Bilder) + `/handy` (`hol-content.py`).
- **Cover:** Titelbild-Editor `outputs/reels/_titelbild-editor/` (Artifact `21e66e0e-…`) + Render-Pipeline `scripts/karussell-render/`.
- **Scheduler:** GitHub Actions (Secrets liegen: ANTHROPIC_API_KEY, BLOTATO_API_KEY, NOTION_TOKEN, TELEGRAM_*, APIFY_API_TOKEN).

## Wochen-Ablauf (Ziel)
| Wann | Automatisch | Patricias Aufwand |
|---|---|---|
| So abend | Konkurrenz-Scrape + Digest | – |
| **Mo früh** | Wochen-Pack ins Cockpit: Markt-Kurzfassung · 2 Karussells (Slide-Texte) · B-Roll-Reels (Hook+Caption+Clip-Wahl) · Talking-Head-Reels **mit Sprechtext** · Cover-Vorschläge · doTERRA-Pack getrennt | – |
| Mo–Di | Cockpit durchschauen, Texte ggf. ändern, **GO** | ~10 Min |
| laufend | Talking-Heads: Sprechtexte ablesen, Clips in `DCIM/Content-Inbox` | 1× filmen |
| nach Clip | Auto: `hol-content` → `videoschnitt` (finish.json auto: Untertitel+Zoom+geplante Inserts) → fertige Reels+Cover auf Telegram | – |
| abends 19–20:15 | Karussells via Blotato raus | – |

**Harte Grenze (ehrlich):** Talking-Head-Reels brauchen Patricia **einmal vor der Kamera** (Gesicht/Stimme). Danach kein weiterer Input nötig. B-Roll + Karussells brauchen sie gar nicht (ausser GO).

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

### Phase 3 — Talking-Head-Auto-Loop
- Trigger: neue Clips in `Content-Inbox` (oder Patricia sagt „Clips sind drin").
- Auto: `hol-content` → Zuordnung Clip↔geplantes Reel → `textebene.py` mit **auto-generiertem finish.json** (Untertitel, Auto-Zoom, Hook-Overlay immer; Spezial-Inserts wie Backoffice-Mockup wenn im Briefing vorgesehen) → Render → Telegram + Cockpit.

## Offene Technik-Fragen (beim Bauen klären)
- Rendering (HyperFrames/ffmpeg) läuft heute **lokal** (Patricias PC). Für Voll-Auto entweder: (a) Render-Schritt bleibt lokal/in-Session wenn Clips da sind, oder (b) GitHub-Action-Runner mit ffmpeg+Chromium. Karussell-PNG-Render ist leichter → eher automatisierbar als Video.
- Blotato-Account-IDs für beide Profile prüfen.
- Cockpit-DB-Schema für „Entwürfe pro Woche" festlegen (Sammlung `wochenpack`?).

## SSOT-Hinweis
Dieses System darf **nie nur in einem Chat leben**. Jeder gebaute Teil kommt ins Repo (Skripte in `scripts/`, Editor in `outputs/reels/_titelbild-editor/`, Workflows in `.github/workflows/`). Dieser Plan ist die Landkarte.
