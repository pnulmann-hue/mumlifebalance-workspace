"""Story-Flyer für die doTERRA BOGO-Woche 20.–27.10.2026.

Baut slides.html (10 Folien, 1080x1920) aus den Original-Fotos des BOGO-Booklets.
Rendern: node scripts/story-render/bogo-2026-10-render.mjs
Quelle der Angebote: Oct26_BOGO_Book_DE.pdf (Booklet vom 12.10.2026).
Compliance: nur Duft, Moment und Fakten aus dem Booklet, keine Wirkung, keine Preise
(stehen nicht im Booklet).
"""
from pathlib import Path
import html

WS = Path(__file__).resolve().parents[2]
ZIEL = WS / "outputs/stories/2026-10-20-bogo-doterra"
FONTS = WS / "scripts/story-render/fonts"

FUSS = "*Nur solange der Vorrat reicht · Marken von dōTERRA Holdings, LLC"


def hv(s):
    """*Wort* wird orange."""
    s = html.escape(s, quote=False)
    import re
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s.replace("™", "<sup>™</sup>")


# art: foto (Foto oben, Creme-Feld unten) · dunkel (Dunkelblau mit Fotokarte)
FOLIEN = [
    dict(art="foto", foto="01-start.jpg", y=280, pille="BOGO-Woche · 20.–27. Oktober",
         titel="Kauf eins, eins gibt's *geschenkt*.",
         text="Eine Woche lang legt doTERRA zu fünf Ölen ein zweites dazu, beim Sandelholz sogar drei. Ich zeig dir, was in den Duos steckt.",
         weiter=True),
    dict(art="foto", foto="02-uebersicht.jpg", y=300, pille="Die Angebote auf einen Blick",
         titel="Die fünf *Duos*",
         liste=[("Baldrian 15 ml", "dōTERRA Serenity™ 15 ml"),
                ("Air-X™ 15 ml", "Eukalyptus 15 ml"),
                ("On Guard™ 15 ml", "Oregano 15 ml"),
                ("Römische Kamille 5 ml", "2× Adaptiv™ Badeöl"),
                ("Sandelholz 5 ml", "Grapefruit, SuperMint™ & Shinrin-Yoku™ Touch")],
         text="Einzeln bestellbar oder alle zusammen als Bundle."),
    dict(art="foto", foto="03-baldrian.jpg", y=200, pille="Duo 1 · nur kurz erhältlich",
         titel="Baldrian + *Serenity*™",
         text="Baldrian riecht holzig und erdig, Serenity süss-blumig mit Lavendel, Zeder und Vanille. Zwei Düfte für den Moment, in dem abends das Haus endlich still wird.",
         deal="15 ml Baldrian kaufen · 15 ml Serenity™ gratis"),
    dict(art="foto", foto="04-airx.jpg", y=150, pille="Duo 2",
         titel="Air-X™ + *Eukalyptus*",
         text="Air-X duftet nach Zitrus mit einem Hauch Holz und Kardamom, Eukalyptus klar und frisch. Für eine 15-ml-Flasche Eukalyptus braucht es rund 1,5 kg Blätter.",
         deal="15 ml Air-X™ kaufen · 15 ml Eukalyptus gratis"),
    dict(art="foto", foto="05-onguard.jpg", y=250, pille="Duo 3",
         titel="On Guard™ + *Oregano*",
         text="On Guard ist warm und würzig mit Orange, Zimt und Nelke, ein Tropfen übers Popcorn ist ein Klassiker. Oregano ist kräftig, in der Küche reicht ein Zahnstocher voll.",
         deal="15 ml On Guard™ kaufen · 15 ml Oregano gratis"),
    dict(art="foto", foto="06-kamille.jpg", y=250, pille="Duo 4",
         titel="Kamille + 2× *Badeöl*",
         text="Die Römische Kamille duftet sanft blumig und süss. Dazu kommen zwei Flaschen Adaptiv™ Badeöl, das sich im Wasser milchig verteilt, ganz ohne Schütteln.",
         deal="5 ml Römische Kamille kaufen · 2× Adaptiv™ Beruhigendes Badeöl gratis"),
    dict(art="foto", foto="07-sandelholz.jpg", y=200, pille="Duo 5 · der grösste Deal",
         titel="Eins kaufen, *drei* dazu",
         text="Zum Sandelholz gibt's Grapefruit, SuperMint™ und den Shinrin-Yoku™ Touch Roller. Sandelholz wächst übrigens mindestens 15 Jahre, bevor es geerntet werden kann.",
         deal="5 ml Sandelholz kaufen · Grapefruit 15 ml, SuperMint™ 15 ml & Shinrin-Yoku™ Touch 10 ml gratis"),
    dict(art="foto", foto="08-douglasie.jpg", y=327, pille="Das BOGO-Bundle",
         titel="Alles zusammen + *Douglasie*",
         text="Wer das ganze Bundle nimmt, bekommt alle fünf Duos und eine 5 ml Douglasie geschenkt. Sie riecht nach Nadelwald mit einer frischen, zitronigen Note.",
         deal="Alle 5 Duos + 5 ml Douglasie gratis"),
    dict(art="dunkel", foto="02-uebersicht.jpg", y=380, pille="Bis 27. Oktober",
         titel="Was davon nimmst du *mit*?",
         text="Antworte mir mit BOGO, dann stell ich dir deinen Warenkorb zusammen, damit du die Duos mitnimmst und nichts doppelt bestellst.",
         sticker=True),
    dict(art="dunkel", foto="01-start.jpg", y=420, pille="Dienstag, 27. Oktober",
         titel="Heute ist *letzter* BOGO-Tag",
         text="Wer noch ein Duo oder das Bundle will: heute ist der letzte Tag. Schreib mir BOGO, ich helf dir beim Bestellen.",
         sticker=True),
]


