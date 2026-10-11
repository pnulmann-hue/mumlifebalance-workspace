# -*- coding: utf-8 -*-
"""Die Uhrzeit gehoert auf die Wochenkarte — sonst geht die Freigabe ins Leere.

**Der Fehler (gefunden 16.09.2026).** Patricia: *„wenn ich es jetzt um 19.50 freigebe,
wirds dann noch gepostet? nicht oder?"* — Sie hatte recht, und der Grund war unsichtbar:

```js
var zeit = bl.zeit || (b.art === "reels" ? "18:00" : "07:30");
```

Auf der Wochenkarte liess sich nur **Datum und Profil** setzen, nie die Uhrzeit. Die
kam aus diesem Vorgabewert. Ein Reel mit dem heutigen Datum bekam damit **18:00** —
und der Einplan-Task laeuft um **20:00**. Der Zeitpunkt war beim Einplanen also
*immer schon vorbei*, und das Skript blockt Zeitpunkte in der Vergangenheit.

🚨 **Damit konnte ein Reel, das am selben Tag freigegeben wurde, nie rausgehen.** Nicht
manchmal — nie. Und weil die Freigabe trotzdem „Freigegeben und abgelegt" meldete, sah
es jedes Mal so aus, als haette es geklappt.

**Drei Aenderungen:**

1. **Ein Zeitfeld auf der Karte**, direkt neben dem Datum. Was rausgeht und wann,
   steht an derselben Stelle.
2. **Vorgabe nach den echten Posting-Zeiten** statt 18:00:
   Reel Mentoring **21:00** · Reel doTERRA **21:30** · Karussell **07:30**.
   Alle drei liegen **nach** dem Einplan-Lauf um 20:00 — ausser dem Karussell, das
   ohnehin fuer den naechsten Morgen gedacht ist.
3. **Warnung, wenn der Zeitpunkt schon vorbei ist.** Dann wird `status:
   "zeitpunkt-vorbei"` abgelegt statt `"wartet"`, der Einplan-Task ueberspringt es,
   und die Meldung sagt, was zu tun ist. Lieber ein sichtbares Nein als ein stilles.

🚨 **Das Zeitfeld darf nicht in die Index-Liste der Fusszeile geraten.** Dort werden
Datum, Kopieren und Freigeben ueber `felder[0]`, `felder[1]` und `felder[laenge-1]`
angesprochen; ein zusaetzliches `<input>` wuerde alles um eins verschieben. Deshalb
traegt es die Klasse `wk-zeit` und wird im Selektor ausgenommen.

    python scripts/cockpit/patch-postzeit.py <html> <html>
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

    # --- A · Eine Stelle, die die Vorgabezeit kennt ------------------------
    t = ersetze(
        t,
        "  var BILDEDITOR = \"https://claude.ai/code/artifact/21e66e0e-2576-41db-8c8d-f14d7079a1e0\";",
        "\n".join([
            "  var BILDEDITOR = \"https://claude.ai/code/artifact/21e66e0e-2576-41db-8c8d-f14d7079a1e0\";",
            "",
            "  /* Posting-Zeiten aus context/reels-framework.md. \U0001F6A8 Reels liegen abends,",
            "     und zwar NACH dem Einplan-Lauf um 20:00 — die alte Vorgabe 18:00 lag davor,",
            "     dadurch war ein am selben Tag freigegebenes Reel beim Einplanen immer schon",
            "     abgelaufen und wurde stillschweigend verworfen. */",
            "  function vorgabeZeit(art, profil) {",
            "    if (art !== \"reels\") return \"07:30\";",
            "    return profil === \"doterra\" ? \"21:30\" : \"21:00\";",
            "  }",
        ]),
        "A Vorgabezeit")

    # --- B · Das Feld auf die Karte ---------------------------------------
    t = ersetze(
        t,
        """        '<div class="wk-fuss">' +
          '<input type="date" value="' + esc(b.obj.datum || "") + '">' +""",
        """        '<div class="wk-fuss">' +
          '<input type="date" value="' + esc(b.obj.datum || "") + '">' +
          // Ohne dieses Feld war die Uhrzeit unsichtbar und kam aus einem Vorgabewert.
          '<input type="time" class="wk-zeit" value="' +
            esc((b.obj.blotato && b.obj.blotato.zeit) ||
                vorgabeZeit(b.art, (b.obj.blotato || {}).profil)) + '">' +""",
        "B Zeitfeld")

    # --- C · Nicht in die Index-Liste geraten lassen -----------------------
    t = ersetze(
        t,
        """    var felder = karte.querySelectorAll(".wk-fuss input, .wk-fuss button");""",
        "\n".join([
            "    // \U0001F6A8 Das Zeitfeld bleibt draussen: darunter wird ueber den Index",
            "    // angesprochen (felder[0] Datum, felder[1] Kopieren, letztes Freigeben).",
            """    var felder = karte.querySelectorAll(".wk-fuss input:not(.wk-zeit), .wk-fuss button");""",
        ]),
        "C Index schuetzen")

    # --- D · Aenderung merken ---------------------------------------------
    t = ersetze(
        t,
        """    var profilWahl = karte.querySelector(".wk-profil");
    if (profilWahl) {
      profilWahl.onchange = function () {
        var bl = b.obj.blotato || (b.obj.blotato = {});
        bl.profil = this.value;
        if (b.art === "reels") saveReel(b.obj); else saveCarousel(b.obj);
      };
    }""",
        """    var zeitFeld = karte.querySelector(".wk-zeit");
    if (zeitFeld) {
      zeitFeld.onchange = function () {
        var bl = b.obj.blotato || (b.obj.blotato = {});
        bl.zeit = this.value;
        merken();
      };
    }

    var profilWahl = karte.querySelector(".wk-profil");
    if (profilWahl) {
      profilWahl.onchange = function () {
        var bl = b.obj.blotato || (b.obj.blotato = {});
        bl.profil = this.value;
        // Die Vorgabezeit haengt am Profil — doTERRA postet spaeter. Eine selbst
        // gesetzte Zeit wird dabei nie ueberschrieben.
        if (!bl.zeit && zeitFeld) zeitFeld.value = vorgabeZeit(b.art, this.value);
        if (b.art === "reels") saveReel(b.obj); else saveCarousel(b.obj);
      };
    }""",
        "D Zeit merken")

    # --- E · Freigabe nimmt die echte Zeit und prueft sie -------------------
    t = ersetze(
        t,
        """      var bl = b.obj.blotato || (b.obj.blotato = {});
      var profil = bl.profil || "mentoring";
      var zeit = bl.zeit || (b.art === "reels" ? "18:00" : "07:30");
      var wann = new Date(b.obj.datum + "T" + zeit);""",
        """      var bl = b.obj.blotato || (b.obj.blotato = {});
      var profil = bl.profil || "mentoring";
      var zeit = (zeitFeld && zeitFeld.value) || bl.zeit || vorgabeZeit(b.art, profil);
      bl.zeit = zeit;
      var wann = new Date(b.obj.datum + "T" + zeit);

      // \U0001F6A8 Ein Zeitpunkt in der Vergangenheit wird von Blotato abgelehnt. Frueher
      // ist das erst beim naechtlichen Einplanen aufgefallen — also gar nicht, weil
      // die Freigabe trotzdem „geklappt“ gemeldet hat.
      var vorbei = !isNaN(wann) && wann.getTime() < Date.now();""",
        "E Zeit pruefen")

    t = ersetze(
        t,
        """          anzahl: anzahl,
          status: "wartet",
          updatedAt: new Date().toISOString()""",
        """          anzahl: anzahl,
          status: vorbei ? "zeitpunkt-vorbei" : "wartet",
          updatedAt: new Date().toISOString()""",
        "F Status setzen")

    t = ersetze(
        t,
        """          bl.status = "wartet";
          merken();
          toast("Freigegeben und abgelegt. Sag es mir im Chat, dann plane ich es ein.");
          render();""",
        """          bl.status = vorbei ? "zeitpunkt-vorbei" : "wartet";
          merken();
          toast(vorbei
            ? "Freigegeben — aber " + zeit + " am " + b.obj.datum + " ist vorbei. "
              + "Instagram nimmt keinen Zeitpunkt in der Vergangenheit. Stell die Uhrzeit "
              + "später oder das Datum auf morgen, dann geht es raus."
            : "Freigegeben für " + b.obj.datum + " um " + zeit
              + ". Wird um 20:00 eingeplant.");
          render();""",
        "G Rueckmeldung")

    ziel.write_text(t + "\n", encoding="utf-8")
    print(f"\nGeschrieben: {ziel}  ({len(t.splitlines())} Zeilen)")


if __name__ == "__main__":
    main()
