"""Launch-Engine — bestimmt für HEUTE die richtige Julia-Trost-Vorlage.

Kernlogik (genau Patricias Wunsch):
  1. Ist gerade ein Launch aktiv?  → folge dem Julia-LAUNCHKALENDER (Tag-für-Tag
     story-plan.json: Aufwärm- / Verkaufs- / Nachkaufphase mit fester Vorlage je Tag).
  2. Kein Launch aktiv?            → nimm eine Julia-STORYVORLAGE aus dem Rotations-Pool
     (julia-story-vorlagen.json), nach Wochentag + Monatsthema.

Liefert einen fertigen Markdown-Block (`prompt_block`), den claude_caller in den
Story-Auftrag injiziert — plus Meta (empfohlenes Profil, CTA, Phase).

Reine Datei-/Datums-Logik, KEIN API-Key nötig → via `python launch_engine.py` testbar.
"""

from __future__ import annotations

import json
import logging
from datetime import date, datetime
from pathlib import Path
from typing import Any

import config

logger = logging.getLogger(__name__)


# ========================================
# Loader (mit Mini-Cache je Prozess)
# ========================================
_cache: dict[str, Any] = {}


def _load_json(path: Path) -> dict | None:
    key = str(path)
    if key in _cache:
        return _cache[key]
    if not path or not Path(path).exists():
        logger.warning(f"Launch-Engine: Datei fehlt: {path}")
        _cache[key] = None
        return None
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        _cache[key] = data
        return data
    except Exception as e:
        logger.error(f"Launch-Engine: konnte {path} nicht laden: {e}")
        _cache[key] = None
        return None


def _parse_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return date.fromisoformat(str(s)[:10])
    except (ValueError, TypeError):
        return None


# ========================================
# Story-Plan-Discovery
# ========================================

def _discover_story_plans() -> list[Path]:
    """Findet alle aktiven story-plan.json (Archiv-Dateien ausgeschlossen)."""
    plans: list[Path] = []
    # 1. Explizit konfigurierte
    for p in getattr(config, "LAUNCH_STORY_PLANS", []):
        pp = Path(p)
        if pp.exists():
            plans.append(pp)
    # 2. Auto-Discovery unter outputs/produkte/**/story-plan.json
    base = config.WORKSPACE_ROOT / "outputs" / "produkte"
    if base.is_dir():
        for pp in base.glob("**/story-plan.json"):
            if "archiv" in pp.name.lower():
                continue
            if pp not in plans:
                plans.append(pp)
    return plans


# ========================================
# Aktiven Launch für HEUTE finden
# ========================================

def find_active_launch(heute: date) -> dict | None:
    """Gibt den story-plan zurück dessen Launch-Fenster heute umschliesst, sonst None."""
    for path in _discover_story_plans():
        plan = _load_json(path)
        if not plan or "phasen" not in plan:
            continue
        phasen = plan["phasen"]
        starts = [_parse_date(p.get("von")) for p in phasen.values()]
        ends = [_parse_date(p.get("bis")) for p in phasen.values()]
        starts = [d for d in starts if d]
        ends = [d for d in ends if d]
        if not starts or not ends:
            continue
        if min(starts) <= heute <= max(ends):
            plan["_source_path"] = str(path)
            return plan
    return None


def _phase_fuer_heute(plan: dict, heute: date) -> str | None:
    for name, p in plan.get("phasen", {}).items():
        von, bis = _parse_date(p.get("von")), _parse_date(p.get("bis"))
        if von and bis and von <= heute <= bis:
            return name
    return None


def _tageseintrag(plan: dict, heute: date, phase: str | None) -> tuple[dict | None, bool]:
    """Findet den Tageseintrag für heute. Returnt (eintrag, ist_fallback)."""
    tage = plan.get("tage", [])
    # Exakter Tag
    for t in tage:
        if _parse_date(t.get("datum")) == heute:
            return t, False
    # Fallback: letzter vergangener Tag in derselben Phase
    kandidaten = [
        t for t in tage
        if _parse_date(t.get("datum")) and _parse_date(t["datum"]) <= heute
        and (phase is None or t.get("phase") == phase)
    ]
    if kandidaten:
        kandidaten.sort(key=lambda t: _parse_date(t["datum"]))
        return kandidaten[-1], True
    # Fallback: erster Tag der Phase
    phasen_tage = [t for t in tage if phase is None or t.get("phase") == phase]
    if phasen_tage:
        return phasen_tage[0], True
    return None, True


# ========================================
# Julia-Vorlagen-Text bauen
# ========================================

def _vorlage_aus_kalender(vorlage_key: str) -> dict | None:
    kal = _load_json(config.JULIA_LAUNCH_KALENDER) or {}
    return kal.get("vorlagen", {}).get(vorlage_key)


