"""
Cover-Generator fuer Reels und Feed-Posts.

Zwei Arten, die sich im Feed abwechseln — das ist Patricias ABAB-Regel:

  foto    ein Standbild aus dem Clip, darueber ein Farbverlauf von unten
  farbe   eine Vollflaeche in einer Brandfarbe, ganz ohne Bild

Die Verlaufs- bzw. Flaechenfarbe **rotiert**: Petrol → Dunkelblau → Orange.
Der Merkzettel dafuer liegt in `outputs/reels/_cover-verlauf.json` — beim
naechsten Cover wird automatisch die naechste Farbe genommen.

Schrift: Philosopher fuer die Headline (Patricias Display-Schrift, kein Zukauf),
Source Sans 3 fuer die Unterzeile. Headline in Creme, optional **ein** Wort in
der Akzentfarbe.

Aufruf:
  python scripts/videoschnitt/cover.py --spec cover.json
  python scripts/videoschnitt/cover.py --beispiele    # vier Muster zum Anschauen

Spezifikation (cover.json):
{
  "art": "foto",                       // oder "farbe"
  "quelle": "video/output/.../rohschnitt.mp4",   // bei art=foto: Video ODER Bild
  "bei_sek": 1.5,                      // welches Standbild aus dem Video
  "headline": "3 Naehrstoffe ab 35",
  "betont": "35",                      // dieses Wort in der Akzentfarbe (optional)
  "unter": "die fast jeder Mama fehlen — und keiner sagt es ihr.",
  "farbe": "petrol",                   // weglassen = naechste aus der Rotation
  "ziel": "outputs/cover/mein-cover.png",
  "format": "reel"                     // reel 1080x1920 | feed 1080x1350
}
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
MERKZETTEL = ROOT / "outputs" / "reels" / "_cover-verlauf.json"
RENDER = ROOT / "scripts" / "karussell-render"

PETROL = "#12828c"
DUNKELBLAU = "#29556d"
CREME = "#f1ecdd"
ORANGE = "#dc822e"

# Rotation. Kein Gelb — das ist nicht Patricias Marke.
FARBEN = ["petrol", "dunkelblau", "orange"]
HEX = {"petrol": PETROL, "dunkelblau": DUNKELBLAU, "orange": ORANGE}

FORMATE = {"reel": (1080, 1920), "feed": (1080, 1350)}


def log(msg):
    print(msg, flush=True)


def naechste_farbe(gewuenscht=None):
    """Rotiert die Farbe, damit nicht jeden Tag dasselbe im Feed steht."""
    zettel = {"letzte": None, "verlauf": []}
    if MERKZETTEL.exists():
        try:
            zettel = json.loads(MERKZETTEL.read_text(encoding="utf-8"))
        except Exception:
            pass
    if gewuenscht in FARBEN:
        farbe = gewuenscht
    else:
        letzte = zettel.get("letzte")
        if letzte in FARBEN:
            farbe = FARBEN[(FARBEN.index(letzte) + 1) % len(FARBEN)]
        else:
            farbe = FARBEN[0]
    zettel["letzte"] = farbe
    zettel.setdefault("verlauf", []).append(farbe)
    zettel["verlauf"] = zettel["verlauf"][-30:]
    MERKZETTEL.parent.mkdir(parents=True, exist_ok=True)
    MERKZETTEL.write_text(json.dumps(zettel, ensure_ascii=False, indent=2), encoding="utf-8")
    return farbe


def standbild(quelle, bei_sek, ziel_png, breite, hoehe):
    """Ein Standbild aus dem Video, auf das Zielformat beschnitten."""
    q = Path(quelle)
    if not q.exists():
        q = ROOT / quelle
    if not q.exists():
        sys.exit("Quelle nicht gefunden: %s" % quelle)
    vf = ("scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d"
          % (breite, hoehe, breite, hoehe))
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    if q.suffix.lower() in {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi"}:
        cmd += ["-ss", "%.2f" % float(bei_sek)]
    cmd += ["-i", str(q), "-frames:v", "1", "-vf", vf, str(ziel_png)]
    subprocess.run(cmd, check=True)
    return ziel_png


def headline_html(headline, betont, akzent):
    """Genau ein Wort darf die Akzentfarbe bekommen."""
    if not betont or betont not in headline:
        return "<span>%s</span>" % headline
    vor, _, nach = headline.partition(betont)
    return ('<span>%s</span><span style="color:%s">%s</span><span>%s</span>'
            % (vor, akzent, betont, nach))


def baue_html(spec, bild_pfad, farbe, breite, hoehe):
    hexf = HEX[farbe]
    akzent = ORANGE if farbe != "orange" else CREME
    gross = 96 if len(spec.get("headline", "")) <= 22 else 76

    if spec.get("art") == "farbe":
        hintergrund = ("background: linear-gradient(160deg, %s 0%%, %s 100%%);"
                       % (hexf, DUNKELBLAU if farbe != "dunkelblau" else PETROL))
        bild = ""
        block = ("position:absolute; inset:0; display:flex; flex-direction:column;"
                 " justify-content:center; align-items:flex-start;")
        schleier = ""
    else:
        hintergrund = "background:#0b1620;"
        bild = ('<img src="%s" alt="">' % Path(bild_pfad).as_uri())
        block = "position:absolute; left:0; right:0; bottom:0;"
        # Zwei Ebenen statt einer harten Kante:
        #   1. ein ruhiger Farbschleier ueber dem GANZEN Bild — der haelt den Feed
        #      in Patricias Farbe zusammen und schluckt fremde Umgebungsfarben
        #   2. ein weicher Verlauf, der nach unten dichter wird, aber nie ganz
        #      zumacht — das Foto bleibt bis unten sichtbar
        # Orange deckt staerker, deshalb dort schwaechere Werte.
        if farbe == "orange":
            tint, mitte, unten = "2E", "6B", "B8"
        else:
            tint, mitte, unten = "3D", "80", "CC"
        schleier = (
            '<div class="schleier" style="background:%s%s; mix-blend-mode:multiply"></div>'
            '<div class="schleier" style="background: linear-gradient(180deg,'
            ' rgba(0,0,0,0) 0%%, %s26 30%%, %s%s 62%%, %s%s 88%%, %s%s 100%%)"></div>'
            % (hexf, tint, hexf, hexf, mitte, hexf, unten, hexf, unten))

    return """<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@700&family=Source+Sans+3:wght@300;400&display=swap" rel="stylesheet">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { width:%(b)dpx; height:%(h)dpx; overflow:hidden; }
  .cover { position:relative; width:%(b)dpx; height:%(h)dpx; overflow:hidden; %(hintergrund)s }
  .cover img { position:absolute; inset:0; width:100%%; height:100%%; object-fit:cover; }
  .schleier { position:absolute; inset:0; }
  .block { %(block)s padding:0 84px %(unten)dpx; }
  .cover.flaeche .block { padding:0 92px; }
  .cover.flaeche h1 { font-size:%(gross_flaeche)dpx; }
  .cover.flaeche p { font-size:50px; margin-top:34px; }
  h1 {
    font-family:"Philosopher", Georgia, serif;
    font-size:%(gross)dpx; font-weight:700; line-height:1.08;
    color:%(creme)s; letter-spacing:-0.01em;
    text-shadow:0 4px 26px rgba(0,0,0,0.45);
  }
  p {
    font-family:"Source Sans 3", "Segoe UI", sans-serif;
    font-weight:300; font-size:52px; line-height:1.30;
    color:#ffffff; margin-top:22px; max-width:88%%;
    text-shadow:0 3px 18px rgba(0,0,0,0.5);
  }
  /* Der Bereich, den Instagram im Raster zeigt (mittiges 4:5) */
  .raster { position:absolute; left:0; right:0; top:%(rt)dpx; height:%(rh)dpx; }
