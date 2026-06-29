const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType
} = require("docx");

const PETROL = "1F6F6B";
const CREME = "F1ECDD";
const GREY = "CCCCCC";

// ---- helpers ----
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const sub = (t) => new Paragraph({ spacing: { before: 160, after: 60 }, children: [new TextRun({ text: t, bold: true, color: PETROL })] });
const p = (t) => new Paragraph({ spacing: { after: 60 }, children: [new TextRun(t)] });
const small = (t) => new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: t, italics: true, size: 20, color: "555555" })] });
const chk = (t) => new Paragraph({ spacing: { after: 40 }, children: [new TextRun("☐  " + t)] });
const line = (label) => new Paragraph({ spacing: { after: 80 }, children: [new TextRun(label ? label + "  " : ""), new TextRun({ text: "______________________________________________", color: "999999" })] });
const blank = () => new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "______________________________________________________________", color: "999999" })] });
const spacer = () => new Paragraph({ children: [new TextRun("")] });

function cell(text, { w, head = false, bold = false } = {}) {
  const border = { style: BorderStyle.SINGLE, size: 1, color: GREY };
  return new TableCell({
    width: { size: w, type: WidthType.DXA },
    borders: { top: border, bottom: border, left: border, right: border },
    shading: head ? { fill: PETROL, type: ShadingType.CLEAR } : { fill: "FFFFFF", type: ShadingType.CLEAR },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ children: [new TextRun({ text: text, bold: head || bold, color: head ? "FFFFFF" : "000000" })] })],
  });
}
function table(widths, rows) {
  const total = widths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map((r, i) =>
      new TableRow({ children: r.map((c) => cell(c, { w: widths[r.indexOf(c) === -1 ? 0 : widths[r.length] ? 0 : 0], head: i === 0 })) })
    ),
  });
}
// simpler table builder (explicit)
function tbl(widths, header, dataRows) {
  return new Table({
    width: { size: widths.reduce((a,b)=>a+b,0), type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ children: header.map((h, i) => cell(h, { w: widths[i], head: true })) }),
      ...dataRows.map((row) => new TableRow({ children: row.map((c, i) => cell(c, { w: widths[i] })) })),
    ],
  });
}
const emptyRows = (cols, n) => Array.from({ length: n }, () => Array.from({ length: cols.length }, () => " "));

const children = [];

// Title
children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "Mama-CEO · Säule 4", bold: true, color: PETROL, size: 24 })] }));
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Arbeitsblatt — Du delegierst den Adminkram")] }));
children.push(small("Wochen 5-6 · 6 Lektionen · Drucke es aus oder fülle es digital. Du musst nichts können — wir gehen in 3 Stufen, und auf jeder nimmst du einen Win mit."));
children.push(spacer());

// ---------------- 4.1 ----------------
children.push(H2("Lektion 4.1 · KI-Mythos vs. Realität — Input ist alles"));
children.push(sub("▸ Dein bisheriger KI-Frust (ehrlich)"));
children.push(p("Wo hat KI dir bisher „nichts gebracht\"? Was hast du gefragt?"));
children.push(blank()); children.push(blank());
children.push(small("→ Am Ende von Säule 4 schaust du nochmal drauf — du wirst sofort sehen, woran's lag."));
children.push(sub("▸ Die 3 Zutaten für einen guten KI-Auftrag (in eigenen Worten)"));
children.push(line("1. Kontext ="));
children.push(line("2. Klare Aufgabe ="));
children.push(line("3. Beispiel ="));
children.push(sub("▸ Was nervt dich am meisten?"));
children.push(chk("Eher Business (Briefing, Planung, Überblick) → freu dich auf den Cockpit-Bot"));
children.push(chk("Eher Zuhause (was steht an, Termine, Haushalt im Kopf) → freu dich auf den Haushalts-Helfer"));
children.push(chk("Beides gleich → perfekt, wir bauen beide"));
children.push(sub("✓ Was du nach 4.1 hast"));
children.push(p("KI verstanden als Praktikantin · Regel „Müll rein, Müll raus\" · die 3 Zutaten · den Fahrplan (2 Bots, Business + Zuhause)."));
children.push(new Paragraph({ pageBreakBefore: true, children: [new TextRun("")] }));

