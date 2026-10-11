"""
Ergaenzt die Startklar-Werkstatt um ein ausformuliertes Beispiel je Feld.

Vorher gab es 13 kurze Hinweise und ein einziges Beispiel. Wer vor einem
leeren Feld sitzt, kommt damit trotzdem nicht ins Schreiben — und die
Verkaufsseite versprach mehr, als drinstand.

Jedes Textfeld bekommt jetzt:
  · ein fertiges Beispiel zum Ansehen
  · einen Knopf, der es als Startpunkt ins Feld setzt

🚨 Alle Beispiele gehoeren derselben erfundenen Person: **Sandra, Energie fuer
Mamas ab 35.** Das ist Absicht — wenn jedes Feld ein anderes Thema zeigt,
versteht niemand, wie die Teile zusammengehoeren. Sandra ist frei erfunden und
wird im Text auch so benannt, damit sie niemand fuer eine echte Kundin haelt.

Aufruf:
  python scripts/startklar/werkstatt-beispiele.py            # einsetzen
  python scripts/startklar/werkstatt-beispiele.py --zeigen   # nur auflisten
"""
import argparse
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATEI = ROOT / "outputs" / "produkte" / "instagram-startklar" / "04-arbeitsblaetter" / "startklar-werkstatt.html"

# Station -> Feld -> Beispiel. Eine Person, ein Thema, durchgehend.
BEISPIELE = {
    "konto": {
        "archiv": "Die Ferienbilder von 2019, die Fasnachtsfotos und alles, wo meine "
                  "Kinder gross im Bild sind. Das bleibt alles da, es sieht nur "
                  "niemand mehr ausser mir.",
    },
    "namen": {
        "user": "sandra.energie",
        "name": "Sandra · Energie für Mamas ab 35",
    },
    # 🚨 Die vier Bio-Zeilen zusammen duerfen 150 Zeichen nicht ueberschreiten —
    # die Station prueft das selbst und wirft sonst einen Stop. Die erste Fassung
    # lag bei 198 und waere an der eigenen Pruefung gescheitert.
    "bio": {
        "z1": "Für Mamas ab 35, die abends nur aufs Sofa fallen.",
        "z2": "3 Kinder, war selbst 2 Jahre dauermüde.",
        "z3": "Dienstags ein Tipp für den Tag.",
        "z4": "Hol dir die 5 Morgen-Ideen ↓",
    },
    "schaufenster": {
        "link": "sandra-energie.ch/start",
    },
    "profilcheck": {
        "eindruck": "Eine Frau, die müden Mamas hilft, wieder durch den Tag zu kommen. "
                    "Man sieht ihr Gesicht, man merkt, dass sie selber Kinder hat, und "
                    "man kann sofort auf einen Link tippen.",
    },
    "hook": {
        # Die Station verlangt Zeitanker oder Zahl und erkennt Ziffern, keine Zahlwörter.
        "hook": "3 Jahre lang dachte ich, ich bin einfach kein Morgenmensch.",
    },
    "karussell": {
        "f1": "4 Sachen, die mich morgens fertiggemacht haben",
        "f2": "1 · Das Handy als Wecker. Ich war wach und im Kopf schon bei anderen Leuten.",
        "f3": "2 · Kaffee auf leeren Magen. Danach war ich hellwach und um zehn am Boden.",
        "f4": "3 · Frühstück im Stehen, während ich Brote geschmiert habe. Gegessen hab ich meistens nichts.",
        "f5": "4 · Der erste Blick auf die Liste. Ich hab den Tag begonnen mit dem Gefühl, schon hinterher zu sein.",
        "f6": "Welche davon kennst du? Schreib mir die Nummer, dann erzähl ich dir, was bei mir geholfen hat.",
    },
    "story": {
        "frage": "Wie wachst du morgens auf?",
        "a": "Direkt hellwach",
        "b": "Brauch erst mal zwanzig Minuten",
    },
    "caption": {
        "text": "Ich hab drei Jahre lang gedacht, ich bin einfach kein Morgenmensch.\n\n"
                "Dann hab ich gemerkt, dass es gar nicht am Aufstehen lag, sondern an "
                "den ersten zwanzig Minuten danach. Die hab ich nämlich jeden Tag "
                "gleich verbracht: Handy, Kaffee, Liste. In dieser Reihenfolge.\n\n"
                "Seit ich das umgedreht habe, ist mein Nachmittag ein anderer. Nicht "
                "weil ich früher aufstehe, sondern weil ich anders anfange.\n\n"
                "Wenn du das kennst, schreib mir MORGEN in die Kommentare, dann schick "
                "ich dir die fünf Ideen, die bei mir geblieben sind.\n\n"
                "#mamaalltag #energieimalltag #mamasab35 #morgenroutine #dreifachmama",
    },
    "fallen": {
        "richtlinien": "Im Backoffice unter Downloads → Richtlinien Social Media (PDF)",
    },
    # 🚨 Hier gehoert hinein, was Sandra WIRKLICH postet — nicht, was der
    # Beitrag bewirken soll. „Wobei ich helfe und wie du mich erreichst" ist
    # eine Aufgabenbeschreibung und hilft niemandem beim Schreiben.
    "startplan": {
        "p1": "Ich bin Sandra, 3 Kinder, und ich hab 2 Jahre gebraucht, um wieder durch den Tag zu kommen.",
        "p2": "Der Nachmittag, an dem ich im Auto sass und einfach nicht mehr aussteigen wollte.",
        "p3": "3 Sachen, die ich morgens geändert hab — die dritte hat am meisten gebracht.",
        "p4": "Dienstag, 7:40 Uhr: Znüni schmieren, Schuhe suchen — und ich hab trotzdem gefrühstückt.",
        "p5": "Was ich Mamas antworte, die sagen „ich bin einfach nur noch müde\". Schreib mir MORGEN, dann schick ich dir meine 5 Ideen.",
    },
}

