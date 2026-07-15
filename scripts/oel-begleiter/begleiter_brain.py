"""Das Gehirn des Öl-Begleiters — generiert die 7 Tages-Etappen.

Jede Etappe nimmt das Testerinnen-Profil + das ECHTE Companion-Kundenwissen (aus
companion_kb.py / Supabase) und baut eine warme, konkrete Etappe in Patricias Stimme.
Der 7-Tage-Bogen führt von „richtig testen“ über die einzelnen Öl-Momente bis zur
sanften Brücke zur eigenen kleinen Hausapotheke.

System-Prompt = Begleiter-Persona + Brand-Voice + doTERRA-Compliance + Voice-Wissen.
User-Prompt  = Profil + Companion-Kundenwissen zu IHREN Ölen + Tages-Auftrag.

HARTE REGEL: Öl-spezifische Aussagen NUR aus dem mitgelieferten Companion-Wissen.
Steht dort nichts zu einem Öl, bleibt der Bot bei neutraler Sinnes-/Ritual-Sprache
und verweist auf Patricia / den Companion — er erfindet NIE Wirkungen.
"""

from __future__ import annotations

import logging
from typing import Any

from anthropic import Anthropic

import companion_kb
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
# System-Prompt — Persona + harte Regeln
# ========================================

def build_system_prompt() -> str:
    return f"""# Du bist der Öl-Begleiter von Patricia (Mum Life Balance)

Du begleitest eine Frau, die von Patricia ätherische Öl-Pröbchen (Samples) bekommen
hat, 7 Tage lang durchs Ausprobieren. Jeden Tag eine kleine, machbare Etappe — kein
Kurs, kein Druck, sondern eine warme Freundin, die ihr zeigt, wie sie ihre Öle
entdecken kann. Ziel: Sie *erlebt* die Öle im Alltag, fühlt sich begleitet und findet
am Ende ihre eigene kleine Routine.

## Wie du klingst (NICHT verhandelbar)
- **Freundin-Voice:** warme Du-Anrede, fliessende Sätze, konkrete Alltags-Anker (Mama-
  Realität: Kinder, Küche, Abend auf dem Sofa). Wie am Küchentisch, nicht wie ein Flyer.
- **KEINE Stakkato-Sätze.** Nie 2-3 abgehackte Kurzsätze hintereinander. Verbinde mit
  und/aber/weil/und da.
- **Echte Umlaute** ä/ö/ü, durchgängig Schweizer „ss“ statt ß.
- **Keine KI-Floskeln** („Tauche ein in…“, „In der heutigen schnelllebigen Zeit…“,
  „Es ist wichtig zu beachten…“). Menschlich und direkt.
- **Keine erfundenen Zahlen.** Erfinde NIE Prozente, Studien-Zahlen, „X% der Frauen…“.

## Öl-Wissen: NUR aus dem Companion (streng)
- Für alles Öl-Spezifische (was ein Öl macht, wofür man es nutzt) verwendest du
  AUSSCHLIESSLICH das mitgelieferte „Companion-Kundenwissen“ im User-Prompt. Das ist
  genau das Wissen, auf das Patricias Kundinnen Zugriff haben.
- Steht dort zu einem Öl NICHTS, dann erfinde nichts. Bleib bei dem, was sie selbst
  sinnlich erleben kann (riechen, ins Ritual einbauen, wie es sich anfühlt) und sag
  ehrlich, dass sie mehr Details bei Patricia / im Companion findet.
- Nenne doTERRA-Ölnamen korrekt (z.B. „Air“ statt „Breathe“, „On Guard“, „Deep Blue“,
  „Adaptiv“).

## doTERRA-Compliance (Pflicht)
- **Keine Heilversprechen, keine medizinischen Aussagen.** Niemals „heilt“, „hilft
  gegen [Krankheit]“, „lindert [Symptom]“. Nutze „kann unterstützen“, „trägt bei zu“,
  „bei mir war“, „viele empfinden“. Bleib in der Lifestyle-/Wohlfühl-Bubble.
- **Sicherheit ist Fürsorge, kein Heilversprechen** — die darfst du sagen: Öle vor
  Hautkontakt verdünnen (mit einem Pflanzenöl), nicht in die Augen, bei Zitrusölen nach
  dem Auftragen die pralle Sonne meiden, bei Schwangerschaft/kleinen Kindern/Haustieren
  vorsichtig sein und im Zweifel Patricia fragen. Immer kurz + beiläufig, nie
  angsteinflössend.
- Kein Druck-Verkauf. Der Verkauf am Ende ist eine ehrliche Einladung, kein „Kauf!“.

## Format deiner Etappen
- Telegram-tauglich: kurze Absätze, ein paar passende Emojis, <b>fett</b> für Wichtiges.
- Immer mit dabei: ein <b>konkreter kleiner Schritt für heute</b> (1 Anwendung, machbar
  in 2 Minuten) und eine leise Einladung, kurz zu <b>beobachten/zurückzumelden</b>, wie
  es war.
- Warm eröffnen, warm schliessen. Erwähne NIE, dass du auf Dokumenten/Wissensbasen
  basierst, und nenne keine Mentoren-Namen.

# === PATRICIAS VOICE- & COMPLIANCE-WISSEN (dein Stil-Fundament) ===
{knowledge.lade_wissen()}
"""


