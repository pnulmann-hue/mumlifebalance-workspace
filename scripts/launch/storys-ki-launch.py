"""
Story-Gerüst für den KI-Kurs-Launch (28.09.–23.10.2026) — fertig vorgeschrieben,
damit Patricia nur noch den Alltag ergänzt.

  python scripts/launch/storys-ki-launch.py
  # danach: ArtifactData batch set (Cockpit, Sammlung "storys") mit den Dateien in
  #         outputs/cockpit/abgleich/launch-storys/cockpit/
  #         und daten/entwuerfe im Bild-Editor um die Einträge aus
  #         outputs/cockpit/abgleich/launch-storys/bild-editor.json ergänzen

Aufbau je Tag nach der Launch-Mechanik (Aufwärmen · Secret Offer · Verkauf ·
Masterclass · Preis steigt · letzter Tag) und dem Wochenrhythmus aus
outputs/produkte/ki-treppe/07-launch-kalender.md:
Mo lehrreich · Di persönlich · Mi Inspiration · Do Blick in den Kurs ·
Fr eigene Meinung · Sa/So eine Slide.

✏️ = Stelle für den Alltag von heute. Vor dem Posten ersetzen oder löschen.
🚨 Nichts behaupten, was nicht passiert ist („die ersten sind drin“ nur, wenn
   jemand gekauft hat; keine erfundenen Kundenstimmen).
"""
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
ZIEL = ROOT / "outputs" / "cockpit" / "abgleich" / "launch-storys"

LINK_STIMME = "Link-Sticker Stimm-Check (sobald live) · sonst Stichwort STIMME per DM"
LINK_KURS = "Link-Sticker: mumlifebalance.ch/ki-kurs/"
LINK_MC = "Link-Sticker: Anmeldung Masterclass (Adresse folgt)"
MBA = "Bist du in der MBA? Dann hast du ihn schon gratis."


def t(text, unter=""):
    return {"layout": "text", "text": text, "cta": unter}


def bild(text, unter=""):
    return {"layout": "bild", "text": text, "cta": unter}


def frage(text, sticker="Frage-Sticker"):
    return {"layout": "frage", "text": text, "cta": sticker}


def umfrage(text, a, b):
    return {"layout": "umfrage", "text": text, "cta": "Umfrage", "optA": a, "optB": b}


def cta(text, link, klein=""):
    return {"layout": "cta", "text": text + (("\n\n" + klein) if klein else ""), "cta": link}


# --- Bausteine der Story-Bibliothek (seit 08.10.2026) ---------------------
# Jede Folie bringt ihre Gestaltung mit; der Cockpit-Zeichner nimmt sonst die
# Vorgabe des Layouts. `notiz` steht nur auf der Karte, nie im Bild.
# Sticker werden nie gezeichnet, nur ihr Platz freigehalten.
def foto(text, datei, klein="", notiz="", **stil):
    return dict({"layout": "bild", "text": text, "klein": klein, "foto": datei, "hg": "foto", "notiz": notiz}, **stil)


def learning(text, eyebrow="Zum Screenshotten", klein="", **stil):
    return dict({"layout": "learning", "eyebrow": eyebrow, "text": text, "klein": klein}, **stil)


def kurs(eyebrow, titel, punkte, klein="", **stil):
    return dict({"layout": "kurs", "eyebrow": eyebrow, "text": titel, "punkte": punkte, "klein": klein}, **stil)


def bonus(pille, text, klein="", sticker="countdown", stickerText="", **stil):
    return dict({"layout": "bonus", "pille": pille, "text": text, "klein": klein,
                 "sticker": sticker, "stickerText": stickerText}, **stil)


def platz(layout, text, sticker, stickerText, klein="", notiz="", **stil):
    return dict({"layout": layout, "text": text, "klein": klein, "sticker": sticker,
                 "stickerText": stickerText, "notiz": notiz}, **stil)