def folie(i, f):
    pille = f'<div class="pille">{hv(f["pille"])}</div>'
    titel = f'<h1>{hv(f["titel"])}</h1>'
    text = f'<p class="text">{hv(f["text"])}</p>'
    liste = ""
    if f.get("liste"):
        liste = '<ul class="liste">' + "".join(
            f'<li><span class="kauf">{hv(a)}</span><span class="plus">+ gratis</span><span class="gratis">{hv(b)}</span></li>'
            for a, b in f["liste"]) + "</ul>"
    deal = f'<div class="deal">{hv(f["deal"])}</div>' if f.get("deal") else ""
    weiter = '<div class="weiter">weiter →</div>' if f.get("weiter") else ""
    fuss = f'<div class="fuss">{hv(FUSS)}</div>'
    if f["art"] == "foto":
        return f'''<section class="slide foto" id="s{i+1:02d}">
  <div class="bild" style="background-image:url('fotos/{f["foto"]}');background-position:center -{f["y"]}px"></div>
  {pille}
  <div class="feld{' mitliste' if liste else ''}">{titel}{liste}{text}{deal}{weiter}</div>
  {fuss}
</section>'''
    return f'''<section class="slide dunkel" id="s{i+1:02d}">
  <div class="karte" style="background-image:url('fotos/{f["foto"]}');background-position:center -{f["y"]}px"></div>
  {pille}
  <div class="feld">{titel}{text}</div>
  {fuss}
</section>'''


CSS = f"""
@font-face {{ font-family: Philosopher; src: url('{(FONTS/'Philosopher-Bold.ttf').as_uri()}'); font-weight: 700; }}
@font-face {{ font-family: Philosopher; src: url('{(FONTS/'Philosopher-Regular.ttf').as_uri()}'); font-weight: 400; }}
@font-face {{ font-family: 'Source Sans 3'; src: url('{(FONTS/'SourceSans3-Regular.ttf').as_uri()}'); }}
:root {{ --creme:#f1ecdd; --blau:#29556d; --text:#0c1c30; --orange:#dc822e; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ background:#888; font-family:'Source Sans 3', sans-serif; }}
.slide {{ width:1080px; height:1920px; position:relative; overflow:hidden; margin:0 auto 40px; }}
em {{ font-style:normal; color:var(--orange); }}
.foto {{ background:var(--creme); color:var(--text); }}
.foto .bild {{ position:absolute; left:0; top:0; width:1080px; height:1240px; background-size:1080px auto; background-repeat:no-repeat; }}
.pille {{ position:absolute; left:72px; top:262px; background:var(--creme); color:var(--blau);
  font:700 34px/1 Philosopher; padding:20px 30px; border-radius:60px; box-shadow:0 6px 24px rgba(12,28,48,.18); }}
.foto .feld {{ position:absolute; left:0; right:0; top:1150px; bottom:0; background:var(--creme);
  border-radius:56px 56px 0 0; padding:70px 80px 0; }}
.foto .feld.mitliste {{ top:800px; padding-top:52px; }}
.mitliste .text {{ font-size:34px; margin-top:22px; }}
sup {{ font-size:.45em; vertical-align:.9em; line-height:0; }}
h1 {{ font:700 84px/1.06 Philosopher; color:var(--blau); letter-spacing:-.5px; }}
.text {{ font-size:38px; line-height:1.42; margin-top:28px; color:var(--text); }}
.deal {{ margin-top:34px; display:inline-block; border:3px solid var(--orange); color:var(--text);
  font-size:31px; line-height:1.3; padding:16px 26px; border-radius:22px; max-width:920px; }}
.weiter {{ margin-top:34px; text-align:right; font:700 34px Philosopher; color:var(--orange); }}
.liste {{ list-style:none; margin-top:30px; }}
.liste li {{ display:grid; grid-template-columns:auto 1fr; column-gap:18px; padding:13px 0; border-bottom:2px solid rgba(41,85,109,.18); }}
.liste .kauf {{ font:700 37px/1.2 Philosopher; color:var(--blau); grid-column:1 / -1; }}
.liste .plus {{ font-size:28px; color:var(--orange); font-weight:700; padding-top:4px; }}
.liste .gratis {{ font-size:31px; line-height:1.3; }}
.fuss {{ position:absolute; left:80px; right:80px; top:1712px; font-size:22px; color:rgba(12,28,48,.55); }}
.dunkel {{ background:var(--blau); color:var(--creme); }}
.dunkel .karte {{ position:absolute; left:72px; right:72px; top:240px; height:780px; border-radius:48px;
  background-size:936px auto; background-repeat:no-repeat; }}
.dunkel .pille {{ top:282px; left:110px; }}
.dunkel .feld {{ position:absolute; left:80px; right:80px; top:1090px; }}
.dunkel h1 {{ color:var(--creme); }}
.dunkel .text {{ color:rgba(241,236,221,.9); }}
.dunkel .fuss {{ color:rgba(241,236,221,.55); }}
"""

seiten = "\n".join(folie(i, f) for i, f in enumerate(FOLIEN))
ZIEL.mkdir(parents=True, exist_ok=True)
(ZIEL / "slides.html").write_text(f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>BOGO-Woche Oktober</title><style>{CSS}</style></head><body>
{seiten}
</body></html>""", encoding="utf-8")
print(f"{len(FOLIEN)} Folien -> {ZIEL/'slides.html'}")
