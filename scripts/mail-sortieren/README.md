# Mail-Sortierung für GMX und info@

Sortiert die ungelesenen Mails im Posteingang von **pnulmann@gmx.ch** und
**info@mumlifebalance.ch** nach denselben Regeln wie beim Gmail-Aufräumen
vom 01.10.2026. Läuft nur mit der Python-Standardbibliothek.

```bash
python scripts/mail-sortieren/sortieren.py             # Probelauf, verschiebt nichts
python scripts/mail-sortieren/sortieren.py --los       # wirklich sortieren
python scripts/mail-sortieren/sortieren.py --nur gmx   # nur ein Postfach (gmx | info)
python scripts/mail-sortieren/sortieren.py --alle      # auch schon gelesene Mails
```

| Wohin | Was |
|---|---|
| `Sortiert/Newsletter und Werbung` | Newsletter, Shops, fremde Kurs-Werbung, doTERRA-Werbung |
| `Sortiert/Technik und Bots` | GitHub, Vercel, Blotato, Supabase … ohne Fehlermeldung |
| `Sortiert/Finanzen` | Rechnungen, Quittungen, Zahlungen (Belege für die Steuer) |
| `Sortiert/Rezepte` · `Sortiert/Garten` | Newsletter zu Kochen und Garten |
| **bleibt im Posteingang** | Sicherheit · Verkäufe und Kundinnen · doTERRA-Bestellungen · Technik-Fehler · Privat/Familie · alles von echten Menschen |

**Zugangsdaten** stehen in `.env` neben dem Skript (gitignored). GMX braucht
„POP3 und IMAP Zugriff erlauben“ in den Einstellungen; bei Zwei-Faktor-Anmeldung
ein anwendungsspezifisches Passwort. info@ läuft über `mail.mumlifebalance.ch`
(MX-Eintrag der Domain); abweichender Server über `INFO_HOST=` in der `.env`.

**Sicherungen:** Kopfzeilen werden mit `BODY.PEEK` gelesen, ungelesen bleibt
ungelesen. Gelöscht wird nichts. Kann der Server kein `MOVE`, wird kopiert und
nur mit `UID EXPUNGE` aufgeräumt — ein normales `EXPUNGE` würde auch fremde, als
gelöscht markierte Mails endgültig entfernen.

**Bericht** nach `outputs/mail-sortieren/<datum>.md` (gitignored, enthält
Absender und Betreffzeilen fremder Leute): alles, was im Posteingang bleibt,
plus die verschobenen Absender zum Gegenprüfen.

Regeln anpassen: die Wortlisten oben in `sortieren.py` (`SICHERHEIT`,
`FINANZEN`, `TECHNIK` …). Wer falsch landet, gehört dort ergänzt.
