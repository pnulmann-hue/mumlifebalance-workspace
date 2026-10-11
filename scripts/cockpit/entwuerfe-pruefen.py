# -*- coding: utf-8 -*-
"""Prüft die Entwürfe im Bild-Editor und wirft die kaputte Generation raus.

Anlass (Patricia, 18.09.2026): *„ich habe da teilweise festgestellt, dass
komische sätze stehen in den vorbereiteten slides. die gar keinen sinn ergeben."*

**Der Befund:** In `daten/entwuerfe` lagen **zwei Generationen** derselben
KW38-Beiträge nebeneinander. Die ältere stammt aus einem Lauf, bei dem die
Umlaute umschrieben waren — und mit ihr kamen zusammengekürzte Sätze:

    alt  kw38-kar-fr-a      „Fuenf Beitraege ohne ein einziges Produkt."
    neu  kar-kw38-kar-fr-a  „Fünf Beiträge, die du posten kannst, ohne ein
                              Produkt zu zeigen."

    alt  kw38-kar-mi-a      Folie 7: „Zu klein heisst nur:" / „du kannst es
                              ohne Nachdenken."        ← Satz in zwei Hälften
    neu  kar-kw38-kar-mi-a  Folie 7: „Wenn der Satz sich zu klein anfühlt, ist
                              er meistens richtig."

🚨 **Die beiden sahen in der Liste fast gleich aus.** Untereinander in einem
Auswahlfeld mit über dreissig Zeilen fällt nicht auf, dass es denselben Beitrag
zweimal gibt — man erwischt die falsche Hälfte der Zeit die alte. Genau das ist
passiert.

**Drei Prüfungen, jede mit Gegenprobe:**

1. **Umschriebene Umlaute** — Wörter mit ae/oe/ue, in denen ein Umlaut gehört.
   🚨 Die Gegenprobe ist hier die halbe Arbeit: „bauen", „dauert", „Frauen",
   „heute", „neues", „zuerst", „Abenteuer" enthalten dieselben Buchstabenpaare
   völlig zu Recht. Ein Muster ohne diese Ausnahmeliste meldet bei jedem
   zweiten Satz etwas, und nach dem dritten Fehlalarm liest niemand mehr hin.
2. **Doppelte** — gleicher Tag, gleiche Art, gleiches Profil und mindestens
   60 % gemeinsame Wörter im Namen. Unter 60 % sind es zwei echte Varianten
   („Letzter Bestelltag — Sofa" und „— Handy" liegen bei 67 % und würden
   fälschlich anschlagen, deshalb entscheidet am Ende nicht die Zahl allein,
   sondern ob eine der beiden umschriebene Umlaute hat).
3. **Abgehackte Folien** — Text endet auf Doppelpunkt und die Unterzeile
   beginnt klein. Das ist nicht immer falsch („Was ich gemacht hab: nichts
   aufgegeben, sondern …" liest sich richtig), deshalb nur eine Meldung.

    python scripts/cockpit/entwuerfe-pruefen.py <entwuerfe.json>
    python scripts/cockpit/entwuerfe-pruefen.py <entwuerfe.json> --putzen <ziel.json>
"""
import argparse
import collections
import io
import json
import re
import sys

# Buchstabenpaare, die in echten deutschen Wörtern vorkommen. Ohne diese Liste
# ist die Prüfung wertlos — sie meldet dann alles.
HARMLOS = re.compile(
    r"(aue|eue|oeu|neu|heu|leu|freu|treu|dau|bau|schau|grau|blau|lau|sau|tau|"
    # „bequem/unbequemer" hat ein ue, das keins ist — beim ersten Lauf ueber die
    # Cockpit-Beitraege war das der einzige Treffer, und er war falsch.
    r"quem|queu|quee|jubel|museum|famil|sequenz)", re.I)
WORTAUSNAHMEN = {
    "aus", "auf", "auch", "zuerst", "aktuell", "aktuelle", "aktuellen",
    "Zuerst", "Aus", "Auf", "Auch", "Aktuell",
}


def umschrieben(text):
    """Wörter, in denen ein Umlaut zu ae/oe/ue geworden ist."""
    raus = []
    for w in re.findall(r"[A-Za-zÄÖÜäöüß]+", text):
        if w in WORTAUSNAHMEN:
            continue
        if re.search(r"[äöüÄÖÜ]", w):
            continue                      # hat schon echte Umlaute
        if not re.search(r"(ae|oe|ue)", w):
            continue
        if HARMLOS.search(w):
            continue
        raus.append(w)
    return sorted(set(raus))


