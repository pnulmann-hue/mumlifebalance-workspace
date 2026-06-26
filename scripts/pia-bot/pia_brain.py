"""PIAs Gehirn — generiert Bio, Hooks, Struktur, Leadmagnet & roten Faden.

Pro Bootcamp-Tag eine Aufgabe (TASKS). Jede nimmt das Teilnehmerinnen-Profil und
baut einen personalisierten Output in DEREN Stimme — warm, konkret, umsetzbar.

System-Prompt = PIA-Persona + Brand-Voice-Regeln + Network-Compliance + Patricias
Voice-/Hook-Wissen (knowledge.py). User-Prompt = Profil + Tages-Aufgabe.
"""

from __future__ import annotations

import logging
from typing import Any

from anthropic import Anthropic

import config
import knowledge

logger = logging.getLogger(__name__)

_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        if not config.ANTHROPIC_API_KEY:
            raise RuntimeError("ANTHROPIC_API_KEY fehlt")
        _client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
    return _client


# ========================================
# System-Prompt — PIA-Persona + harte Regeln
# ========================================

def build_system_prompt() -> str:
    return f"""# Du bist PIA — die KI-Mentorin für Mamas im Network

Du begleitest eine Teilnehmerin durch Patricias 5-Tage-Bootcamp. Du bist die erste
KI-Mentorin SPEZIELL für Mamas im Network-Marketing, die parallel ein eigenes
Standbein aufbauen. Du sprichst warm, ermutigend und auf Augenhöhe — wie eine gute
Freundin, die sich wirklich auskennt.

## Wie du klingst (NICHT verhandelbar)
- **Freundin-Voice:** warme Du-Anrede, längere fliessende Sätze, konkrete Alltags-Anker.
  Wie am Küchentisch zu einer Freundin, nicht wie ein Coach-Lehrbuch.
- **KEINE Stakkato-Sätze.** Niemals 2-3 abgehackte Kurzsätze hintereinander
  („Du brauchst Klarheit. Du brauchst ein System. Du brauchst Umsatz."). Verbinde
  Sätze mit Konjunktionen (und, aber, weil, und da).
- **Echte Umlaute** ä/ö/ü, durchgängig Schweizer „ss" statt ß.
- **Keine KI-Floskeln** („Im heutigen schnelllebigen…", „Tauche ein in…", „In diesem
  Sinne…", „Es ist wichtig zu beachten…"). Schreib menschlich und direkt.
- **Keine erfundenen Zahlen.** Erfinde NIE Umsätze, Prozente, Followerzahlen oder
  Zeitspannen. Nutze nur, was die Teilnehmerin dir selbst gesagt hat.

## Deine Kern-Logik: Transformation, nicht Produkt
Du arbeitest IMMER transformationszentriert. Das Network-Produkt ist nur die Brücke,
nie der Star. Statt „ätherisches Öl" → „ruhiger Schlaf für deine Kinder". Statt
„Hautpflege-Set" → „du fühlst dich wieder wohl in deiner Haut". Hilf der Teilnehmerin,
ihre Transformation zu finden und in IHRER Sprache auszudrücken.

## Network-Compliance (Pflicht)
- **Keine Heilversprechen, keine medizinischen Aussagen.** Niemals „heilt", „hilft
  gegen [Krankheit]", „lindert [Symptom]". Bleib im Lifestyle-/Wohlbefinden-Frame mit
  „bei mir war"-Sprache.
- Das gilt besonders bei doTERRA, Forever & Co. — wenn die Firma der Teilnehmerin
  bekannt ist, halte ihre Compliance-Regeln ein.
- Kein Druck-Verkauf, kein „Kauf bei mir!". Verkauf passiert durch Mehrwert und Beweis.

## Output in IHRER Stimme
Was du generierst (Bio, Hooks, Captions …), soll nach der TEILNEHMERIN klingen —
nicht nach dir und nicht nach einer Werbeagentur. Persönlich, nahbar, echt.

## Format deiner Antworten
- Telegram-tauglich: kurze Absätze, gern ein paar Emojis, <b>fett</b> für Wichtiges.
- Liefere konkrete, fertige Ergebnisse zum Abtippen — keine Theorie-Vorträge.
- Am Ende immer ein warmer, ermutigender Satz + Einladung, das Ergebnis in der
  Bootcamp-Gruppe zu teilen.
- Erwähne NIEMALS, dass du auf Wissensdokumenten basierst, und nenne keine Mentoren-Namen.

# === PATRICIAS VOICE- & HOOK-WISSEN (dein Stil-Fundament) ===
{knowledge.lade_wissen()}
"""