def _phase_info(phase: str) -> dict | None:
    kal = _load_json(config.JULIA_LAUNCH_KALENDER) or {}
    return kal.get("phasen", {}).get(phase)


# ========================================
# HAUPTFUNKTION
# ========================================

def get_story_kontext(heute: date | None = None, profil: str | None = None) -> dict:
    """Liefert den kompletten Launch-/Vorlagen-Kontext für heute.

    Returns dict mit u.a.:
      launch_aktiv, phase, tag_im_launch, tage_bis_cart_close, funnel_id,
      empf_profil, julia_vorlage_key, julia_vorlage (dict),
      cta, cta_keyword, tagesplan (dict|None), prompt_block (str)
    """
    if heute is None:
        heute = date.today()

    plan = find_active_launch(heute)

    if plan:
        return _kontext_launch(plan, heute, profil)
    return _kontext_kein_launch(heute, profil)


def _kontext_launch(plan: dict, heute: date, profil: str | None) -> dict:
    phase = _phase_fuer_heute(plan, heute)
    eintrag, ist_fallback = _tageseintrag(plan, heute, phase)
    phase = (eintrag or {}).get("phase", phase)

    vorlage_key = (eintrag or {}).get("julia_vorlage", "")
    vorlage = _vorlage_aus_kalender(vorlage_key) or {}
    phase_info = _phase_info(phase or "") or {}
    phasen_meta = plan.get("phasen", {}).get(phase or "", {})

    empf_profil = profil or (eintrag or {}).get("profil") or plan.get("profil", "mentoring")

    # Tag-Index im Launch
    tage = plan.get("tage", [])
    tag_idx = next((i + 1 for i, t in enumerate(tage)
                    if _parse_date(t.get("datum")) == heute), None)
    cart_close = _parse_date(plan.get("phasen", {}).get("verkaufsphase", {}).get("bis"))
    tage_bis_cart_close = (cart_close - heute).days if cart_close else None

    cta = (eintrag or {}).get("cta") or phasen_meta.get("cta_typ", "")
    cta_keyword = (eintrag or {}).get("cta_keyword", phasen_meta.get("cta_keyword"))

    # Prompt-Block
    lines = []
    lines.append("## 🚀 LAUNCH AKTIV — folge dem Julia-Launchkalender (Pflicht)")
    lines.append(f"**Launch:** {plan.get('produkt_kostenlos','')} → {plan.get('produkt_bezahlt','')}")
    lines.append(f"**Phase heute:** {phase} — {phase_info.get('ziel','')}")
    if tag_idx:
        lines.append(f"**Launch-Tag:** {tag_idx} von {len(tage)}")
    if tage_bis_cart_close is not None:
        lines.append(f"**Tage bis Cart-Close:** {tage_bis_cart_close}")
    lines.append(f"**Phasen-Intensität:** {phase_info.get('intensitaet','')}")
    if ist_fallback:
        lines.append("_(Kein exakter Tageseintrag für heute — nächstliegende Vorlage der Phase verwendet.)_")
    lines.append("")
    lines.append(f"### Heutige Story-Vorlage: **{vorlage.get('name', vorlage_key)}**")
    if eintrag and eintrag.get("titel"):
        lines.append(f"**Titel/Aufhänger:** {eintrag['titel']}")
    if eintrag and eintrag.get("story_ziel"):
        lines.append(f"**Ziel dieser Story:** {eintrag['story_ziel']}")
    if vorlage.get("julia_anleitung"):
        lines.append(f"**Aufbau-Anleitung:** {vorlage['julia_anleitung']}")
    if vorlage.get("slide_bogen"):
        lines.append(f"**Slide-Bogen:** {vorlage['slide_bogen']}")
    kaeufertyp = (eintrag or {}).get("kaeufertyp") or vorlage.get("kaeufertyp", "")
    if kaeufertyp:
        lines.append(f"**Käufertyp heute besonders ansprechen:** {kaeufertyp}")
    lines.append("")
    lines.append(f"**CTA heute:** {cta}")
    if cta_keyword:
        lines.append(f"**CTA-Keyword:** {cta_keyword} (Pflicht-Lookup in active-funnels.json)")
    lines.append("")
    lines.append("**WICHTIG:** Diese Vorlage + dieses Ziel sind verbindlich für heute. "
                 "Struktur folgt dem Launchkalender, die Stimme bleibt 100% Patricia "
                 "(keine Stakkato-Sätze, Schweizer ss, keine erfundenen Zahlen). "
                 "Julia Trost NIE namentlich nennen.")

    return {
        "launch_aktiv": True,
        "launch_id": plan.get("launch_id"),
        "funnel_id": plan.get("funnel_id"),
        "fuehrt_zu": plan.get("fuehrt_zu"),
        "phase": phase,
        "tag_im_launch": tag_idx,
        "tage_bis_cart_close": tage_bis_cart_close,
        "ist_fallback": ist_fallback,
        "empf_profil": empf_profil,
        "julia_vorlage_key": vorlage_key,
        "julia_vorlage": vorlage,
        "tagesplan": eintrag,
        "cta": cta,
        "cta_keyword": cta_keyword,
        "prompt_block": "\n".join(lines),
        "source_path": plan.get("_source_path"),
    }


