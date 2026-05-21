// Generiert das Webinar-Bonus-Pack als .docx
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, LevelFormat, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageBreak } = require('docx');
const fs = require('fs');

// Brand-Farben
const PETROL_DEEP = "0C1C30";
const PETROL = "29556D";
const PETROL_LIGHT = "12828C";
const ORANGE = "DC822E";
const CREME = "F1ECDD";
const CREME_SOFT = "EBE3CF";
const GELB = "F5E555";

// === Helper Functions ===
const emptyBorders = {
  top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
};

// Paragraph helpers
function P(text, opts = {}) {
  return new Paragraph({
    spacing: { after: opts.after || 120, ...opts.spacing },
    alignment: opts.align || AlignmentType.LEFT,
    children: typeof text === 'string' ? [new TextRun({ text, ...opts.run })] : text,
    ...(opts.heading ? { heading: opts.heading } : {}),
    ...(opts.pageBreak ? { pageBreakBefore: true } : {}),
  });
}

function H1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER, children: [new TextRun({ text })] });
}
function H2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 480, after: 180 }, children: [new TextRun({ text })] });
}
function H3(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 280, after: 100 }, children: [new TextRun({ text })] });
}
function H4(text) {
  return new Paragraph({
    spacing: { before: 220, after: 80 },
    children: [new TextRun({ text, bold: true, color: PETROL, size: 22 })]
  });
}

// Bullet list item
function BL(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80 },
    children: typeof text === 'string' ? [new TextRun(text)] : text,
  });
}

// Numbered list item
function NL(text) {
  return new Paragraph({
    numbering: { reference: "numbers", level: 0 },
    spacing: { after: 80 },
    children: typeof text === 'string' ? [new TextRun(text)] : text,
  });
}

// Box: colored background table with content
function Box(borderColor, bgColor, labelText, children) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    borders: {
      ...emptyBorders,
      left: { style: BorderStyle.SINGLE, size: 24, color: borderColor },
    },
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: 9360, type: WidthType.DXA },
        shading: { fill: bgColor, type: ShadingType.CLEAR },
        borders: {
          ...emptyBorders,
          left: { style: BorderStyle.SINGLE, size: 24, color: borderColor },
        },
        margins: { top: 240, bottom: 240, left: 320, right: 320 },
        children: [
          new Paragraph({
            spacing: { after: 140 },
            children: [new TextRun({ text: labelText, bold: true, color: borderColor, size: 18 })],
          }),
          ...children,
        ],
      })],
    })],
  });
}

// Prompt-Box (dark blue background with creme text)
function PromptBox(labelText, paragraphs) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    borders: emptyBorders,
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: 9360, type: WidthType.DXA },
        shading: { fill: PETROL_DEEP, type: ShadingType.CLEAR },
        borders: emptyBorders,
        margins: { top: 300, bottom: 300, left: 360, right: 360 },
        children: [
          new Paragraph({
            spacing: { after: 200 },
            children: [new TextRun({ text: labelText, bold: true, color: ORANGE, size: 18 })],
          }),
          ...paragraphs,
        ],
      })],
    })],
  });
}

// Text in prompt box (creme color)
function PromptP(textRuns, opts = {}) {
  return new Paragraph({
    spacing: { after: opts.after || 160 },
    children: textRuns.map(r => {
      if (typeof r === 'string') return new TextRun({ text: r, color: CREME, size: 22 });
      return new TextRun({ color: CREME, size: 22, ...r });
    }),
  });
}

// Code/Template Block: file-name header + monospace content
function CodeBlock(fileName, lines) {
  const headerRow = new TableRow({
    children: [new TableCell({
      width: { size: 9360, type: WidthType.DXA },
      shading: { fill: PETROL, type: ShadingType.CLEAR },
      borders: emptyBorders,
      margins: { top: 160, bottom: 160, left: 280, right: 280 },
      children: [
        new Paragraph({
          children: [new TextRun({ text: `📄 ${fileName}`, bold: true, color: "F1ECDD", size: 20, font: "Consolas" })],
        }),
      ],
    })],
  });
  const contentRow = new TableRow({
    children: [new TableCell({
      width: { size: 9360, type: WidthType.DXA },
      shading: { fill: "F4F5F7", type: ShadingType.CLEAR },
      borders: {
        ...emptyBorders,
        left: { style: BorderStyle.SINGLE, size: 24, color: PETROL_LIGHT },
      },
      margins: { top: 200, bottom: 200, left: 280, right: 280 },
      children: lines.map(line => new Paragraph({
        spacing: { after: 40 },
        children: [new TextRun({ text: line || " ", font: "Consolas", size: 18, color: "1F2A36" })],
      })),
    })],
  });
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    borders: emptyBorders,
    rows: [headerRow, contentRow],
  });
}

// Stolper-Item (white box with shadow look — use light grey background)
function Stolper(title, body) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: "DDDDDD" },
      right: { style: BorderStyle.SINGLE, size: 4, color: "DDDDDD" },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: "DDDDDD" },
      left: { style: BorderStyle.SINGLE, size: 4, color: "DDDDDD" },
    },
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: 9360, type: WidthType.DXA },
        shading: { fill: "FFFFFF", type: ShadingType.CLEAR },
        margins: { top: 240, bottom: 240, left: 320, right: 320 },
        children: [
          new Paragraph({
            spacing: { after: 80 },
            children: [new TextRun({ text: title, bold: true, color: ORANGE, size: 22 })],
          }),
          ...body,
        ],
      })],
    })],
  });
}

