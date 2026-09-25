---
tags: [produkt, funnel, freebie, ki, plan]
---

# Stimm-Check bauen — Übergabe für einen neuen Chat

**Stand:** 25.09.2026 · **Status:** entschieden, noch nicht gebaut
**Zweck:** 0€-Freebie der KI-Treppe und Leadmagnet für den KI-Kurs-Launch
(Aufwärmen ab Mo 28.9., Secret Offer Mo 5.10.). **Je früher live, desto mehr Frauen
sind vor dem Secret Offer auf der Liste.**

## Was der Stimm-Check ist

Aus `outputs/produkte/ki-treppe/01-produkttreppe.md`, Stufe 1:

- **Titel:** Der Stimm-Check
- **Unterzeile:** Die sechs Sätze, die deine KI von dir braucht, damit sie klingt wie du
- **Format:** interaktives Tool, Bauart Bio-Check / Freischaufeln, rund 15 Minuten
- **Painpoint:** Die Texte klingen nach irgendwem. Meist merkt sie es erst, wenn der
  Post schon draussen ist.
- **Ergebnis (A→B):** ein Dokument, das sie vor jeden KI-Auftrag kopieren kann, und ein
  erster Text, den sie so posten würde
- **Brücke am Schluss:** „Das war einer. Die Arbeit, die du jede Woche wieder machst,
  geht genauso.“ → Warteliste bzw. ab 5.10. Verkaufsseite des KI-Kurses
- **Stichwort:** `STIMME` (im Plan) — 🚨 im Launch-Kalender ist `MITARBEITERIN` das
  Launch-Stichwort. Zwei Stichwörter oder eins entscheiden, bevor ManyChat gebaut wird.

## Vorlage zum Nachbauen

`scripts/freischaufeln/` ist bereits ein Zwilling vom Bio-Check und wird kopiert:
- `public/index.html` — geführte Web-App
- `api/generate.js` — Claude-Proxy
- `api/tag.js` — AC-Tags (Abschluss + Interesse)
- `lib/system-prompt.md` — das Gehirn (Stimme, Regeln, JSON-Vertrag)
- Deploy-Anleitung: `scripts/freischaufeln/README.md` (Vercel + ENV)
- Bauplan-Muster: `plans/2026-07-04-freischaufeln-freebie.md`
- Landingpage-Muster: `mumlifebalance.ch/freischaufeln` · ManyChat-Muster:
  `outputs/funnels/freischaufeln/manychat-flow-ZEITFENSTER.md`

## Was zu tun ist

| # | Was | Wer |
|---|---|---|
| 1 | Die sechs Angaben festlegen (Inhalt des Checks) — Quelle: Kapitel „Stimme“ im KI-Kurs-Konzept `outputs/produkte/ki-treppe/02-kurs-konzept.md` | Claude, Patricia gibt frei |
| 2 | Tool bauen: `scripts/stimm-check/` aus Freischaufeln kopieren, Ablauf + System-Prompt umschreiben, lokal testen | Claude |
| 3 | AC: Tags `Stimm-Check Lead` + `Stimm-Check abgeschlossen`, Formular, Auslieferungs-Mail | Claude baut, Patricia schaltet frei |
| 4 | WP-Landingpage `/stimm-check/` als Entwurf | Claude |
| 5 | Vercel-Deploy + ENV (Anthropic-Key, AC-Key, Tag-IDs) | Patricia (Schlüssel nie in den Chat) |
| 6 | ManyChat-Stichwort + Flow | Claude baut, Patricia schaltet frei |
| 7 | Nurture: nach dem Check in die KI-Kurs-Warteliste; nach dem Launch → KI-Auftragsbuch 39 | Claude |
| 8 | Eintrag in `context/active-funnels.json` + `context/link-uebersicht.md` + CLAUDE.md | Claude |

## Zu beachten

- 🚨 **Das Karussell vom Di 20.10.** im Launch-Kalender gibt den Stimm-Check-Inhalt
  gratis heraus („Sechs Angaben, die jede KI von dir braucht“). Thema tauschen, sobald
  der Stimm-Check live ist.
- Regeln wie bei allen Kundendokumenten: keine fremden Mentorinnen, Schweizer ss, echte
  Umlaute, kein Stakkato, keine erfundenen Zahlen, keine Geld-zurück-Garantie.
- Die Seite ist öffentlich → keine Personendaten, keine Schlüssel im Code.

## Einstieg im neuen Chat

> „Bitte lies `plans/2026-09-25-stimm-check-bauen.md` und bau den Stimm-Check.“
