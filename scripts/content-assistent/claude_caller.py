"""Claude-Caller — der Brain für die Story-Generierung.

Lädt die komplette Pflicht-Lese-Liste in den System-Prompt, erhält den User-Kontext
(Wochenplan, Monatsplan, Profil, Tag, optional Patricia-Input) und gibt eine
fertige slides.html zurück die direkt mit render_caller gerendert werden kann.

Architektur:
  build_system_prompt(profil)  → langer Skill-Prompt
  build_user_prompt(...)       → konkreter Auftrag inkl. Notion-Daten + DISG
  generate_story_html(...)     → ruft API, validiert HTML, speichert
"""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime, date
from pathlib import Path
from typing import Any

from anthropic import Anthropic

import config
import state

logger = logging.getLogger(__name__)


_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        if not config.ANTHROPIC_API_KEY:
            raise RuntimeError("ANTHROPIC_API_KEY fehlt in .env")
        _client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
    return _client


# ========================================
# Context-Datei-Loader
# ========================================

def _read_context_file(rel_path: str) -> str:
    """Liest eine Context-Datei relativ zum Workspace-Root."""
    full = config.WORKSPACE_ROOT / rel_path
    if not full.exists():
        logger.warning(f"Kontext-Datei fehlt: {rel_path}")
        return ""
    try:
        return full.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning(f"Konnte {rel_path} nicht lesen: {e}")
        return ""


def _read_context_dir(rel_dir: str, max_files: int = 8, max_chars_per_file: int = 3000) -> str:
    """Liest alle .md/.txt aus einem Verzeichnis, gekürzt."""
    full = config.WORKSPACE_ROOT / rel_dir
    if not full.is_dir():
        return ""
    parts = []
    files = sorted([p for p in full.glob("*") if p.is_file() and p.suffix in {".md", ".txt"}])[:max_files]
    for p in files:
        try:
            content = p.read_text(encoding="utf-8")[:max_chars_per_file]
            parts.append(f"### {p.name}\n{content}")
        except Exception:
            pass
    return "\n\n".join(parts)


# ========================================
# System-Prompt-Builder
# ========================================

