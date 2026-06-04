const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, LevelFormat, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageBreak
} = require("docx");

// ---- Brand ----
const PETROL = "1F6F6B";
const PETROL_LIGHT = "EAF2F1";
const GREY = "888888";
const LINE = "BBBBBB";
const A4_W = 11906, A4_H = 16838, MARGIN = 1440;
const CONTENT_W = A4_W - 2 * MARGIN; // 9026

// ---- helpers ----
const T = (text, opts = {}) => new TextRun({ text, ...opts });

const para = (children, opts = {}) =>
  new Paragraph({ children: Array.isArray(children) ? children : [children], ...opts });

// section title (lesson)
const lesson = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 140 },
    children: [T(text)],
  });

// sub-point ▸
const sub = (text) =>
  new Paragraph({
    spacing: { before: 200, after: 60 },
    children: [T("▸ ", { bold: true, color: PETROL }), T(text, { bold: true })],
  });

const body = (text) =>
  new Paragraph({ spacing: { after: 60 }, children: [T(text, { color: "333333" })] });

// a blank writing line (bottom border)
const wline = () =>
  new Paragraph({
    spacing: { before: 90, after: 90 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LINE, space: 1 } },
    children: [T("")],
  });
const wlines = (n) => Array.from({ length: n }, () => wline());

// labeled blank line "Label: ____"
const fieldLine = (label) =>
  new Paragraph({
    spacing: { before: 90, after: 90 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LINE, space: 1 } },
    children: [T(label + "  ", { bold: true })],
  });

const check = (text) =>
  new Paragraph({ spacing: { after: 40 }, children: [T("☐  "), T(text)] });

const numbered = (text, n) =>
  new Paragraph({
    spacing: { before: 90, after: 90 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: LINE, space: 1 } },
    children: [T(n + ".  ", { bold: true })],
  });

// result box (shaded, single cell)
const resultBox = (title, items) => {
  const border = { style: BorderStyle.SINGLE, size: 4, color: PETROL };
  const kids = [
    new Paragraph({ spacing: { after: 80 }, children: [T(title, { bold: true, color: PETROL })] }),
    ...items.map((i) => new Paragraph({ spacing: { after: 30 }, children: [T("✓  ", { bold: true, color: PETROL }), T(i)] })),
  ];
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: { top: border, bottom: border, left: border, right: border },
            width: { size: CONTENT_W, type: WidthType.DXA },
            shading: { fill: PETROL_LIGHT, type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 160, right: 160 },
            children: kids,
          }),
        ],
      }),
    ],
  });
};

// generic table
const cellBorder = { style: BorderStyle.SINGLE, size: 2, color: LINE };
const borders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };
const headCell = (text, w) =>
  new TableCell({
    borders, width: { size: w, type: WidthType.DXA },
    shading: { fill: PETROL, type: ShadingType.CLEAR },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ children: [T(text, { bold: true, color: "FFFFFF" })] })],
  });
const cell = (text, w) =>
  new TableCell({
    borders, width: { size: w, type: WidthType.DXA },
    margins: { top: 70, bottom: 70, left: 100, right: 100 },
    children: [new Paragraph({ children: [T(text || "", { color: "333333" })] })],
  });
const mkTable = (headers, widths, rows) =>
  new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, children: headers.map((h, i) => headCell(h, widths[i])) }),
      ...rows.map((r) => new TableRow({ children: r.map((c, i) => cell(c, widths[i])) })),
    ],
  });

const spacer = () => new Paragraph({ spacing: { after: 80 }, children: [T("")] });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

// ---- content ----
const children = [];

// Title block
children.push(new Paragraph({ spacing: { after: 40 }, children: [T("MAMA-CEO · ARBEITSBLATT", { bold: true, color: PETROL, size: 22 })] }));
children.push(new Paragraph({ children: [T("Säule 3 — Du baust die Struktur", { bold: true, size: 40, color: PETROL })] }));
children.push(new Paragraph({ spacing: { after: 160 }, children: [T("Strategie + Planung · Wochen 3-4", { italics: true, size: 26, color: GREY })] }));
children.push(new Paragraph({
  spacing: { after: 120 },
  border: { left: { style: BorderStyle.SINGLE, size: 18, color: PETROL, space: 8 } },
  children: [T("„Ich weiss genau, wann ich arbeite und wann ich Haushalt + Familie mache — und genau dadurch hab ich endlich verlässlich Zeit fürs Business.“", { italics: true, size: 24 })],
}));
children.push(body("So arbeitest du mit diesem Blatt: Bearbeite jede Sektion NACH dem dazugehörigen Video. Du musst nichts perfekt machen — fertig ist besser als perfekt. Bring das ausgefüllte Blatt zum Live-Call 2 (Notion-Brain-Sprechstunde, Ende Woche 4) mit."));
children.push(spacer());

