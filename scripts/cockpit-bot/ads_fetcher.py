"""Ads-Fetcher — liest Meta Marketing API + baut Performance-Block.

Wird vom Cockpit-Bot täglich im Morgen-Briefing aufgerufen. Liest alle
ACTIVE-Kampagnen und liefert zwei Output-Formate:

- `fetch_ads_block(modus="kompakt")` → 2-4 Zeilen für Telegram-Push
- `fetch_ads_block(modus="volltext")` → ausführlicher Markdown-Block für Notion

Performance-Heuristiken nach Julia-Trost (aus dem Anzeigen-Konzept):
- ✅ SKALIEREN:  CTR > 1.5% AND CPL < 8 CHF AND Frequency < 1.8
- ⚠️ BEOBACHTEN: 0-2 Anmeldungen, Spend > 50 CHF, CTR 0.8-1.5%
- 🛑 PAUSIEREN:  CTR < 0.5% ODER CPL > 15 CHF ODER Frequency > 2.5 ODER
                 (0 Anmeldungen UND Spend > 50 CHF)

Wenn keine ACTIVE-Kampagnen → leerer String (Bot überspringt Sektion).
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


def _token() -> str | None:
    return os.getenv("META_ACCESS_TOKEN") or None


def _ad_account() -> str | None:
    return os.getenv("META_AD_ACCOUNT_ID") or None


def _currency() -> str:
    return os.getenv("META_CURRENCY", "CHF")


# ============================================================
# Meta-API Calls
# ============================================================

def _meta_get(path: str, params: dict | None = None, timeout: float = 15.0) -> dict:
    token = _token()
    if not token:
        raise RuntimeError("META_ACCESS_TOKEN fehlt")
    params = params or {}
    params["access_token"] = token
    res = httpx.get(f"{BASE_URL}{path}", params=params, timeout=timeout)
    res.raise_for_status()
    return res.json()


def list_active_campaigns() -> list[dict]:
    acc = _ad_account()
    if not acc:
        return []
    fields = "id,name,status,objective,daily_budget,start_time,stop_time,created_time"
    data = _meta_get(f"/{acc}/campaigns", {"fields": fields, "limit": 50})
    items = data.get("data", [])
    return [c for c in items if c.get("status") == "ACTIVE"]


def get_campaign_insights(campaign_id: str, days: int = 1) -> dict | None:
    """Holt Insights für eine Kampagne. days=1 → 'today', days=7 → 'last_7d'."""
    fields = ",".join([
        "impressions", "clicks", "ctr", "cpc", "cpm", "spend", "reach", "frequency",
        "actions", "cost_per_action_type",
    ])
    if days <= 1:
        date_preset = "today"
    elif days <= 2:
        date_preset = "yesterday"
    elif days <= 7:
        date_preset = "last_7d"
    elif days <= 30:
        date_preset = "last_30d"
    else:
        date_preset = "last_90d"
    try:
        data = _meta_get(f"/{campaign_id}/insights", {
            "fields": fields,
            "date_preset": date_preset,
            "level": "campaign",
        })
        items = data.get("data", [])
        return items[0] if items else None
    except Exception as e:
        logger.warning(f"Insights-Fetch für {campaign_id} fehlgeschlagen: {e}")
        return None


# ============================================================
# Action-Extraktion (Anmeldungen, Landing-Page-Views)
# ============================================================

LEAD_ACTION_TYPES = {
    "lead",
    "complete_registration",
    "offsite_conversion.fb_pixel_lead",
    "offsite_conversion.fb_pixel_complete_registration",
    "onsite_conversion.lead_grouped",
}


def _extract_actions(insights: dict) -> dict[str, int]:
    """Liest impf. Patriarch.: Anmeldungen, Landing-Page-Views, Link-Clicks."""
    actions = insights.get("actions") or []
    out = {"leads": 0, "lpv": 0, "link_clicks": 0}
    for a in actions:
        t = a.get("action_type", "")
        val = int(float(a.get("value", 0)))
        if t in LEAD_ACTION_TYPES:
            out["leads"] += val
        elif t == "landing_page_view":
            out["lpv"] += val
        elif t == "link_click":
            out["link_clicks"] += val
    return out


def _extract_cpl(insights: dict) -> float | None:
    """Cost per Lead aus cost_per_action_type."""
    cpa = insights.get("cost_per_action_type") or []
    for a in cpa:
        if a.get("action_type") in LEAD_ACTION_TYPES:
            try:
                return float(a.get("value", 0))
            except Exception:
                pass
    return None


# ============================================================
# Performance-Diagnose (Julia-Heuristik)
# ============================================================

def diagnose(insights: dict) -> tuple[str, str]:
    """Liefert (status_emoji, empfehlung_short).

    status_emoji: ✅/⚠️/🛑/⏳
    empfehlung_short: 1-Zeile-Empfehlung
    """
    spend = float(insights.get("spend") or 0)
    ctr = float(insights.get("ctr") or 0)
    freq = float(insights.get("frequency") or 0)
    acts = _extract_actions(insights)
    leads = acts["leads"]
    cpl = _extract_cpl(insights)

    # Zu wenig Daten
    if spend < 5:
        return "⏳", "noch zu wenig Daten — beobachten"

    # 🛑 Pausieren
    if ctr < 0.5:
        return "🛑", f"CTR {ctr:.2f}% zu tief — Hook wechseln oder pausieren"
    if cpl is not None and cpl > 15 and spend > 30:
        return "🛑", f"CPL {cpl:.1f} {_currency()} zu hoch — Creative/Audience überprüfen"
    if freq > 2.5:
        return "🛑", f"Frequency {freq:.1f} zu hoch — Audience Fatigue, pausieren"
    if leads == 0 and spend > 50:
        return "🛑", f"0 Anmeldungen nach {spend:.0f} {_currency()} — pausieren oder neues Creative"

    # ✅ Skalieren
    if ctr >= 1.5 and (cpl is None or cpl <= 8) and freq < 1.8 and leads >= 3:
        return "✅", f"Performance stark — Budget +20-30% erhöhen"

    # ⚠️ Beobachten
    if ctr >= 1.0 and (cpl is None or cpl <= 12):
        return "⚠️", "OK aber nicht stark — beobachten + ggf. neues Creative testen"

    return "⚠️", "mittlere Performance — heute weiter beobachten"


# ============================================================
# Formatter
# ============================================================

def _format_campaign_line_kompakt(c: dict, insights: dict | None) -> str:
    if not insights:
        return f"• {c.get('name', '?')[:40]}: noch keine Daten heute"

    spend = float(insights.get("spend") or 0)
    ctr = float(insights.get("ctr") or 0)
    acts = _extract_actions(insights)
    leads = acts["leads"]
    emoji, rec = diagnose(insights)
    curr = _currency()

    return f"{emoji} {spend:.0f}{curr} · {leads} Lead{'' if leads == 1 else 's'} · CTR {ctr:.1f}% · {rec}"


def _format_campaign_volltext(c: dict, insights_today: dict | None,
                              insights_7d: dict | None) -> str:
    name = c.get("name", "?")
    curr = _currency()
    cid = c.get("id", "")

    lines = [f"### {name}"]
    lines.append(f"_Campaign-ID: `{cid}`_\n")

    if insights_today:
        spend = float(insights_today.get("spend") or 0)
        imp = int(float(insights_today.get("impressions") or 0))
        clicks = int(float(insights_today.get("clicks") or 0))
        ctr = float(insights_today.get("ctr") or 0)
        cpc = float(insights_today.get("cpc") or 0)
        cpm = float(insights_today.get("cpm") or 0)
        freq = float(insights_today.get("frequency") or 0)
        reach = int(float(insights_today.get("reach") or 0))
        acts = _extract_actions(insights_today)
        cpl = _extract_cpl(insights_today)
        emoji, rec = diagnose(insights_today)

        lines.append("**Heute:**")
        lines.append(f"- Status: {emoji} {rec}")
        lines.append(f"- Spend: {spend:.2f} {curr}")
        lines.append(f"- Reach: {reach} · Impressions: {imp}")
        lines.append(f"- Clicks: {clicks} · CTR: {ctr:.2f}% · CPC: {cpc:.2f} {curr} · CPM: {cpm:.2f} {curr}")
        lines.append(f"- Frequency: {freq:.2f}")
        lines.append(f"- Landing-Page-Views: {acts['lpv']}")
        lines.append(f"- Anmeldungen (Leads): {acts['leads']}{f' · CPL {cpl:.2f} {curr}' if cpl else ''}")
    else:
        lines.append("**Heute:** Noch keine Daten (Kampagne neu oder Auslieferung blockiert)")

    if insights_7d:
        spend7 = float(insights_7d.get("spend") or 0)
        acts7 = _extract_actions(insights_7d)
        cpl7 = _extract_cpl(insights_7d)
        ctr7 = float(insights_7d.get("ctr") or 0)
        lines.append("")
        lines.append("**Letzte 7 Tage:**")
        lines.append(f"- Total-Spend: {spend7:.2f} {curr}")
        lines.append(f"- Total-Anmeldungen: {acts7['leads']}{f' · Ø-CPL {cpl7:.2f} {curr}' if cpl7 else ''}")
        lines.append(f"- Ø-CTR: {ctr7:.2f}%")

    return "\n".join(lines)


# ============================================================
# Public API
# ============================================================

def fetch_ads_block(modus: str = "kompakt") -> str:
    """Liest aktive Kampagnen + erzeugt formatierten Block.

    modus="kompakt"  → 2-4 Zeilen für Telegram-Push
    modus="volltext" → ausführlicher Markdown-Block für Notion-Page

    Returns "" wenn keine aktiven Kampagnen oder Meta-API nicht konfiguriert.
    """
    if not _token() or not _ad_account():
        logger.info("Meta-Credentials fehlen → Ads-Block übersprungen")
        return ""

    try:
        active = list_active_campaigns()
    except Exception as e:
        logger.warning(f"Active-Campaigns-Fetch fehlgeschlagen: {e}")
        return ""

    if not active:
        return ""

    if modus == "kompakt":
        # Telegram: Sehr knapp
        lines = ["📊 ANZEIGEN"]
        for c in active[:3]:  # max 3 in Kompakt
            ins = get_campaign_insights(c["id"], days=1)
            lines.append(_format_campaign_line_kompakt(c, ins))
        return "\n".join(lines)

    # Volltext für Notion
    parts = ["## 📊 Werbeanzeigen-Performance", ""]
    for c in active:
        ins_today = get_campaign_insights(c["id"], days=1)
        ins_7d = get_campaign_insights(c["id"], days=7)
        parts.append(_format_campaign_volltext(c, ins_today, ins_7d))
        parts.append("")
    parts.append("**Skalierungs-Heuristik (Julia Trost):**")
    parts.append("- ✅ Skalieren: CTR >1.5% · CPL <8 CHF · Frequency <1.8 · min. 3 Leads")
    parts.append("- ⚠️ Beobachten: CTR 1.0-1.5% · weiter Daten sammeln")
    parts.append("- 🛑 Pausieren: CTR <0.5% · CPL >15 CHF · Frequency >2.5 · 0 Leads bei >50 CHF Spend")

    return "\n".join(parts)


# ============================================================
# CLI-Test
# ============================================================

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    mode = sys.argv[1] if len(sys.argv) > 1 else "kompakt"
    print(f"--- Ads-Block ({mode}) ---")
    print(fetch_ads_block(modus=mode))
