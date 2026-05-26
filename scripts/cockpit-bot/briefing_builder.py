"""Briefing-Builder — generiert Tagesbriefings via Claude API.

Nutzt Notion-Reads + Claude für mobile-friendly Telegram-Briefings.
Output max ~1500 Zeichen damit Telegram-Format gut lesbar bleibt.
"""

from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any

from anthropic import Anthropic

import config

logger = logging.getLogger(__name__)


_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        if not config.ANTHROPIC_API_KEY:
            raise RuntimeError("ANTHROPIC_API_KEY fehlt")
        _client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
    return _client


def _read_context_file(rel_path: str) -> str:
    full = config.WORKSPACE_ROOT / rel_path
    if not full.exists():
        return ""
    try:
        return full.read_text(encoding="utf-8")
    except Exception:
        return ""


# ========================================
# System-Prompt
# ========================================

def build_system_prompt(modus: str = "morgen") -> str:
    """Baut System-Prompt für Cockpit-Briefing-Generierung."""

    pflicht_lese = ""
    for f in config.PFLICHT_LESE_LISTE:
        content = _read_context_file(f)
        if content:
            pflicht_lese += f"\n\n## DATEI: {f}\n{content[:3000]}\n"

    if modus == "morgen_kompakt":
        # Telegram-Push-Format (kompakt, mit Notion-Link)
        format_section = """
## OUTPUT-FORMAT (Mobile-Friendly Telegram, max 1200 Zeichen)

Dies ist die KOMPAKTE Version für Push aufs Handy. Volltext kommt
separat als Notion-Page (Link wird nachher angehängt).

```
🌅 [Wochentag] [DD.MM.] · KW [WW] · [Profil]

WOCHE: [Wochenfokus 1 Zeile]
HEUTE: [Hauptbrocken 1 Zeile]

🎯 TOP 3 HEBEL
1. [Money-Making-Hebel mit Outcome]
2. [Hebel]
3. [Hebel]

✋ NICHT heute: [3 Sachen die ablenken]
💪 Wenn nur 2h: [DER eine Hebel]

[FALLS ads_block_kompakt im User-Prompt vorhanden — direkt darunter einfügen, WORTGENAU. Sonst weglassen.]

📰 [Mo: „News heute: KI · Insta · Solopreneur (6 Themen)" | Di-Fr: „News-Bericht: kommt jeden Mo"]
```

**WICHTIG:**
- Schreibe NICHT „📋 Voller Bericht mit Links:" am Ende — der wird vom Bot-Code
  automatisch angehängt mit der Notion-URL
- Mo: News-Tags zeigen, weil grosser News-Bericht in Notion ist
- Di-Fr: kein News-Tag-Block — stattdessen Hinweis dass News-Bericht Mo kommt
- Du endest mit der News-Zeile (Mo) oder dem News-Bericht-Hinweis (Di-Fr)

REGELN für Telegram-Format:
- Mobile-Friendly: kurze Zeilen
- KEINE erfundenen Zahlen / Daten — Ads-Zahlen NUR aus ads_block_kompakt übernehmen
- News nur als 1-Zeilen-Tags (Volltext ist in Notion)
- Bei Sa+So: kurzer FREI-Push („Heute Auszeit. Lieb dich.")
"""
    elif modus == "morgen_volltext":
        # Notion-Page-Format (vollständig, mit klickbaren Links)
        format_section = """
## OUTPUT-FORMAT (Notion-Volltext, ausführlich)

Dies ist die VOLLE Version die in deine Tagesplaner-Page geschrieben wird.
Patricia liest hier am PC mit allen Links + Erkenntnissen.

```markdown
## 🌅 Tagesbriefing [Wochentag] [DD.MM.YYYY] · KW [WW]

**Profil heute:** [Mentoring / doTERRA]

---

## 📅 Diese Woche

[Wochenfokus aus Notion-Wochenplan]

**Wochen-Hauptprodukt:** [Produkt]
**Sales-Pattern:** [Pattern]

---

## 🎯 Heute

**Hauptbrocken:** [aus Hauptbrocken-Rotation]

### Tagesplan (08:00-11:30, 3,5h)

- 08:00–08:15  Briefing lesen
- 08:15–10:00  [Hauptbrocken-Action mit Skill-Tipp]
- 10:00–10:30  /story rendern + posten
- 10:30–11:30  DMs + Mails + 1 Outreach

### Top 3 Hebel (Money-Making-First)

1. [Hebel] — Erwartet: [konkretes Outcome]
2. [Hebel] — Erwartet: [...]
3. [Hebel] — Erwartet: [...]

### Schutz

- ✋ NICHT heute: [3 Sachen]
- 💪 Wenn nur 2h: [DER eine Hebel]
- 🛏️ Auszeit: Nachmittag ab 11:30

---

## 📋 Tasks aus Notion (heute fällig)

- [Task aus Aufgaben-DB]
- [Task]
- ...

---

[FALLS ads_block_volltext im User-Prompt vorhanden — hier WORTGENAU einfügen. Komplettes Markdown übernehmen inkl. Heuristik-Block. Falls leer: kompletten Sektions-Block weglassen.]

---

## 📰 News der Woche (mit Quellen)

### 🤖 KI / Claude

[Pro News-Item: Headline + 1-2 Sätze Beschreibung + Original-URL als KLICKBARER Link + 1-Satz Erkenntnis-Bezug zu Patricia's Business]

### 📱 Instagram

[gleiches Format]

### 🚀 Solopreneur / Digitale Produkte

[gleiches Format]

---

## 💡 Erkenntnisse für dich

[2-3 Bullet-Points die News mit Patricia's aktueller Strategie verbinden]

---

## 🎯 Skill-Tipps

→ /story [konkrete Verwendung heute]
→ /montag [falls heute Mo]
→ ...
```

REGELN für Notion-Format:
- ALLE URLs WORTGENAU aus News-Block übernehmen (nicht abkürzen)
- URLs als ganze Strings beibehalten — Notion wandelt sie automatisch in clickbare Links
- Mit Headings strukturieren
- Erkenntnisse explizit machen (Patricia will daraus lernen)
- Quellen IMMER nennen (sonst bringen die News nichts zum Vertiefen)
"""
    elif modus == "morgen":
        # Backward-compat: alter Modus → identisch mit kompakt
        format_section = """
## OUTPUT-FORMAT (Mobile-Friendly Telegram, max 1500 Zeichen)

```
🌅 [Wochentag] [DD.MM.] · KW [WW] · [Profil]

WOCHE: [Wochenfokus 1 Zeile]
HEUTE: [Hauptbrocken 1 Zeile]

🎯 TOP 3 HEBEL
1. [Hebel]
2. [Hebel]
3. [Hebel]

✋ NICHT heute: [3 Sachen]
💪 Wenn nur 2h: [DER eine Hebel]

📰 News heute: [3 Themen-Tags]

📋 Voller Bericht: [Notion-Link]
```
"""
    elif modus == "mittag":
        format_section = """
## OUTPUT-FORMAT (Mittag-Reminder, max 600 Zeichen)

```
🍽️ Mittag-Check · [Tag DD.MM.]

✅ STATUS-PRÜFUNG
□ Tageshebel angegangen?
□ Story heute schon?
□ DMs gemacht?

💪 WENN NOCH NICHT:
[Welcher Hebel rettet den Tag in 1h]

🌿 Auszeit-Reminder:
Mittagessen + Pause = OK.
Hauptbrocken-Slot war 08:15-10:00.
Was nicht gemacht: morgen rein-priorisieren.

→ /cockpit für aktuellen Tagesblick
```

REGELN:
- Sehr kurz
- Sanft, nicht antreibend
- Mittagspause ist heilig
- Lass Patricia nicht in Schuld-Spirale fallen wenn nichts passiert ist
"""
    else:
        format_section = "## Allgemeines Briefing-Format"

    return f"""# Cockpit-Bot · Patricia's Daily Operator

Du bist Patricia's Tagesblick-Assistent. Generierst kompakte, mobile-friendly
Telegram-Briefings für Patricia (Solopreneurin, vierfache Mama, Mum Life Balance).

## Deine Rolle
- INFO-LIEFERANT, nicht Moralprediger
- Liest ihr Notion-System (Wochenplan, Monatsplan, Aufgaben, Ziele)
- Generiert Briefing nach festem Format unten
- Spricht Patricia direkt an, du-Form

## Pflicht-Wissen über Patricia
{pflicht_lese}

{format_section}

## Anti-Halluzinations-Härtung
- KEINE erfundenen Zahlen/Daten
- Patricia ist vierfache Mama (steht in personal-info.md)
- 40k CHF/JAHR ist ihr Jahresziel (NICHT pro Monat)
- Cart-Open Mama-CEO Mi 20.5.2026, Cart-Close Mi 27.5.
- Webinar KI-Mastermind Mi 20.5. 09:00 (gleicher Tag wie Cart-Open)
- doTERRA-Phase 1 läuft Mai-Juli (Eimer dichten)

## Deine Antwort
Direkt der Telegram-Text, kein Markdown-Codeblock-Wrapper, kein „hier dein Briefing".
"""