# ========================================
# Der 7-Tage-Bogen
# ========================================

def _profil_block(profil: dict) -> str:
    return f"""## Das Profil deiner Testerin
- Name: {profil.get('name', '(unbekannt)')}
- Ihre Pröbchen: {profil.get('samples', '(nicht angegeben)')}
- Ihr grösster Wunsch gerade: {profil.get('wunsch', '(offen)')}
- Ihr Alltag: {profil.get('alltag', '(offen)')}
- Öl-Erfahrung: {profil.get('erfahrung', '(offen)')}

Sprich sie mit ihrem Vornamen an. Beziehe dich konkret auf IHRE Öle und IHREN Wunsch.
Wähle für heute ein Öl aus IHREM Set, das zum Tages-Thema passt."""


TAGE: dict[int, dict[str, str]] = {
    1: {
        "label": "Tag 1 · Ankommen & richtig testen",
        "auftrag": """# Tag 1 — Ankommen und dein erstes Öl bewusst erleben

Heiss {name} herzlich willkommen und nimm ihr die Unsicherheit: Öle testen ist
einfach, sie kann nichts falsch machen. Erklär ihr kurz und locker, wie man ein Öl
überhaupt kennenlernt:
- am Fläschchen riechen (Deckel auf, kurz dran riechen — der erste Eindruck zählt)
- ein Tropfen auf die Handinnenfläche, verreiben, die Hände zum Gesicht und tief atmen
- oder ein paar Tropfen in einen Diffuser, wenn sie einen hat
- Sicherheit beiläufig: vor Hautkontakt mit einem Pflanzenöl verdünnen, nicht in die
  Augen, bei Zitrusölen danach nicht in die pralle Sonne.

Dann: Such EIN einfaches Öl aus ihrem Set als heutigen Einstieg (z.B. ein Zitrusöl oder
Lavendel, je nach dem, was sie hat) und gib ihr EINEN kleinen, konkreten Schritt für
heute. Lade sie ein, kurz zurückzuschreiben, wie der erste Duft für sie war.""",
    },
    2: {
        "label": "Tag 2 · Frische & Energie am Morgen",
        "auftrag": """# Tag 2 — Ein frischer Start in den Tag

Heute geht's um den Morgen. Wähl aus {name}s Set ein Öl, das zu Frische/Energie passt
(z.B. ein Zitrusöl oder Pfefferminz — nur wenn sie es hat). Zeig ihr eine kleine
Morgen-Anwendung, die in ihren echten Mama-Alltag passt (Diffuser beim Frühstück, ein
Tropfen in die Handfläche vor dem Loslegen, in die Dusche).

Nutze für die Öl-Aussagen nur das Companion-Wissen unten. Ein kleiner Schritt für
heute + Einladung zum Beobachten, wie sich ihr Vormittag anfühlt.""",
    },
    3: {
        "label": "Tag 3 · Fokus im Alltags-Chaos",
        "auftrag": """# Tag 3 — Ein Moment Klarheit mitten im Trubel

Mama-Alltag ist voll. Zeig {name} heute ein Öl aus ihrem Set für einen kurzen Fokus-/
Klarheits-Moment (z.B. Pfefferminz oder ein Zitrusöl, je nach Set) — für den Schreib-
tisch, zwischen zwei To-dos, im Auto. Kleine Anwendung, die 2 Minuten braucht.

Öl-Aussagen nur aus dem Companion-Wissen. Schritt für heute + leise Rückmelde-Frage.""",
    },
    4: {
        "label": "Tag 4 · Ruhe & Runterkommen am Abend",
        "auftrag": """# Tag 4 — Abends bewusst runterfahren

Der wichtigste Moment für viele Mamas: der Übergang in den Feierabend. Wähl aus {name}s
Set ein Öl, das zu Ruhe/Entspannung passt (z.B. Lavendel, Balance, Serenity oder
Adaptiv — nur was sie hat) und bau ihr ein kleines Abend-Ritual: 30 Min vorm Bett Handy
weg, Öl in die Bodylotion oder in den Diffuser, kurz durchatmen.

Öl-Aussagen nur aus dem Companion-Wissen, alles im „bei mir war“-Frame. Schritt für
heute + Einladung, morgen früh zu schauen, wie sie geschlafen hat.""",
    },
    5: {
        "label": "Tag 5 · Ein Wohlfühl-Moment nur für dich",
        "auftrag": """# Tag 5 — Fünf Minuten, die nur dir gehören

Heute keine Funktion, sondern Selfcare. Zeig {name}, wie sie mit einem Öl aus ihrem Set
einen kleinen Wohlfühl-Moment schafft — ein Tropfen in die Bodylotion nach der Dusche,
ein Fussbad, oder einfach kurz die Hände vors Gesicht und dreimal tief atmen. Verknüpf
es mit ihrem Wunsch von der Anmeldung.

Warm und persönlich. Öl-Aussagen nur aus dem Companion-Wissen. Kleiner Schritt für
heute + Einladung, sich diesen Moment wirklich zu gönnen.""",
    },
    6: {
        "label": "Tag 6 · Öle im Familien-Alltag",
        "auftrag": """# Tag 6 — Deine Öle im ganz normalen Familien-Alltag

Zeig {name} heute, wie Öle in den Familien-Alltag passen: ein Diffuser-Duft fürs
Wohnzimmer, ein frischer Raumduft, ein Öl beim Aufräumen/Putzen (z.B. Zitrone). Wenn in
ihrem Set etwas dabei ist, das sich mit Kindern nutzen lässt, erwähne die Vorsicht
(stärker verdünnen, sparsam, im Zweifel Patricia fragen).

Öl-Aussagen nur aus dem Companion-Wissen. Ein kleiner Schritt für heute + Rückmelde-
Frage, welcher Moment ihr am meisten gefallen hat.""",
    },
    7: {
        "label": "Tag 7 · Deine Mini-Routine + Rückblick",
        "auftrag": """# Tag 7 — Dein Rückblick und deine kleine Routine

Letzte Etappe. Fass für {name} liebevoll zusammen, was sie diese Woche ausprobiert hat,
und bau ihr aus IHREN Ölen + IHREM Wunsch eine <b>ganz kleine Alltags-Routine</b> (2-3
feste Öl-Momente: z.B. morgens Frische, abends Ruhe, ein Wohlfühl-Moment). So machbar,
dass sie sie wirklich lebt.

Dann schlag die Brücke — ehrlich und ohne Druck: Diese Woche war ein Vorgeschmack, und
wenn sie mag, kann sie sich ihre eigene kleine Hausapotheke aufbauen, damit die Öle
nicht ausgehen. Lade sie ein: „{kontakt}.“ Kein „Kauf!“, nur eine warme Einladung, und
mach sie stolz auf ihre Woche.

Öl-Aussagen nur aus dem Companion-Wissen.""",
    },
}

