"""
Storys 26.10.–30.11.2026 für beide Profile — fertig vorgeschrieben und gestaltet,
damit Patricia nur noch den Alltag ergänzt. Zwilling von storys-ki-launch.py.

  python scripts/launch/storys-november.py
  # danach: ArtifactData batch set (Cockpit, Sammlung "storys") mit den Dateien in
  #         outputs/cockpit/abgleich/storys-november/

Neu festgelegt mit Patricia am 26.10.2026 (Monatsplan outputs/monatsplaene/2026-11-*.md),
nachdem die Fassung vom 25.10. (Story-Challenge → Kundenmaschine) verworfen wurde:
„ich habe schon so lange immer über instagram geredet … mein hybridmodell (was mich ja
von der konkurrenz abhebt, kommt kaum zum tragen)“.

Mentoring  KW44 Hybridmodell · KW45 Einladung Lead-Challenge · 9.–11.11. Lead-Challenge
           (WhatsApp-Gruppe) · 12.–22.11. Community + Blick in die Digitale Produktwelt ·
           23.–30.11. Kasse Digitale Produktwelt 333, ohne Webinar.
doTERRA    kein Verkauf: aktivieren, Vertrauen, Community („ich habe den account in letzter
           zeit vernachlässigt“). Nur samstags der Gratis-Kickstart, sonst Fragen und Tipps.

Wochenrhythmus wie beim KI-Launch: Mo lehrreich · Di persönlich · Mi Inspiration ·
Do Blick hinter die Kulissen / Business · Fr eigene Meinung · Sa/So eine Folie.

✏️ = Stelle für den Alltag von heute. Vor dem Posten ersetzen oder löschen.
🚨 Nichts behaupten, was nicht passiert ist. Szenen aus Patricias Leben nur aus dem
   Workspace (Chronologie, Ursprungsgeschichte, Energie-Story, Workbook), sonst ✏️.
🚨 Mentoring: die Kundschaft ihrer Kundinnen heisst nie „deine Kundin“.
🚨 doTERRA: keine Wirkversprechen, nur „bei mir“.
"""
import datetime
import importlib.util
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
ZIEL = ROOT / "outputs" / "cockpit" / "abgleich" / "storys-november"


def _laden(name, pfad):
    spec = importlib.util.spec_from_file_location(name, ROOT / pfad)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


KI = _laden("storys_ki", "scripts/launch/storys-ki-launch.py")
GESTALT = _laden("storys_gestalten", "scripts/launch/storys-gestalten.py")
PRUEF = _laden("texte_pruefen", "scripts/cockpit/texte-pruefen.py")
t, bild, frage, umfrage, cta = KI.t, KI.bild, KI.frage, KI.umfrage, KI.cta

LINK_LEAD = "Link-Sticker: mumlifebalance.ch/lead-challenge/"
LINK_IDEEN = "Link-Sticker: mumlifebalance.ch/produkt-ideen-finder/"
LINK_DPW = "Link-Sticker: mumlifebalance.thrivecart.com/digitale-produktwelt/"
LINK_KICK = "Link-Sticker: mumlifebalance.ch/energie-kickstart/"
WARTELISTE = "Sticker „Ich will dabei sein“ → DM"
CD_ANMELDUNG = "Countdown-Sticker · Mo 2.11. 07:00"
CD_KASSE = "Countdown-Sticker · Mo 23.11. 07:00"
FRAGE = "Frage-Sticker"
LINK_NISCHE = "Link-Sticker: Nischengenerator https://mumlifebalance.ch/nischengenerator/"
LINK_WS = "Link-Sticker: ✏️ Link zur Anmeldung Tool-Workshop"


FOTOS = {"mentoring": ["s04.jpg", "s03.jpg", "s01.jpg", "s05.jpg", "s02.jpg", "s06.jpg"],
         "doterra": ["s09.jpg", "s11.jpg", "s07.jpg", "s12.jpg", "s08.jpg", "s10.jpg"]}
BRAND = {"mentoring": "mlb_light", "doterra": "oele"}

