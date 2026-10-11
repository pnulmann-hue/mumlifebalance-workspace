# -*- coding: utf-8 -*-
"""Das Reel-Cover im Cockpit: Shootingbild + Markenfarbe als Schatten, oder Vollfarbe.

**Patricias Vorgabe, 16.09.2026:** *„ich will ein separates coverbild und zwar so, wie
wir das vereinbart haben. ein shootingbild (was ich wechseln kann) inkl meine
brandingfarbe als ‚Schatten‘ drüber. oder dann die vollfarbe in meinem branding"*

Vier Aenderungen, und eine davon ist ein Datenverlust-Fehler, der nichts mit Covern
zu tun hat, aber beim Hinsehen aufgefallen ist:

---

## 🚨 1 · `saveReel` loescht Felder, die es nicht kennt

`db.collection("reels").doc(id).set({...})` schreibt eine **feste Feldliste**. Alles,
was nicht darin steht, ist nach dem naechsten Speichern **weg**. Betroffen waren:

| Feld | Folge |
|---|---|
| `kommentar`, `kommentarStand` | 🔴 Die Kommentarzeile vom selben Tag hat **nie** in die Datenbank geschrieben. Der Knopf meldete „Notiert", der Task um 19:30 haette nie etwas gefunden. |
| `profil` | 🔴 Die sechs am 16.09. nachgetragenen Profile waeren beim naechsten Bearbeiten wieder verschwunden. |
| `coverhook`, `coverunter` | der Cover-Titel |

Dasselbe Muster in `saveCarousel` (dort fehlten `profil` und die Kommentarfelder) und
in `saveStory`. **Ein `set()` mit Feldliste ist eine Falle: neue Felder muessen an
zwei Stellen nachgetragen werden — beim Schreiben und beim Lesen.** Wer nur eine
Stelle aendert, baut einen Datenverlust, den niemand bemerkt, weil das Feld ja
vorhanden *aussieht*, solange die Seite offen bleibt.

---

## 2 · Der Cover-Titel ist nicht der gesprochene Hook

`renderReelCanvas` zeichnete `r.hook` — den Satz fuer die Kamera. Auf dem Cover steht
jetzt `r.coverhook || r.hook`, also der ganze Satz, aus dem beim Scrollen hervorgeht,
worum es geht.

## 3 · Der Schatten traegt die Markenfarbe

Bisher war er `rgba(6,14,24,…)` — ein generisches Dunkelblau-Schwarz. Jetzt kommt er
aus `coverfarbe` (Petrol · Dunkelblau · Orange), damit das Foto in ihrer Farbe liegt.

## 4 · Die Vollfarbe kommt ebenfalls aus `coverfarbe`

Ohne Foto fuellte das Cover mit `BRANDS[brand].bg`. Damit war die Farbwahl auf der
Wochenkarte wirkungslos, sobald kein Bild dahinterlag.

🚨 **`pos` bleibt unveraendert `unten`, wenn es gesetzt ist** — aber neue Cover setzen
`mitte`, weil Instagram unten Caption und Knöpfe darueberlegt (tote Zone 82–100 %).

    python scripts/cockpit/patch-cover-im-cockpit.py <html> <html>
"""
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def ersetze(text, alt, neu, was):
    n = text.count(alt)
    if n != 1:
        sys.exit(f"ABBRUCH bei {was}: {n} Treffer statt 1.")
    print(f"  ok  {was}")
    return text.replace(alt, neu)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    quelle, ziel = Path(sys.argv[1]), Path(sys.argv[2])
    zeilen = quelle.read_text(encoding="utf-8").splitlines()
    if zeilen and zeilen[0].startswith("<!doctype"):
        zeilen = zeilen[1:]
    if zeilen and zeilen[-1].strip() == "</body></html>":
        zeilen = zeilen[:-1]
    t = "\n".join(zeilen)

    # --- 1 · Die Farbtabelle fuer Schatten und Vollfarbe ------------------
    t = ersetze(
        t,
        """  var COVERFARBEN = [""",
        "\n".join([
            "  /* Markenfarben als RGB, damit der Schatten mit Deckkraft gemischt werden",
            "     kann. Patricia will ihre Farbe ueber dem Foto, nicht ein generisches",
            "     Dunkelblau-Schwarz. Kein Gelb, kein Gold, kein Pink — nur diese drei. */",
            "  var COVERRGB = {",
            "    petrol:     [18, 130, 140],   // #12828c",
            "    dunkelblau: [41, 85, 109],    // #29556d",
            "    orange:     [220, 130, 46]    // #dc822e",
            "  };",
            "  function coverRGB(r) { return COVERRGB[r && r.coverfarbe] || COVERRGB.dunkelblau; }",
            "",
            "  var COVERFARBEN = [",
        ]),
        "1 Farbtabelle")

    # --- 2 · Cover-Titel statt gesprochenem Hook --------------------------
    t = ersetze(
        t,
        """      var h = fitLines(ctx, String(r.hook || "").toUpperCase(), maxW, RH * 0.34, b.display, "bold", 104, 44, 1.12);
      var uLines = [];
      if (r.unter) {
        ctx.font = "40px " + b.body;
        uLines = wrap(ctx, r.unter, maxW).slice(0, 3);
      }""",
        "\n".join([
            "      // \U0001F6A8 Auf dem Cover steht der Cover-Titel, nicht der gesprochene Hook.",
            "      // Der Hook ist der Satz fuer die Kamera und dafuer zu lang.",
            "      var coverText = r.coverhook || r.hook || \"\";",
            "      var coverUnter = r.coverunter || r.unter || \"\";",
            """      var h = fitLines(ctx, String(coverText).toUpperCase(), maxW, RH * 0.34, b.display, "bold", 104, 44, 1.12);""",
            "      var uLines = [];",
            "      if (coverUnter) {",
            '        ctx.font = "40px " + b.body;',
            "        uLines = wrap(ctx, coverUnter, maxW).slice(0, 3);",
            "      }",
        ]),
        "2 Cover-Titel")

    # --- 3 · Schatten in der Markenfarbe ---------------------------------
    t = ersetze(
        t,
        """        var g = ctx.createLinearGradient(0, y - 150, 0, y + blockH + 150);
        g.addColorStop(0, "rgba(6,14,24,0)");
        g.addColorStop(0.35, "rgba(6,14,24,0.62)");
        g.addColorStop(0.7, "rgba(6,14,24,0.62)");
        g.addColorStop(1, "rgba(6,14,24,0)");""",
        "\n".join([
            "        // Der Schatten traegt ihre Markenfarbe, nicht ein generisches Dunkel.",
            "        var c3 = coverRGB(r), rgb = c3[0] + \",\" + c3[1] + \",\" + c3[2];",
            "        var g = ctx.createLinearGradient(0, y - 150, 0, y + blockH + 150);",
            '        g.addColorStop(0, "rgba(" + rgb + ",0)");',
            '        g.addColorStop(0.35, "rgba(" + rgb + ",0.88)");',
            '        g.addColorStop(0.7, "rgba(" + rgb + ",0.88)");',
            '        g.addColorStop(1, "rgba(" + rgb + ",0)");',
        ]),
        "3 Schatten in Markenfarbe")

    # --- 4 · Vollfarbe ebenfalls aus coverfarbe ---------------------------
    t = ersetze(
        t,
        """    } else {
      ctx.fillStyle = b.bg;""",
        "\n".join([
            "    } else {",
            "      // Ohne Foto: Vollflaeche in der gewaehlten Markenfarbe. Vorher stand hier",
            "      // die Hintergrundfarbe des Marken-Looks, wodurch die Farbwahl auf der",
            "      // Wochenkarte ohne Bild wirkungslos war.",
            "      var cv = coverRGB(r);",
            '      ctx.fillStyle = "rgb(" + cv[0] + "," + cv[1] + "," + cv[2] + ")";',
        ]),
        "4 Vollfarbe")

    # --- 5 · saveReel verliert keine Felder mehr --------------------------
    t = ersetze(
        t,
        """        name: r.name, hook: r.hook, unter: r.unter, pos: r.pos, brand: r.brand,
        datum: r.datum || "", textfrei: !!r.textfrei,
        coverfarbe: r.coverfarbe || "dunkelblau",
        videourl: r.videourl || "",
        scrim: !!r.scrim, skript: r.skript || "", caption: r.caption || "",
        untertitel: r.untertitel || "", videodatei: r.videodatei || "",
        blotato: r.blotato || null, updatedAt: r.updatedAt""",
        "\n".join([
            "        // \U0001F6A8 Feste Feldliste: was hier fehlt, ist nach dem naechsten",
            "        // Speichern WEG. Bis 16.09. fehlten `kommentar` (die Kommentarzeile hat",
            "        // dadurch nie in die Datenbank geschrieben) und `profil` (die sechs",
            "        // nachgetragenen Profile waeren still verschwunden). Neue Felder immer",
            "        // hier UND beim Lesen weiter unten nachtragen.",
            "        name: r.name, hook: r.hook, unter: r.unter, pos: r.pos, brand: r.brand,",
            '        datum: r.datum || "", textfrei: !!r.textfrei,',
            '        profil: r.profil || "",',
            '        coverfarbe: r.coverfarbe || "dunkelblau",',
            '        coverhook: r.coverhook || "", coverunter: r.coverunter || "",',
            '        kommentar: r.kommentar || "", kommentarStand: r.kommentarStand || "",',
            '        kommentarErledigt: r.kommentarErledigt || "",',
            '        kommentarAntwort: r.kommentarAntwort || "",',
            '        videourl: r.videourl || "",',
            '        scrim: !!r.scrim, skript: r.skript || "", caption: r.caption || "",',
            '        untertitel: r.untertitel || "", videodatei: r.videodatei || "",',
            "        blotato: r.blotato || null, updatedAt: r.updatedAt",
        ]),
        "5 saveReel vollstaendig")

    # --- 6 · und liest sie auch wieder ein --------------------------------
    t = ersetze(
        t,
        """coverfarbe: d0.coverfarbe || "dunkelblau", videourl: d0.videourl || "",""",
        """coverfarbe: d0.coverfarbe || "dunkelblau", """
        """coverhook: d0.coverhook || "", coverunter: d0.coverunter || "", """
        """profil: d0.profil || "", kommentar: d0.kommentar || "", """
        """kommentarStand: d0.kommentarStand || "", """
        """kommentarErledigt: d0.kommentarErledigt || "", """
        """kommentarAntwort: d0.kommentarAntwort || "", videourl: d0.videourl || "",""",
        "6 Reels lesen")

    # --- 7 · Karussell und Story genauso ----------------------------------
    t = ersetze(
        t,
        """        name: car.name, brand: car.brand, handle: car.handle,
        typ: car.typ || "listicle", funnel: car.funnel || "TOF",
        datum: car.datum || "",
        textfrei: !!car.textfrei, blotato: car.blotato || null,""",
        "\n".join([
            "        name: car.name, brand: car.brand, handle: car.handle,",
            '        typ: car.typ || "listicle", funnel: car.funnel || "TOF",',
            '        datum: car.datum || "", profil: car.profil || "",',
            '        kommentar: car.kommentar || "", kommentarStand: car.kommentarStand || "",',
            '        kommentarErledigt: car.kommentarErledigt || "",',
            '        kommentarAntwort: car.kommentarAntwort || "",',
            "        textfrei: !!car.textfrei, blotato: car.blotato || null,",
        ]),
        "7 saveCarousel vollstaendig")

    t = ersetze(
        t,
        """        name: st.name, brand: st.brand, phase: st.phase || "", frames: st.frames,
        datum: st.datum || "", textfrei: !!st.textfrei, updatedAt: st.updatedAt""",
        "\n".join([
            '        name: st.name, brand: st.brand, phase: st.phase || "", frames: st.frames,',
            '        datum: st.datum || "", profil: st.profil || "",',
            '        kommentar: st.kommentar || "", kommentarStand: st.kommentarStand || "",',
            '        kommentarErledigt: st.kommentarErledigt || "",',
            '        kommentarAntwort: st.kommentarAntwort || "",',
            "        textfrei: !!st.textfrei, updatedAt: st.updatedAt",
        ]),
        "8 saveStory vollstaendig")

    ziel.write_text(t + "\n", encoding="utf-8")
    print(f"\nGeschrieben: {ziel}  ({len(t.splitlines())} Zeilen)")


if __name__ == "__main__":
    main()
