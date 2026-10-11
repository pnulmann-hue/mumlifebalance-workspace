"""
Baut die Cockpit-Dokumente fuer KW38 (1 Karussell + 4 Reels) als JSON.

Alle Hooks sind durch `scripts/content/hook-pruefen.py` gelaufen und gegen die
zwei Tore aus `context/hook-framework.md` begruendet. Der Painpoint kommt aus
`context/kern-painpoint.md` — die Rechnung geht nicht auf, die Abhaengigkeit,
der Job am Montagmorgen. Das Network bleibt in jedem Post heil, die Aufloesung
ist immer „daneben stellen".

Aufruf:
  python scripts/cockpit/kw38-dokumente-bauen.py [zielordner]
"""
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

STAND = "2026-09-11T08:00:00.000Z"
HANDLE = "@mumlifebalance_patricia_ulmann"

FOLGEN = ("Falls du gerade denkst: oh, cooler Ansatz, mal was anderes als die 100-Personen-Liste "
          "abzutelefonieren — dann folg mir. Hier gibt es Klartext zum Businessaufbau als Mama "
          "im Network.")
VORSTELLUNG = ("Hi, ich bin Patricia, Mama von vier Kindern. 2023 habe ich mein Network im "
               "Hybridmodell aufgebaut. Bei mir lernst du, wie du mit deinem Thema auf Instagram "
               "sichtbar wirst, wie du digitale Produkte passend zum Network entwickelst und wie "
               "du das ganze Business in deinen Mama-Alltag packst.")


def caption(*absaetze):
    return "\n\n".join(a.strip() for a in absaetze if a and a.strip())


# --------------------------------------------------------------------------
# DI 15.9. · Karussell · Reichweite
# Schmerz: die Abhaengigkeit — vieles liegt nicht in ihrer Macht.
# --------------------------------------------------------------------------
karussell = {
    "name": "KW38 Di · Was nicht in deiner Hand liegt",
    "brand": "mlb_light",
    "handle": HANDLE,
    "typ": "edukativ",
    "funnel": "TOF",
    "textfrei": False,
    "blotato": None,
    "slides": [
        {"layout": "hook", "headline":
            "Dein Einkommen hängt davon ab, dass andere Leute etwas tun.",
         "body": ""},
        {"layout": "text", "headline": "Und das kannst du nicht steuern.",
         "body": "Ob diesen Monat nachbestellt wird. Ob die Neue dranbleibt. Ob die Aktion "
                 "kommt, auf die du gewartet hast."},
        {"layout": "text", "headline": "Das ist kein Vorwurf ans Network.",
         "body": "Es ist einfach, wie es gebaut ist. Die Regeln macht das Partnerunternehmen, "
                 "und das ist auch in Ordnung — solange es nicht dein einziges Bein ist."},
        {"layout": "zitat", "headline":
            "Ein zweites Bein hängt nur an dir.", "body": ""},
        {"layout": "text", "headline": "Was damit gemeint ist.",
         "body": "Etwas Eigenes, das du einmal baust und das verkauft wird, auch wenn du zwei "
                 "Wochen für die Kinder da bist. Dein Wissen, nicht das Produkt einer Firma."},
        {"layout": "text", "headline": "Du gibst dafür nichts auf.",
         "body": "Dein Network bleibt, wo es ist. Team, Produkt, Community — alles bleibt. "
                 "Du stellst nur etwas daneben."},
        {"layout": "split", "headline": "Der Unterschied",
         "body": "Mit einem Bein wartest du darauf, dass andere etwas tun. Mit zwei Beinen hast "
                 "du eine Seite, auf der du selbst entscheidest."},
        {"layout": "cta", "headline": "Wo hängst du gerade am meisten von anderen ab?",
         "body": "Schreib es mir in die Kommentare. Ich antworte dir."},
    ],
    "caption": caption(
        "Letzte Woche hat mir jemand geschrieben, dass die Aktion, auf die sie ihren ganzen Monat "
        "geplant hatte, kurzfristig anders lief. Drei Wochen Arbeit, und dann entscheidet es "
        "jemand anders.",
        "Das ist der Teil am Network, über den wenig geredet wird. Nicht weil er schlimm wäre — "
        "es ist einfach, wie es gebaut ist. Die Regeln macht die Firma.",
        "Mich hat das lange gestört, bis ich aufgehört hab, dagegen anzukämpfen, und stattdessen "
        "etwas danebengestellt hab. Mein Network läuft weiter. Es ist nur nicht mehr das Einzige, "
        "woran mein Einkommen hängt.",
        "Swipe dich durch, dann siehst du, was ich meine.",
        FOLGEN, VORSTELLUNG,
        "#mamabusiness #mamaimnetworkmarketing #onlinebusinessmama #businessmom #nmstrategie"),
    "updatedAt": STAND,
}

