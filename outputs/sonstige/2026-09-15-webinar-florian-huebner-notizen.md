---
tags: [misc, research, ki, externe-wissen]
---

# Webinar Florian Hübner (Mr. Tech) — 15.09.2026

**Live-Notizen von Patricia** (wird während des Webinars gefüllt)

---

## Rohnotizen

<!-- hier kommt rein, was Patricia im Chat schickt — unverändert -->

**Block 1 (Videogenerierung + Arbeitsweise):**
- Empfiehlt zur Video-Generierung: **Higgsfield**, **Nano Banana Pro**, **Kling Motion Control**
- Überarbeitet **alle seine Präsentationen mit Claude** — Ansage an Claude: *"maximaler Business-Impact"*
  → Patricias Randnotiz: das ist für meine Präsentationen sicher auch eine gute Empfehlung
- Sein Webinar läuft über **WebinarJam**
- Nennt **Claude als besten KI-Agenten**
- Zeigt live, wie er mit Claude baut:
  1. Präsentationen
  2. Webseiten für sein Angebot
  3. ein **Business-Dashboard** mit Infos zu den grossen Unternehmen, die für ihn relevant sind
  4. daraus automatisch **personalisierte Mail-Entwürfe pro Unternehmen**

---

## Verdichtet

### Kernthesen

### Tools

### Workflows / Automatisierungen

### Prompts

#### 🔹 Prompt 1 — Instagram-Analyse über Claude in Chrome

**So wie er es im Webinar gezeigt hat** (Claude in Chrome, eingeloggtes Instagram
offen, Profil-Ansicht):

> analysiere meine letzten 50 posts und gib mir handlungsempfehlungen.
> ich brauch 5 mega virale skripte.

Sein Mechanismus dahinter: Claude sieht den Browser mit, liest die sichtbaren
Beiträge samt Zahlen aus und leitet daraus Muster ab. Kein Export, kein Tool
dazwischen.

---

**Patricias Fassung** — dasselbe, aber mit ihren Regeln und ihrem Markenwissen.
Zu benutzen mit *Claude in Chrome*, wenn Instagram eingeloggt und das Profil
offen ist:

```text
Du siehst mein Instagram-Profil im Browser.

SCHRITT 1 — Daten holen
Geh meine letzten 50 Beiträge durch. Scroll so weit, bis du wirklich 50 hast,
und öffne die Insights, wo sie erreichbar sind. Trag pro Beitrag zusammen:
Datum · Format (Reel/Karussell/Bild) · die erste Zeile des Hooks · Thema ·
CTA-Art (Share / Keyword / Speichern / kein CTA) · Aufrufe · Likes ·
Kommentare · Speicherungen · geteilt.
Sag mir ehrlich, welche Zahlen du NICHT sehen konntest — rate nichts dazu.

SCHRITT 2 — Muster erkennen
Vergleiche Top-10 gegen Flop-10. Ich will keine Wetterbericht-Zusammenfassung,
sondern was die Gewinner GEMEINSAM haben und den Verlierern fehlt. Schau auf:
- Format (Reel vs. Karussell vs. Bild)
- Hook-Art (Bekenntnis · Zeitanker · Hot Take · Frage · Zahl)
- Bewusstseinsstufe: stellt der Hook IHRE Frage oder gibt er schon MEINE Antwort?
- Post-Job: Reichweite · Autorität · Story · Sales
- CTA-Art und ob der CTA überhaupt zum Job passte
- Thema: Mama-Alltag vs. Business-intern vs. Öle
- Cover: Foto mit mir · Lifestyle-Foto · Typo-Template, und welche Farbe
Nenne mir 3 Muster, die ich vorher nicht gesehen habe. Keine Binsen.

SCHRITT 3 — Handlungsempfehlungen
Maximal 5. Jede in dieser Form:
„Hör auf mit X → mach stattdessen Y → weil in meinen eigenen Zahlen [konkreter
Beleg aus Schritt 1]."
Was du nicht belegen kannst, lässt du weg.

SCHRITT 4 — 5 Skripte
Schreib mir 5 Reel-Skripte, die auf genau diesen Mustern aufbauen.
Pro Skript: Hook (die gesprochene erste Zeile, wortwörtlich) · 20-40 Sek
Sprechtext · Titelbild-Text · Caption · CTA.

REGELN, die über allem stehen:
- Meine Stimme: wie ein Anruf bei einer Mama-Freundin. Ganze Sätze mit
  Konjunktionen, kein Stakkato, Schweizer ss statt ß, echte Umlaute.
- Nur MEINE Zahlen und MEINE Szenen. Nichts erfinden — keine Einnahmen,
  keine Teamgrössen, keine Ergebnisse, die ich nicht genannt habe.
- Die Gegenspielerin ist der Job, nicht das Network.
- Keine Netzwerkaufbau-Tipps („besser recruiten") — mein Thema ist das eigene.
- Bei doTERRA keine Heilversprechen, immer „bei mir war es so".
- Der Hook nennt nie die Lösung.
- Mindestens 3 verschiedene Angles über die 5 Skripte, nicht fünfmal derselbe.
- Mindestens 3 der 5 sind reine Reichweiten-Posts mit Share-CTA,
  höchstens 1 ist ein Lead-Post mit Keyword-CTA.

Am Schluss: sag mir in einem Satz, was dir an meinem Profil am meisten im Weg
steht.
```

**🚨 Wichtig — der bessere Weg für die Zahlen:**
Was Claude im Browser sieht, ist nur, was Instagram gerade anzeigt. Reichweite,
Speicherungen und Geteilt-Zahlen holt `scripts/instagram-insights/holen.py`
direkt über die Meta-API — **exakt statt abgelesen**. Ideal ist die Kombination:
Zahlen aus dem Skript, Hooks/Cover/Kommentar-Stimmung über den Browser.

### Zahlen & Beispiele

### Sein Funnel / Verkaufsmechanik

---

## Für Patricia relevant

| Erkenntnis | Wo einsetzbar | Nächster Schritt |
|---|---|---|

---

## 🔗 Verwandte Notizen

- [[2026-09-15-florian-huebner-mr-tech-recherche]]