// ---------- L3.1 ----------
children.push(lesson("Lektion 3.1 · Vom Brain Dump zur Struktur"));
children.push(sub("Sortier deinen Brain Dump aus Säule 2 in die 6 Lebens-Bereiche"));
children.push(body("Nimm dein Hütchen-Inventar + deine Aufgaben-Liste (4-Filter) aus Säule 2. Trag jede Aufgabe in den passenden Bereich ein."));
const areas31 = [
  ["🛍  Produkterstellung (eigene Kurse, Mini-Produkte, Templates)", 4],
  ["📱  Sichtbarkeit / Content (Posts, Reels, Stories)", 4],
  ["💬  Kundenbetreuung (DMs, Mails, 1:1, Community)", 4],
  ["🧘  Me-Time (Sport, Spaziergang, Beauty, Lernen)", 3],
  ["👨‍👩‍👧‍👦  Familie + Haushalt (aus deinem Haushalts-Wochenplan, S2 L2.5)", 4],
  ["📊  Reflexion (Sonntag-Reset, Zahlen-Check)", 2],
];
for (const [label, n] of areas31) {
  children.push(new Paragraph({ spacing: { before: 140, after: 40 }, children: [T(label, { bold: true })] }));
  children.push(...wlines(n));
}
children.push(sub("Welcher Bereich ist bei dir am vollsten? Welcher am leersten?"));
children.push(body("(Der leerste ist oft der wichtigste — meistens Me-Time oder Reflexion.)"));
children.push(fieldLine("Am vollsten:"));
children.push(fieldLine("Am leersten:"));
children.push(spacer());
children.push(resultBox("WAS DU NACH LEKTION 3.1 HAST", [
  "Du verstehst: Planung läuft von oben nach unten (Jahr → Tag)",
  "Dein Brain Dump ist in die 6 Lebens-Bereiche sortiert",
  "Du siehst welcher Bereich über- und welcher unterversorgt ist",
]));
children.push(pageBreak());

// ---------- L3.2 ----------
children.push(lesson("Lektion 3.2 · Notion als Business-Brain"));
children.push(sub("Was trägst du gerade alles im Kopf?"));
children.push(body("Schreib 5 Sachen auf, an die du regelmässig „denken musst“ (z.B. „Newsletter rausschicken“, „Termin Kinderarzt“, „Reel für Freitag“). Genau die bekommen ab jetzt einen Platz ausserhalb deines Kopfes."));
children.push(...wlines(5));
children.push(sub("Deine 4 Stufen auf Papier (erste Skizze)"));
children.push(fieldLine("JAHR — welche 3 grossen Sachen kommen dieses Jahr noch? (Produkt/Launch/Thema)"));
children.push(...wlines(2));
children.push(fieldLine("MONAT — was ist dein Fokus diesen Monat?"));
children.push(fieldLine("WOCHE — welche Fokus-Säule hat diese Woche (Plattform/Produkt/Verkauf)?"));
children.push(fieldLine("TAG — was sind heute deine 3 wichtigsten Aufgaben?"));
children.push(...wlines(3));
children.push(sub("Deine 1-3 Ziele (roter Faden)"));
children.push(body("Was ist dein wichtigstes Ziel für die nächsten 90 Tage?"));
children.push(...wlines(2));
children.push(spacer());
children.push(resultBox("WAS DU NACH LEKTION 3.2 HAST", [
  "Du verstehst Notion als Entlastung, nicht als zusätzliche Arbeit",
  "Du kennst die 4 Stufen und wie sie zusammenhängen",
  "Du hast eine erste Papier-Skizze deiner Struktur (bereit für 3.5)",
]));
children.push(pageBreak());

