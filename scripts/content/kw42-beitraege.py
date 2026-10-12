#!/usr/bin/env python3
"""Beitraege 13.-16.10.2026 fuers Cockpit: 4 Karussells (Di + Do, je A/B) und 8 Reels
(Feed Mi + Fr je A/B, Trial Reels T1-T4 inkl. Verlosung).

Hooks: outputs/content/KW42/hooks.md (Fassung 3, Tresor-Formeln).
Ausgabe: outputs/cockpit/abgleich/kw42-neu/<sammlung>/<id>.json  (gitignored)
       + outputs/content/KW42/beitraege-13-16.md (lesbar, fuer den Workspace)
Danach: ArtifactData batch set (Sammlungen karussells / reels).

🚨 Zwei Zielgruppen-Ebenen: wer auf das Profil der Kundin kommt, ist IHRE Kundschaft —
dort „jemand", „man", „wer", nie „sie" oder „Kundin".
"""
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
WURZEL = pathlib.Path(__file__).resolve().parents[2]
AUS = WURZEL / "outputs" / "cockpit" / "abgleich" / "kw42-neu"
MD = WURZEL / "outputs" / "content" / "KW42" / "beitraege-13-16.md"
STAND = "2026-10-12T21:30:00.000Z"

INTRO = ("Hi, ich bin Patricia, Mama von vier Kindern. 2023 habe ich mein Network im "
         "Hybridmodell aufgebaut. Bei mir lernst du, wie du mit deinem Thema auf Instagram "
         "sichtbar wirst, wie du digitale Produkte passend zum Network entwickelst und wie du "
         "das ganze Business in deinen Mama-Alltag packst.")
TAGS_NETWORK = "#mamabusiness #mamaimnetworkmarketing #onlinebusinessmama #networkmarketing #mumpreneur"
TAGS_KI = "#mamabusiness #kifuermamas #mamaimnetworkmarketing #onlinebusinessmama #mumpreneur"

CTA_STIMME = ("Kommentier STIMME, dann schick ich dir den Stimm-Check gratis. Sechs Fragen, "
              "rund 15 Minuten, und deine KI weiss, wie du klingst.\n\nSTIMME ⬇️")
CTA_BIO = ("Kommentier BIO, dann schick ich dir den Bio-Check. Er schaut sich deine Bio an "
           "und sagt dir ehrlich, was fehlt.\n\nBIO ⬇️")
FOLG = ("Schick das der Freundin, die gerade aufhören will. Und folg mir, wenn du dir neben "
        "deinem Network etwas Eigenes aufbauen willst.")


def cap(text, cta, tags):
    return f"{text}\n\n{cta}\n\n{INTRO}\n\n{tags}"


def leer():
    return {"kommentar": "", "kommentarAntwort": "", "kommentarErledigt": "",
            "kommentarStand": "", "abgelehnt": False, "abgelehntStand": "",
            "textfrei": False, "updatedAt": STAND, "profil": "mentoring",
            "handle": "@mumlifebalance_patricia_ulmann"}


