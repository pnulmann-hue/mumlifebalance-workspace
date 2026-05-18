// Mama-CEO Webinar Pitch-Slides — PowerPoint Generator
// 22 Slides, Brand-Farben, 16:9 Format
// Run: cd scripts/pptx-builder && node build-webinar.js

const pptxgen = require("pptxgenjs");
const path = require("path");

// === Brand Colors (no # prefix für pptxgenjs!) ===
const C = {
  creme: "f1ecdd",
  cremeSoft: "faf6ec",
  petrol: "12828c",
  petrolDark: "0a5e66",
  dunkelblau: "29556d",
  dunkelblauDark: "1f4258",
  orange: "dc822e",
  orangeTief: "c06b1e",
  gelb: "f5e555",
  text: "0c1c30",
  muted: "5a6b7a",
  white: "ffffff",
};

// === Fonts (fallback to Cambria/Calibri if Philosopher/Source Sans 3 nicht installiert) ===
const F = {
  serif: "Philosopher",
  serifFallback: "Cambria",
  sans: "Source Sans 3",
  sansFallback: "Calibri",
};

// === Setup ===
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3" × 7.5" — schöne Breite
pres.author = "Patricia Nulmann";
pres.title = "Mama-CEO Webinar — 20. Mai 2026";

// Slide dimensions (W=13.333, H=7.5)
const W = 13.333;
const H = 7.5;

// === HELPER: Eyebrow + Headline + Body Layout ===
function addEyebrow(slide, text, color, x = 1, y = 0.6) {
  slide.addText(text, {
    x, y, w: W - 2, h: 0.4,
    fontFace: F.sans, fontSize: 14, color, bold: true,
    charSpacing: 5, align: "left", margin: 0,
  });
}

function addHeadline(slide, text, color = C.dunkelblau, opts = {}) {
  slide.addText(text, {
    x: opts.x || 1, y: opts.y || 1.2, w: opts.w || W - 2, h: opts.h || 1.8,
    fontFace: F.serif, fontSize: opts.size || 52, color, bold: true,
    align: opts.align || "left", valign: "top",
    margin: 0, ...opts,
  });
}

function addBody(slide, text, color, opts = {}) {
  slide.addText(text, {
    x: opts.x || 1, y: opts.y || 4, w: opts.w || W - 2, h: opts.h || 2,
    fontFace: F.sans, fontSize: opts.size || 18, color,
    align: opts.align || "left", valign: "top",
    paraSpaceAfter: 8, ...opts,
  });
}

function addFooterSignature(slide, text, color = C.muted) {
  slide.addText(text, {
    x: 1, y: H - 0.7, w: W - 2, h: 0.4,
    fontFace: F.serif, fontSize: 13, italic: true, color,
    align: "left", margin: 0,
  });
}

// ============================================================
// SLIDE 1 — TITEL
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.creme };

  s.addText("Live-Webinar · 20. Mai 2026 · 09:00", {
    x: 1, y: 1.2, w: W - 2, h: 0.5,
    fontFace: F.sans, fontSize: 14, color: C.petrol, bold: true,
    charSpacing: 6, align: "center", margin: 0,
  });

  s.addText("In 90 Min:", {
    x: 1, y: 2.0, w: W - 2, h: 0.9,
    fontFace: F.serif, fontSize: 56, color: C.dunkelblau, bold: true,
    align: "center", margin: 0,
  });
  s.addText("Dein Mama-Leben mit KI-Assistenten umkrempeln.", {
    x: 1, y: 2.9, w: W - 2, h: 1.6,
    fontFace: F.serif, fontSize: 48, color: C.dunkelblau, bold: true,
    align: "center", margin: 0,
  });

  s.addText("Mental Load abgeben · Zeit fürs Business zurück gewinnen.", {
    x: 1, y: 4.7, w: W - 2, h: 0.6,
    fontFace: F.serif, italic: true, fontSize: 22, color: C.petrol,
    align: "center", margin: 0,
  });

  // Orange Linie
  s.addShape(pres.shapes.RECTANGLE, {
    x: W/2 - 1, y: 5.6, w: 2, h: 0.06, fill: { color: C.orange }, line: { color: C.orange },
  });

  s.addText("— Patricia · Mum Life Balance", {
    x: 1, y: 6.5, w: W - 2, h: 0.4,
    fontFace: F.serif, italic: true, fontSize: 16, color: C.muted,
    align: "center", margin: 0,
  });

  s.addNotes("Sprechzeit: 1 Min. Willkommen, schön bist du da. Ich bin Patricia, 4-fach-Mama aus dem Appenzellerland. In den nächsten 90 Minuten geben wir dir zurück, was du gerade verlierst: deine Zeit. Mein Plan: Ich zeig dir live, wie ich mit KI-Assistenten 18 Stunden die Woche reichen — und ich bau das genau hier vor deinen Augen auf.");
}

// ============================================================
// SLIDE 2 — Patricias Story (Hamsterrad)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };

  addEyebrow(s, "2023 — wo ich war", C.orange);
  addHeadline(s, "Ich war gefangen.", C.dunkelblau, { y: 1.2, size: 56 });

  s.addText([
    { text: "4 Kinder. Vollzeit-Job in der Sozialverwaltung.", options: { breakLine: true } },
    { text: "Sonntagabend Bauchschmerzen vor Montag.", options: { breakLine: true } },
    { text: "Mama-Logistik-Discos jeden Morgen.", options: {} },
  ], {
    x: 1, y: 3.3, w: W - 2, h: 1.5,
    fontFace: F.sans, fontSize: 22, color: C.text,
    paraSpaceAfter: 6, margin: 0,
  });

  // Orange Quote-Block
  s.addShape(pres.shapes.RECTANGLE, {
    x: 1, y: 5.1, w: 0.1, h: 1.4, fill: { color: C.orange }, line: { color: C.orange },
  });
  s.addText(`„Oh, hoffentlich kann ich morgen arbeiten gehen."`, {
    x: 1.4, y: 5.1, w: W - 2.5, h: 0.9,
    fontFace: F.serif, italic: true, fontSize: 28, color: C.orange,
    align: "left", margin: 0,
  });
  s.addText("Der Satz, den ich mir jeden Sonntag selbst sagte.", {
    x: 1.4, y: 6.0, w: W - 2.5, h: 0.5,
    fontFace: F.sans, fontSize: 16, color: C.muted, italic: true,
    align: "left", margin: 0,
  });

  s.addNotes("Sprechzeit: 3 Min. Ich erzähl dir kurz wo ich vor zwei Jahren stand. Ich war Sachbearbeiterin in der Sozialverwaltung. Hab den Job geliebt — aber jeden Sonntagabend hatte ich Bauchschmerzen vor Montag. Mama-Logistik. Wer holt das Kind ab wenn's krank wird. Mit 4 Kindern konnte ich nicht regulär arbeiten gehen, weil die Kinderbetreuung mehr kostete als mein Lohn. Ich war im Hamsterrad. Genau wie du vielleicht gerade auch.");
}

