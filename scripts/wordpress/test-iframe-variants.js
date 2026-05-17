import { readFile } from 'node:fs/promises';
const auth = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');

let html = await readFile('C:/Users/pnulm/Desktop/Mein Business/.claude/worktrees/upbeat-yalow-d35cfb/outputs/link-in-bio/index.html', 'utf-8');
html = html.replace(/src="patricia\.jpg"/g, 'src="https://mumlifebalance.ch/wp-content/uploads/2026/05/patricia-scaled.jpg"');

const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/);
const styleBlock = `<style>${styleMatch[1]}</style>`;

// Body so wie er ist (Vimeo schon drin im aktuellen HTML, minimal version)
const body = bodyMatch[1];

const tests = [
  // T1: Vimeo iframe komplett raus
  { name: 'NO iframe', body: body.replace(/<iframe[\s\S]*?<\/iframe>/g, '<p>video here</p>') },
  // T2: iframe ganz simpel ohne hash
  { name: 'iframe no-hash', body: body.replace(/<iframe[\s\S]*?<\/iframe>/g, '<iframe src="https://player.vimeo.com/video/1191904968"></iframe>') },
  // T3: iframe mit hash, keine weiteren attrs
  { name: 'iframe with hash', body: body.replace(/<iframe[\s\S]*?<\/iframe>/g, '<iframe src="https://player.vimeo.com/video/1191904968?h=f04e9542a8"></iframe>') },
  // T4: iframe mit hash + style
  { name: 'iframe hash+style', body: body.replace(/<iframe[\s\S]*?<\/iframe>/g, '<iframe src="https://player.vimeo.com/video/1191904968?h=f04e9542a8" style="width:100%;height:300px;"></iframe>') },
  // T5: iframe mit hash + frameborder
  { name: 'iframe hash+frameborder', body: body.replace(/<iframe[\s\S]*?<\/iframe>/g, '<iframe src="https://player.vimeo.com/video/1191904968?h=f04e9542a8" frameborder="0"></iframe>') },
];

for (const t of tests) {
  const content = `<!-- wp:html -->\n${styleBlock}\n${t.body}\n<!-- /wp:html -->`;
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