def build_system_prompt(profil: str = "mentoring") -> str:
    """Baut den Skill-System-Prompt mit allen Pflicht-Wissens-Dokumenten."""

    sections = []

    # ===== Header =====
    sections.append("""# /story Skill — Daily Story Sales Companion

Du bist Patricias Story-Brain. Generiere eine fertige Instagram-Story-Sequenz
als komplette HTML-Datei (slides.html), die direkt von render-stories.js zu
8 PNG-Folien (1080×1920) gerendert werden kann.

## Output-Format
Du gibst NUR HTML zurück — keine Erklärung, kein Markdown-Codeblock, kein „Hier ist".
Direkt mit <!DOCTYPE html> beginnen, mit </html> enden.

## ABSOLUT KRITISCH — KEINE ERFUNDENEN ZAHLEN

**Patricia hat klar gesagt: keine Halluzinationen.**

Verboten:
- „Ich arbeite 2 Stunden am Tag" (es sei denn, Patricia hat das WORTGENAU im Input gesagt)
- „CHF 40'000 Jahresumsatz" als IST-Zustand (40k ist ihr ZIEL, kein erreichter Wert)
- „87 Prozent meiner Kundinnen ..." (Prozent erfunden)
- „X Frauen begleitet" — nur wenn Zahl WORTGENAU im Patricia-Input oder in patricia-expertise.md steht
- „in 6 Wochen" / „nach 3 Monaten" — wenn der Zeitraum nicht explizit in den Quellen steht

**Regel: Wenn du eine konkrete Zahl, Prozent, Zeitspanne oder Kunden-Anzahl
nennen WILLST, prüfe ob sie wortwörtlich in einer der geladenen Dateien oder
im Patricia-Input steht. Wenn nicht: schreibe den Satz OHNE die Zahl.**

Erlaubt sind:
- Zahlen aus Patricia-Expertise / Freebies-Datei (wenn explizit zitierbar)
- Zahlen aus dem Patricia-Input (direkter Quote von ihr)
- Allgemeine Aussagen ohne Zahl („wenig Zeit", „mit Kindern", „schon eine Weile")
- Fakten aus active-funnels.json (Preise der Produkte, KW-Daten)

Patricia ist **vierfache Mama** — das steht in personal-info.md, das darfst du nutzen.

## Harte Regeln
1. **Slide 1 ist BÄM-Hook** — keine „Hallo ihr Lieben", direkt knall.
   **ABER: NIEMALS Stakkato.** Verboten sind 2-3 abgehackte Kurzsätze hintereinander
   („Willst du was sehen? Mein Business läuft. Früher war das anders.").
   Der Hook ist EIN fliessender Gedanke mit Du-Anrede — Sätze mit Konjunktionen
   verbinden (und, aber, weil, und da). Wie am Küchentisch zu einer Freundin.
1b. **Keine vagen Selbst-Behauptungen** wie „mein Business läuft" / „heute geht's mir gut".
    Entweder konkret + wahr (aus Patricia-Input/Quellen) oder den Satz weglassen.
2. **Slide 8 ist CTA** mit konkreter Handlungsaufforderung + Link.
3. **Mix-Stil:** ca. 5 brand-designed Slides + 3 Foto-First Slides.
   **JEDE Foto-Slide trägt einen Story-Satz in der text-box** — KEINE reinen Foto-Slides
   ohne Text (das wirkt wie Füller). Jede Slide bringt die Geschichte einen Schritt weiter.
   Stock-Fotos nur wenn sie zur Aussage passen, nie als blosser Lückenfüller.
4. **KEIN Datum auf Slides** — niemand will sehen welcher Tag heute ist.
5. **Foto-Schutz:** Sticker/Text/Boxen NIE über Gesicht oder Hauptmotiv.
6. **Käufertyp-Rotation:** Sprich heute den vorgegebenen DISG-Käufertyp an.
7. **Echte Umlaute:** ä/ö/ü → echte Umlaute. Schweizer „ss" statt ß.
8. **Pflicht-Lookup vor Produkt-Erwähnung:** Erst active-funnels.json checken!
   Wenn der User-Prompt sagt „Fokus = bio-check", dann nutze EXAKT die Daten
   aus dem bio-check Funnel-Eintrag (URL, ManyChat-Keyword „BIO", Stufen).
9. **Storytelling-Voice** — kein Lehrbuch, immer in Szene.
10. **Patricia-Input ist GOLD** — wenn Patricia O-Töne, Zitate, konkrete Erlebnisse
    geliefert hat, baue sie WORTWÖRTLICH in Slides ein. Erfindekein eigenes Drumherum
    falls Patricia-Input fehlt — dann schreib Slide allgemeiner.
""")

    # ===== Pflicht-Lese-Liste =====
    sections.append("\n# === PFLICHT-WISSEN: Story-Framework ===\n")
    for f in config.PFLICHT_LESE_LISTE:
        content = _read_context_file(f)
        if content:
            sections.append(f"\n## DATEI: {f}\n{content}\n")

    # ===== Profil-spezifisches Zusatzwissen =====
    if profil in {"doterra", "beide"}:
        sections.append("\n# === ZUSATZ doTERRA-PROFIL ===\n")
        for f in config.PFLICHT_LESE_LISTE_DOTERRA:
            full = config.WORKSPACE_ROOT / f
            if full.is_file():
                content = _read_context_file(f)
                if content:
                    sections.append(f"\n## DATEI: {f}\n{content}\n")
            elif full.is_dir():
                content = _read_context_dir(f, max_files=6, max_chars_per_file=2500)
                if content:
                    sections.append(f"\n## VERZEICHNIS: {f}\n{content}\n")

    # ===== HTML-Template-Referenz =====
    sections.append(_html_template_reference())

    return "".join(sections)