# (datum, tag, phase, story-art, gibt-ihr-mit, titel, folien)
MENTORING = [
    # ---------------- KW44 · Inspiration: das Hybridmodell ----------------
    ("2026-10-26", "Mo", "Inspiration", "lehrreich", "einen krassen Tipp", "Etwas Eigenes neben dem Network", [
        bild("✏️ Dein Montagmorgen.\n\nHeute eine Frage, die ich mir viel früher hätte stellen sollen."),
        t("Was davon gehört eigentlich mir? Die Bestellungen laufen über die Firma, die Provision kommt von der Firma, und meine Seite gehört der Plattform."),
        t("Mein Weg da raus heisst Hybridmodell: zwei Einkommensströme, die sich gegenseitig verstärken. Das Network auf der einen Seite und ein eigenes kleines Produkt auf der anderen."),
        t("Zum Screenshotten\n\nSchreib dir heute drei Fragen auf, die dir immer wieder gestellt werden. Das ist der Anfang von deinem eigenen Produkt."),
        umfrage("Hast du neben dem Network etwas Eigenes?", "Ja, schon", "Noch nicht"),
        cta("Am 9. November zeig ich dir in drei Tagen, wie du dein erstes eigenes Freebie baust. Gratis.", WARTELISTE),
    ]),
    ("2026-10-27", "Di", "Inspiration", "persönlich", "warum mit mir", "Die Liste für meinen Mann", [
        bild("✏️ Ein Foto von dir.\n\nWie bei mir alles angefangen hat, erzähl ich dir heute mal von vorn."),
        t("Vor der Geburt meiner dritten Tochter hab ich meinem Mann eine Liste geschrieben. Alles, was ich als Mama nebenbei erledige, damit er weiss, was läuft, wenn ich im Spital bin."),
        t("Aus dieser Liste ist mein erstes eigenes Angebot entstanden: die drei Schritte, um deine To-do-Liste zu halbieren. 30 Bestellungen in zwei Tagen."),
        t("Über dieses Angebot kam ich mit Mamas ins Gespräch, die mich vorher nicht kannten. Und erst dann kamen die Öle zur Sprache."),
        frage("Wie bist du zu deinem Network gekommen?"),
        cta("Genau so ein erstes eigenes Angebot bauen wir am 9. November zusammen. Tipp auf den Sticker.", WARTELISTE),
    ]),
    ("2026-10-28", "Mi", "Inspiration", "Inspiration", "Inspiration", "Das Produkt öffnet die Tür", [
        bild("✏️ Ein Bild von heute, gern ohne Handy."),
        t("Was mir damals passiert ist, sehe ich heute bei vielen: Über das Produkt aus dem Network kommt kaum jemand ins Gespräch, über ein eigenes Thema schon."),
        t("Mit meinem To-do-Angebot hab ich nie über Öle geredet. Ich hab über Alltag und Zeit geredet, und die Leute haben gefragt, wie ich das mit vier Kindern schaffe."),
        t("Heute ausprobieren\n\nPoste eine Story zu deinem Thema, ohne dein Produkt zu zeigen. Nur ein Tipp aus deinem Alltag. Schau, wer antwortet."),
        cta("Schick mir deine Story, wenn du's probiert hast. Ich schau sie mir an.", FRAGE),
    ]),
    ("2026-10-29", "Do", "Inspiration", "Blick hinter die Kulissen", "einen krassen Tipp", "Welche Idee steckt in dir?", [
        bild("✏️ Blick auf deinen Schreibtisch oder Bildschirm, gern unscharf."),
        t("Die häufigste Antwort, wenn ich frage, warum jemand noch kein eigenes Produkt hat: Ich weiss gar nicht, was ich anbieten soll."),
        t("Dafür hab ich mir einen Helfer gebaut, den Produkt-Ideen-Finder. Du beantwortest ein paar Fragen zu dir und bekommst Ideen, die zu deinem Wissen passen."),
        umfrage("Was hält dich bei einem eigenen Produkt am meisten zurück?", "Keine Idee", "Keine Zeit"),
        cta("Probier ihn aus, er ist gratis:", LINK_IDEEN),
    ]),
    ("2026-10-30", "Fr", "Inspiration", "eigene Meinung", "warum mit mir", "Mehr bestellen ist kein Business", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Ich sag's heute mal gerade heraus: Wenn du am Ende des Monats kaum mehr verdienst, als du selbst bestellst, hast du ein teures Hobby."),
        t("Ich meine das nicht böse, ich kenne das von mir selbst. 2018 hab ich mit viel Hoffnung und wenig Klarheit angefangen."),
        t("Erst als ich aufgehört habe, das Produkt in den Vordergrund zu stellen, und mein eigenes Thema gefunden habe, lief es wirklich."),
        umfrage("Wie ist es bei dir gerade?", "Hobby", "Business"),
        cta("Am Montag geht die Anmeldung für meine Gratis-Challenge auf.", CD_ANMELDUNG),
    ]),
    ("2026-10-31", "Sa", "Inspiration", "eine Folie", "Inspiration", "Am Montag geht's los", [
        bild("✏️ Samstagsbild.\n\nAm Montag öffne ich die Anmeldung für meine Lead-Challenge: drei Tage, dein erstes eigenes Freebie, gratis.", CD_ANMELDUNG),
    ]),
    ("2026-11-01", "So", "Inspiration", "eine Folie", "Inspiration", "Morgen früh", [
        bild("✏️ Sonntagsbild.\n\nMorgen geht die Anmeldung auf. Tipp auf den Sticker, dann schreib ich dir als Erstes.", WARTELISTE),
    ]),
    # ---------------- KW45 · Einladung Lead-Challenge ----------------
    ("2026-11-02", "Mo", "Einladung", "lehrreich", "einen krassen Tipp", "Die Anmeldung ist offen", [
        bild("✏️ Montagsfoto.\n\nDie Anmeldung für die Lead-Challenge ist offen! Vorher noch ein Tipp."),
        t("Ein Freebie ist dein erstes eigenes Produkt, nur eben gratis. Wer es haben will, gibt dir dafür ihre Mailadresse."),
        t("Damit baust du dir eine Liste auf, die dir gehört. Egal, was der Algorithmus macht oder was die Firma ändert."),
        t("Was dich erwartet\n\n1. Tag 1: dein Thema\n2. Tag 2: dein Freebie\n3. Tag 3: zeig dich damit"),
        cta("Vom 9. bis 11. November, gratis, in einer WhatsApp-Gruppe:", LINK_LEAD),
    ]),
    ("2026-11-03", "Di", "Einladung", "persönlich", "warum mit mir", "Meine erste Liste", [
        bild("✏️ Ein Foto von dir."),
        t("Meine erste eigene Liste ist mit dem To-do-Angebot entstanden. 30 Frauen in zwei Tagen, die ich vorher nicht kannte."),
        t("✏️ Ein Satz, was diese Liste damals für dich verändert hat."),
        frage("Hast du schon eine eigene Liste, oder nur Follower?"),
        cta("In der Challenge baust du dein Freebie, mit dem deine Liste anfängt.", LINK_LEAD),
    ]),
    ("2026-11-04", "Mi", "Einladung", "Inspiration", "Inspiration", "Zwei Ströme, die sich helfen", [
        bild("✏️ Ein Bild von heute."),
        t("Das Schöne am Hybridmodell: Die zwei Seiten helfen sich gegenseitig."),
        t("Dein eigenes Produkt bringt dir Menschen, die dich kennenlernen, und einige davon interessieren sich danach für dein Network. Umgekehrt kaufen Leute aus deinem Network dein Produkt, weil sie dir schon vertrauen."),
        t("Du fängst also nicht bei null an. Du baust auf dem auf, was du schon weisst."),
        cta("Der erste Schritt ist ein Freebie. Wir starten am 9. November:", LINK_LEAD),
    ]),
    ("2026-11-05", "Do", "Einladung", "Blick hinter die Kulissen", "einen krassen Tipp", "So sieht Tag 1 aus", [
        dict(bild("✏️ Ein Screenshot aus dem Workbook, zum Beispiel Tag 1.\n\nSo sieht Tag 1 im Workbook aus."), notiz="Screenshot vom Lead-Challenge-Workbook einsetzen, Seite „Tag 1 – Was verkaufst du eigentlich?“."),
        t("An Tag 1 findest du dein Thema. Du beschreibst, wo die Leute, für die du da bist, heute stehen und wo sie hinwollen."),
        t("Und du beantwortest eine Frage, die dich überraschen wird: Wofür kommen Freundinnen und Bekannte eigentlich zu dir?"),
        frage("Wofür kommen die Leute bei dir am häufigsten?"),
        cta("Das Workbook bekommst du direkt nach der Anmeldung.", LINK_LEAD),
    ]),
    ("2026-11-06", "Fr", "Einladung", "eigene Meinung", "warum mit mir", "Fertig ist besser als perfekt", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Meine Meinung zu Freebies: Das erste darf klein sein. Eine Checkliste auf einer Seite reicht völlig."),
        t("Die meisten bauen nie eins, weil sie es gleich perfekt wollen. In der Challenge gilt deshalb: Fertig ist besser als perfekt."),
        umfrage("Bist du eher Perfektionistin oder Machertyp?", "Perfektionistin", "Machertyp"),
        cta("Drei Tage, ein fertiges Freebie:", LINK_LEAD),
    ]),
    ("2026-11-07", "Sa", "Einladung", "eine Folie", "Inspiration", "Übermorgen geht's los", [
        bild("✏️ Samstagsbild.\n\nÜbermorgen startet die Lead-Challenge. Wer sich bis Sonntagabend anmeldet, ist ab Tag 1 dabei.", LINK_LEAD),
    ]),
    ("2026-11-08", "So", "Einladung", "eine Folie", "Inspiration", "Letzter Tag vor dem Start", [
        bild("✏️ Sonntagsbild.\n\nMorgen um ✏️ Uhr kommt die erste Aufgabe in die Gruppe. Heute ist der letzte Tag, um von Anfang an dabei zu sein.", LINK_LEAD),
    ]),
    # ---------------- KW46 · Lead-Challenge 9.–11.11., danach Community ----------------
    ("2026-11-09", "Mo", "Challenge", "Tag 1 · dein Thema", "einen krassen Tipp", "Tag 1: Was verkaufst du eigentlich?", [
        bild("✏️ Foto von heute Morgen.\n\nTag 1 der Lead-Challenge! Heute geht es um die wichtigste Frage."),
        t("Was verkaufst du eigentlich? Gemeint ist das, womit du glänzt, nicht das Produkt deiner Firma."),
        t("Bei mir war es Zeit und Alltag mit vier Kindern. Die Öle waren dabei, im Mittelpunkt standen sie nie."),
        frage("Wie lautet dein Thema in einem Satz? Schreib's mir, ich geb dir eine Rückmeldung."),
        cta("Du bist noch nicht dabei? Einsteigen geht noch.", LINK_LEAD),
    ]),
    ("2026-11-10", "Di", "Challenge", "Tag 2 · dein Freebie", "einen krassen Tipp", "Tag 2: Dein Freebie entsteht", [
        bild("✏️ Foto von dir am Laptop oder mit Notizbuch.\n\nTag 2: Heute wird deine Idee ein Freebie."),
        t("Du wählst ein Format, das zu dir passt: eine Checkliste, ein kleines Workbook, ein kurzes Video oder ein paar Mails."),
        t("Zum Screenshotten\n\nDie Formel für den Titel: Ergebnis in Zeit oder Schritten, auch wenn ein Einwand dagegen spricht."),
        umfrage("Welches Format nimmst du?", "Checkliste", "Video"),
        cta("Die Aufgabe für heute steht in der Gruppe.", LINK_LEAD),
    ]),
    ("2026-11-11", "Mi", "Challenge", "Tag 3 · zeig dich", "warum mit mir", "Tag 3: Zeig dich damit", [
        bild("✏️ Foto von dir.\n\nTag 3, der letzte. Heute zeigst du dein Freebie in deinen Storys."),
        t("Am einfachsten fängst du so an: Nimm die Leute mit in die Entstehung. Zeig den Entwurf auf dem Bildschirm und frag, welcher Titel besser klingt."),
        t("So wissen sie schon, dass etwas kommt, bevor es fertig ist."),
        frage("Zeig mir dein Freebie! Verlinke mich in deiner Story, dann teile ich die schönsten."),
        cta("Fertig ist besser als perfekt. Du schaffst das heute.", FRAGE),
    ]),
    ("2026-11-12", "Do", "Community", "Ergebnisse", "Inspiration", "Was in drei Tagen entstanden ist", [
        bild("✏️ Foto von heute.\n\nIch bin noch ganz bei der Challenge."),
        dict(bild("Aus der Gruppe"), notiz="✏️ Screenshot eines Freebies oder einer Nachricht aus der WhatsApp-Gruppe, nur mit Okay der Frau. Gibt es keins, Folie weglassen."),
        t("✏️ Ein, zwei Sätze, was dich in diesen drei Tagen am meisten gefreut hat."),
        cta("Du warst nicht dabei? Mit dem Produkt-Ideen-Finder kannst du trotzdem anfangen:", LINK_IDEEN),
    ]),
    ("2026-11-13", "Fr", "Community", "eigene Meinung", "warum mit mir", "Und was kommt nach dem Freebie?", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Ein Freebie allein bringt noch kein Geld. Es ist die Eingangstür, und die Frage ist, was dahinter wartet."),
        t("Bei mir kommt danach ein kleines Angebot und dann ein grösseres. So entsteht eine Treppe, auf der die Leute Schritt für Schritt mitgehen."),
        umfrage("Weisst du schon, was hinter deinem Freebie kommt?", "Ja", "Keine Ahnung"),
        cta("Wie diese Treppe bei mir aussieht, zeig ich dir nächste Woche.", FRAGE),
    ]),
    ("2026-11-14", "Sa", "Community", "eine Folie", "Inspiration", "Zeig mir dein Freebie", [
        bild("✏️ Samstagsbild.\n\nHast du in der Challenge dein Freebie gebaut? Schick es mir, ich bin richtig gespannt.", FRAGE),
    ]),
    ("2026-11-15", "So", "Community", "eine Folie", "Inspiration", "Eine Frage für die neue Woche", [
        bild("✏️ Sonntagsbild.\n\nWomit kämpfst du gerade am meisten, wenn du an ein eigenes Produkt denkst? Schreib's mir.", FRAGE),
    ]),
    # ---------------- KW47 · Entdecken: die Digitale Produktwelt ----------------
    ("2026-11-16", "Mo", "Entdecken", "lehrreich", "einen krassen Tipp", "Deine Produkttreppe", [
        bild("✏️ Montagsfoto.\n\nWie versprochen: Heute zeig ich dir die Treppe hinter dem Freebie."),
        t("Meine Produkttreppe\n\n1. Ein Freebie, mit dem dich jemand kennenlernt\n2. Ein Minikurs für ein konkretes Problem\n3. Ein grösserer Kurs für die ganze Veränderung"),
        t("Jede Stufe löst genau ein Problem und führt zur nächsten. Die Leute steigen dort ein, wo sie gerade stehen."),
        frage("Auf welcher Stufe stehst du gerade?"),
        cta("Am Montag öffne ich die Digitale Produktwelt. Dort baust du deine eigene Treppe.", CD_KASSE),
    ]),
    ("2026-11-17", "Di", "Entdecken", "persönlich", "warum mit mir", "Warum ich daraus einen Kurs gemacht habe", [
        bild("✏️ Ein Foto von dir."),
        t("Ich werde immer wieder gefragt, wie ich mein eigenes Angebot neben dem Network aufgebaut habe."),
        t("✏️ Ein, zwei Sätze, warum dir das Hybridmodell so wichtig ist und warum du es weitergeben willst."),
        t("Darum habe ich alles, was ich dabei gelernt habe, in einen Kurs gepackt: die Digitale Produktwelt."),
        cta("Am 23. November geht die Kasse auf.", CD_KASSE),
    ]),
    ("2026-11-18", "Mi", "Entdecken", "Inspiration", "Inspiration", "Wissen, das schon da ist", [
        bild("✏️ Ein Bild von heute."),
        t("Was mich immer wieder überrascht: Fast jede Network-Mama weiss genug für ein eigenes Produkt. Sie hat es nur noch nie so gesehen."),
        t("Wer seit Jahren Leute berät, Fragen beantwortet und Familie und Business unter einen Hut bringt, hat Wissen, für das andere bezahlen würden."),
        umfrage("Glaubst du, dein Wissen reicht für ein eigenes Produkt?", "Ja", "Eher nicht"),
        cta("Finde heraus, welche Idee in dir steckt:", LINK_IDEEN),
    ]),
    ("2026-11-19", "Do", "Entdecken", "Blick in den Kurs", "warum mit mir", "Was in der Produktwelt steckt", [
        dict(bild("✏️ Screenshot aus dem Kursbereich der Produktwelt, gern unscharf.\n\nEin Blick in die Digitale Produktwelt."), notiz="Screenshot aus ThriveCart Learn, z.B. die Modulübersicht."),
        t("Was sich für dich verändert\n\n1. Du weisst, welches Produkt zu dir passt\n2. Du hast es gebaut, auch mit Hilfe von KI\n3. Du verkaufst es, ohne zu drängen\n4. Vom Freebie bis zum Angebot läuft vieles von selbst\n5. Die Leute sehen dich als Expertin"),
        t("Aus deinem Network-Wissen wird etwas Eigenes, das dir gehört."),
        frage("Was willst du über die Produktwelt wissen? Frag mich."),
        cta("Die Kasse geht am Montag auf.", CD_KASSE),
    ]),
    ("2026-11-20", "Fr", "Entdecken", "eigene Meinung", "warum mit mir", "Verkaufen ist kein Schimpfwort", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Viele Frauen im Network trauen sich nicht, ein eigenes Produkt anzubieten, weil sich Verkaufen für sie unangenehm anfühlt."),
        t("Meine Meinung: Wer etwas hat, das jemandem weiterhilft, und es nicht anbietet, enthält es den Leuten vor."),
        umfrage("Wie fühlt sich Verkaufen für dich an?", "Unangenehm", "Ganz okay"),
        cta("Wie es leichter geht, steht in der Produktwelt. Ab Montag.", CD_KASSE),
    ]),
    ("2026-11-21", "Sa", "Entdecken", "eine Folie", "Inspiration", "Der nächste Schritt", [
        bild("✏️ Samstagsbild.\n\nAm Montag öffne ich die Digitale Produktwelt. Wer nach der Challenge weiterbauen will: Das ist der nächste Schritt.", CD_KASSE),
    ]),
    ("2026-11-22", "So", "Entdecken", "eine Folie", "Inspiration", "Morgen geht die Kasse auf", [
        bild("✏️ Sonntagsbild.\n\nMorgen früh geht die Kasse für die Digitale Produktwelt auf, für eine Woche.", CD_KASSE),
    ]),
    # ---------------- KW48/49 · Kasse Digitale Produktwelt 23.–30.11. ----------------
    ("2026-11-23", "Mo", "Kasse offen", "Fakten", "warum mit mir", "Die Kasse ist offen", [
        bild("✏️ Montagsfoto.\n\nDie Kasse für die Digitale Produktwelt ist offen!"),
        t("Sie ist für dich, wenn du im Network bist und dir daneben etwas Eigenes aufbauen willst, das dir gehört."),
        t("Was du am Ende hast\n\n1. Dein eigenes Produkt, passend zu deinem Wissen\n2. Eine Treppe vom Freebie bis zum grösseren Angebot\n3. Einen Weg, es zu verkaufen, ohne zu drängen"),
        t("Aus deinem Wissen wird ein eigenes Produkt neben deinem Network. 333 Franken, bis Montag, 30. November."),
        frage("Fragen? Schreib mir, ich antworte dir persönlich."),
        cta("Alle Infos und die Anmeldung:", LINK_DPW),
    ]),
    ("2026-11-24", "Di", "Kasse offen", "persönlich · Einwand", "warum mit mir", "Schauen, wie weit ich selbst komme", [
        bild("✏️ Ein Foto von dir."),
        t("Einen Satz höre ich oft: Ich schau erst mal, wie weit ich selbst komme."),
        t("✏️ Deine ehrliche Geschichte dazu: Wie lange hast du es allein versucht, bevor du dir Hilfe geholt hast?"),
        t("Die Frage, die ich mir dann stelle: Was kostet es mich, wenn ich in einem halben Jahr noch am selben Punkt stehe?"),
        cta("Wenn du genau an diesem Punkt bist:", LINK_DPW),
    ]),
    ("2026-11-25", "Mi", "Kasse offen", "Inspiration", "Inspiration", "Ein Angebot öffnet viele Türen", [
        bild("✏️ Ein Bild von heute."),
        t("Erinnerst du dich an meine Liste für meinen Mann? Aus einem einzigen kleinen Angebot sind damals 30 Bestellungen in zwei Tagen geworden."),
        t("Und aus diesen Gesprächen ist am Ende mehr entstanden als nur ein Kurs, auch im Network."),
        umfrage("Wo stehst du gerade?", "Ganz am Anfang", "Idee ist da"),
        cta("Dein erstes eigenes Angebot, noch bis Montag:", LINK_DPW),
    ]),
    ("2026-11-26", "Do", "Kasse offen", "Blick in den Kurs", "einen krassen Tipp", "Produkte, die immer wieder gekauft werden", [
        dict(bild("✏️ Screenshot einer Lektion, zum Beispiel „Produkte, die immer wieder gekauft werden“.\n\nEine Lektion, die ich besonders mag."), notiz="Screenshot aus ThriveCart Learn einsetzen."),
        t("Eine Lektion in der Produktwelt heisst Produkte, die immer wieder gekauft werden. Darin geht es darum, wie aus einem einmaligen Kauf ein Einkommen wird, das wiederkommt."),
        t("Ein Tipp vorab\n\nFrag dich bei jeder Idee: Braucht jemand das einmal, oder immer wieder? Was immer wieder gebraucht wird, trägt dich über die Monate."),
        frage("Was ist deine grösste Frage zum eigenen Produkt?"),
        cta("Dein eigenes Produkt, noch bis Montag:", LINK_DPW),
    ]),
    ("2026-11-27", "Fr", "Kasse offen", "eigene Meinung", "warum mit mir", "Black Friday ohne Rabatt", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Heute ist Black Friday, und bei mir gibt es keinen Rabatt. Der Preis bleibt 333, wie seit Montag."),
        t("Wer am Montag gekauft hat, soll heute nicht das Gefühl haben, zu viel bezahlt zu haben. Das ist mir wichtiger als ein schneller Verkauf."),
        umfrage("Kaufst du am Black Friday?", "Ja, gezielt", "Lieber nicht"),
        cta("Noch bis Montag um Mitternacht:", LINK_DPW),
    ]),
    ("2026-11-28", "Sa", "Kasse offen", "eine Folie", "Inspiration", "Noch zwei Tage", [
        bild("✏️ Samstagsbild.\n\nNoch zwei Tage, dann geht die Kasse der Digitalen Produktwelt zu.", LINK_DPW),
    ]),
    ("2026-11-29", "So", "Kasse offen", "eine Folie", "Inspiration", "Morgen ist Schluss", [
        bild("✏️ Sonntagsbild.\n\nMorgen um Mitternacht geht die Kasse zu. Wenn du noch eine Frage hast, schreib mir heute.", LINK_DPW),
    ]),
    ("2026-11-30", "Mo", "Kasse offen", "letzter Tag", "warum mit mir", "Heute um Mitternacht", [
        bild("✏️ Foto von dir.\n\nHeute um Mitternacht geht die Kasse für die Digitale Produktwelt zu."),
        t("Sie passt zu dir, wenn du bereit bist, ein paar Wochen an deinem eigenen Produkt zu arbeiten. Sie passt nicht, wenn du dir Ergebnisse wünschst, ohne selbst etwas zu tun."),
        bild("✏️ Dein ehrlicher Satz zum Schluss, frei in die Kamera gesprochen."),
        frage("Noch unsicher? Schreib mir bis 22 Uhr."),
        cta("Letzte Chance, bis 23:59:", LINK_DPW),
    ]),
]