KARUSSELLS = {
    "kw42-kar-m-di-a": dict(
        name="A · Di · 5 Warnsignale, dass alles an einem Produkt hängt",
        datum="2026-10-13", zeit="21:00", typ="listicle", funnel="TOF", job="Reichweite",
        angle="Identität", brand="mlb_light",
        slides=[
            ("hook", "5 Warnsignale, dass dein Network-Einkommen an einem einzigen Produkt hängt 🚨",
             "Nummer 4 hab ich in meinem ersten Network jahrelang übersehen."),
            ("text", "1 · Deine Bio nennt die Firma, aber nicht, wobei du hilfst",
             "Wer dich findet, sieht eine Beraterin von vielen.\n\nWofür man dich fragen soll, steht nirgends."),
            ("text", "2 · Deine letzten neun Beiträge zeigen dasselbe Produkt",
             "Dann wird dein Profil zur Katalogseite.\n\nEinem Katalog folgt man nicht, man blättert weiter."),
            ("text", "3 · Du postest, was in die Teamgruppe kommt",
             "Dann sieht dein Profil aus wie das von allen anderen im Team, oft am selben Abend."),
            ("text", "4 · Fragt dich jemand, was du machst, nennst du den Produktnamen",
             "Dabei kauft niemand ein Produkt.\n\nGekauft wird, was danach anders ist: mehr Energie, mehr Ruhe, weniger Chaos."),
            ("text", "5 · Ohne die Firma hättest du morgen nichts, das dir gehört",
             "Kein Thema, keine Liste, keine Leute, die dir folgen, weil du du bist."),
            ("text", "Das Produkt darf bleiben",
             "Es braucht nur etwas darunter, das dir gehört: ein Thema, für das man dich fragt, und Leute, die wegen dir dranbleiben."),
            ("text", "Zwei oder mehr wiedererkannt?",
             "Dann weisst du jetzt, wo du anfängst.\n\nFang bei Nummer 1 an. Die ist in zehn Minuten erledigt."),
            ("cta", "Schick das einer Freundin im Network 💌",
             "Der, an die du bei Nummer 3 gedacht hast."),
        ],
        caption=("Mein erstes Network hab ich nach drei Jahren aufgegeben. Damals dachte ich, es "
                 "liegt am Produkt oder an mir. Heute weiss ich, dass einfach alles an diesem einen "
                 "Produkt hing, und als es nicht lief, hatte ich nichts, das mir gehörte.\n\n"
                 "Die fünf Warnsignale im Karussell hatte ich damals alle. Nummer 4 am längsten.\n\n"
                 "Das Produkt darf bleiben. Es braucht nur etwas darunter, das dir gehört: ein "
                 "Thema, für das man dich fragt, und Leute, die wegen dir dranbleiben.",
                 "Schick das einer Freundin im Network, bei der du beim Lesen an Nummer 3 gedacht hast. 💌",
                 TAGS_NETWORK)),
    "kw42-kar-m-di-b": dict(
        name="B · Di · POV: Darf ich das überhaupt?",
        datum="2026-10-13", zeit="21:00", typ="edukativ", funnel="TOF", job="Reichweite",
        angle="Identität", brand="mlb_light",
        slides=[
            ("hook", "POV: Du willst endlich etwas Eigenes neben deinem Network.",
             "Und dann kommt dieser kleine fiese Gedanke: Darf ich das überhaupt?"),
            ("text", "Der Gedanke kommt selten von dir",
             "Meistens hast du ihn irgendwo gehört: «Konzentrier dich aufs Network, alles andere lenkt ab.»"),
            ("text", "Und er klingt vernünftig",
             "Wer sich verzettelt, kommt nirgends an.\n\nDas stimmt sogar."),
            ("text", "Etwas Eigenes heisst aber nicht: noch ein Business",
             "Es heisst: ein Thema, für das man dich fragt.\n\nDein Network darf darin vorkommen."),
            ("text", "Bei mir sah das so aus",
             "2023 hab ich mit doTERRA neu angefangen, diesmal mit einem Thema vorne statt mit dem Produkt.\n\nHeute hab ich zwei Standbeine, und keins nimmt dem anderen etwas weg."),
            ("text", "Was das im Alltag ändert",
             "Wenn sich irgendwo etwas ändert, fällt nicht gleich alles um.\n\nUnd ich verlasse mich nicht allein auf Instagram, weil ich eine eigene Mailliste habe."),
            ("text", "Frag dich lieber das",
             "Was würde ich aufbauen, wenn ich niemanden um Erlaubnis fragen müsste?"),
            ("cta", "Schick das der Freundin, die genau diesen Gedanken auch hat 💌", ""),
        ],
        caption=("Darf ich überhaupt etwas Eigenes neben meinem Network aufbauen? Viele stellen "
                 "die Frage nie laut, aber sie denken sie.\n\n"
                 "Meistens stammt sie nicht mal von dir. Du hast irgendwo gehört, dass alles andere "
                 "ablenkt, und das klingt vernünftig. Verzetteln bringt wirklich niemanden weiter.\n\n"
                 "Etwas Eigenes heisst bei mir: ein Thema, für das man mich fragt. Mein Network läuft "
                 "darin weiter, und seit ich zwei Standbeine habe, fällt nicht gleich alles um, wenn "
                 "sich irgendwo etwas ändert.",
                 "Schick das der Freundin, die genau diesen Gedanken auch schon hatte. 💌",
                 TAGS_NETWORK)),
    "kw42-kar-m-do-a": dict(
        name="A · Do · 5 Fragen, warum dein Profil keine Anfragen bringt",
        datum="2026-10-15", zeit="07:30", typ="listicle", funnel="MOF", job="Lead",
        angle="Neugier", brand="mlb_light", keyword="BIO",
        slides=[
            ("hook", "Diese 5 Fragen decken schonungslos auf, warum dein Instagram-Profil keine Anfragen bringt.",
             "Beantworte sie ehrlich. Es dauert zwei Minuten."),
            ("text", "1 · Weiss jemand Fremdes nach der ersten Zeile, wobei du hilfst?",
             "Steht da «Mama · Networkerin · liebe Kaffee», weiss man, wer du bist.\n\nAber nicht, warum man bleiben soll."),
            ("text", "2 · Steht in deinem Namensfeld, was du löst?",
             "Das Namensfeld wird bei der Instagram-Suche mitgelesen.\n\nNach deinem Vornamen allein sucht niemand."),
            ("text", "3 · Gibt es einen nächsten Schritt?",
             "Ein Link, ein Stichwort, ein kleines Angebot.\n\nOhne das liest man, nickt und geht."),
            ("text", "4 · Würde man dich unter zehn Beraterinnen derselben Firma wiedererkennen?",
             "Wenn deine Bio genauso bei den anderen stehen könnte, ist es noch nicht deine."),
            ("text", "5 · Passt deine Bio zu deinen letzten neun Beiträgen?",
             "Verspricht die Bio Energie und der Feed zeigt Produktbilder, glaubt man keinem von beiden."),
            ("text", "Zweimal oder öfter Nein?",
             "Dann liegt es nicht an deinem Fleiss.\n\nEs liegt an den ersten zwei Zeilen, und die sind am schnellsten geändert."),
            ("cta", "Wie wirkt deine Bio auf Fremde?",
             "Kommentier BIO, dann schick ich dir den Bio-Check. Er schaut sich deine Bio an und sagt dir ehrlich, was fehlt."),
        ],
        caption=("Wie viele Anfragen hast du diesen Monat über dein Profil bekommen? Wenn die "
                 "Antwort «fast keine» ist, liegt es selten an deinem Fleiss.\n\n"
                 "Wer auf dein Profil kommt, entscheidet in ein paar Sekunden, ob es sich lohnt zu "
                 "bleiben. Gelesen werden dabei fast nur dein Name und die ersten zwei Zeilen.\n\n"
                 "Im Karussell stehen die fünf Fragen, die ich mir bei einem Profil zuerst stelle. "
                 "Beantworte sie ehrlich, das dauert zwei Minuten. Zweimal Nein reicht, damit du "
                 "weisst, wo du anfängst.",
                 CTA_BIO, TAGS_NETWORK)),
    "kw42-kar-m-do-b": dict(
        name="B · Do · Der grösste Fehler steht in der ersten Zeile",
        datum="2026-10-15", zeit="07:30", typ="edukativ", funnel="MOF", job="Lead",
        angle="Neugier", brand="mlb_light", keyword="BIO",
        slides=[
            ("hook", "Der grösste Fehler in der Instagram-Bio von Networkerinnen?",
             "Er steht meistens schon in der ersten Zeile."),
            ("text", "Die erste Zeile beschreibt dich",
             "Mama von zwei, Networkerin, liebt Sonne und Kaffee.\n\nAlles wahr. Nur fragt niemand danach."),
            ("text", "Wer auf dein Profil kommt, fragt etwas anderes",
             "«Was bringt es mir, wenn ich hier bleibe?»"),
            ("text", "Darum gehört in die erste Zeile, wobei du hilfst",
             "Wem du hilfst, wobei und wozu.\n\nEin Satz, so wie du ihn einer Freundin sagen würdest."),
            ("text", "So kann das aussehen",
             "Vorher: «Mama · Networkerin · Wellness-Liebe»\n\nNachher: «Ich zeige Familien, wie sie gesünder kochen, ohne länger in der Küche zu stehen.»"),
            ("text", "Und die Firma?",
             "Darf drinbleiben, weiter unten oder im Highlight.\n\nSie ist dein Werkzeug. Gefolgt wird dir wegen dem, was du damit möglich machst."),
            ("text", "Der Test für heute",
             "Lies deine erste Zeile laut vor.\n\nWüsste jemand Fremdes danach, wofür man dich fragen kann? Wenn nicht, fang dort an."),
            ("cta", "Wie wirkt deine Bio auf Fremde?",
             "Kommentier BIO, dann schick ich dir den Bio-Check. Er schaut sich deine Bio an und sagt dir ehrlich, was fehlt."),
        ],
        caption=("Mama, Networkerin, liebt Sonne und Kaffee. Kommt dir die erste Zeile bekannt "
                 "vor? So steht sie in sehr vielen Profilen, und alles daran ist wahr.\n\n"
                 "Nur fragt niemand danach. Wer auf dein Profil kommt, will wissen, was es bringt, "
                 "hierzubleiben.\n\n"
                 "Darum gehört in die erste Zeile, wem du hilfst, wobei und wozu. Ein Satz, so wie "
                 "du ihn einer Freundin sagen würdest. Die Firma darf trotzdem bleiben, nur weiter "
                 "unten.",
                 CTA_BIO, TAGS_NETWORK)),
}

