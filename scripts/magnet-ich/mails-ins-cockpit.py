"""
Legt die fertigen Magnet-Ich-Mails als Dokumente fürs Cockpit ab
(Sammlung `mailentwuerfe`, je Mail ein Dokument).

  python scripts/magnet-ich/mails-bauen.py
  python scripts/magnet-ich/mails-ins-cockpit.py
  # danach: ArtifactData batch set -> Sammlung "mailentwuerfe", file_path je Datei

Das Cockpit zeigt sie unter „Listen & Automationen“ bei der Automation, zu der
sie gehören (Feld `automation`), mit Vorschau und Kopier-Knöpfen.
🚨 Die Sammlung gehört diesem Skript, nicht dem täglichen Abgleich.
"""
import importlib.util, json, pathlib, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("mi", ROOT / "scripts/magnet-ich/mails-bauen.py")
mi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mi)

ZIEL = ROOT / "outputs" / "cockpit" / "abgleich" / "mailentwuerfe"
ZIEL.mkdir(parents=True, exist_ok=True)

for i, m in enumerate(mi.MAILS):
    quelle = mi.ZIEL / m["datei"]
    if not quelle.exists():
        sys.exit("Fehlt: %s — zuerst mails-bauen.py laufen lassen." % quelle)
    kennung = "magnet-ich-" + m["datei"].replace(".html", "")
    doc = {
        "automation": "42",
        "reihenfolge": i,
        "tag": m["tag"],
        "warten": m["warten"],
        "wann": m["wann"],
        "betreff": m["betreff"],
        "betreff2": m.get("betreff2", ""),
        "preheader": m.get("preheader", ""),
        "notiz": m.get("notiz", ""),
        "html": quelle.read_text(encoding="utf-8"),
    }
    (ZIEL / (kennung + ".json")).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print("  %s · %d KB" % (kennung, len(doc["html"].encode("utf-8")) // 1024))