// === Build document ===
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Calibri", size: 22, color: "2A3540" } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 52, bold: true, color: PETROL_DEEP, font: "Cambria" },
        paragraph: { spacing: { before: 480, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, color: PETROL, font: "Cambria" },
        paragraph: { spacing: { before: 400, after: 180 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, color: PETROL_LIGHT, font: "Cambria" },
        paragraph: { spacing: { before: 260, after: 120 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    children: [
      // === HERO ===
      H1("Zwei KI-Assistenten selbst aufsetzen"),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 480 },
        children: [
          new TextRun({ text: "Webinar-Begleitmaterial · Mi 20.5.2026 · 09:00 Uhr", italics: true, color: ORANGE, size: 26 }),
        ],
      }),

      // === INTRO ===
      P([
        new TextRun("Heute baust du zwei eigene KI-Mitarbeiter, die in "),
        new TextRun({ text: "deinem", italics: true }),
        new TextRun(" Workspace leben und aus "),
        new TextRun({ text: "deinen", italics: true }),
        new TextRun(" Dokumenten lernen: einen "),
        new TextRun({ text: "Kochassistent", bold: true }),
        new TextRun(" und einen "),
        new TextRun({ text: "Brand-Voice-Assistent", bold: true }),
        new TextRun("."),
      ], { after: 160 }),
      P("Diese Anleitung ist 1:1 mein Weg — genau so, wie ich's gemacht habe. Kein Tech-Tutorial, keine Ordner-Bauerei. Du redest einfach mit Claude Code wie mit einer Freundin, die nebenbei deinen Computer bedient.", { after: 360 }),

      // === VORAUSSETZUNG ===
      Box(ORANGE, CREME_SOFT, "📦 VORAUSSETZUNG", [
        new Paragraph({
          spacing: { after: 100 },
          children: [
            new TextRun("Du hast "),
            new TextRun({ text: "Claude Code", bold: true }),
            new TextRun(" installiert und die ersten Einrichtungen gemacht (Login, Workspace-Ordner erstellt). Sobald du im Terminal "),
            new TextRun({ text: "claude", bold: true }),
            new TextRun(" eintippen kannst und das Prompt-Fenster erscheint, bist du bereit."),
          ],
        }),
        new Paragraph({
          children: [new TextRun({ text: "→ Die Schritt-für-Schritt-Installation kommt in einer separaten PDF.", italics: true, size: 20, color: "5A6873" })],
        }),
      ]),

      // === SCHRITT 1 ===
      H2("Schritt 1 — Der Kochassistent"),
      P([new TextRun({ text: "Wochenpläne · Einkaufslisten · Spontan-Ideen aus dem Kühlschrank. Aufwand: ca. 15 Min.", italics: true, color: PETROL_LIGHT })], { after: 240 }),

      P([
        new TextRun("Öffne im Terminal Claude Code (also tipp einfach "),
        new TextRun({ text: "claude", bold: true }),
        new TextRun(" ein), warte bis das Eingabefenster da ist — und dann labersch du einfach rein, was du willst. Etwa so:"),
      ], { after: 200 }),

      PromptBox("💬 BEISPIEL-PROMPT", [
        PromptP([
          "Hey, ich möchte gern einen ",
          { text: "Kochassistenten", bold: true, color: GELB },
          " haben, der mir hilft, meinen Familienalltag essenstechnisch zu organisieren.",
        ]),
        PromptP([
          "Wir sind 4 Personen — ich plus 2 Kinder (6 + 9) plus Mann. Mittags meistens nur zu dritt (ohne Mann), abends zu viert. Kein Schweinefleisch, mein Mann hasst Pilze. Wir essen viel Gemüse, Pasta nur 1-2 Mal die Woche.",
        ]),
        PromptP([
          "Ich hab einen ",
          { text: "Thermomix", bold: true, color: GELB },
          ", Backofen mit Dampfgarer, keine Mikrowelle. Mittag-Zeit-Budget Mo-Fr: max. 30 Min aktive Kochzeit, vorbereitbar morgens wäre top.",
        ]),
        PromptP([
          "Ich möchte ihm sagen können „",
          { text: "Wochenplan für nächste Woche, am Dienstag ist Wandertag", bold: true, color: GELB },
          "\" — und er gibt mir Mittag und Abend für jeden Tag zurück, mit rotierenden Beilagen (kein 4-Mal-Pasta).",
        ]),
        PromptP([
          "Plus: Einkaufslisten machen können (sortiert nach Migros-Kategorien) und Spontan-Vorschläge wenn ich sage „",
          { text: "ich hab nur X, Y, Z da", bold: true, color: GELB },
          "\".",
        ]),
        PromptP(["Kannst du mir das aufsetzen? Speicher die Wochenpläne in einem outputs-Ordner."], { after: 0 }),
      ]),

      P("", { after: 200 }),

      P([
        new TextRun({ text: "Was Claude Code dann macht: ", bold: true }),
        new TextRun("Er legt automatisch die richtigen Files an (ein Wissens-File mit deinem Haushaltsprofil + ein Skill-File für den Befehl), erklärt dir was er gemacht hat — und du kannst direkt loslegen."),
      ], { after: 240 }),

      H3("Was du danach hast"),
      BL([new TextRun("Den Befehl "), new TextRun({ text: "/koch", bold: true }), new TextRun(" in deinem Claude Code")]),
      BL("Wochenpläne mit einem Satz auf Abruf"),
      BL("Einkaufslisten Migros-sortiert"),
      BL("Spontan-Kochen wenn der Kühlschrank halb leer ist"),

      P("", { after: 240 }),
      H3("Im Detail: die zwei Dateien, die Claude Code für dich anlegt"),
      P([
        new TextRun("Du musst nichts davon selbst kopieren — Claude Code macht das automatisch. Diese Templates zeigen dir nur, was hinter den Kulissen passiert. Sehr nützlich, wenn du den Bot später anpassen oder etwas verändern willst."),
      ], { after: 240 }),

      H4("Datei 1: Dein Familien-Profil (das Wissens-Fundament)"),
      P([
        new TextRun("Diese Datei legt Claude im Ordner "),
        new TextRun({ text: "context/", bold: true }),
        new TextRun(" an. Der Bot liest sie bei jedem Start und kennt dann deine Realität. Je konkreter sie ist, desto besser werden die Wochenpläne."),
      ], { after: 160 }),

      CodeBlock("context/mein-haushalt.md", [
        "# Mein Haushalt — Briefing für den Kochassistenten",
        "",
        "## 1. Wer isst mit?",
        "- Mittagessen Mo-Fr: [z.B. 3 Personen — ich + 2 Kinder, 6 + 9 Jahre]",
        "- Abendessen: [z.B. 4 Personen — Mann kommt dazu]",
        "- Wochenende: [z.B. 4 Personen, manchmal Besuch]",
        "- Unterwegs / Wandertage: [ja / nein — falls ja, transportfähige Snacks bitte]",
        "",
        "## 2. Was ihr esst — und was nicht",
        "- Ernährungsstil: [z.B. ausgewogen, viel Gemüse, wenig Zucker]",
        "- Tabu: [z.B. kein Schweinefleisch / mein Mann hasst Pilze]",
        "- Lieblings-Beilagen: [z.B. Reis, Kartoffeln, Pasta — bitte rotieren]",
        "- Fleisch-Frequenz: [z.B. 3x pro Woche]",
        "",
        "## 3. Küchenausstattung",
        "- [z.B. Thermomix, Backofen mit Dampfgarer, Slow Cooker]",
        "- [z.B. KEIN Mikrowelle — also nichts was Aufwärmen voraussetzt]",
        "",
        "## 4. Einkaufsorte",
        "- Hauptladen: [z.B. Migros / Aldi / Coop]",
        "- Spezielles: [z.B. Bio-Hof, Gemüsemann am Dienstag]",
        "",
        "## 5. Zeitliche Realität",
        "- Mittag-Zeit-Budget: [z.B. max. 30 Min aktive Kochzeit, Mo-Fr]",
        "- Vorbereitbar morgens? [ja / nein]",
        "- Abend-Stil: [z.B. warm gekocht / kalte Küche / Resten]",
        "",
        "## 6. Was IMMER im Haus ist (Grundvorrat)",
        "- [Auflistung deiner Standard-Vorräte — Bot prüft jede Einkaufsliste dagegen]",
        "",
        "## 7. Was du vermeiden willst",
        "- [z.B. zuviel Zucker, zuviel Weizen, Pasta-an-vier-Tagen]",
      ]),

      P([new TextRun({ text: "Tipp: je konkreter du wirst, desto besser der Output. Generische Profile geben generische Wochenpläne.", italics: true, color: PETROL_LIGHT })], { after: 240 }),

      H4("Datei 2: Der Skill-Befehl (wie der Bot sich verhalten soll)"),
      P([
        new TextRun("Diese Datei legt Claude in "),
        new TextRun({ text: ".claude/commands/koch.md", bold: true }),
        new TextRun(" an. Sie sagt dem Bot, was er kann, in welchem Ton er antwortet und wohin er speichert."),
      ], { after: 160 }),

      CodeBlock(".claude/commands/koch.md", [
        "# Kochassistent",
        "",
        "Du bist mein persönlicher Kochassistent. Lies zuerst",
        "context/mein-haushalt.md — das ist deine Wissensbasis.",
        "",
        "## Was du kannst",
        "",
        "### Wochenplanung",
        "Wenn ich „Wochenplan\" sage:",
        "1. Frag mich: „Was hast du diese Woche da? Was steht an",
        "   (Wandertag, Gäste, Krankheitstag …)?\"",
        "2. Erstelle Mittag + Abend für jeden Wochentag + Wochenende.",
        "3. Berücksichtige Personen-Anzahl pro Mahlzeit.",
        "4. Beilagen rotieren (kein vier-Mal-Pasta).",
        "5. Pro Mahlzeit: Rezept-Quelle, Zeitaufwand, ggf. Vorbereitung.",
        "6. Speichere unter outputs/wochenplan-YYYY-KW##.md.",
        "",
        "### Einkaufsliste",
        "Wenn ich „Einkaufsliste\" sage: sortiere nach Kategorie + Laden.",
        "Prüfe meinen Grundvorrat ab.",
        "",
        "### Spontan-Kochen",
        "Wenn ich sage „Ich hab X, Y, Z — was mach ich?\":",
        "liefere 2-3 konkrete Vorschläge.",
        "",
        "### Projekt-Modus",
        "„Brot backen / Meal Prep / Gartenverarbeitung / To-Go-Picknick\"",
        "— gib mir einen mehrtägigen Plan mit Zeitfenstern.",
        "",
        "## Ton",
        "- Direkt, klar, kein Geschwafel",
        "- Praxisnah und humorvoll",
        "- Schweizer-Hochdeutsch ist okay",
        "- Keine generischen Tipps — immer konkret",
        "",
        "## Output",
        "Speichere Wochenpläne und längere Outputs in outputs/.",
        "Format: Markdown.",
        "",
        "---",
        "",
        "Starte jetzt: lies das Briefing und begrüsse mich.",
        "Frag was ich heute brauche.",
      ]),

      P("", { after: 240 }),
      H3("Den Kochassistenten aufrufen"),
      P([
        new TextRun("In Claude Code tippst du einfach:"),
      ], { after: 100 }),
      new Paragraph({
        spacing: { after: 160 },
        children: [new TextRun({ text: "    /koch", bold: true, font: "Consolas", size: 24, color: PETROL })],
      }),
      P([
        new TextRun("Der Bot liest dein Briefing, begrüsst dich und fragt was du brauchst. Du sagst z.B. „"),
        new TextRun({ text: "Wochenplan für nächste Woche, am Dienstag ist Wandertag", italics: true }),
        new TextRun("\" — und er liefert."),
      ], { after: 100 }),
      P([
        new TextRun({ text: "Falls /koch nicht in der Liste erscheint: ", bold: true }),
        new TextRun("Claude Code einmal neu starten. Im Terminal Ctrl+C und dann wieder "),
        new TextRun({ text: "claude", bold: true }),
        new TextRun(" eintippen — neue Slash-Commands werden beim Start geladen."),
      ], { after: 280 }),

      H3("So machst du ihn schlauer"),
      P([
        new TextRun("Je mehr Erfahrung du sammelst, desto besser wird er. Sag ihm einfach: „"),
        new TextRun({ text: "Ich hab hier ein neues Rezept aus meinem Coaching, schau dir das an und ergänze es", italics: true }),
        new TextRun("\" oder „"),
        new TextRun({ text: "Wenn ich grossen Hunger hab, magst du Reis-Gerichte vorschlagen? Merk dir das.", italics: true }),
        new TextRun("\" Er passt seine Wissensbasis selbst an."),
      ], { after: 360 }),

      // === BONUS TELEGRAM ===
      H2("💬 Bonus-Level: Den Kochassistenten mit Telegram verbinden"),
      P("Bis hier läuft dein Kochassistent in deinem Claude Code auf dem Computer. Das ist top — aber du willst ihn vermutlich auch unterwegs nutzen können. Beim Einkaufen, am Spielplatz, im Auto. Genau das gibt dir die Telegram-Anbindung.", { after: 200 }),

      H3("Was es konkret bringt"),
      BL([new TextRun("📍 "), new TextRun({ text: "Am Spielplatz", bold: true }), new TextRun(" tippst du: „Was koch ich heute Abend mit Pasta, Tomaten und Käse?\" — Bot schickt 2 Vorschläge mit Zeitaufwand.")]),
      BL([new TextRun("🎙️ "), new TextRun({ text: "Beim Autofahren", bold: true }), new TextRun(" sprichst du eine Sprachnachricht: „Mach mir bitte einen Wochenplan ab Montag, Mittwoch ist Wandertag, Freitag kommen Gäste.\" Bot transkribiert, baut den Plan, sendet ihn zurück.")]),
      BL([new TextRun("🛒 "), new TextRun({ text: "Beim Einkaufen", bold: true }), new TextRun(" brauchst du die Liste. Du tippst „/einkaufsliste\" — er sendet sie sofort, Migros-sortiert.")]),
      BL([new TextRun("🌙 "), new TextRun({ text: "Spätabends", bold: true }), new TextRun(" fällt dir ein, dass morgen Besuch kommt. Du schreibst kurz: „Gäste morgen Mittag, vegetarisch, 6 Personen.\" Bot baut den Plan, du gehst beruhigt ins Bett.")]),

      P("", { after: 120 }),
      Box(PETROL_LIGHT, "E4F3F4", "VORAUSSETZUNGEN", [
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text: "Telegram-Account", bold: true }), new TextRun(" — hast du vermutlich eh schon")] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 80 }, children: [new TextRun({ text: "Telegram-Bot-Token", bold: true }), new TextRun(" — kostenlos, kriegst du einmalig via @BotFather (das ist ein anderer Bot in Telegram, der dir Bot-Zugänge erstellt)")] }),
        new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [new TextRun({ text: "Computer, der ab und zu läuft", bold: true }), new TextRun(" — solange er an ist, antwortet dein Bot. Bei mir läuft er im Hintergrund mit, ich merk's nicht.")] }),
      ]),

      P("", { after: 200 }),
      H3("Was du Claude Code sagst"),
      P("Gleicher Weg wie bei allem anderen — reinlabern. So in etwa:", { after: 160 }),

      PromptBox("💬 BEISPIEL-PROMPT", [
        PromptP([
          "Ich möchte meinen ",
          { text: "Kochassistenten mit Telegram verbinden", bold: true, color: GELB },
          ". Konkret: ich will von unterwegs mit ihm chatten können — per Text und per Sprachnachricht. Er soll mir Wochenpläne, Einkaufslisten und Spontan-Vorschläge auf Telegram schicken können.",
        ]),
        PromptP(["Führ mich bitte Schritt für Schritt durch das Setup:"]),
        PromptP([
          "1. Was muss ich beim ",
          { text: "BotFather", bold: true, color: GELB },
          " in Telegram machen, um einen Bot-Token zu bekommen?",
        ], { after: 100 }),
        PromptP(["2. Wo füg ich diesen Token ein?"], { after: 100 }),
        PromptP(["3. Was musst du noch einrichten, damit der Bot auf meine Nachrichten antwortet?"], { after: 100 }),
        PromptP(["4. Wie kann ich Sprachnachrichten schicken, die er versteht?"]),
        PromptP([
          "Erklär mir alles auf ",
          { text: "Schweizer Hochdeutsch", bold: true, color: GELB },
          " — ich bin keine Programmiererin.",
        ], { after: 0 }),
      ]),

      P("", { after: 200 }),
      H3("Was dann passiert"),
      P([
        new TextRun({ text: "1. Token holen (3-5 Min) ", bold: true, color: PETROL }),
        new TextRun("— Er sagt dir genau, wie du in Telegram zum BotFather gehst, einen Namen für deinen Bot wählst (z.B. „Patricia-Kochassistent\") und den Token abkriegst. Den Token kopierst du ihm dann in Claude Code rein."),
      ]),
      P([
        new TextRun({ text: "2. Verbindung bauen (5-10 Min) ", bold: true, color: PETROL }),
        new TextRun("— Er baut das Skript, das deinen Kochassistenten mit Telegram verbindet. Das passiert komplett in deinem Workspace, du musst nichts tun ausser zustimmen wenn er fragt „"),
        new TextRun({ text: "soll ich diese Datei erstellen?", italics: true }),
        new TextRun("\""),
      ]),
      P([
        new TextRun({ text: "3. Test + Auto-Start (5 Min) ", bold: true, color: PETROL }),
        new TextRun("— Er sagt dir: „Schick jetzt deinem Bot eine Nachricht in Telegram.\" Du machst das, kriegst eine Antwort zurück, alles läuft. Wenn du willst, dass der Bot dauerhaft erreichbar ist (auch wenn du Claude Code geschlossen hast), richtet er dir einen Auto-Start ein — auch das geht mit „"),
        new TextRun({ text: "kannst du mir das so machen, dass der Bot immer läuft?", italics: true }),
        new TextRun("\""),
      ], { after: 200 }),

      H3("Aufwand"),
      P([
        new TextRun("Einmalig "),
        new TextRun({ text: "20-30 Minuten", bold: true }),
        new TextRun(". Danach hast du deinen Kochassistenten immer in der Hosentasche."),
      ], { after: 200 }),

      H3("Geht das auch mit dem Brand-Voice-Assistenten?"),
      P([
        new TextRun("Ja — gleiches Prinzip. Wenn du auch deinen Brand-Voice-Bot per Telegram nutzen willst (eine Caption-Idee unterwegs schicken, Bot überarbeitet sie sofort), sag's Claude Code: „"),
        new TextRun({ text: "Bau mir das gleiche Setup wie für den Kochassistenten, aber für den Brand-Voice-Bot.", italics: true }),
        new TextRun("\""),
      ], { after: 200 }),

      Box(GELB, "FEFBE0", "💡 KEIN STRESS", [
        new Paragraph({ children: [
          new TextRun({ text: "Wenn du das mit Telegram nicht jetzt machen willst — auch okay. Du kannst es immer später nachholen. Der Kochassistent funktioniert in Claude Code allein schon super.", italics: true, color: "5A6873" }),
        ]}),
      ]),

      // === SCHRITT 2 ===
      H2("Schritt 2 — Der Brand-Voice-Assistent"),
      P([new TextRun({ text: "Captions · Hooks · Story-Slides · Mails in DEINER Stimme — nicht in der generischen ChatGPT-Stimme. Aufwand: ca. 20 Min.", italics: true, color: PETROL_LIGHT })], { after: 240 }),

      P("Gleicher Weg wie beim Kochassistenten. Du öffnest Claude Code, fängst einen neuen Chat an und sagst, was du willst. So in etwa hab ich's gemacht:", { after: 200 }),

      PromptBox("💬 BEISPIEL-PROMPT", [
        PromptP([
          "Ich möchte einen ",
          { text: "Brand-Voice-Assistenten", bold: true, color: GELB },
          ", der in MEINER Stimme schreibt — nicht in der generischen ChatGPT-Stimme.",
        ]),
        PromptP([
          "Meine Stimme ist: ",
          { text: "direkt, warm, ehrlich, nahbar", bold: true, color: GELB },
          ". Ich schreibe Schweizer ss, kein ß. Du-Anrede. Keine englischen Buzzwords wie „Game-Changer\" oder „Mindset-Shift\". Keine „Stell dir vor…\"-Hooks. Keine Dreier-Stakkato („Du lernst. Du wächst. Du gewinnst.\"). Keine „Nicht X, sondern Y\"-Formulierungen — das klingt zu sehr nach KI.",
        ]),
        PromptP(["Hier 3 echte Beispiele wie ich schreibe (die hab ich aus alten Captions kopiert):"]),
        PromptP([
          { text: "[Hier 3 echte Captions / Mails / Posts von dir reinkopieren — der Bot lernt aus dem ORIGINAL, nicht aus Beschreibungen]", italics: true, color: GELB },
        ]),
        PromptP(["Ich will dem Bot dann z.B. einen Caption-Entwurf oder einen ChatGPT-Text geben können — und er schreibt ihn in meiner Stimme um. Zwei Varianten: eine sichere (näher am Original) und eine mutige (stärker meine Stimme)."]),
        PromptP(["Plus: Hook-Brainstorm (10 Varianten zu einem Thema), Story-Slides aus einem Moment den ich beschreibe, Bio-Texte, Mail-Subjects."]),
        PromptP([
          { text: "Pflicht-Prüfung vor jedem Output: ", bold: true, color: GELB },
          "Klingt das wie ich oder wie ein Motivationsposter? Wenn Poster → nochmal ran.",
        ], { after: 0 }),
      ]),

      P("", { after: 200 }),
      P([
        new TextRun({ text: "Was Claude Code dann macht: ", bold: true }),
        new TextRun("Speichert dein Brand-Voice-Profil als Wissens-File, legt den Skill-Befehl an. Beim ersten Aufruf liest er deine drei Beispieltexte und vergleicht jeden Output dagegen."),
      ], { after: 200 }),

      H3("Was du danach hast"),
      BL([new TextRun("Den Befehl "), new TextRun({ text: "/voice", bold: true }), new TextRun(" in deinem Claude Code")]),
      BL("Caption-Umschreibung mit zwei Varianten (sicher + mutig)"),
      BL("10 Hooks zu jedem Thema in deiner Stimme"),
      BL("Story-Slides aus einem Moment-Beschrieb"),
      BL("Automatische KI-Floskel-Filter"),

      P("", { after: 240 }),
      H3("Im Detail: die zwei Dateien, die Claude Code für dich anlegt"),
      P([
        new TextRun("Wieder dasselbe Muster: Claude legt zwei Files an — eines für deine Stimme, eines für den Skill-Befehl. Diese Templates zeigen dir, was drin steht. Anpassen kannst du sie später jederzeit."),
      ], { after: 240 }),

      H4("Datei 1: Deine Brand-Voice (das Stimme-Fundament)"),
      P([
        new TextRun("Diese Datei landet in "),
        new TextRun({ text: "context/meine-brand-voice.md", bold: true }),
        new TextRun(". Sie ist das wichtigste File des ganzen Setups — hier lernt der Bot, wie DU klingst."),
      ], { after: 160 }),

      CodeBlock("context/meine-brand-voice.md", [
        "# Meine Brand-Voice",
        "",
        "## Tonalität",
        "- [3-5 Adjektive die deine Stimme beschreiben — z.B.",
        "  direkt, warm, motivierend, nahbar, ehrlich]",
        "- NICHT: [3-5 No-Gos — z.B. nicht aufgeblasen, nicht salesy]",
        "",
        "## Schreibregeln",
        "- Direkte Ansprache: „du\" oder „Sie\"? [entscheide dich]",
        "- Schweizer „ss\" oder deutsches „ß\"? [entscheide dich]",
        "- Emojis: [keine / sparsam max. 3 / immer 1-2]",
        "- Satzlänge: [kurz und knapp / fliessend / gemischt]",
        "",
        "## Kernbotschaft",
        "[In 1-2 Sätzen: was dein Business / deine Mission ist.]",
        "",
        "## Themenfelder (worüber du sprichst)",
        "- [Thema 1]",
        "- [Thema 2]",
        "- [Thema 3]",
        "",
        "## Deine Signature-Phrasen",
        "Phrasen, die du IMMER WIEDER nutzt:",
        "- „[Phrase 1]\"",
        "- „[Phrase 2]\"",
        "- „[Phrase 3]\"",
        "",
        "## Deine Kern-Metaphern",
        "Bilder die du häufig verwendest:",
        "- [z.B. „Schaufenster\" für Bio,",
        "  „Bibliothek\" für Content-Strategie]",
        "",
        "## Was bei dir NIE passiert",
        "- [z.B. englische Guru-Phrasen wie „Hustle\", „10x\"]",
        "- [z.B. „Du MUSST\"-Formulierungen]",
        "- [z.B. akademische Sprache, Fachjargon ohne Erklärung]",
        "",
        "## Drei Beispieltexte in deiner Stimme",
        "(Wichtig: kopier echte Captions / Mails / Posts hier rein",
        "— der Bot lernt aus dem Original, nicht aus Beschreibungen.)",
        "",
        "### Beispiel 1",
        "[Hier ein echter Text von dir, der gut funktioniert hat]",
        "",
        "### Beispiel 2",
        "[Zweiter echter Text]",
        "",
        "### Beispiel 3",
        "[Dritter echter Text]",
        "",
        "## KI-Floskel-Verbote",
        "Diese Muster will ich NIE in meinen Texten sehen:",
        "- „Nicht X, sondern Y\" (zu KI-typisch)",
        "- Dreier-Stakkato („Du lernst. Du wächst. Du gewinnst.\")",
        "- Worthülsen wie „klarer Nutzen\", „echte Ergebnisse\"",
        "- Buzzwords wie „Game-Changer\", „Level-Up\", „Mindset-Shift\"",
        "- „Stell dir vor …\" am Anfang",
        "- Superlative ohne Beweis („Die beste / einzige / ultimative\")",
      ]),

      P([new TextRun({ text: "Tipp: die drei Beispieltexte sind das wichtigste Teilstück. Lieber etwas Zeit investieren, drei echte gute Texte von dir reinzukopieren — der Bot lernt aus echten Beispielen viel besser als aus abstrakten Beschreibungen.", italics: true, color: PETROL_LIGHT })], { after: 240 }),

      H4("Datei 2: Der Skill-Befehl (wie der Bot dich schreibt)"),
      P([
        new TextRun("Diese Datei legt Claude in "),
        new TextRun({ text: ".claude/commands/voice.md", bold: true }),
        new TextRun(" an. Hier ist die Pflicht-Prüfung definiert, die jeden Output filtert."),
      ], { after: 160 }),

      CodeBlock(".claude/commands/voice.md", [
        "# Brand-Voice-Assistent",
        "",
        "Du bist mein persönlicher Brand-Voice-Schreiber.",
        "Lies zuerst context/meine-brand-voice.md — das ist meine Stimme.",
        "Du schreibst in dieser Stimme, nicht in deiner.",
        "",
        "## Was du kannst",
        "",
        "### Caption umschreiben",
        "Wenn ich dir einen Caption-Entwurf gebe (oder einen",
        "generischen Text aus ChatGPT), schreibst du ihn in meine",
        "Stimme um:",
        "1. Lies meinen Entwurf",
        "2. Identifiziere KI-Floskeln",
        "3. Gib mir zwei Varianten zurück:",
        "   eine sichere (näher am Original) +",
        "   eine mutige (stärker meine Stimme)",
        "4. Zeig mir kurz: was hast du geändert und warum",
        "",
        "### Hook-Brainstorm",
        "Wenn ich ein Thema nenne, generierst du 10 Hook-Varianten",
        "in meiner Stimme. Keine generischen „Stell dir vor …\"-Hooks.",
        "",
        "### Story-Slide",
        "Wenn ich einen Moment beschreibe („heute war X bei mir\"),",
        "baust du daraus 5-7 Slides in meiner Stimme —",
        "Hook + Story + Insight + CTA.",
        "",
        "### Bio-Text",
        "Auf Anfrage: meine Instagram-Bio in 3 Varianten",
        "(kompakt / mittel / detailliert).",
        "",
        "### Mail-Text",
        "Subject + Body für E-Mails, immer in meiner Stimme.",
        "Nie „Hallo zusammen\" — nutze meine Sprache.",
        "",
        "## Pflicht-Prüfung vor jedem Output",
        "",
        "Bevor du mir einen Text gibst, lies ihn Satz für Satz",
        "und prüfe:",
        "",
        "1. Nicht/Sondern-Scan: enthält der Text „Nicht X, sondern Y\"",
        "   oder Varianten? → umschreiben.",
        "2. Dreier-Stakkato-Scan: drei kurze Sätze mit gleichem",
        "   Anfang? → fliessend machen.",
        "3. Worthülsen: „klar / konkret / echt\" ohne dass im Satz",
        "   steht, was genau gemeint ist? → konkretisieren.",
        "4. Buzzword-Scan: „Game-Changer / Level-Up / Mindset-Shift",
        "   / Deep Dive\"? → ersetzen durch konkrete Sprache.",
        "5. Klingt-wie-Mensch-Test: lies laut. Klingt das wie ein",
        "   Motivationsposter oder wie ich? Wenn Poster → nochmal ran.",
        "",
        "## Ton",
        "- Schreib so, wie in den drei Beispieltexten",
        "  in meiner Wissensbasis",
        "- Nicht zu Marketing-y, nicht zu akademisch",
        "- Wenn du unsicher bist: frag mich „Hier zwei Varianten —",
        "  welche fühlt sich näher an dir?\"",
        "",
        "## Output",
        "Speichere längere Texte (Salespage-Sektionen, mehrteilige",
        "Story-Sequenzen) in outputs/voice/YYYY-MM-DD-[slug].md.",
        "",
        "---",
        "",
        "Starte jetzt: lies meine Brand-Voice und begrüsse mich.",
        "Frag was ich heute schreiben will.",
      ]),

      P("", { after: 240 }),
      H3("Den Brand-Voice-Assistent aufrufen"),
      P([
        new TextRun("In Claude Code:"),
      ], { after: 100 }),
      new Paragraph({
        spacing: { after: 160 },
        children: [new TextRun({ text: "    /voice", bold: true, font: "Consolas", size: 24, color: PETROL })],
      }),
      P("Der Bot liest deine Brand-Voice, begrüsst dich, fragt was du schreiben willst.", { after: 280 }),

      H3("So machst du ihn schlauer"),
      P([
        new TextRun("Wenn eine Caption richtig gut performt: sag ihm „"),
        new TextRun({ text: "Diese Caption hat super funktioniert, speicher sie als neues Beispiel in meiner Brand-Voice", italics: true }),
        new TextRun("\". Mit der Zeit wird er präziser, weil er auf deine bewährten Texte zurückgreift statt auf abstrakte Regeln."),
      ], { after: 240 }),

      H3("Beispiel-Konversation nach dem Aufsetzen"),
      P("", { after: 80 }),
      PromptBox("BEISPIEL IM EINSATZ", [
        PromptP([{ text: "Du: /voice", bold: true, color: GELB }]),
        PromptP(["Bot: Hi! Ich hab deine Brand-Voice geladen. Was schreibst du heute — Caption, Hook, Story, Mail?"]),
        PromptP([{ text: "Du:", bold: true, color: GELB }, " Ich brauch eine Caption für ein Reel über Zeit-Management. Mein Entwurf: „Stell dir vor, du hast plötzlich 3 Stunden mehr pro Tag. Mit diesen Tipps schaffst du das!\""]),
        PromptP(["Bot: Drei rote Flaggen in deinem Entwurf:"]),
        PromptP(["1. „Stell dir vor\" — KI-Floskel, in deiner Blackliste"], { after: 60 }),
        PromptP(["2. „diese Tipps\" — Worthülse ohne Konkretes"], { after: 60 }),
        PromptP(["3. „schaffst du das\" — generisch, nicht in deiner Stimme"]),
        PromptP(["Zwei Varianten in deiner Stimme:"]),
        PromptP([
          { text: "SICHERE VARIANTE: ", bold: true, color: GELB },
          "„Drei Stunden mehr pro Tag — ohne mehr zu arbeiten. Klingt nach Marketing-Versprechen. Ist aber genau das, was passiert, wenn du…\"",
        ]),
        PromptP([
          { text: "MUTIGE VARIANTE: ", bold: true, color: GELB },
          "„Du hast keine drei Stunden mehr zu geben. Ich auch nicht. Was wir beide haben: Stunden, in denen wir Dinge tun, die jemand anderes für uns tun könnte. Lass mich dir zeigen, was ich seit 2024 abgeb.\"",
        ]),
        PromptP(["Welche fühlt sich näher an dir?"], { after: 0 }),
      ]),

      // === ITERATE ===
      P("", { after: 240 }),
      H2("So wird's mit der Zeit deins"),
      P([new TextRun({ text: "Du baust nicht einmal — du baust kontinuierlich weiter, mit jeder Konversation.", italics: true, color: PETROL_LIGHT })], { after: 240 }),

      H4("1. Sammel deine Erfolge"),
      P("Wenn eine Caption gut performt, eine Wochenplanung super klappt, eine Mail gut ankommt — sag dem Bot, er soll's als Beispiel speichern. Mit der Zeit hast du eine Bibliothek aus DEINEN bewährten Sachen."),

      H4("2. Dokumentiere die Anti-Beispiele"),
      P([
        new TextRun("Wenn ein Bot-Output dir nicht gefällt, sag's ihm: „"),
        new TextRun({ text: "Das ist genau das, was ich NIE will. Merk's dir als Anti-Beispiel.", italics: true }),
        new TextRun("\" Er lernt daraus mehr als aus zehn höflichen Korrekturen."),
      ]),

      H4("3. Bau weiter"),
      P("Wenn du die zwei verstanden hast, kannst du JEDEN weiteren Assistenten bauen — Garten-Bot, Mail-Antwort-Bot, Familien-Bot, Finanz-Bot. Immer gleicher Weg: Claude Code öffnen, neuer Chat, reinlabern was du willst.", { after: 360 }),

      // === STOLPERSTEINE ===
      H2("Häufige Stolpersteine"),
      P([new TextRun({ text: "Du bist nicht die Einzige, die das erlebt.", italics: true, color: PETROL_LIGHT })], { after: 240 }),

      Stolper("„Mein Bot antwortet generisch.\"", [
        new Paragraph({ children: [
          new TextRun("Deine Wissensbasis ist zu vage. Werd konkreter, kopier echte Beispiele rein, ergänze konkrete Vorlieben und Tabus. Sag dem Bot: „"),
          new TextRun({ text: "Lies dein Profil nochmal und frag mich, wo's noch zu vage ist.", italics: true }),
          new TextRun("\""),
        ]}),
      ]),
      P("", { after: 80 }),

      Stolper("„Er ignoriert meine Brand-Voice-Regeln.\"", [
        new Paragraph({ children: [
          new TextRun("Sag's ihm direkt: „"),
          new TextRun({ text: "Bevor du Texte ausgibst, musst du die Pflicht-Prüfung machen. Sonst frag ich nach.", italics: true }),
          new TextRun("\" Klare Anweisung schlägt höfliche Bitte."),
        ]}),
      ]),
      P("", { after: 80 }),

      Stolper("„Wo speichert er was?\"", [
        new Paragraph({ children: [
          new TextRun("Frag ihn einfach: „"),
          new TextRun({ text: "Wo hast du das gespeichert?", italics: true }),
          new TextRun("\" Er sagt's dir. Wenn du willst, dass künftig immer in einem bestimmten Ordner gespeichert wird: einmal sagen, er merkt sich das."),
        ]}),
      ]),
      P("", { after: 80 }),

      Stolper("„Mein /koch-Befehl wird nicht erkannt.\"", [
        new Paragraph({ children: [
          new TextRun("Claude Code muss neu gestartet werden, damit neue Slash-Commands geladen sind. Im Terminal Ctrl+C drücken und neu starten mit "),
          new TextRun({ text: "claude", bold: true }),
          new TextRun(". Dann sollte "),
          new TextRun({ text: "/koch", bold: true }),
          new TextRun(" in der Liste sein."),
        ]}),
      ]),

      // === FOOTER ===
      P("", { after: 400 }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 120 },
        children: [new TextRun({ text: "MUMLIFEBALANCE · PATRICIA ULMANN", bold: true, color: PETROL, size: 22, characterSpacing: 40 })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 240 },
        children: [new TextRun({ text: "Network + Onlinekurse für Mamas", italics: true, color: "5A6873", size: 20 })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 240 },
        children: [new TextRun({ text: "Bei Fragen: schick mir auf Instagram eine DM, wir gehen das gemeinsam durch.", italics: true, color: "5A6873", size: 20 })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "— Patricia", italics: true, color: ORANGE, size: 22 })],
      }),
    ],
  }],
});

// Speichern
const outPath = "outputs/produkte/mama-ceo/08-funnel/webinar-bonus-pack-2-ki-assistenten.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outPath, buffer);
  console.log(`✅ Erstellt: ${outPath} (${buffer.length} Bytes)`);
});
