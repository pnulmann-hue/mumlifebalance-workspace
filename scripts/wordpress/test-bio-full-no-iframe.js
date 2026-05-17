import { readFile } from 'node:fs/promises';
const auth = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');

let html = await readFile('C:/Users/pnulm/Desktop/Mein Business/.claude/worktrees/upbeat-yalow-d35cfb/outputs/link-in-bio/index.html', 'utf-8');
html = html.replace(/src="patricia\.jpg"/g, 'src="https://mumlifebalance.ch/wp-content/uploads/2026/05/patricia-scaled.jpg"');

// Iframe komplett raus
html = html.replace(/<!-- VIMEO-EMBED[\s\S]*?<script src="https:\/\/player\.vimeo\.com\/api\/player\.js"><\/script>/m, '<p style="text-align:center;color:#999;padding:20px;">Video kommt hier</p>');

const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/);

const wpContent = `<!-- wp:html -->\n<style>${styleMatch[1]}</style>\n${bodyMatch[1]}\n<!-- /wp:html -->`;

console.log(`Payload: ${wpContent.length} Zeichen`);

const res = await fetch(`${process.env.WP_URL}/wp-json/wp/v2/pages`, {
  method: 'POST',
  headers: { 'Authorization': auth, 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'Bio V3 (no iframe)', slug: `bio-test-${Date.now()}`, content: wpContent, status: 'draft' }),
});
console.log('Status:', res.status);
if (res.status === 200 || res.status === 201) {
  const data = await res.json();
  console.log('✅ OK, ID:', data.id, 'Slug:', data.slug);
  await fetch(`${process.env.WP_URL}/wp-json/wp/v2/pages/${data.id}?force=true`, { method: 'DELETE', headers: { 'Authorization': auth } });
} else {
  const text = await res.text();
  console.log('Response:', text.slice(0, 300));
}
