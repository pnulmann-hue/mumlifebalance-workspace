# -*- coding: utf-8 -*-
"""Prueft Hooks und Captions gegen die vollstaendige Blackliste und die Caption-Regeln.

**Warum es das gibt.** Am 16.09.2026 habe ich die Blackliste mit einem von Hand
getippten Muster geprueft — `Nicht .{0,40}, sondern` — und damit **1 von 4** Treffern
gefunden. „Nicht weil etwas war. **Sondern** weil …" steht als zwei Saetze da und
rutschte durch. Patricia: *„kannst du bitte die hooks und captions nochmals pruefen und
zwar auf alle vorgaben"*.

🚨 **Eine Pruefung, die aus dem Gedaechtnis gebaut wird, prueft das, woran man gerade
denkt.** Deshalb steht hier die Liste aus `context/ki-phrasen-blackliste.md` als Code —
vollstaendig, benannt, nachlesbar.

**Was geprueft wird**

| Gruppe | Beispiele |
|---|---|
| Top-Verbote | Nicht/Sondern in allen Varianten · Dreier-Stakkato · Worthuelsen · abstrakte Content-Benefits · abstrakte Verben ohne Handelnden |
| Floskeln | Anleitungs-Floskeln · „Stell dir vor" · „Kennst du das" · Buzzwords · Superlative · Frage-Floskeln · Passiv-Konstruktionen · Zeit-Floskeln |
| Form | Schweizer ss · Hashtag-Zahl · `#mamabusiness` · abgebrochene Caption · Emoji-Zahl |
| Hook | Laenge der ersten Zeile · Loesungswoerter im Hook · Rueckfall auf „Guten Morgen" |
| CTA | Keyword vorhanden oder bewusst keins (Reichweiten-Post) |

**Was NICHT geprueft wird** und deshalb immer noch gelesen werden muss: ob der Hook
wirklich einen Schmerz trifft, ob man den Satz am Kuechentisch so sagen wuerde, und ob
die Leserin etwas Konkretes mitnimmt. Das ist der 🛑 Beitrags-Check, und den kann kein
Muster ersetzen.

    python scripts/cockpit/texte-pruefen.py            # alle
    python scripts/cockpit/texte-pruefen.py --nur reel-kw38-mi

---

🚨 **Wiederhergestellt am 18.09.2026.** Beim Schaerfen zweier Regeln habe ich die Datei
mit einem fehlgeschlagenen Schreibvorgang auf 0 Bytes gekuerzt; sie war nicht in Git.
Rekonstruiert aus `__pycache__/texte-pruefen.cpython-312.pyc` (Stand 16.09.) — die
Muster-Tabellen sind daraus **woertlich** uebernommen, nicht neu getippt.
**Lehre: diese Datei gehoert nach Git.**
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

WURZEL = Path(__file__).resolve().parents[2]
ROH = WURZEL / "outputs" / "cockpit" / "inhalte-roh"

# 🟠/🔴 Kontraste — EINER je Text ist erlaubt, wenn der Satz echt ist (Patricia,
# Interview B2b, 02.10.2026: „ich finde es eigentlich keine ki phrase. ist doch ein
# normaler satz. aber ja logisch wenn er hundertmal in einer caption vorkommt ist es
# doof"). Der erste Fund ist Schwere 2 (ansehen), jeder weitere Schwere 1 (raus).
KONTRAST = (
    (r"\b[Nn]ichts?\b[^.!?]{0,90}[.,;]?\s*[Ss]ondern\b", "Nicht/Sondern"),
    (r"\b[Kk]ein(?:e|en|em|er)?\b[^.!?]{0,90}[.,;]?\s*[Ss]ondern\b", "Kein/Sondern"),
    (r"[Ee]s geht nicht um[^.!?]{0,90}[,.]\s*[Ss]ondern", "Es geht nicht um/sondern"),
    (r"[Ee]s liegt nicht an[^.!?]{0,90}[,.]\s*[Ee]s liegt an",
     "Es liegt nicht an/es liegt an"),
    (r"[Dd]as Problem ist nicht[^.!?]{0,90}[,.]\s*[Dd]as Problem ist",
     "Das Problem ist nicht/ist"),
    (r"[Ee]s braucht kein[^.!?]{0,90}[,.]\s*[Ee]s braucht",
     "Es braucht kein/es braucht"),
    (r"\b[Ww]eniger\s+\w+[,]?\s+mehr\s+\w+", "Weniger X, mehr Y"),
    # Der Kontrast ohne das Wort „sondern" — die Tarnung, die am 16.09. drei von
    # vier Treffern verdeckt hat.
    (r"\b(?:war|ist|liegt|geht|scheiter\w+|hilft|braucht)\s+(?:es\s+)?nicht\b"
     r"[^.!?:;]{0,70}[.!?:;]\s+(?:[Ee]s war|[Ee]s ist|[Ee]s liegt|[Dd]as war"
     r"|[Dd]as ist|Sie scheiter\w+|Er scheiter\w+)\b", "Kontrast ohne sondern"),
)

# 🔴 Schwere 1 — das muss weg, bevor der Beitrag rausgeht.
SCHWER = (
    # Ersatz in ihren Worten (Interview B2/B2b): „Angenommen …" oder
    # „Gehen wir mal davon aus …" — gilt geschrieben UND gesprochen.
    (r"\bStell dir\b[^.!?]{0,70}\bvor\b",
     "Stell dir vor (→ „Angenommen …“ / „Gehen wir mal davon aus …“)"),
    # „tragen" im Sinn von sattmachen (Patricia 21.09.2026: „das traegt wuerde ich
    # NIE so sagen"). Gezielt nur die drei Konstruktionen, NICHT jedes „tragen" —
    # „ab vier Frauen traegt sich die Begleitung" ist Kaufmannssprache und in Ordnung.
    (r"\bd(?:as|er|ie)\s+trägt\b(?!\s+sich)", "das trägt (statt: satt machen)"),
    (r"\bbis\s+\w+\s+(?:trägt|tragen)\b", "bis X tragen (statt: satt machen)"),
    (r"\bdurch\s+den\s+Tag\s+(?:trägt|tragen)\b", "durch den Tag tragen"),
    # Anreden, die sie nie benutzt (Interview B4, 02.10.2026).
    (r"\bMädels\b|\bMaedels\b", "Mädels (sagt sie nie)"),
    (r"\bMamas da dra(?:u|ü)(?:ss|ß)en\b", "Mamas da draussen (sagt sie nie)"),
    (r"[Kk]ennst du (?:das|dies|diese[nsrm]?)\b", "Kennst du das"),
    (r"[Hh]ast du schon mal\b", "Hast du schon mal"),
    (r"[Ww]usstest du, dass\b", "Wusstest du dass"),
)

# 🟠 Schwere 2 — ansehen und begruenden, nicht blind streichen.
FLOSKELN = (
    (r"\bSo machst du\b|\bSo geht'?s\b|\bSo schaffst du\b|\bSo kannst du\b"
     r"|\bHier ist, wie du\b", "Anleitungs-Floskel"),
    (r"\bBist du bereit\b|\bWillst du endlich\b|\bMöchtest du auch\b"
     r"|\bTräumst du davon\b|\bSehnst du dich\b", "Frage-Floskel"),
    (r"[Ee]s wird gesagt|[Mm]an könnte meinen|[Ee]s ist bekannt, dass"
     r"|[Vv]iele denken, dass", "Passiv-Konstruktion"),
    (r"[Gg]ame.?[Cc]hanger|[Ll]evel.?[Uu]p|nächste[sn]? Level|[Dd]eep Dive"
     r"|[Mm]indset.?[Ss]hift|Transformationsreise|Erfolgsreise|[Ss]kaliere dein"
     r"|ultimative Lösung|[Dd]as Geheimnis zu|[Dd]ie Wahrheit über", "Buzzword"),
    (r"[Ll]eichtigkeit|[Ii]nnere Ruhe|[Dd]ein wahres Ich|in deine Kraft"
     r"|[Ff]low.?Zustand|[Mm]anifestier|[Ss]chwingung erhöhen"
     r"|limitierende Glaubenss", "Spirituelle Floskel"),
    (r"\bdie beste\b|\bdie perfekte\b|\bdie ultimative\b|\bdie einzige\b"
     r"|\bnie wieder\b|100\s?% garantiert|absolut sicher|völlig einzigartig",
     "Superlativ"),
    # „über Nacht" nur im Marketing-Sinn. In einem Rezept ist „Teig haelt ueber
    # Nacht" voellig in Ordnung — und zwei Fehlalarme reichen, damit niemand mehr
    # hinschaut (21.09.2026, an den 30 Fruehstuecken aufgefallen).
    (r"[Ii]n nur \d+ Tagen|[Ss]chnell und einfach|[Oo]hne Aufwand"
     r"|(?:[Ee]rfolg|[Dd]urchbruch|berühmt|reich|schlank|fit)\s+über\s+Nacht"
     r"|über\s+Nacht\s+(?:zum|zur|erfolgreich|berühmt)"
     r"|[Ss]ofort umsetzbar|[Ii]n Rekordzeit", "Zeit-Floskel"),
    # 🚨 „auf Augenhöhe" ist nur dann eine Worthuelse, wenn es NICHT die Kamera
    # meint. In einer Drehanleitung steht „Handy hochkant auf Augenhöhe" — das ist
    # eine Massangabe, kein Coaching-Sprech. (Geschaerft 18.09.2026.)
    (r"klare[rn]? Nutzen|echte Ergebnisse|konkrete[rn]? Plan|klare Richtung"
     r"|individuelle Lösung|massgeschneidert|ganz konkret|wertvolle Impulse"
     r"|praxisnah|(?<!Handy )(?<!Kamera )(?<!Linse )auf Augenhöhe", "Worthuelse"),
    (r"sichtbar werden|Wunschkundinnen erreichen|dich zeigen"
     r"|Angebot nach draussen|deine Expertise zeigen", "Abstrakter Content-Benefit"),
    (r"es trägt noch nicht|an dem Punkt, an dem es kippt|da entsteht etwas",
     "Abstraktes Verb ohne Handelnden"),
    # „Erfolg/Balance/Potenzial" nur als Benefit, nicht im Markennamen.
    (r"\bPotenzial entfalten\b|\bdeine Bestimmung\b|\bdeine Vision\b"
     r"|\bdeine Mission\b", "Leeres Versprechen"),
)

# Woerter, die im Hook die Antwort vorwegnehmen.
LOESUNGSWORT = ("eigenes Thema", "Positionierung", "sichtbar werden", "Personal Brand",
                "Reichweite aufbauen", "Funnel", "Leadmagnet", "Content-Strategie")

# Die vorgeschriebene Schluss-Zeile einer Lead-Caption: das Stichwort mit Pfeil,
# z. B. „**STANDBEIN** ⬇️" (content/SKILL.md, Abschnitt CTA). Das ist kein Abbruch.
CTA_SCHLUSS = re.compile(r"(?:\n|^)\s*\**[A-ZÄÖÜ0-9]{3,20}\**\s*[⬇\U0001f447]️?\s*$")


def umschrift(s):
    """ä→ae usw. — fuer Vergleiche, nie fuer Ausgabe."""
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def dreier_stakkato(text):
    """Drei kurze Saetze hintereinander mit gleichem Anfangswort."""
    saetze = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    for i in range(len(saetze) - 2):
        drei = saetze[i:i + 3]
        if all(len(s) < 60 for s in drei):
            anfaenge = [s.split()[0].lower().strip(",.:;„\"") for s in drei if s.split()]
            if len(anfaenge) == 3 and len(set(anfaenge)) == 1:
                return " / ".join(drei)
    return None


def emojis(text):
    return sum(1 for c in text if unicodedata.category(c) == "So")


def pruefe(d, doc_id, art="reels"):
    """Gibt eine Liste (Schwere, Befund, Stelle) zurueck. Schwere: 1 = raus, 2 = pruefen.

    🚨 Die drei Formate sind verschieden gebaut, und das ist kein Mangel:
    eine **Story** hat keine Caption und keinen Hook, sondern Folien; ein
    **Karussell** hat keinen Hook im eigenen Feld, sondern die erste Folie.
    Wer das nicht unterscheidet, erzeugt 17 Fehlalarme und man hoert auf
    hinzusehen — und dann faellt der echte Fund auch nicht mehr auf."""
    befunde = []
    cap = (d.get("caption") or "").strip()
    hook = (d.get("hook") or "").strip()
    if art == "karussells" and not hook and (d.get("slides") or []):
        hook = (d["slides"][0].get("headline") or "").strip()
    skript = (d.get("skript") or "").strip()
    folien = " ".join(((f.get("headline") or "") + " " + (f.get("body") or ""))
                      for f in (d.get("slides") or []))
    # Story-Folien heissen `frames` und tragen den Text in `text`.
    folien += " " + " ".join((f.get("text") or "") + " " + (f.get("cta") or "")
                             for f in (d.get("frames") or []))
    alles = "\n".join([hook, cap, skript, folien])

    # Zwei Muster koennen auf denselben Satz passen („Es geht nicht um X, sondern Y"
    # ist auch ein Nicht/Sondern) — ueberlappende Funde zaehlen nur einmal.
    roh = sorted((m.start(), m.end(), name, m.group(0)) for pat, name in KONTRAST
                 for m in re.finditer(pat, alles))
    kontraste, bis = [], -1
    for start, ende, name, stelle in roh:
        if start < bis:
            continue
        kontraste.append((start, name, stelle))
        bis = ende
    for i, (_, name, stelle) in enumerate(kontraste):
        if i == 0:
            befunde.append((2, name + " (einer erlaubt — ist er echt?)", stelle[:110]))
        else:
            befunde.append((1, name + f" ({i + 1}. Kontrast im Text)", stelle[:110]))
    for pat, name in SCHWER:
        for m in re.finditer(pat, alles):
            befunde.append((1, name, m.group(0)[:110]))
    for pat, name in FLOSKELN:
        for m in re.finditer(pat, alles):
            befunde.append((2, name, m.group(0)[:110]))

    st = dreier_stakkato(cap)
    if st:
        befunde.append((1, "Dreier-Stakkato", st[:110]))

    # --- Form ----------------------------------------------------------
    if "ß" in alles:
        befunde.append((1, "Deutsches ss", "ß gefunden"))
    if cap:
        tags = re.findall(r"#\w+", cap)
        if len(tags) != 5:
            befunde.append((2, "Hashtag-Zahl", f"{len(tags)} statt 5"))
        if not any(umschrift(t).lower() == "#mamabusiness" for t in tags) \
           and d.get("profil") != "doterra":
            befunde.append((2, "Kein #mamabusiness", " ".join(tags)))
        ohne_tags = re.sub(r"(#\w+\s*)+$", "", cap).strip()
        # Die Stichwort-Zeile am Schluss ist das gewollte Ende, kein Abbruch.
        # Vor der Pruefung abziehen — sonst meldet jede Lead-Caption einen Fehler.
        ohne_cta = CTA_SCHLUSS.sub("", ohne_tags).strip()
        if ohne_cta and ohne_cta[-1] not in ".!?\"'“”…)":
            befunde.append((1, "Caption bricht ab", "…" + ohne_cta[-70:]))
        if emojis(cap) > 3:
            befunde.append((2, "Zu viele Emojis", f"{emojis(cap)} Stueck"))
    elif art != "storys":
        befunde.append((1, "Keine Caption", "—"))

    # --- Hook ----------------------------------------------------------
    if hook:
        erste = hook.split("\n")[0]
        if len(erste) > 120:
            befunde.append((2, "Hook zu lang", f"{len(erste)} Zeichen"))
        for w in LOESUNGSWORT:
            if w.lower() in hook.lower():
                befunde.append((1, "Loesungswort im Hook", w))
        if re.match(r"^(Guten Morgen|Hallo|Hey ihr|Liebe )", erste):
            befunde.append((1, "Hook ohne Knall", erste[:60]))
    elif art != "storys":
        befunde.append((2, "Kein Hook-Feld", "—"))

    return befunde


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nur", help="nur diese eine ID pruefen")
    ap.add_argument("--datei", nargs="+", help="Markdown-Dateien statt Cockpit-Beitraegen pruefen (z.B. ein /angebot-Paket)")
    args = ap.parse_args()

    if args.datei:
        # Eine Datei zaehlt wie eine Caption: dieselben Muster, kein Hook-Feld.
        gesamt = {1: 0, 2: 0}
        for pfad in args.datei:
            text = Path(pfad).read_text(encoding="utf-8")
            # Hashtag- und Hook-Pruefungen gelten nur fuer Instagram-Beitraege.
            befunde = [b for b in pruefe({"caption": text}, Path(pfad).name)
                       if not b[1].startswith(("Hashtag", "Kein #", "Kein Hook",
                                               "Caption bricht ab", "Zu viele Emojis"))]
            print(f"\n{pfad}" + ("  —  sauber" if not befunde else ""))
            for schwere, name, stelle in sorted(befunde):
                gesamt[schwere] += 1
                print(f"   {'🔴' if schwere == 1 else '🟠'} {name}: {stelle}")
        print(f"\n{len(args.datei)} Dateien geprueft · 🔴 {gesamt[1]} muss weg · 🟠 {gesamt[2]} ansehen")
        return

    gesamt = {1: 0, 2: 0}
    geprueft = 0
    for ordner in ("reels", "karussells", "storys"):
        p = ROH / ordner
        if not p.is_dir():
            continue
        for datei in sorted(p.glob("*.json")):
            if args.nur and datei.stem != args.nur:
                continue
            d = json.loads(datei.read_text(encoding="utf-8"))
            if not (d.get("name") or "").strip() or d.get("name") == "Neues Reel":
                continue
            geprueft += 1
            befunde = pruefe(d, datei.stem, ordner)
            if not befunde:
                continue
            print(f"\n{datei.stem}  —  {d.get('name', '')}")
            for schwere, name, stelle in sorted(befunde):
                gesamt[schwere] += 1
                zeichen = "🔴" if schwere == 1 else "🟠"
                print(f"   {zeichen} {name}: {stelle}")

    print(f"\n{'=' * 60}")
    print(f"{geprueft} Beitraege geprueft · 🔴 {gesamt[1]} muss weg · "
          f"🟠 {gesamt[2]} ansehen")
    print("🚨 Der Beitrags-Check (berührt es · nimmt sie etwas mit · speichern · "
          "kommentieren · nur von ihr)\n   ist damit NICHT erledigt — den macht kein Muster.")


if __name__ == "__main__":
    main()