# ========================================
# Tages-Aufgaben
# ========================================

def _profil_block(profil: dict) -> str:
    return f"""## Das Profil deiner Teilnehmerin
- Name: {profil.get('name', '(unbekannt)')}
- Network-Firma: {profil.get('firma', '(keine angegeben)')}
- Ihr Thema / ihre Transformation: {profil.get('thema', '(noch offen)')}
- Ihre Zielgruppe: {profil.get('zielgruppe', '(noch offen)')}
- Ihre Lebensphase: {profil.get('lebensphase', '(noch offen)')}
- Business-Stand: {profil.get('stand', '(noch offen)')}

Sprich sie mit ihrem Vornamen an. Beziehe dich konkret auf IHR Thema und IHRE Leute."""


TASKS: dict[str, dict[str, str]] = {
    "bio": {
        "label": "Tag 1 · Deine Bio",
        "auftrag": """# Tag 1 — Dein Thema wird klar + deine Bio

Hilf {name}, ihr Thema auf den Punkt zu bringen, und bau ihr daraus eine fertige
Instagram-Bio.

Liefere:
1. <b>Dein Thema in einem Satz</b> — die Transformation, für die sie steht (kein Produkt).
2. <b>Deine Bio (fertig zum Abtippen)</b> — 3-4 Zeilen für ihr Instagram-Profil:
   - Zeile 1: für wen sie da ist + welche Transformation
   - Zeile 2-3: was sie nahbar macht (Mama-Realität, ihre Lebensphase)
   - Zeile 4: ein klarer nächster Schritt / sanfter CTA
   Nutze sparsam passende Emojis. Klingt nach IHR, nicht nach Werbung.
3. <b>Mini-Tipp</b>: ein Satz, was sie am Bild/Highlight noch anpassen könnte.

Halte es konkret und sofort umsetzbar.""",
    },
    "hooks": {
        "label": "Tag 2 · Deine 3 Hooks",
        "auftrag": """# Tag 2 — Sichtbar werden mit 3 Hooks

Gib {name} <b>3 starke Hooks</b> für ihr Thema — die ersten Zeilen, bei denen ihre
Leserin beim Scrollen hängenbleibt und denkt „die meint ja mich".

Regeln:
- Jeder Hook ein anderes Muster (z.B. Bekenntnis, konkrete Alltags-Situation,
  ehrlicher Gegen-den-Strich-Gedanke). Variiere bewusst.
- Kein „Guten Morgen ihr Lieben", kein Stakkato. Erste Zeile muss in 2 Sekunden catchen.
- Konkret auf ihre Zielgruppe + ihr Thema zugeschnitten.

Liefere die 3 Hooks nummeriert, und schreib zu jedem in einem Halbsatz dazu, warum
er zieht. Dann: lade sie ein, einen davon heute als Post zu nutzen + in der Gruppe
zu teilen.""",
    },
    "struktur": {
        "label": "Tag 3 · Deine Zeit-Struktur",
        "auftrag": """# Tag 3 — Zeit schaffen, ohne dich zu zerreissen

{name} hat wenig Zeit (siehe Lebensphase). Bau ihr eine <b>realistische Mini-Wochen-
struktur</b> für ihr Business, die in ihren Mama-Alltag passt — keine 7 Stunden,
sondern ein paar feste, machbare Fenster.

Liefere:
1. <b>Deine Mini-Wochenstruktur</b> — pro Woche ein paar konkrete, kleine Slots
   (z.B. „Mo 20 Min: 1 Post planen", „Mi: in Stories zeigen, woran du arbeitest").
   Realistisch an ihre Lebensphase angepasst.
2. <b>Dein KI-Impuls</b> — ein konkreter erster Schritt, wie sie sich mit KI Arbeit
   abnehmen lassen kann (z.B. Captions vorschreiben, Ideen sammeln).

Ermutigend rahmen: sie muss nicht mehr arbeiten, nur klarer.""",
    },
    "leadmagnet": {
        "label": "Tag 4 · Dein Leadmagnet",
        "auftrag": """# Tag 4 — Dein erster Schritt zur eigenen Liste

Hilf {name}, ihren ersten <b>Leadmagnet</b> zu entwerfen — ein kleines kostenloses
Geschenk, das ihre Leserin gegen die Mailadresse bekommt. So wird sie unabhängiger
von der warmen Liste.

Liefere das <b>Leadmagnet-Skelett</b>:
1. <b>Titel</b> — griffig, macht neugierig, verspricht ein konkretes Ergebnis.
2. <b>Versprechen</b> — was die Leserin danach kann/hat (1-2 Sätze, Transformation).
3. <b>Format</b> — was am einfachsten zu ihr passt (z.B. 1-Seiten-PDF, kurze Checkliste,
   Mini-Video). Begründe kurz, warum dieses Format für ihren Start am leichtesten ist.

Wichtig: sie muss es heute NICHT fertig produzieren — sie soll nur wissen, was ihr
erstes Geschenk wird. Mach ihr Mut, dass das ein grosser Schritt ist.""",
    },
    "roterfaden": {
        "label": "Tag 5 · Dein roter Faden",
        "auftrag": """# Tag 5 — Dein roter Faden

Fass für {name} zusammen, was sie diese Woche gebaut hat (Thema, Bio, Hooks, Struktur,
Leadmagnet), und mach daraus EINEN klaren <b>roten Faden</b> — einen Weg, dem sie ab
jetzt folgen kann.

Liefere:
1. <b>Dein roter Faden</b> — in 3-4 Schritten, wie ihr Weg aussieht: von „sichtbar
   werden mit deinem Thema" über „Leute auf deine Liste holen" bis „in Kontakt kommen
   und begleiten". Konkret auf ihr Thema gemünzt.
2. <b>Dein nächster Schritt</b> — die EINE Sache, die sie als Nächstes tun sollte.
3. Ein warmer Abschluss-Satz, der sie stolz auf ihre Woche macht und Lust auf mehr.

Du darfst hier sanft die Brücke schlagen: Was sie diese Woche mit dir erlebt hat, ist
ein Vorgeschmack — mit Patricia und PIA an ihrer Seite kann sie genau so weitermachen.
Kein Verkaufsdruck, nur eine ehrliche Einladung.""",
    },
}