// ============================================================
// SLIDE 3 — Wendepunkt (Petrol-Hintergrund)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.petrol };

  s.addText("Mai 2025 — der Wendepunkt", {
    x: 1, y: 1.2, w: W - 2, h: 0.5,
    fontFace: F.sans, fontSize: 14, color: C.gelb, bold: true,
    charSpacing: 6, align: "left", margin: 0,
  });

  s.addText("Meine Schwester ist mit 44 gestorben.", {
    x: 1, y: 2.0, w: W - 2, h: 1.0,
    fontFace: F.serif, fontSize: 44, color: C.creme, bold: true,
    align: "left", margin: 0,
  });
  s.addText("Da hab ich verstanden:", {
    x: 1, y: 3.0, w: W - 2, h: 0.7,
    fontFace: F.serif, fontSize: 28, color: C.creme,
    align: "left", margin: 0,
  });

  s.addText(`„Eine Mutter darf ein eigenes Leben leben."`, {
    x: 1, y: 4.0, w: W - 2, h: 1.0,
    fontFace: F.serif, italic: true, fontSize: 36, color: C.gelb, bold: true,
    align: "left", margin: 0,
  });

  s.addText([
    { text: "Seitdem läuft mein Business mit System + KI.", options: { breakLine: true } },
    { text: "4 Kinder. 18h pro Woche. Kein Monat ohne Verkauf.", options: {} },
  ], {
    x: 1, y: 5.6, w: W - 2, h: 1.0,
    fontFace: F.sans, fontSize: 18, color: C.creme,
    paraSpaceAfter: 4, margin: 0,
  });

  s.addNotes("Sprechzeit: 3 Min. Mai 2019 ist meine Schwester gestorben. Mit 44. Das hat mir die Augen geöffnet — eine Mutter darf ein eigenes Leben leben. Seitdem läuft was. Aber erst Mai 2025 hab ich kapiert: ich brauche kein neues Mindset, ich brauche ein neues System. Ich hab aufgehört, manuell zu arbeiten. Hab angefangen, mir KI-Mitarbeiter zu bauen. Heute hab ich 13. Solo. Ohne Tech-Hintergrund. 18 Stunden die Woche. Kein Monat ohne Verkauf seit Mai 2025.");
}

// ============================================================
// SLIDE 4 — Drei DMs
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.creme };

  addHeadline(s, "Drei Fragen, die ich jeden Tag in die DMs kriege:", C.dunkelblau, { y: 0.8, size: 32, align: "center" });

  // 3 Zitate als Boxen
  const quotes = [
    { text: `„Wie finde ich Kunden?"`, y: 2.5 },
    { text: `„Wo soll ich überhaupt anfangen?"`, y: 3.7 },
    { text: `„Was poste ich jetzt?"`, y: 4.9 },
  ];
  quotes.forEach(q => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: 2, y: q.y, w: 0.1, h: 0.9, fill: { color: C.orange }, line: { color: C.orange },
    });
    s.addText(q.text, {
      x: 2.4, y: q.y, w: W - 4, h: 0.9,
      fontFace: F.serif, italic: true, fontSize: 32, color: C.petrol,
      valign: "middle", margin: 0,
    });
  });

  s.addText("Von Mamas im Network. Seit Jahren dabei. Viele Follower. Null Anfragen.", {
    x: 1, y: 6.4, w: W - 2, h: 0.5,
    fontFace: F.sans, italic: true, fontSize: 16, color: C.muted,
    align: "center", margin: 0,
  });

  s.addNotes("Sprechzeit: 1 Min. Ich bekomm jeden Tag dieselben drei Fragen in die DMs. Wie finde ich Kunden. Wo soll ich anfangen. Was poste ich jetzt. Du auch? Schreib mir kurz im Chat ein 'J' wenn du das kennst.");
}

// ============================================================
// SLIDE 5 — Hamsterrad-Diagnose (4 Pain-Karten)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };

  addHeadline(s, "Du bist nicht faul.", C.dunkelblau, { y: 0.7, size: 42, align: "center" });
  s.addText("Du hast nur kein System.", {
    x: 1, y: 1.6, w: W - 2, h: 0.7,
    fontFace: F.serif, fontSize: 30, italic: true, color: C.orange,
    align: "center", margin: 0,
  });

  // 4 Pain-Karten als Grid (2x2)
  const pains = [
    { num: "01", text: "Du arbeitest noch 60–80% in deinem alten Job.", x: 1, y: 3.0 },
    { num: "02", text: "Dein Mann schaut dein Business als Hobby an.", x: 7, y: 3.0 },
    { num: "03", text: "Du machst alles selbst — bis 22 Uhr.", x: 1, y: 4.7 },
    { num: "04", text: `„Diesen Monat können wir nicht auswärts essen."`, x: 7, y: 4.7 },
  ];
  pains.forEach(p => {
    s.addText(p.num, {
      x: p.x, y: p.y, w: 1, h: 1,
      fontFace: F.serif, fontSize: 48, color: C.orange, bold: true,
      align: "left", valign: "top", margin: 0,
    });
    s.addText(p.text, {
      x: p.x + 1.2, y: p.y + 0.15, w: 4.3, h: 1.3,
      fontFace: F.sans, fontSize: 16, color: C.text,
      align: "left", valign: "top", margin: 0,
    });
  });

  s.addText("Du steckst im Hamsterrad. Das ist System-Problem, nicht Disziplin-Problem.", {
    x: 1, y: 6.6, w: W - 2, h: 0.5,
    fontFace: F.sans, italic: true, fontSize: 14, color: C.muted,
    align: "center", margin: 0,
  });

  s.addNotes("Sprechzeit: 3 Min. Lass mich raten. Du arbeitest noch in deinem alten Job. Dein Mann denkt dein Business ist ein Instagram-Hobby. Du machst alles selbst. Und einmal pro Woche fragst du dich: oh shit, wie viel hab ich noch auf dem Konto. Du bist nicht faul. Du hast nur ein System-Problem. Genau das.");
}