REELS = {
    "kw42-reel-m-mi-a": dict(
        name="A · Mi · Das Peinliche: KI-Texte umgeschrieben", datum="2026-10-14", zeit="21:00",
        job="Lead", angle="Schmerz", keyword="STIMME", video="kw42-m-mi-a",
        hook="Das Peinliche? Ich war felsenfest überzeugt, dass die KI meine Texte schreibt. Umgeschrieben hab ich sie trotzdem jedes Mal.",
        caption=("Monatelang hab ich Texte von der KI schreiben lassen und sie danach komplett "
                 "umgebaut. Jeden einzelnen. Gespart hab ich dabei genau nichts, ausser vielleicht "
                 "den Blick auf den leeren Bildschirm.\n\n"
                 "Der Grund war simpel: Die KI wusste nichts über mich. Sie kannte weder meine Sätze "
                 "noch meine Wörter, und schon gar nicht, was ich nie sagen würde. Also hat sie "
                 "geschrieben wie alle.\n\n"
                 "Seit sie das weiss, schreibe ich nicht mehr um. Ich lese, ändere hier und da ein "
                 "Wort und gebe frei.",
                 CTA_STIMME, TAGS_KI)),
    "kw42-reel-m-mi-b": dict(
        name="B · Mi · POV: ChatGPT motiviert geöffnet", datum="2026-10-14", zeit="21:00",
        job="Lead", angle="Schmerz", keyword="STIMME", video="kw42-m-mi-b",
        hook="POV: Du öffnest ChatGPT motiviert und schliesst es 20 Minuten später mit einem Text, der klingt wie ein Prospekt.",
        caption=("Du tippst «Schreib mir einen Post über Energie» und bekommst einen Text, der auch "
                 "auf einer Packung stehen könnte. Also schreibst du ihn um. Und beim nächsten Mal "
                 "wieder.\n\n"
                 "Das liegt weder an dir noch an der KI. Sie bekommt jedes Mal nur einen Satz und muss "
                 "den Rest raten, und wer raten muss, schreibt den Durchschnitt.\n\n"
                 "Fang mit einer Sache an: Gib ihr drei Texte, die du selbst geschrieben hast, und sag "
                 "dazu: So klinge ich. Allein das verändert den nächsten Entwurf.",
                 CTA_STIMME, TAGS_KI)),
    "kw42-reel-m-fr-a": dict(
        name="A · Fr · Weniger als im Büro, und kein Spruch mehr", datum="2026-10-16", zeit="21:00",
        job="Reichweite", angle="Identität", video="kw42-m-fr-a",
        hook="Unangenehme Wahrheit: Ich verdiene mit meinem Business noch weniger als früher im Büro. Und mein Mann macht trotzdem keinen Spruch mehr.",
        caption=("Ich verdiene mit meinem Business noch weniger als früher in meinem Job im Büro. "
                 "Das sag ich ganz offen, weil hier sonst fast nur Erfolgszahlen stehen.\n\n"
                 "Und trotzdem hat sich etwas verändert. Mein Mann hat lange gesagt, das sei ein "
                 "Instagram-Ding. Heute macht er keinen Spruch mehr. Überzeugt hab ich ihn nie mit "
                 "Worten. Er sieht einfach, dass ich dranbleibe, Woche für Woche.\n\n"
                 "Wenn du gerade belächelt wirst: Das hört selten mit einer Diskussion auf. Es hört "
                 "auf, wenn du es länger durchziehst, als die anderen erwartet haben.",
                 "Schick das einer Freundin im Network, die gerade belächelt wird. 💌",
                 TAGS_NETWORK)),
    "kw42-reel-m-fr-b": dict(
        name="B · Fr · POV: Familienessen", datum="2026-10-16", zeit="21:00",
        job="Reichweite", angle="Identität", video="kw42-m-fr-b",
        hook="POV: Du hoffst heimlich, dass dich beim Familienessen niemand fragt, wie es mit deinem Network läuft.",
        caption=("Irgendwann zwischen Hauptgang und Dessert kommt sie, die Frage: «Und, läuft das "
                 "noch mit deinem … wie heisst das nochmal?»\n\n"
                 "Du sagst «Es läuft so okay» und wechselst das Thema. Du schämst dich nicht mal. Du "
                 "hast einfach keine Lust, dich schon wieder zu rechtfertigen.\n\n"
                 "Leg dir für das nächste Mal einen Satz zurecht, der sagt, wobei du hilfst, und "
                 "nicht, was du verkaufst. «Ich helfe Leuten, die …» löst ein ganz anderes Gespräch "
                 "aus als der Firmenname.",
                 "Schick das der Freundin, die beim nächsten Familienessen wieder gefragt wird. 💌",
                 TAGS_NETWORK)),
    "kw42-trial-m-di": dict(
        name="Trial · Di · Keine Ausreden mehr", datum="2026-10-13", zeit="12:00",
        job="Reichweite", angle="Konträr", video="kw42-t1-di", trial=True,
        hook="Bei mir bekommst du keine Ausreden mehr für deinen Stillstand im Network. Wir finden den Weg raus oder wir lassen es.",
        caption=("Seit 2023 baue ich mein Network neu auf, und beim zweiten Mal anders als beim "
                 "ersten. Was ich dabei gelernt hab: Stillstand hat fast immer einen Grund, den man "
                 "benennen kann. Keine Zeit, kein Plan, kein Thema. Jeder davon lässt sich lösen, wenn "
                 "man ehrlich hinschaut.",
                 FOLG, TAGS_NETWORK)),
    "kw42-trial-m-mi-verlosung": dict(
        name="Trial · Mi · 🎁 Verlosung KI-Kurs", datum="2026-10-14", zeit="12:00",
        job="Reichweite", angle="Ergebnis", video="kw42-t2-mi-verlosung", trial=True,
        hook="Ich verlose einen Platz in meinem KI-Kurs. So bist du dabei: 1 · Folg mir · 2 · Kommentier, was dir die KI abnehmen soll · 3 · Teil das Reel mit einer Network-Freundin",
        caption=("🎁 Ich verlose einen Platz in meinem KI-Kurs «Easy KI für Networkerinnen».\n\n"
                 "Darin lernst du, wie die KI für dich arbeitet: mit einem eigenen Arbeitsplatz, "
                 "der dein Wissen kennt, deinem ersten festen Auftrag und einem Helfer, der sich von "
                 "selbst meldet.\n\n"
                 "So bist du dabei:\n"
                 "1. Folg mir (@mumlifebalance_patricia_ulmann)\n"
                 "2. Kommentier, welche Arbeit dir die KI als Erstes abnehmen soll\n"
                 "3. Teil das Reel mit einer Freundin, die auch im Network ist\n\n"
                 "Mitmachen kannst du bis Do 22.10.2026, 18:00. Am Abend ziehe ich die Gewinnerin in "
                 "meiner Story und schreibe ihr eine Nachricht.",
                 ("Teilnahmebedingungen: Teilnahme ab 18 Jahren, gratis und ohne Kauf. Der Gewinn "
                  "wird nicht in Geld ausbezahlt. Hat die Gewinnerin den Kurs schon gekauft, darf "
                  "sie den Platz einer Freundin schenken. Ich frage nie nach einem Passwort oder "
                  "einer Zahlung, solche Nachrichten sind gefälscht. Diese Verlosung steht in keiner "
                  "Verbindung zu Instagram und wird von Instagram weder gesponsert noch unterstützt."),
                 "#verlosung #gewinnspiel #mamabusiness #kifuermamas #mamaimnetworkmarketing")),
    "kw42-trial-m-do": dict(
        name="Trial · Do · Nicht noch mehr Tipps", datum="2026-10-15", zeit="12:00",
        job="Reichweite", angle="Konträr", video="kw42-t3-do", trial=True,
        hook="Du brauchst nicht noch mehr Tipps fürs Network. Du musst aufhören, das meiste von dem zu machen, was dich nur Zeit kostet.",
        caption=("Du hast vermutlich schon mehr gespeichert, als du je umsetzen kannst. Selten "
                 "fehlt das Wissen. Meistens fehlt die Zeit, weil sie für Dinge draufgeht, die nichts "
                 "bringen: Leute anschreiben, die nicht gefragt haben, Vorlagen umschreiben, Beiträge "
                 "ohne Plan.\n\nStreich eine davon diese Woche. Nur eine.",
                 FOLG, TAGS_NETWORK)),
    "kw42-trial-m-fr": dict(
        name="Trial · Fr · Kein Wundermittel", datum="2026-10-16", zeit="12:00",
        job="Reichweite", angle="Identität", video="kw42-t4-fr", trial=True,
        hook="Ich bin nicht diejenige, die dir fürs Network das nächste Wundermittel verspricht.",
        caption=("Kein Wundermittel, kein Geheimtrick, keine sechsstelligen Versprechen. Bei mir "
                 "gibt es vier Kinder, rund 18 Stunden Arbeit pro Woche und ein Business, das ich "
                 "Schritt für Schritt aufgebaut hab, mit Umwegen.\n\n"
                 "Wenn du genau das suchst, bist du hier richtig.",
                 FOLG, TAGS_NETWORK)),
}


