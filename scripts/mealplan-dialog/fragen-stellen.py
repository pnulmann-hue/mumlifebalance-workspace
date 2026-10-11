# -*- coding: utf-8 -*-
"""Der Assistent fragt, bevor er plant.

    python scripts/mealplan-dialog/fragen-stellen.py [--probe]

Er fragt NUR, was er nicht wissen kann. Alles andere steht schon in seinem
Auftrag: sechs Personen, die Makros, die Verbote (kein Spinat, kein Feta,
kein Fisch ausser Thunfisch kalt), die Migros-Aktionen, und was in den
letzten vier Wochen schon auf dem Tisch stand.

Genau das ist der Unterschied zu einem Chat: ein Chat muesste alles fragen.
"""
import io, os, sys, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import telegram

# Windows-Konsole ist cp1252 und kann weder Emoji noch Umlaute ausgeben.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HIER = os.path.dirname(os.path.abspath(__file__))
MERKZETTEL = os.path.join(HIER, "offene-frage.json")

FRAGEN = [
    "1. An wie vielen Abenden seid ihr daheim?",
    "2. Was muss weg \u2014 aus dem K\u00fchlschrank oder vom Beet?",
    "3. Gibt es einen Tag, an dem es schnell gehen muss?",
    "4. Worauf h\u00e4ttest du Lust?",
]


def kw_von(d):
    return d.isocalendar()[1]


def naechste_woche(heute=None):
    heute = heute or datetime.date.today()
    montag = heute + datetime.timedelta(days=(7 - heute.weekday()))
    return montag, montag + datetime.timedelta(days=6)


def nachricht(heute=None):
    mo, so = naechste_woche(heute)
    kopf = "Essensplan f\u00fcr KW %d (%s. bis %s. %s)" % (
        kw_von(mo), mo.day, so.day,
        ["Januar","Februar","M\u00e4rz","April","Mai","Juni","Juli","August",
         "September","Oktober","November","Dezember"][so.month - 1])
    return (
        "\U0001f37d  %s\n\n"
        "Vier Fragen, dann baue ich ihn. Antworte einfach in einer Nachricht \u2014 "
        "in Stichworten reicht.\n\n%s\n\n"
        "Den Rest weiss ich: sechs Portionen, deine Makros, kein Spinat, kein Feta, "
        "Fisch nur kalt als Thunfisch, die Aktionen bei der Migros und was in den "
        "letzten vier Wochen schon dran war.\n\n"
        "Wenn du nicht antwortest, plane ich einfach eine normale Woche."
        % (kopf, "\n".join(FRAGEN)))


def main():
    probe = "--probe" in sys.argv
    mo, so = naechste_woche()
    text = nachricht()
    if probe:
        print(text)
        print("\n(Probelauf \u2014 nichts geschickt.)")
        return
    mid = telegram.senden(text)
    io.open(MERKZETTEL, "w", encoding="utf-8").write(json.dumps({
        "gefragt_am": datetime.datetime.now().isoformat(timespec="seconds"),
        "message_id": mid,
        "kw": kw_von(mo),
        "von": mo.isoformat(),
        "bis": so.isoformat(),
        "beantwortet": False,
    }, ensure_ascii=False, indent=2))
    print("Fragen f\u00fcr KW %d geschickt (Nachricht %d)." % (kw_von(mo), mid))
    print("Merkzettel:", MERKZETTEL)


if __name__ == "__main__":
    main()
