"""Vorabend-Briefing fuer den Haushalts-Bot.

Baut aus den Haushalts-Liste-Eintraegen (privat) und den offenen Business-
Aufgaben eine Telegram-Nachricht, die am Abend (19:00) kommt und den
NAECHSTEN Tag ankuendigt — Vorabend-Logik, damit Schule + Termine
rechtzeitig gepackt/vorbereitet sind.

Regeln:
- Wiederkehrend morgen: taeglich + (jeden 2. Tag) + woechentlich mit Wochentag = morgen
- Woechentlich OHNE festen Tag: bekommt einen festen, aus dem Aufgabennamen
  abgeleiteten Wochentag (Mo-Sa) — so verteilt sich die Wochenlast, statt
  jeden Montag als Block "diese Woche dran" zu erscheinen.
- Monatlich ohne Tag: analog auf einen festen Tag im Monat verteilt
- Datierte Termine: Fixes Datum morgen bis +3 Tage
- Jaehrliche Termine mit Datum: als Jahrestag, nicht als Einmal-Termin
- Geburtstage: 10-14 Tage vor dem Datum an Geschenk erinnern, am Tag ans Gratulieren
- Schule: Vorabend — Eintraege fuer morgen, immer mit Vorname.
  Schule wird NIE gepinnt: ein vergangener Turn-/Schwimmtag ist vorbei,
  auch wenn niemand "Erledigt" angehakt hat.
- Pinned: ueberfaellige einmalige Termine (Familie/Haushalt) bleiben oben
  bis erledigt, gedeckelt auf PINNED_MAX
- Business: offene Aufgaben mit Datum morgen + die aeltesten Ueberfaelligen
- Wer: Kinder -> "erinnere die Kinder", Mann -> "Mann:", Patricia -> deine Aufgabe
- Erledigte (Erledigt=ja) werden nie genannt
"""

from __future__ import annotations

import re
from calendar import monthrange
from datetime import date, timedelta
from zlib import crc32

import config

