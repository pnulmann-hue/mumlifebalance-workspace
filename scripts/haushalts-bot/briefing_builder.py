"""Vorabend-Briefing fuer den Haushalts-Bot.

Baut aus den Haushalts-Liste-Eintraegen eine kurze Telegram-Nachricht, die
am Abend (19:00) kommt und den NAECHSTEN Tag ankuendigt — Vorabend-Logik,
damit Schule + Termine rechtzeitig gepackt/vorbereitet sind.

Regeln (aus dem Bot-System-Prompt):
- Wiederkehrend morgen: taeglich + (jeden 2. Tag) + woechentlich mit Wochentag = morgen
- Woechentlich ohne festen Tag: 1x/Woche anstossen (am So-Abend = Wochenstart Mo)
- Monatlich: nur wenn morgen der 1. ist
- Datierte Termine: Fixes Datum morgen bis +3 Tage
- Geburtstage: 10-14 Tage vor dem Datum an Geschenk erinnern, am Tag ans Gratulieren
- Schule: Vorabend — Eintraege fuer morgen, immer mit Vorname
- Pinned: ueberfaellige einmalige Termine bleiben ganz oben bis erledigt
- Wer: Kinder -> "erinnere die Kinder", Mann -> "Mann:", Patricia -> deine Aufgabe
- Erledigte (Erledigt=ja) werden nie genannt
"""

from __future__ import annotations

import re
from datetime import date, timedelta

import config

WOCHENTAG_KEY = {0: "Mo", 1: "Di", 2: "Mi", 3: "Do", 4: "Fr", 5: "Sa", 6: "So"}
WOCHENTAG_LANG = {
    "Mo": "Montag", "Di": "Dienstag", "Mi": "Mittwoch", "Do": "Donnerstag",
    "Fr": "Freitag", "Sa": "Samstag", "So": "Sonntag",
}
MONATE = {
    1: "Januar", 2: "Februar", 3: "März", 4: "April", 5: "Mai", 6: "Juni",
    7: "Juli", 8: "August", 9: "September", 10: "Oktober", 11: "November",
    12: "Dezember",
}