// ---------------- 4.2 ----------------
children.push(H2("Lektion 4.2 · Womit du arbeitest — die 3 Stufen"));
children.push(sub("▸ Auf welcher Stufe startest du? (du kannst später jederzeit höher)"));
children.push(chk("🟢 Stufe 0 — nur Notion (gratis, kein Bot, ich nutze die Ansichten)"));
children.push(chk("🟡 Stufe 1 — Claude Cowork (Bot ohne Code) ← Empfehlung für die meisten"));
children.push(chk("🔵 Stufe 2 — Claude Code/Telegram (automatisch, später)"));
children.push(sub("▸ Wenn Stufe 1 (Cowork): Zugang bereit?"));
children.push(chk("Claude-Pro-Abo aktiv (~20-23 CHF/Mt)"));
children.push(chk("Claude Desktop-App installiert (Mac/Windows)"));
children.push(chk("Notion-Connector eingesteckt (einmal: Notion-Login bestätigt + Seiten freigegeben)"));
children.push(sub("▸ Gut zu wissen (häkchen wenn verstanden)"));
children.push(chk("Der nackte Gratis-Chat reicht fürs Business nicht (zu statisch)"));
children.push(chk("„Connector\" = der Stecker, der Claude mit meinem Notion reden lässt"));
children.push(chk("Ich gebe selbst frei, welche Notion-Seiten der Bot sehen darf"));
children.push(chk("Ich muss NICHT Claude Code anfassen — Cowork reicht"));
children.push(sub("▸ Mein Vorsatz"));
children.push(p("„Ich bleib erstmal auf EINER Stufe und bau meine 2 Bots, bevor ich was Neues anschaue.\"  ☐"));
children.push(new Paragraph({ pageBreakBefore: true, children: [new TextRun("")] }));

// ---------------- 4.3 ----------------
children.push(H2("Lektion 4.3 · Dein Business-Brief schreiben"));
children.push(small("Schreib jeden Baustein in 2-4 Sätzen. Kein Roman — Stichworte reichen. Diesen Brief kopierst du später in jeden deiner Bots."));
children.push(small("💡 Lieber im Gespräch statt vor dem leeren Blatt? Nimm den Bonus-Prompt „Business-Brief erarbeiten\": sag der KI, sie soll ein Buch über dich schreiben und so lange fragen, bis sie alles hat — am Schluss spuckt sie dir den fertigen Brief aus. Diese Felder hier dienen dann als deine Checkliste, dass nichts fehlt."));
children.push(sub("▸ Baustein 1 — Wer bin ich (Name, Mama von …, im Network mit …, mein Thema)"));
children.push(blank()); children.push(blank());
children.push(sub("▸ Baustein 2 — Wer ist meine Kundin (so konkret wie möglich)"));
children.push(blank()); children.push(blank());
children.push(sub("▸ Baustein 3 — Was biete ich an (aus Säule 3)"));
children.push(line("🎁 Gratis:"));
children.push(line("💶 Mini:"));
children.push(line("💎 Gross:"));
children.push(sub("▸ Baustein 4 — Meine Themen (Überthemen aus der Jahres-Strategie)"));
children.push(line("1.")); children.push(line("2.")); children.push(line("3."));
children.push(sub("▸ Baustein 5 — Meine Stimme (locker/seriös, du/Sie, typische Wörter)"));
children.push(blank());
children.push(sub("▸ Baustein 6 — Was der Bot NIE tun soll (deine Tabus)"));
children.push(blank());
children.push(sub("▸ Stimm-Beispiele anhängen (2-3 eigene Texte, damit der Bot deinen Ton trifft)"));
children.push(line("1.")); children.push(line("2.")); children.push(line("3."));
children.push(sub("▸ Wo legst du den Business-Brief ab? (z.B. Notion-Seite „Business-Brief\")"));
children.push(blank());
children.push(new Paragraph({ pageBreakBefore: true, children: [new TextRun("")] }));

// ---------------- 4.4 ----------------
children.push(H2("Lektion 4.4 · Dein Cockpit-Bot bauen (in Claude Cowork)"));
children.push(sub("▸ Bau-Checkliste (mach das WÄHREND des Videos, pausier wo nötig)"));
children.push(chk("Schritt 1: Cowork geöffnet + Notion-Connector eingesteckt + Vorlage (Bonus) eingefügt"));
children.push(chk("Schritt 2: Business-Brief (aus 4.3) reingegeben"));
children.push(chk("Schritt 3: Notion verbunden (Bot liest die Wochenplanung direkt)"));
children.push(chk("Schritt 4: Getestet mit „Was ist heute mein Fokus?\""));
children.push(chk("Der Bot hat mir Tagesfokus + 3 Aufgaben ausgegeben ✓"));
children.push(small("Stufe 0 ohne Bot: einfach die Notion-Ansicht „🗓 Nach Wochentag\" öffnen — auch ein Win."));
children.push(line("▸ Mein Cockpit-Bot heisst:"));
children.push(sub("▸ 3-Tage-Test"));
children.push(tbl([1800, 2200, 2200, 3160],
  ["Tag", "gefragt?", "hilfreich?", "Datum"],
  [["Tag 1", "☐", "☐", " "], ["Tag 2", "☐", "☐", " "], ["Tag 3", "☐", "☐", " "]]));