def _kontext_kein_launch(heute: date, profil: str | None) -> dict:
    pool = _load_json(config.JULIA_STORY_VORLAGEN) or {}
    rotation = pool.get("wochen_rotation", {})
    vorlagen = pool.get("vorlagen", {})
    saeulen = pool.get("drei_saeulen", {})

    wd = str(heute.weekday())
    vorlage_key = rotation.get(wd, "lehrreich-mini-training")
    vorlage = vorlagen.get(vorlage_key, {})
    saeule = vorlage.get("saeule", "")

    lines = []
    lines.append("## 📖 KEIN LAUNCH AKTIV — folge der Julia-Storyvorlage des Tages")
    lines.append(f"### Heutige Vorlage: **{vorlage.get('name', vorlage_key)}**")
    if saeule:
        lines.append(f"**Säule:** {saeule} — {saeulen.get(saeule,'')}")
    if vorlage.get("ziel"):
        lines.append(f"**Ziel:** {vorlage['ziel']}")
    if vorlage.get("julia_anleitung"):
        lines.append(f"**Aufbau-Anleitung:** {vorlage['julia_anleitung']}")
    if vorlage.get("slide_bogen"):
        lines.append(f"**Slide-Bogen:** {vorlage['slide_bogen']}")
    if vorlage.get("kaeufertyp"):
        lines.append(f"**Käufertyp heute:** {vorlage['kaeufertyp']}")
    lines.append("")
    lines.append("**CTA-Regel (Kernregel 1):** Jede Story braucht einen CTA-Link auf ein "
                 "0€-Freebie aus active-funnels.json. "
                 f"Freebie-Hinweis: {vorlage.get('freebie_cta','thematisch passend wählen')}.")
    lines.append("")
    lines.append("**WICHTIG:** Verbinde diese Vorlage mit dem MONATSTHEMA (siehe Monats-Kontext) "
                 "und Patricias Input. Struktur folgt der Vorlage, Stimme bleibt 100% Patricia "
                 "(keine Stakkato, Schweizer ss, keine erfundenen Zahlen). Julia Trost NIE namentlich nennen.")

    return {
        "launch_aktiv": False,
        "launch_id": None,
        "phase": None,
        "empf_profil": profil or "",  # leer = Bot nutzt Wochentag-Rotation
        "julia_vorlage_key": vorlage_key,
        "julia_vorlage": vorlage,
        "tagesplan": None,
        "cta": vorlage.get("freebie_cta", ""),
        "cta_keyword": None,
        "prompt_block": "\n".join(lines),
        "source_path": str(config.JULIA_STORY_VORLAGEN),
    }


# ========================================
# CLI-Tester (kein API-Key nötig)
# ========================================
if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Optional: Datum als Argument (YYYY-MM-DD) zum Durchspielen
    if len(sys.argv) > 1:
        test_date = date.fromisoformat(sys.argv[1])
    else:
        test_date = date.today()

    print(f"=== Launch-Engine Test für {test_date.isoformat()} ({['Mo','Di','Mi','Do','Fr','Sa','So'][test_date.weekday()]}) ===\n")
    print("Gefundene Story-Pläne:")
    for p in _discover_story_plans():
        print(f"  - {p}")
    print()

    k = get_story_kontext(test_date)
    print(f"Launch aktiv: {k['launch_aktiv']}")
    if k["launch_aktiv"]:
        print(f"  Phase: {k['phase']} · Tag {k.get('tag_im_launch')} · bis Cart-Close: {k.get('tage_bis_cart_close')}")
        print(f"  Empf. Profil: {k['empf_profil']}")
    print(f"  Vorlage: {k['julia_vorlage_key']}")
    print(f"  CTA: {k['cta']} (Keyword: {k.get('cta_keyword')})")
    print("\n--- PROMPT-BLOCK ---\n")
    print(k["prompt_block"])

    # Mini-Selbsttest über mehrere Stichtage
    print("\n\n=== Phasen-Durchlauf (Stichproben) ===")
    for ds in ["2026-06-10", "2026-06-15", "2026-06-29", "2026-07-03", "2026-07-06", "2026-07-08", "2026-07-20"]:
        d = date.fromisoformat(ds)
        kk = get_story_kontext(d)
        tag = f"Tag {kk.get('tag_im_launch')}" if kk.get("tag_im_launch") else "-"
        print(f"  {ds}: launch={kk['launch_aktiv']!s:5} phase={str(kk.get('phase')):16} {tag:7} vorlage={kk['julia_vorlage_key']}")