# doTERRA im November: kein Verkauf. Aktivieren, Vertrauen, Community.
# Höchstens einmal pro Woche der Gratis-Kickstart (immer samstags), sonst nur Fragen, Umfragen, Tipps.
DOTERRA = [
    # ---------------- KW44 · wieder da sein ----------------
    ("2026-10-26", "Mo", "Aktivieren", "persönlich", "warum mit mir", "Ich war eine Weile still", [
        bild("✏️ Ein Foto von dir heute.\n\nIch war hier in letzter Zeit ziemlich still. Das ändert sich jetzt."),
        t("✏️ Ein ehrlicher Satz, warum du weg warst, gern mit Humor."),
        t("Ab heute bin ich wieder jeden Tag da, mit dem, was mir selbst geholfen hat, wieder zu Energie zu kommen."),
        umfrage("Wie geht's dir gerade?", "Gut", "Bin müde"),
    ]),
    ("2026-10-27", "Di", "Aktivieren", "Kennenlernen", "Inspiration", "Wer bist du?", [
        bild("✏️ Ein Alltagsfoto."),
        t("Ich weiss gar nicht genau, wer hier inzwischen mitliest. Das will ich ändern."),
        umfrage("Wie viele Kinder hast du?", "1 oder 2", "3 oder mehr"),
        frage("Was beschäftigt dich gerade am meisten?"),
    ]),
    ("2026-10-28", "Mi", "Aktivieren", "Tipp", "einen krassen Tipp", "30 Gramm zum Frühstück", [
        bild("✏️ Dein Frühstück von heute."),
        t("Mein einfachster Tipp für mehr Energie am Vormittag: mindestens 30 Gramm Protein zum Frühstück."),
        t("Warum\n\nEin Gipfeli lässt den Blutzucker schnell steigen und genauso schnell wieder fallen. Viele spüren das um halb zehn als Tief."),
        umfrage("Was gibt's bei dir zum Frühstück?", "Süss", "Herzhaft"),
    ]),
    ("2026-10-29", "Do", "Aktivieren", "Geschichte", "warum mit mir", "Der Satz einer Freundin", [
        bild("✏️ Ein Foto von dir."),
        t("Den entscheidenden Satz hat mir eine Freundin gesagt, gleich alt wie ich: Mach doch mal einen Hormontest."),
        t("Da war ich 36. Mit dem Ergebnis hab ich angefangen, meinen Alltag umzubauen, Schritt für Schritt."),
        frage("Wer sagt dir ehrlich, wenn du müde aussiehst?"),
    ]),
    ("2026-10-30", "Fr", "Aktivieren", "eigene Meinung", "Inspiration", "Müde ist nicht normal", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Lange hab ich gedacht: Ich bin halt müde, mit vier Kindern ist das so."),
        t("Heute weiss ich, dass Müdigkeit viele Ursachen haben kann und man einiges davon selbst in der Hand hat."),
        umfrage("Hältst du Müdigkeit für normal?", "Ja, leider", "Nein"),
    ]),
    ("2026-10-31", "Sa", "Aktivieren", "eine Folie", "einen krassen Tipp", "Drei Tage reinschnuppern", [
        bild("✏️ Samstagsbild.\n\nWenn du ausprobieren willst, was mir geholfen hat: drei Tage Energie-Kickstart, gratis per Mail.", LINK_KICK),
    ]),
    ("2026-11-01", "So", "Aktivieren", "eine Folie", "Inspiration", "Wie startest du in den November?", [
        bild("✏️ Sonntagsbild.\n\nWie startest du in den November? Schreib's mir, ich bin gespannt.", FRAGE),
    ]),
    # ---------------- KW45 · Vertrauen ----------------
    ("2026-11-02", "Mo", "Vertrauen", "Tipp", "einen krassen Tipp", "8000 Schritte", [
        bild("✏️ Foto von draussen."),
        t("Ein Tipp, der nichts kostet: Schritte zählen. Ich nehme mir 8000 am Tag vor."),
        t("So klappt's im Mama-Alltag\n\n✏️ Dein bester Trick für mehr Schritte, zum Beispiel zu Fuss zur Schule oder telefonieren im Gehen."),
        frage("Wie viele Schritte machst du an einem normalen Tag?"),
    ]),
    ("2026-11-03", "Di", "Vertrauen", "persönlich", "warum mit mir", "Dreimal die Woche", [
        bild("✏️ Foto von deinem Training oder deinen Turnschuhen."),
        t("Dreimal die Woche Krafttraining. ✏️ Ein ehrlicher Satz, wie du früher darüber gedacht hast."),
        t("Krafttraining ist bei mir einer von vier Bausteinen. Die anderen drei sind Protein, Schritte und mein Nährstoffpaket."),
        umfrage("Machst du Krafttraining?", "Ja", "Noch nicht"),
    ]),
    ("2026-11-04", "Mi", "Vertrauen", "Community", "Inspiration", "Womit kämpfst du gerade?", [
        bild("✏️ Ein Bild von heute."),
        t("Heute will ich von dir hören. Ich mache diese Woche eine Story zu dem Thema, das am häufigsten kommt."),
        umfrage("Was raubt dir gerade am meisten Energie?", "Schlaf", "Alltag"),
        frage("Oder etwas ganz anderes? Schreib's mir."),
    ]),
    ("2026-11-05", "Do", "Vertrauen", "Alltag", "warum mit mir", "Mein Öl-Moment", [
        bild("✏️ Foto von deinen Ölen oder deinem Diffuser."),
        t("✏️ Wann benutzt du deine Öle am liebsten? Ein Moment aus deinem Alltag, zwei Sätze."),
        umfrage("Benutzt du ätherische Öle?", "Jeden Tag", "Noch nie"),
    ]),
    ("2026-11-06", "Fr", "Vertrauen", "Antwort", "einen krassen Tipp", "Eure Antworten", [
        bild("✏️ Du, direkt in die Kamera.\n\nIhr habt mir am Mittwoch geschrieben, was euch Energie raubt."),
        dict(t("✏️ Das Thema, das am häufigsten kam, und dein ehrlicher Tipp dazu."), notiz="Aus den Antworten vom Mittwoch das häufigste Thema nehmen. Kam keine Antwort, eins aus deinem eigenen Alltag."),
        frage("Geht's dir auch so? Erzähl mir davon."),
    ]),
    ("2026-11-07", "Sa", "Vertrauen", "eine Folie", "einen krassen Tipp", "Drei Tage reinschnuppern", [
        bild("✏️ Samstagsbild.\n\nDrei kleine Schritte, drei Tage, gratis per Mail. Für alle, die mal ausprobieren wollen.", LINK_KICK),
    ]),
    ("2026-11-08", "So", "Vertrauen", "eine Folie", "Inspiration", "Was gibt dir Energie?", [
        bild("✏️ Sonntagsbild.\n\nWas gibt dir am Wochenende Energie? Schreib's mir.", FRAGE),
    ]),
    # ---------------- KW46 · Community ----------------
    ("2026-11-09", "Mo", "Community", "Tipp", "einen krassen Tipp", "Auch mittags 30 Gramm", [
        bild("✏️ Dein Mittagessen von heute."),
        t("Auch mittags halte ich mich an meine Faustregel: mindestens 30 Gramm Protein pro Mahlzeit."),
        t("Zum Screenshotten\n\n✏️ Deine liebste Kombination mit 30 Gramm Protein, mit Mengen."),
        frage("Was isst du am liebsten zu Mittag?"),
    ]),
    ("2026-11-10", "Di", "Community", "persönlich", "warum mit mir", "Heute schlafe ich durch", [
        bild("✏️ Foto von dir am Morgen."),
        t("Früher bin ich müde aufgewacht, egal wie lange ich geschlafen habe. Heute schlafe ich acht Stunden durch."),
        t("Bei mir war es keine einzelne Sache. Es war die Kombination aus Protein, Krafttraining, Schritten und meinem Nährstoffpaket."),
        umfrage("Wie schläfst du?", "Gut", "Schlecht"),
    ]),
    ("2026-11-11", "Mi", "Community", "Community", "Inspiration", "Eure Abendroutine", [
        bild("✏️ Ein gemütliches Abendbild."),
        t("Ich bin neugierig, wie euer Abend aussieht, wenn die Kinder im Bett sind."),
        umfrage("Was machst du zuerst?", "Aufräumen", "Sofa"),
        frage("Hast du ein festes Abendritual?"),
    ]),
    ("2026-11-12", "Do", "Community", "Alltag", "warum mit mir", "Ein Blick in meinen Tag", [
        bild("✏️ Ein Foto aus deinem Tag heute."),
        t("✏️ Ein, zwei Sätze, wie dein Tag heute aussieht und wo du dir Zeit für dich nimmst."),
        frage("Wann hast du heute an dich gedacht?"),
    ]),
    ("2026-11-13", "Fr", "Community", "eigene Meinung", "einen krassen Tipp", "Essen statt Shakes", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Meine Meinung, die nicht allen gefällt: Ich brauche keine Shakes, um auf mein Protein zu kommen. Ich esse es."),
        t("Der Ernährungsmediziner Matthias Riedl warnt in seinem Buch Gamechanger Protein sogar vor hochverarbeiteten Proteinprodukten."),
        umfrage("Shake oder richtiges Essen?", "Shake", "Essen"),
    ]),
    ("2026-11-14", "Sa", "Community", "eine Folie", "einen krassen Tipp", "Drei Tage reinschnuppern", [
        bild("✏️ Samstagsbild.\n\nWer mal drei Tage ausprobieren will, wie ich esse und mich bewege: Der Kickstart ist gratis.", LINK_KICK),
    ]),
    ("2026-11-15", "So", "Community", "eine Folie", "Inspiration", "Wie war deine Woche?", [
        bild("✏️ Sonntagsbild.\n\nWie war deine Woche? Erzähl mir in einem Satz.", FRAGE),
    ]),
    # ---------------- KW47 · Vertrauen vertiefen ----------------
    ("2026-11-16", "Mo", "Vertrauen", "Tipp", "einen krassen Tipp", "Protein schon am Morgen planen", [
        bild("✏️ Foto von deinem Abendessen."),
        t("Ein Tipp für den Abend: Plan dein Protein schon am Morgen. Wer um sechs erst überlegt, landet schnell bei Brot und Käse. Ich kenn das."),
        umfrage("Planst du dein Essen?", "Ja", "Spontan"),
    ]),
    ("2026-11-17", "Di", "Vertrauen", "Geschichte", "warum mit mir", "Was sich bei mir verändert hat", [
        bild("✏️ Ein Foto von dir."),
        t("Wenn ich zurückschaue, ist das grösste Geschenk nicht das Gewicht auf der Waage. Es ist, dass ich am Nachmittag noch Energie für meine Kinder habe."),
        t("✏️ Ein konkreter Moment, an dem du das zuletzt gemerkt hast."),
        frage("Wofür hättest du gern mehr Energie?"),
    ]),
    ("2026-11-18", "Mi", "Vertrauen", "Community", "Inspiration", "Eure Fragen", [
        bild("✏️ Ein Bild von heute."),
        t("Heute dürft ihr mich alles fragen: zu Ernährung, Training, Ölen oder wie ich das mit vier Kindern mache."),
        frage("Was willst du von mir wissen?"),
    ]),
    ("2026-11-19", "Do", "Vertrauen", "Antwort", "einen krassen Tipp", "Ich beantworte eure Fragen", [
        bild("✏️ Du, direkt in die Kamera.\n\nIhr habt mir gestern Fragen geschickt. Hier sind meine Antworten."),
        dict(t("✏️ Eine Frage von gestern und deine Antwort darauf."), notiz="Frage als Screenshot oder abgetippt einsetzen, Namen abdecken. Für jede weitere Frage diese Folie kopieren."),
        frage("Noch eine Frage offen? Schreib mir."),
    ]),
    ("2026-11-20", "Fr", "Vertrauen", "eigene Meinung", "Inspiration", "Schenk dir selbst auch was", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Wir Mamas denken im Dezember an alle Geschenke, nur an uns selbst denken wir zuletzt."),
        t("Mein Vorschlag für dieses Jahr: Nimm dir eine Sache vor, die nur dir guttut, und zieh sie durch."),
        frage("Was schenkst du dir selbst?"),
    ]),
    ("2026-11-21", "Sa", "Vertrauen", "eine Folie", "einen krassen Tipp", "Drei Tage reinschnuppern", [
        bild("✏️ Samstagsbild.\n\nDrei Tage, drei kleine Schritte zu mehr Energie. Gratis per Mail.", LINK_KICK),
    ]),
    ("2026-11-22", "So", "Vertrauen", "eine Folie", "Inspiration", "Eine ruhige Minute", [
        bild("✏️ Sonntagsbild.\n\nWo findest du am Sonntag deine ruhige Minute? Zeig's mir.", FRAGE),
    ]),
    # ---------------- KW48/49 · Community, Vorweihnachtszeit ----------------
    ("2026-11-23", "Mo", "Community", "Community", "Inspiration", "Wie sieht dein Dezember aus?", [
        bild("✏️ Montagsfoto."),
        t("✏️ Wie sieht dein Dezember aus? Ein Satz, ehrlich."),
        umfrage("Freust du dich auf den Dezember?", "Sehr", "Er stresst mich"),
    ]),
    ("2026-11-24", "Di", "Community", "Tipp", "einen krassen Tipp", "Energie in der Adventszeit", [
        bild("✏️ Ein winterliches Bild."),
        t("Mein Plan für die vollen Wochen: Ich lasse vieles weg, aber nie das Protein am Morgen und die Schritte."),
        t("✏️ Was du in der Adventszeit bewusst weglässt."),
        frage("Was lässt du dieses Jahr weg?"),
    ]),
    ("2026-11-25", "Mi", "Community", "Alltag", "warum mit mir", "Mein Lieblingsduft im Winter", [
        bild("✏️ Foto von deinem Diffuser oder deinem Lieblingsöl im Winter."),
        t("✏️ Welcher Duft für dich nach Winter riecht und warum."),
        umfrage("Lieber warm oder frisch?", "Warm", "Frisch"),
    ]),
    ("2026-11-26", "Do", "Community", "Geschichte", "warum mit mir", "Wie ich zu den Ölen kam", [
        bild("✏️ Foto von dir."),
        t("Zu den Ölen bin ich über einen Umweg gekommen. Zuerst hab ich Mamas gezeigt, wie sie ihre To-do-Liste halbieren, und dabei kamen wir ins Gespräch."),
        t("✏️ Ein Satz, was die Öle heute für dich bedeuten."),
        frage("Wie bist du hier auf mich gestossen?"),
    ]),
    ("2026-11-27", "Fr", "Community", "eigene Meinung", "einen krassen Tipp", "Black Friday", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Heute ist Black Friday. Mein Tipp: Kauf nichts, was du im Januar wieder bereust."),
        umfrage("Kaufst du heute etwas?", "Ja", "Nein"),
    ]),
    ("2026-11-28", "Sa", "Community", "eine Folie", "einen krassen Tipp", "Drei Tage reinschnuppern", [
        bild("✏️ Samstagsbild.\n\nFür alle, die vor dem Dezember noch durchatmen wollen: drei Tage Energie-Kickstart, gratis.", LINK_KICK),
    ]),
    ("2026-11-29", "So", "Community", "eine Folie", "Inspiration", "Erster Advent", [
        bild("✏️ Adventsbild.\n\nSchönen ersten Advent! Was macht ihr heute?", FRAGE),
    ]),
    ("2026-11-30", "Mo", "Community", "Rückblick", "Inspiration", "Danke für diesen Monat", [
        bild("✏️ Foto von dir."),
        t("Ein Monat, seit ich hier wieder jeden Tag bin. Danke für eure Antworten, ich hab jede gelesen."),
        frage("Worüber soll ich im Dezember mehr erzählen?"),
    ]),
]