def main():
    (AUS / "karussells").mkdir(parents=True, exist_ok=True)
    (AUS / "reels").mkdir(parents=True, exist_ok=True)
    md = ["---", "tags: [content, mentoring]", "---", "",
          "# Beiträge Mentoring 13.–16.10.2026", "",
          "Erzeugt von `scripts/content/kw42-beitraege.py`. Hooks: [[hooks]] · Markt: [[markt]].", ""]
    for kid, k in KARUSSELLS.items():
        d = leer()
        d.update(name=k["name"], datum=k["datum"], typ=k["typ"], funnel=k["funnel"],
                 job=k["job"], angle=k["angle"], brand=k["brand"],
                 caption=cap(*k["caption"]),
                 hinweis="KW42 neu (12.10.) · Variante %s · ersetzt die alte Launch-Fassung nicht automatisch — du wählst." % k["name"][0],
                 blotato={"status": "", "datum": k["datum"], "zeit": k["zeit"], "profil": "mentoring"},
                 slides=[])
        for layout, head, body in k["slides"]:
            s = {"layout": layout, "headline": head, "body": body}
            if layout == "cta" and k.get("keyword"):
                s["keyword"] = k["keyword"]
            d["slides"].append(s)
        assert len(d["slides"]) <= 10, kid
        (AUS / "karussells" / f"{kid}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        md += [f"## {k['name']} — {k['datum']} {k['zeit']}", "",
               f"Typ {k['typ']} · {k['funnel']} · {k['job']}", ""]
        for i, (layout, head, body) in enumerate(k["slides"], 1):
            md.append(f"{i}. **{head}**" + (f" — {body}".replace("\n\n", " / ") if body else ""))
        md += ["", "**Caption**", "", d["caption"], ""]
    for rid, r in REELS.items():
        d = leer()
        trial = r.get("trial")
        d.update(name=r["name"], datum=r["datum"], job=r["job"], angle=r["angle"],
                 brand="mlb_dark", hook=r["hook"], caption=cap(*r["caption"]),
                 videoart="broll", coverhook=r["hook"].split("?")[0] + ("?" if "?" in r["hook"] else ""),
                 coverunter="", coverfarbe="orange", pos="unten", scrim=True, textskala=100, texty=68,
                 unter="", untertitel="", videodatei=f"{r['video']}.mp4", videourl="",
                 skript="B-ROLL, gebaut von Claude (video/output/broll/%s). Musik wählst du in der App." % r["video"],
                 blotato={"status": "", "zeit": r["zeit"]},
                 hinweis=("🧪 TRIAL REEL — beim Posten in der App „Testreel“ einschalten, damit es nur "
                          "Nicht-Followerinnen sehen. " if trial else "") + "KW42 neu (12.10.)")
        (AUS / "reels" / f"{rid}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        md += [f"## {r['name']} — {r['datum']}", "", f"**Hook im Video:** {r['hook']}", "",
               "**Caption**", "", d["caption"], ""]
    MD.write_text("\n".join(md), encoding="utf-8")
    print(f"{len(KARUSSELLS)} Karussells, {len(REELS)} Reels -> {AUS}")


if __name__ == "__main__":
    main()
