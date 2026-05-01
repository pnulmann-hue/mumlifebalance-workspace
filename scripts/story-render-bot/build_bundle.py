"""Bundle-Builder für Railway-Deploy.

Erstellt scripts/story-render-bot/_bundle/ mit:
- Shootingbilder/ (30 ausgewählte Patricia-Bilder, ~200-250 MB)
- stock-fotos/ (alle 3 Atmosphäre-Kategorien, ~70 MB)
- doTERRA/ (nur die .md-Dateien für Claude-Prompt)

Nutzung:
    python build_bundle.py            # baut Bundle (kopiert Files)
    python build_bundle.py --auswahl   # zeigt nur die Auswahl-Liste, kopiert nichts
    python build_bundle.py --refresh   # löscht altes Bundle, baut neu
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import config

BUNDLE_DIR = Path(__file__).resolve().parent / "_bundle"

# Anzahl Shootingbilder im Bundle
SHOOTINGBILDER_ANZAHL = 30


def waehle_shootingbilder(quelle: Path, anzahl: int) -> list[Path]:
    """Wählt ein Subset Shootingbilder aus.

    Strategie: Patricia hat 1007 Bilder. Wir nehmen ein gleichverteiltes Subset.
    """
    alle = sorted([p for p in quelle.iterdir()
                  if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png"}])
    if len(alle) <= anzahl:
        return alle

    # Gleichverteilte Auswahl
    schritt = len(alle) / anzahl
    indizes = [int(i * schritt) for i in range(anzahl)]
    return [alle[i] for i in indizes]


def kopiere_shootingbilder(refresh: bool = False) -> dict:
    quelle = config.SHOOTINGBILDER_DIR
    ziel = BUNDLE_DIR / "Shootingbilder"

    if not quelle.exists():
        return {"ok": False, "error": f"Quelle fehlt: {quelle}"}

    if refresh and ziel.exists():
        shutil.rmtree(ziel)
    ziel.mkdir(parents=True, exist_ok=True)

    auswahl = waehle_shootingbilder(quelle, SHOOTINGBILDER_ANZAHL)
    kopiert = 0
    for src in auswahl:
        dst = ziel / src.name
        if not dst.exists():
            shutil.copy2(src, dst)
            kopiert += 1

    total_size = sum(p.stat().st_size for p in ziel.iterdir()) / (1024 * 1024)
    return {
        "ok": True,
        "anzahl": len(auswahl),
        "kopiert": kopiert,
        "size_mb": round(total_size, 1),
    }


def kopiere_stock_fotos(refresh: bool = False) -> dict:
    quelle = config.STOCK_FOTOS_DIR
    ziel = BUNDLE_DIR / "stock-fotos"

    if not quelle.exists():
        return {"ok": False, "error": f"Quelle fehlt: {quelle}"}

    if refresh and ziel.exists():
        shutil.rmtree(ziel)
    ziel.mkdir(parents=True, exist_ok=True)

    total = 0
    kopiert = 0
    for kat_dir in quelle.iterdir():
        if not kat_dir.is_dir():
            continue
        ziel_kat = ziel / kat_dir.name
        ziel_kat.mkdir(exist_ok=True)
        for f in kat_dir.iterdir():
            if f.suffix.lower() in {".jpg", ".jpeg", ".png"}:
                total += 1
                dst = ziel_kat / f.name
                if not dst.exists():
                    shutil.copy2(f, dst)
                    kopiert += 1

    total_size = sum(p.stat().st_size for p in ziel.rglob("*") if p.is_file()) / (1024 * 1024)
    return {"ok": True, "anzahl": total, "kopiert": kopiert, "size_mb": round(total_size, 1)}


def kopiere_doterra_md(refresh: bool = False) -> dict:
    quelle = config.WORKSPACE_ROOT / "context" / "doTERRA"
    ziel = BUNDLE_DIR / "doTERRA"

    if not quelle.exists():
        return {"ok": False, "error": f"Quelle fehlt: {quelle}"}

    if refresh and ziel.exists():
        shutil.rmtree(ziel)
    ziel.mkdir(parents=True, exist_ok=True)

    kopiert = 0
    for f in quelle.iterdir():
        if f.is_file() and f.suffix == ".md":
            dst = ziel / f.name
            shutil.copy2(f, dst)
            kopiert += 1

    return {"ok": True, "kopiert": kopiert}


def kopiere_context_kerne(refresh: bool = False) -> dict:
    """Kopiert die wichtigsten context/.md-Dateien ins Bundle.

    Damit Bot auf Railway autark läuft, ohne workspace-root abzuhängen.
    """
    quelle = config.WORKSPACE_ROOT / "context"
    ziel = BUNDLE_DIR / "context"

    if refresh and ziel.exists():
        shutil.rmtree(ziel)
    ziel.mkdir(parents=True, exist_ok=True)

    # Pflicht-Lese-Liste + zusätzliche
    pflicht = config.PFLICHT_LESE_LISTE + [
        "context/personal-info.md",
        "context/business-info.md",
        "context/patricia-expertise.md",
        "context/patricia-freebies.md",
        "context/strategy.md",
    ]

    kopiert = 0
    for rel in pflicht:
        src = config.WORKSPACE_ROOT / rel
        if not src.exists():
            continue
        # Pfad relativ zu context/
        rel_path = Path(rel).relative_to("context")
        dst = ziel / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        kopiert += 1

    return {"ok": True, "kopiert": kopiert}


def kopiere_render_pipeline(refresh: bool = False) -> dict:
    """Kopiert render-stories.js + brand-stories.css + package.json ins Bundle."""
    quelle = config.WORKSPACE_ROOT / "scripts" / "karussell-render"
    ziel = Path(__file__).resolve().parent / "render"

    if refresh and ziel.exists():
        shutil.rmtree(ziel)
    ziel.mkdir(parents=True, exist_ok=True)

    files = ["render-stories.js", "brand-stories.css", "package.json"]
    kopiert = 0
    for fn in files:
        src = quelle / fn
        if src.exists():
            shutil.copy2(src, ziel / fn)
            kopiert += 1

    return {"ok": True, "kopiert": kopiert, "files": files}


def main():
    refresh = "--refresh" in sys.argv
    nur_auswahl = "--auswahl" in sys.argv

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=== Bundle-Builder ===")
    print(f"Bundle-Pfad: {BUNDLE_DIR}")
    print(f"Refresh: {refresh}")
    print()

    if nur_auswahl:
        print("--- Shootingbilder-Auswahl ---")
        ausgew = waehle_shootingbilder(config.SHOOTINGBILDER_DIR, SHOOTINGBILDER_ANZAHL)
        for p in ausgew:
            size_mb = p.stat().st_size / (1024 * 1024)
            print(f"  {p.name}  ({size_mb:.1f} MB)")
        total = sum(p.stat().st_size for p in ausgew) / (1024 * 1024)
        print(f"\nTotal: {len(ausgew)} Bilder, {total:.1f} MB")
        return

    print("--- Render-Pipeline ---")
    r = kopiere_render_pipeline(refresh)
    print(f"  {r}")

    print("\n--- Context (Pflicht-Lese-Liste + Patricia-Doks) ---")
    r = kopiere_context_kerne(refresh)
    print(f"  {r}")

    print("\n--- Shootingbilder ---")
    r = kopiere_shootingbilder(refresh)
    print(f"  {r}")

    print("\n--- Stock-Fotos ---")
    r = kopiere_stock_fotos(refresh)
    print(f"  {r}")

    print("\n--- doTERRA .md ---")
    r = kopiere_doterra_md(refresh)
    print(f"  {r}")

    # Gesamtgrösse
    if BUNDLE_DIR.exists():
        total = sum(p.stat().st_size for p in BUNDLE_DIR.rglob("*") if p.is_file()) / (1024 * 1024)
        print(f"\n=== Bundle-Gesamtgrösse: {total:.1f} MB ===")


if __name__ == "__main__":
    main()
