---
tags: [plan, privat, familie]
---

# Familien-App statt FamilyWall — Plan (16.10.2026)

**Anlass:** Patricia: *„wir sind bei familywall und mit allem sind wir nicht so zufrieden“* ·
*„die kosten stören mich“*. Gebraucht wird, was FamilyWall heute kann, aber ohne Abo:
Termine mit Personen-Zuordnung, Wiederholung, Adresse und Anhängen · Push-Erinnerungen ·
Nachrichten (die Kleinen schreiben ihr darüber) · Gäste einladen. Dazu kommen Ämtli und
Stundenplan, die schon als Artifacts existieren.

**Geräte:** alles Android. Patricia und Chläus mit Handy, die Grossen mit Handy, die Kleinen
mit Tablet. Damit funktioniert Web-Push ohne iPhone-Umweg.

**Kosten-Ziel:** 0 Franken. Alles muss in die Gratis-Stufen von Vercel und Supabase passen.

---

## 1 · Bauweise

Wie das Repertoire (`C:\Users\pnulm\repertoire`) — bewährt, läuft schon bei Chläus.

| Teil | Womit | Gratis-Grenze |
|---|---|---|
| App | Web-App (PWA), wird auf jedem Gerät „zum Startbildschirm hinzugefügt“ | — |
| Hosting + Schnittstelle | Vercel (Projekt `familie`) | reicht weit |
| Daten + Chat live | Supabase Datenbank + Realtime | 500 MB DB |
| Anhänge | Supabase Storage, privater Bucket | **1 GB** — Fotos werden beim Hochladen auf ~1600 px verkleinert |
| Erinnerungen | Web-Push (VAPID), ausgelöst jede Minute über `pg_cron` in Supabase | — |

🚨 **Vercel Hobby erlaubt Cron nur einmal am Tag** — darum läuft der Minutentakt in Supabase
(`pg_cron` + `pg_net` ruft `/api/erinnern`), nicht bei Vercel.

🚨 **Eigener Ordner ausserhalb dieses Repos** (`C:\Users\pnulm\familie`), wie beim Repertoire.
Dieses Repo ist öffentlich; Namen, Termine, Arzt-Dokumente der Kinder gehören nicht hinein.
Im Code stehen keine Namen — die Personen liegen nur in der Datenbank.

**Zugang:** Ein Familienlink mit Code (`#k=…`), beim ersten Öffnen wählt das Gerät „Wer bist
du?“ und merkt es sich. Kein Passwort, kein Konto — die Kleinen sollen einfach tippen können.
Eltern-Geräte dürfen alles, Kinder-Geräte können Termine sehen, Ämtli abhaken und schreiben.

⚠️ **Offen:** eigenes Supabase-Projekt oder das bestehende (PIA/Repertoire)? Eigenes ist sauberer
(Kinderdaten getrennt von Mentees), die Gratis-Stufe erlaubt aber nur **zwei aktive Projekte**.
Vor dem Bau im Supabase-Konto nachsehen, wie viele es schon gibt.

---

## 2 · Etappen

FamilyWall läuft weiter, bis Etappe 4 steht und sich zwei Wochen bewährt hat.

### Etappe 1 · Kalender — ✅ live seit 16.10.2026

https://unsere-familie.vercel.app · Code in `C:\Users\pnulm\familie` (README dort). Speicher im
bestehenden Supabase-Projekt (PIA), eigene private Buckets `familie` + `familie-dateien`.
Kinder dürfen Termine eintragen und ändern, löschen auch; nur Personen und Ämtli-Zuordnung sind
den Eltern vorbehalten. Kinder-Namen stehen erst als Initialen da — umbenennen unter „Mehr“.
Offen: wer „Instrument üben“ und „Spange“ hat (unter „Mehr“ zuordnen).
- Monats-, Wochen- und Tagesansicht, Start auf „Heute & Morgen“
- Termin: Titel · Datum/Zeit oder ganztägig · **Personen** (eine oder mehrere, Farbe je Person) ·
  **Adresse** (antippen → Google Maps) · Notiz · **Anhänge** (Foto, PDF)