// ============================================================
// SLIDE 6 — Daten-Anker 58%
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.dunkelblau };

  s.addText("WAS DATEN ZEIGEN 2026", {
    x: 1, y: 1.0, w: W - 2, h: 0.5,
    fontFace: F.sans, fontSize: 14, color: C.gelb, bold: true,
    charSpacing: 8, align: "center", margin: 0,
  });

  // MEGA-Zahl
  s.addText("58 %", {
    x: 1, y: 2.0, w: W - 2, h: 2.5,
    fontFace: F.serif, fontSize: 200, color: C.creme, bold: true,
    align: "center", margin: 0,
  });

  s.addText("der Unternehmerinnen mit KI-Assistenten", {
    x: 1, y: 4.8, w: W - 2, h: 0.7,
    fontFace: F.serif, italic: true, fontSize: 26, color: C.gelb,
    align: "center", margin: 0,
  });
  s.addText("sparen 20+ Stunden pro Monat.", {
    x: 1, y: 5.5, w: W - 2, h: 0.7,
    fontFace: F.serif, italic: true, fontSize: 26, color: C.gelb,
    align: "center", margin: 0,
  });

  s.addText("Quelle: KMU-Tech-Report 2026", {
    x: 1, y: 6.8, w: W - 2, h: 0.4,
    fontFace: F.sans, fontSize: 12, color: C.creme,
    align: "center", margin: 0,
  });

  s.addNotes("Sprechzeit: 2 Min. Das ist keine Bali-Coachin-Behauptung. Das ist eine Studie aus diesem Jahr. 58% der Unternehmerinnen die KI einsetzen, sparen 20 Stunden pro Monat. 20 Stunden. Das sind 5 Stunden pro Woche, die du zurück hättest. Für deine Kinder, für dich, für die wichtigen Sachen — nicht für Posts schreiben.");
}

// ============================================================
// SLIDE 7 — Lücke im Markt
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.creme };

  addHeadline(s, "Was du sonst findest — und was fehlt.", C.dunkelblau, { y: 0.7, size: 32, align: "center" });

  // 3 Spalten: Vergleichs-Tabelle
  const cols = [
    { title: "KI fürs Business", x: 1, items: ["✓ Content erstellen", "— Mental Load weg", "— Wochenrhythmus", "— Verbindet beides"] },
    { title: "KI fürs Privat-Leben", x: 5.2, items: ["— Content erstellen", "✓ Mental Load weg", "— Wochenrhythmus", "— Verbindet beides"] },
    { title: "Mama-CEO", x: 9.4, items: ["✓ Content erstellen", "✓ Mental Load weg", "✓ Wochenrhythmus", "✓ Verbindet beides"], highlight: true },
  ];
  cols.forEach(c => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: c.x, y: 2.4, w: 3.8, h: 3.6,
      fill: { color: c.highlight ? C.petrol : C.white },
      line: { color: c.highlight ? C.petrol : "e5e5e5", width: 1 },
    });
    s.addText(c.title, {
      x: c.x, y: 2.5, w: 3.8, h: 0.6,
      fontFace: F.serif, fontSize: 20, color: c.highlight ? C.gelb : C.dunkelblau, bold: true,
      align: "center", margin: 0,
    });
    s.addText(c.items.map((t, i) => ({ text: t, options: { breakLine: i < c.items.length - 1 } })), {
      x: c.x + 0.3, y: 3.3, w: 3.4, h: 2.5,
      fontFace: F.sans, fontSize: 15, color: c.highlight ? C.creme : C.text,
      paraSpaceAfter: 8, margin: 0,
    });
  });

  s.addText("Mama-CEO verbindet beides — weil dein Mental Load auch beides ist.", {
    x: 1, y: 6.3, w: W - 2, h: 0.7,
    fontFace: F.serif, italic: true, fontSize: 22, color: C.orange,
    align: "center", margin: 0,
  });

  s.addNotes("Sprechzeit: 3 Min. Andere zeigen dir KI fürs Business. Andere zeigen dir KI fürs Privat-Leben. Mama-CEO ist das einzige Programm, das beides verbindet. Warum? Weil dein Mental Load auch beides ist. Du hast nicht 2 Köpfe — einen für Business und einen für Familie. Du hast EINEN Kopf, und der ist voll.");
}

