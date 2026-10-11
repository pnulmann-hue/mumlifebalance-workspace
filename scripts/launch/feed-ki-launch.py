"""
Feed-Beiträge für den KI-Launch (Mentoring, 30.9.–23.10.2026).

Quelle der Themen: outputs/produkte/ki-treppe/07-launch-kalender.md (Feed-Tabellen).
Patricias Entscheide 28.09.2026: eine Variante je Platz, höchstens EIN Sprechreel
(Fr 9.10.), alles andere B-Roll. Flop-Befund dazu: outputs/content/KW40/launch-feed-befund.md

Ablauf:
  python scripts/launch/feed-ki-launch.py          # schreibt JSON je Beitrag + Markdown
  danach: ArtifactData batch set → Cockpit, Sammlungen "reels" und "karussells"

Nur belegte Fakten: 18 Stunden/Woche, 13 Helfer, Kochbot 1–2 Std → 5 Min,
Cockpit-Bot 06:30, Content-Woche Freitag 08:00, Begleitung zur Energie-Routine,
Stimm-Check (sechs Angaben, rund 15 Minuten). Was nicht belegt ist, steht in `hinweis`.
"""
import json, sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
R = Path(__file__).resolve().parents[2]
AUS = R / "outputs/cockpit/abgleich/launch-feed"
MD = R / "outputs/content/KW40/launch-feed-ki.md"
JETZT = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

VORSTELLUNG = ("Hi, ich bin Patricia, Mama von vier Kindern. 2023 habe ich mein Network im "
               "Hybridmodell aufgebaut. Bei mir lernst du, wie du mit deinem Thema auf Instagram "
               "sichtbar wirst, wie du digitale Produkte passend zum Network entwickelst und wie du "
               "das ganze Business in deinen Mama-Alltag packst.")
TAGS = "#mamabusiness #mamaimnetworkmarketing #onlinebusinessmama #kifuermamas #mumpreneur"


def cap(*absaetze, lead=False):
    teile = list(absaetze)
    if lead:
        teile.append("STIMME ⬇️")
    teile += [VORSTELLUNG, TAGS]
    return "\n\n".join(teile)