# Eigene Zusatzprüfungen über die Blackliste hinaus
# ======================================================================================
# Neufassung ab 30.10.2026 nach dem Storytelling-Bauplan (Patricia: „ja, neu bauen“ am 29.10.,
# Befund: outputs/stories/2026-10-29-storys-november-pruefung.md).
# Je Sequenz: Einstieg mitten in der Szene oder mit Neugier · Geschichte mit Sticker · Learning
# zum Screenshotten · Brücke und Weg zum Angebot (doTERRA: der Gratis-Kickstart, kein Verkauf) ·
# Ausklang. Szenen nur aus belegten Geschichten, sonst ✏️ mit einer Frage, die die Szene leicht macht.
# Einstiege, die eine Geschichte ankündigen, sind Hooks und erlaubt (Patricia, 29.10.).
# ======================================================================================
learning = KI.learning

M_NEU = [
    ("2026-10-30", "Fr", "Inspiration", "eigene Meinung", "warum mit mir", "Mehr bestellen ist kein Business", [
        bild("✏️ Du, direkt in die Kamera.\n\nIch sag's heute mal gerade heraus, auch wenn es ein bisschen wehtut."),
        t("Wenn du am Ende des Monats kaum mehr verdienst, als du selbst bestellst, hast du ein teures Hobby."),
        t("Ich kenne das von mir selbst. 2018 hab ich mit viel Hoffnung angefangen und lange vor allem über das Produkt geredet."),
        umfrage("Wie ist es bei dir gerade?", "Eher Hobby", "Schon Business"),
        t("Gekippt ist es, als ich über meinen Alltag mit vier Kindern geredet habe. Daraus wurde mein erstes eigenes Angebot, und über das kamen die Leute zu mir."),
        learning("Ein Business beginnt dort, wo du etwas anbietest, das dir gehört."),
        cta("Darum zeig ich dir im Tool-Workshop, wie du dein eigenes Gratis-Angebot baust, live am 10. und 11. November, für 39 Franken. Die Anmeldung ist offen.", LINK_WS),
        t("So, und jetzt fängt bei uns das Wochenende an."),
    ]),
    ("2026-10-31", "Sa", "Inspiration", "eine Folie", "Inspiration", "Wofür kommen die Leute zu dir?", [
        bild("✏️ Samstagsbild, gern draussen oder mit Familie.\n\nWofür fragen dich die Leute um Rat, auch wenn es gar nicht um dein Produkt geht? Genau dort fängt deine Nische an.", FRAGE),
        cta("Wenn du es genauer wissen willst, probier meinen Nischengenerator aus, gratis:", LINK_NISCHE),
        t("Jetzt aber Wochenende. Bis bald!"),
    ]),
    ("2026-11-01", "So", "Inspiration", "eine Folie", "Inspiration", "Was im November kommt", [
        bild("✏️ Sonntagsbild.\n\nAm 10. und 11. November bauen wir im Tool-Workshop dein eigenes Gratis-Tool, live. Die Anmeldung ist offen.", LINK_WS),
        t("Ich geniess jetzt den Sonntag, du hoffentlich auch."),
    ]),
    # ---------------- Launch Tool-Workshop (Patricias Entscheid 29.10.: Workshop ersetzt Lead-Challenge + DPW-Kasse) ----
    # Gratis-Einstieg Nischengenerator ab 3.11. · Kasse 5.–9.11. · Live 10.11. (Tool) + 11.11. (Seite) · 3 Tage Begleitung
    ("2026-11-02", "Mo", "Anwärmen", "lehrreich", "einen krassen Tipp", "Deine Nische liegt neben dem Produkt", [
        bild("✏️ Montagsfoto.\n\nMit meiner Nische hatte das Öl nichts zu tun, und gerade darum haben mir 30 Mamas in zwei Tagen etwas abgekauft."),
        t("Ich hab ihnen gezeigt, wie sie ihre To-do-Liste halbieren. Das war mein Alltag mit vier Kindern, und genau dafür haben mich die Leute schon vorher um Rat gefragt."),
        umfrage("Weisst du, wofür die Leute dich fragen?", "Ja, ziemlich genau", "Keine Ahnung"),
        learning("Deine Nische ist das, wofür die Leute schon heute zu dir kommen, auch ohne Produkt."),
        cta("Genau das findest du mit meinem Nischengenerator heraus, gratis:", LINK_NISCHE),
        t("So, und jetzt geht's an meinen Montag."),
    ]),
    ("2026-11-03", "Di", "Gratis-Einstieg", "persönlich", "einen krassen Tipp", "Der Nischengenerator ist da", [
        bild("✏️ Foto von dir am Laptop.\n\nWie lange sitzt du schon an der Frage, worüber du eigentlich reden sollst?"),
        t("✏️ Wann du dir diese Frage selbst gestellt hast und wie lange die Antwort gedauert hat."),
        t("Darum hab ich den Nischengenerator gebaut. Du beantwortest ein paar Fragen zu dir und deinem Alltag, und er zeigt dir, welche Nische in deinem Network zu dir passt."),
        learning("Deine Nische steckt in deinem Leben. Das Produkt passt dann dazu."),
        cta("Probier ihn aus, gratis:", LINK_NISCHE),
        frage("Schick mir dein Ergebnis, ich bin gespannt."),
        t("Ich schau mir heute jedes Ergebnis an."),
    ]),
    ("2026-11-04", "Mi", "Gratis-Einstieg", "Inspiration", "Inspiration", "Und dann?", [
        bild("✏️ Ein Bild von heute.\n\nDu kennst jetzt deine Nische. Und was kommt danach?"),
        bild("✏️ Ein Ergebnis aus dem Nischengenerator, das dir jemand geschickt hat, nur mit Okay und Namen abgedeckt. Ohne Okay diese Folie löschen."),
        t("Als Nächstes braucht es etwas, womit dich die Leute kennenlernen. Bei mir ist das der Bio-Check: ein kleines Tool, das dir sofort sagt, was an deiner Bio noch fehlt."),
        umfrage("Was ist dein Gratis-Angebot heute?", "Ein PDF", "Noch keins"),
        learning("Ein PDF wird heruntergeladen, ein Tool wird benutzt."),
        cta("Wie du so ein Tool selbst baust, zeig ich dir im Tool-Workshop am 10. und 11. November:", LINK_WS),
        t("Bis morgen!"),
    ]),
    ("2026-11-05", "Do", "Kasse offen", "Fakten", "warum mit mir", "Dein Freebie als Tool", [
        bild("✏️ Foto von dir.\n\nWann hast du das letzte PDF geöffnet, das du dir irgendwo geholt hast?"),
        t("✏️ Was mit den PDFs in deinem Download-Ordner passiert, ehrlich und gern mit Humor."),
        t("Darum mache ich meine Gratis-Angebote als kleine Tools. Wer sie ausfüllt, bekommt sofort ein Ergebnis, und ich sehe, wofür sich die Person interessiert."),
        learning("Ein Tool liefert sofort ein Ergebnis und zeigt dir, wer sich wofür interessiert."),
        t("Was du nach meinem Tool-Workshop hast\n\n1. Dein eigenes Gratis-Tool, passend zu deiner Nische\n2. Eine Seite, auf der man sich dafür einträgt\n3. Drei Tage Begleitung, damit es auch online geht",
          "Live am 10. und 11. November, für 39 Franken."),
        cta("Anmelden kannst du dich noch bis Montag um Mitternacht, für 39 Franken:", LINK_WS),
        t("So, und jetzt bin ich gespannt, wer als Erste dabei ist."),
    ]),
    ("2026-11-06", "Fr", "Kasse offen", "eigene Meinung", "warum mit mir", "Du brauchst keine Programmiererin", [
        bild("✏️ Du, direkt in die Kamera.\n\nFür ein eigenes Tool brauchst du keine Programmiererin."),
        t("Vor kurzem hab ich mit Claude einen Story-Generator gebaut. ✏️ Wie lange es gedauert hat und was du dabei gedacht hast."),
        umfrage("Traust du dir das zu?", "Ja, zeig's mir", "Eher nicht"),
        learning("Du beschreibst, was dein Tool tun soll, und Claude schreibt den Code dazu."),
        cta("Am 10. November bauen wir deins zusammen, live:", LINK_WS),
        t("Schönes Wochenende!"),
    ]),
    ("2026-11-07", "Sa", "Kasse offen", "eine Folie", "Inspiration", "Noch bis Montag", [
        bild("✏️ Samstagsbild.\n\nNoch bis Montag kannst du dich für meinen Tool-Workshop anmelden. Am 10. November bauen wir dein Gratis-Tool, live.", LINK_WS),
        t("Jetzt aber Wochenende."),
    ]),
    ("2026-11-08", "So", "Kasse offen", "eine Folie", "Inspiration", "Fragen zum Workshop", [
        bild("✏️ Sonntagsbild.\n\nFragen zum Workshop? Schreib mir heute, ich antworte dir persönlich.", FRAGE),
        cta("Anmeldung bis morgen um Mitternacht:", LINK_WS),
        t("Geniess den Sonntag!"),
    ]),
    ("2026-11-09", "Mo", "Kasse offen", "letzter Tag", "warum mit mir", "Heute um Mitternacht", [
        bild("✏️ Foto von dir.\n\nHeute um Mitternacht schliesst die Anmeldung, und ich sag dir ehrlich, für wen der Workshop nichts ist."),
        t("Er passt zu dir, wenn du an beiden Tagen live dabei bist oder die Aufzeichnung schaust und danach drei Tage dranbleibst. Er passt nicht, wenn du ein fertiges Tool von mir erwartest."),
        bild("✏️ Dein ehrlicher Satz zum Schluss, frei in die Kamera gesprochen."),
        frage("Noch unsicher? Schreib mir bis 22 Uhr."),
        cta("Letzte Chance, bis 23:59:", LINK_WS),
        t("Morgen geht's los. Ich freu mich auf alle, die dabei sind."),
    ]),
    ("2026-11-10", "Di", "Workshop", "Blick hinter die Kulissen", "Inspiration", "Heute bauen wir Tools", [
        bild("✏️ Foto von deinem Arbeitsplatz vor dem Call.\n\nHeute bauen wir live Gratis-Tools."),
        t("✏️ Wie es dir vor dem Call geht, ein Satz."),
        bild("✏️ Nach dem Call: Screenshot von einem Tool, das heute entstanden ist, nur mit Okay. Ohne Okay diese Folie löschen."),
        learning("Ein Tool fängt mit einer einzigen Frage an, die sich deine Leute schon heute stellen."),
        frage("Was würdest du in dein eigenes Tool packen?"),
        t("Morgen kommt die Seite dazu. Bis dann!"),
    ]),
    ("2026-11-11", "Mi", "Workshop", "lehrreich", "einen krassen Tipp", "Die Seite dazu", [
        bild("✏️ Foto von heute.\n\nEin Tool braucht eine Seite, auf der sich die Leute dafür eintragen."),
        t("Dafür reicht am Anfang wenig: eine Überschrift, drei Sätze dazu, was man bekommt, und ein Formular. Ganz am Anfang tut es sogar ein Link zu WhatsApp."),
        umfrage("Wie trägt man sich bei dir ein?", "Formular", "Per Nachricht"),
        learning("Fang mit der einfachsten Seite an, die funktioniert. Schöner machen kannst du sie später."),
        t("✏️ Was heute im Call passiert ist, ein, zwei Sätze."),
        cta("Du warst nicht dabei? Mit dem Nischengenerator kannst du trotzdem schon anfangen:", LINK_NISCHE),
        t("Ab morgen begleite ich die Gruppe drei Tage lang. Bis morgen!"),
    ]),
    ("2026-11-12", "Do", "Begleitung", "Ergebnisse", "Inspiration", "Was entstanden ist", [
        bild("✏️ Foto von heute.\n\nWas in zwei Tagen Workshop entstanden ist:"),
        bild("✏️ Screenshot eines Tools oder einer Seite aus der Gruppe, nur mit Okay und Namen abgedeckt. Ohne Okay diese Folie löschen."),
        t("✏️ Was dich daran am meisten freut, ein, zwei Sätze."),
        learning("Ein Tool, das online ist, bringt dir mehr als eines, an dem du noch feilst."),
        cta("Wenn du zuerst deine Nische finden willst:", LINK_NISCHE),
        t("Ich geh jetzt zurück in die Gruppe."),
    ]),
    ("2026-11-13", "Fr", "Begleitung", "eigene Meinung", "warum mit mir", "Warum ich danach noch dabei bin", [
        bild("✏️ Du, direkt in die Kamera.\n\nWarum ich nach dem Workshop noch drei Tage dabei bin?"),
        t("Weil der Alltag mit Kindern genau dann dazwischenkommt, wenn man allein weiterbauen will. ✏️ Wie es dir selbst damit geht."),
        umfrage("Wie machst du lieber weiter?", "Allein", "Mit Begleitung"),
        learning("Mach dein Tool fertig, solange der Schwung vom Workshop noch da ist."),
        t("✏️ Ob und wie die Begleitung weitergeht."),
        t("Schönes Wochenende!"),
    ]),
    ("2026-11-14", "Sa", "danach", "eine Folie", "Inspiration", "Deine Nische", [
        bild("✏️ Samstagsbild.\n\nHast du deine Nische schon gefunden? Der Nischengenerator ist weiter gratis für dich da.", LINK_NISCHE),
        t("Geniess den Samstag!"),
    ]),
    ("2026-11-15", "So", "danach", "eine Folie", "Inspiration", "Die häufigste Frage", [
        bild("✏️ Sonntagsbild.\n\nWelche Frage stellen dir die Leute in deinem Network am häufigsten?", FRAGE),
        t("Ich les jede Antwort."),
    ]),
    ("2026-11-16", "Mo", "danach", "lehrreich", "einen krassen Tipp", "Aus einer Frage wird ein Tool", [
        bild("✏️ Montagsfoto.\n\nAus der Frage, die du am häufigsten hörst, kann dein Gratis-Tool werden."),
        t("✏️ Eine Frage, die dir diese Woche gestellt wurde, und wie ein kleines Tool sie beantworten könnte."),
        learning("Die Frage, die du am häufigsten hörst, ist der Anfang deines Tools."),
        frage("Welche Frage hörst du am häufigsten?"),
        cta("Und wenn du noch nicht weisst, worüber du reden sollst:", LINK_NISCHE),
        t("Gute Woche dir!"),
    ]),
    ("2026-11-17", "Di", "danach", "persönlich", "warum mit mir", "Um halb sieben", [
        bild("✏️ Ein Foto von dir.\n\nUm halb sieben hab ich meinen Ältesten im Badezimmer gehört und mir gedacht: Schon krass, dass uns 60 Jahre lang jemand sagt, wann wir aufzustehen haben."),
        t("Genau das ist bei mir der Grund für die Selbständigkeit. ✏️ Was das heute in deinem Alltag heisst."),
        umfrage("Warum willst du etwas Eigenes?", "Freiheit", "Einkommen"),
        learning("Ein eigenes kleines Angebot ist der erste Schritt zu mehr Selbstbestimmung neben dem Network."),
        cta("Dein erster Schritt ist deine Nische:", LINK_NISCHE),
        t("So, und jetzt fängt mein Tag an."),
    ]),
    ("2026-11-18", "Mi", "danach", "Inspiration", "Inspiration", "Zwei Standbeine", [
        bild("✏️ Ein Bild von heute.\n\nMein Network und mein eigenes Angebot laufen nebeneinander, und sie helfen sich gegenseitig."),
        t("Über mein eigenes Angebot lernen mich Menschen kennen. Ein Teil von ihnen fragt irgendwann nach dem, was mir im Alltag sonst noch hilft, und so kommen die Öle ins Gespräch."),
        umfrage("Hast du schon etwas Eigenes?", "Ja", "Noch nicht"),
        learning("Dein eigenes Angebot öffnet Türen, die dein Network-Produkt allein nicht öffnet."),
        cta("Finde zuerst deine Nische:", LINK_NISCHE),
        t("Bis morgen!"),
    ]),
    ("2026-11-19", "Do", "danach", "Community", "Inspiration", "Frag mich alles", [
        bild("✏️ Foto von dir.\n\nHeute darfst du mich alles fragen: Nische, Tools, Claude oder wie ich das mit vier Kindern mache."),
        frage("Was willst du von mir wissen?"),
        t("Ich beantworte die Fragen morgen in meinen Storys."),
    ]),
    ("2026-11-20", "Fr", "danach", "Antwort", "einen krassen Tipp", "Deine Fragen", [
        bild("✏️ Du, direkt in die Kamera.\n\nGestern kamen Fragen, hier sind meine Antworten."),
        t("✏️ Eine Frage von gestern und deine Antwort darauf, Namen abdecken. Für jede weitere Frage diese Folie kopieren."),
        cta("Wer mit der Nische anfangen will:", LINK_NISCHE),
        t("Schönes Wochenende!"),
    ]),
    ("2026-11-21", "Sa", "danach", "eine Folie", "Inspiration", "Gratis für dich", [
        bild("✏️ Samstagsbild.\n\nIn ein paar Minuten weisst du, welche Nische in deinem Network zu dir passt. Gratis.", LINK_NISCHE),
        t("Geniess das Wochenende!"),
    ]),
    ("2026-11-22", "So", "danach", "eine Folie", "Inspiration", "Eine ruhige Minute", [
        bild("✏️ Sonntagsbild.\n\nWas machst du am Sonntag nur für dich?", FRAGE),
        t("Ich such mir jetzt meine ruhige Minute."),
    ]),
    ("2026-11-23", "Mo", "danach", "lehrreich", "einen krassen Tipp", "Drei Fragen vor dem Bauen", [
        bild("✏️ Montagsfoto.\n\nBevor ich ein neues Tool baue, beantworte ich mir drei Fragen."),
        t("Drei Fragen vor jedem Tool\n\n1. Wer soll es ausfüllen?\n2. Welche Frage beantwortet es ihr?\n3. Was ist danach der nächste Schritt?"),
        learning("Ein Tool ohne nächsten Schritt ist ein nettes Spielzeug."),
        frage("Welche der drei Fragen ist für dich die schwierigste?"),
        cta("Die erste beantwortet dir der Nischengenerator:", LINK_NISCHE),
        t("Gute Woche dir!"),
    ]),
    ("2026-11-24", "Di", "danach", "persönlich", "warum mit mir", "Warum es den Story-Generator gibt", [
        bild("✏️ Foto von dir am Laptop.\n\nViele Frauen, mit denen ich arbeite, tun sich schwer mit Storytelling. Darum hab ich daraus ein Tool gebaut."),
        t("Man gibt eine Alltagssituation und das eigene Produkt ein, und es macht daraus eine Story mit Brücke zum Angebot."),
        t("✏️ Wie die ersten Rückmeldungen waren."),
        learning("Das Problem, das du am häufigsten hörst, ist dein nächstes Tool."),
        frage("Womit tust du dich in deinen Storys am schwersten?"),
        t("Bis morgen!"),
    ]),
    ("2026-11-25", "Mi", "danach", "Community", "Inspiration", "Wo stehst du gerade?", [
        bild("✏️ Ein Bild von heute.\n\nNoch fünf Wochen bis Jahresende, und ich will wissen, wo du gerade stehst."),
        umfrage("Hast du ein eigenes Gratis-Angebot?", "Ja", "Noch nicht"),
        t("✏️ Wo du selbst vor einem Jahr gestanden bist, ein Satz."),
        cta("Wenn du noch ganz am Anfang bist:", LINK_NISCHE),
        t("Ich les jede Antwort."),
    ]),
    ("2026-11-26", "Do", "danach", "Tipp", "einen krassen Tipp", "Nach dem Tool kommt das Angebot", [
        bild("✏️ Foto von heute.\n\nWer dein Gratis-Tool ausgefüllt hat, will meistens wissen, wie es weitergeht."),
        t("Darum gehört ans Ende jedes Tools ein Satz, der den nächsten Schritt zeigt: ein Gespräch, ein kleines Angebot oder eine Nachricht an dich."),
        learning("Das Ergebnis deines Tools ist der beste Moment für deinen nächsten Schritt."),
        frage("Was ist bei dir der nächste Schritt nach dem Gratis-Angebot?"),
        t("Bis morgen!"),
    ]),
    ("2026-11-27", "Fr", "danach", "eigene Meinung", "warum mit mir", "Black Friday", [
        bild("✏️ Du, direkt in die Kamera.\n\nHeute ist Black Friday, und bei mir gibt es heute nichts zu kaufen."),
        t("✏️ Was du heute stattdessen machst."),
        umfrage("Kaufst du heute etwas?", "Ja", "Nein"),
        cta("Etwas, das gar nichts kostet:", LINK_NISCHE),
        t("Schönes Wochenende!"),
    ]),
    ("2026-11-28", "Sa", "danach", "eine Folie", "Inspiration", "Deine Nische", [
        bild("✏️ Samstagsbild.\n\nWer im Dezember mit einer klaren Nische starten will: Der Nischengenerator ist gratis.", LINK_NISCHE),
        t("Geniess den Samstag!"),
    ]),
    ("2026-11-29", "So", "danach", "eine Folie", "Inspiration", "Erster Advent", [
        bild("✏️ Adventsbild.\n\nSchönen ersten Advent! Was machst du heute?", FRAGE),
        t("Ich wünsch dir einen ruhigen Adventssonntag."),
    ]),
    ("2026-11-30", "Mo", "danach", "Rückblick", "Inspiration", "Danke für diesen Monat", [
        bild("✏️ Foto von dir.\n\nIm November haben in meinem Workshop Frauen ihr erstes eigenes Tool gebaut."),
        t("✏️ Was dich in diesem Monat am meisten gefreut hat."),
        frage("Worüber soll ich im Dezember mehr erzählen?"),
        t("Danke, dass du dabei warst."),
    ]),
]

