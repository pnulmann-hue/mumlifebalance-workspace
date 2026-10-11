# -*- coding: utf-8 -*-
"""„Aus deiner Planung" im Bild-Editor: erst den Tag wählen, dann den Entwurf.
Und die Storys aus dem Cockpit nehmen.

Anlass (Patricia, 18.09.2026): *„die storys will ich eigentlich auch nicht hier
drin haben. kannst du mir die nicht in die storybibliothek verschicken? ich habe
die storys jetzt immer im bildgenerator gemacht. es reicht, wenn sie da als
‚entwürfe' oben anwählbar sind pro Tag"* — und danach: *„ich meine in aus deiner
planung"*.

Zwei Teile:

**Bild-Editor** (`outputs/_bild-editor/index.html`)
  Bisher ein einziges Auswahlfeld mit ALLEN Entwürfen des Profils — beim Stand
  vom 18.09. waren das über dreissig Zeilen in einer Liste, quer über zwei
  Wochen und drei Formate. Jetzt zwei Felder: **Tag**, dann **Entwurf**.
  Dazu gefiltert nach dem oben gewählten Format — wer auf „Story 9:16" steht,
  sucht keine Reel-Cover.

**Cockpit** (`outputs/cockpit/mlb-cockpit.html`)
  Storys fliegen aus der Wochen-Vorschau und aus „Fertig zum Posten" raus. Sie
  bleiben in der Datenbank und im Story-Studio — es ist nur die Prüf- und
  Freigabe-Ansicht, in der sie nichts mehr zu suchen haben, weil Patricia sie
  im Bild-Editor baut und selbst vom Handy postet.

  🚨 Das dreht die Entscheidung vom 16.09. um („Die taeglichen Storys gehoeren
  hierher, nicht nur in den Bild-Editor"). Rückgängig zu machen, indem
  `STORY_RAUS` wieder auf False gesetzt und das Skript neu laufen gelassen wird.

Wiederholbar. Schreibt erst daneben und ersetzt danach.
"""
import io
import os
import sys

EDITOR = os.path.join("outputs", "_bild-editor", "index.html")
COCKPIT = os.path.join("outputs", "cockpit", "mlb-cockpit.html")
STORY_RAUS = True


# ============================================================ Bild-Editor

E_MARKUP_ALT = """      <select id="entwurfWahl"></select>
      <button class="btn" id="entwurfLaden">Entwurf in die Folien laden</button>
"""

E_MARKUP_NEU = """      <label for="entwurfTag">Tag</label>
      <select id="entwurfTag"></select>
      <label for="entwurfWahl">Entwurf</label>
      <select id="entwurfWahl"></select>
      <button class="btn" id="entwurfLaden">Entwurf in die Folien laden</button>
"""

E_LOGIK_ALT = """  function entwuerfeFuellen(){
    const liste = (entwurfDaten && entwurfDaten.entwuerfe || []).filter(e => e.profil === profilJetzt());
    const wahl = g('entwurfWahl');
    g('planPanel').style.display = liste.length ? "block" : "none";
    if (!liste.length) return;
    const arten = {karussell:"Karussell", story:"Story", cover:"Reel-Cover"};
    wahl.innerHTML = liste.map((e,i)=>
      `<option value="${i}">${esc(e.datum || "")} · ${esc(arten[e.art] || e.art || "")} · ${esc(e.name || "")}</option>`).join("");
    entwurfInfo();
  }
  function aktuellerEntwurf(){
    const liste = (entwurfDaten && entwurfDaten.entwuerfe || []).filter(e => e.profil === profilJetzt());
    return liste[+g('entwurfWahl').value] || null;
  }
"""

