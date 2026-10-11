# -*- coding: utf-8 -*-
"""Nur Sprechreels und Karussells gehen ueber Blotato. B-Roll postet Patricia selbst.

**Patricia, 16.09.2026:** *„du musst nur sprechreels und karussells über blotato
einplanen. b-roll mach ich wegen der musik selber"*

**Der Grund ist die Musik.** Instagram-Audio laesst sich nur in der App selbst
auswaehlen; ein ueber die Schnittstelle eingeplanter Beitrag kommt ohne Ton-Auswahl
raus. Bei einem B-Roll-Reel ist die Musik aber der halbe Beitrag — ein Clip von sieben
Sekunden ohne Ton traegt nichts.

**Zwei Dinge kommen dazu:**

1. **Feld `videoart`** an jedem Reel: `sprech` oder `broll`, mit einer Auswahl direkt
   auf der Wochenkarte. Vorher liess sich das nur aus dem Hinweistext erraten — und
   Raten reicht nicht, wenn daran haengt, ob ein Beitrag automatisch rausgeht.
2. **Der Freigabe-Knopf verzweigt.** Bei `broll` wird `status: "selber-posten"`
   abgelegt statt `"wartet"`. Der Task `freigaben-einplanen-2000` sucht nur nach
   `"wartet"` und laesst B-Roll damit in Ruhe.

## 🚨 Und ein Knopf gegen den Doppelpost

Am 16.09. hat Patricia das Dienstags-Reel von Hand ueber die App gepostet, die Freigabe
stand aber weiter auf `"wartet"`. Ohne Eingriff haette der Task es um 20:00 **ein
zweites Mal** eingeplant. Deshalb gibt es jetzt **„Hab ich selbst gepostet“** auf jeder
freigegebenen Karte — setzt `gepostet-von-hand` und nimmt den Beitrag damit aus dem
Einplan-Lauf.

    python scripts/cockpit/patch-videoart.py <html> <html>
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

    # --- A · Auswahl und Knopf auf die Karte ------------------------------
    t = ersetze(
        t,
        """        auftragsZeile(b.obj) +""",
        "\n".join([
            "        // \U0001F6A8 Nur Sprechreels und Karussells gehen ueber Blotato. B-Roll",
            "        // postet Patricia selbst, weil die Instagram-Musik nur in der App",
            "        // waehlbar ist — und bei einem Sieben-Sekunden-Clip ist die Musik",
            "        // der halbe Beitrag.",
            "        (b.art === \"reels\"",
            "          ? '<div class=\"wk-auftrag\"><select class=\"btn wk-videoart\">' +",
            "              '<option value=\"sprech\"' +",
            "                ((b.obj.videoart || \"sprech\") === \"broll\" ? \"\" : \" selected\") +",
            "                '>Sprechreel — geht über Blotato raus</option>' +",
            "              '<option value=\"broll\"' +",
            "                ((b.obj.videoart || \"sprech\") === \"broll\" ? \" selected\" : \"\") +",
            "                '>B-Roll — poste ich selbst (Musik)</option>' +",
            "            '</select></div>'",
            "          : \"\") +",
            "        auftragsZeile(b.obj) +",
        ]),
        "A Auswahl Videoart")

    t = ersetze(
        t,
        """          '<button class="btn' + (b.obj.textfrei ? "" : " primary") + '">' +
            (b.obj.textfrei ? "Freigabe zurücknehmen" : "Freigeben") + '</button>' +""",
        "\n".join([
            """          '<button class="btn' + (b.obj.textfrei ? "" : " primary") + '">' +""",
            """            (b.obj.textfrei ? "Freigabe zurücknehmen" : "Freigeben") + '</button>' +""",
            "          // Nach einem Handy-Post muss der Beitrag aus dem Einplan-Lauf raus,",
            "          // sonst steht er zweimal im Feed.",
            "          (b.obj.textfrei && b.art !== \"storys\"",
            "            ? '<button class=\"btn wk-selbst\">Hab ich selbst gepostet</button>'",
            "            : \"\") +",
        ]),
        "B Knopf selbst gepostet")

    # --- C · Verdrahtung ---------------------------------------------------
    t = ersetze(
        t,
        """    var zeitFeld = karte.querySelector(".wk-zeit");""",
        "\n".join([
            "    var artWahl = karte.querySelector(\".wk-videoart\");",
            "    if (artWahl) {",
            "      artWahl.onchange = function () {",
            "        b.obj.videoart = this.value;",
            "        merken();",
            "        toast(this.value === \"broll\"",
            "          ? \"B-Roll — wird nicht eingeplant, du postest ihn selbst.\"",
            "          : \"Sprechreel — geht über Blotato raus.\");",
            "        render();",
            "      };",
            "    }",
            "",
            "    var selbstKnopf = karte.querySelector(\".wk-selbst\");",
            "    if (selbstKnopf) {",
            "      selbstKnopf.onclick = function () {",
            "        var bl2 = b.obj.blotato || (b.obj.blotato = {});",
            "        bl2.status = \"gepostet-von-hand\";",
            "        merken();",
            "        if (db) {",
            "          db.collection(\"freigaben\").doc(b.id).set({",
            "            name: b.titel, status: \"gepostet-von-hand\",",
            "            notiz: \"Von Patricia selbst über die Instagram-App gepostet.\",",
            "            updatedAt: new Date().toISOString()",
            "          }, { merge: true }).catch(function () {});",
            "        }",
            "        toast(\"Notiert — der Beitrag wird nicht mehr eingeplant.\");",
            "        render();",
            "      };",
            "    }",
            "",
            """    var zeitFeld = karte.querySelector(".wk-zeit");""",
        ]),
        "C Verdrahtung")

    # --- D · Die Freigabe verzweigt ---------------------------------------
    t = ersetze(
        t,
        """      if (!db) { toast("Freigegeben — aber ohne Datenbank nur lokal."); render(); return; }""",
        "\n".join([
            '      if (!db) { toast("Freigegeben — aber ohne Datenbank nur lokal."); render(); return; }',
            "",
            "      // \U0001F6A8 B-Roll geht nie ueber Blotato: die Instagram-Musik laesst sich nur",
            "      // in der App waehlen, und ohne sie traegt ein Sieben-Sekunden-Clip nicht.",
            "      var selberPosten = (b.art === \"reels\" && b.obj.videoart === \"broll\");",
        ]),
        "D Verzweigung erkennen")

    t = ersetze(
        t,
        """          status: vorbei ? "zeitpunkt-vorbei" : "wartet",""",
        """          status: selberPosten ? "selber-posten"
                  : (vorbei ? "zeitpunkt-vorbei" : "wartet"),""",
        "E Status beim Ablegen")

    t = ersetze(
        t,
        """          bl.status = vorbei ? "zeitpunkt-vorbei" : "wartet";
          merken();
          toast(vorbei""",
        "\n".join([
            '          bl.status = selberPosten ? "selber-posten"',
            '                     : (vorbei ? "zeitpunkt-vorbei" : "wartet");',
            "          merken();",
            "          if (selberPosten) {",
            "            toast(\"Freigegeben. B-Roll planen wir nicht ein — lad ihn dir \" +",
            "                  \"aufs Handy und poste ihn mit deiner Musik.\");",
            "            render();",
            "            return;",
            "          }",
            "          toast(vorbei",
        ]),
        "F Rueckmeldung")

    # --- G · Feld speichern und lesen --------------------------------------
    t = ersetze(
        t,
        """        texty: (typeof r.texty === "number") ? r.texty : null,""",
        """        videoart: r.videoart || "sprech",
        texty: (typeof r.texty === "number") ? r.texty : null,""",
        "G saveReel")

    t = ersetze(
        t,
        """texty: (typeof d0.texty === "number") ? d0.texty : null,""",
        """videoart: d0.videoart || "sprech", texty: (typeof d0.texty === "number") ? d0.texty : null,""",
        "H Reels lesen")

    ziel.write_text(t + "\n", encoding="utf-8")
    print(f"\nGeschrieben: {ziel}  ({len(t.splitlines())} Zeilen)")


if __name__ == "__main__":
    main()
