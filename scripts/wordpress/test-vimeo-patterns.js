import { readFile } from 'node:fs/promises';
const auth = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');

let html = await readFile('C:/Users/pnulm/Desktop/Mein Business/.claude/worktrees/upbeat-yalow-d35cfb/outputs/link-in-bio/index.html', 'utf-8');
html = html.replace(/src="patricia\.jpg"/g, 'src="https://mumlifebalance.ch/wp-content/uploads/2026/05/patricia-scaled.jpg"');
html = html.replace(/<!-- VIMEO[\s\S]*?<script src="https:\/\/player\.vimeo\.com\/api\/player\.js"><\/script>/m, '<!-- VIMEO_HERE -->');
const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/);
const [before, after] = bodyMatch[1].split('<!-- VIMEO_HERE -->');
const styleBlock = `<style>${styleMatch[1]}</style>`;

const tests = [
  // Variante A: Vimeo Plain URL  als Text
  { name: 'A: Plain Vimeo URL', vimeo: `<p>https://vimeo.com/1191904968/f04e9542a8</p>` },
  // Variante B: Nur URL ohne Hash (privacy code raus)
  { name: 'B: Vimeo URL no hash', vimeo: `<p>https://vimeo.com/1191904968</p>` },
  // Variante C: WP-Block embed-vimeo wrapper aber leer (Pattern test)
  { name: 'C: WP block-vimeo class', vimeo: `<div class="wp-block-embed-vimeo"></div>` },
  // Variante D: iframe player.vimeo.com 
  { name: 'D: player.vimeo iframe', vimeo: `<iframe src="https://player.vimeo.com/video/1191904968"></iframe>` },
];

for (const t of tests) {
  const content = `<!-- wp:html -->\n${styleBlock}\n${before}${t.vimeo}${after}\n<!-- /wp:html -->`;
  const res = await fetch(`${process.env.WP_URL}/wp-json/wp/v2/pages`, {
    method: 'POST',
    headers: { 'Authorization': auth, 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: `T: ${t.name}`, slug: `t-${Date.now()}-${Math.random().toString(36).slice(2,5)}`, content, status: 'draft' }),
  });
  console.log(`${t.name} (${content.length}c): ${res.status === 200 || res.status === 201 ? '✅' : '❌ ' + res.status}`);
  if (res.status === 200 || res.status === 201) {
    const d = await res.json();
    await fetch(`${process.env.WP_URL}/wp-json/wp/v2/pages/${d.id}?force=true`, { method: 'DELETE', headers: { 'Authorization': auth } });
  }
}