// ---------- L3.3 ----------
children.push(lesson("Lektion 3.3 · Jahres-Strategie — was kommt WANN"));
children.push(sub("Schritt 1: Trag ZUERST deine Fixpunkte ein"));
children.push(body("Was steht fest, bevor du planst? (Schulferien, Testwochen, Anlässe/Events)"));
children.push(mkTable(
  ["Monat", "Ferien / reduziert", "Testwoche / Anlass"],
  [2000, 3513, 3513],
  [["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""]]
));
children.push(sub("Schritt 2: Dein Monats-Rhythmus — pro Monat 3 Produkte"));
children.push(body("Für jeden Monat: was ist dein Gratis-, dein Mini-, dein grosses Produkt? (Darf sich wiederholen.)"));
children.push(mkTable(
  ["Monat", "🎁 Gratis", "💶 Mini", "💎 Gross"],
  [2000, 2342, 2342, 2342],
  [["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""]]
));
children.push(sub("Schritt 3: Transformation statt Produkt"));
children.push(fieldLine("Dein Hauptprodukt:"));
children.push(fieldLine("Das ZIEL deiner Kundin dahinter (die Transformation):"));
children.push(body("Was muss sie dafür lernen / können? (= deine Überthemen)"));
children.push(fieldLine("1."));
children.push(fieldLine("2."));
children.push(fieldLine("3."));
children.push(sub("Schritt 4: Überthemen auf die Wochen verteilen"));
children.push(body("Über welches Überthema redest du in welcher Woche? (1 Überthema pro Woche reicht)"));
children.push(mkTable(
  ["Woche", "Überthema"],
  [2000, 7026],
  [["KW ___", ""], ["KW ___", ""], ["KW ___", ""], ["KW ___", ""]]
));
children.push(spacer());
children.push(resultBox("WAS DU NACH LEKTION 3.3 HAST", [
  "Deine Fixpunkte (Ferien, Testwochen, Anlässe) stehen zuerst",
  "Dein Monats-Rhythmus steht: pro Monat Gratis + Mini + grosses Produkt",
  "Du denkst in Transformation statt Produkt — und hast deine Überthemen",
  "Deine Überthemen sind auf Wochen verteilt = du weisst immer, worüber du redest",
  "Du hast das Fundament für deinen Content (das WIE kommt in der Insta-Kundenmaschine)",
]));
children.push(pageBreak());

// ---------- L3.4 ----------
children.push(lesson("Lektion 3.4 · Monats- + Wochenplanung mit den 6 Lebens-Bereichen"));
children.push(sub("Dein Monatsplan (aktueller Monat)"));
children.push(fieldLine("Monatsfokus (1 Satz):"));
children.push(body("3 Monatsziele:"));
children.push(fieldLine("1."));
children.push(fieldLine("2."));
children.push(fieldLine("3."));
children.push(fieldLine("Launch / grosse Sache diesen Monat (falls):"));
children.push(sub("Welche Lebens-Bereiche sind DIESEN Monat aktiv?"));
children.push(body("Markier nur die, die diesen Monat wirklich dran sind (nicht jeder muss jeden Monat). Tipp: Me-Time + Reflexion möglichst nie ganz rauslassen."));
children.push(check("🛍  Produkterstellung"));
children.push(check("📱  Sichtbarkeit"));
children.push(check("💬  Kundenbetreuung"));
children.push(check("🧘  Me-Time"));
children.push(check("👨‍👩‍👧‍👦  Familie + Haushalt"));
children.push(check("📊  Reflexion"));
children.push(sub("Deine Beispiel-Woche — aktive Bereiche in deine eigenen Slots"));
children.push(body("Trag deine echten Power-Slots ein (manche haben 2/Tag, manche nur einen — nimm DEINE). In jeden Slot kommt ein aktiver Bereich PLUS die konkrete Aufgabe aus Säule 2. Format: „Bereich — Aufgabe“ (z.B. „Produkterstellung — Modul 2 aufnehmen“). Der CEO-Fokus ist die Brille, der Bereich die Aufgabe."));
children.push(mkTable(
  ["Tag", "CEO-Fokus (Brille)", "Slot 1", "Slot 2 (falls)", "gelber Mama-Slot"],
  [900, 2100, 2300, 1726, 2000],
  [
    ["Mo", "Strategie", "", "", ""],
    ["Di", "Brand", "", "", ""],
    ["Mi", "Beziehungen", "", "", ""],
    ["Do", "Entscheidungen", "", "", ""],
    ["Fr", "Reflexion", "", "", ""],
    ["Sa", "—", "(frei / Familie)", "—", ""],
    ["So", "Reset 15 Min", "", "—", ""],
  ]
));
children.push(sub("Tagesplaner-Vorlage (zum täglichen Kopieren)"));
children.push(fieldLine("Datum: __________   Tagesfokus:"));
children.push(body("Meine 3 Hauptaufgaben heute:"));
children.push(fieldLine("1."));
children.push(fieldLine("2."));
children.push(fieldLine("3."));
children.push(fieldLine("Abend-Reflexion (1-2 Sätze):"));
children.push(spacer());
children.push(resultBox("WAS DU NACH LEKTION 3.4 HAST", [
  "Dein Monatsplan steht (1 Fokus + 3 Ziele + aktive Bereiche diesen Monat)",
  "Deine Beispiel-Woche hat deine aktiven Bereiche in deinen eigenen Slots",
  "Du hast eine Tagesplaner-Vorlage für 30-Sekunden-Tagesplanung",
]));
children.push(pageBreak());

// ---------- L3.5 ----------
children.push(lesson("Lektion 3.5 · MASTERY · Notion-Master-Template einrichten"));
children.push(sub("Einricht-Checkliste — häkchen-für-häkchen"));
children.push(body("Mach das WÄHREND du das Video schaust. Pause wo nötig."));
children.push(check("Schritt 1: Master-Template dupliziert (Link aus dem Kursbereich)"));
children.push(check("Schritt 2: Jahres-DB gefüllt (aus Arbeitsblatt 3.3)"));
children.push(check("Schritt 3: Monats-DB gefüllt + mit Jahr verknüpft (aus 3.4)"));
children.push(check("Schritt 4: Wochen-DB angelegt — KW, Fokus-Säule, Power-Zeiten, aktive Bereiche"));
children.push(check("Schritt 5: Tagesplaner für heute angelegt + mit Woche verknüpft"));
children.push(check("Schritt 6: 1-3 Ziele eingetragen + als roter Faden verknüpft"));
children.push(check("Schritt 7: 4 Rollen + Hütchen-Inventar (aus S2) als Referenz abgelegt"));
children.push(check("Schritt 8: 90-Tage-Tracker scharf gestellt"));
children.push(sub("Wo hängst du? Notier deine 1 offene Frage für Live-Call 2:"));
children.push(...wlines(2));
children.push(body("→ Bring dein eingerichtetes Notion zum Live-Call 2 (Notion-Brain-Sprechstunde, Ende W4)."));
children.push(spacer());
children.push(resultBox("WAS DU NACH LEKTION 3.5 HAST · KERN-LEISTUNG VON SÄULE 3", [
  "Dein Notion-Business-Brain steht — 4 Stufen + Ziele, alles verknüpft",
  "Jahr, Monat, Woche, Tag sind befüllt und greifen ineinander",
  "Deine Arbeit aus Säule 1+2 ist nach Notion übertragen (nichts verloren)",
  "Der 90-Tage-Tracker läuft",
]));
children.push(pageBreak());

// ---------- L3.6 ----------
children.push(lesson("Lektion 3.6 · Notfall-Modus — dein 50%-Plan"));
children.push(sub("Deine minimale Woche"));
children.push(body("Was ist die EINE Business-Sache, die auch im Notfall nicht warten kann?"));
children.push(...wlines(2));
children.push(sub("Was BLEIBT (grün) — maximal 3 Sachen"));
children.push(fieldLine("1."));
children.push(fieldLine("2."));
children.push(fieldLine("3."));
children.push(sub("Was PAUSIERT (rot) — was darf bewusst warten?"));
children.push(fieldLine("1."));
children.push(fieldLine("2."));
children.push(fieldLine("3."));
children.push(sub("Dein Content-Puffer"));
children.push(body("Wie viele Wochen Content willst du im Voraus vorbereiten, damit Sichtbarkeit auch im Notfall läuft? (Story-Strategie lernst du in der Insta-Kundenmaschine.)"));
children.push(fieldLine("Anzahl Wochen Puffer:"));
children.push(fieldLine("Wann baust du diesen Puffer auf?"));
children.push(sub("Dein Notfall-Tagesplaner (als Notion-Vorlage anlegen)"));
children.push(fieldLine("EINE Business-Sache heute:"));
children.push(new Paragraph({ spacing: { before: 90 }, children: [T("☐  "), T("Rest: Familie. Und: „Heute reicht das.“ "), T("(Erlaubnis-Häkchen)", { italics: true, color: GREY })] }));
children.push(spacer());
children.push(resultBox("WAS DU NACH LEKTION 3.6 HAST · SÄULE 3 KOMPLETT", [
  "Du hast einen 50%-Plan, bevor du ihn brauchst",
  "Du weisst was bleibt und was pausiert — vorher entschieden",
  "Du hast einen Content-Puffer-Plan",
  "Du hast einen Notfall-Tagesplaner als Notion-Vorlage",
  "Du hast Säule 3 abgeschlossen — deine Struktur steht",
]));

// ---- document ----
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: PETROL },
        paragraph: { spacing: { before: 360, after: 140 }, outlineLevel: 0,
          border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: PETROL, space: 4 } } },
      },
    ],
  },
  sections: [{
    properties: { page: { size: { width: A4_W, height: A4_H }, margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN } } },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("mama-ceo-arbeitsblatt-saeule-3.docx", buf);
  console.log("WROTE mama-ceo-arbeitsblatt-saeule-3.docx (" + buf.length + " bytes)");
});