def _html_template_reference() -> str:
    """Konkrete HTML-Template-Referenz für Claude — Beispiel-Slides."""
    return """

# === HTML-TEMPLATE-REFERENZ (Pflicht-Vorlage) ===

Verwende EXAKT diese HTML-Struktur. Die brand-stories.css definiert alle Klassen
(template-hook, template-foto-overlay, template-zitat, template-frage,
template-cta, template-story).

## Skelett

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>[Titel der Story-Sequenz]</title>
<link rel="stylesheet" href="../../../scripts/karussell-render/brand-stories.css">
</head>
<body class="profil-mentoring"> <!-- ODER profil-doterra -->

<div class="grid">

  <!-- SLIDE 1: HOOK (BRAND-DESIGNED) -->
  <div class="stage-wrap">
    <div class="stage">
      <div class="slide template-hook photo-main-bottom-center">
        <div class="content">
          <div class="hook-text" style="margin-top: 250px;">
            [BÄM-Hook hier — eine Aussage die einschlägt]
          </div>
        </div>
        <div class="photo-strip">
          <div style="background: linear-gradient(135deg, #12828c 0%, #29556d 100%); width:100%; height:100%;"></div>
        </div>
        <div class="brand-corner">Mum Life Balance</div>
      </div>
    </div>
    <div class="frame-label">01 Hook · Brand</div>
  </div>

  <!-- SLIDE: FOTO-FIRST mit Box-Oben -->
  <div class="stage-wrap">
    <div class="stage">
      <div class="slide template-foto-overlay box-oben photo-main-bottom-center">
        <img class="bg" src="../../../context/stock-fotos/atmosphaere-mentoring/[FOTO-DATEI].jpg" alt="[Alt]">
        <div class="text-box">
          <span class="eyebrow">[Eyebrow-Label]</span>
          <div class="body">
            [Story-Text mit] <span class="akzent-text">[Akzent]</span>
            <br><br>
            <strong>[Pointe-Satz]</strong>
          </div>
        </div>
        <div class="brand-corner">Mum Life Balance</div>
      </div>
    </div>
    <div class="frame-label">02 Foto-First</div>
  </div>

  <!-- SLIDE: ZITAT/KONTRAST (BRAND-DESIGNED) -->
  <div class="stage-wrap">
    <div class="stage">
      <div class="slide template-zitat">
        <div class="content">
          <div class="quote-marks" style="color: #dc822e;">"</div>
          <div class="quote" style="font-size: 60px;">
            [Zitat-Text mit] <span style="color: #dc822e;">[Akzent]</span>
          </div>
          <div class="signature" style="color: #dc822e;">— Patricia</div>
        </div>
      </div>
    </div>
    <div class="frame-label">03 Zitat · Brand</div>
  </div>

  <!-- SLIDE: FOTO-FIRST mit Patricia-Shootingbild (Box UNTEN bei photo-main-top) -->
  <div class="stage-wrap">
    <div class="stage">
      <div class="slide template-foto-overlay photo-main-top-center">
        <img class="bg" src="../../../context/Shootingbilder/[BILD-DATEI].jpg" alt="Patricia">
        <div class="text-box" style="bottom: 100px;">
          <span class="eyebrow">[Label]</span>
          <div class="body">
            [Insight-Text]
          </div>
        </div>
        <div class="brand-corner">Mum Life Balance</div>
      </div>
    </div>
    <div class="frame-label">05 Insight · Foto-First</div>
  </div>

  <!-- SLIDE: QUIZ/FRAGE (BRAND-DESIGNED) -->
  <div class="stage-wrap">
    <div class="stage">
      <div class="slide template-frage photo-main-top-center">
        <div class="content" style="justify-content: flex-start; padding-top: 180px;">
          <div class="frage-eyebrow">Schnell-Check</div>
          <div class="frage" style="font-size: 76px;">
            [Frage zum Mit-Reagieren]
          </div>
        </div>
        <div class="umfrage-placeholder" style="bottom: 240px;">
          <div class="umfrage-frage">Stimm ab:</div>
          <div class="umfrage-options">
            <div class="umfrage-option">[Option 1]</div>
            <div class="umfrage-option">[Option 2]</div>
            <div class="umfrage-option">[Option 3]</div>
          </div>
        </div>
        <div class="brand-corner">Mum Life Balance</div>
      </div>
    </div>
    <div class="frame-label">06 Quiz · Brand</div>
  </div>

  <!-- SLIDE: CTA -->
  <div class="stage-wrap">
    <div class="stage">
      <div class="slide template-cta">
        <div class="content">
          <div class="cta-eyebrow">Jetzt — kostenlos</div>
          <div class="cta-headline" style="font-size: 110px;">
            Tipp <span class="akzent">[KEYWORD]</span><br>in die Kommentare.
          </div>
          <div class="cta-arrow">↓</div>
          <div class="cta-text">
            [Was passiert dann]
          </div>
          <div class="cta-link-label">— heute noch loslegen</div>
        </div>
        <div class="brand-corner" style="color: rgba(241,236,221,0.6);">[Link-Domain]</div>
      </div>
    </div>
    <div class="frame-label">08 CTA · Brand</div>
  </div>

</div>

</body>
</html>
```

## Klassen-Übersicht
- **template-hook** — Slide 1, BÄM-Hook
- **template-foto-overlay** + (box-oben | nichts) + photo-main-* — Foto-First
- **template-zitat** — Patricia-Zitat-Slide
- **template-frage** — Quiz/Umfrage-Slide
- **template-cta** — Letzte Slide, Action
- **template-story** — Lösung/Produkt-Slide mit Gradient

## Foto-Quellen-Pfade (vom slides.html aus relativ — IMMER mit ../../../)
- Stock Mentoring: `../../../context/stock-fotos/atmosphaere-mentoring/`
- Stock doTERRA: `../../../context/stock-fotos/atmosphaere-doterra/`
- Stock universell: `../../../context/stock-fotos/atmosphaere-universell/`
- Patricia-Shootingbilder: `../../../context/Shootingbilder/`

Verfügbare Foto-Dateien werden im User-Prompt mitgeliefert.

## Foto-Schutz-Regel (KRITISCH)
- Wenn Patricia-Foto OBEN im Foto → Box UNTEN platzieren (`bottom: 100px`)
- Wenn Foto-Hauptmotiv UNTEN → Box OBEN (`box-oben`)
- Niemals Box über Gesicht!

## Body-Klasse
- `<body class="profil-mentoring">` für Mentoring (Petrol/Dunkelblau)
- `<body class="profil-doterra">` für doTERRA (Orange/Creme)
"""


