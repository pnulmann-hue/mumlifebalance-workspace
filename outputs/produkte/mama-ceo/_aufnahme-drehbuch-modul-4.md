---
tags: [produkt, mama-ceo, saeule-4, intern, aufnahme]
---

# 🎬 Aufnahme-Drehbuch Modul 4 — Bots in Claude Cowork

> Dein Schritt-für-Schritt fürs Filmen der Live-Demos (L4.4 Cockpit-Bot + L4.5 Haushalts-Bot).
> Vor jedem ▸ kurz innehalten, machen, dann weiterreden (deine Sprechnotizen stehen in den PPTX).
> Vorbereitung: Claude Desktop offen · Notion offen · dieses Dokument zum Reinkopieren der Prompts.

---

## TEIL 0 — Was VORHER bereit sein muss (vor der Aufnahme)

☐ **0.1 Claude Desktop + Pro-Abo** aktiv, Notion-Connector schon getestet.
☐ **0.2 Deine Haushalts-Liste in Notion** gefüllt ✅ (ist erledigt — 4 Kinder komplett).
☐ **0.3 ⚠️ Dein Business-Brief** — den brauchst du für den Cockpit-Demo (4.4)! Hast du noch NICHT geschrieben.
   → Vorher mit dem Bonus-5-Prompt erarbeiten (10 Min) ODER im Video 4.3 live erarbeiten und gleich für 4.4 nutzen.
☐ **0.4 ⚠️ Notion-Master-Template „Duplizieren erlauben"** einschalten — DAMIT die Mentees die Vorlage (inkl. der neuen Haushalts-Liste) kriegen.
   → Template öffnen → Teilen → „Im Web veröffentlichen" → „Duplizieren als Vorlage erlauben" EIN → Link kopieren.
   → Kurz prüfen: ist die **🏠 Haushalts-Liste** im Template sichtbar (sie ist dort angelegt)? Beim Duplizieren kommt sie mit.
☐ **0.5** Drehbuch + die 6 PPTX (Sprechnotizen) offen.

---

## TEIL A — Cowork einrichten (EINMAL, zeigst du in L4.4)

☐ **A1.** Claude **Desktop-App** öffnen (nicht Browser, nicht Claude Code).
☐ **A2.** Kurz zeigen: „Das ist Cowork — die Desktop-App, mit Knöpfen, kein Code." Pro-Abo erwähnen (~23 CHF/Mt).
☐ **A3.** **Einstellungen (Zahnrad) → Connectors / Verbindungen → Notion → „Verbinden".**
☐ **A4.** Bei Notion **einloggen** → **freigeben**, welche Seiten Claude sehen darf: **„🏡 Privat & Familie"** (Haushalts-Liste) + dein **Business-Brain** (für den Cockpit-Bot).
☐ **A5.** Sagen: „Das ist der Stecker. Einmal eingesteckt — ab jetzt liest Claude mein Notion. Das mache ich nur EINMAL, gilt für alle Bots."

---

## TEIL B — Cockpit-Bot bauen (L4.4)

☐ **B1.** In Cowork **neuen Bot / neues Projekt** anlegen, Name z.B. „Cockpit-Bot".
☐ **B2.** **System-Prompt einfügen** (Kasten unten) — bei `[…]` deinen **Business-Brief** eintragen.
☐ **B3.** Sagen: „Mein Notion ist schon verbunden — er liest meine Wochenplanung direkt."
☐ **B4.** **Testen:** tippe **„Was ist heute mein Fokus?"** → Bot zeigt Tagesfokus + 3 Aufgaben + Wochenblick.
☐ **B5.** Reagieren: „Wie geil ist das denn — genau das hast du gleich auch."

**Cockpit-Bot-Prompt (kopieren):**
```
ROLLE
Du bist mein persönlicher Cockpit-Bot — mein Morgenbriefing-Assistent.
Dein Job ist, mir jeden Morgen in 30 Sekunden Klarheit zu geben, was heute dran ist.

MEIN KONTEXT
[Hier meinen Business-Brief einfügen — wer ich bin, meine Kundin, mein Angebot, meine Stimme.]

WAS DU BEKOMMST
Du bist mit meinem Notion verbunden und liest meine aktuelle Woche
(Wochenfokus, Tagesplaner, Aufgaben, Ziele). Wenn etwas fehlt, frag kurz nach.

WAS DU TUST, wenn ich „Was ist heute dran?" frage:
1. Nenne meinen TAGESFOKUS in einem Satz.
2. Liste meine 3 WICHTIGSTEN AUFGABEN heute (Money-Making + Termine zuerst).
3. Gib einen kurzen WOCHENBLICK (1-2 Sätze).
4. Schliesse mit EINEM motivierenden, ehrlichen Satz — kein Kitsch.

REGELN
- Kurz und konkret. Sprich mich mit DU an, warm wie eine gute Freundin.
- Erfinde keine Termine/Zahlen — nur was in meinem Notion steht.
- Bei vollem Tag: hilf priorisieren statt alles gleich wichtig zu machen.
```

---

## TEIL C — Haushalts-Bot bauen (L4.5 MASTERY)