# Der Block unter jedem Feld plus der Knopf, der ihn uebernimmt.
RENDER_ALT = """  const el = f.typ==="lang" ? document.createElement("textarea") : document.createElement("input");
  if(f.typ!=="lang") el.type="text";
  el.value = v[f.key]||"";
  el.addEventListener("input",()=>{ v[f.key]=el.value; sichern(); railBauen(); });
  l.appendChild(el);
  return l;"""

RENDER_NEU = """  const el = f.typ==="lang" ? document.createElement("textarea") : document.createElement("input");
  if(f.typ!=="lang") el.type="text";
  el.value = v[f.key]||"";
  el.addEventListener("input",()=>{ v[f.key]=el.value; sichern(); railBauen(); });
  l.appendChild(el);

  // Beispiel: zeigt, wie es aussehen kann, und setzt es auf Wunsch ins Feld.
  // Bewusst NICHT als placeholder — der verschwindet beim Tippen und laesst
  // sich nicht kopieren, genau dann wenn man ihn braucht.
  if(f.beispiel){
    const bx=document.createElement("div"); bx.className="beispiel";
    const kopf=document.createElement("div"); kopf.className="bsp-kopf";
    kopf.textContent="So macht es Sandra";
    const txt=document.createElement("div"); txt.className="bsp-text";
    txt.textContent=f.beispiel;
    const knopf=document.createElement("button");
    knopf.type="button"; knopf.className="bsp-knopf";
    knopf.textContent="Als Start übernehmen";
    knopf.addEventListener("click",()=>{
      // Schon Geschriebenes nie stillschweigend ueberschreiben.
      if((el.value||"").trim() && !confirm("Du hast hier schon etwas stehen. Soll das Beispiel es ersetzen?")) return;
      el.value=f.beispiel; v[f.key]=f.beispiel; sichern(); railBauen();
      el.focus();
      knopf.textContent="Drin — jetzt deins draus machen";
      setTimeout(()=>{ knopf.textContent="Als Start übernehmen"; }, 2600);
    });
    bx.append(kopf, txt, knopf);
    l.appendChild(bx);
  }
  return l;"""

CSS_ALT = "  --radius:10px;"
CSS_NEU = """  --radius:10px;
  --bsp-bg:#f2f7f7; --bsp-linie:#cfe3e4;"""