GESAMT_TAGE = 7


def generate_day(day_num: int, profil: dict, extra_input: str = "") -> dict[str, Any]:
    """Generiert die Etappe für einen Tag (1..7).

    Returns: {"ok": True, "text": str, "label": str, "tokens_in": int, "tokens_out": int}
    """
    tag = TAGE.get(day_num)
    if not tag:
        return {"ok": False, "error": f"Unbekannter Tag: {day_num}"}

    name = profil.get("name", "du")
    auftrag = tag["auftrag"].format(name=name, kontakt=config.PATRICIA_KONTAKT)

    # Echtes Companion-Kundenwissen zu IHREN Ölen holen (Supabase, category=product).
    kundenwissen = companion_kb.hole_kundenwissen(
        profil.get("samples", ""), profil.get("wunsch", "")
    )
    if kundenwissen:
        wissen_block = (
            "## Companion-Kundenwissen zu IHREN Ölen "
            "(NUR das hier für Öl-Aussagen verwenden — nichts dazu erfinden):\n"
            + kundenwissen
        )
    else:
        wissen_block = (
            "## Companion-Kundenwissen: aktuell nicht verfügbar.\n"
            "Mach KEINE konkreten Wirkungs-Aussagen zu einzelnen Ölen. Bleib bei dem, was "
            "sie sinnlich erleben kann (riechen, ins Ritual einbauen, wie es sich anfühlt) "
            "und verweise für Details freundlich auf Patricia."
        )

    user_parts = [_profil_block(profil), "\n", wissen_block, "\n", auftrag]
    if extra_input:
        user_parts.append(
            f"\n\n## Zusätzlicher Input von {name} (gerade geschickt)\n"
            f"Beziehe das mit ein, wenn es passt:\n„{extra_input}“"
        )
    user = "\n".join(user_parts)

    client = _get_client()
    try:
        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1600,
            system=build_system_prompt(),
            messages=[{"role": "user", "content": user}],
        )
    except Exception as e:
        logger.error(f"Etappe {day_num} fehlgeschlagen: {e}")
        return {"ok": False, "error": str(e)}

    text = response.content[0].text.strip() if response.content else ""
    if not text:
        return {"ok": False, "error": "Leere Antwort"}

    return {
        "ok": True,
        "text": text,
        "label": tag["label"],
        "tokens_in": getattr(response.usage, "input_tokens", 0),
        "tokens_out": getattr(response.usage, "output_tokens", 0),
    }


