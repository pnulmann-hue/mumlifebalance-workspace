# -*- coding: utf-8 -*-
"""Ordnet jedem Cover-Entwurf ein Shootingbild zu.

Aufruf:
    python scripts/cockpit/cover-fotos-zuordnen.py <entwuerfe.json> <ziel.json>

Danach das Ergebnis mit `ArtifactData set` als `daten/entwuerfe` in den
Bild-Editor schreiben.

**Wie zugeordnet wird:**
- Je Profil ein eigener Bildvorrat. Mentoring bekommt die Aufnahmen, in denen
  sie arbeitet oder zugewandt dasteht; doTERRA die ruhigen draussen.
- Reihum nach Datum, damit **an zwei Tagen hintereinander nie dasselbe Bild**
  steht. Innerhalb eines Tages bekommen A und B verschiedene Bilder — sonst
  sieht die Auswahl im Cockpit nach Kopie aus.
- Die Verlauffarbe wechselt Dunkelblau/Orange.

🚨 **Kein Petrol auf einem Cover.** Welche Beiträge Lead-Posts sind, steht im
Entwurf nicht drin, und Petrol ist auf Lead-Posts verboten
(`feedback_KRITISCH-petrol-cover-nicht-bei-leadposts`). Wo die Unterscheidung
fehlt, gilt die strengere Regel.

🚨 **Das ist ein Vorschlag, keine Festlegung.** Im Bild-Editor lassen sich
Bild, Text, Schriftgrösse und Höhe danach frei ändern.
"""
import datetime
import io
import json
import sys

# Dateiname -> was drauf ist, getrennt nach Stimmung.
#
# 🚨 Der Grund fuer die Trennung: beim ersten Lauf stand die lachende
# Pusteblume auf „Das wird schon wieder, du hast halt vier Kinder." Hat es
# nicht.« — einem Schmerz-Hook. Ein lachendes Gesicht widerspricht dem Satz
# darunter, und das faellt sofort auf. Ein Cover ist nicht nur Platzhalter
# fuer Text, das Bild sagt mit.
# 🚨 Nur wirklich heitere Aufnahmen sind gesperrt. Beim ersten Anlauf hatte ich
# je Profil drei „ruhige" und drei „offene" — und weil fast jeder Hook ein
# Schmerz-Hook ist, blieben drei Bilder fuer zwoelf Cover uebrig und
# wiederholten sich an aufeinanderfolgenden Tagen. Ein zu enger Vorrat ist
# genauso ein Fehler wie ein falsches Bild.
NUR_HEITER = {"s09.jpg", "s10.jpg"}     # Arme offen · Pusteblume lachend

VORRAT = {
    "mentoring": [("s04.jpg", "Oranges Kleid, Hand am Kinn, nachdenklich"),
                  ("s03.jpg", "Nahporträt mit Schal"),
                  ("s01.jpg", "Am Ufer mit Klemmbrett, arbeitend"),
                  ("s05.jpg", "Oranges Kleid am Pfosten, viel freie Fläche"),
                  ("s02.jpg", "Stehend mit Tasche, Bäume"),
                  ("s06.jpg", "Oranges Kleid auf dem Steg, sitzend")],
    "doterra":   [("s07.jpg", "Am Ufer auf dem Fels, Becher in der Hand"),
                  ("s08.jpg", "Fels am Wasser, Blick zur Seite"),
                  ("s12.jpg", "Im Gras, Lederjacke"),
                  ("s11.jpg", "Blumenkleid mit gelbem Schal"),
                  ("s09.jpg", "Wiese, Arme offen, von hinten"),
                  ("s10.jpg", "Pusteblume, lachend")],
}

# Ruhig ist die Vorgabe. Nur wenn der Satz erkennbar nach vorne zeigt, darf ein
# offenes Bild darunter. Umgekehrt waere es riskanter: ein heiterer Hook auf
# einem ruhigen Bild stoert niemanden, andersherum schon.
import re
VORWAERTS = re.compile(
    r"\b(geändert|verändert|besser|zurückgekommen|funktioniert|geholfen|"
    r"gelernt|endlich|seitdem|heute nicht mehr|dabei|freu|geschafft|"
    r"kostet nichts|kostenlos|erste[rn]? Schritt)\b", re.I)

FARBEN = ["#1E3A4C", "#D6832F"]     # Dunkelblau, Orange — kein Petrol

# Cover-Hook: kurz und gross. Hoehe 58 % haelt ihn aus beiden toten Zonen.
# 🚨 Verlauf 62 statt 76: bei 76 lag ein oranger Schleier ueber dem ganzen
# Foto, und von den Shootingbildern blieb kaum etwas uebrig.
FS, POS, GRAD = 80, 58, 62