KICK = "drei Tage Energie-Kickstart, gratis per Mail"

D_NEU = [
    ("2026-10-30", "Fr", "Aktivieren", "eigene Meinung", "Inspiration", "Müde ist nicht normal", [
        bild("✏️ Du, direkt in die Kamera.\n\nLange hab ich gedacht: Ich bin halt müde, mit vier Kindern ist das so."),
        t("✏️ Ein Moment, in dem du damals gemerkt hast, wie müde du bist. Wo warst du, was ist passiert?"),
        umfrage("Hältst du Müdigkeit für normal?", "Ja, leider", "Nein"),
        t("Heute weiss ich, dass Müdigkeit viele Ursachen haben kann und man einiges davon selbst in der Hand hat."),
        learning("Müde sein mit Kindern ist häufig. Hinnehmen musst du es trotzdem nicht."),
        cta(f"Wenn du ausprobieren willst, womit ich angefangen habe: {KICK}.", LINK_KICK),
        t("So, ich geh jetzt meine Schritte machen."),
    ]),
    ("2026-10-31", "Sa", "Aktivieren", "eine Folie", "Inspiration", "Auch am Samstag", [
        bild("✏️ Dein Samstagsfrühstück.\n\nWorauf ich auch am Wochenende nicht verzichte: ein Frühstück mit genug Protein."),
        frage("Was gibt's bei dir heute zum Frühstück?"),
    ]),
    ("2026-11-01", "So", "Aktivieren", "eine Folie", "Inspiration", "Eine Sache für November", [
        bild("✏️ Sonntagsbild.\n\nNeuer Monat, und ich nehm mir für November eine einzige Sache vor."),
        t("✏️ Deine eine Sache für November."),
        frage("Was nimmst du dir für November vor?"),
    ]),
    ("2026-11-02", "Mo", "Vertrauen", "Tipp", "einen krassen Tipp", "8000 Schritte", [
        bild("✏️ Foto von draussen.\n\nDer Tipp, der mich keinen Rappen gekostet hat: Schritte zählen."),
        t("Ich nehme mir 8000 am Tag vor. ✏️ Dein bester Trick, im Mama-Alltag auf mehr Schritte zu kommen."),
        frage("Wie viele Schritte machst du an einem normalen Tag?"),
        learning("Bewegung muss kein Training sein. Jeder Weg zu Fuss zählt."),
        cta(f"Wenn du mehr solche kleinen Schritte willst: {KICK}.", LINK_KICK),
        t("Ich geh jetzt noch eine Runde raus."),
    ]),
    ("2026-11-03", "Di", "Vertrauen", "persönlich", "warum mit mir", "Um Viertel nach fünf", [
        bild("✏️ Foto von deinem Training oder deinen Turnschuhen.\n\nUm Viertel nach fünf steht bei mir das Krafttraining an, dreimal die Woche."),
        t("✏️ Ein ehrlicher Satz, wie du früher über Krafttraining gedacht hast."),
        umfrage("Machst du Krafttraining?", "Ja", "Noch nicht"),
        t("Krafttraining ist bei mir einer von vier Bausteinen. Die anderen drei sind Protein, Schritte und mein Nährstoffpaket."),
        learning("Klein anfangen zählt mehr als perfekt anfangen."),
        t("So, und jetzt ruft der Alltag mit vier Kindern."),
    ]),
    ("2026-11-04", "Mi", "Vertrauen", "Community", "Inspiration", "Was raubt dir Energie?", [
        bild("✏️ Ein Bild von heute.\n\nIch will von dir wissen, was dir gerade Energie raubt, und mache daraus diese Woche eine Story."),
        umfrage("Was raubt dir gerade am meisten Energie?", "Schlaf", "Alltag"),
        frage("Oder etwas ganz anderes? Schreib's mir."),
        cta(f"Bis dahin: {KICK}.", LINK_KICK),
        t("Ich les jede Antwort. Bis Freitag!"),
    ]),
    ("2026-11-05", "Do", "Vertrauen", "Alltag", "warum mit mir", "Mein Moment am Abend", [
        bild("✏️ Foto von deinen Ölen.\n\nAbends creme ich mich mit meinen Ölen ein, und das ist der Moment, der nur mir gehört."),
        t("✏️ Welches Öl du dafür nimmst und wie es sich anfühlt, zwei Sätze."),
        umfrage("Hast du einen Moment am Tag nur für dich?", "Ja", "Selten"),
        learning("Ein kleines Ritual, das nur dir gehört, ist kein Luxus."),
        t("Für mich ist jetzt genau dieser Moment."),
    ]),
    ("2026-11-06", "Fr", "Vertrauen", "Antwort", "einen krassen Tipp", "Deine Antworten", [
        bild("✏️ Du, direkt in die Kamera.\n\nAm Mittwoch hab ich gefragt, was dir Energie raubt, und eine Antwort kam besonders oft."),
        t("✏️ Das Thema, das am häufigsten kam, und dein ehrlicher Tipp dazu. Kam keine Antwort, nimm eins aus deinem Alltag."),
        frage("Geht's dir auch so? Erzähl mir davon."),
        cta(f"Wenn du ausprobieren willst, womit ich angefangen habe: {KICK}.", LINK_KICK),
        t("Schönes Wochenende!"),
    ]),
    ("2026-11-07", "Sa", "Vertrauen", "eine Folie", "einen krassen Tipp", "Drei Tage reinschnuppern", [
        bild("✏️ Samstagsbild.\n\nDrei kleine Schritte, drei Tage, gratis per Mail. Für alle, die mal ausprobieren wollen.", LINK_KICK),
        t("Ich geh jetzt raus. Geniess den Samstag!"),
    ]),
    ("2026-11-08", "So", "Vertrauen", "eine Folie", "Inspiration", "Was gibt dir Energie?", [
        bild("✏️ Sonntagsbild.\n\nWas gibt dir am Wochenende Energie?", FRAGE),
        t("Bei mir ist es Zeit im Garten."),
    ]),
    ("2026-11-09", "Mo", "Community", "Tipp", "einen krassen Tipp", "Auch mittags 30 Gramm", [
        bild("✏️ Dein Mittagessen von heute.\n\nWie viel Protein ist eigentlich in deinem Mittagessen?"),
        t("Ich halte mich an eine Faustregel: mindestens 30 Gramm Protein pro Mahlzeit, auch mittags."),
        learning("✏️ Deine liebste Kombination mit 30 Gramm Protein, mit Mengen."),
        frage("Was isst du am liebsten zu Mittag?"),
        cta(f"Mehr solche Tipps: {KICK}.", LINK_KICK),
        t("En Guete!"),
    ]),
    ("2026-11-10", "Di", "Community", "persönlich", "warum mit mir", "Müde aufgewacht", [
        bild("✏️ Foto von dir am Morgen.\n\nFrüher bin ich müde aufgewacht, egal wie lange ich geschlafen habe."),
        t("✏️ Ein Morgen von damals, an den du dich erinnerst. Wo warst du, wie hat es sich angefühlt?"),
        t("Heute schlafe ich acht Stunden durch. Bei mir war es die Kombination aus Protein, Krafttraining, Schritten und meinem Nährstoffpaket."),
        umfrage("Wie schläfst du?", "Gut", "Schlecht"),
        learning("Bei mir haben vier kleine Dinge jeden Tag mehr bewirkt als eine grosse Veränderung."),
        t("So, und jetzt startet mein Tag."),
    ]),
    ("2026-11-11", "Mi", "Community", "Community", "Inspiration", "Wenn die Kinder schlafen", [
        bild("✏️ Ein gemütliches Abendbild.\n\nWenn die Kinder im Bett sind, lese ich. Jeden Abend, meistens einen Krimi."),
        umfrage("Was machst du zuerst, wenn die Kinder schlafen?", "Aufräumen", "Sofa"),
        frage("Hast du ein festes Abendritual?"),
        cta(f"Wenn du mehr Energie für deine Abende willst: {KICK}.", LINK_KICK),
        t("Mein Buch wartet. Gute Nacht!"),
    ]),
    ("2026-11-12", "Do", "Community", "Alltag", "warum mit mir", "Ein Blick in meinen Tag", [
        bild("✏️ Ein Foto aus deinem Tag heute.\n\nMein Tag mit vier Kindern hat einen Moment, den ich mir nicht nehmen lasse."),
        t("✏️ Ein, zwei Sätze, wie dein Tag heute aussieht und wo du dir Zeit für dich nimmst."),
        frage("Wann hast du heute an dich gedacht?"),
        learning("Zeit für dich bleibt selten übrig. Sie gehört in den Kalender, wie jeder andere Termin."),
        t("Bis morgen!"),
    ]),
    ("2026-11-13", "Fr", "Community", "eigene Meinung", "einen krassen Tipp", "Essen statt Shakes", [
        bild("✏️ Du, direkt in die Kamera.\n\nMeine Meinung, die nicht allen gefällt: Ich brauche keine Shakes für mein Protein. Ich esse es."),
        t("Der Ernährungsmediziner Matthias Riedl warnt in seinem Buch Gamechanger Protein sogar vor hochverarbeiteten Proteinprodukten."),
        umfrage("Shake oder richtiges Essen?", "Shake", "Essen"),
        t("✏️ Was du heute gegessen hast, um auf dein Protein zu kommen."),
        cta(f"Wie ich das im Alltag mache: {KICK}.", LINK_KICK),
        t("Schönes Wochenende!"),
    ]),
    ("2026-11-14", "Sa", "Community", "eine Folie", "einen krassen Tipp", "Drei Tage reinschnuppern", [
        bild("✏️ Samstagsbild.\n\nWer mal drei Tage ausprobieren will, wie ich esse und mich bewege: Der Kickstart ist gratis.", LINK_KICK),
        t("Jetzt aber Wochenende."),
    ]),
    ("2026-11-15", "So", "Community", "eine Folie", "Inspiration", "Wie war deine Woche?", [
        bild("✏️ Sonntagsbild.\n\nWie war deine Woche? Erzähl mir in einem Satz.", FRAGE),
        t("Ich les jede Antwort. Schönen Sonntag!"),
    ]),
    ("2026-11-16", "Mo", "Vertrauen", "Tipp", "einen krassen Tipp", "Protein schon am Morgen planen", [
        bild("✏️ Foto von deinem Abendessen.\n\nWer um sechs Uhr abends erst überlegt, was es gibt, landet schnell bei Brot und Käse. Ich kenn das."),
        t("Mein Tipp: Plan dein Protein schon am Morgen. ✏️ Wie du das machst, zum Beispiel was du am Morgen schon aus dem Tiefkühler nimmst."),
        umfrage("Planst du dein Essen?", "Ja", "Spontan"),
        learning("Der Plan am Morgen entscheidet, was am Abend auf dem Teller landet."),
        cta(f"Mehr solche Tipps: {KICK}.", LINK_KICK),
        t("Ich weiss jedenfalls schon, was es heute gibt."),
    ]),
    ("2026-11-17", "Di", "Vertrauen", "Geschichte", "warum mit mir", "Was sich bei mir verändert hat", [
        bild("✏️ Ein Foto von dir.\n\nDas grösste Geschenk der letzten Zeit hat mit der Waage nichts zu tun."),
        t("Es ist, dass ich am Nachmittag noch Energie für meine Kinder habe."),
        t("✏️ Ein konkreter Moment, an dem du das zuletzt gemerkt hast. Wo wart ihr, was habt ihr gemacht?"),
        frage("Wofür hättest du gern mehr Energie?"),
        learning("Wie viel Energie du hast, merkst du am Nachmittag mit den Kindern."),
        cta(f"Wenn du ausprobieren willst, womit ich angefangen habe: {KICK}.", LINK_KICK),
        t("So, jetzt ist Nachmittag. Bis morgen!"),
    ]),
    ("2026-11-18", "Mi", "Vertrauen", "Community", "Inspiration", "Frag mich alles", [
        bild("✏️ Ein Bild von heute.\n\nHeute darfst du mich alles fragen: Ernährung, Training, Öle oder wie ich das mit vier Kindern mache."),
        frage("Was willst du von mir wissen?"),
        t("Ich beantworte die Fragen morgen in meinen Storys."),
    ]),
    ("2026-11-19", "Do", "Vertrauen", "Antwort", "einen krassen Tipp", "Ich beantworte deine Fragen", [
        bild("✏️ Du, direkt in die Kamera.\n\nGestern kamen Fragen, hier sind meine Antworten."),
        t("✏️ Eine Frage von gestern und deine Antwort darauf. Frage als Screenshot oder abgetippt, Namen abdecken. Für jede weitere Frage diese Folie kopieren."),
        frage("Noch eine Frage offen? Schreib mir."),
        cta(f"Und wer gleich ausprobieren will: {KICK}.", LINK_KICK),
        t("Danke für all die Fragen!"),
    ]),
    ("2026-11-20", "Fr", "Vertrauen", "eigene Meinung", "Inspiration", "Schenk dir selbst auch was", [
        bild("✏️ Du, direkt in die Kamera.\n\nWir Mamas denken im Dezember an alle Geschenke, nur an uns selbst zuletzt."),
        t("✏️ Was du dir letztes Jahr selbst geschenkt hast, oder warum nichts."),
        frage("Was schenkst du dir dieses Jahr selbst?"),
        learning("Nimm dir eine Sache vor, die nur dir guttut, und zieh sie durch."),
        t("Schönes Wochenende!"),
    ]),
    ("2026-11-21", "Sa", "Vertrauen", "eine Folie", "einen krassen Tipp", "Drei Tage reinschnuppern", [
        bild("✏️ Samstagsbild.\n\nDrei Tage, drei kleine Schritte zu mehr Energie. Gratis per Mail.", LINK_KICK),
        t("Geniess den Samstag!"),
    ]),
    ("2026-11-22", "So", "Vertrauen", "eine Folie", "Inspiration", "Eine ruhige Minute", [
        bild("✏️ Sonntagsbild.\n\nWo findest du am Sonntag deine ruhige Minute? Zeig's mir.", FRAGE),
        t("Ich such mir meine jetzt."),
    ]),
    ("2026-11-23", "Mo", "Community", "Community", "Inspiration", "Wie sieht dein Dezember aus?", [
        bild("✏️ Montagsfoto.\n\nNoch eine Woche, dann ist Dezember, und ich will wissen, wie es dir damit geht."),
        umfrage("Freust du dich auf den Dezember?", "Sehr", "Er stresst mich"),
        t("✏️ Wie dein Dezember aussieht, ein Satz, ehrlich."),
        cta(f"Wer vor dem Dezember durchatmen will: {KICK}.", LINK_KICK),
        t("Gute Woche dir!"),
    ]),
    ("2026-11-24", "Di", "Community", "Tipp", "einen krassen Tipp", "Was ich nie weglasse", [
        bild("✏️ Ein winterliches Bild.\n\nIn vollen Wochen lass ich vieles weg, zwei Dinge nie."),
        t("Das Protein am Morgen und meine Schritte."),
        t("✏️ Was du in der Adventszeit bewusst weglässt."),
        frage("Was lässt du dieses Jahr weg?"),
        learning("Wenn alles zu viel wird, lass weg, was nur gut aussieht, und behalte, was dich trägt."),
        t("Bis morgen!"),
    ]),
    ("2026-11-25", "Mi", "Community", "Alltag", "warum mit mir", "Wie Winter riecht", [
        bild("✏️ Foto von deinem Diffuser oder deinem Lieblingsöl im Winter.\n\nWinter riecht bei mir nach einem ganz bestimmten Öl."),
        t("✏️ Welcher Duft für dich nach Winter riecht und warum."),
        umfrage("Lieber warm oder frisch?", "Warm", "Frisch"),
        cta(f"Mehr aus meinem Alltag: {KICK}.", LINK_KICK),
        t("Schönen Abend dir."),
    ]),
    ("2026-11-26", "Do", "Community", "Geschichte", "warum mit mir", "Wie ich zu den Ölen kam", [
        bild("✏️ Foto von dir.\n\nZu den Ölen bin ich über einen Umweg gekommen, und der hatte mit einer To-do-Liste zu tun."),
        t("Ich hab Mamas gezeigt, wie sie ihre To-do-Liste halbieren. Dabei kamen wir ins Gespräch, und irgendwann ging es auch um das, was mir im Alltag hilft."),
        t("✏️ Ein Satz, was die Öle heute für dich bedeuten."),
        frage("Wie bist du hier auf mich gestossen?"),
        t("Danke, dass du da bist."),
    ]),
    ("2026-11-27", "Fr", "Community", "eigene Meinung", "einen krassen Tipp", "Black Friday", [
        bild("✏️ Du, direkt in die Kamera.\n\nHeute ist Black Friday, und mein Tipp ist einfach: Kauf nichts, was du im Januar bereust."),
        umfrage("Kaufst du heute etwas?", "Ja", "Nein"),
        t("✏️ Was du dir heute gönnst, das nichts kostet."),
        cta(f"Etwas, das gar nichts kostet: {KICK}.", LINK_KICK),
        t("Schönes Wochenende!"),
    ]),
    ("2026-11-28", "Sa", "Community", "eine Folie", "einen krassen Tipp", "Drei Tage reinschnuppern", [
        bild(f"✏️ Samstagsbild.\n\nFür alle, die vor dem Dezember noch durchatmen wollen: {KICK}.", LINK_KICK),
        t("Geniess das Wochenende!"),
    ]),
    ("2026-11-29", "So", "Community", "eine Folie", "Inspiration", "Erster Advent", [
        bild("✏️ Adventsbild.\n\nSchönen ersten Advent! Was machst du heute?", FRAGE),
        t("Ich wünsch dir einen ruhigen Adventssonntag."),
    ]),
    ("2026-11-30", "Mo", "Community", "Rückblick", "Inspiration", "Danke für diesen Monat", [
        bild("✏️ Foto von dir.\n\nEin Monat, seit ich hier wieder jeden Tag bin, und ich hab jede Antwort gelesen."),
        t("✏️ Was dich in diesem Monat an den Antworten am meisten berührt hat."),
        frage("Worüber soll ich im Dezember mehr erzählen?"),
        cta(f"Und wer den Dezember mit mehr Energie starten will: {KICK}.", LINK_KICK),
        t("Danke, dass du dabei warst."),
    ]),
]