def freie_frage(profil: dict, frage: str) -> dict[str, Any]:
    """Beantwortet eine freie Frage der Testerin im Begleiter-Stil.

    Auch hier: Öl-Aussagen nur aus dem Companion-Wissen zu ihren Ölen.
    """
    name = profil.get("name", "Die Testerin")
    kundenwissen = companion_kb.hole_kundenwissen(
        profil.get("samples", ""), frage or profil.get("wunsch", "")
    )
    wissen_block = (
        "## Companion-Kundenwissen zu ihren Ölen (nur das für Öl-Aussagen nutzen):\n"
        + kundenwissen
        if kundenwissen
        else "## Companion-Kundenwissen: nicht verfügbar — mach keine erfundenen Öl-Aussagen."
    )
    user = (
        f"{_profil_block(profil)}\n\n{wissen_block}\n\n"
        f"## {name} fragt dich gerade:\n„{frage}“\n\n"
        f"Antworte als ihr Öl-Begleiter — warm, konkret, hilfreich, auf ihre Öle + ihren "
        f"Wunsch bezogen. Öl-Aussagen nur aus dem Companion-Wissen; steht dort nichts, sag "
        f"es ehrlich und verweise auf Patricia. Halte die doTERRA-Compliance ein."
    )
    client = _get_client()
    try:
        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1000,
            system=build_system_prompt(),
            messages=[{"role": "user", "content": user}],
        )
    except Exception as e:
        logger.error(f"freie_frage fehlgeschlagen: {e}")
        return {"ok": False, "error": str(e)}
    text = response.content[0].text.strip() if response.content else ""
    return {"ok": bool(text), "text": text}
