# -*- coding: utf-8 -*-
"""Holt die Untertitel der Kursvideos von Vimeo und legt Transkripte ab.

    python scripts/ki-kurs/vimeo-transkripte.py            # holen und schreiben
    python scripts/ki-kurs/vimeo-transkripte.py --liste    # nur anzeigen

Quelle: `context/Kurse/aktuelle kurse/Easy-KI/videos-roh.json` — Nummer, Hash,
Vimeo-Name und Dauer je Video, abgerufen aus dem Ordner „Easy KI".
Ziel:   `context/Kurse/aktuelle kurse/Easy-KI/Transkripte/` als .vtt und .txt,
        im selben Format wie die Startklar-Transkripte.

🚨 Die Untertitel sind von VIMEO automatisch erzeugt, nicht von Whisper. Sie
   sitzen bei normalem Deutsch gut und verhoeren sich bei Fachwoertern: aus
   „Begriffe-Cheatsheet" wurde „Begriffs-ChatGPT". Jedes Transkript sagt das
   im Kopf, damit niemand eine Schreibweise daraus abschreibt.

🚨 Der Hash im Link ist der Unlisted-Schluessel — wer ihn hat, sieht den
   bezahlten Kurs. Er steht deshalb nur in der gitignorierten Quelldatei und
   nie in einer Datei unter `scripts/` oder `outputs/`.

Kein Schluessel, kein Login: der Player gibt die Untertitel zu einem unlisted
Video heraus, sobald der Hash mitkommt.
"""
import io
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
KURSORDNER = ROOT / "context" / "Kurse" / "aktuelle kurse" / "Easy-KI"
QUELLE = KURSORDNER / "videos-roh.json"
ZIEL = KURSORDNER / "Transkripte"

# Welcher Vimeo-Name gehoert zu welcher Lektion.
#
# 🚨 Modul 1 und 3 sind nur durchnummeriert („Modul 1 (3)"), Modul 4 hat gar
#    keine Namen („video1615913723"). Die Zuordnung ist deshalb NICHT geraten,
#    sondern am Inhalt des Transkripts geprueft — ein Video, das mit „Du hast
#    jetzt gelernt, dass es verschiedene Stufen gibt" anfaengt, ist die
#    Zusammenfassung und nicht die erste Lektion.
#    Ein Name, der hier fehlt, bekommt kein Lektionskuerzel. Lieber „ohne
#    Zuordnung" als eine falsche: ein falsch beschriftetes Transkript landet
#    sonst als Beleg in einer Antwort.
LEKTION = {
    "Modul 1 (1)": "1.1", "Modul 1 (2)": "1.2", "Modul 1 (3)": "1.3",
    "Modul 1 (4)": "1.4", "Modul 1 (5)": "1.5",
    "Modul 2.1": "2.1", "Modul 2.2": "2.2", "Modul 2.3": "2.3",
    "Modul 2.3b": "2.3b", "Modul 2.4": "2.4", "Modul 2.5": "2.5",
    "Modul 2.6": "2.6", "Modul 2.7": "2.7",
    "Modul 3 (1)": "3.1", "Modul 3 (2)": "3.2", "Modul 3 (3)": "3.3",
    "Modul 3 (4)": "3.4", "Modul 3 (5)": "3.5",
    # Modul 4 — zugeordnet am 22.10.2026. Der Beleg ist nicht die Nummer im
    # Dateinamen, sondern der SCHLUSSSATZ: jedes Video kuendigt das naechste an.
    #   video1 „…dann wirst du durchgefuehrt"        -> 4.1 kein Programmieren
    #   video2 „…schauen wir uns deinen Arbeitsplatz" -> 4.2 Einrichten
    #   video3 „…als Naechstes die Claude-MD-Datei"   -> 4.3 Arbeitsplatz
    #   video4 „…wie du mit Claude sprichst"          -> 4.4 Gedaechtnis
    #   video5 „…was du tun kannst, wenn etwas nicht klappt" -> 4.5 Sprechen
    #   video6 „…Zusammenfassung, eine Checkliste"    -> 4.6 wenn es nicht klappt
    #   video7 „Was nimmst du mit?"                   -> 4.7 Zusammenfassung
    # 🚨 Fuer 4.4b und 4.4c gibt es KEIN Video. Die beiden Lektionen sind erst
    #    am 22.10. dazugekommen, aufgenommen wurde vorher. Die Folien und der
    #    Plattformtext dazu stehen bereit — das Video fehlt.
    "video1615913723": "4.1", "video2615913723": "4.2",
    "video3615913723": "4.3", "video4615913723": "4.4",
    "video5615913723": "4.5", "video6615913723": "4.6",
    "video7615913723": "4.7",
}

KOPF = ("# Easy KI %s%s\n\n"
        "Quelle: Vimeo %s (%d:%02d)\n"
        "Untertitel: von Vimeo automatisch erzeugt, geholt %s\n"
        "\U0001f6a8 Fachwoerter koennen verhoert sein — nie eine Schreibweise "
        "hieraus abschreiben.\n\n---\n\n")


