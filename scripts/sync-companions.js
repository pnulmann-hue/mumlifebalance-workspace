const fs = require('fs');
const ROOT = '/home/user/mumlifebalance-workspace';

// ---- 1. Framework-Block aus content-praxis extrahieren (Teil 2-6) ----
const cp = fs.readFileSync(ROOT + '/outputs/kurs-wissen-export/content-praxis-frameworks.md', 'utf8');
const startIdx = cp.indexOf('# TEIL 2 — HOOK-FORMELN');
const endIdx = cp.indexOf('## 🔗 Verwandte Notizen');
if (startIdx < 0 || endIdx < 0) { throw new Error('Anker nicht gefunden'); }
let block = cp.slice(startIdx, endIdx).trim();
// trailing "---" vor Verwandte Notizen entfernen
block = block.replace(/\n-{3,}\s*$/, '').trim();

// Header um eine Ebene demoten (### -> ####, ## -> ###, # -> ##)
function demote(md) {
  return md.split('\n').map(line => {
    if (/^### /.test(line)) return '#' + line;
    if (/^## /.test(line))  return '#' + line;
    if (/^# /.test(line))   return '#' + line;
    return line;
  }).join('\n');
}
const demoted = demote(block);

// ---- 2. IKM-Companion: ZUSATZ-WERKZEUGKASTEN ersetzen ----
const ikmPath = ROOT + '/scripts/ikm-companion/lib/system-prompt.md';
let ikm = fs.readFileSync(ikmPath, 'utf8');
const wkIdx = ikm.indexOf('# 🧰 ZUSATZ-WERKZEUGKASTEN');
if (wkIdx < 0) throw new Error('IKM Werkzeugkasten-Anker fehlt');
const ikmHead = ikm.slice(0, wkIdx).trimEnd();
const ikmNew = ikmHead + '\n\n' +
`# 🧰 ZUSATZ-WERKZEUGKASTEN: HOOK-, CAPTION- & VERKAUFS-FRAMEWORKS

> Wende diese Formeln aktiv an, wenn du der Kaeuferin Hooks, Captions, Story-Ideen oder Verkaufstexte fuer IHR Profil vorschlaegst. Waehle aus diesen Mustern und schneide sie auf ihr Thema + ihre Zielgruppe zu — erfinde nie Zahlen. Pruefe jeden fertigen Text am Ende gegen die 5 Floskel-Scans oben (kein Nicht/Sondern, kein "Stell dir vor" in geschriebenem Content, keine Buzzwords, kein Dreier-Stakkato). Die Blackliste gewinnt immer.

` + demoted + '\n';
fs.writeFileSync(ikmPath, ikmNew);
console.log('IKM system-prompt aktualisiert:', ikmNew.split('\n').length, 'Zeilen');

// ---- 3. Produktwelt-Companion: Hook/Caption/Verkauf-Sektionen ersetzen ----
const pwPath = ROOT + '/scripts/produktwelt-companion/lib/wissensgrundlage.md';
let pw = fs.readFileSync(pwPath, 'utf8');
const hookIdx = pw.indexOf('## HOOK-FORMELN');
const methodeIdx = pw.indexOf('## PRODUKT-METHODE');
if (hookIdx < 0 || methodeIdx < 0) throw new Error('Produktwelt-Anker fehlt');
const pwHead = pw.slice(0, hookIdx).trimEnd();
const pwTail = pw.slice(methodeIdx);
const pwNew = pwHead + '\n\n' + demoted + '\n\n' + pwTail;
fs.writeFileSync(pwPath, pwNew);
console.log('Produktwelt wissensgrundlage aktualisiert:', pwNew.split('\n').length, 'Zeilen');

console.log('Framework-Block:', demoted.split('\n').length, 'Zeilen eingesetzt.');
