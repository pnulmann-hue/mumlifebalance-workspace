const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, AlignmentType } = require("docx");
const PETROL = "1F6F6B", GREY = "CCCCCC";
const sub = (t) => new Paragraph({ spacing: { before: 160, after: 60 }, children: [new TextRun({ text: t, bold: true, color: PETROL })] });
const p = (t) => new Paragraph({ spacing: { after: 60 }, children: [new TextRun(t)] });
const small = (t) => new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: t, italics: true, size: 20, color: "555555" })] });
const chk = (t) => new Paragraph({ spacing: { after: 40 }, children: [new TextRun("☐  " + t)] });
const line = (label) => new Paragraph({ spacing: { after: 80 }, children: [new TextRun(label ? label + "  " : ""), new TextRun({ text: "____________________________________________", color: "999999" })] });
const blank = () => new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "______________________________________________________________", color: "999999" })] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const cell = (text, w, head) => { const b = { style: BorderStyle.SINGLE, size: 1, color: GREY }; return new TableCell({ width: { size: w, type: WidthType.DXA }, borders: { top: b, bottom: b, left: b, right: b }, shading: head ? { fill: PETROL, type: ShadingType.CLEAR } : { fill: "FFFFFF", type: ShadingType.CLEAR }, margins: { top: 60, bottom: 60, left: 100, right: 100 }, children: [new Paragraph({ children: [new TextRun({ text, bold: !!head, color: head ? "FFFFFF" : "000000" })] })] }); };
const tbl = (widths, header, rows) => new Table({ width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths, rows: [new TableRow({ children: header.map((h, i) => cell(h, widths[i], true)) }), ...rows.map((r) => new TableRow({ children: r.map((c, i) => cell(c, widths[i])) }))] });
const empty = (widths, n) => Array.from({ length: n }, () => widths.map(() => " "));

const c = [];
c.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "Mama-CEO · Säule 5", bold: true, color: PETROL, size: 24 })] }));
c.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Arbeitsblatt — Business skalieren")] }));
c.push(small("Wochen 7-8 · 4 Lektionen · Das Finale: deine Mama-CEO-Matrix + dein 90-Tage-Plan."));
c.push(new Paragraph({ children: [new TextRun("")] }));

// 5.1
c.push(H2("Lektion 5.1 · Die Mama-CEO-Matrix"));
c.push(sub("▸ Schreib zu jedem Feld 1 Beispiel aus deinem Alltag"));
c.push(line("🙋 ICH (nur ich):"));
c.push(line("🤖 KI (Bot bereitet vor):"));
c.push(line("⚙️ SYSTEM (läuft ohne mich / festes Ämtli):"));
c.push(line("🗑 RAUS (darf aufhören):"));
c.push(sub("▸ Der KI-vs-System-Test (in eigenen Worten)"));
c.push(line("KI ist es, wenn:"));
c.push(line("System ist es, wenn:"));
c.push(new Paragraph({ pageBreakBefore: true, children: [new TextRun("")] }));

// 5.2
c.push(H2("Lektion 5.2 · MASTERY · Deine 25-Task-Matrix"));
c.push(small("Sammle 25 echte Aufgaben (Hütchen aus Säule 2 + Business-Alltag) und stempel jede in EIN Feld: 🙋 ich · 🤖 KI · ⚙️ System · 🗑 raus."));
c.push(tbl([900, 6060, 2200], ["#", "Aufgabe", "Feld"], Array.from({ length: 14 }, (_, i) => [String(i + 1), " ", " "])));
c.push(small("(Tipp: am besten direkt in deinem Notion-Template füllen — dort hast du die Matrix schon.)"));
c.push(sub("▸ Hilfsfragen, wenn du unsicher bist"));
c.push(p("🙋 ICH: Würde es meiner Marke/Beziehung schaden, wenn das wer anders macht?"));
c.push(p("🤖 KI: Vorbereitend/wiederholbar, braucht aber Urteil?"));
c.push(p("⚙️ SYSTEM: Läuft mechanisch / kann jemand fix übernehmen?"));
c.push(p("🗑 RAUS: Braucht das wirklich jemand?"));
c.push(sub("▸ Auswertung"));
c.push(p("Wie viele in 🙋 ich? ____   🤖 KI? ____   ⚙️ System? ____   🗑 raus? ____"));
c.push(line("Mein grösster Aha:"));
c.push(sub("▸ Meine nächsten 3 (aus KI/System — einrichten)"));
c.push(line("1.")); c.push(line("2.")); c.push(line("3."));
c.push(new Paragraph({ pageBreakBefore: true, children: [new TextRun("")] }));

// 5.3
c.push(H2("Lektion 5.3 · Dein innerer Kreis"));
c.push(sub("▸ Wer gehört in deinen inneren Kreis? (bleibt immer DEINS, nie KI/System)"));
c.push(line("👩 Bestandskundinnen / wichtigste Kundinnen:"));
c.push(line("🤝 Sparring-Partnerinnen / Mentorin:"));
c.push(line("👨‍👩‍👧‍👦 Familie (innerster Kreis):"));
c.push(sub("▸ Wie schützt du den Kreis? (feste Zeit reservieren)"));
c.push(tbl([4580, 4580], ["Beziehung", "Wann hat sie festen Platz in meiner Woche?"], empty([0, 0], 3)));
c.push(sub("▸ Eine Sache, die du ab heute NICHT mehr automatisierst:"));
c.push(blank());
c.push(new Paragraph({ pageBreakBefore: true, children: [new TextRun("")] }));

// 5.4
c.push(H2("Lektion 5.4 · Dein 90-Tage-Plan"));
c.push(sub("▸ Deine 3 Bauten für die nächsten 90 Tage (aus KI/System deiner Matrix)"));
c.push(line("1.   (bis wann: ____)"));
c.push(line("2.   (bis wann: ____)"));
c.push(line("3.   (bis wann: ____)"));
c.push(sub("▸ Was du JETZT NICHT machst (deine Fokus-Schutz-Liste)"));
c.push(line("1.")); c.push(line("2.")); c.push(line("3."));
c.push(sub("▸ Dein „fertig besser als perfekt\"-Vorsatz"));
c.push(p("Was startest du bewusst in Version 1 (statt es noch zu verschönern)?"));
c.push(blank());
c.push(sub("▸ Wie's weitergeht"));
c.push(chk("Ich bleibe in der Community aktiv"));
c.push(chk("Mein Cockpit-Bot erinnert mich täglich an meinen Plan"));
c.push(chk("Ich komme mit Matrix + Plan in den Live-Call 4"));
c.push(sub("✓ Was du nach Säule 5 hast — PROGRAMM ABGESCHLOSSEN"));
c.push(p("Deine Matrix gefüllt · innerer Kreis geschützt · 90-Tage-Plan + Nicht-Liste · du führst statt zu funktionieren. Du bist Mama-CEO. 💛"));

const doc = new Document({
  styles: { default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", run: { size: 34, bold: true, font: "Arial", color: PETROL }, paragraph: { spacing: { before: 120, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", run: { size: 26, bold: true, font: "Arial", color: PETROL }, paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 1 } },
    ] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1280, right: 1280, bottom: 1280, left: 1280 } } }, children: c }],
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(process.argv[2], b); console.log("written"); });
