# -*- coding: utf-8 -*-
"""Reel als Format im Content-Studio + das passende Framework je Format (14.09.2026).

Patricia: „hier im content studio gebe ich ja an ist es ein karussell, story sequenz.
wäre hier nicht auch klug für ein reel mit hook und caption? bei reels wäre dann aber
das wissen aus skill reel wichtig, bei karussell das von karussell und bei story der
storyskill."

Zwei Sachen also:
1. Reel fehlte als Format — jetzt mit Titelbild-Hook, Unterzeile, Sprechskript und Caption.
2. Das Format-Wissen hing nirgends dran. `wissen-bauen.py` legt es unter `formate` ab,
   und `wissenText(format)` haengt nur den passenden Block an — nicht alle drei, sonst
   schleppt jeder Auftrag 65'000 Zeichen mit, die er nicht braucht.

Wiederholbar.
"""
import io, os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PFAD = "outputs/cockpit/mlb-cockpit.html"
t = io.open(PFAD, encoding="utf-8").read()
vorher = t
getan, schon = [], []


def setze(alt, neu, was, marker=None):
    global t
    if alt in t:
        t = t.replace(alt, neu, 1)
        getan.append(was)
    elif (marker or neu.strip().split("\n")[0]) in t:
        schon.append(was)
    else:
        print("!! Anker nicht gefunden:", was)


# 1 — wissenText nimmt das Format entgegen
setze("  function wissenText() {",
      "  function wissenText(format) {",
      "wissenText nimmt ein Format entgegen",
      marker="function wissenText(format)")

setze('''    if (wissenVoll && wissenVoll.text) {
      teile.push("DAS VOLLSTAENDIGE MARKENWISSEN (Stand " +
        (wissenVoll.stand || "unbekannt") + ")\\n" + wissenVoll.text);
    }''',
      '''    if (wissenVoll && wissenVoll.text) {
      teile.push("DAS VOLLSTAENDIGE MARKENWISSEN (Stand " +
        (wissenVoll.stand || "unbekannt") + ")\\n" + wissenVoll.text);
    }
    // Nur das Framework des gewaehlten Formats — Reel, Karussell oder Story.
    if (format && wissenVoll && wissenVoll.formate && wissenVoll.formate[format]) {
      teile.push("WISSEN ZUM FORMAT " + format.toUpperCase() + "\\n" +
                 wissenVoll.formate[format]);
    }''',
      "Format-Wissen wird angehaengt",
      marker="WISSEN ZUM FORMAT")

# 2 — Reel als Format im Studio
setze('feld("Was soll entstehen", sel("format", ["Karussell", "Story-Sequenz", "Nur Hooks", "Nur Caption"]));',
      'feld("Was soll entstehen", sel("format", ["Karussell", "Reel", "Story-Sequenz", "Nur Hooks", "Nur Caption"]));',
      "Reel steht als Format zur Auswahl",
      marker='"Karussell", "Reel", "Story-Sequenz"')

# 3 — Format an wissenText durchreichen
setze('''    var basis =
      "Du bist die Ghostwriterin von Patricia Ulmann. Hier ist alles, was du über ihre Marke, ihre Zielgruppe und ihre Regeln wissen musst:\\n\\n" +
      wissenText() +''',
      '''    var FORMAT_SCHLUESSEL = { "Karussell": "karussell", "Reel": "reel", "Story-Sequenz": "story" };
    var basis =
      "Du bist die Ghostwriterin von Patricia Ulmann. Hier ist alles, was du über ihre Marke, ihre Zielgruppe und ihre Regeln wissen musst:\\n\\n" +
      wissenText(FORMAT_SCHLUESSEL[f.format] || "") +''',
      "Studio reicht das Format durch",
      marker="var FORMAT_SCHLUESSEL")

# 4 — Auftrag und Antwortform fuer das Reel
setze('''    } else if (f.format === "Story-Sequenz") {''',
      '''    } else if (f.format === "Reel") {
      auftrag = "Baue ein Reel. Halte dich an die Reel-Regeln oben: 3-Sekunden-Regel, " +
        "Struktur-Formel, On-Screen-Text, kein langweiliges Reel. " +
        "Das Sprechskript ist fuer ein Selfie-Video von dreissig bis fuenfundvierzig Sekunden, " +
        "in gesprochener Sprache, ohne Regieanweisungen im Text. " +
        "Die Titelbild-Hook hat hoechstens acht Woerter und steht gross lesbar auf dem Standbild. " +
        "Sag ausserdem, was auf dem Titelbild zu sehen sein soll, und gib drei alternative Hooks.\\n\\n" +
        'Antworte als JSON: {"name": "kurzer Titel", "hook": "Titelbild-Hook", "unter": "kurze Unterzeile oder leer", "hooks": ["...","...","..."], "skript": "das Sprechskript", "caption": "die fertige Caption", "bildidee": "was auf dem Titelbild zu sehen ist"}';
    } else if (f.format === "Story-Sequenz") {''',
      "Reel-Auftrag im Studio",
      marker='f.format === "Reel"')

# 5 — Ergebnis anzeigen und als Reel anlegen
setze('''    if (r.frames && r.frames.length) {''',
      '''    if (studioResult.__format === "Reel" && (r.skript || r.hook)) {
      var rw = document.createElement("div");
      rw.style.cssText = "display:flex;flex-direction:column;gap:10px";
      if (r.hook) {
        var hz = document.createElement("div");
        hz.className = "sp";
        hz.innerHTML = "<b>" + esc(r.hook) + "</b>" + esc(r.unter || "");
        rw.appendChild(hz);
      }
      if (r.skript) {
        var st = document.createElement("textarea");
        st.style.cssText = "width:100%;min-height:190px;background:var(--ground);border:1px solid var(--line);border-radius:8px;padding:10px 12px;font-size:13px";
        st.value = r.skript;
        rw.appendChild(st);
      }
      var rb = document.createElement("button");
      rb.className = "btn primary";
      rb.textContent = "Als Reel anlegen";
      rb.onclick = function () {
        var neu = neuesReel(r.name || studioForm.idee.slice(0, 40));
        neu.hook = r.hook || "";
        neu.unter = r.unter || "";
        neu.skript = r.skript || "";
        neu.caption = r.caption || "";
        saveReel(neu);
        activeTab = "reels";
        render();
        toast("Reel angelegt. Video reinziehen, Titelbild waehlen, fertig.");
      };
      rw.appendChild(rb);
      block("Reel — Titelbild-Hook und Sprechskript", rw);
    }

    if (r.frames && r.frames.length) {''',
      "Reel-Ergebnis mit Knopf ins Reel-Studio",
      marker='Als Reel anlegen')

# 6 — Der Generator im Reel-Studio bekommt das Reel-Wissen auch
setze('''          "Du bist die Ghostwriterin von Patricia Ulmann. Ihr Wissen und ihre Regeln:\\n\\n" + wissenText() +
          "\\n\\nSchreibe ein Reel zu diesem Thema: " + thema +''',
      '''          "Du bist die Ghostwriterin von Patricia Ulmann. Ihr Wissen und ihre Regeln:\\n\\n" + wissenText("reel") +
          "\\n\\nSchreibe ein Reel zu diesem Thema: " + thema +''',
      "Reel-Studio nutzt das Reel-Wissen",
      marker='wissenText("reel")')

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
