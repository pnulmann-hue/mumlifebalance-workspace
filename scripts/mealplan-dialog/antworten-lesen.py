# -*- coding: utf-8 -*-
"""Liest Patricias Antwort auf die vier Fragen.

    python scripts/mealplan-dialog/antworten-lesen.py
    python scripts/mealplan-dialog/antworten-lesen.py --warten 120

Gibt die Antwort als Text aus und schreibt sie nach antwort-kw<NN>.md,
damit der Plan-Bau sie lesen kann.

Zwei Dinge, die hier schiefgehen koennen und deshalb geprueft werden:

* Es kommt NICHTS. Dann sagt das Skript das und nennt den Grund. Eine leere
  Antwort darf nie wie eine gegebene aussehen.
* Es kommen aeltere Nachrichten mit. getUpdates liefert alles seit dem
  letzten Abholen, auch von vorletzter Woche. Gezaehlt wird nur, was NACH
  dem Zeitpunkt der Frage kam.
"""
import io, os, sys, json, time, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import telegram

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HIER = os.path.dirname(os.path.abspath(__file__))
MERKZETTEL = os.path.join(HIER, "offene-frage.json")


def merkzettel():
    if not os.path.exists(MERKZETTEL):
        raise SystemExit(
            "Keine offene Frage. Erst fragen-stellen.py laufen lassen.")
    return json.loads(io.open(MERKZETTEL, encoding="utf-8").read())


def hole(seit_ts, nach_mid):
    """Alle eigenen Textnachrichten, die nach der Frage kamen."""
    antwort = telegram.ruf("getUpdates?timeout=0&limit=100")
    if not antwort.get("ok"):
        raise SystemExit("Telegram: %s" % antwort.get("description"))
    raus = []
    for u in antwort.get("result", []):
        n = u.get("message") or u.get("edited_message") or {}
        text = (n.get("text") or "").strip()
        if not text or n.get("from", {}).get("is_bot"):
            continue
        if n.get("message_id", 0) <= nach_mid:      # vor der Frage
            continue
        if n.get("date", 0) < seit_ts:
            continue
        raus.append((n["date"], n["message_id"], text))
    raus.sort()
    return raus


def main():
    m = merkzettel()
    gefragt = datetime.datetime.fromisoformat(m["gefragt_am"])
    seit_ts = int(gefragt.timestamp())
    warten = 0
    if "--warten" in sys.argv:
        warten = int(sys.argv[sys.argv.index("--warten") + 1])

    ende = time.time() + warten
    while True:
        treffer = hole(seit_ts, m["message_id"])
        if treffer or time.time() >= ende:
            break
        time.sleep(5)

    if not treffer:
        print("Noch keine Antwort auf die Fragen von %s." % m["gefragt_am"])
        print("Der Plan wird als normale Woche gebaut.")
        return 1

    text = "\n".join(t for _, _, t in treffer)
    ziel = os.path.join(HIER, "antwort-kw%02d.md" % m["kw"])
    io.open(ziel, "w", encoding="utf-8", newline="\n").write(
        "---\ntags: [mealplan]\n---\n\n"
        "# Antworten f\u00fcr KW %02d (%s bis %s)\n\n"
        "Gefragt am %s, beantwortet in %d Nachricht%s.\n\n%s\n"
        % (m["kw"], m["von"], m["bis"], m["gefragt_am"],
           len(treffer), "" if len(treffer) == 1 else "en", text))

    m["beantwortet"] = True
    m["antwort_datei"] = os.path.basename(ziel)
    io.open(MERKZETTEL, "w", encoding="utf-8").write(
        json.dumps(m, ensure_ascii=False, indent=2))

    print("Antwort f\u00fcr KW %02d:" % m["kw"])
    print("-" * 60)
    print(text)
    print("-" * 60)
    print("Gespeichert:", ziel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
