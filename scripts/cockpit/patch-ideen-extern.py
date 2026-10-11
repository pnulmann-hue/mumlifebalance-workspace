"""Reiter «Ideen von anderen» mit Bau-Knopf.

Patricia am 24.09.2026: *„ein ideekasten wo du ja meine konkurrenzprofile
scrapps nach beitragsideen, die gut performt sind. da wäre dann ein reiter cool
mit „fertig bauen" und dieser befehl löst dann aus, dass du mir ein b-Roll,
sprechreel oder kaurssell machst"*.

**Die Ausbeute ist ehrlich mager, und der Reiter sagt das auch.** Von 1'098
gescrapten Beiträgen bleiben nach der Filterung 11 — und davon sind zwei
wirklich übertragbar. Die grossen Ausreisser sind persönliche Posts
(„Drei Wochen ohne meine drei ❤️") und Produktwerbung; die laufen, weil 35'000
Leute die Person kennen, nicht weil der Inhalt trägt.

🚨 **Deshalb heisst der Reiter „Ideen von anderen" und nicht „Top-Content".**
Eine Liste, die so tut, als wäre jeder Eintrag eine Goldader, wird nach dem
dritten Blick nicht mehr geöffnet.

**Der Knopf ist der eigentliche Wert.** Er legt einen Auftrag in die Sammlung
`bauauftraege`, den Claude beim nächsten Lauf abholt — dieselbe Mechanik wie
die Kommentarzeile. Patricia wählt dabei das Format: **B-Roll · Sprechreel ·
Karussell**.

🚨 **Im Auftrag steht, dass nicht kopiert wird.** Übernommen wird die
*Mechanik* — welche Frage, welcher Winkel, welches Format. Szene, Zahlen und
Sprache kommen aus Patricias Leben. Das ist keine Höflichkeit, sondern
[[feedback_hooks-inspiration-nicht-copypaste]].

🚨 **Der Knopf meldet nie „erledigt".** Er nimmt entgegen, sonst nichts — genau
wie der Cockpit-Bot. Eine Bestätigung, die nach Erledigung klingt, ist der
Fehler vom 16.09.

    python scripts/cockpit/patch-ideen-extern.py [--pruefen] [--datei <pfad>]
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

# ------------------------------------------------------------ 1 · Reiter

ALT_TAB = '''    { id: "ideenkasten", label: "Ideenkasten" },'''
NEU_TAB = '''    { id: "ideenkasten", label: "Ideenkasten" },
    { id: "ideenextern", label: "Ideen von anderen" },'''

# ------------------------------------------------------------- 2 · Laden

ALT_LADE = '''      db.doc("daten/gepostet-zuordnung").onSnapshot(function (snap) {'''
NEU_LADE = '''      db.doc("daten/ideen-extern").onSnapshot(function (snap) {
        if (!snap.exists) return;
        ideenExtern = snap.data() || { ideen: [] };
        lsSet("ideen-extern", ideenExtern);
        if (activeTab === "ideenextern") render();
      }, function () {});
      db.doc("daten/gepostet-zuordnung").onSnapshot(function (snap) {'''

ALT_INIT = '''  igZuordnung = lsGet("ig-zuordnung", { zuordnung: {} }) || { zuordnung: {} };'''
NEU_INIT = '''  igZuordnung = lsGet("ig-zuordnung", { zuordnung: {} }) || { zuordnung: {} };
  ideenExtern = lsGet("ideen-extern", { ideen: [] }) || { ideen: [] };'''

ALT_VAR = '''  var igZuordnung = { zuordnung: {}, nicht_pruefbar: [] };'''
NEU_VAR = '''  var igZuordnung = { zuordnung: {}, nicht_pruefbar: [] };
  var ideenExtern = { ideen: [] };'''

# ------------------------------------------------------------ 3 · Ansicht

ANKER_RENDER = '''  /* Reiter „Fertig zum Posten": nur das, was schon steht. */'''

NEU_RENDER = '''  /* Reiter „Ideen von anderen": was bei den beobachteten Profilen deutlich
     ueber deren eigenem Schnitt lag. Gebaut von ideen-extern-bauen.py.
     Siehe Kopf von patch-ideen-extern.py, warum der Reiter bewusst nicht
     „Top-Content" heisst. */
  function renderIdeenExtern(main) {
    var alle = (ideenExtern && ideenExtern.ideen) || [];
    var stand = (ideenExtern && ideenExtern.stand) || "";
    var alt = stand ? Math.round((Date.now() - new Date(stand + "T00:00:00")) / 86400000) : 99;

    main.innerHTML =
      '<div class="page-head"><div><h1>Ideen von anderen</h1>' +
      '<p>Beitr\\u00e4ge aus deiner Beobachtungsliste, die deutlich \\u00fcber dem ' +
      '<strong>eigenen Schnitt des jeweiligen Kontos</strong> lagen \\u2014 absolute ' +
      'Likes sagen nichts, wenn ein Konto zwanzigmal so gross ist wie deins. ' +
      'Das ist eine Anregung, kein Katalog: \\u00fcbernommen wird die Machart, ' +
      'nie der Text.</p></div></div>' +
      (alt > 2 ? '<div class="panel warn"><strong>Der Stand ist ' + alt +
        ' Tage alt.</strong> Neu holen mit <code>python ' +
        'scripts/cockpit/ideen-extern-bauen.py</code>.</div>' : "") +
      '<div class="tiles">' +
      tile("Ideen", alle.length, stand ? "Stand " + fmtDate(stand) : "kein Stand") +
      tile("Eingeschlagen", alle.filter(function (i) {
             return i.stufe === "eingeschlagen"; }).length, "ab 3\\u00d7 eigener Schnitt") +
      '</div><div id="ideliste"></div>';

    var box = main.querySelector("#ideliste");
    if (!alle.length) {
      box.innerHTML = '<div class="panel"><div class="empty">Noch nichts da. ' +
        'Der Scrape l\\u00e4uft t\\u00e4glich \\u2014 das Dokument wird beim ' +
        'n\\u00e4chsten Abgleich gef\\u00fcllt.</div></div>';
      return;
    }

    alle.forEach(function (i) {
      var k = document.createElement("div");
      k.className = "panel idee-karte";
      var fmt = i.format === "reel" ? "Reel" : (i.format === "karussell" ? "Karussell" : "Bild");
      k.innerHTML =
        '<div class="idee-kopf">' +
          '<span class="tp-stand ' + (i.stufe === "eingeschlagen" ? "gut" : "info") + '">' +
            i.faktor + '\\u00d7 eigener Schnitt</span>' +
          '<span class="tp-format">' + esc(fmt) + '</span>' +
          '<span class="idee-quelle">' + esc(i.label || i.konto) +
            ' \\u00b7 ' + (i.follower || 0).toLocaleString("de-CH") + ' Follower' +
            ' \\u00b7 ' + esc(fmtDate(i.datum)) + '</span>' +
          (i.link ? '<a class="btn ghost" href="' + esc(i.link) +
            '" target="_blank" rel="noopener">Ansehen</a>' : "") +
        '</div>' +
        '<p class="idee-hook">' + esc(i.hook) + '</p>' +
        '<details class="idee-mehr"><summary>Ganzer Text</summary>' +
          '<p class="note" style="white-space:pre-wrap">' + esc(i.caption) + '</p>' +
        '</details>' +
        '<div class="idee-fuss">' +
          '<span class="note">Bau mir daraus:</span>' +
          '<button class="btn ib" data-f="broll">B-Roll</button>' +
          '<button class="btn ib" data-f="sprech">Sprechreel</button>' +
          '<button class="btn ib" data-f="karussell">Karussell</button>' +
          '<span class="idee-stand note"></span>' +
        '</div>';

      var stelle = k.querySelector(".idee-stand");
      [].forEach.call(k.querySelectorAll(".ib"), function (b) {
        b.onclick = function () {
          if (!db) { toast("Ohne Datenbank kann ich den Auftrag nicht ablegen."); return; }
          var was = b.getAttribute("data-f");
          db.collection("bauauftraege").doc("idee-" + i.id + "-" + was).set({
            quelle: "ideen-extern",
            format: was,
            ideeId: i.id,
            konto: i.konto,
            link: i.link || "",
            hook: i.hook,
            caption: i.caption,
            faktor: i.faktor,
            profil: i.profil || "",
            /* 🚨 Steht im Auftrag, nicht nur in der Doku: uebernommen wird die
               Machart, nie der Text. */
            hinweis: "Nur die Machart übernehmen — Frage, Winkel, Aufbau. " +
                     "Szene, Zahlen und Sprache kommen aus Patricias Leben. " +
                     "Durch Blacklisten-Prüfung und den letzten Hook-Check.",
            stand: new Date().toISOString(),
            erledigt: ""
          }).then(function () {
            // Nie „erledigt" melden — nur „notiert".
            stelle.textContent = "Notiert \\u2014 ich bau es beim nächsten Lauf.";
            toast("Auftrag notiert. Ich melde mich, wenn es steht.");
          }).catch(function () { toast("Konnte den Auftrag nicht ablegen."); });
        };
      });
      box.appendChild(k);
    });
  }

  /* Reiter „Fertig zum Posten": nur das, was schon steht. */'''

# ----------------------------------------------------------- 4 · Routing

ALT_ROUTE = '''    else if (activeTab === "fertig") renderFertig(main);'''
NEU_ROUTE = '''    else if (activeTab === "ideenextern") renderIdeenExtern(main);
    else if (activeTab === "fertig") renderFertig(main);'''

# --------------------------------------------------------------- 5 · CSS

ALT_CSS = '''  .uehook.klickbar { cursor: pointer; }'''
NEU_CSS = '''  .idee-karte { margin-bottom: 14px; }
  .idee-kopf { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-bottom: 10px; }
  .idee-quelle { font-size: 12px; color: var(--ink-soft); }
  .idee-kopf .btn.ghost { margin-left: auto; }
  .idee-hook { font-family: var(--display); font-size: 17px; line-height: 1.35; margin: 0 0 10px; }
  .idee-mehr > summary { cursor: pointer; font-size: 13px; color: var(--ink-soft); }
  .idee-fuss { display: flex; gap: 8px; align-items: center; flex-wrap: wrap;
               margin-top: 12px; padding-top: 10px; border-top: 1px solid var(--line); }
  .idee-stand { color: var(--good); }
  .uehook.klickbar { cursor: pointer; }'''


def setze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet genau 1x. Nichts geändert."
                 % (name, n))
    return text.replace(alt, neu, 1)


def js_pruefen(html):
    for i, block in enumerate(re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)):
        if len(block.strip()) < 200:
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                         encoding="utf-8") as f:
            f.write(block)
            p = f.name
        r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
        Path(p).unlink(missing_ok=True)
        if r.returncode != 0:
            return "Block %d: %s" % (i, (r.stderr or "")[:700])
    return ""


def main():
    nur_pruefen = "--pruefen" in sys.argv
    datei = ROOT / "outputs" / "cockpit" / "mlb-cockpit-neu.html"
    if "--datei" in sys.argv:
        datei = Path(sys.argv[sys.argv.index("--datei") + 1])

    s = datei.read_text(encoding="utf-8")
    if "renderIdeenExtern" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ALT_TAB, NEU_TAB, "Reiter")
    s = setze(s, ALT_VAR, NEU_VAR, "Variable")
    s = setze(s, ALT_LADE, NEU_LADE, "Ladestelle")
    s = setze(s, ALT_INIT, NEU_INIT, "Init")
    s = setze(s, ANKER_RENDER, NEU_RENDER, "Ansicht")
    s = setze(s, ALT_ROUTE, NEU_ROUTE, "Routing")
    s = setze(s, ALT_CSS, NEU_CSS, "CSS")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Reiter «Ideen von anderen» eingebaut · %d KB" % (len(s) / 1024))
    print("  Knopf legt Aufträge in die Sammlung «bauauftraege».")


if __name__ == "__main__":
    main()