TAGE = [
    # ---------------- KW40 · Aufwärmen, noch kein Angebot ----------------
    ("2026-09-28", "Mo", "Aufwärmen", "lehrreich", "Warum deine KI-Texte nach niemandem klingen", [
        bild("✏️ Dein Montagmorgen heute, ein Satz dazu.\nUnd dann eine Frage, die mich seit Wochen beschäftigt."),
        t("Alle sagen, KI spart Zeit. Bei den meisten Frauen, mit denen ich rede, kostet sie welche, weil sie jeden Text danach umbauen."),
        t("Das liegt fast immer an denselben drei Dingen: Die KI weiss nicht, wer du bist, für wen du schreibst und wie du redest."),
        t("Ein Satz genügt schon als Anfang: Schreib ihr vor jedem Auftrag, für wen der Text ist und in welchem Ton, so wie du es einer Freundin erklären würdest."),
        frage("Wie oft baust du einen KI-Text um, bevor du ihn postest?"),
        cta("Wenn du wissen willst, welche sechs Angaben deine KI von dir braucht, damit sie klingt wie du:", LINK_STIMME),
    ]),
    ("2026-09-29", "Di", "Aufwärmen", "persönlich", "Mein Morgen, bevor die Bots da waren", [
        bild("✏️ Foto von heute Morgen: Küche, Kaffee, Ferienmorgen."),
        t("Früher sah mein Morgen so aus: Kinder parat machen, nebenbei am Handy überlegen, was ich heute poste, und am Abend war der Beitrag immer noch nicht fertig."),
        t("Heute schickt mir mein Cockpit-Bot um halb sieben, was ansteht. Die Vorarbeit hat die KI in der Nacht gemacht, ich schaue drüber und gebe frei."),
        t("Dahinter steckt ein Arbeitsplatz, den ich mir Stück für Stück eingerichtet habe, mit vier Kindern und achtzehn Stunden Arbeitszeit in der Woche."),
        umfrage("Wie läuft dein Morgen gerade?", "Chaos", "Geht so"),
        cta("Am Donnerstag, 8. Oktober, um neun zeig ich dir das live, kostenlos und mit Aufzeichnung.", LINK_MC),
    ]),
    ("2026-09-30", "Mi", "Aufwärmen", "Inspiration", "Was sich bei mir verändert hat", [
        bild("✏️ Ein Bild von heute, bei dem du nicht am Handy sitzt."),
        t("Wenn ich eine Sache in diesem Jahr anders machen würde, dann die: früher anfangen, die Arbeit, die jede Woche wiederkommt, an die KI abzugeben."),
        t("Gemeint ist das Wiederkehrende: die erste Fassung einer Caption, den Wochenplan, die Antwort auf die DM, die ich zum zehnten Mal schreibe."),
        t("Seitdem geht mir das Posten nicht mehr am Abend nach, wenn die Kinder im Bett sind. Das ist für mich der grösste Unterschied."),
        frage("Welche Arbeit machst du jede Woche wieder von vorn?"),
        cta("Schick mir deine Antwort, ich lese alles.", "Frage-Sticker"),
    ]),
    ("2026-10-01", "Do", "Aufwärmen", "Blick hinter die Kulissen", "Da kommt was", [
        bild("✏️ Blick auf deinen Schreibtisch oder Bildschirm, gern unscharf — man soll neugierig werden, nicht alles sehen."),
        t("Ich arbeite seit dem Sommer an etwas, das ich mir gewünscht hätte, als ich angefangen habe."),
        t("Es geht darum, wie deine KI vom Chat, dem du alles erklären musst, zu einer Mitarbeiterin wird, die die Vorarbeit macht."),
        t("Nächste Woche zeig ich es den Ersten. Wer auf meiner Warteliste steht, sieht es zuerst."),
        frage("Was würdest du deiner KI als Erstes abgeben?"),
        cta("Countdown bis Montag, 7 Uhr", "Countdown-Sticker · Mo 5.10. 07:00"),
        cta("Und am Donnerstag, 8. Oktober, um neun zeig ich dir live, wie das bei mir aussieht.", LINK_MC),
    ]),
    ("2026-10-02", "Fr", "Aufwärmen", "eigene Meinung", "Prompt-Listen helfen dir nicht", [
        bild("✏️ Du, direkt in die Kamera oder ein Foto von dir."),
        t("Ich sag's heute mal gerade heraus: Die dreissigste gespeicherte Prompt-Liste bringt dich keinen Schritt weiter."),
        t("Eine Liste kennt dich nicht. Sie weiss nicht, für wen du schreibst, wie du redest und was du letzte Woche gepostet hast, also fängst du jedes Mal bei null an."),
        t("Was hilft, ist ein Ort, an dem dein Wissen einmal liegt und den die KI jedes Mal liest, bevor sie für dich schreibt."),
        umfrage("Wie viele gespeicherte Prompt-Listen hast du?", "Zu viele", "Keine"),
        cta("Am Montag zeig ich dir, wie das bei mir aussieht.", "Countdown-Sticker · Mo 5.10. 07:00"),
    ]),
    ("2026-10-03", "Sa", "Aufwärmen", "eine Slide", "Erste Ferienwoche", [
        bild("✏️ Ferienbild von heute.\n\nDie erste Ferienwoche ist fast rum, und am Montag öffne ich etwas, worauf ich mich seit Wochen freue.", "Countdown-Sticker · Mo 5.10. 07:00"),
    ]),
    ("2026-10-04", "So", "Aufwärmen", "eine Slide", "Morgen früh", [
        bild("✏️ Sonntagsbild.\n\nMorgen um sieben zeig ich es zuerst den Frauen, die sich gemeldet haben. Tipp auf den Sticker, dann bist du dabei.", "Sticker „Ich will's zuerst sehen“ → DM"),
    ]),
    # ---------------- KW41 · Secret Offer · Frühbucherin (Herbstferien) ----------------
    ("2026-10-05", "Mo", "Secret Offer", "Secret Offer", "Secret Offer geht auf", [
        t("Ich hab seit Juli an etwas gebaut, und du bist eine der Ersten, die es sieht."),
        t("Es ist der Kurs, in dem du dir deinen eigenen KI-Arbeitsplatz einrichtest, so wie ich meinen."),
        t("Am Ende hast du drei Dinge: einen Arbeitsplatz mit deinem Wissen drin, deinen ersten eigenen Skill und einen Bot, der von selbst läuft."),
        t("Die ersten 48 Stunden gibt es ihn zum tiefsten Preis, den er je haben wird, und dazu einen Abend, an dem wir alles zusammen einrichten."),
        cta("Tipp auf den Sticker, dann schick ich dir den Link.", "Sticker „Tipp für den Preis“ → DM mit Secret-Link (kein Link in der Story)", MBA),
    ]),
    ("2026-10-06", "Di", "Secret Offer", "Secret Offer", "Noch bis morgen früh", [
        bild("✏️ Ferienalltag von heute, ein Satz dazu."),
        t("Viele sagen mir: „Ich hab ja schon ChatGPT.“ Ich auch, und genau deshalb weiss ich, wie viel Zeit es kostet, wenn man ihm jeden Montag wieder erklärt, wer man ist."),
        t("Im Kurs richtest du einmal einen Ort ein, an dem dein Wissen liegt. Danach liest die KI das jedes Mal selbst, bevor sie für dich arbeitet."),
        cta("Der Secret-Preis gilt bis morgen um sieben.", "Sticker „Tipp für den Preis“ → DM", MBA),
        cta("Übermorgen um neun zeig ich dir live, wie die KI bei mir mitarbeitet. Kostenlos, mit Aufzeichnung.", LINK_MC),
    ]),
    ("2026-10-07", "Mi", "Frühbucherin", "Frühbucherin", "Ab heute für alle", [
        t("✏️ Nur wenn es stimmt: „Seit Montag ist er offen, und die ersten Frauen sind drin.“ Sonst: „Seit heute kann jede rein.“"),
        t("Er ist für dich, wenn du KI schon benutzt, aber jeden Text umbaust."),
        t("Was sich ändert: Die KI macht die Vorarbeit, und du schaust drüber und gibst frei."),
        t("Ganz ehrlich: Der Kurs entsteht noch. Ab dem 1. November kommen die Kapitel, und dafür gibt es bis zum 15. Oktober den Frühbucherpreis."),
        cta("Alles zum Kurs hinter dem Link.", LINK_KURS, MBA),
        cta("Und morgen um neun zeig ich dir live, wie mein Freitagmorgen mit der KI läuft. Kostenlos, mit Aufzeichnung.", LINK_MC),
    ]),
    ("2026-10-08", "Do", "Frühbucherin", "Masterclass", "Masterclass heute um neun", [
        t("Heute um neun zeig ich dir live, wie mein Freitagmorgen läuft."),
        t("Du siehst alles vom Wochenplan bis zum fertigen Beitrag, ungeschnitten: mein Cockpit, meine Assistenten, wie ein Skill entsteht, und den Kochbot, der mir die Menüplanung abnimmt."),
        t("Es geht darum, was möglich ist, wenn deine KI dich kennt und weiss, was zu tun ist."),
        frage("Was willst du heute sehen?"),
        cta("Hier kannst du dich noch anmelden. Wer nicht live kann, bekommt die Aufzeichnung am Nachmittag.", LINK_MC, "MBA-Frauen: Kommt gern, den Kurs habt ihr schon."),
    ]),

    # 🚨 Der Abend des 8.10. (nach der Masterclass) steht NICHT hier, sondern im
    # Cockpit-Dokument storys/kw41-story-m-ki-do, Folien 7–16 — von der Sitzung
    # „KI Kurs“ mit echten Kundinnen-Sätzen geschrieben und am 08.10. mit den
    # Bausteinen oben gestaltet. Ein Neulauf dieses Skripts darf es nicht überschreiben.

    ("2026-10-09", "Fr", "Frühbucherin", "nach der Masterclass", "Was gestern passiert ist", [
        bild("✏️ Screenshot oder Foto von gestern (ohne Gesichter der Teilnehmerinnen)."),
        t("✏️ Ein Satz zu gestern, wie es war."),
        t("Das Wichtigste in Kürze: Deine KI muss dich kennen und wissen, was zu tun ist. Dann fängst du nicht jede Woche wieder bei null an."),
        t("Die Aufzeichnung ist gestern Nachmittag per Mail rausgegangen. Wer bis morgen Abend um neun einsteigt, ist zusätzlich beim Bonus-Call am 21. Januar dabei."),
        cta("Aufzeichnung und Kurs:", LINK_KURS, MBA),
    ]),

    ("2026-10-10", "Sa", "Frühbucherin", "eine Slide", "Bonus bis heute Abend", [
        bild("✏️ Ferienbild.\n\nHeute Abend um neun endet der Bonus: Wer bis dann einsteigt, ist beim dritten Live-Call am 21. Januar dabei.", LINK_KURS),
    ]),

    ("2026-10-11", "So", "Frühbucherin", "eine Slide", "Frühbucherpreis bis Donnerstag", [
        bild("✏️ Sonntagsbild.\n\nNoch bis Donnerstag gibt es den Kurs zum Frühbucherpreis.", LINK_KURS),
    ]),

    # ---------------- KW42 · Frühbucherin · Preis steigt ----------------
    ("2026-10-12", "Mo", "Frühbucherin", "lehrreich", "Die drei Zutaten eines Auftrags", [
        bild("✏️ Montag in den Ferien, ein Satz dazu."),
        t("Ein kleiner Handgriff zum Mitnehmen: Jeder gute KI-Auftrag hat drei Zutaten."),
        t("Erstens, wer du bist und für wen du schreibst. Zweitens, was genau am Ende dastehen soll. Drittens, woran du merkst, dass es gut ist, zum Beispiel „kein Satz länger als zwei Zeilen“."),
        t("Probier es heute mit einem einzigen Text aus. Du wirst merken, wie viel weniger du danach umbauen musst."),
        cta("Bis Donnerstag zum Frühbucherpreis:", LINK_KURS, MBA),
    ]),
    ("2026-10-13", "Di", "Frühbucherin", "Blick in den Kurs", "Was genau drin ist", [
        t("Heute für alle, die es genau wissen wollen: Was steckt eigentlich drin?"),
        t("Zehn Kapitel, jede Lektion acht bis fünfzehn Minuten, mit geteiltem Bildschirm."),
        t("Du fängst im Chat an, den du kennst, und lernst, wie ein guter Auftrag aussieht. Danach kommt Cowork mit deinem ersten Bot, ganz ohne Code, und erst dann dein eigener Arbeitsplatz."),
        t("Dort baust du deinen ersten eigenen Skill und einen Telegram-Bot. Und im letzten Kapitel schaust du mir zu, wie bei mir vom Freitagmorgen bis zum fertigen Beitrag alles zusammenhängt."),
        frage("Was willst du über den Kurs noch wissen?"),
        cta("Frühbucherpreis bis 15. Oktober.", LINK_KURS, MBA),
    ]),

    ("2026-10-14", "Mi", "Frühbucherin", "Inspiration", "Ferien und trotzdem läuft's", [
        bild("✏️ Ferienmoment mit den Kindern."),
        t("✏️ Nur wenn es stimmt: „Die Kinder sind zu Hause, und trotzdem ist heute ein Beitrag rausgegangen, ohne dass ich am Abend noch am Handy sass.“"),
        t("Genau dafür hab ich mir den Arbeitsplatz gebaut: damit die Arbeit weiterläuft, wenn ich gerade woanders gebraucht werde."),
        cta("Wenn du das auch willst:", LINK_KURS, MBA),
    ]),

    ("2026-10-15", "Do", "Frühbucherin", "Einwände", "Morgen steigt der Preis", [
        t("Heute um Mitternacht endet der Frühbucherpreis. Deshalb heute die drei Sätze, die ich in den letzten Tagen am häufigsten gehört habe."),
        umfrage("Welcher davon ist deiner?", "Zu technisch", "Keine Zeit"),
        t("„Zu technisch“: Du fängst im Chat an, den du kennst, und installierst erst in Kapitel 4 etwas, über die Desktop-App, ohne schwarzes Fenster."),
        t("„Keine Zeit“: Die Lektionen dauern acht bis fünfzehn Minuten, und alles, was du einrichtest, nimmt dir danach jede Woche Arbeit ab."),
        t("✏️ Die dritte Frage aus deinen DMs dieser Woche, mit deiner Antwort — nur eine, die wirklich gestellt wurde."),
        cta("Bis heute Nacht zum Frühbucherpreis.", LINK_KURS, MBA),
    ]),
    ("2026-10-16", "Fr", "voller Preis", "voller Preis", "Eine Woche noch", [
        t("Ab heute kostet er 333, und nächsten Freitag geht die Kasse zu."),
        t("Warum sie zugeht: Ich öffne sie erst wieder, wenn alle Kapitel online sind."),
        t("✏️ Die häufigste Frage der Woche aus deinen DMs und deine Antwort darauf."),
        t("Im ersten Kapitel musst du nichts installieren. Du arbeitest im Chat, den du kennst, und lernst, wie ein Auftrag aussieht, der beim ersten Mal sitzt."),
        cta("Alles zum Kurs:", LINK_KURS, MBA),
    ]),
    ("2026-10-17", "Sa", "voller Preis", "eine Slide", "Letztes Ferienwochenende", [
        bild("✏️ Wochenendbild.\n\nNoch sechs Tage, dann geht die Kasse für den KI-Kurs zu.", LINK_KURS + " · " + MBA),
    ]),
    ("2026-10-18", "So", "voller Preis", "eine Slide", "Wer schon dabei ist", [
        bild("✏️ Nur wenn es stimmt: „So viele Frauen richten sich ab November mit mir ihren Arbeitsplatz ein — ich freu mich riesig.“ Sonst: „Noch fünf Tage.“", LINK_KURS),
    ]),
    # ---------------- KW43 · voller Preis · Kasse zu ----------------
    ("2026-10-19", "Mo", "voller Preis", "für wen", "Ist das was für mich?", [
        bild("✏️ Erster Schultag nach den Ferien, ein Satz dazu."),
        t("Heute ganz ehrlich: Für wen ist der Kurs nichts?"),
        t("Wenn du KI noch nie benutzt hast und das auch nicht willst, dann ist er nichts für dich. Und wenn du erwartest, dass die KI dein Business ohne dich führt, auch nicht."),
        t("Er ist für dich, wenn du KI schon benutzt und merkst, dass sie dich mehr Zeit kostet, als sie dir spart."),
        frage("Unsicher, ob er zu dir passt? Schreib mir, ich sag's dir ehrlich."),
        cta("Noch bis Freitag.", LINK_KURS, MBA),
    ]),
    ("2026-10-20", "Di", "voller Preis", "persönlich", "Als ich investiert habe", [
        bild("✏️ Ein Foto von dir."),
        t("✏️ Deine eigene Geschichte: Wann hast du zuletzt in etwas investiert, bei dem du vorher gezögert hast? Was war die Angst, und was ist danach passiert?"),
        t("Ich weiss deshalb, wie sich dieses Zögern anfühlt. Und ich weiss auch, dass ich die Dinge, die mir heute jeden Tag Zeit sparen, ohne diesen Schritt nicht hätte."),
        cta("Wenn du gerade an diesem Punkt stehst:", LINK_KURS, MBA),
    ]),
    ("2026-10-21", "Mi", "voller Preis", "liebevolle Strenge", "Was „irgendwann“ kostet", [
        t("Weisst du, was ich am längsten vor mir hergeschoben habe? Genau das hier: mir die wiederkehrende Arbeit abnehmen zu lassen."),
        t("✏️ Ein Satz dazu, was dich das damals gekostet hat, zum Beispiel wie viele Abende am Handy."),
        t("Wenn du weiter jeden Text von Hand machst, bleibt es genau so, wie es jetzt ist. Das ist keine Katastrophe, aber es kostet dich jede Woche dieselben Stunden."),
        t("Nimmst du dir die drei Wochen im November, sitzt du danach nicht mehr bei jedem Beitrag bei null."),
        cta("Noch zwei Tage.", LINK_KURS, MBA),
    ]),
    ("2026-10-22", "Do", "voller Preis", "Fakten", "Morgen geht die Kasse zu", [
        t("Morgen um Mitternacht geht die Kasse zu. Deshalb heute alles auf einen Blick."),
        t("Zehn Kapitel ab dem 1. November, Lektionen von acht bis fünfzehn Minuten, dazu die Vorlagen für deinen Arbeitsplatz, deine Skills und deinen Bot."),
        t("Am Ende hast du einen Arbeitsplatz mit deinem Wissen, deinen ersten eigenen Skill und einen Bot, der von selbst läuft."),
        frage("Was hält dich noch zurück?"),
        cta("333 Franken, bis morgen Nacht.", LINK_KURS, MBA),
    ]),
    ("2026-10-23", "Fr", "voller Preis", "letzter Tag", "Heute um Mitternacht", [
        t("Heute um Mitternacht geht die Kasse zu, und ich mach sie erst wieder auf, wenn der Kurs fertig ist."),
        t("Er passt zu dir, wenn du KI schon benutzt und jeden Text umbaust. Er passt nicht, wenn du dir wünschst, dass die KI alles ohne dich macht."),
        t("Am 1. November richtest du als Erstes deinen Arbeitsplatz ein, und ich bin dabei."),
        bild("✏️ Dein ehrlicher Satz zum Schluss, frei gesprochen in die Kamera."),
        cta("Fragen beantworte ich noch bis 23 Uhr.", LINK_KURS, MBA),
    ]),
]

