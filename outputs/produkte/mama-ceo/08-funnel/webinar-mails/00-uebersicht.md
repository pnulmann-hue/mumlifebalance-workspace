# Mama-CEO Webinar-Mail-Sequenz — Übersicht

**Letzte Aktualisierung:** 2026-05-04 (3-Tage-Cart Variante)
**Webinar:** „In 90 Min: Dein Mama-Leben mit KI-Assistenten umkrempeln" · Mi 20.5.2026 · 09:00
**Cart:** Mi 20.5. 09:00 → **Sa 23.5. 23:59** · Earlybird CHF 249 (3 Tage)
**Pilot-Phase Start:** Mo 1.6.2026

---

## Sequenz auf einen Blick (12 Mails)

| # | Mail | Wann | An wen | Datei |
|---|---|---|---|---|
| 1 | **Anmelde-Bestätigung** | Sofort nach Anmeldung | Neuer Anmelder | `01-bestaetigung.html` |
| 2 | **In 1 Woche LIVE** | Mi 13.5. 14:00 | Ganze Liste | `02-1woche-vorher.html` |
| 3 | **Story-Mail (Brandastic)** | So 17.5. 09:00 | Webinar-Anmelder | `03-story-3tage.html` |
| 4 | **Reminder 24h** | Di 19.5. 09:00 | Webinar-Anmelder | `04-reminder-24h.html` |
| 5 | **Reminder 1h** | Mi 20.5. 08:00 | Webinar-Anmelder | `05-reminder-1h.html` |
| 6 ⭐ | **CLIFFHANGER LIVE** | Mi 20.5. 09:15 | **GANZE LISTE** (ohne Anmelder) | `06-cliffhanger-live.html` |
| 7 | **Cart-Open + Replay** | Mi 20.5. 11:00 | Ganze Liste | `07-cart-open.html` |
| 8 | **Painpoint-Tag** | Do 21.5. 08:00 | Liste (ohne Käufer) | `08-painpoint.html` |
| 9 | **Aha-Tag (KI-Demo)** | Fr 22.5. 08:00 | Liste (ohne Käufer) | `09-aha-ki.html` |
| 10 | **Cart-Close-Morgens** | Sa 23.5. 08:00 | Liste (ohne Käufer) | `10-close-morgens.html` |
| 11 | **Cart-Close-Abends** | Sa 23.5. 18:00 | Liste (ohne Käufer) | `11-close-abends.html` |
| 12 | **Cart-Close-Last-2h** | Sa 23.5. 22:00 | Liste (ohne Käufer) | `12-close-letzte2h.html` |

---

## Zeitlicher Ablauf

```
KW 19 (4.-10.5.)    Aufwärmphase 1 — Validierung
KW 20 (11.-17.5.)
   Mi 13.5. 14:00    Mail 2 → Ganze Liste (1 Wo vor Webinar)
   So 17.5. 09:00    Mail 3 → Anmelder (Story)
KW 21 (18.-24.5.)
   Di 19.5. 09:00    Mail 4 → Anmelder (24h Reminder)
   Mi 20.5. 08:00    Mail 5 → Anmelder (1h Reminder + Zoom)
   Mi 20.5. 09:00    🎤 KI-WEBINAR LIVE
   Mi 20.5. 09:15    Mail 6 → Liste (Cliffhanger)
   Mi 20.5. 10:30    Webinar-Ende
   Mi 20.5. 11:00    Mail 7 → Liste (Cart-Open + Replay)
   Do 21.5. 08:00    Mail 8 → Liste (Painpoint)
   Fr 22.5. 08:00    Mail 9 → Liste (Aha KI, „morgen schliesst")
   Sa 23.5. 08:00    Mail 10 → Liste (Close-Morgens, 16h)
   Sa 23.5. 18:00    Mail 11 → Liste (Close-Abends, 6h)
   Sa 23.5. 22:00    Mail 12 → Liste (Last 2h)
   Sa 23.5. 23:59    🚨 CART-CLOSE
KW 22 (25.-31.5.)    Pilot-Käuferinnen-Onboarding
Mo 1.6.              🚀 Pilot-Phase Start
```