REELS = [
    dict(
        id="kw40-reel-m-mi-ki", datum="2026-09-30", job="Lead", angle="Identität",
        name="KI · Mi · Keine Zeit, das auch noch zu lernen",
        text="Zwischen Teamcall, Bestellungen und Hausaufgaben jetzt auch noch KI lernen?",
        betont="Meine erste Stunde pro Woche kam beim Menüplan zurück.",
        coverhook="Keine Zeit, jetzt auch noch KI zu lernen?",
        caption=cap(
            "„Zwischen Teamcall, Bestellungen und Hausaufgaben soll ich jetzt auch noch KI lernen?“",
            "Den Satz hör ich oft, und ich versteh ihn gut. Deshalb fang ich bei etwas an, das mit Business gar nichts zu tun hat: mit dem Menüplan.",
            "Früher hab ich dafür jede Woche ein bis zwei Stunden gebraucht. Überlegen, was es gibt, Rezepte zusammensuchen, dann die Einkaufsliste schreiben. Heute beantworte ich drei Fragen: Ist nächste Woche etwas Besonderes? Wo bleibt wenig Zeit, oder kommt Besuch? Muss im Kühlschrank etwas weg? Danach liegen die Menüliste und die Einkaufsliste aus meinen eigenen Rezepten auf dem Handy. Fünf Minuten, zehn, wenn mir etwas nicht passt.",
            "Gelernt hab ich dafür nichts Technisches. Ich hab einmal aufgeschrieben, wie ich es sonst selbst mache: welche Fragen ich mir stelle, woher die Rezepte kommen und wie die Liste aussehen soll.",
            "Genau da kannst du heute anfangen. Nimm eine Arbeit, die jede Woche gleich abläuft, und schreib die Fragen auf, die du dir dabei jedes Mal stellst. Mehr braucht der erste Schritt nicht.",
            "Beim Schreiben ist es übrigens genauso. Solange deiner KI niemand gesagt hat, wie du klingst, schreibt sie nach irgendwem.",
            "Kommentier STIMME, dann schick ich dir den Stimm-Check, und in rund 15 Minuten hast du einen Brief, mit dem deine KI Texte in deinem Ton schreibt.",
            lead=True),
        hinweis="Launch KI · KW40 · B-Roll baut Claude, sobald du den Hook freigibst.",
    ),
    dict(
        id="kw40-reel-m-fr-ki", datum="2026-10-02", job="Reichweite", angle="Identität",
        name="KI · Fr · Ich kann nicht programmieren",
        text="Ich kann nicht programmieren.",
        betont="Und hab mir trotzdem dreizehn KI-Helfer gebaut.",
        coverhook="Nicht programmieren können und trotzdem dreizehn KI-Helfer",
        caption=cap(
            "Wie viele Arbeiten machst du jede Woche genau gleich?",
            "Ich frag das, weil die meisten bei KI an Leute denken, die programmieren können. Ich kann es nicht. Trotzdem arbeiten heute dreizehn Helfer für mich, vom Menüplan bis zur Übersicht über meine Beiträge.",
            "Ich quatsche einfach mit der KI, und sie setzt es um. Wenn ich etwas überhaupt nicht kapiere, sag ich ihr, sie soll es mir erklären, und dann erklärt sie es so lange, bis ich es verstehe.",
            "Was ich dafür gebraucht hab, kannst du auch: erklären, wie du etwas machst. Das tust du jeden Tag, bei deinen Kindern, bei einer neuen Teampartnerin, bei einer Kundin, die zum ersten Mal bestellt.",
            "Probier es heute einmal aus. Nimm eine Sprachnachricht auf, in der du jemandem erklärst, wie du eine Bestellung nachfasst: was du zuerst schreibst, wann du nachfragst, was du nie sagen würdest. Tipp das ab, und du hast den ersten Auftrag für deine KI. So redest du mit ihr, in ganz normalen Sätzen.",
            "Schick das der Freundin, die bei KI immer sagt, sie sei dafür nicht technisch genug.",
        ),
        hinweis="Launch KI · KW40 · „Ich kann nicht programmieren“ und das Quatschen mit der KI von dir bestätigt (28.09.).",
    ),
    dict(
        id="kw41-reel-m-mo-ki", datum="2026-10-05", job="Lead", angle="Ergebnis",
        name="KI · Mo · Gemütlich frühstücken, der Plan steht schon",
        text="Sitzt du um acht schon am Handy und planst den Tag?",
        betont="Ich frühstücke um die Zeit gemütlich. Mein Plan liegt seit halb sieben bereit.",
        coverhook="Um acht frühstücke ich gemütlich. Der Plan steht schon.",
        caption=cap(
            "Wann planst du eigentlich deinen Tag?",
            "An Schultagen frühstücke ich um acht, wenn die Kinder aus dem Haus sind, und zwar ganz gemütlich. Am Montag, Mittwoch und Freitag kommt danach das Krafttraining, dreissig bis vierzig Minuten, und noch zwanzig Minuten Crosstraining. Dann geht es vielleicht noch schnell ins Büro, ich koche das Mittagessen, und am Nachmittag setze ich mich nochmals ran.",
            "Um halb sieben schickt mir mein Cockpit-Bot eine Nachricht aufs Handy: welches Profil heute dran ist, was der grosse Brocken des Tages ist, welche drei Sachen diese Woche Geld bringen und welche Aufgaben noch offen sind. Wenn ich mich an den Frühstückstisch setze, ist das Nachdenken über den Tag schon erledigt, und genau deshalb kann ich dort in Ruhe sitzen.",
            "Die Fragen, die der Bot für mich beantwortet, kannst du dir heute Abend selbst auf einen Zettel schreiben. Welches Profil ist morgen dran? Was ist der eine grosse Brocken? Welche drei Sachen bringen diese Woche Geld? Wer das am Vorabend beantwortet, fängt am Morgen nicht bei null an.",
            "Kommentier STIMME, dann bekommst du den Stimm-Check von mir: sechs Fragen, und nach 15 Minuten weiss deine KI, wie du schreibst.",
            lead=True),
        hinweis="Launch KI · KW41 · Morgenablauf von dir am 28.09. bestätigt. Liegt in den Herbstferien, deshalb „an Schultagen“.",
    ),
    dict(
        id="kw41-reel-m-mi-ki", datum="2026-10-07", job="Lead", angle="Vergleich",
        name="KI · Mi · Jeden Montag erklären, wer du bist",
        text="Jeden Montag erklärst du ChatGPT wieder, wer du bist und was du verkaufst?",
        betont="Meine KI weiss das seit Monaten.",
        coverhook="Jeden Montag erklärst du der KI wieder, wer du bist?",
        caption=cap(
            "„Ich tipp jedes Mal wieder ein, wer ich bin und was ich verkaufe.“",
            "So fängt fast jede an, und es ist auch kein Fehler. Ein Chat vergisst eben alles, sobald du ein neues Fenster öffnest. Bei mir liegt deshalb alles, was die KI über mich wissen muss, fest abgelegt: wer ich bin, für wen ich schreibe, welche Angebote gerade laufen und welche Wörter bei mir nie vorkommen. Das liest sie jedes Mal zuerst, bevor sie irgendetwas macht.",
            "Im Kleinen geht das bei dir schon heute. Schreib ein Dokument „Über mich“ mit fünf Punkten: was du machst, für wen, was du anbietest, wie du klingst, was du nie sagen würdest. Kopier es an den Anfang jedes neuen Chats, oder leg es dort ab, wo dein Programm eigene Anweisungen oder Projekte speichert. Ab da fängst du nicht mehr bei null an.",
            "Kommentier STIMME, dann liegt der Stimm-Check in deinen Nachrichten, und nach rund 15 Minuten hast du das Dokument, das du deiner KI jedes Mal mitgibst.",
            lead=True),
        hinweis="Launch KI · KW41",
    ),
    dict(
        id="kw41-reel-m-fr-ki", datum="2026-10-09", job="Reichweite", angle="Bekenntnis",
        videoart="sprech",
        name="KI · Fr · Am Anfang war's mehr Arbeit (Sprechreel)",
        text="Am Anfang hat mich die KI mehr Zeit gekostet, als sie mir gespart hat.",
        betont="",
        coverhook="Am Anfang hat mich die KI mehr Zeit gekostet",
        caption="",
        skript=(
            "SPRECHREEL — das einzige im Launch. Dreh es bis Fr 2.10., dann bau ich es fertig.\n"
            "Dauer: 30–45 Sekunden. Setting: Küchentisch oder Laptop, Tageslicht, Handy auf Augenhöhe.\n\n"
            "🚨 Nur drehen, wenn der erste Satz bei dir stimmt. Wenn nicht, sag's mir, dann bau ich ein B-Roll.\n\n"
            "1 · HOOK wortwörtlich: „Am Anfang hat mich die KI mehr Zeit gekostet, als sie mir gespart hat.“\n"
            "2 · Ein Beispiel in deinen Worten: Was hast du damals gemacht, das so viel Zeit gefressen hat? "
            "(z.B. jeden Text umgeschrieben, jedes Mal neu erklärt, wer du bist — nur was wirklich war)\n"
            "3 · Der Moment, wo es gekippt ist: Was hast du anders gemacht?\n"
            "4 · Der Satz für die Frau, die es gerade probiert: Was würdest du ihr sagen?\n"
            "5 · Schluss: „Schick das der Freundin, die gerade aufgeben will.“\n\n"
            "Versprecher und Wiederholungen sind egal, ich schneide das. Einfach einmal durchreden."),
        hinweis="Launch KI · KW41 · Die Caption schreibe ich nach dem Dreh aus deinen Worten, damit nichts drinsteht, was nicht war.",
    ),
    dict(
        id="kw42-reel-m-mo-ki", datum="2026-10-12", job="Lead", angle="Neugier",
        name="KI · Mo · Nach der Bestellung",
        text="Was passiert bei dir nach der Bestellung?",
        betont="Meine Kundschaft bekommt dreissig Tage Begleitung aufs Handy.",
        coverhook="Was passiert bei dir nach der Bestellung?",
        caption=cap(
            "Was bekommt deine Kundschaft von dir, nachdem die Bestellung raus ist?",
            "Bei mir ist das seit diesem Herbst eine eigene kleine Seite fürs Handy. Wer bei mir die 30-Tage-Energie-Routine macht, findet dort über hundert Rezepte, jeden Tag einen kurzen Impuls, eine Checkliste, die über die Wochen mitwächst, und einen Vorrat, den man Schritt für Schritt aufbaut. Jeden Tag geht ein neuer Artikel auf.",
            "Programmiert hab ich davon nichts. Ich hab der KI gesagt, was meine Kundschaft in den dreissig Tagen braucht, in welcher Reihenfolge, und wie es sich anfühlen soll. Den Rest hat sie gebaut, und ich hab so lange nachgebessert, bis es gepasst hat.",
            "Wenn du so etwas auch willst, fang nicht bei der Technik an. Schreib die drei Fragen auf, die dir nach einer Bestellung immer wieder gestellt werden. Genau das ist der Inhalt deiner ersten Begleitseite, und die Antworten hast du längst im Kopf.",
            "Kommentier STIMME, dann bekommst du den Stimm-Check, und in 15 Minuten steht fest, wie alles klingen soll, was die KI für deine Kundschaft schreibt.",
            lead=True),
        hinweis="Launch KI · KW42 · Die Begleitung zur Energie-Routine ist die Station aus der Masterclass. 🟡 Bitte bestätigen: „seit diesem Herbst“.",
    ),
    dict(
        id="kw42-reel-m-mi-ki", datum="2026-10-14", job="Lead", angle="Schmerz",
        name="KI · Mi · Lohnt sich das Abo",
        text="Noch ein Abo, bei dem du nicht weisst, ob es sich lohnt?",
        betont="Ich hab nachgerechnet, was meins mir jede Woche abnimmt.",
        coverhook="Noch ein Abo? Ich hab nachgerechnet, ob es sich lohnt.",
        caption=cap(
            "„Noch ein Abo, bei dem ich nicht weiss, ob es sich lohnt.“",
            "Das hab ich mir auch überlegt, und ich sag dir ehrlich: Ein KI-Abo lohnt sich keinen Rappen, solange du die KI wie eine Suchmaschine benutzt. Dann zahlst du für etwas, das Google gratis kann.",
            "Es lohnt sich erst, wenn die KI dir Arbeit abnimmt, die jede Woche wiederkommt. Bei mir ist das zum Beispiel der Tagesplan, der um halb sieben schon auf dem Handy liegt, und die Beiträge der ganzen Woche, die am Freitag vorbereitet sind und die ich nur noch lese und freigebe. Genau diese Arbeiten würden sonst jede Woche wieder bei mir landen.",
            "So rechnest du es für dich nach: Schreib drei Arbeiten auf, die jede Woche wiederkommen, und daneben, wie lange sie dauern. Wenn eine davon eine Stunde frisst, ist das die, mit der du anfängst. Wenn keine eine Stunde frisst, brauchst du das Abo noch nicht.",
            "Kommentier STIMME, dann schick ich dir den Stimm-Check gratis, und in rund 15 Minuten siehst du, was eine KI mit deinen eigenen Angaben schreibt.",
            lead=True),
        hinweis="Launch KI · KW42 · Ohne Preis (Patricia, 28.09.: Abo-Kosten nicht öffentlich).",
    ),
    dict(
        id="kw42-reel-m-fr-ki", datum="2026-10-16", job="Reichweite", angle="Identität",
        name="KI · Fr · 18 Stunden für alles",
        text="„Die anderen haben halt mehr Zeit als ich.“",
        betont="Ich hab 18 Stunden die Woche. Für alles.",
        coverhook="Ich hab 18 Stunden die Woche. Für alles.",
        caption=cap(
            "„Die anderen haben halt mehr Zeit als ich.“",
            "Ich hab mal zusammengezählt, wie viel Zeit ich wirklich hab. Mit vier Kindern bleiben mir rund 18 Stunden die Woche fürs ganze Geschäft.",
            "Darin steckt alles: jeden Tag Storys und ein Beitrag auf zwei Kanälen, jeden Monat ein Gratis- und ein bezahltes Produkt, das Network mit Kundschaft und Team, und die ganze Administration dazu. Ohne meine KI-Helfer wäre das nie möglich, das sag ich dir ganz ehrlich.",
            "Wenn du wissen willst, wo deine Zeit steckt, mach es eine Woche lang wie ich: Schreib in Stichworten auf, was du fürs Geschäft tust. Am Freitag streichst du alles an, was jede Woche gleich abläuft. Das ist die Liste, die dir Zeit zurückgeben kann, mit KI oder ohne.",
            "Schick das der Freundin, die immer sagt, die anderen hätten halt mehr Zeit.",
        ),
        hinweis="Launch KI · KW42 · 18 Std./Woche und der Inhalt sind von dir bestätigt (25.09.).",
    ),
    dict(
        id="kw43-reel-m-mo-ki", datum="2026-10-19", job="Lead", angle="Identität",
        name="KI · Mo · Für wen das nichts ist",
        text="Ist das mit der KI überhaupt was für eine Networkerin wie mich?",
        betont="Für manche ehrlich nicht.",
        coverhook="Ist das mit der KI überhaupt was für mich?",
        caption=cap(
            "Ist das mit der KI überhaupt was für eine Networkerin wie dich?",
            "Ich sag es dir ehrlich, für manche nicht. Wenn bei dir kaum eine Arbeit jede Woche gleich abläuft, nimmt dir eine KI wenig ab. Wenn du nicht bereit bist, einmal eine Stunde lang aufzuschreiben, wie du arbeitest und wie du klingst, bekommst du Texte von irgendwem. Und wenn du willst, dass sie dir Geschichten erfindet, die du nie erlebt hast, bist du bei mir falsch, weil genau das deine Kundschaft irgendwann merkt.",
            "Für alle anderen gibt es einen einfachen Test. Beantworte drei Fragen mit Ja oder Nein: Gibt es eine Arbeit, die du jede Woche wieder machst? Kannst du einer Freundin erklären, wie du sie machst? Hast du schon einen Text geschrieben, bei dem du dachtest: Ja, so klinge ich? Zweimal Ja reicht für den Anfang.",
            "Kommentier STIMME, dann schick ich dir den Stimm-Check, und nach 15 Minuten weisst du selbst, ob dir das liegt.",
            lead=True),
        hinweis="Launch KI · KW43",
    ),
    dict(
        id="kw43-reel-m-mi-ki", datum="2026-10-21", job="Reichweite", angle="Schmerz",
        name="KI · Mi · Zwischen Znüni und Schulweg",
        text="Zwischen Znüni-Boxen und Schulweg keine Stunde für KI?",
        betont="Der erste Schritt dauert zehn Minuten.",
        coverhook="Der erste Schritt mit KI dauert zehn Minuten",
        caption=cap(
            "Wie viele Minuten hast du heute wirklich für dich gehabt?",
            "Wenn die Antwort „kaum welche“ ist, geht es dir wie den meisten Mamas, mit denen ich rede. Deshalb hier drei Schritte, jeder so klein, dass er zwischen Znüni-Boxen und Schulweg passt.",
            "Erstens: Schreib fünf Sätze über dich. Was du machst, für wen, was du anbietest, wie du klingst und was du nie sagen würdest. Zehn Minuten.",
            "Zweitens: Such dir einen Text, den du selbst geschrieben hast und magst, eine Caption, eine Nachricht an eine Kundin, egal. Den gibst du der KI künftig als Beispiel mit. Zwei Minuten.",
            "Drittens: Beschreib eine Arbeit, die jede Woche gleich abläuft, so, als würdest du sie einer Freundin erklären. Zehn Minuten.",
            "Mehr ist es für den Anfang nicht. Wer diese drei Zettel hat, fängt bei der KI nie mehr bei null an.",
            "Schick das der Freundin, die dir gestern noch geschrieben hat, sie habe für so was keine Zeit.",
        ),
        hinweis="Launch KI · KW43",
    ),
    dict(
        id="kw43-reel-m-fr-ki", datum="2026-10-23", job="Lead", angle="Schmerz",
        name="KI · Fr · Irgendwann, wenn es ruhiger ist",
        text="„Mach ich irgendwann, wenn es ruhiger ist.“",
        betont="Mit vier Kindern wird es nicht ruhiger.",
        coverhook="Irgendwann, wenn es ruhiger ist?",
        caption=cap(
            "„Mach ich irgendwann, wenn es ruhiger ist.“",
            "Das ist der Satz, den ich am häufigsten höre, und ich versteh ihn gut. Nur wird es mit vier Kindern nicht ruhiger, es wird nur anders voll.",
            "Rechne einmal mit mir. Mein Menüplan hat früher ein bis zwei Stunden pro Woche gebraucht. Aufs Jahr gerechnet sind das fünfzig bis hundert Stunden, nur für die Frage, was es zu essen gibt. Jede Woche, in der ich „irgendwann“ gesagt hätte, hätte mich diese Zeit gekostet.",
            "Mach die Rechnung heute für eine eigene Arbeit: Wie lange dauert sie pro Woche, mal zweiundfünfzig? Die Zahl, die dabei rauskommt, ist der Preis von „irgendwann“.",
            "Kommentier STIMME, dann bekommst du den Stimm-Check, der 15 Minuten dauert und den du heute Abend machen kannst statt irgendwann.",
            lead=True),
        hinweis="Launch KI · KW43 · Letzter Tag der Kasse. Im Feed bleibt es ohne Preis und Kursname, die Frist steht in Storys und Mails.",
    ),
]