# --------------------------------------------------------------------------
# Die vier Reels
# --------------------------------------------------------------------------
reels = {}

# MO · Reichweite · Schmerz: die Rechnung geht nicht auf, und sie weicht ihr aus.
reels["reel-kw38-mo"] = {
    "name": "KW38 Mo · Hat sich das gelohnt (Reichweite)",
    "hook": "Ich hab das Thema gewechselt.",
    "unter": "Mein Mann hat gefragt, ob sich das Network dieses Jahr gelohnt hat.",
    "pos": "unten",
    "brand": "mlb_dark",
    "scrim": True,
    "skript": "\n".join([
        "Mein Mann hat gefragt, ob sich das Network dieses Jahr gelohnt hat.",
        "Ich hab das Thema gewechselt.",
        "Dabei kenn ich die Antwort ganz genau.",
    ]),
    "caption": caption(
        "„Und, hat sich das dieses Jahr eigentlich gelohnt?“",
        "Mein Mann hat das mal beim Abendessen gefragt. Ganz beiläufig, ohne Hintergedanken. Und "
        "ich hab über das Wetter weitergeredet.",
        "Dabei kannte ich die Antwort ganz genau. Ich hab sie nur nicht laut sagen wollen.",
        "Das Verrückte daran: ich hab mein Network wirklich gemocht. Gutes Produkt, Leute, mit "
        "denen ich gern arbeite. Es hat einfach noch nicht gereicht. Und weil ich niemandem davon "
        "erzählt hab, hab ich auch nichts daran geändert.",
        "Geändert hat es sich erst, als ich aufgehört hab, mehr vom Gleichen zu machen, und "
        "angefangen hab, etwas Eigenes danebenzustellen. Aufgegeben hab ich dafür nichts.",
        "Falls dir diese Frage auch schon mal gestellt wurde und du ausgewichen bist: damit bist "
        "du ziemlich sicher nicht allein.",
        FOLGEN, VORSTELLUNG,
        "#mamabusiness #mamaimnetworkmarketing #onlinebusinessmama #selbstständigemama "
        "#nmstrategie"),
    "untertitel": "",
    "videodatei": "kw38-mo-hat-sich-gelohnt.mp4",
    "blotato": None,
    "updatedAt": STAND,
}

# MI · LEAD · Schmerz: wie lange dauert das noch — und bitte nicht wieder anschreiben.
reels["reel-kw38-mi"] = {
    "name": "KW38 Mi · 3 Wege ohne Namensliste (LEAD · STANDBEIN)",
    "hook": "3 Wege — ohne eine einzige Namensliste.",
    "unter": "Wär schon schön, damit mal richtig Geld zu verdienen.",
    "pos": "unten",
    "brand": "mlb_dark",
    "scrim": True,
    "skript": "\n".join([
        "Wär schon schön, damit mal richtig Geld zu verdienen.",
        "3 Wege — ohne eine einzige Namensliste.",
        "Und ohne dein Network aufzugeben.",
    ]),
    "caption": caption(
        "Wär schon schön, damit mal richtig Geld zu verdienen, oder?",
        "Und zwar ohne noch eine Namensliste durchzutelefonieren und ohne dein Network "
        "aufzugeben. Drei Wege, die genau das machen:",
        "1. Dein Wissen wird ein kleines eigenes Produkt. Du beantwortest sowieso ständig Fragen. "
        "Einmal aufgeschrieben, verkauft sich das auch dann, wenn du gerade am Familientisch "
        "sitzt.",
        "2. Die Leute kommen über dein Thema, nicht über dein Produkt. Wer dir wegen deines "
        "Themas folgt, kauft irgendwann auch das, was du daneben empfiehlst. In der Reihenfolge "
        "funktioniert es, umgekehrt selten.",
        "3. Ein Angebot, das nur an dir hängt. Kein Warten auf Aktionen, keine Abhängigkeit davon, "
        "ob diesen Monat jemand nachbestellt.",
        "Welcher davon zu dir passt, hängt davon ab, was du schon kannst. Genau dafür hab ich ein "
        "kleines Tool gebaut: du beantwortest ein paar Fragen und hast in fünf Minuten ein bis "
        "drei konkrete Ideen. Kostenlos.",
        "Kommentier STANDBEIN, dann schick ich dir den Link.",
        VORSTELLUNG,
        "#mamabusiness #onlinebusinessmama #mamaimnetworkmarketing #expertenbusiness #businessmom"),
    "untertitel": "",
    "videodatei": "kw38-mi-3-wege-STANDBEIN.mp4",
    "blotato": None,
    "updatedAt": STAND,
}

