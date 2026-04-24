# Montag-Workflow V2 — Content-Session in 60 Min

**Ziel:** Von 0 auf 3-4 fertig-geschedulte Posts pro Woche in einer einzigen Session.
**Startet mit:** `/montag` (siehe Command-Datei)
**Dauert:** ~60 Minuten
**Liefert:** Di/Mi/Fr Posts für beide Profile, Captions + Canva-Designs + Blotato-Configs

---

## Die 5 Phasen

### Phase 1 · Patricia spricht · 10 Min

**Du lieferst (Voice-Memo, Bullets oder einfach Chat):**

1. **Woche-Kontext:** Was ist diese Woche passiert? Was hast du beobachtet? Was beschäftigt dich?
2. **Echte Geschichte pro Profil:**
   - Mentoring: Bei welchem Mentoring-Moment warst du emotional drin?
   - doTERRA: Bei welchem Körper/Hormon/Energie-Moment war was los?
3. **Echte Zahlen/Fakten:** Was darf ich zitieren? (Jahre Business, Anzahl Kundinnen, konkrete Produkt-Erfahrungen, Körper-Reaktionen etc.)

**Claude tut:** NICHTS fragen. Nur zuhören und mitschreiben. Maximal eine einzige Klarstellungsfrage am Ende, wenn etwas fundamental unklar ist.

**Formal-Check:** Claude schreibt deine Inputs in `outputs/montag/YYYY-MM-DD-briefing.md` damit nichts verloren geht.

---

### Phase 2a · Pre-Research · 10 Min (Claude arbeitet still)

**Bevor Claude Konzepte schreibt, ERST dieser Dreier-Check — nicht verhandelbar:**

**1. Marktforschung (WebSearch)**
- Instagram + TikTok: was ist in Patricia's 2 Nischen die letzten 7 Tage viral gegangen?
  - Mentoring: „Network Marketing Mama", „Instagram Sichtbarkeit Solopreneurin", „Mama Business starten"
  - doTERRA: „Perimenopause Ü35", „Hormone Mama", „Erschöpfte Mama", „3 Uhr nachts wach"
- Notiere 3-5 **aktuelle Hook-Patterns** die gerade funktionieren (Zahlen, Provokationen, POV-Formate)
- NICHT copy-paste — als Inspiration verstehen

**2. Hook-Fundus**
- Lies `context/hook-framework.md` — die 5 Kategorien durchgehen (Zahlen/Anleitung/Provokant/Neugier/Identifikation)
- Check `outputs/karussells/` + `outputs/reels/` der letzten 4 Wochen: welche Hooks HABEN funktioniert (Saves/Kommentare)? Welche Patterns nicht? Muster abstrahieren.
- Memory-Regel `feedback_hooks-inspiration-nicht-copypaste.md` ernstnehmen — Muster variieren, nicht wiederholen.

**3. Notion-Verkaufsfokus**
- Öffne Notion Content-Management-DB (`2ae7078e-8b7e-811a-ad14-000ba5820c09`) UND Produkte-DB (`2ae7078e-8b7e-81ef-aafa-f03993ef344f`)
- Filter: **„Wochen-Fokus" oder „Aktiv im Verkauf" für KW = aktuelle Woche**
- Dokumentiere: Welches Produkt läuft diese Woche? Welcher Funnel? Welches Freebie ist gerade Lead-Magnet?
- Wenn Notion-MCP nicht verbunden: Patricia fragen „Was steht diese Woche im Verkaufsfokus?" (einzige erlaubte Rückfrage an diesem Punkt)

**Output dieser Phase:** Kurz-Liste in deinem Arbeitskontext (nicht an Patricia liefern):
- 3-5 Markt-Trend-Patterns
- 10 Hook-Kategorien mit diese-Woche-tauglichen Varianten
- 1-2 aktive Produkte/Funnels/Freebies im Verkaufsfokus

---

### Phase 2b · Konzepte schreiben · 10 Min (Claude arbeitet still)

Claude schreibt **6 Post-Konzepte** (Di/Mi/Fr × 2 Profile), je maximal 2 Sätze:
- Hook (max. 80 Zeichen, identifizierend) — **informiert durch Phase-2a-Research**
- Kern-Message (max. 140 Zeichen) — aus Patricia's Story
- Welches Keyword → welche DM-Automation (passend zum **Wochen-Verkaufsfokus**)
- Welche Canva-Template-ID aus Patricia's Library

**Grundregeln:**
- Strikt basiert auf Phase-1-Input + Phase-2a-Research
- **Mindestens 1 von 6 Konzepten muss direkt auf den Notion-Verkaufsfokus einzahlen** (Freebie-Lead-Magnet, Produkt-Teaser, Funnel-Einstieg)
- Nur Patricia-Zahlen aus dem Briefing oder aus `context/patricia-expertise.md`
- Nur Canva-Designs aus Patricia's bestehenden Template-IDs (keine AI-Generation)
- Nur validierte Hooks aus `context/hook-framework.md` + Markt-Patterns (als Inspiration variieren, nicht copy-paste)

