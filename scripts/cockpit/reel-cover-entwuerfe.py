# -*- coding: utf-8 -*-
"""Legt jedes Reel und jedes Karussell als Entwurf in den Bild-Editor.

**Der Befund vom 16.09.2026.** Patricia: *„ich will aber ein Cover aus meinen
Shootingbildern. wir haben das mal definiert. dass ich das Bild ändern kann, den Text
auch, die höhe des Textes und der Verlauf. ob es kein Verlauf drin hat oder in einer
meiner Brandingfarben"*

Genau das kann der **Bild-Editor** seit dem 14.09. — Format `cover` (1080×1920),
„Bild aus deinen Shootings", Brandfarbe als Verlauf oder Unifarbe mit Stärke-Regler,
Textbalken mit verschiebbarer Höhe. 🚨 **Das Reel-Studio im Cockpit kann das nicht**:
es zieht ein Standbild aus dem Video. Wer ein Cover aus einem Shootingbild will, muss
in den Bild-Editor.

Nur wusste der Bild-Editor nichts von den Reels. In `daten/entwuerfe` lagen acht
Einträge — zwei Karussells, sechs Storys, **alle Mentoring, kein einziges Cover**. Auf
dem doTERRA-Profil war die Liste leer. Deshalb dieses Skript.

**Was daraus wird:**

| Quelle | wird zu | Folien |
|---|---|---|
| ein Reel | Entwurf `art: "cover"`, Format `cover` | eine — Titelzeile + Unterzeile |
| ein Karussell | Entwurf `art: "karussell"`, Format `slide` | alle, im Wortlaut |

🚨 **Auf dem Cover steht ein HOOK, nicht der Beitragsname.** Patricia am 16.09.2026:
*„auf das Reelcover muss auch ein hook. kann abgekürzter sein als im video aber auch ein
hook."* Der erste Anlauf hat den Namen genommen („Sieben Uhr vierzig") — das ist eine
Überschrift und zieht niemanden in ein Video.

Die Cover-Hooks stehen in **`outputs/content/KW38/cover-hooks.json`**, je Reel eine
`text`- und eine `unter`-Zeile, **aus dem `hook`-Feld des Reels gekürzt**. Nichts davon
ist neu behauptet. Reihenfolge beim Suchen:

1. Feld `coverhook` am Reel selbst (falls Patricia es im Cockpit gesetzt hat)
2. `cover-hooks.json`
3. Der Beitragsname — **mit Warnung**, weil das eben kein Hook ist

    python scripts/cockpit/reel-cover-entwuerfe.py
    # danach: ArtifactData set → Bild-Editor, collection "daten", doc_id "entwuerfe",
    #         file_path outputs/cockpit/abgleich/entwuerfe.json

Quelle sind die Rohdateien aus `inhalte-sichern.py` (Kopf dort lesen).
"""
import json
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

WURZEL = Path(__file__).resolve().parents[2]
ROH = WURZEL / "outputs" / "cockpit" / "inhalte-roh"
ZIEL = WURZEL / "outputs" / "cockpit" / "abgleich" / "entwuerfe.json"
COVERHOOKS = WURZEL / "outputs" / "content" / "KW38" / "cover-hooks.json"

# Variantenbuchstabe und Wochentag vorne wegschneiden: "B · Mo · Text" -> "Text",
# "KW38 Mi · Text" -> "Text". Der Rest ist die Zeile, die aufs Cover gehoert.
# 🚨 Der Trenner ist nicht immer derselbe: "B · Mo · Text" hat einen Punkt,
# "KW38 Mi · Text" ein Leerzeichen. Wer nur den Punkt erlaubt, laesst bei jedem
# dritten Reel "KW38 Mi · " auf dem Cover stehen.
VORSPANN = re.compile(
    r"^(?:[A-Z]|KW\d{2})\s*(?:·|\s)\s*(?:Mo|Di|Mi|Do|Fr|Sa|So)\s*·\s*"
    r"(?:doTERRA\s*·\s*)?", re.IGNORECASE)

# Keyword -> Profil. Nur fuer Beitraege, bei denen das Feld leer ist; erfunden wird
# nichts, das Stichwort steht in context/manychat-keywords.md.
KEYWORD_PROFIL = {"STANDBEIN": "mentoring", "ECHT1": "mentoring",
                  "SYSTEM": "mentoring", "THEMA": "mentoring",
                  "ENERGIE": "doterra"}


def titelzeile(name):
    kurz = VORSPANN.sub("", (name or "").strip())
    # Ein Klammer-Zusatz wie "(LEAD · STANDBEIN)" ist eine Notiz an Patricia,
    # keine Cover-Zeile.
    kurz = re.sub(r"\s*\([^)]*\)\s*$", "", kurz).strip()
    return kurz or (name or "").strip()


def profil_raten(d):
    """Gibt (profil, woher) zurueck. Nie stillschweigend setzen — die Herkunft
    steht im Ergebnis, damit man es nachpruefen kann."""
    if d.get("profil"):
        return d["profil"], "gesetzt"
    text = " ".join(str(d.get(f, "")) for f in ("caption", "hinweis", "name", "skript"))
    for wort, profil in KEYWORD_PROFIL.items():
        if re.search(r"\b" + wort + r"\b", text):
            return profil, f"aus Keyword {wort}"
    return None, "unbekannt"


