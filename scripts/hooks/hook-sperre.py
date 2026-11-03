#!/usr/bin/env python3
"""Die Hook-Sperre: kein Hook wird gebaut oder ins Cockpit gelegt, der nicht bestanden hat.

Patricia, 01.11.2026: *„was muss ich tun, damit wirklich jeder hook geprüft wird??
wir haben das ja nun schon xmal besprochen“*. Bis dahin hing die Prüfung daran, dass
Claude an sie denkt. Beim Paar vom 6.11. hat genau das gefehlt: es kam aus der ersten
Runde und ging ungeprüft ins November-Set. Eine Regel in einer Anleitung schützt nicht.

Zwei Stufen je Hook (ganzer Satz, so wie er im Bild steht):

1. **Maschine:** 10–14 Wörter · Blackliste über `texte-pruefen.py` (Hook und Caption) ·
   kein Werkzeug im Hook · Schweizer ss · Stichwort nur im letzten Caption-Absatz.
2. **Zweiter Blick:** ein eigener Claude-Aufruf bekommt nur die Pflichtregeln aus
   `/content` (Garten, Sandra, Pflichtregeln, TEIL 3) und den Hook — nicht die
   Begründung dessen, der ihn geschrieben hat. Eine Antwort mit Nein = gesperrt.

Das Ergebnis steht in der Quelle unter `pruefung.<a|b>` samt Fingerabdruck des Satzes.
Ändert sich ein Hook, passt der Fingerabdruck nicht mehr, und der Hook ist wieder gesperrt.
`radar-brolls.py` und `testreels-ins-cockpit.py` rufen `freigabe()` und brechen sonst ab.

    python scripts/hooks/hook-sperre.py                 # alle ungeprüften/geänderten
    python scripts/hooks/hook-sperre.py --nur 06,10     # einzelne Paare
    python scripts/hooks/hook-sperre.py --neu           # alles neu prüfen
    python scripts/hooks/hook-sperre.py --zeigen        # nur den Stand ausgeben
"""
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
QUELLE = ROOT / "outputs" / "reels" / "2026-11-testreels.json"
SKILL = ROOT / ".claude" / "skills" / "content" / "SKILL.md"
MODELL = "claude-opus-5-5"
# Abschnitte aus /content, die der zweite Blick bekommt (Überschriften, nicht Zeilennummern)
ABSCHNITTE = ["## DER GARTEN", "## TEIL 0: FÜR WEN", "## DIE PFLICHTREGELN", "## TEIL 3: HOOKS"]
WERKZEUG = re.compile(r"\b(KI|Claude|ChatGPT|Tool|Tools|Generator|Nischengenerator|Instagram|Insta|"
                      r"Reel|Reels|Kurs|Kurse|Freebie|Workshop|Öle?n?|Funnel|App)\b", re.I)
BINDEWORT = re.compile(r"\b(trotzdem|obwohl|aber|dabei|sondern|doch)\b", re.I)


def satz(paar, teil):
    return " ".join(t for t in paar[teil] if t).strip()