// ============================================================
// SLIDE 8 — "Jetzt zeig ich's dir live" (Orange-Hintergrund)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.orange };

  addHeadline(s, "Jetzt zeig ich dir's live.", C.white, { y: 1.5, size: 60, align: "center" });

  s.addText("2 Bots. Selbst gebaut. Ohne Tech-Hintergrund.", {
    x: 1, y: 3.0, w: W - 2, h: 0.7,
    fontFace: F.sans, fontSize: 22, color: C.white, italic: true,
    align: "center", margin: 0,
  });

  s.addText([
    { text: "→ Bot 1: Mein Kochassistent (17 Min)", options: { breakLine: true } },
    { text: "→ Bot 2: Mein Brand-Voice-Bot (13 Min)", options: { breakLine: true } },
    { text: "→ Beide hab ich SELBST mit Claude Code gebaut.", options: {} },
  ], {
    x: 1, y: 4.1, w: W - 2, h: 2.2,
    fontFace: F.sans, fontSize: 22, color: C.white, bold: true,
    paraSpaceAfter: 10, align: "center", margin: 0,
  });

  s.addText("Bring Notizblock mit. Schreib mit.", {
    x: 1, y: 6.6, w: W - 2, h: 0.5,
    fontFace: F.serif, italic: true, fontSize: 18, color: C.white,
    align: "center", margin: 0,
  });

  s.addNotes("Sprechzeit: 1 Min. Jetzt kommt das Herzstück. Ich zeig dir zwei Bots, die ich täglich nutze. Beide hab ich selbst gebaut. Mit Claude Code. Ohne Tech-Vorwissen. Wenn ich das kann, kannst du das auch. Lass die Bildschirm-Aufnahme auf dich wirken — schreib mit, was dich interessiert.");
}

// ============================================================
// SLIDE 9 — LIVE-DEMO Platzhalter
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.cremeSoft };

  s.addText("LIVE-DEMO", {
    x: 1, y: 0.8, w: W - 2, h: 0.5,
    fontFace: F.sans, fontSize: 14, color: C.orange, bold: true,
    charSpacing: 8, align: "center", margin: 0,
  });

  s.addText("[Bildschirm-Aufnahme — 30 Min]", {
    x: 1, y: 1.8, w: W - 2, h: 1.2,
    fontFace: F.serif, fontSize: 40, color: C.dunkelblau, bold: true,
    align: "center", margin: 0,
  });

  // Demo-Plan
  s.addShape(pres.shapes.RECTANGLE, {
    x: 1.5, y: 3.5, w: 4.8, h: 3.2,
    fill: { color: C.white }, line: { color: C.petrol, width: 1 },
  });
  s.addText("Demo 1 · 17 Min", {
    x: 1.7, y: 3.7, w: 4.4, h: 0.4,
    fontFace: F.sans, fontSize: 13, color: C.orange, bold: true, charSpacing: 5, margin: 0,
  });
  s.addText("Kochassistent", {
    x: 1.7, y: 4.1, w: 4.4, h: 0.5,
    fontFace: F.serif, fontSize: 22, color: C.dunkelblau, bold: true, margin: 0,
  });
  s.addText("Claude Code · /mealplan · Wochenplan + Einkaufsliste in 90 Sek.", {
    x: 1.7, y: 4.7, w: 4.4, h: 2,
    fontFace: F.sans, fontSize: 14, color: C.text, margin: 0,
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 7, y: 3.5, w: 4.8, h: 3.2,
    fill: { color: C.white }, line: { color: C.petrol, width: 1 },
  });
  s.addText("Demo 2 · 13 Min", {
    x: 7.2, y: 3.7, w: 4.4, h: 0.4,
    fontFace: F.sans, fontSize: 13, color: C.orange, bold: true, charSpacing: 5, margin: 0,
  });
  s.addText("Brand-Voice-Bot", {
    x: 7.2, y: 4.1, w: 4.4, h: 0.5,
    fontFace: F.serif, fontSize: 22, color: C.dunkelblau, bold: true, margin: 0,
  });
  s.addText("3 Reels-Hooks zur Schuld-Spirale, in Patricia-Stimme, in 30 Sek.", {
    x: 7.2, y: 4.7, w: 4.4, h: 2,
    fontFace: F.sans, fontSize: 14, color: C.text, margin: 0,
  });

  s.addNotes("Während dieser 30 Min: Bildschirm-Sharing aktivieren. Demo 1 = /mealplan, dann Demo 2 = Brand-Voice-Bot. Slide bleibt als Backup falls Bildschirm-Share crasht.");
}

// ============================================================
// SLIDE 10 — Recap nach Demo (Petrol)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.petrolDark };

  addHeadline(s, "Was du gerade gesehen hast:", C.creme, { y: 0.9, size: 36, align: "center" });

  s.addText([
    { text: "✓ Bot 1: Familienwoche geplant in 90 Sek.", options: { breakLine: true } },
    { text: "✓ Bot 2: 3 Reels-Hooks in deiner Stimme in 30 Sek.", options: { breakLine: true } },
    { text: "✓ BEIDE SELBST GEBAUT. Ohne Tech-Hintergrund.", options: {} },
  ], {
    x: 1, y: 2.4, w: W - 2, h: 2.0,
    fontFace: F.sans, fontSize: 22, color: C.gelb, bold: true,
    paraSpaceAfter: 8, align: "center", margin: 0,
  });

  s.addText(`„Wenn ich das kann, kannst du das auch."`, {
    x: 1, y: 5.0, w: W - 2, h: 1.0,
    fontFace: F.serif, italic: true, fontSize: 38, color: C.orange, bold: true,
    align: "center", margin: 0,
  });

  s.addText("Im Programm zeig ich dir Schritt für Schritt wie.", {
    x: 1, y: 6.4, w: W - 2, h: 0.5,
    fontFace: F.sans, fontSize: 16, color: C.creme,
    align: "center", margin: 0,
  });

  s.addNotes("Sprechzeit: 1 Min. Das hast du gerade live gesehen. Familien-Bot. Brand-Voice-Bot. In Minuten. SELBST GEBAUT. Wenn ich das kann mit 4 Kindern und ohne IT-Hintergrund — du kannst das auch. Genau das zeig ich dir in den 8 Wochen Mama-CEO.");
}

