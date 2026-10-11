# -*- coding: utf-8 -*-
"""Macht aus den rohen Cockpit-Dokumenten lesbare Dateien im Workspace.

**Warum es das gibt:** Alle fertigen Beitraege lagen bis 16.09.2026 ausschliesslich
in der Artifact-Datenbank. Ein Artifact ist kein Backup — es gibt keine Historie, kein
Git, und wer versehentlich ein `set` darueberschreibt, hat den Text verloren. Patricia:
*„bitte alle inhalte speichern, dass sie im workspace drin sind"*.

**Zwei Schritte, der erste ist nicht dieses Skript:**

1. Rohdaten holen — das macht Claude mit dem ArtifactData-Werkzeug, weil ein Python-
   Skript nicht an die Artifact-Datenbank kommt:

       ArtifactData list → collection "reels"      → out_dir outputs/cockpit/inhalte-roh
       ArtifactData list → collection "karussells" → dito
       ArtifactData list → collection "storys"     → dito
       ArtifactData list → collection "daten"      → dito

2. Dieses Skript laeuft ueber die JSON-Dateien und schreibt Markdown:

       python scripts/cockpit/inhalte-sichern.py

**Was rausfaellt:** `daten/wissen-voll` (178 KB erzeugter Markenbrief, kommt aus
`wissen-bauen.py` und steht ohnehin in `context/`) und `daten/kurse` (210 KB, kommt aus
`kurse-indexieren.py`). Beides sind Kopien, keine Originale — die gehoeren nicht nochmal
in den Vault.
"""
import json
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

WURZEL = Path(__file__).resolve().parents[2]
ROH = WURZEL / "outputs" / "cockpit" / "inhalte-roh"
ZIEL = WURZEL / "outputs" / "content" / "KW38"

PROFIL = {"mentoring": "Mentoring", "doterra": "doTERRA"}
WOCHENTAG = {
    "mo": "Montag", "di": "Dienstag", "mi": "Mittwoch",
    "do": "Donnerstag", "fr": "Freitag", "sa": "Samstag", "so": "Sonntag",
}


def laden(ordner):
    """Nach Datum sortiert, dann nach Dateiname — sonst steht C vor A."""
    p = ROH / ordner
    if not p.is_dir():
        return []
    raus = []
    for datei in sorted(p.glob("*.json")):
        d = json.loads(datei.read_text(encoding="utf-8"))
        d["_id"] = datei.stem
        raus.append(d)
    return sorted(raus, key=lambda d: (d.get("datum", "9999"), d["_id"]))


def block(titel, wert):
    """Leere Felder gar nicht erst schreiben — sonst besteht die Haelfte der
    Datei aus Ueberschriften ohne Inhalt."""
    if not wert or not str(wert).strip():
        return ""
    return f"**{titel}**\n\n{str(wert).strip()}\n\n"


def profilzeile(d):
    teile = []
    if d.get("datum"):
        teile.append(d["datum"])
    if d.get("profil"):
        teile.append(PROFIL.get(d["profil"], d["profil"]))
    if d.get("typ"):
        teile.append(d["typ"])
    if d.get("funnel"):
        teile.append(d["funnel"])
    if d.get("brand"):
        teile.append(f"Look {d['brand']}")
    return " · ".join(teile)


def reels_schreiben():
    posts = laden("reels")
    zeilen = ["---", "tags: [content, reels]", "---", "",
              "# Reels aus dem Cockpit — Stand 16.09.2026", "",
              "Gesichert aus der Cockpit-Datenbank (Sammlung `reels`). **Die Datenbank",
              "bleibt die Arbeitsfassung** — wer hier etwas aendert, aendert nichts im",
              "Cockpit. Diese Datei ist die Sicherung und die Lesefassung.", "",
              f"**{len(posts)} Reels.**", ""]

    mit_video = [p for p in posts if p.get("videourl")]
    zeilen += [f"🎬 **Video vorhanden: {len(mit_video)} von {len(posts)}.** "
               "Bei allen anderen fehlt das Rohmaterial — das ist Drehen, nicht Bauen.",
               ""]
    for p in mit_video:
        zeilen.append(f"- {p.get('name', p['_id'])} → `{p.get('videodatei', p['videourl'])}`")
    zeilen += ["", "---", ""]

    for d in posts:
        zeilen.append(f"## {d.get('name', d['_id'])}")
        zeilen.append("")
        kopf = profilzeile(d)
        if kopf:
            zeilen.append(f"*{kopf}* · `{d['_id']}`")
            zeilen.append("")
        for titel, feld in [("Hook", "hook"), ("Unterzeile", "unter"),
                            ("Sprechskript", "skript"), ("Caption", "caption"),
                            ("Hinweis", "hinweis")]:
            zeilen.append(block(titel, d.get(feld)))
        if d.get("videourl"):
            zeilen.append(f"**Video:** `{d.get('videodatei', '—')}` · {d['videourl']}\n")
        zeilen.append("---\n")
    return "\n".join(zeilen)