</style></head>
<body>
  <div class="cover %(klasse)s">
    %(bild)s
    %(schleier)s
    <div class="block">
      <h1>%(headline)s</h1>
      %(unter)s
    </div>
  </div>
  <script>
    // Die Headline wird eingepasst, nicht geschaetzt: so gross wie moeglich,
    // hoechstens drei Zeilen, und immer innerhalb des Textblocks.
    function einpassen() {
      var h = document.querySelector('h1');
      var block = document.querySelector('.block');
      if (!h || !block) return;
      var innen = block.clientWidth
        - parseFloat(getComputedStyle(block).paddingLeft)
        - parseFloat(getComputedStyle(block).paddingRight);
      var max = %(fit_max)d, min = 56, zeilen = 3;
      var s = max;
      h.style.fontSize = s + 'px';
      h.style.whiteSpace = 'normal';
      while (s > min) {
        var zh = s * 1.08;
        if (h.scrollWidth <= innen + 1 && h.offsetHeight <= zh * zeilen + 2) break;
        s -= 2;
        h.style.fontSize = s + 'px';
      }
    }
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(einpassen);
    } else {
      window.addEventListener('load', einpassen);
    }
  </script>
</body></html>
""" % {
        "b": breite, "h": hoehe,
        "hintergrund": hintergrund,
        "bild": bild,
        "schleier": schleier,
        "block": block,
        "klasse": "flaeche" if spec.get("art") == "farbe" else "foto",
        "gross": gross,
        "gross_flaeche": gross + 26,
        "fit_max": 170 if spec.get("art") == "farbe" else 148,
        # Unterkante der Raster-Sicherheitszone (mittiges 4:5) plus Luft
        "unten": int(hoehe - (hoehe + breite * 1.25) / 2 + 40)
                 if hoehe > breite * 1.3 else 132,
        "creme": CREME,
        "headline": headline_html(spec.get("headline", ""), spec.get("betont"), akzent),
        "unter": ("<p>%s</p>" % spec["unter"]) if spec.get("unter") else "",
        "rt": int((hoehe - hoehe * 0.7) / 2), "rh": int(hoehe * 0.7),
    }


def rendern(html_pfad, ziel_png, breite, hoehe):
    js = RENDER / "_cover-shot.mjs"
    js.write_text("""import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