def volltext(e):
    teile = [e.get("name") or "", e.get("cta") or ""]
    for f in (e.get("folien") or []):
        teile.append(f.get("text") or "")
        teile.append(f.get("unter") or "")
    return " ".join(teile)


def namenskern(s):
    s = (s or "").lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(a, b)
    return set(w for w in re.findall(r"[a-z0-9]+", s) if len(w) > 3)


def pruefen(eintraege):
    """Gibt (befunde, raus) zurueck — raus sind die ids der kaputten Generation."""
    befunde = []
    kaputt = {}
    for e in eintraege:
        w = umschrieben(volltext(e))
        if w:
            kaputt[e["id"]] = w
            befunde.append((1, e["id"], e.get("name", ""),
                            "umschriebene Umlaute: " + ", ".join(w[:6])))

    gruppen = collections.defaultdict(list)
    for e in eintraege:
        gruppen[(e.get("datum"), e.get("art"), e.get("profil"))].append(e)
    doppelt = []
    for schluessel, liste in sorted(gruppen.items(), key=lambda x: str(x[0])):
        for i in range(len(liste)):
            for j in range(i + 1, len(liste)):
                a, b = liste[i], liste[j]
                ka, kb = namenskern(a.get("name")), namenskern(b.get("name"))
                if not ka or not kb:
                    continue
                if len(ka & kb) / min(len(ka), len(kb)) < 0.6:
                    continue
                # 🚨 Nur wenn genau EINE der beiden kaputt ist, ist klar, welche
                # weg muss. Sonst sind es zwei echte Varianten (A und B).
                ka_kaputt, kb_kaputt = a["id"] in kaputt, b["id"] in kaputt
                if ka_kaputt != kb_kaputt:
                    weg = a if ka_kaputt else b
                    doppelt.append((weg["id"], (b if ka_kaputt else a)["id"]))
                    befunde.append((1, weg["id"], weg.get("name", ""),
                                    "Doppelt zu " + (b if ka_kaputt else a)["id"]))
                else:
                    befunde.append((2, a["id"], a.get("name", ""),
                                    "aehnlicher Name wie " + b["id"] +
                                    " — von Hand ansehen"))

    for e in eintraege:
        for i, f in enumerate(e.get("folien") or [], 1):
            t = (f.get("text") or "").strip()
            u = (f.get("unter") or "").strip()
            if t.endswith(":") and u and u[0].islower():
                befunde.append((2, e["id"], e.get("name", ""),
                                "Folie %d: Satz auf zwei Felder verteilt — "
                                "„%s“ + „%s…“" % (i, t, u[:40])))
    return befunde, set(kaputt)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("datei")
    p.add_argument("--putzen", metavar="ZIEL",
                   help="kaputte Generation entfernen und nach ZIEL schreiben")
    a = p.parse_args()

    with io.open(a.datei, encoding="utf-8") as f:
        d = json.load(f)
    eintraege = d.get("entwuerfe") or []
    befunde, raus = pruefen(eintraege)

    rot = [b for b in befunde if b[0] == 1]
    gelb = [b for b in befunde if b[0] == 2]
    print("%d Entwuerfe geprueft.\n" % len(eintraege))
    for stufe, name in ((rot, "\U0001f534 muss weg"), (gelb, "\U0001f7e0 ansehen")):
        if not stufe:
            continue
        print(name + ":")
        for _, eid, nm, was in stufe:
            print("  %-26s %-44s %s" % (eid, (nm or "")[:42], was))
        print()

    if not a.putzen:
        print("Nichts geschrieben. Mit --putzen <ziel.json> entfernen.")
        return
    if not raus:
        print("Nichts zu entfernen.")
        return
    d["entwuerfe"] = [e for e in eintraege if e["id"] not in raus]
    d["stand"] = d.get("stand", "")
    with io.open(a.putzen, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print("Entfernt: %d — %s" % (len(raus), ", ".join(sorted(raus))))
    print("Geschrieben: %s (%d Entwuerfe bleiben)" % (a.putzen, len(d["entwuerfe"])))


if __name__ == "__main__":
    main()