☐ **C1.** In Cowork **neuen Bot** anlegen, Name z.B. „Haushalts-Helfer".
☐ **C2.** **Haushalts-Prompt einfügen** (Kasten unten). Notion ist schon verbunden (aus Teil A).
☐ **C3.** Sagen: „Gleiche Mechanik wie der Cockpit-Bot — nur eine andere Liste, eine andere Vorlage."
☐ **C4.** **Testen:** tippe **„Was ist heute zu Hause dran?"** → Bot zeigt Haushalt + Familien-Termine + Schule (Vorabend).
☐ **C5.** Reagieren: „Das musste ich vorher alles im Kopf haben — jetzt sagt's mir mein Helfer."

**Haushalts-Bot-Prompt (kopieren) — deine persönliche Version:**
```
ROLLE
Du bist mein persönlicher Haushalts-Helfer — der Zwilling meines Cockpit-Bots,
nur für zu Hause. Dein Job ist, mir morgens zu sagen, was an Haushalt und
Familie heute dran ist, damit das nicht mehr alles in meinem Kopf liegt.

MEIN KONTEXT
Vierfache Mama. Besonderheit: ich begleite gerade jemanden familiär jeden
Nachmittag — meine Nachmittage sind aktuell geblockt, plane Haushalt auf
Vormittag/Abend/Wochenende.

WAS DU BEKOMMST
Du liest meine Notion-Liste „🏠 Haushalts-Liste". Darin stehen:
- WIEDERKEHREND (Rhythmus + Wochentag, z.B. Wäsche, Müll-Mittwoch)
- DATIERT (festes Datum, z.B. Frühlingskleider Ende März)
- FAMILIEN-TERMINE / GEBURTSTAGE (Geschenk ~10-14 Tage vorher)
- SCHULE (am VORABEND erinnern: Schwimmen/Turnen/Wald — mit Vorname des Kindes)

WAS DU TUST, wenn ich „Was ist heute zu Hause dran?" frage:
1. Wiederkehrendes heute (täglich + wöchentlich mit heutigem Wochentag).
2. Termine/Daten von heute + nächste Tage (Datumsregeln korrekt rechnen).
3. SCHULE am Vorabend ansagen („morgen Schwimmen für Lukas — Sachen packen").
4. „Wer = Kinder" → „erinnere die Kinder an …".
5. Format: kurze Tagesliste — 🏠 Haushalt · 👨‍👩‍👧 Familie/Termine · 🎒 Schule (morgen) · 🧒 Ämtli.

REGELN
- Kurz + konkret, DU-Anrede, warm. Erfinde nichts — nur was in der Liste steht.
- Me-Time-Slots erinnern als Schutz, nie mit Druck.
- Nachmittage sind aktuell geblockt — Haushalt auf Vormittag/Abend vorschlagen.
- Wenn heute wenig ansteht: ehrlich sagen + Pause gönnen.
```

---

## TEIL D — Für die, die KEIN Cowork haben (kurz im Video erwähnen)
☐ **D1.** „Kein Pro/Cowork? Geht auch:"
- **Browser-Projekt** (claude.ai / ChatGPT): Vorlage + Liste reinkopieren
- **Gratis-Chat-One-Shot** (Bonus 4): einmal Prompt + Liste reinwerfen
- **Nur Notion** (Stufe 0): die Ansichten „Kommende Termine" / „Nach Wochentag" öffnen
☐ **D2.** „Jede nimmt einen Win mit — niemand bleibt aussen vor."

---

## 📦 Was die Mentees bekommen (in ThriveCart hochladen / verlinken)

**Downloads (Bonus-Dateien, je bei der passenden Lektion):**
- L4.1: 📋 Arbeitsblatt Säule 4 (.docx)
- L4.2: 💬 Gratis-Chat-One-Shot (Bonus 4)
- L4.3: ✍️ Business-Brief-Erarbeiten-Prompt (Bonus 5)
- L4.4: 🖥 Cowork-einrichten-Anleitung (Bonus 6) · 🌅 Cockpit-Bot-Vorlage (Bonus 1) · ⚙️ Claude-Code-Anleitung (Bonus 7, Stufe 2)
- L4.5: 🏠 Haushalts-Helfer-Vorlage (Bonus 2) · 🍳 Kochassistent-Vorlage (Bonus 3)

**📂 Notion-Vorlage (WICHTIG — der Punkt, an den man leicht vergisst):**
- Die **🏠 Haushalts-Liste** ist Teil deines **Master-Templates** (das die Mentees in Säule 3 duplizieren).
- → Stell sicher: **„Duplizieren erlauben" ist EIN** (Teil 0.4) und der **Duplikat-Link** steht bei **L3.5 UND L4.5**.
- → Die Mentees: in Säule 2 Brain-Dump gemacht → in 4.5 in die duplizierte Haushalts-Liste eintragen → Bot drauf.

---

## ✅ Vor dem Aufnehmen — Quick-Check
☐ Claude Desktop offen + Pro aktiv
☐ Notion-Connector verbunden (Test: „Was steht in meiner Wochenplanung?")
☐ Haushalts-Liste in Notion gefüllt (ist sie ✓)
☐ Business-Brief griffbereit (für Cockpit-Bot)
☐ Dieses Drehbuch + die PPTX (Sprechnotizen) offen
