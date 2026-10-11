"""Thema-Finder für PIA — der mehrstufige Dialog `/thema`.

Anders als die Tages-Aufgaben in `pia_brain.py` (Ein-Schuss-Generierung) ist das hier
ein GESPRÄCH über mehrere Runden. Der Zustand lebt im Profil unter `thema_dialog`.

Die Reihenfolge ist bewusst AUSSEN → INNEN:

    Runde 1  Zielgruppe schärfen      (wen willst du erreichen?)
    Runde 2  Marktrecherche           ← echte Websuche, keine erfundenen Zahlen
    Runde 3  Deine Seite              (welches Problem kennst du von innen?)
    Runde 4  Match                    (Überschneidung = ihr Thema)
    Runde 5  Prüfen + Experten-Satz

Warum nicht innen anfangen: Wer bei sich selbst startet, verliebt sich in ein Thema
und sucht danach nur noch Bestätigung. Wer bei den echten Problemen startet, sieht
erst mal, was überhaupt da ist.

Runde 2 nutzt das server-seitige Websuche-Tool. Das ist der Kern-Unterschied zu einer
Prompt-Vorlage, die man in ein KI-Fenster kopiert: dort erfindet die KI Statistiken
samt plausibel aussehender Quellen, und die Teilnehmerin merkt es nicht.
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


# Server-seitiges Websuche-Tool (Runde 2). Läuft auf Anthropics Infrastruktur,
# kein eigener Loop nötig — die Ergebnisse kommen als Content-Blöcke zurück.
WEB_SEARCH_TOOL = {
    "type": "web_search_20260209",
    "name": "web_search",
    "max_uses": 6,
}


# ========================================
# System-Prompt — erbt PIAs Persona, ergänzt die Thema-Regeln
# ========================================

THEMA_REGELN = """
# Deine Zusatz-Regeln für den Thema-Dialog

