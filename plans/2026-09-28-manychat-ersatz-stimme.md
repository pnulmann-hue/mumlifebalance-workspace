---
tags: [plan, funnel, instagram]
---

# ManyChat-Ersatz — zuerst nur für STIMME

**Auftrag (Patricia, 28.09.2026):** „ja bitte manychatersatz starten. und erstmal nur für
stimme.“ ManyChat (Pro-Abo) läuft parallel weiter, bis der Ersatz sich bewährt hat.

**Anlass:** ManyChat löst bei jedem Kommentar aus, in dem das Wort vorkommt. Bei STIMME
heisst das: „Ich stimme dir zu“ bekommt den Stimm-Check-Link.

## Was der Dienst tut

1. Instagram meldet einen neuen Kommentar (Webhook).
2. `lib/entscheiden.mjs` prüft: ist das eine Anfrage?
   - **ja:** Stichwort allein, mit Höflichkeit („Stimme, bitte“) oder in Grossbuchstaben
   - **nein:** Wort fehlt, oder „stimme“ als Verb / „meine innere Stimme“
   - **frag:** kurz und unklar → Claude (Haiku) entscheidet mit dem Beitrag als Kontext
3. Bei ja: öffentliche Antwort unter dem Kommentar („Schau in deine Nachrichten 💌“) und
   eine private Nachricht mit dem Link zu `https://mumlifebalance.ch/stimm-check/`.
4. Jede Entscheidung wird protokolliert (auch die Neins), damit Fehlgriffe sichtbar werden.

**Stand 28.09.:** Entscheider gebaut, 27 Gegenproben grün
(`node scripts/kommentar-antwort/test/entscheiden-test.mjs`).

## Schritte

| # | Was | Wer | Stand |
|---|---|---|---|
| 1 | Entscheider + Gegenproben | Claude | ✅ |
| 2 | Meta-App: Instagram-Produkt, Webhook „comments“, Berechtigungen für Kommentare verwalten und Nachrichten senden | Patricia klickt, Claude schreibt die Anleitung | offen |
| 3 | In der Instagram-App: Einstellungen → Nachrichten → „Zugriff auf Nachrichten erlauben“ für verbundene Tools | Patricia | offen |
| 4 | Dienst auf Vercel (`scripts/kommentar-antwort/`): Webhook prüfen, entscheiden, antworten, protokollieren | Claude | offen |
| 5 | Test nur mit Patricias eigenem Zweitkonto (App im Entwicklungsmodus — antwortet nur Konten mit einer Rolle in der App) | beide | offen |
| 6 | App-Prüfung bei Meta für den Zugriff auf alle Kommentare (Tage bis Wochen) | Patricia reicht ein, Claude bereitet Texte + Screencast-Ablauf vor | offen |
| 7 | Scharf schalten für STIMME, eine Woche beobachten | beide | offen |
| 8 | Weitere Stichwörter einzeln herüberholen, dann entscheiden, ob ManyChat gekündigt wird | Patricia | später |

## 🚨 Was man wissen muss

- **Ohne App-Prüfung antwortet der Dienst nur Konten, die in der Meta-App eine Rolle
  haben.** Für echte Kommentare braucht es die Prüfung. Bis dahin ist STIMME in keinem
  System eingerichtet — ein STIMME-Aufruf im Feed läuft solange ins Leere.
- **Private Antwort auf einen Kommentar geht einmal je Kommentar und nur innert 7 Tagen.**
- **Nie zwei Systeme auf dasselbe Stichwort.** STIMME bleibt in ManyChat ausgeschaltet.
- Zugang aus `.env`, nie im Code. Das Protokoll speichert keine Namen, nur Kommentar-ID,
  Text, Urteil und Stufe — das Repo ist öffentlich.
- Kostenvergleich ManyChat Pro gegen Vercel (gratis) + Claude (Bruchteile eines Rappens
  je unklarem Fall) rechnen, sobald der ManyChat-Betrag feststeht.