**Output:** Tabelle mit 6 Konzepten, klar lesbar, kein Fluff. Markiere mit 🎯 welches Konzept auf den Wochen-Verkaufsfokus einzahlt.

---

### Phase 3 · Patricia pickt · 15 Min

Du kreuzt 3-4 Konzepte an die du willst. Kurze Änderungen (einzelne Worte, Framing) schreibst du direkt als Kommentar dazu.

**Claude tut:** NICHTS schreiben. Nur warten.

**Erwartung:** Du kreuzt MAX 4 an. Lieber 3 gute Posts als 6 mittelmässige.

---

### Phase 4 · Claude liefert Block · 15 Min

Für jeden ausgewählten Post:
- Volle Caption (Preflight-geprüft: kein Nicht/Sondern, kein Dreier-Stakkato, kein „Stell dir vor" ausser explizit gewünscht)
- Canva-Design ID referenziert (bestehende Vorlage geklont via merge-designs)
- Blotato-Config vorbereitet (mit Post-Zeit + accountId)
- Alles als einzelne `.md`-Dateien in `outputs/karussells/` oder `outputs/reels/`

**Reel-Handling (FESTGELEGT seit 2026-04-22):**
- Claude liefert NUR Briefing (Shotlist + VO-Skript + Cover-Hinweis + Caption + Hashtags)
- Video + Cover + Posting machst DU manuell (Canva bauen → Instagram App direkt posten)
- **KEIN Blotato-Scheduling für Reels** (Blotato kann keine Cover-Images setzen — Limitation)
- Reel-Format-Standard: Stock-Video + deine Voiceover, Cover als erste 1-2 Sek im Video integriert

**Karussell-Handling:**
- Claude baut Design via `merge-designs` + Caption + Blotato-Config
- Patricia: Canva-Export → URLs in Config → Claude schedulet via Blotato
- Vollautomatisch, keine manuelle Post-Arbeit

---

### Phase 5 · Patricia gated · 5 Min

Du liest die 3-4 Captions. Drei mögliche Reaktionen:

- **✅ Freigabe** → Claude schedulet via Blotato (sobald Canva-Exports da sind)
- **✏️ Ein Edit-Round** → Du schreibst die Änderungen als Liste (nicht einzeln), Claude macht alle auf einmal
- **❌ Stopp** → Du sagst was stört, wir reden, neuer Block

---

## Commitments die Claude einhält

1. **Zero invented numbers** — jede Zahl muss aus deinem Input oder `patricia-expertise.md` kommen. Im Zweifel: abstrahieren oder weglassen.
2. **Zero AI-generated Visuals** — Canva-Designs werden aus deinen bestehenden Templates geklont via `merge-designs` tool. Keine `generate-design`-Aufrufe mehr.
3. **Ein Reel-Format** — Stock-Video + Voiceover. Festgelegt. Keine Tool-Experimente ohne dein explizites Go.
4. **Batch-Edits** — Änderungen kommen als Liste in einer Nachricht. Claude macht alle auf einmal, nicht sequenziell.
5. **Patricia-Voice-Check** — vor jedem Liefern fragt Claude sich: „Würde Patricia das WIRKLICH so sagen?" Wenn nicht → umschreiben.
6. **Schweizer ss, echte Umlaute** — immer.
7. **Blackliste respektieren** — Nicht/Sondern, Dreier-Stakkato, Marketing-Buzzwords. Ausnahmen nur auf deine explizite Ansage.

---

## Anti-Pattern (was Claude ab jetzt NICHT mehr macht)

- ❌ Zahlen zum „abrunden" erfinden („412 Follower", „38 Jahre")
- ❌ AI-Stock-Video-Assembly-Experimente ohne Abstimmung
- ❌ 5-Szenen-Storyboards bauen ohne Check
- ❌ Chrome-MCP-Klonen wenn `merge-designs` funktioniert
- ❌ Einzeln iterierte Fragen statt Batch
- ❌ Captions schreiben bevor deine echte Story steht

---

## Wenn die Session entgleist

**Claude sagt selbst „Stopp"** wenn:
- Mehr als 3 Korrektur-Runden auf einer Caption stattfinden (dann ist das Konzept falsch, nicht die Caption)
- Zahlen gefordert werden die Claude nicht hat (dann: abstrahieren oder dich fragen)
- Design-Arbeit länger als 10 Min ohne sichtbares Ergebnis läuft

---

## Wöchentliche Rotation

Welche Themen-Pillars laufen wann:

**Mentoring:**
- Di: Authentizität / NM 2.0
- Mi: Business/Sichtbarkeit
- Fr: Mythen/Provokant

**doTERRA:**
- Di: Wake-Up / Hormone
- Mi: Energie/Ernährung
- Fr: Mitte-30-Phase / Perimenopause

(Kann Claude in Phase 2 automatisch einhalten, oder du brichst die Rotation bewusst.)
