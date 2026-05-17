import { readFile } from 'node:fs/promises';
const WP_URL = process.env.WP_URL;
const auth = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');

let html = await readFile('C:/Users/pnulm/Desktop/Mein Business/.claude/worktrees/upbeat-yalow-d35cfb/outputs/link-in-bio/index.html', 'utf-8');
html = html.replace(/src="patricia\.jpg"/g, 'src="https://mumlifebalance.ch/wp-content/uploads/2026/05/patricia-scaled.jpg"');

// IFRAME-Block komplett rausnehmen (inkl. wrapping div + script)
html = html.replace(/<!-- VIMEO-EMBED[\s\S]*?<script src="https:\/\/player\.vimeo\.com\/api\/player\.js"><\/script>/m, '<p style="text-align:center;color:#999;padding:20px;">(Vimeo-Video kommt hier später)</p>');

const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
const fontLinks = (html.match(/<link[^>]+fonts\.googleapis[^>]+>/g) || []).join('\n');
const fontPreconnect = (html.match(/<link[^>]+fonts\.gstatic[^>]+>/g) || []).join('\n');
const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/);

const wpContent = `<!-- wp:html -->\n${fontPreconnect}\n${fontLinks}\n<style>${styleMatch[1]}</style>\n${bodyMatch[1]}\n<!-- /wp:html -->`;

const res = await fetch(`${WP_URL}/wp-json/wp/v2/pages`, {
  method: 'POST',
  headers: { 'Authorization': auth, 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'Bio Test (no iframe)', slug: 'bio-test', content: wpContent, status: 'draft' }),
});
const data = await res.text();
console.log('Status:', res.status);
console.log('Response:', data.slice(0, 400));