const a = Object.fromEntries(process.argv.slice(2).map(x => {
  const [k, ...r] = x.replace(/^--/, '').split('='); return [k, r.join('=') || true];
}));
await fs.mkdir(path.dirname(path.resolve(a.output)), { recursive: true });
const browser = await puppeteer.launch({ headless: 'new',
  args: ['--allow-file-access-from-files', '--disable-web-security', '--no-sandbox'] });
try {
  const page = await browser.newPage();
  await page.setViewport({ width: Number(a.w), height: Number(a.h), deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.resolve(a.input)).href, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 400));
  const el = await page.$('.cover');
  await el.screenshot({ path: path.resolve(a.output), type: 'png' });
  console.log('OK');
} finally { await browser.close(); }
""", encoding="utf-8")
    subprocess.run(["node", str(js), "--input=%s" % html_pfad, "--output=%s" % ziel_png,
                    "--w=%d" % breite, "--h=%d" % hoehe], cwd=str(RENDER), check=True)


def ein_cover(spec):
    breite, hoehe = FORMATE.get(spec.get("format", "reel"), FORMATE["reel"])
    farbe = naechste_farbe(spec.get("farbe"))
    ziel = Path(spec.get("ziel") or (ROOT / "outputs" / "cover" / "cover.png"))
    if not ziel.is_absolute():
        ziel = ROOT / ziel
    ziel.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        bild = None
        if spec.get("art") != "farbe":
            bild = standbild(spec["quelle"], spec.get("bei_sek", 1.0),
                             Path(tmp) / "still.png", breite, hoehe)
        html = Path(tmp) / "cover.html"
        html.write_text(baue_html(spec, bild, farbe, breite, hoehe), encoding="utf-8")
        rendern(html, ziel, breite, hoehe)

    log("  %-7s %-11s → %s" % (spec.get("art", "foto"), farbe, ziel.relative_to(ROOT)))
    return ziel


def beispiele():
    """Vier Muster: dreimal Foto mit rotierendem Verlauf, einmal Vollflaeche."""
    B = Path(r"C:\Users\pnulm\CrossDevice\S25 Ultra von Patricia\storage\DCIM\Reel-Videos")
    clips = sorted([p for p in B.glob("*.mp4")], key=lambda p: p.stat().st_size, reverse=True)
    if not clips:
        sys.exit("Keine Clips gefunden — haengt das Handy?")
    muster = [
        {"art": "foto", "quelle": str(clips[0]), "bei_sek": 2.0, "farbe": "petrol",
         "headline": "3 Nährstoffe ab 35", "betont": "35",
         "unter": "die fast jeder Mama fehlen — und keiner sagt es ihr.",
         "ziel": "outputs/cover/_muster-1-petrol.png"},
        {"art": "foto", "quelle": str(clips[1 % len(clips)]), "bei_sek": 2.0, "farbe": "dunkelblau",
         "headline": "Mehr posten war nie dein Problem", "betont": "nie",
         "unter": "Was wirklich fehlt, ist eine Entscheidung.",
         "ziel": "outputs/cover/_muster-2-dunkelblau.png"},
        {"art": "foto", "quelle": str(clips[2 % len(clips)]), "bei_sek": 2.0, "farbe": "orange",
         "headline": "Du bist nicht kaputt", "betont": "nicht",
         "unter": "Vieles davon kann hormonell sein — und du kannst etwas tun.",
         "ziel": "outputs/cover/_muster-3-orange.png"},
        {"art": "farbe", "farbe": "petrol",
         "headline": "In 4 Schritten zu deinem eigenen Thema", "betont": "4",
         "unter": "Ohne dein Network aufzugeben.",
         "ziel": "outputs/cover/_muster-4-flaeche.png"},
    ]
    log("Baue vier Muster …")
    return [ein_cover(m) for m in muster]


def main():
    p = argparse.ArgumentParser(description="Cover bauen (Foto mit Verlauf oder Vollflaeche)")
    p.add_argument("--spec", help="Pfad zur cover.json")
    p.add_argument("--beispiele", action="store_true", help="vier Muster zum Anschauen bauen")
    args = p.parse_args()

    if args.beispiele:
        beispiele()
        return
    if not args.spec:
        sys.exit("Bitte --spec <cover.json> oder --beispiele angeben.")
    s = Path(args.spec)
    if not s.exists():
        s = ROOT / args.spec
    ein_cover(json.loads(s.read_text(encoding="utf-8")))


if __name__ == "__main__":
    main()