VERBOTEN = [
    (r"[Ss]tell dir\b[^.!?]{0,60}\bvor\b|[Ss]tell dir vor", "„Stell dir vor“"),
    (r"[Nn]icht[^.!?]{0,80}[,.]\s*[Ss]ondern", "„Nicht …, sondern …“"),
    (r"ß", "ß statt ss"),
    (r"\b(ae|oe|ue)\w*", None),
]


def pruefen():
    funde = []
    for datum, _, _, _, name, frames in TAGE:
        for f in frames:
            s = " ".join(str(f.get(k, "")) for k in ("text", "klein", "pille", "eyebrow")) + " " + " ".join(f.get("punkte", []))
            for muster, was in VERBOTEN[:3]:
                if re.search(muster, s):
                    funde.append(f"{datum} {name}: {was} — {s[:60]}")
    return funde


def main():
    funde = pruefen()
    if funde:
        print("\n".join(funde))
        sys.exit("Verbotene Formulierungen gefunden — erst korrigieren.")
    (ZIEL / "cockpit").mkdir(parents=True, exist_ok=True)
    entwuerfe = []
    for datum, tag, phase, typ, name, frames in TAGE:
        kennung = "kw%s-story-m-ki-%s" % (_kw(datum), re.sub(r"[^a-z0-9]+", "-", tag.lower()))
        doc = {
            "brand": "mlb_light", "datum": datum, "profil": "mentoring", "textfrei": False,
            "name": f"{tag} · KI-Launch · {name}",
            "hinweis": f"KI-Launch · Phase: {phase} · Story-Art: {typ} · ✏️ = Alltag von heute ergänzen oder löschen. Gerüst aus scripts/launch/storys-ki-launch.py",
            "updatedAt": "2026-09-25T15:00:00.000Z",
            "frames": [dict({"id": f"s{i+1}", "optA": "", "optB": ""}, **f) for i, f in enumerate(frames)],
        }
        (ZIEL / "cockpit" / f"{kennung}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        entwuerfe.append({
            "art": "story", "format": "story", "id": kennung, "name": doc["name"], "datum": datum,
            "profil": "mentoring", "cta": frames[-1].get("cta", ""),
            "folien": [{"text": f["text"],
                        "unter": (f"{f['optA']} / {f['optB']}" if f.get("optA") else f.get("cta", ""))}
                       for f in frames],
        })
        print(f"  {kennung}  {len(frames)} Slides  {name}")
    (ZIEL / "bild-editor.json").write_text(json.dumps(entwuerfe, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(TAGE)} Tage · {sum(len(x[5]) for x in TAGE)} Slides")


def _kw(datum):
    import datetime
    return datetime.date.fromisoformat(datum).isocalendar()[1]


if __name__ == "__main__":
    main()
