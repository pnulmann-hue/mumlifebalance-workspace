# -*- coding: utf-8 -*-
"""Die Lese- und Schreibliste der Karussells war unvollstaendig.

Gefunden am 08.10.2026, weil Patricia ein frisch abgelegtes Karussell im
Cockpit nicht gefunden hat.

Der Loader `db.collection("karussells").limit(60).get()` baut je Dokument ein
Objekt — und darin fehlten **`profil` und die vier Kommentar-Felder**, obwohl
`saveCarousel` sie schreibt. Umgekehrt fehlt `hinweis` in der Schreibliste.

🚨 **Dieselbe Falle, viermal derselbe Ort.** Am 16.09.2026 stand das Profil auf
   der Reel-Karte immer auf „Mentoring", weil nur `blotato.profil` gelesen
   wurde. Am 18.09. ging `hinweis` verloren, weil es in der Feldliste von
   `saveReel` fehlte. Am 24.09. wurde die Leseliste der **Storys** nachgezogen
   („Die Leseliste muss so lang sein wie die Schreibliste, sonst kommen Felder
   nie an") — die der Karussells blieb liegen.

**Was das anrichtet**

- `kartenProfil(o)` geht `blotato.profil` -> `o.profil` -> `"mentoring"`.
  Ohne `profil` landet jedes doTERRA-Karussell nach einem Neuladen auf
  **Mentoring** — und eine Freigabe plant es aufs falsche Konto.
- Ein Kommentar, den Patricia auf der Wochenkarte tippt, ist nach dem
  Neuladen aus der Ansicht verschwunden. Geschrieben wurde er, gelesen nicht.
- `hinweis` (z.B. „ANGEPINNTER BEITRAG, nicht ueber Blotato einplanen")
  ueberlebt die erste Bearbeitung nicht.

⚠️ **Offen:** `hinweis` wird jetzt gelesen und geschrieben, aber auf der
   Wochenkarte noch **nicht angezeigt**. Das ist ein eigener Schritt.

Wiederholbar: jede Ersetzung muss genau einmal passen, danach laeuft
`node --check` ueber das ganze eingebettete Skript.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
ZIEL = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"

# --- Teil 1: Leseliste -----------------------------------------------------
L_ALT = ('abgelehntStand: d0.abgelehntStand || "", caption: d0.caption || "", '
         'slides: d0.slides || [], updatedAt: d0.updatedAt || "" };')
L_NEU = ('abgelehntStand: d0.abgelehntStand || "", caption: d0.caption || "", '
         'slides: d0.slides || [], '
         'profil: d0.profil || "", hinweis: d0.hinweis || "", '
         'kommentar: d0.kommentar || "", '
         'kommentarStand: d0.kommentarStand || "", '
         'kommentarErledigt: d0.kommentarErledigt || "", '
         'kommentarAntwort: d0.kommentarAntwort || "", '
         'updatedAt: d0.updatedAt || "" };')
L_MARKE = 'profil: d0.profil || "", hinweis: d0.hinweis || "",'

# --- Teil 2: Schreibliste --------------------------------------------------
W_ALT = '        datum: car.datum || "", profil: car.profil || "",'
W_NEU = ('        datum: car.datum || "", profil: car.profil || "",'
         + chr(10) + '        hinweis: car.hinweis || "",')
W_MARKE = 'hinweis: car.hinweis || "",'


def pruefe_js(js, wo):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as f:
        f.write(js)
        tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("\U0001f6a8 node --check (%s): %s" % (wo, r.stderr or r.stdout))


def ersetze(t, alt, neu, marke, name, getan):
    if marke in t:
        return t
    if t.count(alt) != 1:
        sys.exit("\U0001f6a8 %s: Anker %sx gefunden, erwartet 1x"
                 % (name, t.count(alt)))
    getan.append(name)
    return t.replace(alt, neu)


def main():
    t = ZIEL.read_text(encoding="utf-8")
    getan = []
    t = ersetze(t, L_ALT, L_NEU, L_MARKE,
                "Leseliste (profil, hinweis, 4x kommentar*)", getan)
    t = ersetze(t, W_ALT, W_NEU, W_MARKE, "Schreibliste (hinweis)", getan)
    if not getan:
        sys.exit("\U0001f6a8 schon gepatcht")

    # Gegenprobe: alles, was gelesen wird, muss auch geschrieben werden.
    i = t.find('db.collection("karussells").doc(car.id).set({')
    schreibt = t[i:i + t[i:].find("})")]
    for feld in ("profil", "hinweis", "kommentar", "kommentarStand",
                 "kommentarErledigt", "kommentarAntwort"):
        if re.search(r"\b" + feld + r":", schreibt) is None:
            sys.exit("\U0001f6a8 %s wird gelesen, aber nicht geschrieben" % feld)

    pruefe_js(t[t.rfind("<script>") + 8:t.rfind("</script>")], "ganze Seite")
    ZIEL.write_text(t, encoding="utf-8")
    for z in getan:
        print("  " + z)
    print("node --check gruen")
    print("⚠️  hinweis wird jetzt gespeichert und gelesen, aber auf "
          "der Wochenkarte noch nicht angezeigt.")


if __name__ == "__main__":
    main()
