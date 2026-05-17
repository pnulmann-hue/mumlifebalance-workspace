const auth = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');
const tests = [
  { name: 'Plain text', content: '<!-- wp:html -->\n<p>Hallo Welt</p>\n<!-- /wp:html -->' },
  { name: 'With inline style', content: '<!-- wp:html -->\n<div style="background:#dc822e;padding:20px;color:white;">Test</div>\n<!-- /wp:html -->' },
  { name: 'With script tag', content: '<!-- wp:html -->\n<div id="t">Hallo</div>\n<script>document.getElementById("t").style.color="red";</script>\n<!-- /wp:html -->' },
  { name: 'With mailto', content: '<!-- wp:html -->\n<p><a href="mailto:info@mumlifebalance.ch">E-Mail</a></p>\n<!-- /wp:html -->' },
];

for (const t of tests) {
  const res = await fetch(`${process.env.WP_URL}/wp-json/wp/v2/pages`, {
    method: 'POST',
    headers: { 'Authorization': auth, 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: `Test: ${t.name}`, slug: `test-${t.name.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}`, content: t.content, status: 'draft' }),
  });
  console.log(`${t.name}: ${res.status === 200 || res.status === 201 ? '✅ OK' : '❌ ' + res.status}`);
  // Clean up — delete if created
  if (res.status === 200 || res.status === 201) {
    const data = await res.json();
    await fetch(`${process.env.WP_URL}/wp-json/wp/v2/pages/${data.id}?force=true`, { method: 'DELETE', headers: { 'Authorization': auth } });
  }
}
