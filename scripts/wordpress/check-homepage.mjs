const auth = 'Basic ' + Buffer.from(`${process.env.WP_USER}:${process.env.WP_APP_PASSWORD}`).toString('base64');
const res = await fetch(`${process.env.WP_URL}/wp-json/wp/v2/settings`, {
  headers: { 'Authorization': auth }
});
const data = await res.json();
console.log('show_on_front:', data.show_on_front);
console.log('page_on_front:', data.page_on_front);
console.log('page_for_posts:', data.page_for_posts);
if (data.page_on_front) {
  const page = await fetch(`${process.env.WP_URL}/wp-json/wp/v2/pages/${data.page_on_front}`, { headers: { 'Authorization': auth } }).then(r => r.json());
  console.log('Homepage:', page.title?.rendered, '| Slug:', page.slug, '| Status:', page.status);
}
