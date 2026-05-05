# Mama-CEO Webinar-Mail-Sequenz — Übersicht

**Letzte Aktualisierung:** 2026-05-05 (14 Mails · 2-Phasen-Cart)
**Webinar:** „In 90 Min: Dein Mama-Leben mit KI-Assistenten umkrempeln" · Mi 20.5.2026 · 09:00
**Cart-Logik (2-Phasen):**
- 🟠 Mi 20.5. 11:00 → Sa 23.5. 23:59 = **Earlybird CHF 249** (3 Tage)
- 🔵 So 24.5. 00:00 → So 31.5. 23:59 = **Final CHF 333** (8 Tage)
- 🚀 Mo 1.6.2026 = **Pilot-Phase Start**

---

## Sequenz auf einen Blick (14 Mails)

| # | Mail | Wann | An wen | Datei |
|---|---|---|---|---|
| 1 | **Anmelde-Bestätigung** | Sofort nach Anmeldung | Neuer Anmelder | `01-bestaetigung.html` |
| 2 | **In 1 Woche LIVE** | Mi 13.5. 14:00 | Ganze Liste | `02-1woche-vorher.html` |
| 3 | **Reminder 24h** | Di 19.5. 09:00 | Webinar-Anmelder | `03-reminder-24h.html` |
| 4 | **Reminder 1h** | Mi 20.5. 08:00 | Webinar-Anmelder | `04-reminder-1h.html` |
| 5 ⭐ | **CLIFFHANGER LIVE** | Mi 20.5. 09:15 | **GANZE LISTE** (ohne Anmelder) | `05-cliffhanger-live.html` |
| 6 | **Cart-Open + Replay** | Mi 20.5. 11:00 | Ganze Liste | `06-cart-open.html` |
| 7 | **Painpoint + Aha-KI** | Do 21.5. 08:00 | Liste (ohne Käufer) | `07-painpoint.html` |
| 8 | **Earlybird endet heute (16h)** | Sa 23.5. 08:00 | Liste (ohne Käufer) | `08-earlybird-end-morgens.html` |
| 9 | **Earlybird endet (2h)** | Sa 23.5. 22:00 | Liste (ohne Käufer) | `09-earlybird-end-last2h.html` |
| 10 | **Earlybird vorbei · Cart läuft** | So 24.5. 09:00 | Liste (ohne Käufer) | `10-earlybird-vorbei.html` |
| 11 | **Antikunden / Wer es NICHT ist** | Mi 27.5. 08:00 | Liste (ohne Käufer) | `11-midweek-antikunden.html` |
| 12 | **Letzte Tage · Persönlicher Brief** | Fr 29.5. 08:00 | Liste (ohne Käufer) | `12-letzte-tage.html` |
| 13 | **Cart-Close-Morgens (16h)** | So 31.5. 08:00 | Liste (ohne Käufer) | `13-close-morgens.html` |
| 14 | **Cart-Close-Last-2h** | So 31.5. 22:00 | Liste (ohne Käufer) | `14-close-letzte2h.html` |

---

## Zeitlicher Ablauf

```
KW 19 (4.-10.5.)    Aufwärmphase 1 — Validierung
KW 20 (11.-17.5.)
   Mi 13.5. 14:00    Mail 2 → Ganze Liste (1 Wo vor Webinar)
KW 21 (18.-24.5.)   Webinar + Earlybird-Phase
   Di 19.5. 09:00    Mail 3 → Anmelder (24h Reminder)
   Mi 20.5. 08:00    Mail 4 → Anmelder (1h Reminder + Zoom)
   Mi 20.5. 09:00    🎤 KI-WEBINAR LIVE
   Mi 20.5. 09:15    Mail 5 → Liste (Cliffhanger)
   Mi 20.5. 10:30    Webinar-Ende
   Mi 20.5. 11:00    Mail 6 → Liste (Cart-Open EARLYBIRD)
   Do 21.5. 08:00    Mail 7 → Liste (Painpoint + Aha-KI)
   Sa 23.5. 08:00    Mail 8 → Liste (Earlybird endet heute)
   Sa 23.5. 22:00    Mail 9 → Liste (Earlybird Last 2h)
   Sa 23.5. 23:59    🟠 EARLYBIRD ENDE · Preis-Switch CHF 249 → 333
KW 22 (25.-31.5.)   Final-Phase
   So 24.5. 09:00    Mail 10 → Liste (Earlybird vorbei, Cart läuft)
   Mi 27.5. 08:00    Mail 11 → Liste (Antikunden / Wer es nicht ist)
   Fr 29.5. 08:00    Mail 12 → Liste (Persönlicher Brief)
   So 31.5. 08:00    Mail 13 → Liste (Heute Cart-Close, 16h)
   So 31.5. 22:00    Mail 14 → Liste (Last 2h)
   So 31.5. 23:59    🚨 CART-CLOSE ENDGÜLTIG
Mo 1.6.              🚀 Pilot-Phase Start (Onboarding-Mail an Käuferinnen)
```

