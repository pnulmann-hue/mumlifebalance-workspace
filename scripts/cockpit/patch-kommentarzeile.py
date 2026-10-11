# -*- coding: utf-8 -*-
"""Eine Zeile je Beitrag, in die Patricia schreibt, was geaendert werden soll.

**Patricia, 16.09.2026:** *„wäre es auch möglich eine kommentarzeile reinzutippen, die du
dann ausliest? wenn mir z.B. das video nicht gefällt oder du die caption neu schreiben
sollst? und das automatisch siehst anpasst und mir wieder aktualisierst und auf telegram
schreibst, dass der beitrag aktualisiert wurde und zur freigabe steht?"*

Bisher lief jede Korrektur über den Chat: Beitrag suchen, beschreiben, welchen sie meint,
warten. Jetzt steht die Zeile an der Karte, und der Beitrag ist damit eindeutig.

**Vier Felder am Beitrag:**

| Feld | wer schreibt | was drin steht |
|---|---|---|
| `kommentar` | Patricia | was geaendert werden soll |
| `kommentarStand` | Cockpit | wann sie es geschrieben hat (ISO) |
| `kommentarErledigt` | Claude | wann es eingearbeitet wurde (ISO) |
| `kommentarAntwort` | Claude | was tatsaechlich geaendert wurde |

**Offen heisst:** `kommentar` ist gefuellt und `kommentarErledigt` fehlt oder ist aelter
als `kommentarStand`. 🚨 **Der Vergleich muss ueber die Zeitstempel laufen, nicht ueber
ein Haekchen** — sonst bleibt ein zweiter Kommentar zum selben Beitrag unbemerkt, weil
der erste schon als erledigt markiert ist.

Der Kommentar wird beim Einarbeiten **nicht geloescht**. Er bleibt als Verlauf stehen,
damit man sieht, was gewuenscht war und was daraus wurde.

Abgeholt wird das vom Scheduled Task `kommentare-einarbeiten`
(`reference/scheduled-task-kommentare.md`).

    python scripts/cockpit/patch-kommentarzeile.py <html> <html>
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

    # --- A · Aussehen -----------------------------------------------------
    t = ersetze(
        t,
        "  .wk-unter { font-size: 13px; color: var(--ink-soft); }",
        "\n".join([
            "  .wk-unter { font-size: 13px; color: var(--ink-soft); }",
            "  /* Die Auftragszeile an Claude. Sitzt ueber der Fusszeile und nicht darin,",
            "     weil die Fusszeile ihre Knoepfe ueber den Index anspricht — ein",
            "     zusaetzliches Feld darin wuerde Datum, Kopieren und Freigeben",
            "     durcheinanderbringen. */",
            "  .wk-auftrag { display: flex; gap: 8px; align-items: center;"
            " margin: 10px 0 4px; flex-wrap: wrap; }",
            "  .wk-auftrag input { flex: 1 1 260px; min-width: 0; padding: 8px 10px;"
            " border: 1px solid var(--linie); border-radius: 8px; font: inherit;"
            " font-size: 14px; background: #fff; }",
            "  .wk-auftrag input:focus { outline: 2px solid var(--petrol);"
            " outline-offset: -1px; }",
            "  .wk-warte { border-left: 3px solid var(--orange); background: #fdf3e8;"
            " padding: 8px 10px; border-radius: 0 8px 8px 0; font-size: 13px;"
            " margin: 6px 0; }",
            "  .wk-erledigt { border-left: 3px solid var(--petrol); background: #eaf4f5;"
            " padding: 8px 10px; border-radius: 0 8px 8px 0; font-size: 13px;"
            " margin: 6px 0; }",
        ]),
        "A Aussehen")

    # --- B · Die Zeile in die Karte ---------------------------------------
    t = ersetze(
        t,
        """        '<div class="wk-fuss">' +
          '<input type="date" value="' + esc(b.obj.datum || "") + '">' +""",
        """        auftragsZeile(b.obj) +
        '<div class="wk-fuss">' +
          '<input type="date" value="' + esc(b.obj.datum || "") + '">' +""",
        "B Zeile einsetzen")

    # --- C · Der Baustein dafuer ------------------------------------------
    t = ersetze(
        t,
        """  var BILDEDITOR = \"https://claude.ai/code/artifact/21e66e0e-2576-41db-8c8d-f14d7079a1e0\";""",
        "\n".join([
            """  var BILDEDITOR = "https://claude.ai/code/artifact/21e66e0e-2576-41db-8c8d-f14d7079a1e0";""",
            "",
            "  /* ---------- Auftragszeile an Claude ----------",
            "     Patricia tippt hinein, was geaendert werden soll. Der Scheduled Task",
            "     `kommentare-einarbeiten` liest es, arbeitet es ein, traegt Antwort und",
            "     Zeitstempel nach und meldet per Telegram.",
            "     \U0001F6A8 Offen/erledigt wird ueber die ZEITSTEMPEL entschieden, nicht ueber",
            "     ein Haekchen — sonst bleibt ein zweiter Kommentar zum selben Beitrag",
            "     unbemerkt, weil der erste noch als erledigt markiert ist. */",
            "  function auftragOffen(o) {",
            "    if (!o || !(o.kommentar || \"\").trim()) return false;",
            "    if (!o.kommentarErledigt) return true;",
            "    return (o.kommentarStand || \"\") > o.kommentarErledigt;",
            "  }",
            "  function auftragsZeile(o) {",
            "    var offen = auftragOffen(o), s = \"\";",
            "    if (offen) {",
            "      s += '<div class=\"wk-warte\">⏳ <b>Bei Claude:</b> „' +",
            "        esc(o.kommentar) + '“<br>Wird bis 20:00 eingearbeitet, ' +",
            "        'du bekommst eine Telegram-Nachricht.</div>';",
            "    } else if ((o.kommentarAntwort || \"\").trim()) {",
            "      s += '<div class=\"wk-erledigt\">✅ <b>Geaendert:</b> ' +",
            "        esc(o.kommentarAntwort) + '</div>';",
            "    }",
            "    s += '<div class=\"wk-auftrag\">' +",
            "      '<input type=\"text\" class=\"wk-kommentar\" value=\"' +",
            "        esc(offen ? \"\" : (o.kommentar || \"\")) + '\" ' +",
            "        'placeholder=\"Was soll ich ändern? z.B. Caption neu schreiben, ' +",
            "        'Video passt nicht, Hook zu brav\">' +",
            "      '<button class=\"btn wk-senden\">An Claude</button>' +",
            "      '</div>';",
            "    return s;",
            "  }",
        ]),
        "C Baustein")

    # --- D · Verdrahtung ---------------------------------------------------
    t = ersetze(
        t,
        """    var felder = karte.querySelectorAll(".wk-fuss input, .wk-fuss button");""",
        "\n".join([
            "    // Ueber die Klasse angesprochen, nicht ueber den Index — sonst haengt es",
            "    // daran, in welcher Reihenfolge die Knoepfe stehen.",
            "    var kommentarFeld = karte.querySelector(\".wk-kommentar\");",
            "    var sendeKnopf = karte.querySelector(\".wk-senden\");",
            "    if (kommentarFeld && sendeKnopf) {",
            "      sendeKnopf.onclick = function () {",
            "        var txt = kommentarFeld.value.trim();",
            "        if (!txt) { toast(\"Schreib zuerst hinein, was ich ändern soll.\"); return; }",
            "        b.obj.kommentar = txt;",
            "        b.obj.kommentarStand = new Date().toISOString();",
            "        merken();",
            "        render();",
            "        toast(\"Notiert. Ich arbeite das bis 20:00 ein und melde mich per Telegram.\");",
            "      };",
            "      kommentarFeld.onkeydown = function (e) {",
            "        if (e.key === \"Enter\") { e.preventDefault(); sendeKnopf.click(); }",
            "      };",
            "    }",
            "",
            """    var felder = karte.querySelectorAll(".wk-fuss input, .wk-fuss button");""",
        ]),
        "D Verdrahtung")

    ziel.write_text(t + "\n", encoding="utf-8")
    print(f"\nGeschrieben: {ziel}  ({len(t.splitlines())} Zeilen)")


if __name__ == "__main__":
    main()