def _parse_datum(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return date.fromisoformat(s[:10])
    except (ValueError, TypeError):
        return None


def _tage_bis_jahrestag(d: date, ab: date) -> int:
    """Tage bis zum naechsten Vorkommen von Tag/Monat von d, ab Datum 'ab'."""
    try:
        naechster = d.replace(year=ab.year)
    except ValueError:
        naechster = d.replace(year=ab.year, day=28)
    if naechster < ab:
        try:
            naechster = d.replace(year=ab.year + 1)
        except ValueError:
            naechster = d.replace(year=ab.year + 1, day=28)
    return (naechster - ab).days


_WD_RE = re.compile(r"\b(Mo|Di|Mi|Do|Fr|Sa|So)\b")


def _wochentage_aus_notiz(notiz: str) -> set[str]:
    """Liest Wochentag-Kuerzel aus einer Notiz (z.B. 'Mo / Mi / Fr')."""
    if not notiz:
        return set()
    return set(_WD_RE.findall(notiz))


def _wer_prefix(wer: str | None, text: str) -> str:
    """Formatiert eine Zeile je nach Zustaendigkeit."""
    if wer == "Kinder":
        return f"erinnere die Kinder: {text}"
    if wer == "Mann":
        return f"Mann: {text}"
    return text


def baue_vorabend_briefing(eintraege: list[dict], heute: date | None = None) -> str:
    """Baut die Vorabend-Nachricht fuer morgen."""
    if heute is None:
        heute = date.today()
    morgen = heute + timedelta(days=1)
    morgen_key = WOCHENTAG_KEY[morgen.weekday()]
    morgen_lang = WOCHENTAG_LANG[morgen_key]

    offen = [e for e in eintraege if not e["erledigt"]]

    pinned: list[str] = []
    haushalt: list[str] = []
    familie: list[str] = []
    schule: list[str] = []
    aemtli: list[str] = []
    slot: list[str] = []

    for e in offen:
        bereich = e["bereich"]
        rhythmus = e["rhythmus"]
        wochentag = e["wochentag"]
        notiz = (e["notiz"] or "").strip()
        aufgabe = e["aufgabe"]
        wer = e["wer"]
        d = _parse_datum(e["fixes_datum"])
        notiz_low = notiz.lower()

        zeile = aufgabe
        if notiz:
            zeile = f"{aufgabe} — {notiz}"

        # ---- 1. PINNED: ueberfaellige einmalige Termine (bis erledigt) ----
        ueberfaellig = (
            rhythmus == "einmalig"
            and (
                ("überfällig" in notiz_low or "ueberfaellig" in notiz_low
                 or "jetzt" in notiz_low)
                or (d is not None and d <= heute)
            )
        )
        if ueberfaellig:
            pinned.append(_wer_prefix(wer, zeile))
            continue

        # ---- 2. SCHULE (Vorabend fuer morgen) ----
        if bereich == "Schule":
            faellig_morgen = (wochentag == morgen_key) or (d == morgen)
            if faellig_morgen:
                schule.append(zeile)
            continue

        # ---- 3. GEBURTSTAG (Geschenk-Vorlauf / Tag selbst) ----
        if bereich == "Geburtstag" and d is not None:
            tage = _tage_bis_jahrestag(d, morgen)
            if tage == 0:
                familie.append(f"🎂 {aufgabe} — morgen ist der Tag, ans Gratulieren denken")
            elif config.GEBURTSTAG_VORLAUF_MIN <= tage <= config.GEBURTSTAG_VORLAUF_MAX:
                familie.append(f"🎁 {aufgabe} — in {tage} Tagen, jetzt Geschenk besorgen")
            continue

        # ---- 4. DATIERTE TERMINE (morgen bis +Lookahead) ----
        if d is not None:
            delta = (d - morgen).days
            if 0 <= delta <= config.TERMIN_LOOKAHEAD_TAGE:
                wann = "morgen" if delta == 0 else f"in {delta + 1} Tagen ({d.strftime('%d.%m.')})"
                familie.append(_wer_prefix(wer, f"{zeile} ({wann})"))
            continue

        # ---- 5. WIEDERKEHREND ----
        ziel = haushalt
        if bereich == "Kinder-Ämtli":
            ziel = aemtli
        elif bereich == "Selbst/Me-Time":
            ziel = slot
        elif bereich == "Familie/Termin":
            ziel = familie

        if rhythmus == "täglich":
            ziel.append(_wer_prefix(wer, zeile))
        elif rhythmus == "jeden 2. Tag":
            ziel.append(_wer_prefix(wer, f"{aufgabe} (jeden 2. Tag — schau ob morgen dran)"))
        elif rhythmus == "wöchentlich":
            if wochentag and wochentag != "–":
                if wochentag == morgen_key:
                    ziel.append(_wer_prefix(wer, zeile))
            else:
                # kein festes Wochentag-Feld: erst Notiz nach Tagen absuchen
                # (z.B. Krafttraining "Mo / Mi / Fr"), sonst 1x/Woche zum
                # Wochenstart (morgen = Montag) anstossen.
                tage_notiz = _wochentage_aus_notiz(notiz)
                if tage_notiz:
                    if morgen_key in tage_notiz:
                        ziel.append(_wer_prefix(wer, zeile))
                elif morgen_key == "Mo":
                    ziel.append(_wer_prefix(wer, f"{aufgabe} (diese Woche dran)"))
        elif rhythmus == "monatlich":
            if morgen.day == 1:
                ziel.append(_wer_prefix(wer, f"{aufgabe} (diesen Monat dran)"))
        # alle 3 Monate / 2x-3x/Jahr / jaehrlich / saisonal / nach Bedarf:
        # bewusst NICHT im taeglichen Push (sonst Dauer-Nagging) — kommen ueber
        # die datierten Termine bzw. werden manuell angestossen.

    # ---- Nachricht zusammenbauen ----
    lines: list[str] = []
    lines.append(f"🌙 Vorabend — morgen ist {morgen_lang}, {morgen.day}. {MONATE[morgen.month]}")
    lines.append("")

    if pinned:
        lines.append("📌 Dranbleiben (bis erledigt):")
        for x in pinned:
            lines.append(f"   ⚠️ {x}")
        lines.append("")

    bloecke = [
        ("🏠 Haushalt", haushalt),
        ("👨‍👩‍👧 Familie / Termine", familie),
        ("🎒 Schule (für morgen packen)", schule),
        ("🧒 Kinder-Ämtli", aemtli),
        ("🧘 Dein Slot", slot),
    ]
    hat_inhalt = bool(pinned)
    for titel, items in bloecke:
        if items:
            hat_inhalt = True
            lines.append(f"{titel}:")
            for x in items:
                lines.append(f"   • {x}")
            lines.append("")

    if not hat_inhalt:
        lines.append("Morgen ist zu Hause wenig los — gönn dir einen ruhigen Tag. 💛")
        lines.append("")

    if slot:
        lines.append("Dein Slot ist Schutz, kein Druck — nimm ihn dir, wenn er passt. 💛")

    return "\n".join(lines).strip()
