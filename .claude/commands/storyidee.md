# /storyidee — Täglicher Story-Ideen-Vorschlag (doTERRA + Mumlifebalance)

**Zweck:** Liefert pro Tag **2 Story-Ideen — eine je Profil (doTERRA + Mumlifebalance)**. Jede Idee (a) baut auf dem **letzten veröffentlichten Beitrag** auf, (b) nimmt eine Idee aus dem **90-Storyideen-Workbook**, (c) schlägt die **Brücke zum aktuellen Fokus-Angebot** (aus der Notion Wochen-/Monatsplanung).

Das ist ein schlanker **Ideen-Vorschlag**, KEINE fertige Slide-Produktion. Wenn Patricia daraus Slides will → `/story`.

Läuft auch mobil (claude.ai/code): einfach `/storyidee` tippen.

---

## Ablauf bei jedem Aufruf

1. **Wochentag → Säule.** Lies `context/julia-story-vorlagen.json` → `wochen_rotation` (Mo=Mini-Training, Di=persönliche Story, Mi=eigene Meinung, Do=Quick-Win, Fr=Inspiration/Vision, Sa=Social-Proof, So=Lifestyle-Reflexion). Das sorgt für Säulen-Abwechslung.

2. **Aktuelles Fokus-Angebot je Profil holen** (das ist der Verkaufs-Anker der Brücke):
   - Primär: Notion **Wochenplanung-DB** `collection://2ae7078e-8b7e-81e7-9083-000b01908eb5` → Property „Fokus der Woche" + Body-Tabelle „Was planst du je Business-Säule?". Falls Monatsfokus relevant: jüngster `outputs/monatsplaene/YYYY-MM*.md`.
   - Fallback (wenn Notion nicht erreichbar): `context/active-funnels.json` → live-Funnel + `manychat_keyword` je Profil.

3. **Letzten veröffentlichten Beitrag je Profil holen** (der Anker der Story):
   - Notion **Content-Management-DB** `2ae7078e-8b7e-811a-ad14-000ba5820c09` → jüngster Eintrag mit Status „veröffentlicht/gepostet" je Plattform (Instagram Mentoring / Instagram doTERRA).
   - Falls kein Eintrag / keine Caption abrufbar: **Patricia kurz fragen** — „Was war dein letzter Post pro Profil? 1 Satz reicht." NICHT erfinden.

4. **Passende Workbook-Idee wählen** aus `outputs/produkte/storyideen-networkerinnen/workbook.md` (8 Kapitel, 90 Ideen, je mit Impuls + Beispiel). Kriterien: passt zur **Tages-Säule** UND lässt sich sinnvoll an das **Thema des letzten Beitrags** anknüpfen. Nicht dieselbe Idee/dasselbe Kapitel wie an den Vortagen (Abwechslung).

5. **Ausgeben — je Profil:**
   - **Bezug zum Beitrag:** 1 Anschluss-Satz („Falls du meinen Post … gesehen hast …").
   - **Worüber du reden könntest:** konkreter Vorschlag, auf Patricias echtes Leben / den Zielgruppen-Schmerz gemünzt (nicht generisch).
   - **Brücke zum Angebot:** ein Brückensatz + Keyword, nach dem Brücken-Baukasten im Workbook (Abschnitt „Die Story-Brücke"). Bevorzugt zum **Freebie** (kleinste Hürde); nur wenn die Story warm genug ist, zum bezahlten Angebot.

---

## Regeln (Pflicht)

- **Voice:** `context/patricia-vollprofil.md` + `context/ki-phrasen-blackliste.md` (kein Nicht/Sondern-Konstrukt, keine Dreier-Stakkato, keine Worthülsen). Schweizer „ss", echte Umlaute, Du-Anrede.
- **doTERRA:** kein Heilversprechen, Lifestyle-Bubble, „bei mir war"-Frame — `context/doterra/patricia-wendepunkt-story.md` beachten. „Sich besser fühlen braucht Zeit", nie „heilt/hilft gegen".
- **Nicht jede Story braucht harten Verkauf:** bei reinen Nähe-/Reichweiten-Ideen weiche oder keine Brücke (Workbook-Regel: nicht bei jeder Story die Brücke).
- **Keine erfundenen Zahlen**, keine erfundenen Post-Inhalte.
- **Kurz halten:** 2 knappe Vorschläge, kein Roman. Patricia pickt und spricht/tippt selbst.

---

## Output-Format

```
🟦 Mumlifebalance  ·  [Wochentag] · Säule: [Säule]
- Anker (letzter Beitrag): […]
- Workbook-Idee: [Kapitel X, #N — Name]
- Worüber du reden könntest: […]
- Brücke: „[Brückensatz]" → Kommentier [KEYWORD]

🟧 doTERRA  ·  Säule: [Säule]
- Anker (letzter Beitrag): […]
- Workbook-Idee: [Kapitel X, #N — Name]
- Worüber du reden könntest: […]  (Lifestyle-Frame)
- Brücke: „[Brückensatz]" → Kommentier [KEYWORD]
```

---

## Wissensquellen (Pfade)
- Ideen-Pool: `outputs/produkte/storyideen-networkerinnen/workbook.md` (90 Ideen) + Brücken-Baukasten darin
- Wochentag-Rhythmus: `context/julia-story-vorlagen.json`
- Fokus/Angebot: Notion Wochenplanung `collection://2ae7078e-8b7e-81e7-9083-000b01908eb5` + `context/active-funnels.json` (Fallback + Keywords)
- Letzter Beitrag: Notion Content-DB `2ae7078e-8b7e-811a-ad14-000ba5820c09`
- Voice/Compliance: `context/patricia-vollprofil.md`, `context/ki-phrasen-blackliste.md`, `context/doterra/patricia-wendepunkt-story.md`