CSS_BLOCK = """
/* Beispiel-Kasten unter jedem Feld */
.beispiel{
  margin-top:8px; background:var(--bsp-bg); border:1px solid var(--bsp-linie);
  border-radius:8px; padding:10px 12px;
}
.bsp-kopf{
  font-size:11px; letter-spacing:.09em; text-transform:uppercase;
  color:var(--petrol); font-weight:700; margin-bottom:5px;
}
.bsp-text{
  font-size:14px; line-height:1.55; color:var(--ink); white-space:pre-wrap;
}
.bsp-knopf{
  margin-top:9px; background:transparent; border:1px solid var(--petrol);
  color:var(--petrol); border-radius:999px; padding:5px 13px;
  font:600 13px/1 inherit; cursor:pointer;
}
.bsp-knopf:hover{ background:var(--petrol); color:#fff; }
"""



def js_text(s):
    """Text so absichern, dass er in einer JS-Zeichenkette stehen kann.

    JSON-Escaping entspricht dem von JavaScript — das erspart die
    Backslash-Akrobatik, an der ich hier zweimal gescheitert bin.
    """
    return json.dumps(s, ensure_ascii=False)[1:-1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zeigen", action="store_true", help="nur auflisten, nichts ändern")
    ap.add_argument("--aktualisieren", action="store_true",
                    help="bestehende Beispiele durch die aktuellen ersetzen")
    args = ap.parse_args()

    if args.zeigen:
        n = 0
        for st, felder in BEISPIELE.items():
            print("\n### %s" % st)
            for k, b in felder.items():
                print("  %-12s %s" % (k, b[:72].replace("\n", " ⏎ ")))
                n += 1
        print("\n%d Beispiele in %d Stationen" % (n, len(BEISPIELE)))
        return

    text = DATEI.read_text(encoding="utf-8")
    if "bsp-knopf" in text and not args.aktualisieren:
        print("Schon gesetzt — mit --aktualisieren werden die Texte nachgezogen.")
        return
    if args.aktualisieren:
        # Nur die Texte tauschen, Aufbau und Knopf bleiben stehen.
        geaendert = 0
        for station, felder in BEISPIELE.items():
            anf = text.find('id:"%s"' % station)
            if anf == -1:
                continue
            ende = text.find('id:"', anf + 8)
            ende = len(text) if ende == -1 else ende
            block = text[anf:ende]
            for key, beispiel in felder.items():
                js = js_text(beispiel)
                muster = r'(key:"%s",[^}]*?beispiel:")[^"]*(")' % re.escape(key)
                block, n = re.subn(muster, lambda m: m.group(1) + js + m.group(2), block)
                geaendert += n
            text = text[:anf] + block + text[ende:]
        DATEI.write_text(text, encoding='utf-8')
        print('%d Beispiele nachgezogen.' % geaendert)
        return

    gesetzt, fehlend = 0, []
    for station, felder in BEISPIELE.items():
        # Den Block dieser Station eingrenzen, damit gleiche Feldnamen in
        # anderen Stationen nicht mitgetroffen werden.
        anf = text.find('id:"%s"' % station)
        if anf == -1:
            fehlend.append(station + " (Station fehlt)")
            continue
        ende = text.find('id:"', anf + 8)
        if ende == -1:
            ende = len(text)
        block = text[anf:ende]
        neu = block
        for key, beispiel in felder.items():
            muster = r'(\{typ:"(?:kurz|lang)",\s*key:"%s",[^}]*?)\}' % re.escape(key)
            m = re.search(muster, neu)
            if not m:
                fehlend.append("%s.%s" % (station, key))
                continue
            js = js_text(beispiel)
            neu = neu[:m.end(1)] + ', beispiel:"%s"' % js + neu[m.end(1):]
            gesetzt += 1
        text = text[:anf] + neu + text[ende:]

    if RENDER_ALT not in text:
        print("FEHLER: die Feld-Zeichenroutine sieht anders aus als erwartet.")
        print("Erst nachsehen, wie feldBauen() heute gebaut ist — nichts geändert.")
        sys.exit(1)
    text = text.replace(RENDER_ALT, RENDER_NEU, 1)
    text = text.replace(CSS_ALT, CSS_NEU, 1)
    text = text.replace("</style>", CSS_BLOCK + "</style>", 1)

    DATEI.write_text(text, encoding="utf-8")
    print("%d Beispiele eingesetzt." % gesetzt)
    if fehlend:
        print("NICHT gefunden (bitte prüfen): " + ", ".join(fehlend))
    print("Datei: %s" % DATEI)


if __name__ == "__main__":
    main()
