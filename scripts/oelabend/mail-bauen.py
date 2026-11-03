"""Öl-Abend: Nachfass-Mail für alle, die „eine Nacht darüber schlafen“ angekreuzt haben.

Das Gerüst (Outlook-Tabellen, Farben, Fuss) kommt aus scripts/startklar/mails-bauen.py
und wird importiert, nicht kopiert. Dieses Skript ist die Quelle des Wortlauts; es
schreibt HTML zum Einfügen in ActiveCampaign und eine Markdown-Fassung zum Lesen.

    python scripts/oelabend/mail-bauen.py
"""
import html
import importlib.util
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("sk", ROOT / "scripts/startklar/mails-bauen.py")
sk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sk)
absatz, kasten, ps, gruss = sk.absatz, sk.kasten, sk.ps, sk.gruss

ZIEL = ROOT / "outputs" / "doterra-strategie" / "oelabend"

ANTWORTEN = kasten(
    sk.P_ENG % "<strong>BESTELLEN</strong>: Ich schicke dir den Link, und wir gehen die Bestellung zusammen durch."
    + sk.P_ENG % "<strong>ABEND</strong>: Wir suchen einen Termin für einen Öl-Abend bei dir."
    + sk.P_ENG % "<strong>FRAGE</strong>: Schreib sie gleich dazu, ich antworte dir persönlich.",
    "#fdf1e6", rand=sk.ORANGE, kopf="Antworte mir mit einem Wort", kopffarbe=sk.ORANGE)

MAIL = {
    "datei": "mail-ueberschlafen.html",
    "marke": "Mum Life Balance · Öl-Abend",
    "betreff": "Hast du gut darüber geschlafen?",
    "betreff2": "Ein Wort als Antwort genügt",
    "preheader": "Ein Wort als Antwort genügt, den Rest machen wir zusammen.",
    "wann": "2 Tage nach dem Öl-Abend, nur wenn „Ich schlafe noch eine Nacht darüber“ angekreuzt ist",
    "notiz": """
Auslöser: Tag „Öl-Abend“ (Formular 77)
Bedingung: Feld „Öl-Abend · Mein nächster Schritt“ enthält „Ich schlafe noch eine Nacht darüber“
Warten: 2 Tage
""",
    "h1": "Hast du gut darüber geschlafen?",
    "bloecke": [
        absatz("Hallo %FIRSTNAME%,"),
        absatz("danke dir nochmals für den Öl-Abend. Du hast angekreuzt, dass du noch eine Nacht "
               "darüber schlafen willst, und das finde ich ganz ganz gut so. Wer sich Zeit lässt, "
               "kauft am Ende das, was sie dann auch wirklich benutzt."),
        absatz("Und genau da liegt der Punkt, an dem ich dich gern abholen möchte. Angenommen, die "
               "Fläschchen stehen nächste Woche bei dir im Regal: Dann ist die grosse Frage meistens, "
               "wann du im Alltag überhaupt daran denkst. Sonst wird aus der Hausapotheke einfach ein sehr hübsches Regal."),
        absatz("Darum bekommst du von mir mein Programm „Mama wird Hausapothekerin“ dazu, wenn du die "
               "Hausapotheke über mich bestellst. Ein Workbook, kurze Videos und dein eigener Plan für "
               "morgens und abends, damit die Öle ihren festen Platz in deinem Tag finden."),
        absatz("Und falls dir der Abend so gefallen hat, dass du ihn deinen Freundinnen gönnen magst: "
               "Ich komme auch zu dir. Du lädst ein, ich bringe die Öle mit, und als Dankeschön "
               "bekommst du von mir ein Gastgeberinnen-Geschenk."),
        ANTWORTEN,
        absatz("Und wenn es gerade nicht passt, ist das völlig okay. Kein Druck, die Öle laufen dir "
               "nicht davon.", letzter=True),
        gruss("Herzlich,"),
        ps("Falls du am Abend dein Lieblingsöl gefunden hast und lieber klein anfangen magst: "
           "Ein einzelnes Fläschchen geht auch. Schreib mir einfach, welches."),
    ],
}


def markdown(m):
    teile = []
    for b in m["bloecke"]:
        t = re.sub(r"<br\s*/?>", "\n", b)
        t = re.sub(r"</p>", "\n\n", t)
        t = re.sub(r"<strong>(.*?)</strong>", r"**\1**", t)
        t = html.unescape(re.sub(r"<[^>]+>", "", t))
        t = "\n".join(z.strip() for z in t.splitlines())
        teile.append(re.sub(r"\n{3,}", "\n\n", t).strip())
    return f"""---
tags: [doterra, mail]
---

# Öl-Abend · Nachfass-Mail „überschlafen“

| | |
|---|---|
| Betreff | {m['betreff']} |
| Zweiter Betreff (Test) | {m['betreff2']} |
| Vorschautext | {m['preheader']} |
| Wann | {m['wann']} |

Quelle: `scripts/oelabend/mail-bauen.py` — dort ändern, nicht hier.

---

""" + "\n\n".join(t for t in teile if t) + "\n"


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    seite = sk.bauen(MAIL)
    (ZIEL / MAIL["datei"]).write_text(seite, encoding="utf-8")
    md = ZIEL / "2026-11-03-mail-ueberschlafen.md"
    md.write_text(markdown(MAIL), encoding="utf-8")
    sk.umlaute_pruefen(MAIL["datei"], seite)
    print("→", ZIEL / MAIL["datei"])
    print("→", md)


if __name__ == "__main__":
    main()