KARUSSELLS = [
    dict(
        id="kw40-kar-m-di-ki", datum="2026-09-29", job="Lead", angle="Neugier",
        typ="listicle", funnel="MOF",
        name="KI · Di · Fünf Sätze, an denen man die KI erkennt",
        slides=[
            ("hook", "Fünf Sätze, an denen jede merkt: Das hat die KI geschrieben.", "Und wie du sie in einer Minute rausnimmst."),
            ("text", "1 · „Stell dir vor …“", "Fast jeder KI-Text über Mamas fängt so an.\n\nFang stattdessen mit ihrem Satz an, so wie sie ihn denkt: „Ich hab schon wieder nichts gepostet.“"),
            ("text", "2 · „Nicht X, sondern Y“", "„Es geht nicht um mehr Posts, sondern um die richtigen.“\n\nKlingt klug und sagt so niemand. Mach zwei Sätze draus: „Mehr Posts bringen dir nichts. Die richtigen schon.“"),
            ("text", "3 · Drei kurze Sätze hintereinander", "„Du lernst. Du wächst. Du strahlst.“\n\nSo redet keine Freundin. Verbinde sie mit „und“ oder „weil“, dann klingt es nach dir."),
            ("text", "4 · „Kennst du das?“", "Die Frage beantwortet sich selbst, deshalb liest niemand weiter.\n\nBeschreib lieber gleich die Situation: „Neun Uhr abends, und die Story ist immer noch leer.“"),
            ("text", "5 · Wörter, die nach Prospekt klingen", "„ganz konkret“ · „echte Ergebnisse“ · „auf Augenhöhe“ · „Game-Changer“\n\nStreich sie. Wenn danach etwas fehlt, fehlt ein Beispiel."),
            ("text", "Der schnellste Test", "Lies den Text laut vor.\n\nÜberall, wo du stockst oder denkst „das würd ich so nie sagen“, hat die KI geschrieben und nicht du."),
            ("text", "Warum sie so schreibt", "Die KI kennt dich nicht. Solange ihr niemand gesagt hat, wie du klingst, schreibt sie den Durchschnitt von allen.\n\nDas lässt sich ändern."),
            ("cta", "Damit deine KI nach dir klingt", "Kommentier STIMME, dann schick ich dir den Stimm-Check.\n\nSechs Fragen, rund 15 Minuten, und die KI weiss, wie du schreibst."),
        ],
        caption=cap(
            "„Das klingt irgendwie gar nicht nach mir.“",
            "Wenn du das bei deinen KI-Texten denkst, liegst du richtig, und meistens sind es immer dieselben fünf Sätze, die den Text verraten. Deine Leserinnen merken es auch, oft ohne zu wissen, woran.",
            "Im Karussell stehen alle fünf, jeweils mit dem Satz, den du stattdessen nehmen kannst. Der schnellste Test steht auf Folie sieben: laut vorlesen. Überall, wo du stockst, klingt der Text nicht nach dir.",
            "Streichen hilft beim einzelnen Text. Damit du es nicht jedes Mal machen musst, braucht deine KI eine Beschreibung davon, wie du klingst.",
            "Kommentier STIMME, dann bekommst du den Stimm-Check, mit dem deine KI in rund 15 Minuten lernt, wie du klingst.",
            lead=True),
        hinweis="Launch KI · KW40 · Seit 28.09. Lead mit STIMME (Patricia). Ersetzt „Keine Expertin“ bei Blotato.",
    ),
    dict(
        id="kw40-kar-m-do-ki", datum="2026-10-01", job="Lead", angle="Konträr",
        typ="kontrovers", funnel="MOF", brand="mlb_dark",
        name="KI · Do · Dreissig Prompt-Listen und keine benutzt",
        slides=[
            ("hook", "Dreissig Prompt-Listen gespeichert und keine einzige benutzt?", ""),
            ("text", "Sie sind für niemanden geschrieben", "Eine Liste weiss nicht, wer du bist, was du anbietest und wie du redest.\n\nAlso kommt ein Text raus, der zu allen passt und damit zu keiner."),
            ("text", "Du musst jeden erst umbauen", "Name einsetzen, Angebot einsetzen, Ton anpassen.\n\nBis du fertig bist, hättest du den Text auch selbst geschrieben."),
            ("text", "Du findest den richtigen nicht", "Achtzig Prompts in drei Ordnern, und keiner heisst so, wie deine Aufgabe heute.\n\nAlso fängst du doch wieder von vorne an."),
            ("text", "Was stattdessen hilft", "Ein Blatt über dich, das die KI jedes Mal zuerst liest: wer du bist, für wen du schreibst, wie du klingst, was bei dir nie vorkommt.\n\nDas schreibst du einmal."),
            ("text", "Und ein fester Auftrag je Arbeit", "Für das, was jede Woche wiederkommt, schreibst du einmal auf, wie du es machst.\n\nAb dann sagst du nur noch „mach die Einkaufsliste“ und nicht mehr fünf Absätze."),
            ("text", "Wofür Listen trotzdem gut sind", "Zum Ausprobieren, um zu sehen, was überhaupt geht, sind sie super.\n\nNur für die tägliche Arbeit taugen sie nicht, weil sie dich nicht kennen."),
            ("cta", "Ich zeig dir live, wie das bei mir aussieht", "Kostenlose Masterclass am Donnerstag, 8. Oktober, um 9 Uhr.\n\nKommentier STIMME, dann schick ich dir die Einladung und den Stimm-Check gleich dazu."),
        ],
        caption=cap(
            "Wie viele Prompt-Listen hast du auf dem Handy gespeichert?",
            "Bei den meisten, mit denen ich rede, sind es mehr, als sie je benutzt haben. Und das ist kein Zeichen dafür, dass sie es nicht können. Die Listen sind einfach für niemanden geschrieben, und deshalb kommt aus ihnen ein Text, der zu allen passt.",
            "Im Karussell steht, warum das so ist und was stattdessen hilft: ein Blatt über dich, das die KI jedes Mal zuerst liest, und ein fester Auftrag für jede Arbeit, die jede Woche wiederkommt. Auf Folie sieben steht auch, wofür Listen trotzdem gut sind.",
            "Wie das bei mir aussieht, vom Blatt über mich bis zu den Helfern, die jede Woche für mich arbeiten, zeig ich dir live in meiner kostenlosen Masterclass am Donnerstag, 8. Oktober, um 9 Uhr.",
            "Kommentier STIMME, dann schick ich dir die Einladung, und dazu den Stimm-Check, mit dem du in rund 15 Minuten dein eigenes Blatt hast.",
            lead=True),
        hinweis="Launch KI · KW40 · ⚠️ Auf diesem Tag ist schon „Drei Dinge, warum ich nichts bei dir bestellen würde“ bei Blotato eingeplant (07:30). Liegt hier als Variante — tauschen nur auf dein Wort.",
    ),
    dict(
        id="kw41-kar-m-di-ki", datum="2026-10-06", job="Reichweite", angle="Beweis",
        typ="listicle", funnel="TOF",
        name="KI · Di · Fünf Arbeiten, die ich abgegeben habe",
        slides=[
            ("hook", "Fünf Arbeiten, die ich dieses Jahr abgegeben habe.", "An meine KI-Helfer.\n\nMit vier Kindern und 18 Stunden die Woche fürs Geschäft."),
            ("text", "1 · Den Menüplan", "Früher ein bis zwei Stunden pro Woche.\n\nHeute drei Fragen, dann liegen Menüliste und Einkaufsliste aus meinen Rezepten auf dem Handy. Fünf Minuten."),
            ("text", "2 · Den Tagesplan", "Um halb sieben kommt eine Nachricht aufs Handy: welches Profil heute dran ist, der grosse Brocken des Tages und drei Sachen, die Geld bringen.\n\nBevor ich mich an den Frühstückstisch setze."),
            ("text", "3 · Den Entwurf für die Content-Woche", "Freitags um acht bereitet ein Helfer alle Beiträge der Woche vor, nach meinen Regeln.\n\nIch lese, ändere und gebe frei."),
            ("text", "4 · Das Belege-Suchen", "Die Rechnungen fürs Geschäft sammelt ein Helfer aus meinem Postfach und legt sie beschriftet ab.\n\nFür die Steuer muss ich nichts mehr zusammensuchen."),
            ("text", "5 · Die Begleitung für meine Kundschaft", "Wer bei mir die 30-Tage-Energie-Routine macht, hat eine eigene Seite aufs Handy: Rezepte, Tagesimpuls, Checkliste.\n\nGebaut hat sie die KI nach meiner Anleitung."),
            ("text", "Was alle fünf gemeinsam haben", "Sie laufen jede Woche gleich ab.\n\nUnd ich hab einmal aufgeschrieben, wie ich sie selbst machen würde."),
            ("cta", "Welche wäre deine erste?", "Schau auf deine Woche und such die Arbeit, die jedes Mal gleich abläuft.\n\nSchick das der Freundin, mit der du immer über zu wenig Zeit redest."),
        ],
        caption=cap(
            "Was macht die KI eigentlich konkret bei mir?",
            "Das werde ich oft gefragt, und die ehrliche Antwort ist unspektakulärer, als viele denken. Es sind keine Zauberkunststücke, es sind Arbeiten, die jede Woche gleich ablaufen und die mich früher Stunden gekostet haben.",
            "Im Karussell stehen fünf davon, jede mit einem Satz dazu, wie sie heute läuft. Vom Menüplan bis zur Begleitseite für meine Kundschaft. Auf Folie sieben steht, was alle fünf gemeinsam haben, und genau daran erkennst du deine erste.",
            "Schick das der Freundin, mit der du immer über zu wenig Zeit redest.",
        ),
        hinweis="Launch KI · KW41 · 🟡 Belege-Helfer: Stimmt „sammelt aus meinem Postfach“ so für dich? (Gebaut am 24.09., läuft über Claude.)",
    ),
    dict(
        id="kw41-kar-m-do-ki", datum="2026-10-08", job="Lead", angle="Neugier",
        typ="edukativ", funnel="MOF",
        name="KI · Do · Der feste Auftrag am Menüplan erklärt",
        slides=[
            ("hook", "Machst du jede Woche dieselbe Arbeit wieder von vorne?", "Am Beispiel Menüplan."),
            ("text", "Was ein fester Auftrag ist", "Du schreibst einmal auf, wie du etwas machst.\n\nAb dann sagst du nur noch „mach das“, und die KI weiss, was gemeint ist."),
            ("text", "Teil 1 · Die Fragen, die du dir stellst", "Beim Menüplan sind es drei: Ist nächste Woche etwas Besonderes? Wo bleibt wenig Zeit, oder kommt Besuch? Muss etwas weg?\n\nDie stellt die KI jetzt mir."),
            ("text", "Teil 2 · Woher das Wissen kommt", "Meine eigenen Rezepte, keine aus dem Internet.\n\nBei dir wären es deine Produktinfos, deine Texte, deine Antworten auf Kundenfragen."),
            ("text", "Teil 3 · Wie das Ergebnis aussehen soll", "Eine Menüliste für die Woche und eine Einkaufsliste, fertig aufs Handy.\n\nJe genauer du das beschreibst, desto weniger musst du nachbessern."),
            ("text", "Teil 4 · Was nie vorkommen darf", "Bei mir: kein Fisch, Fleisch höchstens drei-, viermal die Woche, und am Mittag unter der Woche nichts, was länger als 30 bis 40 Minuten am Herd braucht.\n\nDas sind deine Regeln."),
            ("text", "Das Ergebnis", "Früher ein bis zwei Stunden pro Woche.\n\nHeute fünf Minuten, zehn, wenn mir etwas nicht passt."),
            ("text", "Das geht mit jeder Arbeit", "Die Nachfass-Nachricht nach einer Bestellung, die Wochenplanung, die Antwort auf die Frage, die du jede Woche bekommst.\n\nVier Teile, einmal aufgeschrieben."),
            ("cta", "Fürs Schreiben gibt es das auch", "Kommentier STIMME, und der Stimm-Check landet in deinen Nachrichten.\n\nEr ist so ein fester Auftrag, nur für deine Texte."),
        ],
        caption=cap(
            "„Jede Woche dieselbe Arbeit, und jedes Mal fang ich wieder von vorne an.“",
            "Wenn du das kennst, ist ein fester Auftrag für die KI genau das, was dir fehlt. Auf Englisch heisst das Skill, und es klingt komplizierter, als es ist. Ich erklär es dir an meinem Menüplan, weil das jede Mama kennt.",
            "Im Karussell stehen die vier Teile, aus denen so ein Auftrag besteht: die Fragen, die du dir sonst selbst stellst, woher das Wissen kommt, wie das Ergebnis aussehen soll und was nie vorkommen darf. Auf Folie acht steht, bei welchen Arbeiten im Network das genauso geht.",
            "Kommentier STIMME, dann schick ich dir den Stimm-Check, einen festen Auftrag fürs Schreiben, den du in 15 Minuten fertig hast.",
            lead=True),
        hinweis="Launch KI · KW41 · Masterclass-Tag (09:00). Regeln auf Folie 6 aus context/meal-planning-bot.md (kein Fisch · Fleisch 3–4×/Woche · Mittag max. 30–40 Min.).",
    ),
    dict(
        id="kw42-kar-m-di-ki", datum="2026-10-13", job="Reichweite", angle="Konträr",
        typ="kontrovers", funnel="TOF",
        name="KI · Di · Was die KI nicht kann",
        slides=[
            ("hook", "„Wenn die KI das alles kann, braucht mich ja bald keiner mehr.“", "Ich versteh die Angst.\n\nUnd ich sehe jeden Tag, was sie nicht kann."),
            ("text", "Sie hat deine Geschichte nicht erlebt", "Sie kann sie aufschreiben, wenn du sie erzählst.\n\nAber sie weiss nicht, wie es sich angefühlt hat. Das weisst nur du."),
            ("text", "Sie weiss nicht, wer gerade eine schwere Woche hat", "Welche Kundin du heute anrufen solltest, merkst du an einem Satz in einer Nachricht.\n\nDas sieht keine KI."),
            ("text", "Sie ist nicht der Grund, warum jemand bei dir bestellt", "Die Leute bestellen bei dir, weil sie dir vertrauen.\n\nDieses Vertrauen hast du über Jahre aufgebaut, nicht ein Programm."),
            ("text", "Sie entscheidet nicht, was du nie sagen würdest", "Welche Versprechen du nicht machst, welche Wörter nicht zu dir passen, wo deine Grenze ist.\n\nDas legst du fest."),
            ("text", "Was tatsächlich wegfällt", "Ja, manche Arbeit fällt weg: Texte umformulieren, Listen tippen, dieselbe Antwort zum zehnten Mal schreiben.\n\nFür diese Arbeit hat dich nie jemand bezahlt."),
            ("text", "Und wer es anders sieht, hat einen Punkt", "Wer KI nur einsetzt, damit sie für sie denkt, wird tatsächlich austauschbar.\n\nDer Unterschied ist, ob du ihr sagst, wer du bist."),
            ("cta", "Wem schickst du das?", "Schick das der Freundin, die bei KI immer als Erstes sagt, dass sie uns alle ersetzt."),
        ],
        caption=cap(
            "„Wenn die KI das alles kann, braucht mich ja bald keiner mehr.“",
            "Den Satz höre ich im Moment oft, und ich nehme ihn ernst. Deshalb hab ich im Karussell aufgeschrieben, was ich jeden Tag sehe: vier Dinge, die meine KI-Helfer nicht können, egal wie gut sie schreiben.",
            "Und ich sag auch ehrlich, was tatsächlich wegfällt. Es ist die Arbeit, für die dich nie jemand bezahlt hat. Auf Folie sieben steht, wann die Angst berechtigt ist, weil auch das stimmt.",
            "Schick das der Freundin, die bei KI immer als Erstes sagt, dass sie uns alle ersetzt.",
        ),
        hinweis="Launch KI · KW42 · Kontroverser Take mit Nuancierungsfolie (7).",
    ),
    dict(
        id="kw42-kar-m-do-ki", datum="2026-10-15", job="Lead", angle="Neugier",
        typ="edukativ", funnel="MOF",
        name="KI · Do · Was von deiner Kundschaft in die KI darf",
        slides=[
            ("hook", "Darf ich die Daten meiner Kundschaft überhaupt in die KI tippen?", "Die Antwort ist einfacher, als du denkst."),
            ("text", "Das bleibt draussen", "Namen, Adressen, Telefonnummern, Mailadressen.\n\nUnd alles, was jemand dir im Vertrauen über die eigene Gesundheit erzählt hat."),
            ("text", "Auch nicht „nur kurz“", "Die Bestellliste mit Namen, der Screenshot aus dem Chat, die Notiz zur Kundin.\n\nWas einmal drin ist, holst du nicht mehr zurück."),
            ("text", "Das darf rein", "Dein Wissen, deine eigenen Texte, deine Produktinfos in deinen Worten.\n\nDas ist genau das, womit die KI am besten arbeitet."),
            ("text", "Fragen ohne Namen", "Aus „Frau Meier fragt, ob …“ wird „Jemand fragt, ob …“.\n\nDie Antwort ist dieselbe, nur ohne Person dahinter."),
            ("text", "Die Regeln deiner Firma gelten auch hier", "Was du nicht über Wirkung versprechen darfst, darf auch die KI nicht für dich schreiben.\n\nSchreib das in dein Blatt über dich."),
            ("text", "Einmal in den Einstellungen nachschauen", "Viele Programme haben eine Einstellung, ob deine Eingaben zum Trainieren verwendet werden.\n\nSchau nach, und schalte sie aus, wenn du das nicht willst."),
            ("text", "Die Faustregel", "Würdest du es auf eine Postkarte schreiben, die jeder lesen kann?\n\nWenn nicht, bleibt es draussen. Im Zweifel immer draussen."),
            ("cta", "Dein Blatt über dich", "Kommentier STIMME für den Stimm-Check.\n\nDort kommt genau hinein, was bei dir nie vorkommen darf, samt den Regeln deiner Firma."),
        ],
        caption=cap(
            "Was darf von deiner Kundschaft eigentlich in die KI?",
            "Das ist eine der ersten Fragen, die mir Networkerinnen stellen, und ich finde sie richtig. Im Karussell steht, was draussen bleibt, was rein darf und wie du Fragen deiner Kundschaft stellst, ohne dass eine Person dahinter erkennbar ist.",
            "Auf der letzten Folie steht meine Faustregel: Würdest du es auf eine Postkarte schreiben, die jeder lesen kann? Wenn nicht, bleibt es draussen. Das ist keine Rechtsberatung, aber es bewahrt dich vor dem, was du nicht mehr zurückholen kannst.",
            "Kommentier STIMME, dann liegt der Stimm-Check bei dir, in dem du in 15 Minuten festlegst, was bei dir nie vorkommen darf, samt den Regeln deiner Firma.",
            lead=True),
        hinweis="Launch KI · KW42 · Keine Rechtsberatung, steht so in der Caption.",
    ),
    dict(
        id="kw43-kar-m-di-ki", datum="2026-10-20", job="Reichweite", angle="Ergebnis",
        typ="edukativ", funnel="TOF",
        name="KI · Di · Sechs Angaben für deine eigene Stimme",
        slides=[
            ("hook", "Sechs Angaben, und deine KI klingt nicht mehr nach irgendwem.", "Die komplette Liste.\n\nSpeicher sie dir, bevor du den nächsten Text schreiben lässt."),
            ("text", "1 · Wer bist du?", "Was machst du, seit wann, und was würde eine Freundin über dich sagen?\n\nDrei Sätze reichen."),
            ("text", "2 · Für wen schreibst du?", "In welcher Lage steckt diese Person, und was hat sie schon probiert?\n\nDazu ein Satz, den sie selbst so sagen würde."),
            ("text", "3 · Was bietest du an?", "Den Namen und was sich danach verändert.\n\nKeine Liste mit Inhalten."),
            ("text", "4 · Worüber sprichst du, und worüber nie?", "Deine Themen, und ganz ausdrücklich die, die bei dir nichts verloren haben."),
            ("text", "5 · Wie klingst du?", "Lange oder kurze Sätze, Emojis ja oder nein, Mundart, Wörter, die du oft sagst."),
            ("text", "6 · Was kommt bei dir nie vor?", "Wörter, die du nicht magst, und Dinge, die du nie behaupten würdest.\n\nIm Network gehören die Regeln deiner Firma dazu."),
            ("text", "Und das Wichtigste: ein Text von dir", "Ein bis drei Texte, die du selbst geschrieben hast. Eine Caption, eine Mail, eine abgetippte Sprachnachricht.\n\nDaran merkt die KI am meisten, wie du wirklich klingst."),
            ("cta", "Speicher dir die sechs", "Schreib sie einmal auf und gib sie deiner KI jedes Mal mit.\n\nUnd schick das der Freundin, die sagt, KI klinge halt immer gleich."),
        ],
        caption=cap(
            "„Egal was ich eintippe, es klingt nie nach mir.“",
            "Das liegt fast nie an der KI. Sie kennt dich einfach nicht. Hier sind die sechs Angaben, die sie von dir braucht, komplett und ohne Haken. Dazu kommt das Wichtigste auf Folie acht: ein Text, den du selbst geschrieben hast.",
            "Schreib die sechs Antworten einmal auf und gib sie deiner KI jedes Mal mit. Den Unterschied merkst du beim ersten Text.",
            "Schick das der Freundin, die sagt, KI klinge halt immer gleich.",
        ),
        hinweis="Launch KI · KW43 · Gibt den Stimm-Check-Inhalt gratis raus, so im Launch-Kalender gewollt (Reichweite mit echtem Mehrwert).",
    ),
    dict(
        id="kw43-kar-m-do-ki", datum="2026-10-22", job="Lead", angle="Beweis",
        typ="story", funnel="MOF",
        name="KI · Do · Von Freitag 08:00 bis zum fertigen Beitrag",
        slides=[
            ("hook", "Freitag, acht Uhr: Meine Content-Woche fängt an, bevor ich etwas tippe.", ""),
            ("text", "08:00 · Der Helfer startet", "Um acht fängt ein fester Auftrag an zu arbeiten, jeden Freitag gleich.\n\nIch muss dafür nichts anklicken."),
            ("text", "Zuerst: Was beschäftigt meine Leute?", "Er schaut, worüber meine Zielgruppe gerade spricht und was sie beschäftigt.\n\nDaraus kommen die Themen der Woche."),
            ("text", "Dann: die ersten Zeilen", "Für jedes Thema schreibt er Einstiege nach meinen Regeln, und jeder muss durch meinen Check.\n\nWas nach KI klingt, fliegt raus."),
            ("text", "Dann: die ganzen Beiträge", "Reels, Karussells und Captions für beide Profile, fünf Plätze pro Woche.\n\nIn meiner Stimme, weil sie aufgeschrieben ist."),
            ("text", "Alles landet in meiner Übersicht", "Eine Seite, auf der ich die ganze Woche sehe.\n\nIch lese, ändere, oder schreibe in eine Zeile, was anders werden soll."),
            ("text", "Ich gebe frei", "Ein Klick je Beitrag. Die Karussells gehen danach von selbst raus.\n\nDie Reels plane ich in der App ein, wegen der Musik."),
            ("text", "Der eigentliche Trick", "Es ist nicht die Technik.\n\nEs sind die Regeln, die ich einmal aufgeschrieben habe: wie ich klinge, für wen ich schreibe, was nie vorkommt."),
            ("cta", "Fang bei deinen Regeln an", "STIMME in die Kommentare, und du bekommst den Stimm-Check.\n\nDamit schreibst du in 15 Minuten das Wichtigste davon auf."),
        ],
        caption=cap(
            "Wie hängt das bei mir eigentlich alles zusammen?",
            "Das fragen mich gerade viele, und deshalb zeig ich dir meine Freitage einmal von Anfang bis Ende. Um acht Uhr startet ein Helfer und bereitet die ganze Content-Woche vor, und am Ende sitze ich da, lese, ändere und gebe frei.",
            "Im Karussell steht jeder Schritt. Auf Folie acht steht der Teil, den die meisten übersehen: Das Entscheidende sind die Regeln, die ich einmal aufgeschrieben habe. Ohne die würde auch der beste Helfer nach irgendwem klingen.",
            "Kommentier STIMME, dann schick ich dir den Stimm-Check, und in 15 Minuten hast du die wichtigsten deiner Regeln beisammen.",
            lead=True),
        hinweis="Launch KI · KW43 · Ablauf aus dem Scheduled Task „content-woche-freitag“. 🟡 Folie 3: Der Marktcheck läuft nur im begleiteten Modus mit Zitaten — soll der Schritt drinbleiben?",
    ),
]