---

## AC-Setup-Übersicht (kurz)

**Tags die du brauchst:**
- `mama-ceo-webinar-anmeldung` (wird durch das Form gesetzt) ✓
- `mama-ceo-webinar-live-teilnehmer` (manuell setzen wer am Webinar live war)
- `mama-ceo-webinar-kauf` (wird gesetzt wenn jemand Mama-CEO via ThriveCart kauft)

**3 Automations:**
1. **Webinar-Anmelder-Sequenz** (Mails 1, 3, 4, 5) — Trigger: Tag `mama-ceo-webinar-anmeldung`
2. **Webinar-Day Mass-Send** (Mails 2, 6, 7) — Trigger: Datum (an Liste)
3. **Cart-Window-Sequenz** (Mails 8-12) — Trigger: Datum

**Voll-Anleitung:** Siehe `99-AC-SETUP.md`

---

## Brand-Design

Alle Mails sind im offiziellen `mail-design-onlinebusiness.html` Template gebaut:
- **Header:** Petrol-Gradient mit Eyebrow-Tag (Orange) + Headline (Creme, Georgia) + Subheadline (italic)
- **Body:** Weißer Hintergrund mit Pull-Quotes (Creme + Orange-Border), Info-Boxes (Türkis-Light), CTA-Buttons (Orange)
- **Footer:** Dunkelblau mit „MUMLIFEBALANCE · PATRICIA ULMANN"

**Brand-Farben:**
- `#0c1c30` Text-Dunkel
- `#29556d` Dunkelblau
- `#12828c` Petrol
- `#f1ecdd` Creme
- `#dc822e` Orange
- `#e4f3f4` Türkis-Light

---

## Platzhalter die du noch ersetzen musst

| Platzhalter | In welchen Mails | Was eintragen |
|---|---|---|
| `{{first_name}}` | Alle 12 Mails | AC-Variable für Vornamen einsetzen (in AC: Personalisations-Tag) |
| `https://us02web.zoom.us/j/DEIN-ZOOM-LINK` | Mails 5, 6 | Echter Zoom-Webinar-Link |
| `[Mama-CEO Cart-Link]` | Mails 7-12 | ThriveCart-Cart-URL |
| `[Replay-Link]` | Mail 7 | Vimeo-Replay-URL (passwortgeschützt, 48h) |

---

## Prinzipien die in jeder Mail drin sind (Sternbauer + Julia Trost)

✅ **Vorher-Nachher** — Schmerz benennen → Lösung zeigen
✅ **EIN klarer CTA** pro Mail
✅ **Resultate, nicht Methoden** — was hat die Leserin am Ende?
✅ **Storytelling** — Problem → Höhepunkt → Lösung
✅ **Patricia-Voice** — Du-Form, ss statt ß, Schweizer
✅ **Authentizität** — wie zu einer Freundin
✅ **Brandastic-Anker** — Schwester-Tod-Aha als Tiefen-Story
✅ **P.S.** — als emotionaler Anker oder Scarcity-Push

---

## Was nicht drin ist (im Vergleich zu Original-16-Mail-Plan)

❌ **Sozial-Beweis-Mail** (Sa 23.5. ursprünglich) — fällt weg, weil noch keine Pilot-Käuferinnen-Quotes verfügbar sind
❌ **Replay-läuft-aus-Mail** — nicht nötig, da Replay parallel zum 3-Tage-Cart aussläuft
❌ **Letzte-Tage-Mail / Final-Push** — fällt weg, da 3-Tage-Cart schon kompakt genug ist

→ Resultat: 12 Mails statt 16. Klare Knappheit. Kein Plot-Filler.

---

**Nächste Schritte für Patricia:**
1. Lies eine Mail nach der anderen, prüf Voice
2. Wenn alles passt: AC-Setup nach `99-AC-SETUP.md` einrichten
3. Test-Anmeldung machen (Mail 1 sollte ankommen)
4. Bei Fragen / Anpassungen: sag bescheid