children.push(line("Was würdest du am Bot noch verbessern?"));
children.push(sub("▸ Stufe 2 — nur falls dich der Ehrgeiz packt (KEIN Muss)"));
children.push(chk("Mir ist klar: automatischer Telegram-Bot = Hosting (~5 CHF/Mt) + etwas Code (Claude Code macht's)"));
children.push(chk("Interessiert mich später → in Live-Call 3 ansprechen"));
children.push(new Paragraph({ pageBreakBefore: true, children: [new TextRun("")] }));

// ---------------- 4.5 ----------------
children.push(H2("Lektion 4.5 · MASTERY · Dein Haushalts-Helfer-Bot"));
children.push(sub("▸ Schritt 1: Hol deinen Brain Dump aus Säule 2 raus"));
children.push(p("Nimm dein Hütchen-Inventar — alle „muss ich noch\"-Sachen rund um Haushalt + Familie."));
children.push(sub("▸ Schritt 2: Sortier sie in 3 Sorten"));
children.push(p("🔁 WIEDERKEHREND (immer am gleichen Tag/Rhythmus)"));
children.push(tbl([5680, 3480], ["Aufgabe", "Rhythmus (z.B. montags / monatlich)"], emptyRows([0,0], 4)));
children.push(p("📅 DATIERT (einmal an einem festen Datum, z.B. saisonal)"));
children.push(tbl([5680, 3480], ["Aufgabe", "Datum"], emptyRows([0,0], 3)));
children.push(p("👨‍👩‍👧 FAMILIEN-TERMINE / SCHULE (Arzt, Schwimmen, Waldtag, Anlässe)"));
children.push(tbl([5680, 3480], ["Termin", "Wann"], emptyRows([0,0], 3)));
children.push(sub("▸ Schritt 3: In Notion eintragen"));
children.push(chk("Haushalts-Liste in Notion (Felder: Aufgabe · Bereich · Rhythmus · Wochentag · Fixes Datum · Wer · Erledigt)"));
children.push(chk("Wiederkehrende Sachen eingetragen"));
children.push(chk("Datierte Sachen eingetragen"));
children.push(chk("Familien-Termine + Schule (Vorabend) eingetragen"));
children.push(sub("▸ Schritt 4: Bot bauen (WÄHREND des Videos)"));
children.push(chk("Haushalts-Helfer-Vorlage (Bonus) in Cowork eingesetzt"));
children.push(chk("Notion verbunden (Bot liest die Haushalts-Liste direkt — Connector aus 4.4)"));
children.push(chk("Getestet mit „Was ist heute zu Hause dran?\""));
children.push(chk("Der Bot hat mir Haushalt + Termine für heute ausgegeben ✓"));
children.push(small("Stufe 0 ohne Bot: Notion-Ansichten „📅 Termine & Schule\" + „🗓 Nach Wochentag\" öffnen."));
children.push(line("▸ Mein Haushalts-Helfer heisst:"));
children.push(sub("▸ Extra-Bonus Kochassistent — will ich den auch bauen?"));
children.push(p("☐ Ja, jetzt gleich   ☐ Später   (Vorlage liegt im Bonus-Bereich)"));
children.push(new Paragraph({ pageBreakBefore: true, children: [new TextRun("")] }));

// ---------------- 4.6 ----------------
children.push(H2("Lektion 4.6 · KI-Wochenplan — Mensch vs. Maschine"));
children.push(sub("▸ Die Regel in deinen Worten"));
children.push(line("KI macht:"));
children.push(line("Ich mache:"));
children.push(sub("▸ Deine 5 CEO-Aufgaben — bleiben IMMER deins"));
children.push(p("☐ Vision & Strategie    ☐ Entscheidungen    ☐ Brand & Stimme    ☐ Beziehungen    ☐ Reflexion & Zahlen"));
children.push(sub("▸ Dein KI-Wochenplan — stempel jede Aufgabe (🤖 KI / 🙋 ich)"));
children.push(tbl([6960, 2200], ["Aufgabe", "🤖 KI / 🙋 ich"], emptyRows([0,0], 10)));
children.push(sub("▸ Dein grösster „Aha\""));
children.push(p("Welche Aufgabe gibst du ab heute an die KI ab, die du bisher selbst gemacht hast?"));
children.push(blank());
children.push(sub("✓ Was du nach Säule 4 hast"));
children.push(p("2 KI-Mitarbeiter (Cockpit + Haushalt) · klare Mensch-Maschine-Linie · bereit für Säule 5 (Mama-CEO-Matrix)."));

// ---- doc ----
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 34, bold: true, font: "Arial", color: PETROL },
        paragraph: { spacing: { before: 120, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: PETROL },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 1 } },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1280, right: 1280, bottom: 1280, left: 1280 } } },
    children,
  }],
});

const out = process.argv[2];
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(out, buf); console.log("written " + out); });