## Du führst ein Gespräch, kein Formular
Stell EINE Frage pro Runde. Wenn ihre Antwort zu vage ist („irgendwas mit Gesundheit",
„Frauen halt"), hak einmal freundlich nach, statt weiterzumachen. Eine unscharfe
Zielgruppe in Runde 1 macht die ganze Recherche in Runde 2 wertlos.

## Zielgruppen-Ebenen auseinanderhalten (wichtig!)
Die Kundinnen deiner Teilnehmerin sind NICHT automatisch Mamas oder Frauen. Wenn sie
Tiernahrung vertreibt, sind es Hundebesitzer. Wenn sie Werkzeug vertreibt, vielleicht
Handwerker. Frag nach, statt zu unterstellen — und sprich dann von „Menschen" oder
„Interessenten", solange du es nicht sicher weisst.

## Niemals erfundene Zahlen
Wenn du eine Zahl oder Statistik nennst, muss sie aus deiner Websuche stammen und mit
Quelle belegt sein. Findest du nichts Belastbares, sag das offen — eine ehrliche Lücke
ist besser als eine schöne erfundene Prozentzahl, die sie später öffentlich postet.

## Das Produkt bleibt draussen
Es geht um das Problem der Menschen, nicht um das Produkt der Firma. Wenn die
Teilnehmerin in Produktsprache antwortet („die brauchen mein Kollagen"), führ sie
zurück zum Alltag: Was merkt die Person morgens, wenn sie aufwacht?
"""


def build_system_prompt() -> str:
    """PIAs Persona (aus pia_brain) + die Thema-Regeln."""
    import pia_brain  # spät importieren, um Zirkelbezug zu vermeiden

    return pia_brain.build_system_prompt() + "\n\n" + THEMA_REGELN


# ========================================
# Die Runden
# ========================================

RUNDEN: dict[int, dict[str, Any]] = {
    1: {
        "label": "Runde 1 · Wen willst du erreichen?",
        "websuche": False,
        "auftrag": """# Runde 1 — Zielgruppe schärfen

Begrüsse {name} kurz und warm, erklär ihr in zwei Sätzen, was in den nächsten Runden
passiert (erst schauen wir, was ihre Leute wirklich beschäftigt, dann was sie selber
dazu beitragen kann).

Dann stell ihr die EINE Frage: Wen will sie eigentlich erreichen?

Gib ihr zwei, drei Beispiele mit, wie eine brauchbare Antwort aussieht — konkret genug,
dass man danach suchen könnte. „Frauen zwischen 30 und 50" ist zu breit. „Mütter mit
Kindern im Kindergartenalter, die abends nicht mehr abschalten können" ist gut.

Falls in ihrem Profil schon eine Zielgruppe steht, greif die auf und frag, ob das noch
stimmt oder ob sie es schärfen will.

Halte es kurz. Sie soll antworten, nicht lesen.""",
    },
    2: {
        "label": "Runde 2 · Was drückt die wirklich?",
        "websuche": True,
        "auftrag": """# Runde 2 — Marktrecherche

{name} hat dir ihre Zielgruppe beschrieben:
„{antwort_1}"

<b>Recherchiere jetzt im Netz</b>, welche konkreten Alltagsprobleme diese Menschen
wirklich haben. Such in Foren, Communities, Ratgeberseiten, Studien — dort, wo diese
Menschen selber schreiben. Deutschsprachiger Raum bevorzugt.

Liefere ihr <b>5 bis 7 konkrete Probleme</b>, und pro Problem:
- <b>Die Szene:</b> Wie sieht das im Alltag aus? Ein Moment, kein Oberbegriff.
  Nicht „Schlafprobleme", sondern „sie liegt um halb drei wach und rechnet aus, wie
  viele Stunden noch bleiben".
- <b>Was es kostet:</b> Was macht das mit ihr, ihrer Beziehung, ihrem Tag?
- <b>Beleg:</b> Woher weisst du das? Studie, Forendiskussion, Artikel — mit Quelle.
  Wenn du zu einem Problem nichts Belastbares findest, schreib „nur Beobachtung,
  nicht belegt" dazu. Erfinde nichts.

Geh in die Tiefe. Oberflächliche Probleme kennt sie selber schon — such das, was
darunter liegt und was niemand laut sagt.

Am Ende: Sag ihr, dass sie sich das in Ruhe durchlesen soll, und dass es in der
nächsten Runde darum geht, welches davon sie selber von innen kennt.""",
    },
    3: {
        "label": "Runde 3 · Was kennst du davon von innen?",
        "websuche": False,
        "auftrag": """# Runde 3 — Ihre Seite

{name} hat die Problemliste aus Runde 2 gesehen. Jetzt kommt ihre Seite.

Frag sie nach den <b>vier Quellen</b>, aber als Gespräch, nicht als Fragebogen —
und beziehe dich dabei konkret auf die Probleme aus Runde 2:

1. <b>Erfahrung</b> — Welches dieser Probleme hat sie selber durchgemacht?
2. <b>Ergebnisse</b> — Was hat sich bei ihr verändert? Es muss nichts Spektakuläres
   sein. Eine Routine, die hält. Ein Abend, der anders läuft als früher.
3. <b>Perspektive</b> — Wo sieht sie etwas anders als alle anderen, die darüber reden?
4. <b>Fragen von früher</b> — Was hat sie sich vor zwei Jahren gefragt, das ihre Leute
   sich heute fragen?

Stell die vier nicht als nummerierte Liste ab, sondern führ sie durch. Sag ihr, sie
darf auch per Sprachnotiz antworten und muss nicht zu allen vier etwas haben.

Der Satz, auf den es hinausläuft: Sie muss das Problem nicht gelöst haben — sie muss
es kennen und einen Schritt weiter sein als die, der sie hilft.""",
    },
    4: {
        "label": "Runde 4 · Dein Thema",
        "websuche": False,
        "auftrag": """# Runde 4 — Der Match

Jetzt legst du beide Seiten übereinander: die recherchierten Probleme aus Runde 2 und
das, was {name} in Runde 3 von sich erzählt hat.

Hier ist ihre Antwort aus Runde 3:
„{antwort_3}"

Liefere <b>2 bis 3 Themen-Kandidaten</b>. Pro Kandidat:
- <b>Das Thema</b> in einem Satz, aus Sicht der Menschen formuliert, denen sie hilft
- <b>Warum ausgerechnet sie</b> — welche ihrer vier Quellen das trägt
- <b>Der Beleg</b> — welches recherchierte Problem aus Runde 2 dahinterliegt
- <b>Ehrlich:</b> Was an diesem Kandidaten noch dünn ist

Sortiere sie: der stärkste zuerst. Und sag dazu, was ihn stark macht.

Frag am Ende, welcher sich für sie am richtigsten anfühlt — ihr Bauchgefühl zählt hier
genauso wie die Recherche, weil sie mit dem Thema jahrelang leben muss.""",
    },
    5: {
        "label": "Runde 5 · Prüfen + dein Satz",
        "websuche": True,
        "auftrag": """# Runde 5 — Qualifizieren und festzurren

{name} hat sich für einen Kandidaten entschieden:
„{antwort_4}"

<b>Erst prüfen.</b> Recherchiere kurz und sag ihr ehrlich, was du findest:
- Reden Menschen im Netz über dieses Thema, oder ist es still?
- Gibt es schon Angebote dazu? (Konkurrenz ist ein gutes Zeichen, kein schlechtes —
  sie beweist, dass jemand dafür zahlt.)
- Ist es ein Dauerthema oder eine Modewelle?

<b>Dann die zwei Fragen, die keine Recherche beantwortet:</b>
- Kann sie über dieses Thema in zwei Jahren noch reden, ohne sich zu langweilen?
- Können die Menschen, denen sie hilft, für eine Lösung Geld ausgeben?

<b>Zum Schluss ihr Satz</b>, in drei Varianten zur Auswahl:
„Ich helfe [wem] dabei [was zu verändern], damit [welches Ergebnis]."

Schreib alle drei so, dass sie ihn morgen in ihre Bio setzen könnte. Kein
Marketing-Sprech, ihre Sprache.

Dann sag ihr, dass sie mit /hooks direkt weitermachen kann — die ersten Zeilen für
ihre Posts bauen dann auf genau diesem Satz auf.""",
    },
}

LETZTE_RUNDE = max(RUNDEN)


# ========================================
# Dialog-State
# ========================================

def start_dialog(profil: dict) -> dict[str, Any]:
    """Frischer Dialog-Zustand (kommt ins Profil unter `thema_dialog`)."""
    return {"runde": 1, "antworten": {}, "fertig": False}


def antwort_speichern(dialog: dict, runde: int, antwort: str) -> dict:
    dialog.setdefault("antworten", {})[str(runde)] = antwort
    return dialog


def _auftrag_fuellen(runde: int, profil: dict, dialog: dict) -> str:
    """Setzt Name und die bisherigen Antworten in den Runden-Auftrag ein."""
    antworten = dialog.get("antworten", {})
    return RUNDEN[runde]["auftrag"].format(
        name=profil.get("name", "du"),
        antwort_1=antworten.get("1", "(noch offen)"),
        antwort_3=antworten.get("3", "(noch offen)"),
        antwort_4=antworten.get("4", "(noch offen)"),
    )


def _verlauf_block(dialog: dict) -> str:
    """Kompakter Rückblick, damit PIA den Gesprächsfaden behält."""
    antworten = dialog.get("antworten", {})
    if not antworten:
        return ""
    zeilen = ["## Was sie dir bisher gesagt hat"]
    for nr in sorted(antworten, key=int):
        label = RUNDEN[int(nr)]["label"]
        zeilen.append(f"- {label}: „{antworten[nr]}\"")
    return "\n".join(zeilen)


# ========================================
# Ausführung
# ========================================

def runde_ausfuehren(runde: int, profil: dict, dialog: dict) -> dict[str, Any]:
    """Generiert die Ausgabe für eine Runde.

    Returns: {"ok": True, "text": str, "label": str, "quellen": list[str],
              "letzte_runde": bool}
    """
    if runde not in RUNDEN:
        return {"ok": False, "error": f"Unbekannte Runde: {runde}"}

    import pia_brain

    spec = RUNDEN[runde]
    user_parts = [pia_brain._profil_block(profil)]
    verlauf = _verlauf_block(dialog)
    if verlauf:
        user_parts.append(verlauf)
    user_parts.append(_auftrag_fuellen(runde, profil, dialog))

    kwargs: dict[str, Any] = {
        "model": config.CLAUDE_MODEL,
        "max_tokens": 16000,
        "system": build_system_prompt(),
        "messages": [{"role": "user", "content": "\n\n".join(user_parts)}],
        # Opus 4.8 denkt nur, wenn man es explizit einschaltet.
        "thinking": {"type": "adaptive"},
    }
    if spec["websuche"]:
        kwargs["tools"] = [WEB_SEARCH_TOOL]

    client = _get_client()
    try:
        response = client.messages.create(**kwargs)
    except Exception as e:
        logger.error(f"Thema-Runde {runde} fehlgeschlagen: {e}")
        return {"ok": False, "error": str(e)}

    text = "\n".join(
        b.text for b in response.content if getattr(b, "type", "") == "text"
    ).strip()
    if not text:
        return {"ok": False, "error": "Leere Antwort"}

    return {
        "ok": True,
        "text": text,
        "label": spec["label"],
        "quellen": _quellen_sammeln(response),
        "letzte_runde": runde >= LETZTE_RUNDE,
        "tokens_out": getattr(response.usage, "output_tokens", 0),
    }


def _quellen_sammeln(response) -> list[str]:
    """Zieht die URLs aus den Websuche-Ergebnissen — fürs Logging und zum Nachprüfen.

    Achtung: Fehler der Websuche kommen als HTTP 200 zurück. Bei Erfolg ist `.content`
    eine Liste von Treffern, im Fehlerfall ein einzelnes Fehler-Objekt — deshalb wird
    hier auf den Typ geprüft, statt blind zu iterieren.
    """
    urls: list[str] = []
    for block in response.content:
        if getattr(block, "type", "") != "web_search_tool_result":
            continue
        inhalt = getattr(block, "content", None)
        if not isinstance(inhalt, list):
            fehler = getattr(inhalt, "error_code", None)
            if fehler:
                logger.warning(f"Websuche meldet Fehler: {fehler}")
            continue
        for treffer in inhalt:
            url = getattr(treffer, "url", None)
            if url and url not in urls:
                urls.append(url)
    return urls