E_LOGIK_NEU = """  const ARTEN = {karussell:"Karussell", story:"Story", cover:"Reel-Cover"};
  const WOTAG = ["So","Mo","Di","Mi","Do","Fr","Sa"];
  /* Zum Format oben gehoert eine Entwurfsart. Wer auf „Story 9:16" steht,
     soll keine Reel-Cover in der Liste haben. */
  const FMT_ART = {story:"story", cover:"cover", slide:"karussell"};

  function tagLabel(iso){
    const t = new Date(iso + "T12:00:00");
    if (isNaN(t)) return iso || "ohne Datum";
    return WOTAG[t.getDay()] + " " + iso.slice(8,10) + "." + iso.slice(5,7) + ".";
  }

  /* Alle Entwuerfe, die gerade in Frage kommen: richtiges Profil, richtige Art.
     🚨 Ein einziges Auswahlfeld ueber alle Tage und Formate hatte ueber dreissig
     Zeilen — darin findet niemand den Dienstag. */
  function planEntwuerfe(){
    const art = FMT_ART[fmt] || "";
    return (entwurfDaten && entwurfDaten.entwuerfe || [])
      .filter(e => e.profil === profilJetzt() && (!art || (e.art || "") === art));
  }

  function entwuerfeFuellen(){
    const liste = planEntwuerfe();
    g('planPanel').style.display = liste.length ? "block" : "none";
    if (!liste.length) return;
    const tage = [...new Set(liste.map(e => e.datum || ""))].sort();
    const tagFeld = g('entwurfTag');
    const vorher = tagFeld.value;
    tagFeld.innerHTML = tage.map(d => {
      const n = liste.filter(e => (e.datum || "") === d).length;
      return `<option value="${esc(d)}">${esc(tagLabel(d))}`
           + (n > 1 ? ` · ${n} Entwürfe` : "") + `</option>`;
    }).join("");
    // Denselben Tag behalten, wenn es ihn noch gibt — sonst den naechsten
    // ab heute, damit sie nicht jedes Mal bei letzter Woche landet.
    if (tage.indexOf(vorher) >= 0) tagFeld.value = vorher;
    else {
      const heute = new Date().toISOString().slice(0,10);
      tagFeld.value = tage.find(d => d >= heute) || tage[0];
    }
    tagFuellen();
  }

  function tagFuellen(){
    const tag = g('entwurfTag').value;
    const drin = planEntwuerfe().filter(e => (e.datum || "") === tag);
    g('entwurfWahl').innerHTML = drin.map((e,i)=>
      `<option value="${i}">${esc(ARTEN[e.art] || e.art || "")} · ${esc(e.name || "")}</option>`).join("");
    entwurfInfo();
  }

  function aktuellerEntwurf(){
    const tag = g('entwurfTag').value;
    const drin = planEntwuerfe().filter(e => (e.datum || "") === tag);
    return drin[+g('entwurfWahl').value] || null;
  }
"""

E_HANDLER_ALT = """  g('entwurfWahl').onchange = entwurfInfo;
"""
E_HANDLER_NEU = """  g('entwurfWahl').onchange = entwurfInfo;
  g('entwurfTag').onchange = tagFuellen;
"""

# Beim Formatwechsel muss die Liste neu — sonst zeigt sie die Art von vorhin.
E_FMT_ALT = """    g('fmtHint').textContent = FORMATE[fmt].hinweis;
    stripBauen(); render();
  });
"""
E_FMT_NEU = """    g('fmtHint').textContent = FORMATE[fmt].hinweis;
    // Die Entwurfsliste haengt am Format — sonst stehen nach dem Wechsel
    // noch die Eintraege der vorigen Art darin.
    if (typeof entwuerfeFuellen === "function") entwuerfeFuellen();
    stripBauen(); render();
  });
"""


# ================================================================ Cockpit

C_STORY_ALT = """    // Die taeglichen Storys gehoeren dazu, nicht nur in den Bild-Editor —
    // hier prueft Patricia am Freitag.
    state.storys.forEach(function (s) {
      var f1 = (s.frames && s.frames[0]) || {};
      beitraege.push({ art: "storys", id: s.id, obj: s, format: "Story",
                       titel: s.name, hook: f1.text || "",
                       unter: (s.frames ? s.frames.length : 0) + " Folien",
                       caption: "", datei: "" });
    });
    return beitraege;
"""

C_STORY_NEU = """    // 🚨 Storys stehen seit 18.09. NICHT mehr hier. Patricia baut sie im
    // Bild-Editor und postet sie selbst vom Handy — in der Prüf- und
    // Freigabe-Ansicht haben sie damit nichts zu suchen, sie haben die Liste
    // nur verdoppelt. Sie bleiben in der Datenbank und im Story-Studio, und
    // in „Aus deiner Planung“ im Bild-Editor sind sie pro Tag anwählbar.
    // (Das dreht die Entscheidung vom 16.09. um. Rückgängig: diesen Block
    // wieder wie die beiden darüber aufbauen.)
    return beitraege;
"""