// ============================================================
// SLIDE 11 — 3 Bausteine
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.creme };

  addHeadline(s, "3 Bausteine. Mehr nicht.", C.dunkelblau, { y: 0.7, size: 42, align: "center" });

  const blocks = [
    { num: "01", title: "Wochenrhythmus", desc: "Power-Zeiten + 4 Rollen + Abend-Wand", x: 0.6 },
    { num: "02", title: "Strukturen", desc: "Notion + Hütchenmethode + Workflows", x: 4.7 },
    { num: "03", title: "Tools mit KI", desc: "Bots, die für dich mitarbeiten", x: 8.8 },
  ];
  blocks.forEach(b => {
    // Orange Kreis mit Nummer
    s.addShape(pres.shapes.OVAL, {
      x: b.x + 1.5, y: 2.0, w: 1.4, h: 1.4,
      fill: { color: C.orange }, line: { color: C.orange },
    });
    s.addText(b.num, {
      x: b.x + 1.5, y: 2.0, w: 1.4, h: 1.4,
      fontFace: F.serif, fontSize: 36, color: C.white, bold: true,
      align: "center", valign: "middle", margin: 0,
    });

    s.addText(b.title, {
      x: b.x, y: 3.8, w: 4.4, h: 0.7,
      fontFace: F.serif, fontSize: 26, color: C.dunkelblau, bold: true,
      align: "center", margin: 0,
    });
    s.addText(b.desc, {
      x: b.x, y: 4.6, w: 4.4, h: 1.5,
      fontFace: F.sans, fontSize: 16, color: C.text,
      align: "center", margin: 0,
    });
  });

  s.addText("Genau das baust du in 8 Wochen Mama-CEO.", {
    x: 1, y: 6.5, w: W - 2, h: 0.5,
    fontFace: F.serif, italic: true, fontSize: 20, color: C.petrol,
    align: "center", margin: 0,
  });

  s.addNotes("Sprechzeit: 2 Min. Du brauchst nicht 100 Tools. Du brauchst 3 Bausteine. Erstens deinen Wochenrhythmus, damit du weisst wann du Zeit hast. Zweitens deine Strukturen, damit dir nichts mehr durch die Lappen geht. Drittens deine Tools mit KI, damit du nicht mehr alles selbst machst. Das ist Mama-CEO.");
}

// ============================================================
// SLIDE 12 — Programm-Übersicht
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };

  addHeadline(s, "Mama-CEO — 8 Wochen Live-Programm", C.dunkelblau, { y: 0.7, size: 32, align: "center" });

  // Timeline mit 5 Säulen
  const timeline = [
    { label: "Säule 1+2", sub: "Energie + Mindset (parallel)", x: 0.8, w: 2.8 },
    { label: "Säule 3", sub: "System + Orga", x: 3.8, w: 2.5 },
    { label: "Säule 4", sub: "KI-Mitarbeiter", x: 6.5, w: 2.5 },
    { label: "Säule 5", sub: "Skalieren", x: 9.2, w: 2.5 },
  ];
  // Linie
  s.addShape(pres.shapes.LINE, {
    x: 0.8, y: 2.8, w: 10.9, h: 0,
    line: { color: C.petrol, width: 3 },
  });
  timeline.forEach((t, i) => {
    s.addText(`W${i*2+1}–${(i+1)*2}`, {
      x: t.x, y: 2.3, w: t.w, h: 0.4,
      fontFace: F.sans, fontSize: 13, color: C.orange, bold: true, charSpacing: 5,
      align: "center", margin: 0,
    });
    // Punkt
    s.addShape(pres.shapes.OVAL, {
      x: t.x + t.w/2 - 0.15, y: 2.65, w: 0.3, h: 0.3, fill: { color: C.orange }, line: { color: C.orange },
    });
    s.addText(t.label, {
      x: t.x, y: 3.2, w: t.w, h: 0.5,
      fontFace: F.serif, fontSize: 22, color: C.dunkelblau, bold: true,
      align: "center", margin: 0,
    });
    s.addText(t.sub, {
      x: t.x, y: 3.7, w: t.w, h: 0.7,
      fontFace: F.sans, fontSize: 13, color: C.muted,
      align: "center", margin: 0,
    });
  });

  // 4 Hauptzutaten unten
  const features = [
    "22 Lektionen (8–15 Min)",
    "4 Live-Termine (alle 2 Wochen)",
    "Telegram-Gruppe (8 Wo + danach offen)",
    "3 Boni: Cockpit + Familien-Bot + Notion",
  ];
  features.forEach((f, i) => {
    s.addText(`✓ ${f}`, {
      x: 1 + (i % 2) * 5.7, y: 5.3 + Math.floor(i / 2) * 0.7, w: 5.5, h: 0.5,
      fontFace: F.sans, fontSize: 16, color: C.text,
      align: "left", margin: 0,
    });
  });

  s.addNotes("Sprechzeit: 2 Min. Mama-CEO sind 8 Wochen. 5 Säulen. 22 kurze Lektionen — keine die länger ist als 15 Minuten, weil du keine Zeit für 60-Minuten-Filme hast. 4 Live-Termine direkt mit mir. Telegram-Gruppe. 3 echte Boni — keine zusammengewürfelten Standard-Templates. Lass mich dir die 5 Säulen kurz zeigen.");
}

