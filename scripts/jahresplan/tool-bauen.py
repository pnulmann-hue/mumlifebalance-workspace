"""Baut aus fragen.json die Jahresplaner-Seite und den Fragenteil im /jahresplan-Skill.

    python scripts/jahresplan/tool-bauen.py

Gleiche Fragen, zwei Wege: die Seite (ohne Anmeldung, für alle) und der Skill (für
Claude-Nutzerinnen). Geändert wird nur fragen.json, nie eine der beiden Ausgaben.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
WURZEL = HIER.parents[1]
FRAGEN = HIER / "fragen.json"
VORLAGE = HIER / "tool-vorlage.html"
SEITE = WURZEL / "outputs" / "produkte" / "jahresplanung" / "jahresplaner.html"
SKILL = WURZEL / ".claude" / "skills" / "jahresplan" / "SKILL.md"
ANFANG, ENDE = "<!-- FRAGEN:ANFANG (aus scripts/jahresplan/fragen.json, nicht von Hand) -->", "<!-- FRAGEN:ENDE -->"

daten = json.loads(FRAGEN.read_text(encoding="utf-8"))
vorlage = VORLAGE.read_text(encoding="utf-8")
assert vorlage.count("/*FRAGEN*/") == 1, "Platzhalter /*FRAGEN*/ fehlt oder doppelt"

# --patricia: eigene Fassung mit Patricias Angeboten statt Sandras Beispiel, Skill bleibt unberührt
if "--patricia" in sys.argv:
    eigen = json.loads((HIER / "patricia.json").read_text(encoding="utf-8"))
    for s in daten["schritte"]:
        for f in s.get("fragen", []):
            f["beispiel"] = eigen["antworten"].get(f["id"], [] if f["typ"] == "tage" else "")
        if "liste" in s:
            s["liste"]["beispiel"] = eigen["angebote"]
        if "monate" in s:
            s["monate"]["beispiel"] = {}
    sandra = '<p><strong>Das ist ein Beispiel von Sandra</strong> (Energie für Mamas ab 35), damit du siehst, wie ein fertiger Plan aussieht.</p>'
    assert vorlage.count(sandra) == 1
    vorlage = vorlage.replace(sandra, f'<p>{eigen["hinweis"]}</p>').replace("<title>Mein Jahresplan</title>", f'<title>{eigen["titel"]}</title>', 1)
    vorlage = vorlage.replace(">Meinen Plan leer starten<", ">Alles löschen und leer beginnen<").replace('"Meinen Plan leer starten"', '"Alles löschen und leer beginnen"')
    SEITE = SEITE.with_name("jahresplaner-patricia.html")

# 1 · Seite
seite = vorlage.replace("/*FRAGEN*/", json.dumps({"schritte": daten["schritte"]}, ensure_ascii=False).replace("</", "<\\/"))
for verboten in ["capabilities", "claude.use(", "Julia", "Trost"]:
    assert verboten not in seite, f"verboten in der Seite: {verboten}"
assert not re.search(r"\b[Dd]eine Kundin", seite), "zweite Zielgruppen-Ebene heisst nie Kundin"
SEITE.parent.mkdir(parents=True, exist_ok=True)
SEITE.write_text(seite, encoding="utf-8")

skript = re.search(r"<script>(.*)</script>", seite, re.S).group(1)
probe = HIER / "_probe.js"
probe.write_text(skript, encoding="utf-8")
try:
    r = subprocess.run(["node", "--check", str(probe)], capture_output=True, text=True)
finally:
    probe.unlink()
if r.returncode:
    sys.exit("Skript kaputt:\n" + r.stderr)

# 2 · Skill
zeilen = []
for i, s in enumerate(daten["schritte"], 1):
    zeilen.append(f"### Schritt {i} · {s['titel']} — {s['kurz']}\n")
    zeilen.append(f"*{s['einleitung']}*\n")
    for f in s.get("fragen", []):
        extra = f" (Auswahl: {' · '.join(f['optionen'])})" if f.get("optionen") else ""
        zeilen.append(f"- **{f['frage']}**{extra}" + (f" — {f['hilfe']}" if f.get("hilfe") else ""))
    if "liste" in s:
        zeilen.append("- Je Angebot: " + " · ".join(f["frage"] for f in s["liste"]["felder"]))
    if "monate" in s:
        zeilen.append("- Je Monat: " + " · ".join(f["frage"] for f in s["monate"]["felder"]))
    zeilen.append("")
block = f"{ANFANG}\n\n" + "\n".join(zeilen) + f"\n{ENDE}"

skill = SKILL.read_text(encoding="utf-8")
if "--patricia" in sys.argv:
    print("Skill: bei --patricia nicht angefasst")
elif ANFANG in skill:
    skill = re.sub(re.escape(ANFANG) + r".*?" + re.escape(ENDE), lambda m: block, skill, flags=re.S)
    SKILL.write_text(skill, encoding="utf-8")
    print("Skill: Fragenteil erneuert")
else:
    print("Skill: Marken fehlen noch, Fragenteil nicht eingesetzt")

print(f"Seite: {SEITE.relative_to(WURZEL)} ({len(seite):,} Zeichen)")