C_TILE_ALT = """      tile("Storys bereit", storys.length, "die postest du selbst") +
"""
C_TILE_NEU = ""

C_GRUPPE_ALT = """    gruppe("Storys \\u2014 die postest du selbst",
           "Storys gehen nie \\u00fcber Blotato. Folien im Bild-Editor bauen, "
           + "herunterladen, vom Handy posten.", storys);
"""
C_GRUPPE_NEU = ""

C_VAR_ALT = """    // Eine Story mit einem Datum von gestern ist vorbei, nicht offen.
    var storys = fertig.filter(function (b) {
      return b.art === "storys" && !zeitpunktVorbei(b);
    }).sort(nachDatum);
"""
C_VAR_NEU = ""

C_LEER_ALT = """    if (!kannRaus.length && !durch.length && !frei.length && !storys.length) {"""
C_LEER_NEU = """    if (!kannRaus.length && !durch.length && !frei.length) {"""

# Der Story-Hinweis in der Freigegeben-Liste kann bleiben (alte Freigaben),
# aber der Einleitungstext der Wochen-Vorschau nennt Storys nicht mehr.
C_TEXT_ALT = """      '<p>Jeder Beitrag so, wie er rausgeht: Cover, Hook, Caption und Hashtags. ' +"""
C_TEXT_NEU = """      '<p>Reels und Karussells so, wie sie rausgehen: Cover, Hook, Caption und ' +
      'Hashtags. Storys stehen im Bild-Editor unter „Aus deiner Planung“. ' +"""


def anwenden(pfad, paare, titel):
    if not os.path.isfile(pfad):
        sys.exit("Nicht gefunden: " + pfad)
    with io.open(pfad, encoding="utf-8") as f:
        text = f.read()
    getan, offen = [], []
    print("\n" + titel)
    for alt, neu, name in paare:
        if neu and neu in text:
            getan.append(name + " (war schon gesetzt)")
            continue
        if neu == "" and alt not in text:
            getan.append(name + " (war schon entfernt)")
            continue
        if text.count(alt) != 1:
            offen.append("%s — Anker %dx gefunden" % (name, text.count(alt)))
            continue
        text = text.replace(alt, neu)
        getan.append(name)
    for z in getan:
        print("  ok    " + z)
    for z in offen:
        print("  OFFEN " + z)
    if offen:
        sys.exit("\nAbgebrochen — nichts geschrieben.")
    tmp = pfad + ".neu"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, pfad)
    print("  geschrieben: %s (%d Zeichen)" % (pfad, len(text)))


def main():
    anwenden(EDITOR, [
        (E_MARKUP_ALT, E_MARKUP_NEU, "Zwei Felder: Tag und Entwurf"),
        (E_LOGIK_ALT, E_LOGIK_NEU, "Nach Tag und Format gruppieren"),
        (E_HANDLER_ALT, E_HANDLER_NEU, "Tag-Wechsel fuellt die Entwuerfe neu"),
        (E_FMT_ALT, E_FMT_NEU, "Formatwechsel fuellt die Liste neu"),
    ], "Bild-Editor")

    if not STORY_RAUS:
        print("\nCockpit: uebersprungen (STORY_RAUS = False)")
        return
    anwenden(COCKPIT, [
        (C_STORY_ALT, C_STORY_NEU, "Storys nicht mehr in die Beitragsliste"),
        (C_VAR_ALT, C_VAR_NEU, "Story-Gruppe entfaellt"),
        (C_TILE_ALT, C_TILE_NEU, "Kachel „Storys bereit“ entfaellt"),
        (C_GRUPPE_ALT, C_GRUPPE_NEU, "Story-Block entfaellt"),
        (C_LEER_ALT, C_LEER_NEU, "Leertext ohne Storys"),
        (C_TEXT_ALT, C_TEXT_NEU, "Einleitung nennt den Bild-Editor"),
    ], "Cockpit")


if __name__ == "__main__":
    main()