# ========================================
# User-Prompt-Builder
# ========================================

def build_user_prompt(profil: str, kontext: dict[str, Any], heute: date = None) -> str:
    """Baut den konkreten Auftrag mit aktuellem Kontext."""
    if heute is None:
        heute = date.today()

    parts = []
    parts.append(f"# Heutige Story-Sequenz — {heute.isoformat()}")
    parts.append(f"\n**Profil:** {profil}")
    parts.append(f"**Wochentag:** {['Mo','Di','Mi','Do','Fr','Sa','So'][heute.weekday()]}")
    parts.append(f"**KW:** {heute.isocalendar().week}")

    # DISG-Käufertyp für heute
    disg = state.empfehle_disg_heute()
    parts.append(f"\n**DISG-Käufertyp heute:** {disg}")
    parts.append(f"**Kürzlich angesprochen (letzte 3 Tage):** {state.disg_letzte_3_tage()}")
    parts.append(f"**Diese Woche schon abgedeckt:** {sorted(state.disg_diese_woche())}")

    # WOCHEN-FOKUS — Override hat Vorrang vor Notion
    fokus_override = state.get_wochen_fokus_override(heute.isocalendar().week)
    if fokus_override:
        parts.append("\n## ⚠️ FOKUS-OVERRIDE (Patricia hat manuell gesetzt)")
        parts.append(f"**Diese Woche IST der Fokus:** {fokus_override['thema']}")
        if fokus_override.get("funnel_id"):
            parts.append(f"**Funnel-ID:** {fokus_override['funnel_id']} (siehe active-funnels.json)")
        if fokus_override.get("produkt"):
            parts.append(f"**Produkt:** {fokus_override['produkt']}")
        parts.append("**WICHTIG:** Dieser Override hat Vorrang vor allem — auch vor Launch-Plan und Monatsplan!")
        parts.append("")

    # === LAUNCH-STATUS / JULIA-VORLAGE DES TAGES (höchste inhaltliche Priorität) ===
    launch = kontext.get("launch")
    if launch and launch.get("prompt_block"):
        parts.append("")
        parts.append(launch["prompt_block"])
        parts.append("")

    # === MONATSPLAN (verbindliche MD-Quelle — Single Source of Truth) ===
    mp = kontext.get("monatsplan_md")
    if mp:
        parts.append(f"\n## 📅 Monats-Kontext (verbindlicher Plan: {mp.get('datei','')})")
        if mp.get("wochen_pillar"):
            parts.append(f"**Wochen-Pillar (KW {mp.get('kw')}):** {mp['wochen_pillar']}")
        if mp.get("kw_block"):
            parts.append(f"\n**Wochen-Plan dieser Woche:**\n{mp['kw_block']}")
        if mp.get("tagesslot"):
            parts.append(f"\n**Heute geplant (Feed — als Themen-Anker, die Story ergänzt das):**\n{mp['tagesslot']}")

    # Notion-Kontext
    if kontext.get("monatsplan"):
        m = kontext["monatsplan"]
        parts.append(f"\n## Monats-Kontext: {m.get('monat', '')}")
        parts.append(f"**3 Monatsziele:**\n{m.get('drei_monatsziele', '')[:1500]}")
        if m.get("body_text"):
            parts.append(f"\n**Monatsplan-Body (Themenplanung etc.):**\n{m['body_text'][:2500]}")

    if kontext.get("wochenplan"):
        w = kontext["wochenplan"]
        parts.append(f"\n## Wochen-Kontext (Notion)")
        if fokus_override:
            parts.append("⚠️ Hinweis: Der Fokus-Override oben überschreibt diesen Notion-Inhalt!")
        parts.append(f"**Fokus der Woche:** {w.get('fokus_der_woche', '')[:1000]}")
        if w.get("body_text"):
            parts.append(f"\n**Wochenplan-Body:**\n{w['body_text'][:2000]}")

    # Patricia-Input (Voice-Transkripte / Text-Antworten aus Sparring)
    if kontext.get("patricia_input"):
        parts.append(f"\n## ⭐ Patricia-Input (Sprachnotiz/Text)")
        parts.append("Diese Worte sind GOLD — baue sie WORTGENAU in die Story ein.")
        parts.append("Erfinde keine eigenen Geschichten oder Zahlen drumherum.")
        parts.append(f"\n{kontext['patricia_input']}")

    # Patricia-Foto-Hinweis
    if kontext.get("patricia_foto"):
        parts.append(f"\n## ⭐ Patricia-Foto verfügbar")
        parts.append(f"Patricia hat ein Foto geschickt: `{kontext['patricia_foto']}`")
        parts.append("Nutze ES als Patricia-Bild in Slide 5 oder 6 (statt Shootingbild).")

    # Foto-Liste
    parts.append("\n## Verfügbare Fotos\n")
    parts.append(_liste_verfuegbare_fotos(profil, max_per_kategorie=12))

    # Auftrag
    fokus_hint = ""
    if fokus_override:
        fokus_hint = f"\n- Diese Woche STRIKT auf '{fokus_override['thema']}' fokussieren"
        if fokus_override.get("funnel_id"):
            fokus_hint += f" (Funnel: {fokus_override['funnel_id']})"

    parts.append(f"""

## Dein Auftrag

Generiere eine 8-Slide-Story-Sequenz als komplette slides.html für Profil = **{profil}**.{fokus_hint}

- Mix-Stil: 5 Brand-Designed + 3 Foto-First
- DISG heute = {disg} → sprich diesen Käufertyp besonders an
- Hook in Slide 1 muss knallen (siehe hook-framework.md)
- Wenn ein Produkt/Funnel erwähnt wird: vorher active-funnels.json checken (Pflicht!)
- CTA in Slide 8 mit konkretem Handeln (Kommentar-Keyword + Link)

**ANTI-HALLUZINATIONS-CHECK** (vor jeder Slide-Zeile):
- Enthält der Satz eine konkrete Zahl/Prozent/Zeit?
- Wenn ja: Steht diese Zahl WORTGENAU im Patricia-Input oder den Pflicht-Lese-Dateien?
- Wenn nein: Schreibe den Satz UM ohne die Zahl. Lieber allgemein als erfunden.

WICHTIG: Antwort = NUR HTML (Beginn `<!DOCTYPE html>`, Ende `</html>`).
Kein Markdown, kein „Hier ist das HTML", keine Erklärung.
""")

    return "\n".join(parts)