AB = "2026-10-30"


def ersetzen(alt, neu):
    """Vor dem 30.10. bleibt die gepostete Fassung, ab dann gilt die Neufassung."""
    return [x for x in alt if x[0] < AB] + neu


EIGENE = [
    (r"[Dd]eine[rn]? Kundin", "mentoring", "Zielgruppen-Ebene: „deine Kundin“"),
    (r"drei Kinder|Mama von 3|3 Kinder", None, "Kinderzahl falsch"),
    (r"\b199\b", "mentoring", "199 nur auf der Danke-Seite"),
    (r"\b(heilt|heilen|gegen (Krebs|Depression|Angst))\b", "doterra", "Wirkversprechen"),
]


def sticker_aus(text):
    """Übersetzt die Sticker-Angabe der Vorlage in Feld und Beschriftung der Story-Bibliothek."""
    text = text or ""
    if text.startswith("Link-Sticker:"):
        return "link", text.split(":", 1)[1].strip()
    if text.startswith("Countdown-Sticker"):
        return "countdown", text.split("·", 1)[1].strip() if "·" in text else ""
    m = re.match(r"Sticker „(.+?)“", text)
    if m:
        return "frage", m.group(1)
    if text == "Frage-Sticker":
        return "frage", ""
    return None, ""


def kennung(profil, datum, tag):
    kw = datetime.date.fromisoformat(datum).isocalendar()[1]
    return "kw%d-story-%s-nov-%s" % (kw, "m" if profil == "mentoring" else "d", tag.lower())