# ========================================
# User-Prompt
# ========================================

def build_user_prompt(modus: str, kontext: dict[str, Any], heute: date = None) -> str:
    """Baut User-Prompt mit aktuellem Notion-Kontext."""
    if heute is None:
        heute = date.today()

    wochentag = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'][heute.weekday()]
    profil = config.TAGES_PROFIL_ROTATION.get(heute.weekday(), "frei")
    hauptbrocken = config.HAUPTBROCKEN_ROTATION.get(heute.weekday(), "FREI")

    # Erster Mo im Monat = Blog-Day Override
    if heute.weekday() == 0 and heute.day <= 7:
        hauptbrocken = "BLOG-DAY (1. Mo): Blog zum Monatsthema schreiben (~/blog-Skill)"

    parts = []
    parts.append(f"# {modus.upper()}-BRIEFING · {heute.strftime('%a %d.%m.%Y')}")
    parts.append(f"\nWochentag: {wochentag} (KW {heute.isocalendar().week})")
    parts.append(f"Profil: {profil}")
    parts.append(f"Hauptbrocken: {hauptbrocken}")

    if kontext.get("monatsplan"):
        m = kontext["monatsplan"]
        parts.append(f"\n## Monats-Trio:")
        if m.get("gratis_fokus"):
            parts.append(f"- 🎁 {m['gratis_fokus']['name']}")
        if m.get("mini_fokus"):
            parts.append(f"- 💸 {m['mini_fokus']['name']}")
        if m.get("gross_fokus"):
            parts.append(f"- 👑 {m['gross_fokus']['name']}")
        if m.get("begruendung_fokus"):
            parts.append(f"\nBegründung: {m['begruendung_fokus'][:500]}")

    if kontext.get("wochenplan"):
        w = kontext["wochenplan"]
        parts.append(f"\n## Aktuelle Woche")
        if w.get("wochen_hauptprodukt"):
            parts.append(f"Wochen-Hauptprodukt: {w['wochen_hauptprodukt']['name']}")
        if w.get("sales_pattern"):
            parts.append(f"Sales-Pattern: {w['sales_pattern'][:600]}")
        if w.get("fokus_der_woche"):
            parts.append(f"Wochenfokus: {w['fokus_der_woche'][:300]}")

    if kontext.get("offene_tasks"):
        parts.append(f"\n## Offene Tasks aus Aufgaben-DB:")
        for t in kontext["offene_tasks"][:10]:
            parts.append(f"- [{t.get('prioritaet', '?')}] {t.get('aufgabe', '')}")

    if kontext.get("habit_goals"):
        parts.append(f"\n## Aktive Habit Goals:")
        for h in kontext["habit_goals"][:5]:
            parts.append(f"- {h.get('name', '')}")

    # ADS-BLOCK (täglich Mo-Fr wenn aktive Kampagnen)
    ads_kompakt = kontext.get("ads_block_kompakt", "")
    ads_volltext = kontext.get("ads_block_volltext", "")
    if ads_kompakt:
        parts.append(f"\n## ADS-BLOCK KOMPAKT (für Telegram-Push)")
        parts.append(ads_kompakt)
        parts.append("INSTRUCTION (Telegram-Modus): Füge diesen Ads-Block WORTGENAU vor der News-Zeile ein. Falls kompakt-Modus: leicht kürzen erlaubt, aber Zahlen + Empfehlungen MÜSSEN unverändert bleiben.")
    if ads_volltext:
        parts.append(f"\n## ADS-BLOCK VOLLTEXT (für Notion-Page)")
        parts.append(ads_volltext)
        parts.append("INSTRUCTION (Volltext-Modus): Übernimm diesen Ads-Block WORTGENAU als eigene Sektion '## 📊 Werbeanzeigen-Performance' direkt nach den Tasks. Inklusive aller Zahlen + Heuristik-Block. Nichts kürzen, nichts hinzufügen.")
    if not ads_kompakt and not ads_volltext:
        parts.append(f"\n## KEIN ADS-BLOCK heute")
        parts.append("Keine aktiven Werbeanzeigen — Sektion komplett weglassen.")

    if kontext.get("news_block"):
        parts.append(f"\n## NEWS-BLOCK (vom news_fetcher gesammelt)")
        parts.append(kontext["news_block"])
        parts.append("\nINSTRUCTION: Übernimm den News-Block WORTGENAU in deine Output-Section '📰 News der Woche'. Behalte alle URLs unverändert für klickbare Links.")
    else:
        parts.append("\n## KEIN NEWS-BLOCK heute")
        parts.append("Heute ist kein Mo — News-Bericht erscheint wöchentlich.")
        parts.append("INSTRUCTION: Lass die Sektion '📰 News der Woche' und '💡 Erkenntnisse' im Output KOMPLETT WEG. Kein Platzhalter, einfach weglassen. Direkt zu Skill-Tipps.")

    parts.append(f"\n\nGeneriere jetzt das {modus}-Briefing nach Format-Vorgabe oben.")

    return "\n".join(parts)