TAG_ZU_TASK = {1: "bio", 2: "hooks", 3: "struktur", 4: "leadmagnet", 5: "roterfaden"}


def generate(task_key: str, profil: dict, extra_input: str = "") -> dict[str, Any]:
    """Generiert den Output für eine Tages-Aufgabe.

    Returns: {"ok": True, "text": str, "label": str, "tokens_in": int, "tokens_out": int}
    """
    task = TASKS.get(task_key)
    if not task:
        return {"ok": False, "error": f"Unbekannte Aufgabe: {task_key}"}

    name = profil.get("name", "du")
    auftrag = task["auftrag"].format(name=name)

    user_parts = [_profil_block(profil), "\n", auftrag]
    if extra_input:
        user_parts.append(
            f"\n\n## Zusätzlicher Input von {name} (gerade geschickt)\n"
            f"Beziehe das mit ein, wenn es passt:\n„{extra_input}\""
        )
    user = "\n".join(user_parts)

    client = _get_client()
    try:
        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=2000,
            system=build_system_prompt(),
            messages=[{"role": "user", "content": user}],
        )
    except Exception as e:
        logger.error(f"PIA-Generierung ({task_key}) fehlgeschlagen: {e}")
        return {"ok": False, "error": str(e)}

    text = response.content[0].text.strip() if response.content else ""
    if not text:
        return {"ok": False, "error": "Leere Antwort"}

    return {
        "ok": True,
        "text": text,
        "label": task["label"],
        "tokens_in": getattr(response.usage, "input_tokens", 0),
        "tokens_out": getattr(response.usage, "output_tokens", 0),
    }


def freie_frage(profil: dict, frage: str) -> dict[str, Any]:
    """Beantwortet eine freie Frage der Teilnehmerin im PIA-Stil."""
    name = profil.get("name", "Die Teilnehmerin")
    user = (
        f"{_profil_block(profil)}\n\n"
        f"## {name} fragt dich gerade:\n„{frage}\"\n\n"
        f"Antworte als PIA — warm, konkret, hilfreich, auf ihr Thema bezogen. "
        f"Wenn die Frage nicht zum Bootcamp passt, lenk freundlich zurück zur "
        f"heutigen Mission."
    )
    client = _get_client()
    try:
        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1200,
            system=build_system_prompt(),
            messages=[{"role": "user", "content": user}],
        )
    except Exception as e:
        logger.error(f"PIA freie_frage fehlgeschlagen: {e}")
        return {"ok": False, "error": str(e)}
    text = response.content[0].text.strip() if response.content else ""
    return {"ok": bool(text), "text": text}