// ============================================================
// SLIDE 13-17 — Die 5 Säulen
// ============================================================
const saulen = [
  {
    num: "01", title: "Du erschaffst dir die Zeit", weeks: "WOCHEN 1–2",
    bg: C.creme,
    bullets: [
      "Productivity für Mamas (Pomodoro & Co. — was greift)",
      "Deine Realität: wann hast du wirklich Zeit?",
      "Die 3 Säulen (Plattform · Produkt · Verkauf)",
      "Wochenrhythmus mit 4 Rollen aufbauen",
    ],
    sprung: `„Ich kenne meine Realität, weiss was zählt, habe meinen Rhythmus."`,
    notes: "Säule 1: Du verstehst zuerst, wann du wirklich Zeit hast. Power-Zeiten finden, 4 Rollen verteilen, dein Wochenrhythmus steht. Plus: was bringt dein Business wirklich vorwärts? 3 Säulen — Plattform, Produkt, Verkauf. Alle drei müssen laufen.",
  },
  {
    num: "02", title: "Du brichst aus dem Hamsterrad aus", weeks: "WOCHEN 1–2 (parallel)",
    bg: C.white,
    bullets: [
      "Hamsterrad-Diagnose",
      "Hütchenmethode (Brain Dump + Rollen sortieren)",
      "Was kann weg — bewusst loslassen",
      "5 Mama-CEO-Blockaden auflösen",
      "Dein Sonntag-Reset (15 Min wöchentlich)",
    ],
    sprung: `„Ich tue, was dran ist. Ohne Schuld."`,
    notes: "Säule 2 läuft parallel zu Säule 1. Weil eine Mama mit 'Ich-bin-nicht-genug'-Glaubenssatz keinen Wochenrhythmus baut. Du brauchst BEIDES gleichzeitig. Brain Dump. Hütchen sortieren. Was kann weg. Und ein Sonntag-Reset, der dich aus dem Hamsterrad holt.",
  },
  {
    num: "03", title: "Du baust die Struktur", weeks: "WOCHEN 3–4",
    bg: C.creme,
    bullets: [
      "Aufgaben auf Tage/Wochen verteilen",
      "Die 5 Kern-Workflows dokumentieren",
      "Notion Business Brain aufsetzen (Live-Demo!)",
      "Notfall-Modus für Kinder-Kranktage",
    ],
    sprung: `„Ich habe Workflows, die immer gleich laufen — und einen 50%-Plan."`,
    notes: "Säule 3: Aus dem Brain Dump entsteht ein System. Aufgaben auf Tage und Wochen verteilen — nie zu viel an einem Tag. Notion als dein Business Brain. Ich zeig dir mein Setup. Plus: was läuft trotzdem, wenn ein Kind krank ist? 50%-Plan.",
  },
  {
    num: "04", title: "Du delegierst den Adminkram", weeks: "WOCHEN 5–6",
    bg: C.white,
    bullets: [
      "KI-Mythos vs. Realität — KI nur so gut wie dein Input",
      "Cockpit-Bot bauen (Live-Demo)",
      "Haushalts-Helfer bauen (Live-Demo Kochassistent)",
      "Welche Bots brauchst DU? (Bot-Audit)",
      "KI-Wochenplan: Mensch vs. KI",
    ],
    sprung: `„KI-Mitarbeiter nehmen mir den Adminkram ab — Business UND Haushalt."`,
    notes: "Säule 4: Hier wird's konkret. KI-Mitarbeiter bauen. Ich zeig dir mein Cockpit-Bot Setup. Mein Kochassistent. Du baust den, den DU brauchst — kein Schema F. Plus die Entscheidungs-Logik: wann tust du, wann delegierst du.",
  },
  {
    num: "05", title: "Business skalieren", weeks: "WOCHEN 7–8",
    bg: C.creme,
    bullets: [
      "Mama-CEO-Matrix (ich · KI · System · raus)",
      "Was DEINS bleibt (1:1 · Projekte · Events)",
      "90-Tage-Wachstums-Plan",
      "Was du JETZT NICHT machst (→ Premium-Bundle)",
    ],
    sprung: `„Ich weiss, was DEINS bleibt, was die KI macht, was raus muss."`,
    notes: "Säule 5: jetzt skalierst du klug. Mama-CEO-Matrix: was bleibt deins, was geht zur KI, was raus muss. 90-Tage-Plan. Und ganz wichtig: was JETZT noch NICHT dran ist — Insta-Verkauf-Tiefe, eigene Produkte erstellen, Team aufbauen. Das kommt im nächsten Programm.",
  },
];

saulen.forEach(saule => {
  const s = pres.addSlide();
  s.background = { color: saule.bg };

  // Mega-Nummer links
  s.addText(saule.num, {
    x: 0.6, y: 1.0, w: 2.5, h: 4.5,
    fontFace: F.serif, fontSize: 240, color: C.orange, bold: true,
    align: "center", valign: "top", margin: 0,
  });

  // Eyebrow rechts
  s.addText(`SÄULE ${saule.num} · ${saule.weeks}`, {
    x: 3.5, y: 1.2, w: W - 4.5, h: 0.5,
    fontFace: F.sans, fontSize: 14, color: C.orange, bold: true,
    charSpacing: 6, align: "left", margin: 0,
  });

  // Titel rechts
  s.addText(saule.title, {
    x: 3.5, y: 1.9, w: W - 4.5, h: 1.4,
    fontFace: F.serif, fontSize: 36, color: C.dunkelblau, bold: true,
    align: "left", margin: 0,
  });

  // Bullets rechts
  s.addText(saule.bullets.map((b, i) => ({
    text: b,
    options: { breakLine: i < saule.bullets.length - 1 },
  })), {
    x: 3.5, y: 3.4, w: W - 4.5, h: 2.6,
    fontFace: F.sans, fontSize: 16, color: C.text,
    bullet: { code: "2192" }, // → arrow
    paraSpaceAfter: 8, margin: 0,
  });

  // Sprung-Zitat unten
  s.addShape(pres.shapes.RECTANGLE, {
    x: 3.5, y: 6.2, w: 0.08, h: 0.8, fill: { color: C.petrol }, line: { color: C.petrol },
  });
  s.addText(saule.sprung, {
    x: 3.7, y: 6.2, w: W - 4.7, h: 0.8,
    fontFace: F.serif, italic: true, fontSize: 16, color: C.petrol,
    valign: "middle", margin: 0,
  });

  s.addNotes(`Sprechzeit: 1.5 Min. ${saule.notes}`);
});