WOCHENTAG_KEY = {0: "Mo", 1: "Di", 2: "Mi", 3: "Do", 4: "Fr", 5: "Sa", 6: "So"}
WOCHENTAG_LANG = {
    "Mo": "Montag", "Di": "Dienstag", "Mi": "Mittwoch", "Do": "Donnerstag",
    "Fr": "Freitag", "Sa": "Samstag", "So": "Sonntag",
}
# Pro Block: (Telegram-Titel mit Emoji, PDF-Ressort-Marker ohne Emoji —
# Emojis rendern in den PDF-Standardfonts nicht).
BLOCK_META = {
    "pinned":        ("📌 Dranbleiben (bis erledigt)", "DRANBLEIBEN"),
    "schule":        ("🎒 Schule (für morgen packen)", "SCHULE — FÜR MORGEN PACKEN"),
    "content_feed":  ("📱 Content morgen", "CONTENT MORGEN"),
    "content_story": ("📖 Story morgen", "STORY MORGEN"),
    "business":      ("💼 Business", "BUSINESS"),
    "familie":       ("👨‍👩‍👧 Familie / Termine", "FAMILIE & TERMINE"),
    "haushalt":      ("🏠 Haushalt", "HAUSHALT"),
    "aemtli":        ("🧒 Kinder-Ämtli", "KINDER-ÄMTLI"),
    "slot":          ("🧘 Dein Slot", "DEIN SLOT"),
    # Titel wird zur Laufzeit mit der Saison gefuellt
    "saison":        ("Saison-Liste", "SAISON-LISTE"),
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


_EMOJI_RE = re.compile(
    "["
    "\U0001F000-\U0001FAFF"    # Emoji-Bloecke
    "←-⇿"            # Pfeile
    "⌀-⏿"            # Misc Technical (u.a. Sanduhr ⏳)
    "■-➿"            # Geometrisch + Dingbats (u.a. Warnzeichen ⚠)
    "⬀-⯿"
    "〰〽⃣"
    "︎️‍"       # Variantenselektoren + ZWJ
    "]+"
)

# Emojis, die im Telegram-Text Bedeutung tragen, bekommen fuers PDF ein Wort.
# Reine Typ-Icons (Karussell, Reel, Story) brauchen keins — der Typ steht
# ohnehin als Wort daneben.
_EMOJI_WORT = {
    "⏳": "überfällig — ",
    "⚠️": "Achtung: ",
    "🎁": "Geschenk: ",
    "🎂": "Geburtstag: ",
}


def _strip_emoji(text: str) -> str:
    """Macht eine Zeile PDF-tauglich.

    Die PDF-Standardfonts (Helvetica) koennen keine Emojis rendern und
    zeichnen stattdessen schwarze Kaesten. Bedeutungstragende Emojis werden
    darum durch ein Wort ersetzt, der Rest faellt weg.
    """
    for emoji, wort in _EMOJI_WORT.items():
        text = text.replace(emoji, wort)
    return _EMOJI_RE.sub("", text).strip()


# Woerter in der Notiz, die eine Saison verraten. Die Liste deckt ab, was in
# Patricias Haushalts-Liste tatsaechlich steht ("Herbst", "Frühling + Winter",
# "Dezember", "vor Fasnacht (Feb)", "vor Ostern").
_SAISON_WORTE = {
    "frühling": "Frühling", "fruehling": "Frühling", "frühjahr": "Frühling",
    "ostern": "Frühling", "märz": "Frühling", "april": "Frühling", "mai": "Frühling",
    "sommer": "Sommer", "juni": "Sommer", "juli": "Sommer", "august": "Sommer",
    "herbst": "Herbst", "september": "Herbst", "oktober": "Herbst",
    "november": "Herbst", "nov": "Herbst",
    "winter": "Winter", "dezember": "Winter", "advent": "Winter",
    "weihnacht": "Winter", "januar": "Winter", "februar": "Winter",
    "feb": "Winter", "fasnacht": "Winter",
}


def _saisonen_aus_notiz(notiz: str) -> set[str]:
    """Welche Saisons nennt die Notiz? Leer = keine Zuordnung moeglich."""
    if not notiz:
        return set()
    low = notiz.lower()
    return {saison for wort, saison in _SAISON_WORTE.items() if wort in low}


def _streu(text: str) -> int:
    """Stabiler Streuwert fuer einen Aufgabennamen.

    crc32 statt hash(): hash() ist pro Prozess randomisiert, der Wochentag
    einer Aufgabe wuerde sonst bei jedem Lauf springen.
    """
    return crc32(text.encode("utf-8"))


def _slot_wochentag(aufgabe: str) -> str:
    """Fester Wochentag (Mo-Sa) fuer eine Aufgabe ohne eigenen Wochentag."""
    slots = config.WOCHEN_SLOTS
    return slots[_streu(aufgabe) % len(slots)]


_MONATSTAG_RE = re.compile(r"\bam\s+(\d{1,2})\.")


def _monatstag_aus_notiz(notiz: str) -> int | None:
    """Liest einen festen Monatstag aus der Notiz (z.B. 'am 10. des Monats')."""
    if not notiz:
        return None
    m = _MONATSTAG_RE.search(notiz)
    if not m:
        return None
    tag = int(m.group(1))
    return tag if 1 <= tag <= 31 else None


def _slot_monatstag(aufgabe: str) -> int:
    """Fester Tag im Monat (1-28) fuer eine monatliche Aufgabe ohne Datum."""
    return _streu(aufgabe) % 28 + 1


def _ist_zweitagesslot(aufgabe: str, tag: date) -> bool:
    """Deterministisches 'jeden 2. Tag' — gerade/ungerade Tage je Aufgabe."""
    return tag.toordinal() % 2 == _streu(aufgabe) % 2


def _wer_prefix(wer: str | None, text: str) -> str:
    """Formatiert eine Zeile je nach Zustaendigkeit."""
    if wer == "Kinder":
        return f"erinnere die Kinder: {text}"
    if wer == "Mann":
        return f"Mann: {text}"
    return text


def _business_titel(morgen_key: str) -> str:
    """Blocktitel mit dem Tagesthema aus dem Business-Wochenrhythmus."""
    thema = config.BUSINESS_TAGESTHEMA.get(morgen_key)
    if not thema:
        return "💼 Business"
    return f"💼 Business — morgen ist {thema}-Tag ({config.BUSINESS_ARBEITSFENSTER})"


def _business_marker(morgen_key: str) -> str:
    """PDF-Ressort-Marker mit Tagesthema, ohne Emoji."""
    thema = config.BUSINESS_TAGESTHEMA.get(morgen_key)
    if not thema:
        return "BUSINESS"
    sauber = _strip_emoji(thema).upper()
    return f"BUSINESS — {sauber}-TAG ({config.BUSINESS_ARBEITSFENSTER})"


def _business_block(
    aufgaben: list[dict], heute: date, morgen: date, morgen_key: str
) -> list[str]:
    """Baut die Business-Zeilen: morgen faellig + aelteste Ueberfaellige.

    Einmal pro Woche kommen zusaetzlich die Aufgaben ohne Datum dazu — sonst
    bleiben sie fuer immer unsichtbar, weil der taegliche Block nur "morgen
    faellig" und "ueberfaellig" kennt.
    """
    faellig: list[str] = []
    ueberfaellig: list[tuple[date, str]] = []
    undatiert: list[str] = []

    for a in aufgaben:
        d = _parse_datum(a.get("datum"))
        if d is None:
            titel = a.get("aufgabe") or ""
            if titel and a.get("prioritaet") in config.BUSINESS_UNDATIERT_PRIOS:
                undatiert.append(f"{titel} [{a['prioritaet']}]")
            continue
        titel = a.get("aufgabe") or ""
        if not titel:
            continue
        prio = a.get("prioritaet")
        suffix = f" [{prio}]" if prio else ""
        if d == morgen:
            faellig.append(f"{titel}{suffix}")
        elif d < heute:
            ueberfaellig.append((d, f"{titel} (seit {d.strftime('%d.%m.')})"))

    zeilen: list[str] = []
    for x in faellig:
        zeilen.append(x)

    if not faellig:
        zeilen.append("nichts mit Datum morgen eingetragen")

    if ueberfaellig:
        ueberfaellig.sort(key=lambda t: t[0])
        rest = len(ueberfaellig) - config.BUSINESS_UEBERFAELLIG_MAX
        for _, text in ueberfaellig[:config.BUSINESS_UEBERFAELLIG_MAX]:
            zeilen.append(f"⏳ {text}")
        if rest > 0:
            wort = "weitere überfällige Aufgabe" if rest == 1 else "weitere überfällige Aufgaben"
            # bewusst ohne ⏳ — sonst liest es sich im PDF als
            # "überfällig — … und 1 weitere überfällige Aufgabe"
            zeilen.append(f"… und {rest} {wort}")

    if undatiert and morgen_key == config.BUSINESS_UNDATIERT_TAG:
        undatiert.sort()
        n = len(undatiert)
        max_u = config.BUSINESS_UNDATIERT_MAX
        zeilen.append("— ohne Termin, willst du eine davon diese Woche einplanen? —")
        if n <= max_u:
            zeilen.extend(undatiert)
        else:
            # wie die Saison-Liste woechentlich weiterdrehen, damit nicht immer
            # dieselben oben stehen
            offset = (morgen.isocalendar()[1] * max_u) % n
            zeilen.extend((undatiert + undatiert)[offset:offset + max_u])
            zeilen.append(f"… und {n - max_u} weitere ohne Termin")

    return zeilen


def _content_block(content: list[dict], morgen: date) -> tuple[list[str], list[str]]:
    """Trennt den Content fuer morgen in (Feed-Posts, Stories).

    Feed-Posts (Reel/Karussell/Einzelpost/...) und Stories werden getrennt
    ausgegeben, weil sie unterschiedliche Vorbereitung brauchen.
    """
    feed: list[str] = []
    stories: list[str] = []

    for c in content:
        if _parse_datum(c.get("datum")) != morgen:
            continue
        titel = (c.get("titel") or "").strip()
        if not titel:
            continue

        typen = c.get("typen") or []
        ist_story = "Story" in typen
        haupt_typ = typen[0] if typen else None
        icon = config.CONTENT_ICONS.get(haupt_typ, "•")

        teile = []
        if haupt_typ:
            teile.append(haupt_typ)
        if c.get("profil"):
            teile.append(c["profil"])
        kopf = f"{icon} {' · '.join(teile)}: " if teile else f"{icon} "

        zeile = f"{kopf}{titel}"
        if c.get("keyword"):
            zeile += f" · Keyword {c['keyword']}"
        if c.get("status") in config.CONTENT_STATUS_UNFERTIG:
            zeile += f" ⚠️ noch „{c['status']}\""

        (stories if ist_story else feed).append(zeile)

    return feed, stories


def baue_briefing_struktur(
    eintraege: list[dict],
    heute: date | None = None,
    business: list[dict] | None = None,
    content: list[dict] | None = None,
) -> dict:
    """Sammelt alles fuer morgen und gibt eine Render-neutrale Struktur zurueck.

    Telegram-Text und PDF rendern beide hieraus — so koennen die beiden
    Ausgaben nie inhaltlich auseinanderlaufen.
    """
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
    aemtli_taeglich: list[str] = []
    slot: list[str] = []
    saison_liste: list[str] = []

    saison = config.SAISON_MONATE[(heute + timedelta(days=1)).month]

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

        # ---- 1. SCHULE (Vorabend fuer morgen) ----
        # Bewusst VOR dem Pinned-Block: ein vergangener Turn-/Schwimm-/Waldtag
        # ist vorbei und darf nicht als "Dranbleiben" haengenbleiben, auch
        # wenn die Erledigt-Checkbox nie gesetzt wurde.
        if bereich == "Schule":
            faellig_morgen = (wochentag == morgen_key) or (d == morgen)
            if faellig_morgen:
                schule.append(zeile)
            continue

        # ---- 2. PINNED: ueberfaellige einmalige Termine (bis erledigt) ----
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

        # ---- 3. GEBURTSTAG (Geschenk-Vorlauf / Tag selbst) ----
        if bereich == "Geburtstag" and d is not None:
            tage = _tage_bis_jahrestag(d, morgen)
            if tage == 0:
                familie.append(f"🎂 {aufgabe} — morgen ist der Tag, ans Gratulieren denken")
            elif config.GEBURTSTAG_VORLAUF_MIN <= tage <= config.GEBURTSTAG_VORLAUF_MAX:
                familie.append(f"🎁 {aufgabe} — in {tage} Tagen, jetzt Geschenk besorgen")
            continue

        # ---- 4. JAEHRLICHE TERMINE MIT DATUM (Jahrestag, nicht einmalig) ----
        if rhythmus == "jährlich" and d is not None:
            tage = _tage_bis_jahrestag(d, morgen)
            if tage <= config.TERMIN_LOOKAHEAD_TAGE:
                wann = "morgen" if tage == 0 else f"in {tage + 1} Tagen"
                ziel = familie if bereich in ("Familie/Termin", "Geburtstag") else haushalt
                ziel.append(_wer_prefix(wer, f"{zeile} ({wann})"))
            continue

        # ---- 5. DATIERTE TERMINE (morgen bis +Lookahead) ----
        if d is not None:
            delta = (d - morgen).days
            if 0 <= delta <= config.TERMIN_LOOKAHEAD_TAGE:
                wann = "morgen" if delta == 0 else f"in {delta + 1} Tagen ({d.strftime('%d.%m.')})"
                familie.append(_wer_prefix(wer, f"{zeile} ({wann})"))
            continue

        # ---- 6. WIEDERKEHREND ----
        ziel = haushalt
        if bereich == "Kinder-Ämtli":
            ziel = aemtli
        elif bereich == "Selbst/Me-Time":
            ziel = slot
        elif bereich == "Familie/Termin":
            ziel = familie

        if rhythmus == "täglich":
            if ziel is aemtli:
                # Die taeglichen Kinder-Aemtli sind jeden Tag dieselben —
                # als eine Zeile buendeln statt sieben Zeilen Rauschen.
                aemtli_taeglich.append(aufgabe)
            else:
                ziel.append(_wer_prefix(wer, zeile))
        elif rhythmus == "jeden 2. Tag":
            if _ist_zweitagesslot(aufgabe, morgen):
                ziel.append(_wer_prefix(wer, zeile))
        elif rhythmus == "wöchentlich":
            if wochentag and wochentag != "–":
                if wochentag == morgen_key:
                    ziel.append(_wer_prefix(wer, zeile))
            else:
                # kein Wochentag-Feld: erst Notiz nach Tagen absuchen
                # (z.B. Krafttraining "Mo / Mi / Fr"), sonst festen Slot
                # aus dem Aufgabennamen ableiten.
                tage_notiz = _wochentage_aus_notiz(notiz)
                if tage_notiz:
                    if morgen_key in tage_notiz:
                        ziel.append(_wer_prefix(wer, zeile))
                elif _slot_wochentag(aufgabe) == morgen_key:
                    ziel.append(_wer_prefix(wer, zeile))
        elif rhythmus == "monatlich":
            if wochentag and wochentag != "–":
                # z.B. "Mi" = am ersten passenden Wochentag des Monats
                if wochentag == morgen_key and morgen.day <= 7:
                    ziel.append(_wer_prefix(wer, f"{zeile} (diesen Monat dran)"))
            elif (gewuenscht := _monatstag_aus_notiz(notiz)) is not None:
                # Patricia hat einen Tag vorgegeben ("am 10. des Monats").
                # In kurzen Monaten auf den letzten Tag ziehen, damit ein
                # 31. im Februar nicht verschluckt wird.
                letzter = monthrange(morgen.year, morgen.month)[1]
                if morgen.day == min(gewuenscht, letzter):
                    ziel.append(_wer_prefix(wer, zeile))
            elif _slot_monatstag(aufgabe) == morgen.day:
                ziel.append(_wer_prefix(wer, f"{zeile} (diesen Monat dran)"))
        elif rhythmus in config.SAISON_RHYTHMEN:
            # Saison-Aufgaben haben keinen Kalendertag. Sie kommen einmal pro
            # Woche (Vorabend von SAISON_TAG) und nur, wenn die Notiz die
            # laufende Saison nennt — sonst wuerde geraten.
            if morgen_key != config.SAISON_TAG:
                pass
            elif saison in _saisonen_aus_notiz(notiz):
                saison_liste.append(_wer_prefix(wer, zeile))
            elif (rhythmus == "alle 3 Monate"
                  and not _saisonen_aus_notiz(notiz)
                  and morgen.month in config.SAISON_START_MONATE):
                # Quartalsaufgaben ohne Saison-Angabe: viermal im Jahr, jeweils
                # zum Saisonwechsel. Das ist genau ihr Rhythmus — kein Raten.
                # Kein Suffix, wenn die Notiz das schon sagt ("quartalsweise").
                suffix = "" if "quartal" in notiz_low else " (quartalsweise)"
                saison_liste.append(_wer_prefix(wer, f"{zeile}{suffix}"))
        # "nach Bedarf" sowie Saison-Aufgaben ohne Saison-Angabe in der Notiz:
        # bewusst NICHT im Push — lieber nichts sagen als raten.

    # ---- Struktur zusammenbauen ----
    if aemtli_taeglich:
        aemtli.insert(0, "tägliche Ämtli-Runde: " + " · ".join(aemtli_taeglich))

    if len(saison_liste) > config.SAISON_MAX:
        # Nicht einfach abschneiden — dann haengt es an der zufaelligen
        # Reihenfolge in Notion, welche Aufgabe nie drankommt (die
        # Steuererklaerung war so ein Fall). Stattdessen wird die alphabetisch
        # sortierte Liste woechentlich weitergedreht: ueber zwei, drei Wochen
        # sieht Patricia alles, und die Liste bleibt trotzdem kurz.
        saison_liste.sort()
        n = len(saison_liste)
        rest_saison = n - config.SAISON_MAX
        offset = (morgen.isocalendar()[1] * config.SAISON_MAX) % n
        gedreht = saison_liste[offset:] + saison_liste[:offset]
        saison_liste = gedreht[:config.SAISON_MAX]
        wort = "weiterer Punkt" if rest_saison == 1 else "weitere Punkte"
        saison_liste.append(f"… und {rest_saison} {wort} — kommen nächste Woche dran")

    if pinned:
        rest_pins = len(pinned) - config.PINNED_MAX
        pinned = pinned[:config.PINNED_MAX]
        if rest_pins > 0:
            wort = "weiterer offener Punkt" if rest_pins == 1 else "weitere offene Punkte"
            pinned.append(f"… und {rest_pins} {wort}")

    # Business-Block nur an Arbeitstagen — Sa/So bleibt frei.
    tagesthema = config.BUSINESS_TAGESTHEMA.get(morgen_key)
    if tagesthema:
        business_zeilen = _business_block(business or [], heute, morgen, morgen_key)
        notiz_tag = config.BUSINESS_TAGESNOTIZ.get(morgen_key)
        if notiz_tag and business_zeilen:
            business_zeilen.append(notiz_tag)
    else:
        business_zeilen = []

    content_feed, content_stories = _content_block(content or [], morgen)

    roh = [
        ("pinned", pinned),
        ("schule", schule),
        ("content_feed", content_feed),
        ("content_story", content_stories),
        ("business", business_zeilen),
        ("familie", familie),
        ("haushalt", haushalt),
        ("aemtli", aemtli),
        ("saison", saison_liste),
        ("slot", slot),
    ]

    bloecke = []
    for key, items in roh:
        if not items:
            continue
        titel, marker = BLOCK_META[key]
        if key == "business":
            titel = _business_titel(morgen_key)
            marker = _business_marker(morgen_key)
        elif key == "saison":
            emoji = config.SAISON_EMOJI.get(saison, "")
            titel = f"{emoji} {saison}-Liste (einmal pro Woche)".strip()
            marker = f"{saison.upper()}-LISTE"
        bloecke.append({"key": key, "titel": titel, "marker": marker, "items": items})

    return {
        "heute": heute,
        "morgen": morgen,
        "morgen_key": morgen_key,
        "morgen_lang": morgen_lang,
        "datum_lang": f"{morgen_lang}, {morgen.day}. {MONATE[morgen.month]} {morgen.year}",
        "tagesthema": tagesthema,
        "saison": saison,
        "bloecke": bloecke,
        "hat_inhalt": bool(bloecke),
    }


def baue_vorabend_briefing(
    eintraege: list[dict],
    heute: date | None = None,
    business: list[dict] | None = None,
    content: list[dict] | None = None,
    struktur: dict | None = None,
) -> str:
    """Rendert die Vorabend-Nachricht als Telegram-Text."""
    if struktur is None:
        struktur = baue_briefing_struktur(eintraege, heute, business, content)

    lines: list[str] = []
    lines.append(f"🌙 Vorabend — morgen ist {struktur['datum_lang']}")
    lines.append("")

    for block in struktur["bloecke"]:
        bullet = "⚠️" if block["key"] == "pinned" else "•"
        lines.append(f"{block['titel']}:")
        for x in block["items"]:
            lines.append(f"   {bullet} {x}")
        lines.append("")

    if not struktur["hat_inhalt"]:
        lines.append("Morgen ist zu Hause wenig los — gönn dir einen ruhigen Tag. 💛")
        lines.append("")

    if any(b["key"] == "slot" for b in struktur["bloecke"]):
        lines.append("Dein Slot ist Schutz, kein Druck — nimm ihn dir, wenn er passt. 💛")

    return "\n".join(lines).strip()


def baue_kurzfassung(struktur: dict) -> str:
    """Kurze Telegram-Begleitnachricht zum PDF (Sperrbildschirm-tauglich)."""
    kopf = f"🌙 Vorabend — morgen ist {struktur['datum_lang']}"
    if struktur["tagesthema"]:
        kopf += f" · {struktur['tagesthema']}-Tag"

    lines = [kopf, ""]
    # Die Blöcke, die am Abend noch Handlung auslösen
    for key in ("pinned", "schule", "content_feed", "content_story"):
        block = next((b for b in struktur["bloecke"] if b["key"] == key), None)
        if not block:
            continue
        lines.append(f"{block['titel']}:")
        for x in block["items"][:3]:
            lines.append(f"   • {x}")
        rest = len(block["items"]) - 3
        if rest > 0:
            lines.append(f"   • … +{rest} im PDF")
        lines.append("")

    if len(lines) <= 2:
        lines.append("Morgen ist wenig los — Details im PDF. 💛")
    else:
        lines.append("Alles Weitere steht im PDF. 💛")

    text = "\n".join(lines).strip()
    # Telegram-Caption-Limit
    return text[:1000]