def hole(url, referer="https://vimeo.com/"):
    bitte = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0", "Referer": referer,
        "Accept": "*/*"})
    with urllib.request.urlopen(bitte, timeout=60) as antwort:
        return antwort.read().decode("utf-8")


def spur_von(nummer, hash_):
    """Die Untertitel-Adresse aus der Einbettungsseite.

    🚨 NICHT über `/video/<nr>/config?h=<hash>` — das antwortet mit **403**,
       mit Hash, mit Browser-Kennung und mit jedem Referer. Die Seite
       `/video/<nr>?h=<hash>` antwortet mit 200 und traegt dieselbe
       Konfiguration als `window.playerConfig` im Quelltext, samt
       unterschriebener Untertitel-Adresse. Geprueft an beiden Wegen am
       22.10.2026."""
    seite = hole("https://player.vimeo.com/video/%s?h=%s" % (nummer, hash_))
    m = re.search(r"window\.playerConfig\s*=\s*", seite)
    if not m:
        return None
    # 🚨 Nicht mit einem Muster bis zum naechsten `};` schneiden — in der
    #    Konfiguration stehen verschachtelte Objekte, und `{.*?\}\s*;` endet
    #    mitten drin (geprueft: Abbruch bei Zeichen 16'345). `raw_decode`
    #    liest ab der Klammer genau ein Objekt und sagt selbst, wo es endet.
    cfg, _ = json.JSONDecoder().raw_decode(seite, m.end())
    spuren = (cfg.get("request") or {}).get("text_tracks") or []
    if not spuren:
        return None
    adresse = spuren[0].get("url", "")
    if adresse.startswith("/"):
        adresse = "https://player.vimeo.com" + adresse
    return adresse


def prosa(vtt):
    """Nur der gesprochene Text — Zeitmarken, Nummern und Kopf raus.

    🚨 Nicht mit einem Leerzeichen zusammenkleben: die Zeilen sind an
       Sprechpausen geschnitten und ergeben zusammengefuegt eine Wand. Eine
       Zeile je Zeile bleibt lesbar und ist fuer die Suche genauso gut."""
    raus = []
    for z in vtt.splitlines():
        z = z.strip()
        if not z or z == "WEBVTT" or z.isdigit() or "-->" in z:
            continue
        if z.startswith("NOTE") or z.startswith("Kind:") or z.startswith("Language:"):
            continue
        raus.append(z)
    return "\n".join(raus)


def dateiname(i, name, lek):
    teil = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if lek:
        return "%02d-lektion-%s" % (i, lek.replace(".", "-"))
    return "%02d-%s" % (i, teil)


def main():
    from datetime import date
    nur_liste = "--liste" in sys.argv
    daten = json.loads(QUELLE.read_text(encoding="utf-8"))
    videos = daten["videos"]
    heute = date.today().strftime("%d.%m.%Y")

    ZIEL.mkdir(parents=True, exist_ok=True)
    gemacht, ohne = [], []
    for i, (nummer, hash_, name, dauer) in enumerate(videos, 1):
        lek = LEKTION.get(name)
        stamm = dateiname(i, name, lek)
        if nur_liste:
            print("  %-18s %-6s %3d:%02d  %s"
                  % (name, lek or "—", dauer // 60, dauer % 60, stamm))
            continue
        try:
            adresse = spur_von(nummer, hash_)
        except urllib.error.HTTPError as f:
            print("  ⚠ %s: Player antwortet %s" % (name, f.code))
            ohne.append(name)
            continue
        if not adresse:
            print("  ⚠ %s: keine Untertitel-Spur" % name)
            ohne.append(name)
            continue
        vtt = hole(adresse)
        text = prosa(vtt)
        if len(text) < 80:
            print("  ⚠ %s: Untertitel fast leer (%d Zeichen)" % (name, len(text)))
            ohne.append(name)
            continue
        titel = lek or ("ohne Zuordnung — " + name)
        kopf = KOPF % (titel, "" if lek else "", name, dauer // 60, dauer % 60, heute)
        io.open(ZIEL / (stamm + ".txt"), "w", encoding="utf-8", newline="\n").write(kopf + text + "\n")
        io.open(ZIEL / (stamm + ".vtt"), "w", encoding="utf-8", newline="\n").write(vtt)
        gemacht.append((stamm, lek, name, len(text)))
        print("  %-26s %-6s %6d Zeichen" % (stamm, lek or "—", len(text)))

    if nur_liste:
        return
    print("")
    print("  %d von %d Videos transkribiert -> %s" % (len(gemacht), len(videos), ZIEL))
    offen = [g for g in gemacht if not g[1]]
    if offen:
        print("  ⚠ %d ohne Lektionskuerzel — Zuordnung in LEKTION nachtragen:"
              % len(offen))
        for stamm, _, name, _ in offen:
            print("      %s  (%s)" % (name, stamm))
    if ohne:
        print("  ⚠ ohne Untertitel: %s" % ", ".join(ohne))


if __name__ == "__main__":
    main()
