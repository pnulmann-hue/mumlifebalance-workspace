"""
Baut aus dem veroeffentlichten Cockpit-Artifact eine neue Fassung mit dem
Karussell-Prozess aus Jenya Korks Guide:

  1. vier feste Karussell-Typen (Listicle, Storytelling, Edukativ, Kontrovers)
  2. Funnel-Stufe TOF/MOF/BOF pro Karussell
  3. Text-Freigabe-Gate: Export erst, wenn die Texte freigegeben sind
  4. Content-Studio fragt Typ und Funnel-Stufe mit ab

Quelle: die von der Artifact-Leseaktion gespeicherte HTML.
Ziel:   outputs/cockpit/mlb-cockpit.html (ohne den Publish-Rahmen).

Aufruf:
  python scripts/cockpit/patch-karussell.py <quelle.html>
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ZIEL = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"


def ersetze(text, alt, neu, name):
    if alt not in text:
        sys.exit("FEHLER: Textstelle '%s' nicht gefunden — Vorlage hat sich geaendert." % name)
    if text.count(alt) != 1:
        sys.exit("FEHLER: Textstelle '%s' kommt %dx vor, erwartet 1x." % (name, text.count(alt)))
    print("  ersetzt: %s" % name)
    return text.replace(alt, neu, 1)


# ---------------------------------------------------------------- 1 STRUKTUREN

STRUKTUREN_ALT_START = "  var STRUKTUREN = {"
STRUKTUREN_ALT_ENDE = "\n  };\n\n  /* =========================================================\n     State + Speicherung"

STRUKTUREN_NEU = '''  /* Die vier Karussell-Typen. Jeder Typ hat eine feste Dramaturgie —
     das ist der Unterschied zwischen einem Karussell und sechs Textkacheln. */
  var TYPEN = {
    listicle:  "Listicle · X Dinge, die Y",
    story:     "Storytelling · persoenliche Geschichte",
    edukativ:  "Edukativ · etwas erklaeren",
    kontrovers:"Kontroverser Take · fuer Reichweite"
  };

  var FUNNEL = {
    TOF: "TOF · Reichweite",
    MOF: "MOF · Vertrauen",
    BOF: "BOF · Verkauf"
  };

  var TYP_HINWEIS = {
    listicle: "Der einfachste Typ, weil die Struktur schon steht. Pro Slide genau ein Punkt: Headline ist der Punkt selbst, Body erklaert ihn in ein bis zwei Saetzen.",
    story: "Hoechste Bindung, weil die Leute bis zum Ende wischen. Jede Slide muss so enden, dass man die naechste lesen will. Braucht eine echte Geschichte, keine erfundene.",
    edukativ: "Der Typ, der am meisten gespeichert wird, und Speicherungen bringen am laengsten Reichweite. Ohne Fachbegriffe, oder den Fachbegriff sofort erklaeren.",
    kontrovers: "Groesste Reichweite, groesstes Risiko. Die vorletzte Slide ist die Nuancierung, also wo du die Gegenposition verstehst. Genau die sorgt fuer Diskussion statt Streit. Nie weglassen."
  };

  var FUNNEL_HINWEIS = {
    TOF: "Reichweite. Kein Angebot, keine Preise. Der Post soll geteilt werden.",
    MOF: "Vertrauen. Du zeigst, wie du denkst und arbeitest. Keyword-Aufruf am Schluss.",
    BOF: "Verkauf gehoert nicht in den Feed, sondern in Stories und Mails. Wenn du hier BOF waehlst, halte das Angebot im Karussell trotzdem raus und verkauf ueber den Keyword-Weg."
  };

  var STRUKTUREN = {
    listicle: {
      name: "Listicle (7 Slides)",
      typ: "listicle", funnel: "TOF",
      slides: [
        { layout: "hook",  headline: "4 Saetze, die dich als Networkerin sofort verraten", body: "" },
        { layout: "text",  headline: "1. Schau mal, was ich gefunden habe", body: "Klingt harmlos, ist aber der Satz, bei dem jede weiss, was gleich kommt. Sag stattdessen, welches Problem du geloest hast." },
        { layout: "text",  headline: "2. Ich hab da was fuer dich", body: "Fuer wen genau, und wofuer? Wer das nicht dazusagt, verkauft an alle und damit an niemanden." },
        { layout: "text",  headline: "3. Das musst du selbst erleben", body: "Das ist keine Antwort, das ist ein Ausweichen. Erzaehl, was sich bei dir konkret veraendert hat." },
        { layout: "text",  headline: "4. Melde dich, wenn du mehr wissen willst", body: "Der Ball liegt bei ihr, und da bleibt er liegen. Gib ihr einen naechsten Schritt, den sie in zehn Sekunden machen kann." },
        { layout: "split", headline: "Was stattdessen wirkt", body: "Ein Thema, das dir gehoert, und eine Sprache, die aus deinem Alltag kommt statt aus dem Teamchat." },
        { layout: "cta",   headline: "Willst du deins finden?", body: "Kommentiere mit dem Keyword und ich schicke dir die Anleitung." }
      ]
    },
    story: {
      name: "Storytelling (7 Slides)",
      typ: "story", funnel: "MOF",
      slides: [
        { layout: "bild",  headline: "Der Abend, an dem ich alles hingeworfen haette", body: "" },
        { layout: "text",  headline: "Wo ich stand", body: "Warmmarkt abgegrast, Liste leer, und trotzdem jeden Tag drei Stunden im Handy. Und dann kam der Satz, der mir den Rest gab." },
        { layout: "text",  headline: "Was ich mir eingeredet habe", body: "Ich muss nur konsequenter sein. Mehr posten, mehr anschreiben, frueher aufstehen. Es lag nie am Fleiss." },
        { layout: "text",  headline: "Der Moment, an dem es kippte", body: "Eine Frau schrieb mir wegen etwas, wofuer ich gar nicht geworben hatte. Da habe ich gemerkt, wofuer ich eigentlich stehe." },
        { layout: "text",  headline: "Was sich geaendert hat", body: "Ich habe aufgehoert, Produkte zu zeigen, und angefangen, mein Thema zu besetzen. Das Produkt kommt seitdem von allein vor." },
        { layout: "text",  headline: "Was ich heute anders mache", body: "Ich frage mich vor jedem Post nur noch eins: wofuer soll man mich fragen? Alles, was darauf nicht einzahlt, faellt weg." },
        { layout: "cta",   headline: "Wenn du gerade da stehst", body: "Schreib mir das Keyword und ich zeige dir den ersten Schritt." }
      ]
    },
    edukativ: {
      name: "Edukativ (7 Slides)",
      typ: "edukativ", funnel: "MOF",
      slides: [
        { layout: "hook",  headline: "Warum dein Content keine Anfragen bringt", body: "" },
        { layout: "text",  headline: "Der Denkfehler", body: "Du postest ueber dein Produkt. Deine Wunschkundin sucht aber nach ihrem Problem, und das kommt bei dir nicht vor." },
        { layout: "text",  headline: "Schritt 1: Das Problem benennen", body: "Schreib in ihren Worten auf, was sie abends denkt. Nicht in deinen Fachworten, sondern so, wie sie es einer Freundin sagen wuerde." },
        { layout: "text",  headline: "Schritt 2: Ein Ergebnis versprechen", body: "Niemand sucht Mentalload-Management. Alle suchen einen Abend, an dem nichts mehr offen ist." },
        { layout: "text",  headline: "Schritt 3: Einen Schritt zeigen", body: "Gib etwas mit, das sie heute umsetzen kann. Wer einmal etwas von dir umgesetzt hat, fragt beim naechsten Mal dich." },
        { layout: "text",  headline: "In einem Satz", body: "Content bringt Anfragen, wenn er ihr Problem loest, nicht wenn er dein Produkt zeigt." },
        { layout: "cta",   headline: "Hol dir den Fahrplan", body: "Kommentiere mit dem Keyword und ich schicke dir die Schritt-fuer-Schritt-Anleitung." }
      ]
    },
    kontrovers: {
      name: "Kontroverser Take (7 Slides)",
      typ: "kontrovers", funnel: "TOF",
      slides: [
        { layout: "hook",  headline: "Mehr posten war noch nie dein Problem", body: "" },
        { layout: "text",  headline: "Was alle raten", body: "Sei konsequent, poste taeglich, bleib dran. Als waere Sichtbarkeit eine Frage der Menge." },
        { layout: "text",  headline: "Warum das nicht aufgeht", body: "Dreissig Posts ueber dreissig Themen ergeben kein Bild von dir. Man erinnert sich an Menschen, die fuer eine Sache stehen." },
        { layout: "text",  headline: "Was wirklich fehlt", body: "Nicht Frequenz, sondern eine Entscheidung. Wofuer sollen dich Leute fragen, ohne dass du es dazusagen musst?" },
        { layout: "text",  headline: "Was ich stattdessen mache", body: "Weniger Posts, aber alle auf dieselbe Frage. Nach ein paar Wochen kamen die Anfragen von allein." },
        { layout: "text",  headline: "Wo die anderen recht haben", body: "Ohne Regelmaessigkeit passiert nichts, das stimmt. Nur ist sie die Bedingung und nicht die Loesung. Wer schon ein Thema hat, fuer die ist taeglich posten goldrichtig." },
        { layout: "cta",   headline: "Wie siehst du das?", body: "Schreib es mir in die Kommentare, ich lese alles selbst." }
      ]
    },
    problem: {
      name: "Problem zu Loesung (5 Slides)",
      typ: "edukativ", funnel: "MOF",
      slides: [
        { layout: "hook",  headline: "Warum deine Produktposts niemanden abholen", body: "" },
        { layout: "text",  headline: "Das Muster", body: "Du zeigst das Produkt. Deine Community sieht Werbung. Und scrollt weiter, weil nichts ueber sie selbst darin vorkommt." },
        { layout: "text",  headline: "Der Denkfehler", body: "Nicht das Produkt verkauft, sondern das Problem, das du sichtbar loest. Das Produkt ist nur der Weg dorthin." },
        { layout: "split", headline: "So drehst du es um", body: "Schreibe zuerst auf, wofuer deine Wunschkundin dich fragen soll. Erst danach ueberlegst du, welches Produkt in dieser Antwort vorkommt." },
        { layout: "cta",   headline: "Hol dir den Fahrplan", body: "Kommentiere mit dem Keyword und ich schicke dir die Schritt-fuer-Schritt-Anleitung." }
      ]
    },
    schritte: {
      name: "Schritt fuer Schritt (6 Slides)",
      typ: "listicle", funnel: "MOF",
      slides: [
        { layout: "hook",  headline: "In 4 Schritten zu deinem eigenen Thema", body: "" },
        { layout: "text",  headline: "Schritt 1", body: "Schreib auf, wofuer dich Leute schon heute fragen, ohne dass du dafuer wirbst." },
        { layout: "text",  headline: "Schritt 2", body: "Streiche alles, was du nur kannst, aber nicht gerne machst." },
        { layout: "text",  headline: "Schritt 3", body: "Formuliere ein Ergebnis, kein Thema. Niemand sucht Mentalload, alle suchen ruhige Abende." },
        { layout: "text",  headline: "Schritt 4", body: "Poste dreissig Tage lang nur dazu und schau, was zurueckkommt." },
        { layout: "cta",   headline: "Willst du das begleitet machen?", body: "Kommentiere mit deinem Keyword, dann schicke ich dir die Details." }
      ]
    }
  };'''


def main():
    if len(sys.argv) < 2:
        sys.exit("Bitte die gespeicherte Artifact-HTML als Argument angeben.")
    quelle = Path(sys.argv[1])
    if not quelle.exists():
        sys.exit("Quelle nicht gefunden: %s" % quelle)

    t = quelle.read_text(encoding="utf-8")
    print("Quelle: %s (%d Zeichen)" % (quelle.name, len(t)))

    # --- Publish-Rahmen abstreifen (wird beim Veroeffentlichen neu gesetzt)
    i = t.find("<body>")
    if i == -1:
        sys.exit("Kein <body> gefunden.")
    t = t[i + len("<body>"):]
    t = t.rstrip()
    for ende in ("</body></html>", "</body>\n</html>", "</html>"):
        if t.endswith(ende):
            t = t[: -len(ende)].rstrip()
            break
    print("Publish-Rahmen entfernt.")

    # --- 1) STRUKTUREN ersetzen
    a = t.find(STRUKTUREN_ALT_START)
    b = t.find(STRUKTUREN_ALT_ENDE, a)
    if a == -1 or b == -1:
        sys.exit("STRUKTUREN-Block nicht gefunden.")
    t = t[:a] + STRUKTUREN_NEU + t[b + len("\n  };"):]
    print("  ersetzt: STRUKTUREN (4 Typen + Funnel + Hinweise)")

    # --- 2) CSS fuer die Textliste
    t = ersetze(
        t,
        "  @media (max-width: 860px) {\n    .shell { grid-template-columns: 1fr; }",
        """  /* Text-Freigabe */
  .textliste {
    white-space: pre-wrap; font-family: var(--body); font-size: 13px; line-height: 1.62;
    background: var(--ground); border: 1px solid var(--line); border-radius: 8px;
    padding: 14px 16px; max-height: 340px; overflow-y: auto; margin: 0;
  }
  .gate { border-left: 3px solid var(--orange); }
  .gate.frei { border-left-color: var(--good); }

  @media (max-width: 860px) {
    .shell { grid-template-columns: 1fr; }""",
        "CSS Textliste")

    # --- 3) neuesKarussell: Typ, Funnel, Freigabe-Status mitschreiben
    t = ersetze(
        t,
        """    var car = {
      id: uid("kar"),
      name: s ? s.name.replace(/\\s*\\(.*\\)$/, "") : "Neues Karussell",
      brand: "mlb_dark",
      handle: BRANDS.mlb_dark.handle,
      caption: "",""",
        """    var car = {
      id: uid("kar"),
      name: s ? s.name.replace(/\\s*\\(.*\\)$/, "") : "Neues Karussell",
      brand: "mlb_dark",
      handle: BRANDS.mlb_dark.handle,
      typ: s ? s.typ : "listicle",
      funnel: s ? s.funnel : "TOF",
      textfrei: false,
      caption: "",""",
        "neuesKarussell")

    # --- 4) saveCarousel: neue Felder mitspeichern
    t = ersetze(
        t,
        """      db.collection("karussells").doc(car.id).set({
        name: car.name, brand: car.brand, handle: car.handle,
        slides: car.slides, caption: car.caption || "", updatedAt: car.updatedAt
      })""",
        """      db.collection("karussells").doc(car.id).set({
        name: car.name, brand: car.brand, handle: car.handle,
        typ: car.typ || "listicle", funnel: car.funnel || "TOF",
        textfrei: !!car.textfrei,
        slides: car.slides, caption: car.caption || "", updatedAt: car.updatedAt
      })""",
        "saveCarousel")

    # --- 5) Karussells aus der Datenbank: neue Felder uebernehmen
    t = ersetze(
        t,
        """          var car = { id: doc.id, name: d0.name || "Karussell", brand: d0.brand || "mlb_dark", handle: d0.handle || "", caption: d0.caption || "", slides: d0.slides || [], updatedAt: d0.updatedAt || "" };""",
        """          var car = { id: doc.id, name: d0.name || "Karussell", brand: d0.brand || "mlb_dark", handle: d0.handle || "", typ: d0.typ || "listicle", funnel: d0.funnel || "TOF", textfrei: !!d0.textfrei, caption: d0.caption || "", slides: d0.slides || [], updatedAt: d0.updatedAt || "" };""",
        "Karussell aus DB")

    # --- 6) Editbar: Typ + Funnel-Stufe, Export gesperrt bis freigegeben
    t = ersetze(
        t,
        """        '<div class="field" style="flex:1 1 240px"><label for="handlein">Handle auf den Slides</label><input id="handlein" value="' + esc(car.handle || "") + '" placeholder="leer lassen für kein Handle"></div>' +
        '<button class="btn" id="dupbtn">Duplizieren</button>' +
        '<button class="btn" id="delbtn">Löschen</button>' +
        '<button class="btn primary" id="exportbtn">Alle Slides exportieren</button>' +
      '</div>' +
      '<div class="slidestrip" id="strip"></div>' +""",
        """        '<div class="field"><label for="typpick">Typ</label><select id="typpick"></select></div>' +
        '<div class="field"><label for="funnelpick">Funnel-Stufe</label><select id="funnelpick"></select></div>' +
        '<div class="field" style="flex:1 1 240px"><label for="handlein">Handle auf den Slides</label><input id="handlein" value="' + esc(car.handle || "") + '" placeholder="leer lassen für kein Handle"></div>' +
        '<button class="btn" id="dupbtn">Duplizieren</button>' +
        '<button class="btn" id="delbtn">Löschen</button>' +
        '<button class="btn primary" id="exportbtn"' + (car.textfrei ? "" : " disabled") + '>Alle Slides exportieren</button>' +
      '</div>' +
      '<div class="panel gate' + (car.textfrei ? " frei" : "") + '" style="margin-bottom:16px">' +
        '<h2>Schritt 1: Texte prüfen</h2>' +
        '<div class="note" id="typnote" style="margin-bottom:10px"></div>' +
        '<pre class="textliste" id="textliste"></pre>' +
        '<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:12px">' +
          '<button class="btn" id="textcopy">Texte kopieren</button>' +
          '<button class="btn' + (car.textfrei ? "" : " primary") + '" id="freigabebtn">' +
            (car.textfrei ? "Freigabe zurücknehmen" : "Texte freigeben") + '</button>' +
          '<span class="note" id="gatenote"></span>' +
        '</div>' +
      '</div>' +
      '<div class="slidestrip" id="strip"></div>' +""",
        "Editbar + Freigabe-Panel")

    # --- 7) Verdrahtung der neuen Bedienelemente
    t = ersetze(
        t,
        """    ed.querySelector("#carname").oninput = function () { car.name = this.value; saveCarousel(car); };""",
        """    var tp = ed.querySelector("#typpick");
    Object.keys(TYPEN).forEach(function (k) {
      var o = document.createElement("option");
      o.value = k; o.textContent = TYPEN[k];
      if ((car.typ || "listicle") === k) o.selected = true;
      tp.appendChild(o);
    });
    tp.onchange = function () { car.typ = tp.value; saveCarousel(car); render(); };

    var fp = ed.querySelector("#funnelpick");
    Object.keys(FUNNEL).forEach(function (k) {
      var o = document.createElement("option");
      o.value = k; o.textContent = FUNNEL[k];
      if ((car.funnel || "TOF") === k) o.selected = true;
      fp.appendChild(o);
    });
    fp.onchange = function () { car.funnel = fp.value; saveCarousel(car); render(); };

    // Text-Freigabe: erst lesen, dann bauen. Das ist die Regel, die am meisten Zeit spart.
    var tl = ed.querySelector("#textliste");
    function textlisteFuellen() {
      tl.textContent = car.slides.map(function (s, i) {
        var kopf = "Slide " + (i + 1) + (i === 0 ? " (Hook)" : (s.layout === "cta" ? " (CTA)" : "")) + ":";
        var zeilen = [kopf, s.headline || "—"];
        if (s.body) zeilen.push(s.body);
        if (s.keyword) zeilen.push("Keyword: " + s.keyword.toUpperCase());
        return zeilen.join("\\n");
      }).join("\\n\\n");
    }
    textlisteFuellen();

    ed.querySelector("#typnote").textContent =
      (TYP_HINWEIS[car.typ || "listicle"] || "") + " " + (FUNNEL_HINWEIS[car.funnel || "TOF"] || "");

    ed.querySelector("#gatenote").textContent = car.textfrei
      ? "Freigegeben. Der Export ist offen."
      : "Solange die Texte nicht freigegeben sind, bleibt der Export gesperrt.";

    ed.querySelector("#textcopy").onclick = function () {
      var ta = document.createElement("textarea");
      ta.value = tl.textContent;
      ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) {}
      ta.remove();
      toast(ok ? "Texte kopiert." : "Markier den Text und kopier ihn von Hand.");
    };

    ed.querySelector("#freigabebtn").onclick = function () {
      car.textfrei = !car.textfrei;
      saveCarousel(car);
      render();
      toast(car.textfrei ? "Texte freigegeben. Jetzt kannst du bauen." : "Freigabe zurückgenommen.");
    };

    ed.querySelector("#carname").oninput = function () { car.name = this.value; saveCarousel(car); };""",
        "Verdrahtung Typ/Funnel/Freigabe")

    # --- 8) Textaenderung hebt die Freigabe wieder auf
    t = ersetze(
        t,
        """    var h = document.createElement("textarea");
    h.rows = 2; h.placeholder = "Headline"; h.value = slide.headline || "";
    h.oninput = function () { slide.headline = h.value; saveCarousel(car); draw(); };
    body.appendChild(h);

    var t = document.createElement("textarea");
    t.rows = 3; t.placeholder = "Fliesstext"; t.value = slide.body || "";
    t.oninput = function () { slide.body = t.value; saveCarousel(car); draw(); };
    body.appendChild(t);""",
        """    // Wer den Text aendert, hebt die Freigabe auf — sonst exportierst du
    // eine Fassung, die du nie gelesen hast.
    function freigabeAufheben() {
      if (!car.textfrei) return;
      car.textfrei = false;
      saveCarousel(car);
      toast("Text geändert, Freigabe aufgehoben.");
      setTimeout(render, 300);
    }

    var h = document.createElement("textarea");
    h.rows = 2; h.placeholder = "Headline"; h.value = slide.headline || "";
    h.oninput = function () { slide.headline = h.value; saveCarousel(car); draw(); freigabeAufheben(); };
    body.appendChild(h);

    var t = document.createElement("textarea");
    t.rows = 3; t.placeholder = "Fliesstext"; t.value = slide.body || "";
    t.oninput = function () { slide.body = t.value; saveCarousel(car); draw(); freigabeAufheben(); };
    body.appendChild(t);""",
        "Freigabe faellt bei Textaenderung")

    # --- 9) Content-Studio: Typ und Funnel-Stufe mitfragen
    t = ersetze(
        t,
        """  var studioForm = { idee: "", ziel: "Vertrauen", archetyp: "Zögerliche Zoe", angebot: "", phase: "", format: "Karussell" };""",
        """  var studioForm = { idee: "", ziel: "Vertrauen", archetyp: "Zögerliche Zoe", angebot: "", phase: "", format: "Karussell", typ: "listicle", funnel: "TOF" };""",
        "studioForm")

    t = ersetze(
        t,
        """    feld("Was soll entstehen", sel("format", ["Karussell", "Story-Sequenz", "Nur Hooks", "Nur Caption"]));""",
        """    feld("Was soll entstehen", sel("format", ["Karussell", "Story-Sequenz", "Nur Hooks", "Nur Caption"]));

    var typSel = document.createElement("select");
    Object.keys(TYPEN).forEach(function (k) {
      var op = document.createElement("option");
      op.value = k; op.textContent = TYPEN[k];
      if (studioForm.typ === k) op.selected = true;
      typSel.appendChild(op);
    });
    var typHint = document.createElement("div");
    typHint.className = "note";
    typHint.textContent = TYP_HINWEIS[studioForm.typ] || "";
    typSel.onchange = function () {
      studioForm.typ = typSel.value;
      typHint.textContent = TYP_HINWEIS[studioForm.typ] || "";
    };
    feld("Karussell-Typ", typSel);
    sf.appendChild(typHint);

    var funSel = document.createElement("select");
    Object.keys(FUNNEL).forEach(function (k) {
      var op = document.createElement("option");
      op.value = k; op.textContent = FUNNEL[k];
      if (studioForm.funnel === k) op.selected = true;
      funSel.appendChild(op);
    });
    var funHint = document.createElement("div");
    funHint.className = "note";
    funHint.textContent = FUNNEL_HINWEIS[studioForm.funnel] || "";
    funSel.onchange = function () {
      studioForm.funnel = funSel.value;
      funHint.textContent = FUNNEL_HINWEIS[studioForm.funnel] || "";
    };
    feld("Funnel-Stufe", funSel);
    sf.appendChild(funHint);""",
        "Studio-Felder Typ/Funnel")

    # --- 10) Studio-Prompt: Typ-Dramaturgie und Funnel-Stufe mitgeben
    t = ersetze(
        t,
        """    if (f.format === "Karussell") {
      auftrag = "Baue ein Instagram-Karussell mit sechs bis acht Slides. Slide eins ist die Hook, dann Aufbau, dann ein klarer Aufruf am Schluss. \"""",
        """    var TYP_AUFTRAG = {
      listicle: "Bau es als Listicle. Slide eins ist eine starke Headline mit einer Zahl, die neugierig macht. Danach pro Slide genau ein Punkt: die Headline IST der Punkt, der Body erklaert ihn in ein bis zwei Saetzen. Letzte Slide kurzer klarer Aufruf.",
      story: "Bau es als persoenliche Geschichte. Slide eins ist ein Hook, der neugierig macht. Die Slides danach erzaehlen die Geschichte in Etappen wie eine Mini-Serie, und jede Slide endet so, dass man die naechste lesen will. Die vorletzte Slide sagt, was sie daraus mitgenommen hat und heute anders macht. Ton wie zu einer Freundin. Erfinde nichts dazu.",
      edukativ: "Bau es als Erklaerung. Slide eins stellt eine Frage oder benennt ein Problem. Danach Schritt fuer Schritt, klar und ohne Fachbegriffe, oder den Fachbegriff sofort erklaeren. Die vorletzte Slide fasst alles in einem Satz zusammen.",
      kontrovers: "Bau es als kontroversen Take. Slide eins ist eine provokante Headline, die zum Widerspruch einlaedt. Danach die Argumentation Schritt fuer Schritt mit konkreten Beispielen. Die vorletzte Slide ist die Nuancierung, also wo die Gegenposition recht hat. Diese Slide ist Pflicht und darf nicht fehlen, sie sorgt fuer Diskussion statt Streit."
    };
    var FUNNEL_AUFTRAG = {
      TOF: "Funnel-Stufe TOF: Der Post soll Reichweite bringen und geteilt werden. Kein Angebot, keine Preise, kein Programmname.",
      MOF: "Funnel-Stufe MOF: Der Post soll Vertrauen aufbauen und zeigen, wie sie denkt und arbeitet. Am Schluss ein Keyword-Aufruf.",
      BOF: "Funnel-Stufe BOF: Verkauft wird bei ihr nicht im Feed, sondern in Stories und Mails. Halte Angebot und Preis aus den Slides raus und fuehre ueber den Keyword-Aufruf zum Gespraech."
    };

    if (f.format === "Karussell") {
      auftrag = (TYP_AUFTRAG[f.typ] || TYP_AUFTRAG.listicle) + "\\n" + (FUNNEL_AUFTRAG[f.funnel] || "") + "\\n\\n" +
        "Baue ein Instagram-Karussell mit sechs bis acht Slides. \"""",
        "Studio-Prompt Typ/Funnel")

    # --- 11) Studio-Ergebnis: Typ und Funnel ans neue Karussell weiterreichen
    t = ersetze(
        t,
        """        var car = {
          id: uid("kar"), name: r.name || studioForm.idee.slice(0, 40), brand: "mlb_dark",
          handle: BRANDS.mlb_dark.handle, caption: r.caption || "",""",
        """        var car = {
          id: uid("kar"), name: r.name || studioForm.idee.slice(0, 40), brand: "mlb_dark",
          handle: BRANDS.mlb_dark.handle, caption: r.caption || "",
          typ: studioForm.typ, funnel: studioForm.funnel, textfrei: false,""",
        "Studio-Ergebnis Karussell")

    t = ersetze(
        t,
        """        toast("Karussell angelegt, jetzt nur noch Bilder rein.");""",
        """        toast("Karussell angelegt. Erst die Texte prüfen und freigeben, dann bauen.");""",
        "Toast nach Anlegen")

    # --- 12) Editor-Einleitung an den neuen Ablauf anpassen
    t = ersetze(
        t,
        """      '<p>Text eintippen, Bild hochladen, zurechtschieben, exportieren. Deine Marke ist fest eingebaut, du musst nie wieder ein Template duplizieren.</p></div>' +""",
        """      '<p>Erst die Texte lesen und freigeben, dann Bilder rein und exportieren. Der Export bleibt gesperrt, bis die Texte stehen — das spart dir die Runde, in der du alles nochmal baust.</p></div>' +""",
        "Editor-Einleitung")

    # --- 13) Blotato-Freigabe: Datum, Profil, Go-Knopf
    t = ersetze(
        t,
        """        '<div class="hooklist" id="hooklist"></div>' +
      '</div>';""",
        """        '<div class="hooklist" id="hooklist"></div>' +
      '</div>' +
      '<div class="panel gate' + (blo(car).status === "wartet" ? " frei" : "") + '" style="margin-top:18px">' +
        '<h2>Schritt 2: An Blotato geben</h2>' +
        '<div class="note" id="blonote" style="margin-bottom:10px"></div>' +
        '<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end">' +
          '<div class="field"><label for="blodatum">Datum</label><input type="date" id="blodatum" value="' + esc(blo(car).datum || "") + '"></div>' +
          '<div class="field"><label for="blozeit">Uhrzeit</label><input type="time" id="blozeit" value="' + esc(blo(car).zeit || "07:30") + '"></div>' +
          '<div class="field"><label for="bloprofil">Profil</label><select id="bloprofil">' +
            '<option value="mentoring"' + (blo(car).profil === "doterra" ? "" : " selected") + '>Instagram Mentoring</option>' +
            '<option value="doterra"' + (blo(car).profil === "doterra" ? " selected" : "") + '>Instagram doTERRA</option>' +
          '</select></div>' +
          '<button class="btn primary" id="blobtn">Für Blotato freigeben</button>' +
          '<button class="btn ghost" id="blozurueck" hidden>Freigabe zurückziehen</button>' +
        '</div>' +
      '</div>';""",
        "Blotato-Panel")

    t = ersetze(
        t,
        """    renderStrip(ed.querySelector("#strip"), car);
    setupHooks(ed, car);
  }""",
        """    renderStrip(ed.querySelector("#strip"), car);
    setupHooks(ed, car);
    setupBlotato(ed, car);
  }

  /* Freigabe-Daten eines Karussells, mit Vorbelegung. */
  function blo(car) {
    return car.blotato || (car.blotato = { datum: "", zeit: "07:30", profil: "mentoring", status: "" });
  }

  /* Eine Slide als JPEG, klein genug fuer ein Dokument. */
  function slideJpeg(car, slide, i, cb) {
    var cv = document.createElement("canvas");
    renderSlide(cv, slide, car, i, car.slides.length);
    setTimeout(function () {
      var q = 0.92;
      var out = cv.toDataURL("image/jpeg", q);
      while (out.length > 700000 && q > 0.45) { q -= 0.08; out = cv.toDataURL("image/jpeg", q); }
      cb(out);
    }, 320);
  }

  function setupBlotato(ed, car) {
    var b = blo(car);
    var note = ed.querySelector("#blonote");
    var btn = ed.querySelector("#blobtn");
    var zurueck = ed.querySelector("#blozurueck");
    var datum = ed.querySelector("#blodatum");
    var zeit = ed.querySelector("#blozeit");
    var profil = ed.querySelector("#bloprofil");

    function speichern() {
      b.datum = datum.value; b.zeit = zeit.value; b.profil = profil.value;
      saveCarousel(car);
    }
    datum.onchange = zeit.onchange = profil.onchange = speichern;

    if (!db) {
      note.textContent = "Die Freigabe braucht die Verbindung zur Datenbank. Öffne das Cockpit über den Link, dann geht es.";
      btn.disabled = true;
      return;
    }
    if (!car.textfrei) {
      note.textContent = "Erst die Texte oben freigeben. Was du nicht gelesen hast, geht auch nicht raus.";
      btn.disabled = true;
      return;
    }
    if (b.status === "wartet") {
      note.textContent = "Freigegeben für " + (b.datum || "kein Datum") + " um " + (b.zeit || "") +
        ", Profil " + (b.profil === "doterra" ? "doTERRA" : "Mentoring") +
        ". Sag es mir im Chat, dann lade ich die Folien hoch und plane den Beitrag ein.";
      btn.textContent = "Folien neu ablegen";
      zurueck.hidden = false;
      zurueck.onclick = function () {
        b.status = ""; saveCarousel(car);
        db.collection("freigaben").doc(car.id).set({
          name: car.name, status: "zurueckgezogen", updatedAt: new Date().toISOString()
        }).catch(function () {});
        render();
        toast("Freigabe zurückgezogen.");
      };
    } else if (b.status === "geplant") {
      note.textContent = "Eingeplant bei Blotato für " + (b.datum || "") + " um " + (b.zeit || "") + ".";
      btn.disabled = true;
      return;
    } else {
      note.textContent = "Datum und Uhrzeit setzen, dann freigeben. Dabei werden die fertigen Folien abgelegt — genau so, wie sie hier aussehen.";
    }

    btn.onclick = function () {
      if (!datum.value) { datum.focus(); toast("Setz zuerst ein Datum."); return; }
      if (!(car.caption || "").trim()) { toast("Ohne Caption kein Beitrag. Schreib sie oben rein."); return; }
      speichern();
      btn.disabled = true;
      var gesamt = car.slides.length;
      var i = 0;
      var basis = "freigaben/" + car.id;

      function naechste() {
        if (i >= gesamt) {
          var wann = new Date(datum.value + "T" + (zeit.value || "07:30"));
          db.collection("freigaben").doc(car.id).set({
            name: car.name,
            caption: car.caption || "",
            profil: profil.value,
            datum: datum.value,
            zeit: zeit.value || "07:30",
            zeitpunktISO: isNaN(wann) ? "" : wann.toISOString(),
            typ: car.typ || "",
            funnel: car.funnel || "",
            anzahl: gesamt,
            status: "wartet",
            updatedAt: new Date().toISOString()
          }).then(function () {
            b.status = "wartet";
            saveCarousel(car);
            btn.disabled = false;
            render();
            toast("Freigegeben. Sag mir im Chat Bescheid, dann geht es raus.");
          }).catch(function () {
            btn.disabled = false;
            btn.textContent = "Für Blotato freigeben";
            toast("Das Ablegen hat nicht geklappt.");
          });
          return;
        }
        var nr = i++;
        btn.textContent = "lege Folie " + (nr + 1) + " von " + gesamt + " ab …";
        slideJpeg(car, car.slides[nr], nr, function (dataUrl) {
          db.doc(basis).collection("bilder")
            .doc("slide-" + String(nr + 1).padStart(2, "0"))
            .set({ dataUrl: dataUrl, nr: nr + 1 })
            .then(naechste)
            .catch(function () {
              btn.disabled = false;
              btn.textContent = "Für Blotato freigeben";
              toast("Folie " + (nr + 1) + " liess sich nicht ablegen.");
            });
        });
      }
      naechste();
    };
  }""",
        "Blotato-Verdrahtung")

    t = ersetze(
        t,
        """        typ: car.typ || "listicle", funnel: car.funnel || "TOF",
        textfrei: !!car.textfrei,""",
        """        typ: car.typ || "listicle", funnel: car.funnel || "TOF",
        textfrei: !!car.textfrei, blotato: car.blotato || null,""",
        "saveCarousel Blotato")

    t = ersetze(
        t,
        """typ: d0.typ || "listicle", funnel: d0.funnel || "TOF", textfrei: !!d0.textfrei,""",
        """typ: d0.typ || "listicle", funnel: d0.funnel || "TOF", textfrei: !!d0.textfrei, blotato: d0.blotato || null,""",
        "DB-Laden Blotato")

    # --- 14) Reel-Freigabe im Cockpit (derselbe Weg wie beim Karussell)
    t = ersetze(
        t,
        """        '<button class="btn" id="stdel">Löschen</button>' +""",
        """        '<button class="btn" id="stdel">Löschen</button>' +""",
        "Platzhalter Story (unveraendert)")

    t = ersetze(
        t,
        """    var del = document.createElement("button");
    del.className = "btn ghost";
    del.textContent = "Dieses Reel löschen";""",
        """    // --- Freigabe fuer Blotato, wie beim Karussell
    var bloBox = document.createElement("div");
    bloBox.className = "panel gate" + (bloR(r).status === "wartet" ? " frei" : "");
    bloBox.style.marginTop = "18px";
    bloBox.innerHTML =
      '<h2>An Blotato geben</h2>' +
      '<div class="note" id="rblonote" style="margin-bottom:10px"></div>' +
      '<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end">' +
        '<div class="field"><label for="rblodatum">Datum</label>' +
          '<input type="date" id="rblodatum" value="' + esc(bloR(r).datum || "") + '"></div>' +
        '<div class="field"><label for="rblozeit">Uhrzeit</label>' +
          '<input type="time" id="rblozeit" value="' + esc(bloR(r).zeit || "18:00") + '"></div>' +
        '<div class="field"><label for="rbloprofil">Profil</label><select id="rbloprofil">' +
          '<option value="mentoring"' + (bloR(r).profil === "doterra" ? "" : " selected") + '>Instagram Mentoring</option>' +
          '<option value="doterra"' + (bloR(r).profil === "doterra" ? " selected" : "") + '>Instagram doTERRA</option>' +
        '</select></div>' +
        '<button class="btn primary" id="rblobtn">Für Blotato freigeben</button>' +
        '<button class="btn ghost" id="rblozurueck" hidden>Freigabe zurückziehen</button>' +
      '</div>';
    rt.appendChild(bloBox);
    setupBlotatoReel(bloBox, r);

    var del = document.createElement("button");
    del.className = "btn ghost";
    del.textContent = "Dieses Reel löschen";""",
        "Reel-Blotato-Panel")

    t = ersetze(
        t,
        """  function komprimiereDataUrl(dataUrl, cb) {""",
        """  /* Freigabe-Daten eines Reels. */
  function bloR(r) {
    return r.blotato || (r.blotato = { datum: "", zeit: "18:00", profil: "mentoring", status: "" });
  }

  function setupBlotatoReel(box, r) {
    var b = bloR(r);
    var note = box.querySelector("#rblonote");
    var btn = box.querySelector("#rblobtn");
    var zurueck = box.querySelector("#rblozurueck");
    var datum = box.querySelector("#rblodatum");
    var zeit = box.querySelector("#rblozeit");
    var profil = box.querySelector("#rbloprofil");

    function speichern() {
      b.datum = datum.value; b.zeit = zeit.value; b.profil = profil.value;
      saveReel(r);
    }
    datum.onchange = zeit.onchange = profil.onchange = speichern;

    if (!db) {
      note.textContent = "Die Freigabe braucht die Verbindung zur Datenbank. Öffne das Cockpit über den Link.";
      btn.disabled = true;
      return;
    }
    if (!r.videodatei) {
      note.textContent = "Für dieses Reel ist noch keine fertige Videodatei hinterlegt. " +
        "Die trägt Claude ein, sobald das Reel geschnitten und gerendert ist.";
      btn.disabled = true;
      return;
    }
    if (b.status === "wartet") {
      note.textContent = "Freigegeben für " + (b.datum || "kein Datum") + " um " + (b.zeit || "") +
        ". Sag es mir im Chat, dann lade ich Video und Cover hoch und plane den Beitrag ein.";
      btn.textContent = "Cover neu ablegen";
      zurueck.hidden = false;
      zurueck.onclick = function () {
        b.status = ""; saveReel(r);
        db.collection("freigaben").doc(r.id).set({
          name: r.name, typ: "reel", status: "zurueckgezogen",
          updatedAt: new Date().toISOString()
        }).catch(function () {});
        render();
        toast("Freigabe zurückgezogen.");
      };
    } else if (b.status === "geplant") {
      note.textContent = "Eingeplant bei Blotato für " + (b.datum || "") + " um " + (b.zeit || "") + ".";
      btn.disabled = true;
      return;
    } else {
      note.textContent = "Datum und Uhrzeit setzen, dann freigeben. Dabei wird das Titelbild " +
        "als Cover abgelegt — genau so, wie es hier aussieht.";
    }

    btn.onclick = function () {
      if (!datum.value) { datum.focus(); toast("Setz zuerst ein Datum."); return; }
      if (!(r.caption || "").trim()) { toast("Ohne Caption kein Beitrag. Schreib sie oben rein."); return; }
      speichern();
      btn.disabled = true;
      btn.textContent = "lege ab …";

      var wann = new Date(datum.value + "T" + (zeit.value || "18:00"));
      var basis = "freigaben/" + r.id;

      function steuerSchreiben() {
        db.collection("freigaben").doc(r.id).set({
          name: r.name,
          typ: "reel",
          videodatei: r.videodatei,
          caption: r.caption || "",
          profil: profil.value,
          datum: datum.value,
          zeit: zeit.value || "18:00",
          zeitpunktISO: isNaN(wann) ? "" : wann.toISOString(),
          status: "wartet",
          updatedAt: new Date().toISOString()
        }).then(function () {
          b.status = "wartet";
          saveReel(r);
          btn.disabled = false;
          render();
          toast("Freigegeben. Sag mir im Chat Bescheid, dann geht es raus.");
        }).catch(function () {
          btn.disabled = false;
          btn.textContent = "Für Blotato freigeben";
          toast("Das Ablegen hat nicht geklappt.");
        });
      }

      // Das Titelbild wird als Cover mitgegeben, damit im Feed steht, was sie sieht.
      var c = document.createElement("canvas");
      renderReelCanvas(c, r, {});
      setTimeout(function () {
        var q = 0.9, out = c.toDataURL("image/jpeg", q);
        while (out.length > 700000 && q > 0.45) { q -= 0.08; out = c.toDataURL("image/jpeg", q); }
        db.doc(basis).collection("bilder").doc("cover").set({ dataUrl: out, nr: 1 })
          .then(steuerSchreiben)
          .catch(function () {
            btn.disabled = false;
            btn.textContent = "Für Blotato freigeben";
            toast("Das Cover liess sich nicht ablegen.");
          });
      }, 320);
    };
  }

  function komprimiereDataUrl(dataUrl, cb) {""",
        "Reel-Blotato-Verdrahtung")

    t = ersetze(
        t,
        """        scrim: !!r.scrim, skript: r.skript || "", caption: r.caption || "",
        untertitel: r.untertitel || "", updatedAt: r.updatedAt""",
        """        scrim: !!r.scrim, skript: r.skript || "", caption: r.caption || "",
        untertitel: r.untertitel || "", videodatei: r.videodatei || "",
        blotato: r.blotato || null, updatedAt: r.updatedAt""",
        "saveReel Blotato")

    t = ersetze(
        t,
        """caption: d0.caption || "", untertitel: d0.untertitel || "", updatedAt: d0.updatedAt || "" };""",
        """caption: d0.caption || "", untertitel: d0.untertitel || "", videodatei: d0.videodatei || "", blotato: d0.blotato || null, updatedAt: d0.updatedAt || "" };""",
        "Reel aus DB")

    # --- 15) Echte Umlaute herstellen.
    # Patricias Regel: echte ä/ö/ü, Schweizer ss statt ß. Ein pauschales
    # Ersetzen von "ae/oe/ue" waere falsch ("neue", "Baue"), deshalb eine
    # ausdrueckliche Wortliste.
    UMLAUTE = {
        "Saetze": "Sätze", "geloest": "gelöst", "Fuer": "Für", "fuer": "für",
        "wofuer": "wofür", "veraendert": "verändert", "naechste": "nächste",
        "naechsten": "nächsten", "waehlst": "wählst", "gehoert": "gehört",
        "ueber": "über", "haette": "hätte", "taeglich": "täglich",
        "waere": "wäre", "erklaert": "erklärt", "erklaeren": "erklären",
        "Erklaerung": "Erklärung", "Loesung": "Lösung",
        "zurueckkommt": "zurückkommt", "ueberlegst": "überlegst",
        "Gespraech": "Gespräch", "einlaedt": "einlädt",
        "Regelmaessigkeit": "Regelmässigkeit", "laengsten": "längsten",
        "groesste": "grösste", "groesstes": "grösstes",
        "persoenliche": "persönliche", "Persoenliche": "Persönliche",
        "fuehre": "führe", "hoechste": "höchste", "Hoechste": "Höchste",
        "ausdrueckliche": "ausdrückliche", "Erklaeren": "Erklären",
        "Aufloesung": "Auflösung", "moeglich": "möglich",
        "Schritt fuer Schritt": "Schritt für Schritt",
        "Erzaehl": "Erzähl", "erzaehlen": "erzählen", "Wofuer": "Wofür",
        "dafuer": "dafür", "frueher": "früher", "geaendert": "geändert",
        "veraendert": "verändert", "aendert": "ändert",
    }
    # uebersicht und waehrung sind Bezeichner im bestehenden Code — nicht anfassen.
    anzahl = 0
    for a, b in sorted(UMLAUTE.items(), key=lambda x: -len(x[0])):
        neu_t, n = re.subn(r"\b%s\b" % re.escape(a), b, t)
        t = neu_t
        anzahl += n
    print("  Umlaute korrigiert: %d Stellen" % anzahl)

    rest = re.findall(r"\b\w*(?:aeh|ueh|oeh|fuer|ueber|aende|oese)\w*\b", t)
    if rest:
        print("  HINWEIS: pruefen ->", sorted(set(rest))[:12])

    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.write_text(t, encoding="utf-8")
    print("\nGeschrieben: %s (%d Zeichen)" % (ZIEL, len(t)))


if __name__ == "__main__":
    main()