def laden(ordner):
    p = ROH / ordner
    if not p.is_dir():
        sys.exit(f"Fehlt: {p} — zuerst mit ArtifactData holen.")
    raus = []
    for datei in sorted(p.glob("*.json")):
        d = json.loads(datei.read_text(encoding="utf-8"))
        d["_id"] = datei.stem
        raus.append(d)
    return raus


def coverzeilen(d, tabelle, ohne_hook):
    """Die zwei Zeilen fuers Cover. Reihenfolge: eigenes Feld am Reel, dann die
    gepflegte Tabelle, dann notgedrungen der Name — der wird gemeldet, weil ein
    Name kein Hook ist."""
    if (d.get("coverhook") or "").strip():
        return d["coverhook"].strip(), (d.get("coverunter") or d.get("unter") or "").strip()
    eintrag = tabelle.get(d["_id"])
    if eintrag and (eintrag.get("text") or "").strip():
        return eintrag["text"].strip(), (eintrag.get("unter") or "").strip()
    ohne_hook.append((d["_id"], d.get("name", "")))
    return titelzeile(d.get("name")), (d.get("unter") or "").strip()


def main():
    eintraege, offen, ohne_hook = [], [], []
    tabelle = {}
    if COVERHOOKS.is_file():
        tabelle = json.loads(COVERHOOKS.read_text(encoding="utf-8")).get("hooks", {})

    # --- Reels -> Reel-Cover -----------------------------------------
    for d in laden("reels"):
        name = (d.get("name") or "").strip()
        if not name or name == "Neues Reel":
            continue                       # leerer Platzhalter, kein Beitrag
        profil, woher = profil_raten(d)
        if not profil:
            offen.append((d["_id"], name))
            continue
        gross, klein = coverzeilen(d, tabelle, ohne_hook)
        eintraege.append({
            "id": "cover-" + d["_id"],
            "art": "cover",
            "format": "cover",
            "profil": profil,
            "datum": d.get("datum", ""),
            "name": name,
            "cta": d.get("keyword", "") or "",
            "folien": [{"text": gross, "unter": klein}],
            "_profil_woher": woher,
        })

    # --- Karussells -> Folien im Wortlaut ------------------------------
    for d in laden("karussells"):
        name = (d.get("name") or "").strip()
        if not name:
            continue
        profil, woher = profil_raten(d)
        if not profil:
            offen.append((d["_id"], name))
            continue
        folien = []
        for f in d.get("slides") or []:
            folien.append({"text": (f.get("headline") or "").strip(),
                           "unter": (f.get("body") or "").strip()})
        if not folien:
            continue
        eintraege.append({
            "id": "kar-" + d["_id"],
            "art": "karussell",
            "format": "slide",
            "profil": profil,
            "datum": d.get("datum", ""),
            "name": name,
            "cta": "",
            "folien": folien,
            "_profil_woher": woher,
        })

    # --- Vorhandene Story-Boegen behalten ------------------------------
    # 🚨 Nie ueberschreiben: die sechs Story-Entwuerfe vom 14.09. stehen nur dort.
    alt = ROH / "bild-editor" / "daten" / "entwuerfe.json"
    behalten = []
    if alt.is_file():
        vorher = json.loads(alt.read_text(encoding="utf-8")).get("entwuerfe", [])
        neue_ids = {e["id"] for e in eintraege}
        neue_namen = {(e["profil"], e["name"]) for e in eintraege}
        for e in vorher:
            if e.get("id") in neue_ids:
                continue
            if (e.get("profil"), e.get("name")) in neue_namen:
                continue
            behalten.append(e)

    alles = behalten + eintraege
    alles.sort(key=lambda e: (e.get("profil", ""), e.get("datum", ""), e.get("name", "")))

    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    # Die Herkunft des Profils ist hier drin nuetzlich, im Artifact aber Ballast —
    # sie steht stattdessen in der Ausgabe unten.
    sauber = [{k: v for k, v in e.items() if not k.startswith("_")} for e in alles]
    ZIEL.write_text(json.dumps({
        "entwuerfe": sauber,
        "stand": "2026-09-16",
        "quelle": "Cockpit-Datenbank, Sammlungen reels + karussells + bestehende Storys",
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    art = {}
    for e in alles:
        art[(e.get("profil"), e.get("art"))] = art.get((e.get("profil"), e.get("art")), 0) + 1
    print(f"{len(alles)} Entwuerfe ({len(behalten)} behalten, {len(eintraege)} neu gebaut)\n")
    for (p, a), n in sorted(art.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
        print(f"  {str(p):10} {str(a):10} {n:3}")
    if offen:
        print("\n⚠ Ohne Profil, deshalb NICHT uebernommen "
              "(im Cockpit nachtragen):")
        for i, n in offen:
            print(f"  {i}  —  {n}")
    if ohne_hook:
        print("\n⚠ KEIN Cover-Hook hinterlegt — dort steht jetzt der Beitragsname, "
              "und ein Name ist kein Hook.\n  Eintragen in "
              "outputs/content/KW38/cover-hooks.json:")
        for i, n in ohne_hook:
            print(f"  {i}  —  {n}")
    print(f"\nGeschrieben: {ZIEL}")


if __name__ == "__main__":
    main()