- **Wiederholen:** täglich · wöchentlich (mit Wochentagen) · alle 2 Wochen · monatlich ·
  jährlich, mit Enddatum und einzelnen Ausnahmen („diesen Termin verschieben/absagen“)
- Filter „nur meine“ / pro Person
- **Stundenplan** aus `context/persoenlich/schulzeiten/schulzeiten.html` übernehmen
  (inkl. gerade/ungerade KW, Ferien bis 2028) — als eigene Ebene, ein- und ausblendbar
- **Ämtli** aus `context/persoenlich/haushalt/seed` übernehmen, mit der Monats-Rotation
  L→N→B→C, abhakbar vom Kind selbst

**Fertig, wenn:** auf Patricias Handy und einem Kinder-Tablet installiert, ein wiederkehrender
Termin mit PDF angelegt und auf dem anderen Gerät sichtbar ist.

### Etappe 2 · Erinnerungen
- Pro Termin: keine · zur Zeit · 15 Min · 1 Std · 1 Tag vorher (mehrere möglich)
- Push geht an die zugeordneten Personen, nicht an alle
- Ämtli: Abend-Push „Morgen dran: …“ an das Kind
- Pro Gerät ein-/ausschaltbar

**Fertig, wenn:** ein Test-Termin in 5 Minuten auf dem gesperrten Handy und Tablet ankommt.

### Etappe 3 · Nachrichten
- Ein Familien-Chat plus Einzelchat Kind ↔ Mama/Papa
- Text, Foto, Sprachnachricht (Tablet-tauglich für die Kleinen)
- Push bei neuer Nachricht, gelesen-Haken
- Auf einen Termin antworten („Wann muss ich los?“) verknüpft Nachricht und Termin

**Fertig, wenn:** ein Kind vom Tablet schreibt und es auf Patricias gesperrtem Handy aufpoppt.

### Etappe 4 · Gäste + Umzug
- **Gäste-Link pro Termin:** z. B. Grosi sieht nur diesen Termin (Zeit, Ort, Anhang falls
  freigegeben), ohne Konto, mit „In meinen Kalender“ (.ics)
- Familienkalender als **Kalender-Abo** (.ics-Link) für alle, die zusätzlich den Handykalender
  nutzen wollen
- Termine aus FamilyWall übernehmen — ⚠️ prüfen, ob FamilyWall einen Export (.ics) anbietet;
  sonst wiederkehrende Termine von Hand neu anlegen, einmalige nur die kommenden
- Danach FamilyWall-Abo kündigen (macht Patricia)

---

## 3 · Was ersetzt wird

| Bisher | Danach |
|---|---|
| FamilyWall (Abo) | Familien-App |
| Artifact Schulzeiten | Ebene „Stundenplan“ in der App — Artifact bleibt, bis alles drüben ist |
| Artifact Haushaltsplan (Ämtli-Teil) | Ämtli in der App. ⚠️ Offen: ob die übrigen Haushaltsaufgaben (Putzen, Garten-Routine) mit umziehen oder im Artifact bleiben |
| Wunschzettel | bleibt, wie er ist (nur für Patricia) |

Grundsatz aus dem Workspace: **jede Sache hat genau einen Ort.** Was umgezogen ist, wird im
alten Artifact nicht weiter gepflegt.

## 4 · Risiken

- **Zustellung:** ein Chat, der einmal nicht zustellt, ist schlimmer als ein falscher Termin.
  Deshalb Etappe 3 erst nach zwei Wochen stabiler Erinnerungen.
- **Supabase pausiert Gratis-Projekte nach einer Woche ohne Zugriff** — bei täglicher
  Nutzung kein Thema, in den Ferien aber möglich. Der Minuten-Cron hält das Projekt wach.
- **Speicher:** 1 GB Anhänge. Bei 80 % meldet die App es; dann Ablage auf Google Drive umstellen,
  nicht auf ein Abo.
- **Sicherung:** wie beim Repertoire täglich eine Sicherung der Termine als JSON in den Storage.