# ========================================
# Hauptfunktion
# ========================================

def generate_briefing(modus: str, kontext: dict[str, Any],
                     heute: date = None) -> dict[str, Any]:
    """Generiert ein Briefing via Claude API.

    modus: "morgen" oder "mittag"
    kontext: dict mit monatsplan, wochenplan, offene_tasks, habit_goals, news_block
    """
    if heute is None:
        heute = date.today()

    # Sa+So: kurzer Auszeit-Push
    if heute.weekday() >= 5:
        text = (
            f"🌿 {['Mo','Di','Mi','Do','Fr','Sa','So'][heute.weekday()]} {heute.strftime('%d.%m.')}\n\n"
            "Heute AUSZEIT. Sa+So sind dein FREI-Block laut Wochenstruktur.\n\n"
            "Familie. Pause. Garten.\n\n"
            "→ Mo morgen 06:30 kommt nächstes Briefing.\n"
            "Lieb dich."
        )
        return {"ok": True, "text": text, "tokens_in": 0, "tokens_out": 0}

    system = build_system_prompt(modus)
    user = build_user_prompt(modus, kontext, heute)

    try:
        # DIAGNOSE: ENV-Vars auf Non-ASCII pruefen (Umlaute in Secrets fangen)
        import os as _os
        for _name in ("ANTHROPIC_API_KEY", "NOTION_API_KEY", "META_ACCESS_TOKEN",
                      "META_AD_ACCOUNT_ID", "TELEGRAM_COCKPIT_BOT_TOKEN",
                      "TELEGRAM_CHAT_ID", "CLAUDE_MODEL"):
            _val = _os.environ.get(_name, "")
            for _i, _ch in enumerate(_val):
                if ord(_ch) > 127:
                    raise ValueError(
                        f"ENV {_name} enthaelt Non-ASCII an Position {_i}: "
                        f"\\x{ord(_ch):x} (Laenge gesamt: {len(_val)})"
                    )
        client = _get_client()
        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=2000,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        logger.error(f"Claude-API-Fehler:\n{tb}")
        # Kompakter Telegram-Push: letzte 4 Frames, max ~1200 Zeichen
        short_tb = "\n".join(tb.splitlines()[-8:])
        return {"ok": False, "error": f"{type(e).__name__}: {e}\n\n{short_tb}"}

    text = response.content[0].text if response.content else ""

    return {
        "ok": True,
        "text": text.strip(),
        "tokens_in": response.usage.input_tokens if hasattr(response, "usage") else 0,
        "tokens_out": response.usage.output_tokens if hasattr(response, "usage") else 0,
    }