---

## AC-Setup-Übersicht (kurz)

**Tags die du brauchst:**
- `mama-ceo-webinar-anmeldung` (wird durch das Form gesetzt) ✓
- `mama-ceo-webinar-live-teilnehmer` (manuell setzen wer am Webinar live war)
- `mama-ceo-webinar-kauf` (wird gesetzt wenn jemand Mama-CEO via ThriveCart kauft)

**3 Automations:**
1. **Webinar-Anmelder-Sequenz** (Mails 1, 3, 4) — Trigger: Tag `mama-ceo-webinar-anmeldung`
2. **Webinar-Day Mass-Send** (Mails 2, 5, 6) — Trigger: Datum (an Liste)
3. **Cart-Window-Sequenz** (Mails 7-14) — Trigger: Datum, exclude `mama-ceo-webinar-kauf`

**Voll-Anleitung:** Siehe `99-AC-SETUP.md`

---

## Brand-Design

Alle Mails sind im offiziellen `mail-design-onlinebusiness.html` Template gebaut:
- **Header:** Petrol-Gradient mit Eyebrow-Tag (Orange) + Headline (Creme, Georgia) + Subheadline (italic)
- **Body:** Weisser Hintergrund mit Pull-Quotes (Creme + Orange-Border), Info-Boxes (Türkis-Light), CTA-Buttons (Orange/Dunkelblau)
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
| `{{first_name}}` | Alle 14 Mails | AC-Variable für Vornamen einsetzen (in AC: Personalisations-Tag) |
| `https://us02web.zoom.us/j/DEIN-ZOOM-LINK` | Mails 4, 5 | Echter Zoom-Webinar-Link |
| `[Mama-CEO Cart-Link]` | Mails 6-14 | ThriveCart-Cart-URL |
| `[Replay-Link]` | Mail 6 | Vimeo-Replay-URL (passwortgeschützt, 48h) |

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

## Warum 14 Mails (statt 12 oder 18)?

**Gegen 18 Mails:** Patricias Bauchgefühl — „arg viel" für 3-Wochen-Window. 14 Mails respektiert das.
**Gegen 12 Mails:** 2-Phasen-Cart braucht eine Final-Phase-Sequenz (5 Mails: Earlybird-vorbei, Antikunden, Letzte-Tage, Close-Morgens, Close-2h). Sonst verliert man den 8-Tage-Cart-Window.

**Kompromiss:**
- Aufwärmphase verschlankt (5 statt 6 — keine separate Story-Mail, in Mail 2 integriert)
- Cliffhanger bleibt (das ist der Killer)
- Earlybird kompakt (3 Mails: Cart-Open, Painpoint, Earlybird-End-2x)
- Final-Phase mit 5 Mails (Earlybird-vorbei, Antikunden, Persönlicher Brief, Close-2x)

---

**Nächste Schritte für Patricia:**
1. Lies eine Mail nach der anderen, prüf Voice
2. Wenn alles passt: AC-Setup nach `99-AC-SETUP.md` einrichten
3. Test-Anmeldung machen (Mail 1 sollte ankommen)
4. Bei Fragen / Anpassungen: sag bescheid