def karussells_schreiben():
    posts = laden("karussells")
    zeilen = ["---", "tags: [content, karussell]", "---", "",
              "# Karussells aus dem Cockpit — Stand 16.09.2026", "",
              "Gesichert aus der Cockpit-Datenbank (Sammlung `karussells`), **mit allen",
              "Folien im Wortlaut**. Die Datenbank bleibt die Arbeitsfassung.", "",
              f"**{len(posts)} Karussells.**", "", "---", ""]

    for d in posts:
        zeilen.append(f"## {d.get('name', d['_id'])}")
        zeilen.append("")
        kopf = profilzeile(d)
        if kopf:
            zeilen.append(f"*{kopf}* · `{d['_id']}`")
            zeilen.append("")
        folien = d.get("slides") or []
        if folien:
            zeilen.append(f"**Folien ({len(folien)})**\n")
            for i, f in enumerate(folien, 1):
                kopfzeile = (f.get("headline") or "").strip()
                text = (f.get("body") or "").strip()
                art = f.get("layout", "")
                zeilen.append(f"{i}. **{kopfzeile}**" + (f"  ·  _{art}_" if art else ""))
                if text:
                    # Eingerueckt, damit die Nummerierung nicht bricht.
                    zeilen.append("   " + text.replace("\n", "\n   "))
            zeilen.append("")
        zeilen.append(block("Caption", d.get("caption")))
        zeilen.append(block("Hinweis", d.get("hinweis")))
        zeilen.append("---\n")
    return "\n".join(zeilen)


def storys_schreiben():
    posts = laden("storys")
    zeilen = ["---", "tags: [content, story]", "---", "",
              "# Story-Bögen aus dem Cockpit — Stand 16.09.2026", "",
              "Gesichert aus der Cockpit-Datenbank (Sammlung `storys`), Folie für Folie.",
              "🚨 **Storys werden nie automatisch eingeplant** — die postet Patricia selbst.",
              "", f"**{len(posts)} Bögen.**", "", "---", ""]

    for d in posts:
        zeilen.append(f"## {d.get('name', d['_id'])}")
        zeilen.append("")
        kopf = profilzeile(d)
        if kopf:
            zeilen.append(f"*{kopf}* · `{d['_id']}`")
            zeilen.append("")
        for i, f in enumerate(d.get("frames") or [], 1):
            text = (f.get("text") or "").strip()
            zeilen.append(f"**Folie {i}** · _{f.get('layout', '')}_")
            if text:
                zeilen.append("> " + text.replace("\n", "\n> "))
            wahl = [f.get("optA"), f.get("optB")]
            wahl = [w for w in wahl if w and w.strip()]
            if wahl:
                zeilen.append(f"> **Umfrage:** " + "  ·  ".join(wahl))
            if (f.get("cta") or "").strip():
                zeilen.append(f"> **CTA:** {f['cta'].strip()}")
            zeilen.append("")
        zeilen.append("---\n")
    return "\n".join(zeilen)


def main():
    if not ROH.is_dir():
        sys.exit(f"Keine Rohdaten in {ROH} — zuerst mit ArtifactData holen, "
                 "siehe Kopf dieser Datei.")
    ZIEL.mkdir(parents=True, exist_ok=True)
    for name, bauer in [("cockpit-reels.md", reels_schreiben),
                        ("cockpit-karussells.md", karussells_schreiben),
                        ("cockpit-storys.md", storys_schreiben)]:
        text = bauer()
        (ZIEL / name).write_text(text + "\n", encoding="utf-8")
        print(f"  {name}  ({len(text.splitlines())} Zeilen)")
    print(f"\nGeschrieben nach {ZIEL}")


if __name__ == "__main__":
    main()