def reel_doc(r):
    art = r.get("videoart", "broll")
    skript = r.get("skript") or (
        "B-ROLL, ein Clip, rund 7 Sekunden, candid beim Tun (Küche, Alltag) — Clip sucht Claude aus.\n"
        f"TEXT weiss: „{r['text']}“\n" + (f"TEXT orange: „{r['betont']}“\n" if r["betont"] else "") +
        "Kein Schnitt, keine Untertitel, kein Ton — Musik kommt in der App.")
    hook = r["text"] + (" " + r["betont"] if r["betont"] else "")
    return {
        "name": r["name"], "profil": "mentoring", "datum": r["datum"], "videoart": art,
        "hook": hook, "coverhook": r["coverhook"], "coverunter": "", "caption": r["caption"],
        "skript": skript, "hinweis": r["hinweis"], "brand": "mlb_dark", "coverfarbe": "orange",
        "pos": "unten", "scrim": True, "texty": 68, "textskala": 100, "textfrei": False,
        "blotato": {"status": "", "zeit": "21:00"}, "launch": "ki-kurs",
        "job": r["job"], "angle": r["angle"],
        "kommentar": "", "kommentarAntwort": "", "kommentarErledigt": "", "kommentarStand": "",
        "abgelehnt": False, "abgelehntStand": "", "unter": "", "untertitel": "",
        "videourl": "", "videodatei": "", "updatedAt": JETZT,
    }


