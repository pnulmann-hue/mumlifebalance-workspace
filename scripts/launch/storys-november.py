"""
Storys 26.10.–30.11.2026 für beide Profile — fertig vorgeschrieben und gestaltet,
damit Patricia nur noch den Alltag ergänzt. Zwilling von storys-ki-launch.py.

  python scripts/launch/storys-november.py
  # danach: ArtifactData batch set (Cockpit, Sammlung "storys") mit den Dateien in
  #         outputs/cockpit/abgleich/storys-november/

Festgelegt mit Patricia am 25.10.2026 (Monatsplan outputs/monatsplaene/2026-11-*.md):

Mentoring  KW44 Inspiration · KW45 Einladung Story-Challenge · KW46 Challenge läuft
           (9.–15.11., WhatsApp-Gruppe) · KW47 Ergebnisse + Blick in die Kundenmaschine ·
           23.–30.11. Kasse Instagram-Kundenmaschine 333, ohne Calls, ohne Webinar.
doTERRA    Energie-Routine (Start jeden 10., Bestellschluss Ende Vormonat) ·
           Gratis-Kickstart · Business sichtbar (Rise to Lead) · ab 16.11. Geschenke.

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

LINK_STORY = "Link-Sticker: mumlifebalance.ch/story-challenge/"
LINK_BIO = "Link-Sticker: mumlifebalance.ch/bio-check/"
LINK_IKM = "Link-Sticker: mumlifebalance.thrivecart.com/instagram-kundenmaschine/"
LINK_ROUTINE = "Link-Sticker: mumlifebalance.ch/energieroutine/"
LINK_KICK = "Link-Sticker: mumlifebalance.ch/energie-kickstart/"
WARTELISTE = "Sticker „Ich will dabei sein“ → DM"
CD_ANMELDUNG = "Countdown-Sticker · Mo 2.11. 07:00"
CD_KASSE = "Countdown-Sticker · Mo 23.11. 07:00"
DM_BUSINESS = "Sticker „Erzähl mir mehr“ → DM"
DM_IDEEN = "Sticker „Ideen bitte“ → DM"

FOTOS = {"mentoring": ["s04.jpg", "s03.jpg", "s01.jpg", "s05.jpg", "s02.jpg", "s06.jpg"],
         "doterra": ["s09.jpg", "s11.jpg", "s07.jpg", "s12.jpg", "s08.jpg", "s10.jpg"]}
BRAND = {"mentoring": "mlb_light", "doterra": "oele"}

# (datum, tag, phase, story-art, gibt-ihr-mit, titel, folien)
MENTORING = [
    # ---------------- KW44 · Inspiration, Warteliste Story-Challenge ----------------
    ("2026-10-26", "Mo", "Inspiration", "lehrreich", "einen krassen Tipp", "Warum auf deine Storys niemand antwortet", [
        bild("✏️ Dein Montagmorgen, ein Satz dazu.\n\nUnd dann eine Frage: Wann hat dir zuletzt jemand auf eine Story geantwortet?"),
        t("Bei mir war die ehrliche Antwort lange: fast nie. Zwei Jahre lang hab ich gepostet, und es kam kaum etwas zurück."),
        t("Heute weiss ich, woran es lag. Ich hab erzählt und selten gefragt, und wenn ich gefragt habe, musste man zuerst lange nachdenken."),
        t("Zum Screenshotten\n\nEine Frage, auf die man mit einem Tipp antworten kann, bekommt mehr Antworten als eine, über die man nachdenken muss.\n\nAlso lieber eine Umfrage mit zwei Antworten als „Was meint ihr dazu?“."),
        umfrage("Wie oft antwortet dir jemand auf deine Storys?", "Fast nie", "Ab und zu"),
        cta("Ab 9. November mach ich sieben Tage lang eine Story-Challenge, gratis. Willst du dabei sein?", WARTELISTE),
    ]),
    ("2026-10-27", "Di", "Inspiration", "persönlich", "warum mit mir", "Als meine Posts ins Leere gingen", [
        bild("✏️ Ein Foto von dir heute.\n\nHeute mal ein Blick zurück, auf den ich nicht besonders stolz bin."),
        t("2023 hab ich meinen Job gekündigt. Danach kamen zwei Jahre mit Programmen, die niemand gekauft hat, und Posts, auf die kaum jemand reagiert hat."),
        t("Ich hab mich damals hinter dem Produkt versteckt. Die Leute haben gesehen, was ich verkaufe, aber nicht, wer ich bin."),
        t("Das ist im Network völlig normal, und ich meine das echt nicht vorwurfsvoll. Das Produkt gibt es aber mehrfach. Dich gibt es nur einmal."),
        frage("Erkennst du dich da wieder?"),
        cta("Genau darum geht es in meiner Story-Challenge ab 9. November. Tipp auf den Sticker, dann bist du auf der Liste.", WARTELISTE),
    ]),
    ("2026-10-28", "Mi", "Inspiration", "Inspiration", "Inspiration", "Verstanden fühlen", [
        bild("✏️ Ein Bild von heute, gern ohne Handy."),
        t("Ein Satz aus meinem Workbook, den ich mir selbst immer wieder sagen muss: Menschen kaufen nicht wegen perfekter Storys. Sie kaufen, wenn sie sich verstanden fühlen."),
        t("Verstanden fühlt sich jemand, wenn sie merkt: Die weiss, wie mein Alltag aussieht. Das schafft eine Szene aus deinem Tag oft besser als jedes Produktbild."),
        t("Heute ausprobieren\n\nZeig eine Szene aus deinem Tag, die nichts mit deinem Produkt zu tun hat, und frag am Schluss mit einer Umfrage, ob es bei ihnen auch so ist."),
        cta("Schick mir deine Story, wenn du's probiert hast. Und wenn du mehr davon willst: Ab 9. November gibt es sieben Tage dazu.", WARTELISTE),
    ]),
    ("2026-10-29", "Do", "Inspiration", "Blick hinter die Kulissen", "einen krassen Tipp", "Sieben Tage, sieben Aufgaben", [
        bild("✏️ Blick auf deinen Schreibtisch oder Bildschirm, gern unscharf."),
        t("Ich hab in den letzten Tagen meine Story-Challenge nochmal durchgearbeitet. Sieben Tage, jeden Tag eine Aufgabe für deine Storys."),
        t("Am ersten Tag erzählst du deine Geschichte, am dritten etwas, das schiefgegangen ist, und am siebten ein Learning aus deinem Bereich."),
        umfrage("Welcher Tag wäre für dich der schwerste?", "Meine Geschichte", "Was schiefging"),
        cta("Ab 9. November, gratis, in einer WhatsApp-Gruppe. Die Anmeldung geht am Montag auf.", CD_ANMELDUNG),
    ]),
    ("2026-10-30", "Fr", "Inspiration", "eigene Meinung", "einen krassen Tipp", "Mehr posten hilft nicht", [
        bild("✏️ Du, direkt in die Kamera, oder ein Foto von dir."),
        t("Ich sag's heute mal gerade heraus: Noch mehr Storys am Tag bringen dir keine einzige Antwort mehr."),
        t("Ich hab's an meinen eigenen Zahlen gesehen. Im Juni hab ich 54 Beiträge gepostet, im Februar 12. Im Juni hat jeder Beitrag im Mittel nicht mal halb so viele Leute erreicht."),
        t("Was den Unterschied macht, ist, ob die Leute danach etwas zu sagen haben. Eine Story, auf die man antworten will, ist mehr wert als zehn, die man wegtippt."),
        umfrage("Wie viele Storys machst du an einem normalen Tag?", "1 bis 3", "Mehr als 5"),
        cta("In der Challenge machen wir genau das: weniger, dafür so, dass jemand antwortet.", WARTELISTE),
    ]),
    ("2026-10-31", "Sa", "Inspiration", "eine Folie", "Inspiration", "Am Montag geht die Anmeldung auf", [
        bild("✏️ Samstagsbild.\n\nAm Montag geht die Anmeldung für meine Story-Challenge auf. Sieben Tage, gratis, ab 9. November.", CD_ANMELDUNG),
    ]),
    ("2026-11-01", "So", "Inspiration", "eine Folie", "Inspiration", "Morgen früh", [
        bild("✏️ Sonntagsbild.\n\nHeute starten die Frauen aus meinem KI-Kurs, und morgen öffne ich die Anmeldung für die Story-Challenge. Tipp auf den Sticker, dann schreib ich dir.", WARTELISTE),
    ]),
    # ---------------- KW45 · Einladung Story-Challenge ----------------
    ("2026-11-02", "Mo", "Einladung", "lehrreich", "einen krassen Tipp", "Die Anmeldung ist offen", [
        bild("✏️ Montagsfoto.\n\nDie Anmeldung für die Story-Challenge ist offen! Vorher noch ein Tipp für heute."),
        t("Bevor du heute eine Produkt-Story postest, frag dich: Könnte jemand anderes aus deiner Firma genau dieselbe Story posten?"),
        t("Wenn ja, erzähl dazu, was du selbst damit erlebt hast. Erst dann wird es deine Story."),
        t("Was dich erwartet\n\n1. Sieben Tage, jeden Tag eine Aufgabe\n2. Ein Workbook mit Beispielen\n3. Eine WhatsApp-Gruppe zum Austauschen"),
        cta("Ab 9. November, gratis. Hier meldest du dich an:", LINK_STORY),
    ]),
    ("2026-11-03", "Di", "Einladung", "persönlich", "warum mit mir", "Mein Lieblingssnack", [
        bild("✏️ Ein Foto von etwas, das du gerade gern magst: Snack, Kaffee, Buch."),
        t("✏️ Ein, zwei Sätze, warum du das so magst."),
        t("Warum ich dir das zeige? Gespräche entstehen erst, wenn die Leute das Gefühl haben, dich zu kennen. In der Challenge ist das eine eigene Aufgabe."),
        frage("Was ist dein Lieblingssnack im Moment?"),
        cta("Am 9. November geht's los. Noch sechs Tage zum Anmelden.", LINK_STORY),
    ]),
    ("2026-11-04", "Mi", "Einladung", "Inspiration", "Inspiration", "Noch nicht aufgeben", [
        bild("✏️ Ein Bild von heute."),
        t("Eine Frau, die bei mir mit der Instagram-Kundenmaschine angefangen hat, war schon ein paar Jahre im Network, ohne dass es so richtig lief. Daneben arbeitet sie Teilzeit und will weg vom Job."),
        t("Heute ist sie in meiner Academy und hat mir geschrieben, warum sie nochmal weitergegangen ist."),
        t("Ihre Worte\n\n„Für mich war es ein jetzt oder nie Entscheid.“\n\nUnd am Schluss: „… nochmals weiterzugehen und noch nicht aufzugeben.“"),
        t("Viele, die zu mir kommen, haben schon einmal aufgehört. Das ist normal. Wichtig ist, dass du wieder anfängst, und zwar mit etwas Kleinem."),
        cta("Etwas Kleines: sieben Tage Storys, ab 9. November, gratis.", LINK_STORY),
    ]),
    ("2026-11-05", "Do", "Einladung", "Blick hinter die Kulissen", "einen krassen Tipp", "So sieht Tag 1 aus", [
        dict(bild("✏️ Ein Screenshot aus dem Workbook, zum Beispiel Tag 1.\n\nSo sieht Tag 1 im Workbook aus."), notiz="Screenshot vom Workbook einsetzen, Seite „Tag 1 – Vorstellungsrunde“."),
        t("An Tag 1 erzählst du eine Situation aus deinem Leben, die mit deinem Thema zu tun hat, und führst dann zu deinem Angebot."),
        t("Dazu nennst du drei Dinge, die deine Zielgruppe oft macht und von denen du abraten würdest, und was sie stattdessen tun kann."),
        frage("Was würdest du an Tag 1 erzählen?"),
        cta("Das Workbook bekommst du direkt nach der Anmeldung.", LINK_STORY),
    ]),
    ("2026-11-06", "Fr", "Einladung", "eigene Meinung", "warum mit mir", "Perfekt muss es nicht sein", [
        bild("✏️ Du, direkt in die Kamera."),
        t("✏️ Was magst du an dir in Storys nicht? Ein ehrlicher Satz, gern mit Humor."),
        t("Ich rede trotzdem in die Kamera, weil die Leute mich sonst nicht kennenlernen. Perfekt muss es nicht sein, man muss dich nur erkennen."),
        umfrage("Redest du in deinen Storys in die Kamera?", "Ja, regelmässig", "Lieber nicht"),
        cta("In der Challenge musst du nicht jeden Tag in die Kamera reden. Du entscheidest.", LINK_STORY),
    ]),
    ("2026-11-07", "Sa", "Einladung", "eine Folie", "Inspiration", "Übermorgen geht's los", [
        bild("✏️ Samstagsbild.\n\nÜbermorgen startet die Story-Challenge. Wer sich bis Sonntagabend anmeldet, ist ab Tag 1 dabei.", LINK_STORY),
    ]),
    ("2026-11-08", "So", "Einladung", "eine Folie", "Inspiration", "Letzter Tag vor dem Start", [
        bild("✏️ Sonntagsbild.\n\nMorgen um ✏️ Uhr kommt die erste Aufgabe in die Gruppe. Heute ist der letzte Tag, um von Anfang an dabei zu sein.", LINK_STORY),
    ]),
    # ---------------- KW46 · Story-Challenge läuft 9.–15.11. ----------------
    ("2026-11-09", "Mo", "Challenge", "Tag 1 · meine Geschichte", "warum mit mir", "Tag 1: die Liste für meinen Mann", [
        bild("✏️ Foto von heute Morgen.\n\nTag 1 der Story-Challenge! Ich mach die Aufgabe heute selbst mit."),
        t("Vor der Geburt meiner dritten Tochter hab ich meinem Mann eine Liste geschrieben. Alles, was ich als Mama nebenbei erledige, damit er weiss, was läuft, wenn ich im Spital bin."),
        t("Aus dieser Liste ist mein erstes Angebot entstanden: die drei Schritte, um deine To-do-Liste zu halbieren. 30 Bestellungen in zwei Tagen."),
        t("Über dieses Angebot kam ich mit Mamas ins Gespräch, die mich vorher nicht kannten. Und erst dann kamen die Öle zur Sprache."),
        frage("Was ist deine Geschichte? Erzähl sie heute in deinen Storys und verlinke mich, dann schau ich sie an."),
        cta("Du bist noch nicht dabei? Einsteigen geht die ganze Woche.", LINK_STORY),
    ]),
    ("2026-11-10", "Di", "Challenge", "Tag 2 · Privates + Tipp", "einen krassen Tipp", "Tag 2: etwas Privates", [
        bild("✏️ Foto von deinem Lieblingssnack, Kaffee oder was du gerade gern magst."),
        umfrage("✏️ Weisst du, was mein Lieblingssnack ist?", "Süss", "Salzig"),
        t("✏️ Was es ist und warum du es so magst, in zwei Sätzen."),
        t("Tag 2 in der Challenge\n\nGenau so baust du heute deine Story: etwas Privates zeigen und einen Tipp aus deinem Bereich daran hängen."),
        cta("Wer heute einsteigt, holt Tag 1 einfach nach.", LINK_STORY),
    ]),
    ("2026-11-11", "Mi", "Challenge", "Tag 3 · was schiefging", "warum mit mir", "Tag 3: was schiefgegangen ist", [
        bild("✏️ Foto von dir.\n\nTag 3 ist der unbequemste: Heute geht es um etwas, das schiefgegangen ist."),
        t("Bei mir waren das die zwei Jahre nach meiner Kündigung. Programme, die niemand gekauft hat, Posts ins Leere und dieser Blick auf den Kontostand."),
        t("Gefehlt haben mir drei Dinge: ein Thema, das man mir sofort abnimmt, ein fester Wochenrhythmus und Hilfe bei der Arbeit, die jede Woche wiederkommt."),
        t("Seit ich diese drei Dinge im Mai 2025 geändert habe, gab es keinen Monat mehr ohne Einkommen aus meiner Selbständigkeit."),
        frage("Was ist bei dir mal richtig schiefgegangen? Du musst es nicht posten, schreib's mir."),
        cta("Die Aufgabe für heute steht in der Gruppe.", LINK_STORY),
    ]),
    ("2026-11-12", "Do", "Challenge", "Tag 4 · Branche + Privates", "einen krassen Tipp", "Tag 4: was mir im Network auffällt", [
        bild("✏️ Foto von heute.\n\nHalbzeit! Tag 4 dreht sich um etwas, das dir in deiner Branche immer wieder auffällt."),
        t("Mir fällt im Network seit Jahren dasselbe auf: Wir lernen, wie man Produkte erklärt, und kaum jemand lernt, wie man über sich selbst redet."),
        t("Dabei ist genau das der Grund, warum jemand bei dir bestellt und nicht bei der Frau nebenan, die dasselbe verkauft."),
        umfrage("Was fällt dir leichter?", "Übers Produkt reden", "Über mich reden"),
        cta("Halbzeit, und einsteigen geht immer noch.", LINK_STORY),
    ]),
    ("2026-11-13", "Fr", "Challenge", "Tag 5 · Trend + Meinung", "einen krassen Tipp", "Tag 5: alle wollen viral gehen", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Tag 5, und ich mach's vor. Der Trend, der mir gerade überall auffällt: Alle wollen viral gehen."),
        t("Ich verstehe, warum, viele Aufrufe fühlen sich gut an. Meine zwei Beiträge mit den meisten Aufrufen haben aber kaum Reaktionen gebracht."),
        t("Meine Meinung dazu: Lieber weniger Leute, die dich kennen, als viele, die weiterwischen. Mit denen, die dich kennen, entstehen Gespräche."),
        frage("Welcher Trend in deiner Branche nervt dich?"),
        cta("Morgen und übermorgen noch, dann ist die Woche rum.", LINK_STORY),
    ]),
    ("2026-11-14", "Sa", "Challenge", "Tag 6 · etwas ohne Business", "warum mit mir", "Tag 6: meine Lieblingsserie", [
        bild("✏️ Foto von deiner Lieblingsserie, deinem Buch oder Film.\n\nTag 6 ist der leichteste: Heute redest du über etwas, das nichts mit deinem Business zu tun hat."),
        umfrage("Schon mal geschaut?", "Ja!", "Nie gehört"),
    ]),
    ("2026-11-15", "So", "Challenge", "Tag 7 · ein Learning", "einen krassen Tipp", "Tag 7: das letzte Learning", [
        bild("✏️ Sonntagsfoto.\n\nTag 7, der letzte. Heute teilst du ein Learning aus deinem Bereich, das deine Familie schon nicht mehr hören kann."),
        frage("Was war für dich der wichtigste Tag dieser Woche?"),
    ]),
    # ---------------- KW47 · Ergebnisse, Blick in die Kundenmaschine ----------------
    ("2026-11-16", "Mo", "Entdecken", "lehrreich", "einen krassen Tipp", "Die Woche in einer Folie", [
        bild("✏️ Montagsfoto.\n\nDie Challenge ist vorbei. Für alle, die nicht dabei waren, das Wichtigste in einer Folie."),
        t("Was ich aus sieben Tagen mitgebe\n\n1. Zeig dich, bevor du das Produkt zeigst\n2. Frag so, dass man mit einem Tipp antworten kann\n3. Erzähl auch, was schiefgegangen ist"),
        t("Das Ziel dahinter sind Nachrichten, in denen die Leute nach dir fragen und nicht nur nach dem Preis."),
        frage("Warst du dabei? Was nimmst du mit?"),
        cta("Wie wirkt dein Profil auf jemanden, der dich nicht kennt? Mein Bio-Check sagt es dir, gratis.", LINK_BIO),
    ]),
    ("2026-11-17", "Di", "Entdecken", "persönlich", "warum mit mir", "Nach der Challenge", [
        bild("✏️ Foto von dir.\n\n✏️ Ein Satz, wie es dir nach der Challenge-Woche geht."),
        dict(bild("Aus der Gruppe"), notiz="✏️ Screenshot einer Nachricht aus der WhatsApp-Gruppe einsetzen, Namen abdecken oder nur mit Okay. Gibt es keine, Folie weglassen."),
        t("✏️ Was hat dich in der Gruppe am meisten gefreut? Ein, zwei Sätze."),
        cta("Am Montag, 23. November, öffne ich die Instagram-Kundenmaschine. Das System hinter dem, was wir in der Challenge geübt haben.", CD_KASSE),
    ]),
    ("2026-11-18", "Mi", "Entdecken", "Inspiration", "einen krassen Tipp", "Vom Katalog zum Schaufenster", [
        bild("✏️ Ein Bild von heute."),
        t("Wie sieht ein Profil aus, bei dem die Leute von selbst fragen? Bei mir war es der Schritt vom Produktkatalog zum Schaufenster."),
        t("Im Katalog liegt alles nebeneinander, und man blättert weiter. Im Schaufenster sieht man auf einen Blick, wer da arbeitet und wofür sie steht."),
        t("Heute ausprobieren\n\nScroll durch deine letzten neun Beiträge, als würdest du dich nicht kennen. Weisst du danach, wofür du stehst?"),
        umfrage("Wie wirkt dein Profil gerade?", "Katalog", "Schaufenster"),
        cta("Wenn du's genau wissen willst, mach den Bio-Check, gratis.", LINK_BIO),
    ]),
    ("2026-11-19", "Do", "Entdecken", "Blick in den Kurs", "warum mit mir", "Was in der Kundenmaschine steckt", [
        dict(bild("✏️ Screenshot aus dem Kursbereich der Kundenmaschine, gern unscharf.\n\nEin Blick in die Instagram-Kundenmaschine."), notiz="Screenshot aus ThriveCart Learn, z.B. die Lektionsliste."),
        t("Die Challenge war für deine Storys. Die Instagram-Kundenmaschine ist das System für dein ganzes Profil."),
        t("Was drin ist\n\n1. Deine Content-Säulen, damit du weisst, worüber du postest\n2. Wie Beiträge und Storys gebaut sind, damit Vertrauen entsteht\n3. Wie aus Reaktionen Gespräche werden\n4. Eine Instagram-Routine, die ohne Motivation läuft"),
        t("31 Lektionen, zum Selbermachen in deinem Tempo."),
        frage("Was willst du über die Kundenmaschine wissen? Frag mich."),
        cta("Die Kasse geht am Montag auf.", CD_KASSE),
    ]),
    ("2026-11-20", "Fr", "Entdecken", "eigene Meinung", "warum mit mir", "Nach Plan statt nach Lust", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Meine Meinung, auch wenn sie unbequem ist: Wer nur postet, wenn sie Lust hat, postet im November fast gar nicht mehr."),
        t("Bei mir läuft Instagram mit vier Kindern und rund 18 Stunden Arbeit pro Woche, weil ich einen festen Rhythmus habe. Lust hab ich nicht jeden Tag."),
        umfrage("Postest du nach Plan oder nach Lust?", "Nach Plan", "Nach Lust"),
        cta("Wie dieser Rhythmus aussieht, steht in der Kundenmaschine. Ab Montag.", CD_KASSE),
    ]),
    ("2026-11-21", "Sa", "Entdecken", "eine Folie", "Inspiration", "Der nächste Schritt", [
        bild("✏️ Samstagsbild.\n\nAm Montag öffne ich die Instagram-Kundenmaschine. Wer nach der Challenge weitermachen will: Das ist der nächste Schritt.", CD_KASSE),
    ]),
    ("2026-11-22", "So", "Entdecken", "eine Folie", "Inspiration", "Morgen geht die Kasse auf", [
        bild("✏️ Sonntagsbild.\n\nMorgen früh geht die Kasse für die Kundenmaschine auf, für eine Woche.", CD_KASSE),
    ]),
    # ---------------- KW48/49 · Kasse Kundenmaschine 23.–30.11. ----------------
    ("2026-11-23", "Mo", "Kasse offen", "Fakten", "warum mit mir", "Die Kasse ist offen", [
        bild("✏️ Montagsfoto.\n\nDie Kasse für die Instagram-Kundenmaschine ist offen!"),
        t("Sie ist für dich, wenn du im Network bist, regelmässig postest und merkst, dass daraus kaum Gespräche entstehen."),
        t("Was du am Ende hast\n\n1. Deine Content-Säulen\n2. Beiträge und Storys, die Vertrauen aufbauen\n3. Einen Weg von der Reaktion zum Gespräch\n4. Eine Routine, die auch ohne Motivation läuft"),
        t("31 Lektionen, in deinem Tempo. 333 Franken, bis Montag, 30. November."),
        frage("Fragen? Schreib mir, ich antworte dir persönlich."),
        cta("Alle Infos und die Anmeldung:", LINK_IKM),
    ]),
    ("2026-11-24", "Di", "Kasse offen", "persönlich · Einwand", "warum mit mir", "Nicht noch mehr Geld ausgeben", [
        bild("✏️ Ein Foto von dir."),
        t("Einen Satz höre ich oft: Ich will nicht noch mehr Geld für Kurse ausgeben."),
        t("✏️ Deine ehrliche Geschichte zu einem Kauf, bei dem du gezögert hast, und was danach passiert ist."),
        t("Die Frage, die ich mir dann stelle: Was kostet es mich, wenn alles bleibt, wie es ist? Bei Instagram heisst das meistens noch ein halbes Jahr posten, ohne dass jemand fragt."),
        cta("Wenn du genau an diesem Punkt bist:", LINK_IKM),
    ]),
    ("2026-11-25", "Mi", "Kasse offen", "Inspiration", "Inspiration", "Ein Schritt nach dem anderen", [
        bild("✏️ Ein Bild von heute."),
        t("Erinnerst du dich an die Frau, die nach Jahren im Network nochmal angefangen hat? Ihr erster Schritt bei mir war die Instagram-Kundenmaschine."),
        t("Danach kam mein Kurs Mama-CEO, heute ist sie in meiner Academy. Ein Schritt nach dem anderen, neben Teilzeitjob, Network und mehreren Kindern."),
        umfrage("Wo stehst du gerade?", "Ganz am Anfang", "Schon länger dabei"),
        cta("Der erste Schritt, noch bis Montag:", LINK_IKM),
    ]),
    ("2026-11-26", "Do", "Kasse offen", "Blick in den Kurs", "einen krassen Tipp", "Vom Kommentar zum Gespräch", [
        dict(bild("✏️ Screenshot einer Lektion, zum Beispiel „Keywords, die Entscheidungen auslösen“.\n\nEine Lektion, die ich besonders mag."), notiz="Screenshot aus ThriveCart Learn einsetzen."),
        t("Eine Lektion in der Kundenmaschine heisst Keywords, die Entscheidungen auslösen. Darin geht es darum, wie aus einem Kommentar ein Gespräch wird."),
        t("Ein Tipp vorab\n\nEin Aufruf funktioniert besser, wenn man nicht nachdenken muss: ein Wort zum Kommentieren, und man weiss genau, was danach kommt."),
        frage("Was ist deine grösste Frage zu Instagram gerade?"),
        cta("Alle 31 Lektionen, noch bis Montag:", LINK_IKM),
    ]),
    ("2026-11-27", "Fr", "Kasse offen", "eigene Meinung", "warum mit mir", "Black Friday ohne Rabatt", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Heute ist Black Friday, und bei mir gibt es keinen Rabatt. Der Preis bleibt 333, wie seit Montag."),
        t("Wer am Montag gekauft hat, soll heute nicht das Gefühl haben, zu viel bezahlt zu haben. Das ist mir wichtiger als ein schneller Verkauf."),
        umfrage("Kaufst du am Black Friday?", "Ja, gezielt", "Lieber nicht"),
        cta("Noch bis Montag um Mitternacht:", LINK_IKM),
    ]),
    ("2026-11-28", "Sa", "Kasse offen", "eine Folie", "Inspiration", "Noch zwei Tage", [
        bild("✏️ Samstagsbild.\n\nNoch zwei Tage, dann geht die Kasse der Kundenmaschine zu.", LINK_IKM),
    ]),
    ("2026-11-29", "So", "Kasse offen", "eine Folie", "Inspiration", "Morgen ist Schluss", [
        bild("✏️ Sonntagsbild.\n\nMorgen um Mitternacht geht die Kasse zu. Wenn du noch eine Frage hast, schreib mir heute.", LINK_IKM),
    ]),
    ("2026-11-30", "Mo", "Kasse offen", "letzter Tag", "warum mit mir", "Heute um Mitternacht", [
        bild("✏️ Foto von dir.\n\nHeute um Mitternacht geht die Kasse für die Kundenmaschine zu."),
        t("Sie passt zu dir, wenn du bereit bist, ein paar Wochen an deinem Profil zu arbeiten. Sie passt nicht, wenn du dir Ergebnisse wünschst, ohne selbst etwas zu tun."),
        bild("✏️ Dein ehrlicher Satz zum Schluss, frei in die Kamera gesprochen."),
        frage("Noch unsicher? Schreib mir bis 22 Uhr."),
        cta("Letzte Chance, bis 23:59:", LINK_IKM),
    ]),
]

DOTERRA = [
    # ---------------- KW44 · Bestellschluss Runde 10.11. ----------------
    ("2026-10-26", "Mo", "Routine Nov", "lehrreich", "Inspiration", "Kein Mittagstief mehr", [
        bild("✏️ Montagsfoto.\n\nWeisst du, was bei mir heute anders ist als früher? Ich hab kein Mittagstief mehr."),
        t("Dahinter steckt keine Wunderpille. Bei mir sind es Protein zu jeder Mahlzeit, Krafttraining, genug Schritte und mein Nährstoffpaket, jeden Tag."),
        t("Genau das machen wir in meiner 30-Tage-Energie-Routine zusammen. Die nächste Runde startet am 10. November."),
        cta("Bestellen bis Samstag, damit dein Paket rechtzeitig da ist.", LINK_ROUTINE),
    ]),
    ("2026-10-27", "Di", "Routine Nov", "persönlich", "warum mit mir", "Der Satz einer Freundin", [
        bild("✏️ Ein Foto von dir."),
        t("Den entscheidenden Satz hat mir eine Freundin gesagt, gleich alt wie ich: Mach doch mal einen Hormontest."),
        t("Da war ich 36. Mit dem Ergebnis hab ich angefangen, meinen Alltag umzubauen, Schritt für Schritt."),
        frage("Wer sagt dir ehrlich, wenn du müde aussiehst?"),
        cta("Ich bin gern diese Freundin für dich, 30 Tage lang. Start am 10. November.", LINK_ROUTINE),
    ]),
    ("2026-10-28", "Mi", "Routine Nov", "Tipp", "einen krassen Tipp", "30 Gramm zum Frühstück", [
        bild("✏️ Dein Frühstück von heute."),
        t("Mein einfachster Tipp für mehr Energie am Vormittag: mindestens 30 Gramm Protein zum Frühstück."),
        t("Warum\n\nEin Gipfeli lässt den Blutzucker schnell steigen und genauso schnell wieder fallen. Viele spüren das um halb zehn als Tief."),
        cta("120 Rezepte dazu bekommst du in der Energie-Routine sofort nach der Buchung.", LINK_ROUTINE),
    ]),
    ("2026-10-29", "Do", "Routine Nov", "Business", "warum mit mir", "Wie machst du das mit vier Kindern?", [
        bild("✏️ Foto von dir bei der Arbeit, mit Laptop oder Handy."),
        t("Die Frage höre ich oft: Wie machst du das, mit vier Kindern?"),
        t("Ein Teil der Antwort: Ich baue mir von zu Hause aus ein Business mit den Ölen auf, in meinem Tempo. Und ich suche gerade Frauen, die das mit mir zusammen machen wollen."),
        cta("Neugierig? Bei mir kannst du starten, ganz ohne Druck.", DM_BUSINESS),
    ]),
    ("2026-10-30", "Fr", "Routine Nov", "Fakten", "warum mit mir", "Morgen ist Bestellschluss", [
        bild("✏️ Foto von heute."),
        t("Morgen ist Bestellschluss für die Runde ab 10. November. Wer später bestellt, startet im Dezember."),
        t("Du bekommst dein Nährstoffpaket, 120 Rezepte, deinen Plan, mein Krafttraining, die Gruppe und ein Start-Gespräch mit mir."),
        cta("270 Franken, bis morgen.", LINK_ROUTINE),
    ]),
    ("2026-10-31", "Sa", "Routine Nov", "eine Folie", "Inspiration", "Letzter Tag für November", [
        bild("✏️ Samstagsbild.\n\nHeute ist der letzte Tag, um bei der November-Runde der Energie-Routine dabei zu sein.", LINK_ROUTINE),
    ]),
    ("2026-11-01", "So", "Kickstart", "eine Folie", "einen krassen Tipp", "Erst mal reinschnuppern", [
        bild("✏️ Sonntagsbild.\n\nDu willst erst mal reinschnuppern? Drei Tage Energie-Kickstart, gratis per Mail.", LINK_KICK),
    ]),
    # ---------------- KW45 · Kickstart ----------------
    ("2026-11-02", "Mo", "Kickstart", "lehrreich", "einen krassen Tipp", "Müde trotz Schlaf", [
        bild("✏️ Montagsfoto."),
        t("Müde trotz Schlaf? Das hab ich lange für normal gehalten, mit vier Kindern halt."),
        t("Heute weiss ich, dass Müdigkeit viele Ursachen haben kann, und dass man einiges davon selbst in der Hand hat."),
        cta("Drei Tage, drei kleine Schritte, gratis per Mail:", LINK_KICK),
    ]),
    ("2026-11-03", "Di", "Kickstart", "persönlich", "warum mit mir", "Dreimal die Woche", [
        bild("✏️ Foto von deinem Training oder deinen Turnschuhen."),
        t("Dreimal die Woche Krafttraining. ✏️ Ein ehrlicher Satz, wie du früher darüber gedacht hast."),
        t("Krafttraining ist bei mir einer von vier Bausteinen. Die anderen drei sind Protein, Schritte und mein Nährstoffpaket."),
        umfrage("Machst du Krafttraining?", "Ja", "Noch nicht"),
        cta("Mein Training ist in der Energie-Routine mit drin. Nächste Runde ab 10. Dezember.", LINK_ROUTINE),
    ]),
    ("2026-11-04", "Mi", "Kickstart", "Tipp", "einen krassen Tipp", "8000 Schritte", [
        bild("✏️ Foto von draussen."),
        t("Ein Tipp, der nichts kostet: Schritte zählen. Ich nehme mir 8000 am Tag vor."),
        t("So klappt's im Mama-Alltag\n\n✏️ Dein bester Trick für mehr Schritte, zum Beispiel zu Fuss zur Schule oder telefonieren im Gehen."),
        cta("Mehr kleine Schritte im Gratis-Kickstart:", LINK_KICK),
    ]),
    ("2026-11-05", "Do", "Kickstart", "Business", "warum mit mir", "Über einen Umweg zu den Ölen", [
        bild("✏️ Foto von deinen Ölen oder deinem Diffuser."),
        t("Ich hab zuerst Mamas gezeigt, wie sie ihre To-do-Liste halbieren. Darüber kamen wir ins Gespräch, und erst dann kamen die Öle zur Sprache."),
        t("Heute baue ich daraus von zu Hause aus ein kleines Business auf. Wenn dich das neugierig macht, erzähl ich dir gern mehr."),
        cta("Schreib mir, ganz unverbindlich.", DM_BUSINESS),
    ]),
    ("2026-11-06", "Fr", "Kickstart", "eigene Meinung", "Inspiration", "Ich warte nicht mehr ab", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Lange hab ich gedacht: Ich bin halt müde, das wird schon wieder. Heute warte ich nicht mehr ab."),
        t("Ich nenne das Selbstermächtigung. Niemand kommt und ändert es für dich, aber du kannst heute mit einem kleinen Schritt anfangen."),
        cta("Ein kleiner Schritt, gratis:", LINK_KICK),
    ]),
    ("2026-11-07", "Sa", "Kickstart", "eine Folie", "Inspiration", "Was gibt dir Energie?", [
        bild("✏️ Samstagsbild.\n\nWas gibt dir am Wochenende Energie? Schreib's mir.", "Frage-Sticker"),
    ]),
    ("2026-11-08", "So", "Kickstart", "eine Folie", "Inspiration", "Übermorgen startet die Runde", [
        bild("✏️ Sonntagsbild.\n\nÜbermorgen startet die November-Runde der Energie-Routine. Die nächste beginnt am 10. Dezember.", LINK_ROUTINE),
    ]),
    # ---------------- KW46 · Routine läuft ----------------
    ("2026-11-09", "Mo", "Routine läuft", "lehrreich", "warum mit mir", "Das Start-Gespräch", [
        bild("✏️ Montagsfoto."),
        t("Morgen startet die Energie-Routine. Wer bei mir startet, bekommt vorher ein Gespräch von 20 Minuten, in dem wir schauen, wo du stehst."),
        umfrage("Wie ist dein Energielevel heute?", "Voll da", "Auf Reserve"),
        cta("Nächste Runde: 10. Dezember.", LINK_ROUTINE),
    ]),
    ("2026-11-10", "Di", "Routine läuft", "persönlich", "Inspiration", "Heute geht's los", [
        bild("✏️ Foto von deinem Frühstück oder deinem Nährstoffpaket.\n\nHeute startet die Energie-Routine."),
        t("✏️ Was hat sich bei dir als Erstes verändert, als du mit deiner Routine angefangen hast?"),
        cta("Du willst im Dezember mitmachen?", LINK_ROUTINE),
    ]),
    ("2026-11-11", "Mi", "Routine läuft", "Tipp", "einen krassen Tipp", "Auch mittags 30 Gramm", [
        bild("✏️ Dein Mittagessen von heute."),
        t("Auch mittags halte ich mich an meine Faustregel: mindestens 30 Gramm Protein pro Mahlzeit."),
        t("Zum Screenshotten\n\n✏️ Deine liebste Kombination mit 30 Gramm Protein, mit Mengen."),
        cta("Gratis reinschnuppern:", LINK_KICK),
    ]),
    ("2026-11-12", "Do", "Routine läuft", "Business", "warum mit mir", "Network ohne Druck", [
        bild("✏️ Foto von dir."),
        t("Viele denken bei Network an Partys und Druck. Bei mir sieht es anders aus: Ich rede über meinen Alltag, und wer mehr wissen will, fragt."),
        t("Ich suche gerade ein paar Frauen, die das auch für sich ausprobieren möchten."),
        cta("Schreib mir „Business“.", DM_BUSINESS),
    ]),
    ("2026-11-13", "Fr", "Routine läuft", "eigene Meinung", "einen krassen Tipp", "Essen statt Shakes", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Meine Meinung, die nicht allen gefällt: Ich brauche keine Shakes, um auf mein Protein zu kommen. Ich esse es."),
        t("Der Ernährungsmediziner Matthias Riedl warnt in seinem Buch Gamechanger Protein sogar vor hochverarbeiteten Proteinprodukten."),
        umfrage("Shake oder richtiges Essen?", "Shake", "Essen"),
        cta("120 Rezepte ohne Shakes, in der Energie-Routine.", LINK_ROUTINE),
    ]),
    ("2026-11-14", "Sa", "Routine läuft", "eine Folie", "Inspiration", "Routine am Wochenende", [
        bild("✏️ Samstagsbild.\n\nWie hältst du deine Routine am Wochenende? Ich bin gespannt.", "Frage-Sticker"),
    ]),
    ("2026-11-15", "So", "Routine läuft", "eine Folie", "Inspiration", "Nächste Woche: Geschenke", [
        bild("✏️ Sonntagsbild.\n\nNächste Woche zeige ich dir, welche Öle ich dieses Jahr verschenke.", "Frage-Sticker"),
    ]),
    # ---------------- KW47 · Öle als Geschenk ----------------
    ("2026-11-16", "Mo", "Geschenke", "lehrreich", "Inspiration", "Ein Geschenk, das benutzt wird", [
        bild("✏️ Foto von deinen Ölen."),
        t("✏️ Ein Satz, was du dieses Jahr verschenken willst."),
        t("Ein Öl-Geschenk wird benutzt und verstaubt nicht im Schrank. ✏️ Welches Öl du am liebsten verschenkst und warum."),
        cta("Willst du Ideen für deine Liste? Schreib mir.", DM_IDEEN),
    ]),
    ("2026-11-17", "Di", "Geschenke", "persönlich", "warum mit mir", "Mein Öl-Moment", [
        bild("✏️ Foto von einem gemütlichen Moment zu Hause, zum Beispiel mit Diffuser."),
        t("✏️ Wann benutzt du deine Öle am liebsten? Ein Moment aus deinem Alltag."),
        umfrage("Benutzt du Öle zu Hause?", "Jeden Tag", "Noch nie"),
        cta("Neugierig auf Öle? Schreib mir, ich berate dich gern.", DM_IDEEN),
    ]),
    ("2026-11-18", "Mi", "Geschenke", "Tipp", "einen krassen Tipp", "Selbst gebastelt", [
        bild("✏️ Foto einer selbst gebastelten Verpackung für ein Öl."),
        t("Mein Lieblingsteil beim Schenken ist die Verpackung. Ich bastle sie selbst."),
        umfrage("Bastelst du deine Geschenke auch?", "Ja!", "Keine Zeit"),
        cta("Willst du eine Öl-Geschenkidee von mir? Schreib mir.", DM_IDEEN),
    ]),
    ("2026-11-19", "Do", "Geschenke", "Business", "warum mit mir", "Schon mal überlegt?", [
        bild("✏️ Foto von dir."),
        t("Ich bin gerade in einem Programm, in dem ich lerne, mit den Ölen ein eigenes Team aufzubauen."),
        t("Darum frag ich dich ganz direkt: Hast du dir schon einmal überlegt, mit Ölen etwas dazuzuverdienen?"),
        umfrage("Schon mal überlegt?", "Ja, öfter", "Noch nie"),
        cta("Wenn ja: Schreib mir, ich erzähl dir, wie ich angefangen habe.", DM_BUSINESS),
    ]),
    ("2026-11-20", "Fr", "Geschenke", "eigene Meinung", "Inspiration", "Schenk dir selbst auch was", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Wir Mamas denken im Dezember an alle Geschenke, nur an uns selbst denken wir zuletzt."),
        t("Mein Vorschlag: Schenk dir dieses Jahr einen Dezember, in dem du nicht auf Reserve läufst. Die nächste Runde der Energie-Routine startet am 10. Dezember."),
        cta("Bestellen bis 30. November.", LINK_ROUTINE),
    ]),
    ("2026-11-21", "Sa", "Geschenke", "eine Folie", "Inspiration", "Steht ein Öl drauf?", [
        bild("✏️ Samstagsbild.\n\nDie Geschenkliste wird länger. Steht bei dir ein Öl drauf?", "Frage-Sticker"),
    ]),
    ("2026-11-22", "So", "Geschenke", "eine Folie", "Inspiration", "Noch eine Woche", [
        bild("✏️ Sonntagsbild.\n\nNoch eine Woche bis zum Bestellschluss für die Dezember-Runde der Energie-Routine.", LINK_ROUTINE),
    ]),
    # ---------------- KW48/49 · Runde 10.12., Bestellschluss 30.11. ----------------
    ("2026-11-23", "Mo", "Routine Dez", "lehrreich", "Inspiration", "Bevor der Dezember kommt", [
        bild("✏️ Montagsfoto."),
        t("✏️ Wie sieht dein Dezember aus? Ein Satz, ehrlich."),
        t("Darum startet die nächste Runde der Energie-Routine am 10. Dezember. Damit du nicht erst im Januar merkst, wie leer du bist."),
        cta("Bestellschluss: Montag, 30. November.", LINK_ROUTINE),
    ]),
    ("2026-11-24", "Di", "Routine Dez", "persönlich", "warum mit mir", "Heute schlafe ich durch", [
        bild("✏️ Foto von dir am Morgen."),
        t("Früher bin ich müde aufgewacht, egal wie lange ich geschlafen habe. Heute schlafe ich acht Stunden durch."),
        t("Bei mir war es keine einzelne Sache. Es war die Kombination aus Protein, Krafttraining, Schritten und meinem Nährstoffpaket."),
        cta("Diese Kombination zeig ich dir in 30 Tagen.", LINK_ROUTINE),
    ]),
    ("2026-11-25", "Mi", "Routine Dez", "Tipp", "einen krassen Tipp", "Protein schon am Morgen planen", [
        bild("✏️ Foto von deinem Abendessen."),
        t("Ein Tipp für den Abend: Plan dein Protein schon am Morgen. Wer um sechs erst überlegt, landet schnell bei Brot und Käse. Ich kenn das."),
        cta("Drei Tage Rezepte und Schritte, gratis:", LINK_KICK),
    ]),
    ("2026-11-26", "Do", "Routine Dez", "Business", "warum mit mir", "Im Januar starten", [
        bild("✏️ Foto von dir."),
        t("Wer im Januar mit einem eigenen kleinen Business starten will, fängt am besten jetzt an, darüber nachzudenken."),
        t("Ich nehme mir im Dezember Zeit für Gespräche mit Frauen, die das mit mir angehen möchten."),
        cta("Schreib mir „Business“.", DM_BUSINESS),
    ]),
    ("2026-11-27", "Fr", "Routine Dez", "eigene Meinung", "einen krassen Tipp", "Black Friday", [
        bild("✏️ Du, direkt in die Kamera."),
        t("Heute ist Black Friday. Mein Tipp: Kauf nichts, was du im Januar wieder bereust."),
        t("Wenn du etwas für dich tun willst, das bleibt: Die Energie-Routine startet am 10. Dezember, Bestellschluss ist am Montag."),
        cta("270 Franken, ganz ohne Black-Friday-Rabatt.", LINK_ROUTINE),
    ]),
    ("2026-11-28", "Sa", "Routine Dez", "eine Folie", "Inspiration", "Noch zwei Tage", [
        bild("✏️ Samstagsbild.\n\nNoch zwei Tage für die Dezember-Runde der Energie-Routine.", LINK_ROUTINE),
    ]),
    ("2026-11-29", "So", "Routine Dez", "eine Folie", "Inspiration", "Morgen ist Bestellschluss", [
        bild("✏️ Sonntagsbild.\n\nMorgen ist Bestellschluss. Fragen beantworte ich dir heute gern.", LINK_ROUTINE),
    ]),
    ("2026-11-30", "Mo", "Routine Dez", "letzter Tag", "warum mit mir", "Letzter Tag für Dezember", [
        bild("✏️ Foto von dir."),
        t("Heute ist der letzte Tag, um für die Runde ab 10. Dezember zu bestellen."),
        t("Dein Nährstoffpaket, 120 Rezepte, dein Plan, mein Krafttraining, die Gruppe und ein Start-Gespräch mit mir."),
        cta("Bis heute Nacht:", LINK_ROUTINE),
    ]),
]

# Eigene Zusatzprüfungen über die Blackliste hinaus
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
    docs = bauen("mentoring", MENTORING) + bauen("doterra", DOTERRA)
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