def fingerabdruck(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def freigabe(paar, teil):
    """(ok, grund) — die Sperre, die Bau- und Cockpit-Skript abfragen."""
    p = (paar.get("pruefung") or {}).get(teil)
    if not p:
        return False, "nie geprüft"
    if p.get("fingerabdruck") != fingerabdruck(satz(paar, teil)):
        return False, "Hook geändert seit der Prüfung"
    if not p.get("bestanden"):
        return False, "durchgefallen: " + "; ".join(p.get("gruende", [])[:3])
    return True, ""


def texte_pruefen():
    spec = importlib.util.spec_from_file_location("tp", ROOT / "scripts" / "cockpit" / "texte-pruefen.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def woerter(text):
    return [w for w in re.split(r"\s+", text) if re.search(r"\w", w)]


def maschine(paar, teil, tp):
    s, gruende = satz(paar, teil), []
    n = len(woerter(s))
    if not 10 <= n <= 14:
        gruende.append("%d Wörter (10–14)" % n)
    if "ß" in s:
        gruende.append("ß statt ss")
    m = WERKZEUG.search(s)
    if m:
        gruende.append("Werkzeug im Hook: „%s“" % m.group(0))
    for schwere, befund, stelle in tp.pruefe({"hook": s, "caption": paar.get("caption", "")}, paar["nr"]):
        if schwere == 1 and not befund.startswith("Keine Caption"):
            gruende.append("Blackliste: %s (%s)" % (befund, stelle[:60]))
    cap = paar.get("caption", "")
    if cap:
        absaetze = [a for a in cap.split("\n\n") if a.strip()]
        if any(re.search(r"Kommentier", a) for a in absaetze[:-1]):
            gruende.append("Stichwort nicht nur am Schluss der Caption")
    return gruende


DOTERRA = ROOT / "context" / "doterra" / "energie-story-profil.md"
# Für doTERRA-Hooks (seit 03.11.2026): andere Leserin, andere Grenzen. TEIL 0 (Sandra) passt nicht.
ABSCHNITTE_DOTERRA = ["## DER GARTEN", "## DIE PFLICHTREGELN", "## TEIL 3: HOOKS"]
COMPLIANCE_DOTERRA = """## doTERRA-Profil (@patricia_ulmann) — gilt vor allem anderen
- Mama-Account, kein Produkt-Account. Leserin: erschöpfte Mama ab 35 mit Müdigkeit, Mittagstief, Haarausfall,
  Schlafstörungen, Hormonchaos, die sich oft noch nie mit Perimenopause beschäftigt hat. Kein Network-Thema.
- Keine Heilversprechen: nie „heilt, hilft gegen, behandelt, bekämpft“. Frame „bei mir war es so“.
- Kein Produkt, keine Marke, kein Öl, kein Nahrungsergänzungsmittel im Hook. doTERRA ist im Feed unsichtbar.
- Keine medizinischen Fakten, Werte oder Wirkzeiten, die nicht im BELEGT oder im Story-Profil stehen.
"""


def regeln(profil="mentoring"):
    t = SKILL.read_text(encoding="utf-8")
    teile = []
    if profil == "doterra":
        teile.append(COMPLIANCE_DOTERRA)
        teile.append(DOTERRA.read_text(encoding="utf-8"))
    for kopf in (ABSCHNITTE_DOTERRA if profil == "doterra" else ABSCHNITTE):
        i = t.find(kopf)
        if i < 0:
            sys.exit("Abschnitt fehlt in /content: " + kopf)
        j = t.find("\n## ", i + 4)
        teile.append(t[i:j if j > 0 else None])
    return "\n\n".join(teile)


def schluessel():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        for z in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
            if z.startswith("ANTHROPIC_API_KEY="):
                os.environ["ANTHROPIC_API_KEY"] = z.split("=", 1)[1].strip().strip('"')
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY fehlt (.env im Wurzelordner)")


def zweiter_blick(client, regeltext, paar, teil, profil="mentoring"):
    from pydantic import BaseModel

    class Antwort(BaseModel):
        ja: bool
        warum: str

    class Pruefung(BaseModel):
        schmerz: Antwort
        gedanke_gelesen: Antwort
        kuechentisch: Antwort
        bezug_der_zeilen: Antwort
        loesung_draussen: Antwort
        in_drei_sekunden_klar: Antwort
        mikro_szene: Antwort
        gegner_gestaendnis_oder_zitat: Antwort
        nische_network_mama: Antwort
        passt_zur_rolle: Antwort
        vorschlag: str

    s = satz(paar, teil)
    bind = BINDEWORT.findall(s)
    if profil == "doterra":
        # gleiche Felder, damit Auswertung und Cockpit-Skripte nichts Neues lernen müssen;
        # „nische_network_mama“ heisst hier: trifft die erschöpfte Mama ab 35
        auftrag_kopf = (
            "Du prüfst einen Instagram-Hook für Patricias doTERRA-Profil, einen Mama-Account für erschöpfte "
            "Mamas ab 35 (Müdigkeit, Hormone, Schlaf, Haarausfall). Der Hook steht als Text über einem Clip "
            "aus ihrem Alltag. Prüfe streng nach den Regeln oben, besonders Heilversprechen, Produkte und "
            "erfundene Fakten. Im Zweifel Nein. Jede Antwort mit einem kurzen Satz warum.\n\n")
        fragen_schmerz, fragen_nische = ("trifft einen echten Schmerz der erschöpften Mama ab 35",
                                         "nische_network_mama (hier: trifft klar die erschöpfte Mama ab 35, "
                                         "nicht Network, kein Produkt, kein Heilversprechen)")
    else:
        auftrag_kopf = (
            "Du prüfst einen Instagram-Hook für Patricia (Mentorin für Network-Mamas, die ein eigenes "
            "Standbein neben dem Network aufbauen wollen). Der Hook steht 7 Sekunden als Text über einem "
            "stillen B-Roll-Clip aus ihrem Alltag. Prüfe streng nach den Regeln oben. Im Zweifel Nein. "
            "Jede Antwort mit einem kurzen Satz warum.\n\n")
        fragen_schmerz, fragen_nische = "trifft einen echten Schmerz der Network-Mama", "nische_network_mama"
    auftrag = auftrag_kopf + (
        "HOOK: %s\n"
        "ROLLE im Monatsgarten: %s\n"
        "WAS DER BEITRAG MITGIBT: %s\n"
        "BELEGT (von Patricia bestätigt, gilt wie die Eckdaten, ist also nicht erfunden): %s\n"
        "%s"
        "\nFragen: schmerz (" + fragen_schmerz + ") · gedanke_gelesen "
        "(„krass, wieso weiss die, was ich denke“) · kuechentisch (so sagt man es einer Freundin) · "
        "bezug_der_zeilen (die Teile hängen logisch richtig zusammen, kein Bindewort dreht den Sinn) · "
        "loesung_draussen (keine Lösung, kein Angebot im Hook) · in_drei_sekunden_klar (wer sie nicht "
        "kennt, versteht sofort, um welche Welt es geht, ohne Vorwissen) · mikro_szene (ein konkreter "
        "Moment statt einer Behauptung) · gegner_gestaendnis_oder_zitat · " + fragen_nische + " · "
        "passt_zur_rolle. vorschlag: nur wenn eine Antwort Nein ist, ein besserer Hook (10–14 Wörter, "
        "erfinde keine Fakten, Zahlen oder Szenen, die nicht im Hook oder in WAS DER BEITRAG MITGIBT "
        "oder BELEGT stehen); sonst leer."
    ) % (s, paar.get("rolle") or "nicht angegeben", paar.get("mit") or "nicht angegeben",
         paar.get("belegt") or "nichts über die Eckdaten hinaus",
         ("ACHTUNG Bindewort: %s — prüfe besonders, ob dort wirklich ein Gegensatz steht.\n"
          % ", ".join(bind)) if bind else "")
    r = client.messages.parse(
        model=MODELL, max_tokens=8000, output_config={"effort": "medium"},
        system=[{"type": "text", "text": "REGELN (aus Patricias Content-Skill):\n\n" + regeltext,
                 "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": auftrag}], output_format=Pruefung)
    return r.parsed_output.model_dump()


def einzeln():
    """Einzelne Hooks prüfen (Feed-Beiträge, Sprechreels): eine JSON-Liste
    [{id, hook, rolle, mit, caption}] → Ergebnis daneben als <datei>.pruefung.json."""
    pfad = Path(sys.argv[sys.argv.index("--datei") + 1])
    liste = json.loads(pfad.read_text(encoding="utf-8"))
    profil = sys.argv[sys.argv.index("--profil") + 1] if "--profil" in sys.argv else "mentoring"
    tp = texte_pruefen()
    schluessel()
    import anthropic
    client, regeltext = anthropic.Anthropic(), regeln(profil)
    erg = {}
    for e in liste:
        p = {"nr": e["id"], "a": [e["hook"]], "rolle": e.get("rolle"), "mit": e.get("mit"),
             "caption": e.get("caption", ""), "belegt": e.get("belegt", "")}
        gruende = maschine(p, "a", tp)
        blick = zweiter_blick(client, regeltext, p, "a", profil)
        gruende += ["%s: %s" % (k, v["warum"]) for k, v in blick.items() if isinstance(v, dict) and not v["ja"]]
        erg[e["id"]] = {"hook": e["hook"], "fingerabdruck": fingerabdruck(e["hook"]), "bestanden": not gruende,
                        "gruende": gruende, "vorschlag": blick.get("vorschlag", "") if gruende else "",
                        "antworten": {k: v for k, v in blick.items() if isinstance(v, dict)}}
        print("%s %s  %s" % (e["id"], "✓" if not gruende else "✗", e["hook"]), flush=True)
        for g in gruende:
            print("      · " + g)
    pfad.with_suffix(".pruefung.json").write_text(json.dumps(erg, ensure_ascii=False, indent=1), encoding="utf-8")


def main():
    if "--datei" in sys.argv:
        return einzeln()
    d = json.loads(QUELLE.read_text(encoding="utf-8"))
    nur = None
    if "--nur" in sys.argv:
        nur = set(sys.argv[sys.argv.index("--nur") + 1].split(","))
    if "--zeigen" in sys.argv:
        for p in d["paare"]:
            for t in "ab":
                ok, g = freigabe(p, t)
                print("%s %s %s  %s" % (p["datum"], p["nr"], t.upper(), "✓" if ok else "✗ " + g))
        return
    tp = texte_pruefen()
    schluessel()
    import anthropic
    client, regeltext = anthropic.Anthropic(), regeln()
    gesperrt = 0
    for p in d["paare"]:
        if nur and p["nr"] not in nur:
            continue
        for t in "ab":
            if "--neu" not in sys.argv and not nur and freigabe(p, t)[0]:
                continue
            s = satz(p, t)
            gruende = maschine(p, t, tp)
            try:
                blick = zweiter_blick(client, regeltext, p, t)
            except Exception as e:
                # Abgeschnittene Antwort (02.11.2026 bei 3000 Token): diesen Hook auslassen, nicht den ganzen Lauf.
                print("%s %s %s ?  Prüfung abgebrochen (%s), bleibt gesperrt" % (p["datum"], p["nr"], t.upper(),
                                                                          type(e).__name__), flush=True)
                gesperrt += 1
                continue
            for k, v in blick.items():
                if isinstance(v, dict) and not v["ja"]:
                    gruende.append("%s: %s" % (k, v["warum"]))
            ok = not gruende
            p.setdefault("pruefung", {})[t] = {
                "fingerabdruck": fingerabdruck(s), "bestanden": ok, "gruende": gruende,
                "antworten": {k: v for k, v in blick.items() if isinstance(v, dict)},
                "vorschlag": blick.get("vorschlag", "") if not ok else "", "modell": MODELL}
            gesperrt += not ok
            print("%s %s %s %s  %s" % (p["datum"], p["nr"], t.upper(), "✓" if ok else "✗", s), flush=True)
            for g in gruende:
                print("      · " + g)
            if not ok and blick.get("vorschlag"):
                print("      → Vorschlag: " + blick["vorschlag"])
            tmp = QUELLE.with_suffix(".tmp")
            tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
            tmp.replace(QUELLE)
    print("\n%d gesperrt" % gesperrt)


if __name__ == "__main__":
    main()