# ========================================
# Foto-Liste
# ========================================

def _liste_verfuegbare_fotos(profil: str, max_per_kategorie: int = 12) -> str:
    """Listet verfügbare Foto-Dateinamen für Claude."""
    parts = []

    kategorien = []
    if profil in {"mentoring", "beide"}:
        kategorien.append(("atmosphaere-mentoring", "Stock Mentoring"))
    if profil in {"doterra", "beide"}:
        kategorien.append(("atmosphaere-doterra", "Stock doTERRA"))
    kategorien.append(("atmosphaere-universell", "Stock Universell"))

    for ordner, label in kategorien:
        d = config.STOCK_FOTOS_DIR / ordner
        if d.exists():
            files = sorted([f.name for f in d.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png"}])
            files = files[:max_per_kategorie]
            if files:
                parts.append(f"\n### {label} (`context/stock-fotos/{ordner}/`)\n")
                for f in files:
                    parts.append(f"- {f}")

    # Patricia-Shootingbilder
    if config.SHOOTINGBILDER_DIR.exists():
        files = sorted([f.name for f in config.SHOOTINGBILDER_DIR.iterdir()
                       if f.suffix.lower() in {".jpg", ".jpeg", ".png"}])[:max_per_kategorie]
        if files:
            parts.append(f"\n### Patricia-Shootingbilder (`context/Shootingbilder/`)\n")
            for f in files:
                parts.append(f"- {f}")

    return "\n".join(parts)


# ========================================
# Haupt-Funktion
# ========================================

def generate_story_html(profil: str, kontext: dict[str, Any], heute: date = None,
                        output_dir: Path = None, slug: str = None) -> dict[str, Any]:
    """Generiert eine slides.html-Datei via Claude API.

    Returns:
        {
          "ok": True,
          "html_path": Path,
          "slug": "2026-05-01-mentoring-bio-check-...",
          "tokens_in": int,
          "tokens_out": int,
        }
    """
    if heute is None:
        heute = date.today()

    if output_dir is None:
        if slug is None:
            slug = f"{heute.isoformat()}-{profil}-auto"
        output_dir = config.OUTPUTS_STORIES_DIR / slug
    output_dir.mkdir(parents=True, exist_ok=True)

    system = build_system_prompt(profil)
    user = build_user_prompt(profil, kontext, heute)

    # Debug-Dump
    (output_dir / "_user_prompt.md").write_text(user, encoding="utf-8")
    logger.info(f"Story-Generierung gestartet: {profil} {heute} → {output_dir.name}")
    logger.info(f"  System-Prompt: {len(system)} chars")
    logger.info(f"  User-Prompt: {len(user)} chars")

    client = _get_client()
    try:
        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=8000,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
    except Exception as e:
        logger.error(f"Claude-API-Fehler: {e}")
        return {"ok": False, "error": str(e)}

    raw = response.content[0].text if response.content else ""

    # HTML extrahieren (falls Claude doch Markdown-Codeblock liefert)
    html = _extract_html(raw)
    if not html:
        logger.error("Claude lieferte kein gültiges HTML zurück")
        (output_dir / "_raw_response.txt").write_text(raw, encoding="utf-8")
        return {"ok": False, "error": "Kein HTML in Response", "raw_path": str(output_dir / "_raw_response.txt")}

    html_path = output_dir / "slides.html"
    html_path.write_text(html, encoding="utf-8")

    # Slide-Count zählen
    slide_count = len(re.findall(r'class="[^"]*\bslide\b', html))

    return {
        "ok": True,
        "html_path": html_path,
        "output_dir": output_dir,
        "slug": output_dir.name,
        "slide_count": slide_count,
        "tokens_in": response.usage.input_tokens if hasattr(response, "usage") else 0,
        "tokens_out": response.usage.output_tokens if hasattr(response, "usage") else 0,
    }


def generate_briefing_anfrage(profil: str, kontext: dict[str, Any],
                              heute: date = None) -> dict[str, Any]:
    """Sparringpartner-Modus: Generiert eine Telegram-Briefing-Anfrage.

    Statt sofort eine Story zu generieren, schickt der Bot Patricia einen
    Vorschlag was er heute machen würde + 3-5 konkrete Fragen, die sie
    beantworten soll. Dann wartet er auf Antwort und generiert erst dann.

    Returns:
        {
          "ok": True,
          "telegram_text": "<formatted text>",
          "fragen": ["Frage 1", "Frage 2", ...],
          "tokens_in": int,
          "tokens_out": int,
        }
    """
    if heute is None:
        heute = date.today()

    # Mini-System-Prompt — keine Pflicht-Lese-Liste, viel kürzer
    system = """Du bist Patricias Story-Sparringpartner. Aufgabe: Bevor du eine Story generierst,
fragst du Patricia nach den konkreten Details damit nichts erfunden werden muss.

Du formulierst eine kurze, persönliche Telegram-Nachricht (max. 800 Zeichen) die:
1. Zeigt welchen Fokus du heute siehst (in dieser Reihenfolge: Patricia-Override > Launch-Vorlage des Tages > Monatsplan-Wochenthema)
2. Schlägt 1 konkreten Story-Ansatz vor. WENN ein Launch aktiv ist: der Ansatz MUSS der vorgegebenen Julia-Launch-Vorlage + dem Tagesziel folgen (nicht frei erfinden). WENN kein Launch: folge der Julia-Storyvorlage des Tages + dem Monatsthema.
3. Stellt 3-5 KONKRETE Fragen, die Patricia per Sprachnotiz oder Text beantworten kann
4. Fragt am Ende: „Hast du ein aktuelles Foto/Video? Sonst nehme ich Shootingbilder."

Output-Format:
- DU-Form, locker, freundlich (Patricia mag keine KI-Floskeln)
- Keine Headers/Markdown-Codeblöcke — direkt der Telegram-Text
- Konkrete Fragen mit Bullet-Points
- Sprachnotiz aktiv anbieten („du kannst das auch per Sprachnotiz beantworten")

Anti-Halluzination: Erfinde KEINE Zahlen/Fakten in deinem Vorschlag. Wenn du nicht
weisst was Patricia diese Woche genau macht, FRAG sie — schlage nicht vor.

Output ist ein JSON-Block mit zwei Feldern:
```json
{
  "telegram_text": "der Text der per Telegram gesendet wird",
  "fragen": ["Frage 1", "Frage 2", ...]
}
```
Nichts anderes. Keine weitere Erklärung."""

    # User-Prompt: Kontext zusammenstellen
    user_parts = []
    user_parts.append(f"Heute: {heute.isoformat()} ({['Mo','Di','Mi','Do','Fr','Sa','So'][heute.weekday()]}, KW {heute.isocalendar().week})")
    user_parts.append(f"Profil: {profil}")
    user_parts.append(f"DISG-Käufertyp heute: {state.empfehle_disg_heute()}")

    fokus_override = state.get_wochen_fokus_override(heute.isocalendar().week)
    if fokus_override:
        user_parts.append(f"\n**FOKUS-OVERRIDE (Patricia gesetzt):** {fokus_override['thema']}")
        if fokus_override.get("funnel_id"):
            user_parts.append(f"Funnel: {fokus_override['funnel_id']}")

    # Launch-Status / Julia-Vorlage des Tages (höchste inhaltliche Priorität)
    launch = kontext.get("launch")
    if launch and launch.get("prompt_block"):
        user_parts.append("\n" + launch["prompt_block"])

    # Monatsplan-MD (verbindlicher Plan)
    mp = kontext.get("monatsplan_md")
    if mp:
        user_parts.append(f"\nMonats-Kontext (verbindlich, {mp.get('datei','')}):")
        if mp.get("wochen_pillar"):
            user_parts.append(f"Wochen-Pillar KW {mp.get('kw')}: {mp['wochen_pillar']}")
        if mp.get("kw_block"):
            user_parts.append(mp["kw_block"][:1200])

    if kontext.get("monatsplan"):
        m = kontext["monatsplan"]
        user_parts.append(f"\nMonatsplan {m.get('monat', '')}:")
        user_parts.append(m.get("drei_monatsziele", "")[:600])

    if kontext.get("wochenplan"):
        w = kontext["wochenplan"]
        user_parts.append(f"\nWochenplan-Fokus: {w.get('fokus_der_woche', '')[:400]}")

    # active-funnels.json wichtig
    af_text = _read_context_file("context/active-funnels.json")
    if af_text:
        user_parts.append(f"\nactive-funnels.json (gekürzt):")
        user_parts.append(af_text[:3000])

    user_parts.append("""

Erstelle jetzt die Telegram-Briefing-Anfrage. Beachte:
- Wenn ein Fokus-Override gesetzt ist: nimm DEN als Story-Thema, nicht den Notion-Wochenplan
- Schlage nur EINEN Story-Ansatz vor (nicht mehrere Optionen)
- 3-5 konkrete Fragen, die Patricia in 2-3 Min per Sprachnotiz beantworten kann
- Frage am Ende nach aktuellem Foto/Video""")

    user = "\n".join(user_parts)

    client = _get_client()
    try:
        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1500,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
    except Exception as e:
        logger.error(f"Briefing-Anfrage fehlgeschlagen: {e}")
        return {"ok": False, "error": str(e)}

    raw = response.content[0].text if response.content else ""

    # JSON extrahieren
    json_text = raw.strip()
    if json_text.startswith("```"):
        json_text = re.sub(r"^```(?:json)?\s*", "", json_text)
        json_text = re.sub(r"\s*```$", "", json_text)

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        logger.error(f"Briefing-JSON-Parse-Fehler: {e}\nRaw: {raw[:500]}")
        # Fallback: nimm den ganzen Raw-Text als Telegram-Message
        return {
            "ok": True,
            "telegram_text": raw,
            "fragen": [],
            "tokens_in": response.usage.input_tokens,
            "tokens_out": response.usage.output_tokens,
        }

    return {
        "ok": True,
        "telegram_text": data.get("telegram_text", ""),
        "fragen": data.get("fragen", []),
        "tokens_in": response.usage.input_tokens,
        "tokens_out": response.usage.output_tokens,
    }


def _extract_html(raw: str) -> str:
    """Extrahiert HTML aus Claude-Response (entfernt eventuelle Markdown-Wrapper)."""
    text = raw.strip()
    # Entferne ```html ... ``` Wrapper
    if text.startswith("```"):
        text = re.sub(r"^```(?:html)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    text = text.strip()
    if "<!DOCTYPE html>" in text or "<html" in text:
        return text
    return ""


# ========================================
# CLI-Tester
# ========================================
if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    profil = sys.argv[1] if len(sys.argv) > 1 else "mentoring"

    print(f"=== Story-Generator Test ({profil}) ===\n")

    # Notion-Kontext laden
    import notion_reader
    print("Lade Notion-Kontext...")
    kontext = notion_reader.lade_wochen_kontext()
    print(f"  Monatsplan: {'OK' if kontext.get('monatsplan') else 'FEHLT'}")
    print(f"  Wochenplan: {'OK' if kontext.get('wochenplan') else 'FEHLT'}")

    print(f"\nGeneriere Story für {profil}...")
    result = generate_story_html(profil, kontext, slug=f"test-{profil}-{datetime.now().strftime('%H%M')}")

    if result["ok"]:
        print(f"\n[OK] Story generiert: {result['slug']}")
        print(f"  HTML: {result['html_path']}")
        print(f"  Slides: {result['slide_count']}")
        print(f"  Tokens: in={result['tokens_in']}, out={result['tokens_out']}")
    else:
        print(f"\n[FEHLER] {result.get('error')}")
        sys.exit(1)