def folien(k):
    """Titelfolie: nur der erste Absatz als Unterzeile — mehr passt am Handy nicht lesbar
    unter einen grossen Hook (Patricia, 28.09.). Lead-Schlussfolie: Stichwort als Knopf."""
    raus = []
    for i, (l, h, b) in enumerate(k["slides"]):
        s = {"layout": l, "headline": h, "body": b.split("\n\n")[0] if l == "hook" else b}
        if l == "cta" and k["job"] == "Lead":
            s["keyword"] = "STIMME"
        raus.append(s)
    return raus


def kar_doc(k):
    return {
        "name": k["name"], "profil": "mentoring", "datum": k["datum"], "typ": k["typ"],
        "funnel": k["funnel"], "handle": "@mumlifebalance_patricia_ulmann", "brand": k.get("brand", "mlb_light"),
        "slides": folien(k),
        "caption": k["caption"], "hinweis": k["hinweis"], "launch": "ki-kurs",
        "job": k["job"], "angle": k["angle"],
        "blotato": {"status": "", "zeit": "07:30"}, "textfrei": False,
        "kommentar": "", "kommentarAntwort": "", "kommentarErledigt": "", "kommentarStand": "",
        "abgelehnt": False, "abgelehntStand": "", "updatedAt": JETZT,
    }