def bauen(profil, tage):
    GESTALT.FOTOS = FOTOS[profil]
    jetzt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    docs = []
    for nr, (datum, tag, phase, art, mit, titel, frames) in enumerate(tage):
        roh = [dict({"id": f"s{i+1}", "optA": "", "optB": ""}, **f) for i, f in enumerate(frames)]
        # „✏️ Montagsfoto.\n\nEchter Satz“: die Foto-Anweisung gehört in die Notiz, nie gross ins Bild
        for f in roh:
            teile = f["text"].split("\n\n", 1)
            foto_anweisung = re.compile(r"(?i)foto|bild|kamera|screenshot|frühstück|mittagessen|abendessen")
            if (f["text"].startswith("✏️") and len(teile) == 2
                    and (not teile[1].startswith("✏️") or foto_anweisung.search(teile[0]))):
                f["notiz"] = (teile[0][2:].strip() + " " + f.get("notiz", "")).strip()
                f["text"] = teile[1]
            elif (f["text"].startswith("✏️") and len(teile) == 1 and f.get("layout") == "bild"
                  and foto_anweisung.search(f["text"])):
                # reine Foto-Anweisung: Foto ohne Text, Anweisung auf die Karte
                f["notiz"] = (f["text"][2:].strip() + " " + f.get("notiz", "")).strip()
                f["text"] = ""
        doc = {"datum": datum, "frames": roh}
        neu = GESTALT.gestalten(doc, nr)
        for alt, n in zip(roh, neu):
            art_st, beschr = sticker_aus(alt.get("cta"))
            if art_st and alt.get("layout") not in ("umfrage",):
                n["sticker"] = art_st
                n["stickerText"] = beschr
                n.setdefault("stickerPos", 66)
            if alt.get("notiz"):
                n["notiz"] = (alt["notiz"] + " · " + n["notiz"]) if n.get("notiz") else alt["notiz"]
        d = datetime.date.fromisoformat(datum)
        wort = "November" if profil == "mentoring" else "doTERRA"
        docs.append((kennung(profil, datum, tag), {
            "brand": BRAND[profil], "datum": datum, "profil": profil, "textfrei": False,
            "name": "%d.%d. · %s · %s · %s" % (d.day, d.month, GESTALT.WOCHENTAG[d.weekday()], wort, titel),
            "hinweis": (f"{'Monatsplan Nov' if profil == 'mentoring' else 'doTERRA Nov'} · Phase: {phase} · "
                        f"Story-Art: {art} · Gibt ihr heute mit: {mit} · ✏️ = Alltag von heute ergänzen oder "
                        f"löschen. Gerüst aus scripts/launch/storys-november.py"),
            "updatedAt": jetzt,
            "frames": neu,
        }))
    return docs


