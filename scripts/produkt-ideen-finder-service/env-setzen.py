"""
Traegt die Umgebungsvariablen des Produkt-Ideen-Finders ins Vercel-Projekt ein.

Liest die Werte aus den bestehenden .env-Dateien im Workspace und reicht sie
ueber die Standardeingabe an die Vercel-CLI weiter. **Die Werte selbst werden
nirgends ausgegeben** — weder in der Konsole noch in einer Datei.

Aufruf:
  python scripts/produkt-ideen-finder-service/env-setzen.py           # eintragen
  python scripts/produkt-ideen-finder-service/env-setzen.py --pruefen # nur zeigen, was fehlt
"""
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
DIENST = ROOT / "scripts" / "produkt-ideen-finder-service"


def aus_env(datei, schluessel):
    p = ROOT / datei
    if not p.exists():
        return None
    for zeile in p.read_text(encoding="utf-8", errors="replace").splitlines():
        z = zeile.strip()
        if z.startswith(schluessel + "="):
            return z.split("=", 1)[1].strip().strip('"\'')
    return None


# Was gesetzt wird und woher es kommt.
VARIABLEN = [
    ("ANTHROPIC_API_KEY", lambda: aus_env(".env", "ANTHROPIC_API_KEY")),
    ("AC_API_URL", lambda: aus_env("04-projects/activecampaign-mcp/.env", "AC_API_URL")),
    ("AC_API_KEY", lambda: aus_env("04-projects/activecampaign-mcp/.env", "AC_API_KEY")),
    ("AC_LIST_ID", lambda: "2"),      # Regulaerer Newsletter/Interessenten
    ("AC_TAG_LEAD", lambda: "98"),    # Tag produkt-ideen-finder-lead
]


def main():
    nur_pruefen = "--pruefen" in sys.argv
    fehlt = []
    for name, holen in VARIABLEN:
        wert = holen()
        if not wert:
            print("  %-20s QUELLE FEHLT" % name)
            fehlt.append(name)
            continue
        if nur_pruefen:
            print("  %-20s bereit (%d Zeichen)" % (name, len(wert)))
            continue
        for umgebung in ("production", "preview"):
            r = subprocess.run(
                ["npx", "--yes", "vercel@latest", "env", "add", name, umgebung],
                cwd=str(DIENST), input=wert, text=True,
                capture_output=True, shell=True)
            ok = r.returncode == 0 or "already exists" in (r.stderr or "")
            print("  %-20s %-11s %s" % (name, umgebung, "OK" if ok else "FEHLER"))
            if not ok:
                print("      " + (r.stderr or "").strip().splitlines()[-1][:160])
    if fehlt:
        print("\nNicht gesetzt, weil die Quelle fehlt: %s" % ", ".join(fehlt))
        sys.exit(1)
    if not nur_pruefen:
        print("\nDanach neu ausrollen, damit die Variablen greifen:")
        print("  cd scripts/produkt-ideen-finder-service && npx vercel --prod")


if __name__ == "__main__":
    main()