// ============================================================
// SLIDE 18 — Bonus-Pack (Petrol-Hintergrund)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.petrolDark };

  s.addText("3 BONI — ALLE PATRICIA-EIGEN.", {
    x: 1, y: 0.7, w: W - 2, h: 0.5,
    fontFace: F.sans, fontSize: 16, color: C.gelb, bold: true,
    charSpacing: 6, align: "center", margin: 0,
  });

  addHeadline(s, "Keine zusammengewürfelten Standard-Templates.", C.creme, { y: 1.4, size: 24, align: "center" });

  const boni = [
    { icon: "🌅", title: "Cockpit-Bot", desc: "System-Prompt + Anleitung. Strategische Planung + Reflexion + Tagesbriefing.", x: 0.6 },
    { icon: "🏠", title: "Familien-Bot", desc: "System-Prompt für deinen Mental-Load-Speicher. Termine, Geschenke, Reisen.", x: 4.7 },
    { icon: "📂", title: "Notion-Master-Template", desc: "Abgespeckte Kopie meines echten Workspaces. 4 DBs + 5 Workflows + 90-Tage-Tracker.", x: 8.8 },
  ];
  boni.forEach((b, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: b.x, y: 2.6, w: 0.08, h: 3.4, fill: { color: C.orange }, line: { color: C.orange },
    });
    s.addText(b.icon, {
      x: b.x + 0.3, y: 2.6, w: 4, h: 0.8,
      fontSize: 36, align: "left", margin: 0,
    });
    s.addText(`BONUS 0${i+1}`, {
      x: b.x + 0.3, y: 3.5, w: 4, h: 0.4,
      fontFace: F.sans, fontSize: 12, color: C.gelb, bold: true,
      charSpacing: 6, margin: 0,
    });
    s.addText(b.title, {
      x: b.x + 0.3, y: 3.9, w: 4, h: 0.7,
      fontFace: F.serif, fontSize: 22, color: C.creme, bold: true,
      margin: 0,
    });
    s.addText(b.desc, {
      x: b.x + 0.3, y: 4.6, w: 4, h: 1.5,
      fontFace: F.sans, fontSize: 14, color: C.creme,
      margin: 0,
    });
  });

  s.addText("Plus Claude-Code-Einrichtungs-Anleitung als Material.", {
    x: 1, y: 6.6, w: W - 2, h: 0.4,
    fontFace: F.sans, italic: true, fontSize: 14, color: C.gelb,
    align: "center", margin: 0,
  });

  s.addNotes("Sprechzeit: 2 Min. Drei Boni. Alle drei sind meine echten Tools, die ich täglich nutze. Kein zusammengewürfelter Standard-Mist. Mein Cockpit-Bot, der mir morgens den Tag bringt. Familien-Bot für Mental-Load. Und mein Notion-Workspace als duplizierbares Template — du fängst nicht bei Null an.");
}

// ============================================================
// SLIDE 19 — PRICING (3-Spalten)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };

  s.addText("ERSTE RUNDE · 15 PLÄTZE", {
    x: 1, y: 0.7, w: W - 2, h: 0.5,
    fontFace: F.sans, fontSize: 14, color: C.petrol, bold: true,
    charSpacing: 6, align: "center", margin: 0,
  });

  addHeadline(s, "Komm jetzt rein — solange's noch 333 sind.", C.dunkelblau, { y: 1.3, size: 28, align: "center" });

  const prices = [
    { label: "🔥 FRÜHBUCHER · 72H", amount: "249", note: "Heute 11:00 → Sa 23.5. 23:59", x: 0.6, featured: false },
    { label: "FINAL · ERSTE RUNDE", amount: "333", note: "Ab So 24.5. → So 31.5. 23:59", x: 4.7, featured: true },
    { label: "RUNDE 2 · HERBST", amount: "444", note: "Boni werden ausgebaut", x: 8.8, featured: false },
  ];
  prices.forEach(p => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: p.x, y: 2.6, w: 4, h: 3.6,
      fill: { color: C.white },
      line: { color: p.featured ? C.orange : "e5e5e5", width: p.featured ? 3 : 1 },
    });
    if (p.featured) {
      // BESTE WAHL Badge
      s.addShape(pres.shapes.RECTANGLE, {
        x: p.x + 1.2, y: 2.35, w: 1.6, h: 0.5,
        fill: { color: C.orange }, line: { color: C.orange },
      });
      s.addText("BESTE WAHL", {
        x: p.x + 1.2, y: 2.35, w: 1.6, h: 0.5,
        fontFace: F.sans, fontSize: 10, color: C.white, bold: true,
        charSpacing: 8, align: "center", valign: "middle", margin: 0,
      });
    }
    s.addText(p.label, {
      x: p.x, y: 3.0, w: 4, h: 0.4,
      fontFace: F.sans, fontSize: 12, color: C.petrol, bold: true,
      charSpacing: 5, align: "center", margin: 0,
    });
    s.addText(`${p.amount} CHF`, {
      x: p.x, y: 3.6, w: 4, h: 1.4,
      fontFace: F.serif, fontSize: 56, color: C.dunkelblau, bold: true,
      align: "center", margin: 0,
    });
    s.addText(p.note, {
      x: p.x, y: 5.3, w: 4, h: 0.7,
      fontFace: F.sans, fontSize: 13, color: C.muted,
      align: "center", margin: 0,
    });
  });

  s.addText("Programm-Start: Mo 1. Juni 2026 · Cart schliesst endgültig So 31.5.", {
    x: 1, y: 6.7, w: W - 2, h: 0.4,
    fontFace: F.sans, fontSize: 13, color: C.muted,
    align: "center", margin: 0,
  });

  s.addNotes("Sprechzeit: 3 Min. Pricing-Logik. Heute Earlybird 249. Drei Tage. Bis Samstag 23 Uhr 59. Danach 333 bis Sonntag 31. Mai. Beim 2. Mal — Herbst 2026 — sind's 444. Warum? Weil die Boni dann ausgebaut sind und ich beim 2. Mal weiss, wo's bei euch hakt. Wer JETZT einsteigt, zahlt am wenigsten und hat mich am nähesten dran in den 4 Live-Terminen.");
}