def pruefen(docs):
    funde = []
    for kenn, doc in docs:
        for schwere, befund, stelle in PRUEF.pruefe(doc, kenn, art="storys"):
            funde.append((schwere, kenn, befund, stelle))
        text = " ".join(" ".join(str(f.get(k, "")) for k in ("text", "klein", "eyebrow", "stickerText"))
                        + " " + " ".join(f.get("punkte", [])) for f in doc["frames"])
        for muster, nur, was in EIGENE:
            if (nur is None or nur == doc["profil"]) and re.search(muster, text):
                funde.append((1, kenn, was, re.search(muster, text).group(0)))
    return funde


def main():
    docs = (bauen("mentoring", ersetzen(MENTORING, M_NEU))
            + bauen("doterra", ersetzen(DOTERRA, D_NEU)))
    funde = pruefen(docs)
    for schwere, kenn, befund, stelle in funde:
        print(("✗ " if schwere == 1 else "? ") + f"{kenn}: {befund} — {stelle}")
    if any(s == 1 for s, *_ in funde) and "--trotzdem" not in sys.argv:
        sys.exit("Harte Funde — erst korrigieren.")
    ZIEL.mkdir(parents=True, exist_ok=True)
    for kenn, doc in docs:
        (ZIEL / f"{kenn}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(docs)} Story-Sequenzen · {sum(len(d['frames']) for _, d in docs)} Folien → {ZIEL}")


if __name__ == "__main__":
    main()
