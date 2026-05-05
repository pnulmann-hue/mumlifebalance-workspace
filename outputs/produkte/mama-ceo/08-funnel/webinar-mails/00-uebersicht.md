# Mama-CEO Webinar-Mail-Sequenz — Übersicht

**Letzte Aktualisierung:** 2026-05-04
**Webinar:** „In 90 Min: Dein Mama-Leben mit KI-Assistenten umkrempeln" · Mi 20.5.2026 · 09:00
**Cart:** Mi 20.5. 09:00 → Mi 27.5. 23:59 · Earlybird CHF 249

---

## Sequenz auf einen Blick

| # | Mail | Wann | An wen | Datei |
|---|---|---|---|---|
| 1 | **Anmelde-Bestätigung** | Sofort nach Anmeldung | Neuer Anmelder | `01-bestaetigung.html` |
| 2 | **In 1 Woche LIVE** | Mi 13.5. 14:00 | Ganze Liste | `02-1woche-vorher.html` |
| 3 | **Story-Mail (Brandastic)** | So 17.5. 09:00 | Webinar-Anmelder | `03-story-3tage.html` |
| 4 | **Reminder 24h** | Di 19.5. 09:00 | Webinar-Anmelder | `04-reminder-24h.html` |
| 5 | **Reminder 1h** | Mi 20.5. 08:00 | Webinar-Anmelder | `05-reminder-1h.html` |
| 6 ⭐ | **CLIFFHANGER LIVE** | Mi 20.5. 09:15 | **GANZE LISTE** | `06-cliffhanger-live.html` |
| 7 | **Cart-Open + Replay** | Mi 20.5. 11:00 | Anmelder + Liste | `07-cart-open.html` |
| 8 | **Painpoint-Tag** | Do 21.5. 08:00 | Liste | `08-painpoint.html` |
| 9 | **Aha-Tag (KI-Demo)** | Fr 22.5. 08:00 | Liste | `09-aha-ki.html` |
| 10 | **Sozial-Beweis** | Sa 23.5. 08:00 | Liste | `10-sozialbeweis.html` |
| 11 | **Replay läuft aus** | So 24.5. 09:00 | Liste | `11-replay-aus.html` |
| 12 | **Letzte-Tage-Mail** | Mo 25.5. 09:00 | Liste | `12-letzte-tage.html` |
| 13 | **Final-Push + Antikunden** | Di 26.5. 09:00 | Liste | `13-final-push.html` |
| 14 | **Cart-Close-Tag 08:00** | Mi 27.5. 08:00 | Liste | `14-close-morgens.html` |
| 15 | **Cart-Close-Tag 18:00** | Mi 27.5. 18:00 | Liste | `15-close-abends.html` |
| 16 | **Cart-Close-Tag 22:00** | Mi 27.5. 22:00 | Liste | `16-close-letzte2h.html` |

---

## AC-Setup-Übersicht (kurz)

**Tags die du brauchst:**
- `mama-ceo-webinar-anmeldung` (wird durch das Form gesetzt) ✓
- `mama-ceo-webinar-live-teilnehmer` (manuell setzen wer am Webinar live war)
- `mama-ceo-webinar-replay-watcher` (manuell oder via Vimeo-Tracking)
- `mama-ceo-webinar-kauf` (wird gesetzt wenn jemand Mama-CEO via ThriveCart kauft)

**3 Automations:**
1. **Webinar-Anmelder-Sequenz** (Mails 1, 3, 4, 5) — Trigger: Tag `mama-ceo-webinar-anmeldung`
2. **Webinar-Day Mass-Send** (Mails 2, 6) — Trigger: Datum (an Liste)
3. **Cart-Window-Sequenz** (Mails 7-16) — Trigger: Webinar-Datum erreicht

**Voll-Anleitung:** Siehe `99-AC-SETUP.md`

---

## Prinzipien die in jeder Mail drin sind (Sternbauer + Julia Trost)

✅ **Vorher-Nachher** — Schmerz benennen → Lösung zeigen
✅ **EIN klarer CTA** pro Mail — keine Doppelung
✅ **Resultate, nicht Methoden** — was hat die Leserin am Ende?
✅ **Storytelling** — Problem → Höhepunkt → Lösung
✅ **Patricia-Voice** — Du-Form, ss statt ß, Schweizer
✅ **Authentizität** — wie zu einer Freundin
✅ **Brandastic-Anker** — Schwester-Tod-Aha als Tiefen-Story
✅ **P.S.** — als emotionaler Anker oder Scarcity-Push

---

## Brand-Voice-Reminder

**Patricia spricht:**
- Direkt: „Du", nie „Sie"
- Mit Punch: kurze Sätze + konkreten Bildern
- Ehrlich: keine Buzzwords, keine generischen KI-Phrasen
- Empathisch: kennt den Mama-Mental-Load aus eigenem Erleben
- Konkret: Zahlen + echte Beispiele (4 Kids, 6 Personen, Migros, Garten)

**Patricia spricht NICHT:**
- „Skalieren", „Funnel optimieren", „Mindset shiften" → zu Coaching-Sprache
- Künstliche Empathie („Ich verstehe genau wie du dich fühlst...")
- Generische Versprechen („Verändere dein Leben in 7 Tagen!")

---

**Nächste Schritte für Patricia:**
1. Lies eine Mail nach der anderen, prüf Voice
2. Wenn alles passt: AC-Setup nach `99-AC-SETUP.md` einrichten
3. Test-Anmeldung machen (Mail 1 sollte ankommen)
4. Bei Fragen / Anpassungen: sag bescheid
