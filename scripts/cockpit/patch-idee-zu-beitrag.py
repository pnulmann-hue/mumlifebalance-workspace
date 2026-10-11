# -*- coding: utf-8 -*-
"""Aus einer Idee wird ein Beitrag (14.09.2026).

Patricia: „idee wäre gut. aber dann müsste ich ja auch auf den beitrag klicken können und
ihn überarbeiten können mit hook, text usw. dann wäre es eine coole idee und ich könnte
sie wenn ich sie posten will in die wochenvorschau nehmen und dort freigeben."

Die Kette gab es fast ganz — nur der erste Schritt fehlte. Jede Zeile in „Ideen & Hooks"
bekommt jetzt einen Knopf, der die Idee ins Content-Studio trägt. Dort wählt sie das
Format, lässt schreiben, legt es an — und landet in der Wochen-Vorschau, wo sie Datum
setzt und freigibt. Die Idee wird dabei auf „Verwendet" gesetzt, damit der Vorrat nicht
zumüllt.

Wiederholbar.
"""
import io, os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PFAD = "outputs/cockpit/mlb-cockpit.html"
t = io.open(PFAD, encoding="utf-8").read()
vorher = t
getan, schon = [], []


def setze(alt, neu, was, marker):
    global t
    if alt in t:
        t = t.replace(alt, neu, 1)
        getan.append(was)
    elif marker in t:
        schon.append(was)
    else:
        print("!! Anker nicht gefunden:", was)


# 1 — Die Ideen-Tabelle bekommt eine Aktion
setze("""      neu: function () { return { id: uid("i"), typ: "Hook", saeule: SAEULEN[0], text: "", quelle: "", status: "Offen" }; },""",
      """      neu: function () { return { id: uid("i"), typ: "Hook", saeule: SAEULEN[0], text: "", quelle: "", status: "Offen" }; },
      aktion: { label: "→ Beitrag", titel: "Daraus einen Beitrag machen" },""",
      "Ideen-Tabelle bekommt eine Aktion",
      marker='aktion: { label: "→ Beitrag"')

# 2 — renderTable zeichnet den Knopf
setze("""    var def = TABLES[key];
    var grid = def.cols.map(function (c) { return c.w; }).join(" ") + " 34px";""",
      """    var def = TABLES[key];
    var grid = def.cols.map(function (c) { return c.w; }).join(" ") +
               (def.aktion ? " 108px" : "") + " 34px";""",
      "Platz fuer den Knopf in der Tabelle",
      marker='(def.aktion ? " 108px" : "")')

setze("""    head.innerHTML = def.cols.map(function (c) { return "<span>" + esc(c.l) + "</span>"; }).join("") + "<span></span>";
    rows.appendChild(head);

    var list = state[key].slice();""",
      """    head.innerHTML = def.cols.map(function (c) { return "<span>" + esc(c.l) + "</span>"; }).join("") +
                     (def.aktion ? "<span></span>" : "") + "<span></span>";
    rows.appendChild(head);

    var list = state[key].slice();""",
      "Kopfzeile bekommt die Spalte",
      marker='(def.aktion ? "<span></span>" : "")')

setze("""      var del = document.createElement("button");
      del.className = "del"; del.title = "Zeile löschen"; del.textContent = "×";""",
      """      if (def.aktion) {
        var akt = document.createElement("button");
        akt.className = "btn";
        akt.style.cssText = "font-size:12px;padding:5px 8px";
        akt.textContent = def.aktion.label;
        akt.title = def.aktion.titel;
        akt.onclick = function () { ideeInsStudio(item); };
        r.appendChild(akt);
      }
      var del = document.createElement("button");
      del.className = "del"; del.title = "Zeile löschen"; del.textContent = "×";""",
      "Knopf steht in jeder Ideen-Zeile",
      marker="ideeInsStudio(item);")

# 3 — Die Idee ins Studio tragen
setze("""  /* =========================================================
     Content-Studio
     ========================================================= */
  var studioForm = {""",
      """  /* =========================================================
     Content-Studio
     ========================================================= */
  /* Traegt eine Idee aus dem Vorrat ins Studio. Von dort geht es ueber
     „Als … anlegen" in die Wochen-Vorschau, wo Patricia freigibt. */
  function ideeInsStudio(idee) {
    studioForm.idee = idee.text || "";
    studioForm.ideeId = idee.id;
    if (idee.typ === "Angebot") studioForm.ziel = "Verkauf";
    else if (idee.typ === "Story") studioForm.format = "Story-Sequenz";
    studioResult = null;
    activeTab = "studio";
    render();
    toast("Idee ins Studio übernommen. Format wählen und schreiben lassen.");
  }

  /* Wird ein Beitrag daraus, ist die Idee verbraucht. */
  function ideeVerbraucht() {
    if (!studioForm.ideeId) return;
    var i = state.ideen.filter(function (x) { return x.id === studioForm.ideeId; })[0];
    if (i && i.status === "Offen") { i.status = "Verwendet"; saveList("ideen"); }
    studioForm.ideeId = null;
  }

  var studioForm = {""",
      "Idee wandert ins Studio",
      marker="function ideeInsStudio(idee) {")

# 4 — Beim Anlegen die Idee abhaken
for alt, marker, was in [
    ('        toast("Karussell angelegt. Texte prüfen und freigeben, gebaut wird im Bild-Editor.");',
     'ideeVerbraucht();\n        toast("Karussell angelegt',
     "Karussell hakt die Idee ab"),
    ('        toast("Sequenz angelegt.");',
     'ideeVerbraucht();\n        toast("Sequenz angelegt.");',
     "Story-Sequenz hakt die Idee ab"),
    ('        toast("Reel angelegt. Video reinziehen, Titelbild waehlen, fertig.");',
     'ideeVerbraucht();\n        toast("Reel angelegt.',
     "Reel hakt die Idee ab"),
]:
    setze(alt, "        ideeVerbraucht();\n" + alt, was, marker)

# 5 — Im Studio sichtbar machen, woher die Idee kommt
setze("""      '<div class="page-head"><div><h1>Content-Studio</h1>' +
      '<p>Eine Idee rein, fertiger Content raus. Alles wird mit deinem hinterlegten Wissen geschrieben, also mit deinem Ton, deinen Hookregeln und deinen Angeboten.</p></div></div>' +""",
      """      '<div class="page-head"><div><h1>Content-Studio</h1>' +
      '<p>Eine Idee rein, fertiger Content raus. Alles wird mit deinem hinterlegten Wissen geschrieben, also mit deinem Ton, deinen Hookregeln und deinen Angeboten.' +
      (studioForm.ideeId ? ' <b>Kommt gerade aus deinem Ideen-Vorrat.</b>' : '') +
      '</p></div></div>' +""",
      "Studio zeigt die Herkunft",
      marker="Kommt gerade aus deinem Ideen-Vorrat")

if t != vorher:
    io.open(PFAD, "w", encoding="utf-8", newline="\n").write(t)

print("Geaendert:")
for z in getan:
    print("  +", z)
if schon:
    print("Schon so:")
    for z in schon:
        print("  =", z)
if not getan:
    print("  (nichts zu tun)")