# DO · Reichweite · Einwand „ohne noch mehr zu arbeiten" plus KI-Alltag.
reels["reel-kw38-do"] = {
    "name": "KW38 Do · Zwischen Znüni und Abwasch (Reichweite)",
    "hook": "Zwischen Znüni und Abwasch.",
    "unter": "„Und wann machst du das alles — neben Kindern und Network?“",
    "pos": "unten",
    "brand": "mlb_dark",
    "scrim": True,
    "skript": "\n".join([
        "„Und wann machst du das alles — neben Kindern und Network?“",
        "Zwischen Znüni und Abwasch.",
        "Den Rest macht die KI.",
    ]),
    "caption": caption(
        "„Und wann machst du das alles?“ ist die Frage, die mir am häufigsten gestellt wird. "
        "Meistens von Frauen, die selbst gerade überlegen, ob sie noch etwas anfangen sollen.",
        "Die ehrliche Antwort: zwischen Znüni machen und Abwasch. Also in den Lücken, die sowieso "
        "da sind.",
        "Das geht, weil ich die langweiligen Teile abgegeben hab. Ich erzähl der KI, was ich sagen "
        "will, und sie macht die erste Fassung. Ich korrigiere, ich entscheide, ich gebe frei. "
        "Der Kopf bleibt bei mir, das Tippen nicht.",
        "Darum stimmt der Satz „ich hab keine Zeit für noch was“ in den allermeisten Fällen nicht "
        "mehr. Du brauchst keine zusätzlichen Stunden. Du brauchst andere Stunden.",
        "Falls du wissen willst, womit ich anfangen würde: schreib mir, woran du gerade am "
        "längsten sitzt. Dann sag ich dir, ob sich das abgeben lässt.",
        FOLGEN, VORSTELLUNG,
        "#mamabusiness #mamaimnetworkmarketing #onlinebusinessmama #selbstständigemama "
        "#businessmom"),
    "untertitel": "",
    "videodatei": "kw38-do-znueni-abwasch.mp4",
    "blotato": None,
    "updatedAt": STAND,
}

# FR · LEAD · Schmerz: der Job am Montagmorgen. Das Network steht auf ihrer Seite.
reels["reel-kw38-fr"] = {
    "name": "KW38 Fr · POV Montag ins Büro (LEAD · STANDBEIN)",
    "hook": "Und du gehst trotzdem am Montag ins Büro.",
    "unter": "POV: dein Network läuft.",
    "pos": "unten",
    "brand": "mlb_dark",
    "scrim": True,
    "skript": "\n".join([
        "POV: dein Network läuft.",
        "Und du gehst trotzdem am Montag ins Büro.",
    ]),
    "caption": caption(
        "POV: dein Network läuft. Gutes Produkt, gutes Team, du machst das wirklich gern.",
        "Und am Montag stehst du trotzdem auf und fährst in einen Job, den du eigentlich nicht "
        "mehr machen willst.",
        "Das ist der Punkt, an dem die meisten anfangen, an sich zu zweifeln. Dabei ist das kein "
        "Fleissproblem. Es ist eine Frage der Struktur: dein Einkommen hängt daran, dass andere "
        "Leute etwas tun, und das dauert eben.",
        "Was den Unterschied gemacht hat, war nicht mehr Einsatz. Es war ein zweites Bein daneben "
        "— etwas Eigenes, das mir gehört und das auch dann verkauft, wenn ich gerade nicht kann.",
        "Aufgegeben hab ich dafür nichts. Mein Network läuft bis heute.",
        "Wenn du wissen willst, was bei dir als Zweites danebenpasst: kommentier STANDBEIN, dann "
        "schick ich dir mein Tool. Fünf Minuten, kostenlos, und am Ende hast du ein bis drei "
        "konkrete Ideen.",
        VORSTELLUNG,
        "#mamabusiness #expertenbusiness #mamaimnetworkmarketing #selbstständigemama "
        "#nmstrategie"),
    "untertitel": "",
    "videodatei": "kw38-fr-pov-buero-STANDBEIN.mp4",
    "blotato": None,
    "updatedAt": STAND,
}


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("outputs/cockpit/kw38")
    ziel.mkdir(parents=True, exist_ok=True)
    dateien = {"kar-kw38-di.json": karussell}
    dateien.update({k + ".json": v for k, v in reels.items()})
    for name, doc in dateien.items():
        (ziel / name).write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        print("  %-24s Caption %4d Zeichen" % (name, len(doc.get("caption", ""))))
    print("\nAbgelegt in: %s" % ziel.resolve())


if __name__ == "__main__":
    main()
