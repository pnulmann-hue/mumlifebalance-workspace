"""
Posting-Checker — abendlicher Live-Check Mo-Fr 19:00.

Liest context/insta-post-schedule.json + scripts/blotato-post/post-configs/*.json
und schickt Patricia eine Telegram-Nachricht mit den heutigen geplanten Posts +
fragt ob sie alle live im Feed sind.

Patricia antwortet via /posting_ja oder /posting_nein.
"""
from __future__ import annotations
import json
import logging
import os
from datetime import date as date_cls, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Repo-Root finden (Cockpit-Bot läuft in scripts/cockpit-bot/)
REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_FILE = REPO_ROOT / "context" / "insta-post-schedule.json"
POST_CONFIGS_DIR = REPO_ROOT / "scripts" / "blotato-post" / "post-configs"


def _load_schedule_json() -> list[dict]:
    """Lade context/insta-post-schedule.json (zentrale Liste)."""
    try:
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("schedule", [])
    except FileNotFoundError:
        logger.warning(f"Schedule-Datei fehlt: {SCHEDULE_FILE}")
        return []
    except Exception as e:
        logger.error(f"Schedule-Load-Error: {e}")
        return []


def _load_post_configs() -> list[dict]:
    """Lade Karussell-Configs aus scripts/blotato-post/post-configs/*.json."""
    posts = []
    if not POST_CONFIGS_DIR.exists():
        return posts
    for cfg_file in POST_CONFIGS_DIR.glob("*.json"):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            sched_time = cfg.get("scheduledTime", "")
            if not sched_time:
                continue
            # Extrahiere Profil aus Filename: 2026-06-15-mo-mentoring-bootcamp-promo-viral.json
            parts = cfg_file.stem.split("-")
            profile = "mentoring"  # default
            for p in parts:
                if p in ("mentoring", "doterra"):
                    profile = p
                    break
            slug = "-".join(parts[5:]) if len(parts) > 5 else cfg_file.stem
            posts.append({
                "date": sched_time[:10],
                "time": sched_time[11:16],
                "type": "karussell",
                "slug": slug,
                "profile": profile,
                "submission": cfg.get("_newSubmissionId_v2")
                              or cfg.get("_newSubmissionId")
                              or cfg.get("_submissionId"),
                "config_file": cfg_file.name,
            })
        except Exception as e:
            logger.warning(f"Config-Parse-Error {cfg_file.name}: {e}")
    return posts


def get_geplante_posts(target_date: date_cls) -> list[dict]:
    """Hole alle Posts für ein konkretes Datum aus beiden Quellen, deduped."""
    date_str = target_date.strftime("%Y-%m-%d")
    schedule = _load_schedule_json()
    configs = _load_post_configs()

    # Beide Listen mergen, mit insta-post-schedule.json als Priorität
    by_slug = {}
    for item in schedule + configs:
        if item.get("date") != date_str:
            continue
        slug = item.get("slug", "")
        if slug not in by_slug:
            by_slug[slug] = item
        else:
            # Merge: behalte existing, ergänze fehlende fields
            for k, v in item.items():
                if not by_slug[slug].get(k):
                    by_slug[slug][k] = v
    return sorted(by_slug.values(), key=lambda x: x.get("time", "00:00"))


def format_posting_check_message(target_date: date_cls) -> str | None:
    """Formatiere die Telegram-Nachricht für den Posting-Check.
    Returns None wenn keine Posts heute (z.B. Sa/So)."""
    posts = get_geplante_posts(target_date)
    if not posts:
        return None

    weekday_de = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"][target_date.weekday()]
    date_short = target_date.strftime("%d.%m.")

    lines = [
        f"📲 *POSTING-CHECK* {weekday_de} {date_short}",
        "",
        f"Heute geplant für *@mum.life.balance* ({len(posts)} Post{'s' if len(posts) > 1 else ''}):",
        "",
    ]
    type_emoji = {"karussell": "🎨", "reel": "🎬", "single-image": "🖼️"}
    for p in posts:
        emoji = type_emoji.get(p.get("type"), "📌")
        slug = p.get("slug", "?")
        time = p.get("time", "?")
        lines.append(f"  {emoji} *{time}* — {slug}")

    lines += [
        "",
        "👀 Schau kurz in deinen Feed:",
        "  ✅ Alles live → antworte `/posting_ja`",
        "  ❌ Etwas fehlt → antworte `/posting_nein` + welches",
        "",
        "Bei NEIN starte ich automatisch das Nachposten.",
    ]
    return "\n".join(lines)


# ===== Test/CLI =====
if __name__ == "__main__":
    today = date_cls.today()
    msg = format_posting_check_message(today)
    if msg:
        print(msg)
    else:
        print(f"Keine Posts für {today.isoformat()} (vermutlich Sa/So).")