def vortagVon(iso):
    """Der kalendarische Vortag. Leerer String, wenn das Datum unbrauchbar ist."""
    try:
        return (datetime.date.fromisoformat(iso) - datetime.timedelta(days=1)).isoformat()
    except Exception:
        return ""


def folgetag(a, b):
    """Liegen die beiden Tage direkt nebeneinander?"""
    try:
        return (datetime.date.fromisoformat(b)
                - datetime.date.fromisoformat(a)).days == 1
    except Exception:
        return False


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    quelle, ziel = sys.argv[1], sys.argv[2]
    with io.open(quelle, encoding="utf-8") as f:
        d = json.load(f)

    cover = [e for e in d.get("entwuerfe", []) if e.get("art") == "cover"]
    cover.sort(key=lambda e: (e.get("profil") or "", e.get("datum") or "",
                              e.get("name") or ""))

    # Gierig statt reihum: fuer jedes Cover das erlaubte Bild nehmen, das am
    # laengsten nicht dran war und weder heute noch gestern schon vorkommt.
    # Reihum scheitert, sobald die Zahl der Cover pro Tag wechselt.
    zuletzt = {}                       # (profil, foto) -> laufende Nummer
    proTag = {}                        # (profil, datum) -> {fotos}
    lauf = 0
    gesetzt = 0
    for e in cover:
        p = e.get("profil") or "mentoring"
        tag = e.get("datum") or ""
        text = " ".join((f.get("text") or "") + " " + (f.get("unter") or "")
                        for f in (e.get("folien") or []))
        heiter_ok = bool(VORWAERTS.search(text))
        stimmung = "offen" if heiter_ok else "ruhig"

        # 🚨 „Vortag" heisst der KALENDARISCHE Vortag, nicht der letzte Tag mit
        # einem Beitrag. Sonst gelten der 16. und der 18. als aufeinanderfolgend,
        # obwohl zwei Feed-Tage dazwischenliegen — und die Sperre engt den
        # Vorrat ohne Grund ein.
        gesperrt = set(proTag.get((p, tag), set())) | set(proTag.get((p, vortagVon(tag)), set()))

        erlaubt = [(d, w) for d, w in VORRAT[p]
                   if heiter_ok or d not in NUR_HEITER]
        frei = [(d, w) for d, w in erlaubt if d not in gesperrt]
        if not frei:                   # Vorrat zu klein — dann wenigstens nicht am selben Tag
            frei = [(d, w) for d, w in erlaubt
                    if d not in proTag.get((p, tag), set())] or erlaubt
        datei, was = min(frei, key=lambda x: zuletzt.get((p, x[0]), -1))

        lauf += 1
        zuletzt[(p, datei)] = lauf
        proTag.setdefault((p, tag), set()).add(datei)
        e["foto"] = datei
        e["fotoText"] = was
        e["farbe"] = FARBEN[gesetzt % len(FARBEN)]
        e["grad"] = GRAD
        e["fs"] = FS
        e["pos"] = POS
        e["_stimmung"] = stimmung          # nur fuer die Ausgabe
        gesetzt += 1

    # Gegenprobe: an keinem Tag zweimal dasselbe Bild, und nie zwei Tage in Folge.
    fehler = []
    for p in ("mentoring", "doterra"):
        reihe = [e for e in cover if (e.get("profil") or "mentoring") == p]
        proTag = {}
        for e in reihe:
            proTag.setdefault(e.get("datum") or "", []).append(e["foto"])
        for tag, fotos in proTag.items():
            if len(fotos) != len(set(fotos)):
                fehler.append("%s %s: zweimal dasselbe Bild am selben Tag" % (p, tag))
        tage = sorted(proTag)
        for a, b in zip(tage, tage[1:]):
            if not folgetag(a, b):
                continue          # zwei Tage Abstand reicht, das faellt niemandem auf
            gleich = set(proTag[a]) & set(proTag[b])
            if gleich:
                fehler.append("%s %s/%s: %s an zwei Tagen in Folge"
                              % (p, a, b, ", ".join(sorted(gleich))))

    for e in cover:
        print("  %-9s %s  %-6s %-32s %s"
              % (e.get("profil") or "—", e.get("datum") or "—",
                 e["_stimmung"], (e.get("name") or "")[:30], e["foto"]))
    print("\n%d Cover mit Bildvorschlag." % gesetzt)
    for f_ in fehler:
        print("  🚨 " + f_)
    if fehler:
        sys.exit("\nAbgebrochen — Zuordnung wiederholt sich.")

    for e in cover:
        e.pop("_stimmung", None)
    with io.open(ziel, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print("Geschrieben: %s" % ziel)


if __name__ == "__main__":
    main()