// ============================================================
// SLIDE 20 — Antikunden (Ja/Nein)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.creme };

  addHeadline(s, "Bevor du klickst:", C.dunkelblau, { y: 0.7, size: 36, align: "center" });

  // Linke Spalte JA
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.8, y: 2.0, w: 5.7, h: 4.7,
    fill: { color: C.white }, line: { color: C.petrol, width: 2 },
  });
  s.addText("✓ JA, wenn du …", {
    x: 1, y: 2.3, w: 5.4, h: 0.6,
    fontFace: F.serif, fontSize: 26, color: C.petrol, bold: true, margin: 0,
  });
  s.addText([
    { text: "seit min. 6 Monaten im Network bist", options: { breakLine: true } },
    { text: "dein Thema schon grob weisst", options: { breakLine: true } },
    { text: "bereit bist, in 8 Wochen aktiv mitzubauen", options: { breakLine: true } },
    { text: "Notion + KI einsetzen willst (egal ob du heute weisst wie)", options: {} },
  ], {
    x: 1, y: 3.2, w: 5.4, h: 3.3,
    fontFace: F.sans, fontSize: 15, color: C.text,
    bullet: { code: "2192" }, paraSpaceAfter: 12, margin: 0,
  });

  // Rechte Spalte NEIN
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.8, y: 2.0, w: 5.7, h: 4.7,
    fill: { color: C.white }, line: { color: C.orange, width: 2 },
  });
  s.addText("✗ NEIN, wenn du …", {
    x: 7, y: 2.3, w: 5.4, h: 0.6,
    fontFace: F.serif, fontSize: 26, color: C.orange, bold: true, margin: 0,
  });
  s.addText([
    { text: "noch nicht weisst, was du anbietest (→ Insta-Kundenmaschine zuerst)", options: { breakLine: true } },
    { text: "in 6 Monaten 6-stellig willst", options: { breakLine: true } },
    { text: "erwartest, dass ich's für dich baue", options: { breakLine: true } },
    { text: "seit Jahren Kurse buchst und nichts umsetzt", options: {} },
  ], {
    x: 7, y: 3.2, w: 5.4, h: 3.3,
    fontFace: F.sans, fontSize: 15, color: C.text,
    bullet: { code: "2192" }, paraSpaceAfter: 12, margin: 0,
  });

  s.addNotes("Sprechzeit: 2 Min. Eine kurze Sortier-Übung. JA wenn du seit mindestens 6 Monaten im Network bist und schon Kundinnen hattest. Wenn du dein Thema schon grob weisst. NEIN wenn du noch gar nicht weisst was du anbietest — dann geh erst in die Instagram-Kundenmaschine. NEIN wenn du 6-stellig in 6 Monaten willst — das versprech ich nicht. Und NEIN wenn du seit Jahren Kurse buchst und nichts umsetzt. Mama-CEO ist für Frauen, die TUN.");
}

// ============================================================
// SLIDE 21 — CTA Mega
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.orange };

  addHeadline(s, "Sichere dir deinen Platz.", C.white, { y: 1.0, size: 60, align: "center" });

  s.addText([
    { text: "Heute, 11:00 → Sa 23.5. 23:59", options: { breakLine: true } },
    { text: "Earlybird CHF 249", options: {} },
  ], {
    x: 1, y: 2.6, w: W - 2, h: 1.5,
    fontFace: F.sans, fontSize: 24, color: C.white, bold: true,
    paraSpaceAfter: 8, align: "center", margin: 0,
  });

  // Mega CTA Button
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: W/2 - 4.5, y: 4.3, w: 9, h: 1.4,
    fill: { color: C.white }, line: { color: C.white },
    rectRadius: 0.7,
  });
  s.addText("🔗 mumlifebalance.ch/mama-ceo", {
    x: W/2 - 4.5, y: 4.3, w: 9, h: 1.4,
    fontFace: F.sans, fontSize: 28, color: C.dunkelblau, bold: true,
    align: "center", valign: "middle", margin: 0,
  });

  s.addText("Cart-Link im Chat ab Min 60. Nur 15 Plätze.", {
    x: 1, y: 6.4, w: W - 2, h: 0.5,
    fontFace: F.serif, italic: true, fontSize: 18, color: C.white,
    align: "center", margin: 0,
  });

  s.addNotes("Sprechzeit: 1 Min. Cart ist offen. Earlybird läuft 72 Stunden. 15 Plätze. Wer jetzt klickt, zahlt 249 statt 333. Den Link siehst du im Chat. Lass uns kurz Fragen sammeln — schreibt im Chat, ich beantworte alle.");
}

// ============================================================
// SLIDE 22 — Q&A + Closing
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.dunkelblau };

  addHeadline(s, "Deine Fragen.", C.creme, { y: 1.2, size: 56, align: "center" });

  s.addText("Schreib im Chat — ich beantworte alle. 20 Min Zeit.", {
    x: 1, y: 2.6, w: W - 2, h: 0.7,
    fontFace: F.sans, fontSize: 22, color: C.creme,
    align: "center", margin: 0,
  });

  // Linie
  s.addShape(pres.shapes.LINE, {
    x: W/2 - 1, y: 3.8, w: 2, h: 0,
    line: { color: C.orange, width: 2 },
  });

  s.addText(`„Funktionieren war gestern."`, {
    x: 1, y: 4.5, w: W - 2, h: 1.5,
    fontFace: F.serif, italic: true, fontSize: 44, color: C.orange, bold: true,
    align: "center", margin: 0,
  });

  s.addText("— Patricia", {
    x: 1, y: 6.4, w: W - 2, h: 0.4,
    fontFace: F.serif, italic: true, fontSize: 18, color: C.creme,
    align: "center", margin: 0,
  });

  s.addNotes("Während Q&A läuft Slide 22 als Hintergrund. Patricia geht auf alle Fragen ein. 5 Backup-Q&A vorbereitet (siehe 06-webinar-pitch-slides.md). Closing: Danke, dass du dabei warst. Wer im Earlybird kauft — bis Samstag 23 Uhr 59 — bekommt das Replay permanent UND 15 Minuten 1:1-Audio mit mir. Cart-Link ist im Chat. Bis Mi 1. Juni dann live im Programm. Mach das Beste aus deinen 18 Stunden die Woche. Funktionieren war gestern.");
}

// === WRITE FILE ===
const outPath = path.resolve(__dirname, "../../outputs/produkte/mama-ceo/06-webinar-pitch-slides.pptx");
pres.writeFile({ fileName: outPath }).then(() => {
  console.log(`✅ PPTX geschrieben: ${outPath}`);
});
