const fs = require('fs');

const SRC = '/home/user/mumlifebalance-workspace/outputs/produkte/claude-als-networkerin/03-business-brain-setup-paket.md';
const OUT_HTML = '/tmp/claude-0/-home-user-mumlifebalance-workspace/f0de49ee-3b32-5bb6-a1b0-af7e1ff508f4/scratchpad/setup-paket.html';

let md = fs.readFileSync(SRC, 'utf8');
// strip frontmatter
md = md.replace(/^---[\s\S]*?---\s*/, '');
// strip trailing "Verwandte Notizen" section (internal)
md = md.replace(/\n---\s*\n+##\s*🔗[\s\S]*$/, '\n');

function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function inline(s) {
  s = esc(s);
  s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  // curly-ify not needed
  return s;
}

const lines = md.split('\n');
let html = '';
let i = 0;
let inList = false;
function closeList() { if (inList) { html += '</ul>\n'; inList = false; } }

while (i < lines.length) {
  let line = lines[i];

  // fenced code block -> prompt box
  if (line.trim().startsWith('```')) {
    closeList();
    i++;
    let buf = [];
    while (i < lines.length && !lines[i].trim().startsWith('```')) {
      buf.push(lines[i]);
      i++;
    }
    i++; // skip closing fence
    html += '<div class="prompt"><div class="prompt__label">📋 Zum Kopieren</div><pre>' +
            esc(buf.join('\n')) + '</pre></div>\n';
    continue;
  }

  // horizontal rule -> section divider
  if (/^---\s*$/.test(line)) {
    closeList();
    html += '<hr class="divider"/>\n';
    i++;
    continue;
  }

  // headings
  let m;
  if ((m = line.match(/^#\s+(.*)$/))) { closeList(); i++; continue; } // titel steht schon auf dem cover
  if ((m = line.match(/^##\s+(.*)$/))) { closeList(); html += `<h2>${inline(m[1])}</h2>\n`; i++; continue; }
  if ((m = line.match(/^###\s+(.*)$/))) { closeList(); html += `<h3>${inline(m[1])}</h3>\n`; i++; continue; }

  // list items
  if ((m = line.match(/^[-*]\s+(.*)$/))) {
    if (!inList) { html += '<ul>\n'; inList = true; }
    html += `<li>${inline(m[1])}</li>\n`;
    i++;
    continue;
  }

  // blank
  if (line.trim() === '') { closeList(); i++; continue; }

  // paragraph (gather until blank)
  closeList();
  let para = [line];
  i++;
  while (i < lines.length && lines[i].trim() !== '' &&
         !/^[-*#]/.test(lines[i]) && !lines[i].trim().startsWith('```') && !/^---\s*$/.test(lines[i])) {
    para.push(lines[i]); i++;
  }
  html += `<p>${inline(para.join(' '))}</p>\n`;
}
closeList();

const page = `<!DOCTYPE html>
<html lang="de"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet"/>
<style>
  :root{
    --petrol:#12828c; --blau:#29556d; --creme:#f1ecdd; --orange:#dc822e;
    --ink:#2b2b2b; --muted:#6b6b6b;
  }
  @page { size: A4; margin: 20mm 18mm 18mm 18mm; }
  * { box-sizing: border-box; }
  body{ font-family:'Source Sans 3',-apple-system,'Segoe UI',sans-serif; color:var(--ink);
        font-size:11.5pt; line-height:1.6; margin:0; }
  h1,h2,h3{ font-family:'Philosopher','Georgia',serif; color:var(--blau); line-height:1.25; }
  h1{ font-size:24pt; color:var(--petrol); margin:0 0 4pt; }
  h2{ font-size:16pt; margin:22pt 0 6pt; padding-bottom:4pt; border-bottom:2px solid var(--creme); page-break-after:avoid; }
  h3{ font-size:12.5pt; color:var(--petrol); margin:14pt 0 2pt; page-break-after:avoid; }
  p{ margin:6pt 0; }
  strong{ color:var(--blau); font-weight:700; }
  code{ font-family:'DejaVu Sans Mono',monospace; background:var(--creme); padding:1px 4px; border-radius:3px; font-size:10pt; }
  ul{ margin:6pt 0 6pt 0; padding-left:18pt; }
  li{ margin:3pt 0; }
  hr.divider{ border:none; border-top:1px solid #ddd6c4; margin:16pt 0; }
  .prompt{ background:#fbf9f2; border:1px solid #e5ddc7; border-left:4px solid var(--petrol);
           border-radius:6px; margin:10pt 0; page-break-inside:avoid; overflow:hidden; }
  .prompt__label{ background:var(--petrol); color:#fff; font-size:8.5pt; font-weight:700;
                  letter-spacing:.5px; text-transform:uppercase; padding:3pt 10pt; }
  .prompt pre{ margin:0; padding:10pt 12pt; white-space:pre-wrap; word-break:break-word;
               font-family:'DejaVu Sans Mono',monospace; font-size:9.3pt; line-height:1.5; color:#33332e; }
  /* Cover */
  .cover{ page-break-after:always; height:calc(100vh - 40mm); display:flex; flex-direction:column;
          justify-content:center; }
  .cover__kicker{ font-size:11pt; letter-spacing:2px; text-transform:uppercase; color:var(--orange); font-weight:700; }
  .cover__title{ font-family:'Philosopher','Georgia',serif; font-size:34pt; color:var(--petrol);
                 line-height:1.15; margin:8pt 0 12pt; }
  .cover__sub{ font-size:13pt; color:var(--muted); max-width:120mm; }
  .cover__brand{ margin-top:26pt; font-family:'Philosopher',serif; font-size:13pt; color:var(--blau); }
  .cover__rule{ width:60mm; height:4px; background:var(--orange); border-radius:2px; margin:0 0 18pt; }
  .lead{ font-size:12pt; color:#3a3a3a; }
</style></head><body>
<div class="cover">
  <div class="cover__kicker">Dein Starter-Kit</div>
  <div class="cover__rule"></div>
  <div class="cover__title">Dein Claude-<br/>Business-Brain</div>
  <div class="cover__sub">Setup, Skill-Datei &amp; Prompts — damit Claude dein Kurs-Wissen kennt und dich. Schritt für Schritt zum Assistenten, der in deiner Sprache denkt.</div>
  <div class="cover__brand">Patricia Ulmann · Mum Life Balance</div>
</div>
${html}
</body></html>`;

fs.writeFileSync(OUT_HTML, page);
console.log('HTML geschrieben:', OUT_HTML, page.length, 'Zeichen');