def main():
    (AUS / "reels").mkdir(parents=True, exist_ok=True)
    (AUS / "karussells").mkdir(parents=True, exist_ok=True)
    zeilen = ["---", "tags: [content, launch, ki]", "---", "",
              "# KI-Launch — Feed Mentoring 30.9.–23.10.2026", "",
              f"Erzeugt von `scripts/launch/feed-ki-launch.py` am {JETZT[:10]}. "
              "Quelle der Themen: [[07-launch-kalender]]. Befund zu den Flops: [[launch-feed-befund]].", ""]
    alle = [("reel", r, reel_doc(r)) for r in REELS] + [("kar", k, kar_doc(k)) for k in KARUSSELLS]
    alle.sort(key=lambda x: x[1]["datum"])
    for art, q, d in alle:
        ordner = "reels" if art == "reel" else "karussells"
        (AUS / ordner / f"{q['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        zeilen += [f"## {q['datum']} · {d['name']}", "",
                   f"**{ 'Reel · ' + d['videoart'] if art == 'reel' else 'Karussell · ' + d['typ']}** · {q['job']} · {q['angle']} · Kennung `{q['id']}`", ""]
        if art == "reel":
            zeilen += [f"**Hook:** {d['hook']}", "", f"**Cover:** {d['coverhook']}", "", "```", d["skript"], "```", ""]
        else:
            for i, s in enumerate(d["slides"], 1):
                zeilen += [f"**Folie {i} — {s['headline']}**", "", s["body"], ""]
        zeilen += ["**Caption:**", "", d["caption"] or "_(folgt nach dem Dreh)_", "", f"> {d['hinweis']}", ""]
    MD.parent.mkdir(parents=True, exist_ok=True)
    MD.write_text("\n".join(zeilen), encoding="utf-8")
    print(f"{len(REELS)} Reels · {len(KARUSSELLS)} Karussells → {AUS}")
    print(f"Markdown → {MD}")


if __name__ == "__main__":
    main()
