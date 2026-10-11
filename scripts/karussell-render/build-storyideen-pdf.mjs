#!/usr/bin/env node
// Baut das Workbook "90 Storyideen für Networkerinnen" als ausfüllbares Brand-PDF.
// Datenstruktur -> HTML (Brand-CSS) -> Puppeteer A4-PDF.
import puppeteer from 'puppeteer';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..', '..');
const OUT_DIR = path.join(REPO_ROOT, 'outputs', 'produkte', 'storyideen-networkerinnen');
const HTML_PATH = path.join(OUT_DIR, 'workbook-print.html');
const PDF_PATH = path.join(OUT_DIR, '90-storyideen-fuer-networkerinnen.pdf');

// ---------------------------------------------------------------------------
// INHALT
// ---------------------------------------------------------------------------
const chapters = [
  {
    num: 1, icon: '❤️', accent: 'petrol', anlass: 'Nähe',
    title: 'Dein Alltag & du als Mensch',
    subtitle: 'Die einfachsten Stories überhaupt. Kein Produkt, kein Thema — nur du. Und genau die schaffen am meisten Vertrauen.',
    ideas: [
      { t: 'Ein ganz normaler Morgen bei dir', p: 'Zeig einfach, wie dein Tag anfängt. Kaffee, Chaos, Kinder, Stille — was auch immer.', ex: '„6 Uhr, das Haus schläft noch, und ich sitze mit meinem Kaffee am Küchentisch und plane meinen Tag. Diese halbe Stunde gehört nur mir. Wie sieht dein Morgen aus?"' },
      { t: 'Der Moment, in dem heute alles schiefging', p: 'Ein kleines Missgeschick, ehrlich und mit Humor erzählt. Nichts verbindet mehr als „mir passiert das auch".', ex: '„Ich hatte einen wichtigen Call — und mein Kind kommt weinend rein, weil der Turnbeutel weg ist. Willkommen im echten Business-Alltag."' },
      { t: 'Was gerade auf deinem Schreibtisch liegt', p: 'Ein Foto von deinem Arbeitsplatz, so wie er wirklich aussieht.', ex: '„So sieht\'s gerade bei mir aus: drei Notizzettel, ein kalter Tee und eine To-do-Liste, die mich auslacht. Wer kennt\'s?"' },
      { t: 'Deine kleine Freude des Tages', p: 'Ein Moment, der dich heute glücklich gemacht hat. Ganz klein darf er sein.', ex: '„Ich hab heute zum ersten Mal seit Wochen wieder in Ruhe ein Buch gelesen. 20 Minuten. Und es hat sich angefühlt wie Urlaub."' },
      { t: 'Wie du deine Pausen verbringst', p: 'Zeig, dass du auch mal nichts tust. Das nimmt den Druck raus — bei dir und deinen Followern.', ex: '„Mein Sonntagnachmittag: Sofa, Decke, kein Handy. Ich hab gelernt, dass Pause kein Luxus ist, sondern Teil der Arbeit."' },
      { t: 'Dein Lieblingsplatz zum Arbeiten', p: 'Wo entstehen deine besten Ideen? Zeig den Ort.', ex: '„Meine besten Ideen kommen nicht am Schreibtisch, sondern im Auto. Kein Witz. Musik laut, allein, und plötzlich ist der Kopf frei."' },
      { t: 'Ein Blick aus deinem Fenster', p: 'So simpel, so schön. Zeig einfach, wo du gerade bist.', ex: '„Das ist mein Ausblick beim Arbeiten. An manchen Tagen vergesse ich, wie sehr ich das hier liebe."' },
      { t: 'Womit du gerade kämpfst (ehrlich)', p: 'Kein Drama, aber auch keine Hochglanz-Fassade. Eine echte Herausforderung im Moment.', ex: '„Gerade fällt es mir schwer, Arbeit und Familie unter einen Hut zu bringen. Ich sag\'s laut, weil ich weiss, ich bin nicht die Einzige."' },
      { t: 'Deine ehrliche Abend-Bilanz', p: 'Wie war dein Tag wirklich? Zeig auch die durchwachsenen.', ex: '„Heute war so ein Tag, an dem meine Liste länger wurde statt kürzer. Und weisst du was? Das ist okay. Morgen ist auch noch ein Tag."' },
      { t: 'Was du gerade lernst', p: 'Ein Buch, ein Kurs, ein Podcast — teil, was dich gerade weiterbringt.', ex: '„Ich stecke gerade tief in einem Thema drin und sauge alles auf wie ein Schwamm. Ich liebe dieses Gefühl, wenn der Kopf raucht."' },
      { t: 'Dein kleines Ritual', p: 'Etwas, das du jeden Tag machst und das dir guttut.', ex: '„Bevor ich abends das Handy weglege, schreibe ich drei Dinge auf, die heute gut waren. Klingt kitschig, verändert aber alles."' },
      { t: 'Ein Foto von vor ein paar Jahren', p: 'Zeig, wie weit du gekommen bist — im Kleinen oder im Grossen.', ex: '„Dieses Foto ist von vor zwei Jahren. Ich hätte damals nie gedacht, wo ich heute stehe. Und wenn ich das schaffe, dann du auch."' },
      { t: 'Was dich heute zum Lachen gebracht hat', p: 'Humor macht nahbar. Teil einen Moment, über den du lachen musstest.', ex: '„Meine Tochter hat mich heute gefragt, ob ich am Handy \'wichtige Sachen\' mache oder nur Katzen anschaue. Ehrliche Kinder, ehrliche Antworten."' },
      { t: 'Dein Wochenend-Modus', p: 'Zeig, wie du abschaltest. Menschen lieben es zu sehen, dass du auch ein Leben hast.', ex: '„Am Wochenende bin ich nicht Businessfrau, sondern einfach Mama. Handy in der Schublade, Kopf im Hier und Jetzt."' },
    ],
  },
  {
    num: 2, icon: '❤️', accent: 'teal', anlass: 'Nähe',
    title: 'Dein Warum & deine Geschichte',
    subtitle: 'Deine Geschichte ist das Einzige, was niemand kopieren kann. Sie ist der stärkste Grund, warum Menschen ausgerechnet dir folgen.',
    ideas: [
      { t: 'Der Moment, in dem du „jetzt reicht\'s" gedacht hast', p: 'Was war der Auslöser, dass du etwas verändern wolltest?', ex: '„Es gab diesen einen Moment, in dem ich mir dachte: So kann es nicht weitergehen. Ich will nicht funktionieren — ich will leben."' },
      { t: 'Warum du dich für diesen Weg entschieden hast', p: 'Erzähl, was dich zu deinem Business gebracht hat — abseits vom Produkt.', ex: '„Ich wollte ein eigenes Einkommen, das zu meinem Leben passt. Nicht mehr abhängig sein, nicht mehr fragen müssen. Das war mein Warum."' },
      { t: 'Was du früher gemacht hast', p: 'Dein Vorher. Wo kommst du her? Das schafft Identifikation.', ex: '„Bevor ich das hier gemacht habe, war ich in einem ganz anderen Beruf. Und trotzdem hat mich immer dasselbe angetrieben: Menschen weiterzuhelfen."' },
      { t: 'Dein grösster Zweifel am Anfang', p: 'Sei ehrlich über die Angst, die du am Start hattest.', ex: '„Am Anfang dachte ich ständig: Wer bin ich, dass mir jemand zuhört? Heute weiss ich — genau dieser Gedanke hält die meisten zurück."' },
      { t: 'Der erste kleine Erfolg, der alles verändert hat', p: 'Nicht der grosse Durchbruch — der erste kleine Moment, in dem du dachtest: Es funktioniert.', ex: '„Die erste Nachricht von jemandem, dem ich wirklich helfen konnte — die hab ich heute noch. Ab da wusste ich, ich bin auf dem richtigen Weg."' },
      { t: 'Was du deinem früheren Ich sagen würdest', p: 'Ein Rat an dich selbst, als du angefangen hast.', ex: '„Wenn ich mit mir von vor zwei Jahren reden könnte, würde ich sagen: Hör auf zu warten, bis du bereit bist. Fang einfach an."' },
      { t: 'Ein Mensch, der an dich geglaubt hat', p: 'Wer hat dich unterstützt, als du selbst noch gezweifelt hast?', ex: '„Es gab eine Person, die von Anfang an gesagt hat: Du schaffst das. An manchen Tagen war das das Einzige, woran ich mich festgehalten hab."' },
      { t: 'Ein Rückschlag und was du daraus gelernt hast', p: 'Etwas, das nicht funktioniert hat — und was du mitgenommen hast.', ex: '„Ich hab mal etwas gestartet, das komplett gefloppt ist. Niemand hat gekauft. Heute weiss ich, warum — und genau das hat mich besser gemacht."' },
      { t: 'Warum du nicht aufgegeben hast', p: 'Es gab bestimmt einen Punkt, an dem du fast hingeschmissen hättest. Erzähl davon.', ex: '„Es gab Wochen, in denen ich dachte, ich lass es sein. Was mich gehalten hat? Die Vorstellung, wie mein Leben aussieht, wenn ich dranbleibe."' },
      { t: 'Dein grösster Antrieb heute', p: 'Was treibt dich morgens an? Wofür machst du das alles?', ex: '„Ich mach das nicht für ein Ranking oder einen Titel. Ich mach das, damit meine Kinder eine Mama erleben, die ihren eigenen Weg geht."' },
      { t: 'Wie du zu der Person geworden bist, die du heute bist', p: 'Ein Wendepunkt, der dich geprägt hat.', ex: '„Es gibt einen Moment, der mich zu der Frau gemacht hat, die ich heute bin. Und der hatte erstmal gar nichts mit Business zu tun."' },
      { t: 'Was du an deinem Leben heute liebst', p: 'Zeig, wofür sich der Weg gelohnt hat — konkret und ehrlich.', ex: '„Dass ich heute aufstehen kann, wann ich will, und trotzdem für meine Familie da bin — dafür hab ich lange gearbeitet. Und es fühlt sich jeden Tag richtig an."' },
    ],
  },
  {
    num: 3, icon: '💡', accent: 'orange', anlass: 'Mehrwert',
    title: 'Mehrwert & Mini-Trainings zu deinem Thema',
    subtitle: 'Hier zeigst du, dass du weisst, wovon du sprichst — bei deinem Thema, nicht bei deinem Produkt. Nutze deinen Satz aus Übung 1 als Kompass.',
    ideas: [
      { t: 'Ein einfacher Tipp, den man heute umsetzen kann', p: 'Ein kleiner, konkreter Schritt zu deinem Thema, der sofort was bringt.', ex: '„Ein simpler Trick gegen das Nachmittagstief: ein grosses Glas Wasser, bevor du zum Kaffee greifst. Klingt banal, wirkt aber."' },
      { t: 'Der grösste Fehler, den du immer wieder siehst', p: 'Ein typischer Fehler bei deinem Thema — und wie man ihn vermeidet.', ex: '„Der grösste Fehler, den ich immer wieder sehe: Menschen ändern alles auf einmal und geben nach drei Tagen auf. Fang mit einer Sache an."' },
      { t: 'Ein Glaubenssatz, der deine Menschen zurückhält', p: 'Nenn eine falsche Überzeugung und stell ihr eine bessere gegenüber.', ex: '„Viele denken, sie hätten keine Zeit für Veränderung. Die Wahrheit ist: Es geht nicht um Zeit, es geht um die ersten fünf Minuten."' },
      { t: 'Drei Dinge, die du früher gern gewusst hättest', p: 'Deine wichtigsten Learnings zu deinem Thema, kompakt.', ex: '„Drei Dinge, die ich gern früher gewusst hätte: Weniger ist mehr. Dranbleiben schlägt perfekt. Und: Du musst nicht alles allein machen."' },
      { t: 'Eine kleine Anleitung in Schritten', p: 'Zerleg etwas aus deinem Thema in einfache Schritte.', ex: '„So startest du in einen ruhigeren Morgen — in drei Schritten: 1. Handy erst nach dem Frühstück. 2. Ein Glas Wasser. 3. Drei tiefe Atemzüge."' },
      { t: 'Beantworte eine Frage, die dir oft gestellt wird', p: 'Was fragen dich Menschen immer wieder? Antworte ausführlich.', ex: '„Ich werde oft gefragt, wie ich das alles unter einen Hut bringe. Meine ehrliche Antwort: Ich mache nicht alles — ich mache das Richtige."' },
      { t: 'Ein Mythos in deinem Bereich, den du aufklärst', p: 'Räum mit einer verbreiteten Fehlannahme auf.', ex: '„Der Mythos, du müsstest Tausende Follower haben, um erfolgreich zu sein? Vergiss ihn. Es geht um die richtigen, nicht um die vielen."' },
      { t: 'Was du selbst gerade zu deinem Thema ausprobierst', p: 'Zeig dich als jemand, der auch noch lernt und testet.', ex: '„Ich teste gerade eine neue Morgenroutine und nehme euch mit. Tag 1 war ehrlich gesagt holprig, aber ich bleib dran."' },
      { t: 'Ein Vorher-Nachher zu deinem Thema', p: 'Zeig eine Veränderung — bei dir oder allgemein — ganz ohne Produktfokus.', ex: '„Vor einem Jahr war mein Kopf abends noch voll mit To-dos. Heute schlafe ich ruhiger. Was sich verändert hat, erzähl ich dir gleich."' },
      { t: 'Die eine Sache, mit der man anfangen sollte', p: 'Wenn jemand nur eine Sache umsetzen würde — welche?', ex: '„Wenn du nur eine Sache änderst, dann diese: Hör auf, dich mit anderen zu vergleichen. Dein Weg ist deiner. Punkt."' },
      { t: 'Ein Quiz oder eine Wissensfrage zu deinem Thema', p: 'Nutze den Quiz- oder Umfrage-Sticker und bau Interaktion ein.', ex: '„Kleine Frage zum Mitmachen: Was gibt dir mehr Energie — 10 Minuten Bewegung oder 10 Minuten Handy-Pause? Stimm ab!"' },
      { t: 'Was du jemandem am Anfang raten würdest', p: 'Dein bester Einstiegs-Tipp für Neulinge in deinem Thema.', ex: '„Wenn du gerade erst anfängst: Mach es dir nicht zu kompliziert. Ein kleiner Schritt, jeden Tag, schlägt jeden perfekten Plan."' },
      { t: 'Ein häufiges Missverständnis, das du klarstellst', p: 'Etwas, das oft falsch verstanden wird bei deinem Thema.', ex: '„Viele glauben, Selbstfürsorge sei egoistisch. Dabei ist sie das Gegenteil — nur wer selbst aufgetankt ist, kann für andere da sein."' },
      { t: 'Deine ehrliche Meinung zu einem aktuellen Trend', p: 'Ordne einen Trend aus deinem Bereich ein — mit deiner eigenen Sicht.', ex: '„Alle reden gerade über diesen einen Trend. Meine ehrliche Meinung? Für manche super, für die meisten überschätzt. Und hier ist, warum."' },
      { t: 'Ein Werkzeug oder eine Methode, die dir hilft', p: 'Zeig etwas, das du im Alltag nutzt — kein Produkt, sondern eine Methode.', ex: '„Meine Rettung im Alltag: eine simple Wochenplanung am Sonntagabend. 15 Minuten, und die ganze Woche fühlt sich sortierter an."' },
      { t: 'Was passiert, wenn man nichts ändert', p: 'Mach den Schmerz sichtbar, ganz ohne Panikmache — mit Wärme.', ex: '„Ich sag dir das, weil ich\'s selbst kenne: Wenn du nichts änderst, sitzt du in einem Jahr an genau demselben Punkt. Das muss nicht sein."' },
    ],
  },
  {
    num: 4, icon: '💡', accent: 'petrol', anlass: 'Haltung',
    title: 'Haltung & Meinung',
    subtitle: 'Klare Kante schafft Verbindung. Wer für etwas steht, zieht die richtigen Menschen an — und darf ruhig die falschen abstossen.',
    ideas: [
      { t: 'Eine Meinung, für die du einstehst', p: 'Sag klar, wofür du stehst — auch wenn\'s nicht jedem passt.', ex: '„Ich glaube nicht an das ständige Höher-schneller-weiter. Ich glaube an ein Business, das zu deinem Leben passt — nicht andersrum."' },
      { t: 'Etwas, das dich in deiner Branche stört', p: 'Benenn ehrlich, was dir gegen den Strich geht.', ex: '„Was mich wirklich stört: dieses ewige Vorspielen von Perfektion. Kein Mensch lebt so. Ich zeig lieber, wie\'s wirklich ist."' },
      { t: 'Ein „unpopulärer" Gedanke', p: 'Sprich etwas aus, das viele denken, aber wenige sagen.', ex: '„Unpopuläre Meinung: Du brauchst nicht noch einen Kurs. Du brauchst den Mut, das umzusetzen, was du längst weisst."' },
      { t: 'Woran du glaubst, wenn es um deine Arbeit geht', p: 'Deine Grundüberzeugung, dein Leitsatz.', ex: '„Für mich heisst helfen nicht verkaufen um jeden Preis. Für mich heisst es: den Menschen wirklich sehen. Der Rest ergibt sich."' },
      { t: 'Was du in der Network-Welt anders machst', p: 'Zeig, dass es auch anders geht — ehrlich, ohne die Branche schlechtzureden.', ex: '„Ich mach das hier anders. Ich stell nicht das Produkt in den Mittelpunkt, sondern den Menschen und sein Thema. Das ändert alles."' },
      { t: 'Ein Satz, den du nicht mehr hören kannst', p: 'Eine Floskel oder ein Klischee, das dich nervt — mit deiner Gegenposition.', ex: '„Ich kann den Satz \'Das läuft von allein\' nicht mehr hören. Nichts läuft von allein. Aber mit dem richtigen System läuft\'s leichter."' },
      { t: 'Wofür du früher Kritik bekamst — und heute stolz bist', p: 'Etwas, das dich ausmacht und für das du dich nicht mehr rechtfertigst.', ex: '„Früher hiess es, ich sei zu direkt. Heute ist genau das der Grund, warum Menschen mir vertrauen. Ich sag, was ist."' },
      { t: 'Deine Antwort auf einen typischen Einwand', p: 'Was sagst du zu jemandem, der zweifelt?', ex: '„\'Ich hab keine Zeit dafür\' — den Satz höre ich oft. Meine Antwort: Du hast keine Zeit, weil du kein System hast. Genau da fangen wir an."' },
      { t: 'Was du dir für deine Branche wünschst', p: 'Eine Zukunftsvision oder ein Wunsch für dein Feld.', ex: '„Ich wünsche mir eine Network-Welt, in der Frauen nicht ihre Freundschaften verlieren, weil sie was verkaufen. Das geht — anders."' },
      { t: 'Ein Wert, der dir wichtiger ist als schneller Erfolg', p: 'Zeig, was für dich zählt, jenseits von Zahlen.', ex: '„Mir ist Ehrlichkeit wichtiger als der schnelle Abschluss. Lieber verkaufe ich weniger und schlafe ruhig, als andersrum."' },
    ],
  },
  {
    num: 5, icon: '❤️', accent: 'teal', anlass: 'Nähe',
    title: 'Verbindung & Interaktion',
    subtitle: 'Diese Stories bauen Reichweite und Nähe. Frag, lass abstimmen, lass die Menschen mitmachen. Nichts bindet mehr als das Gefühl, gesehen zu werden.',
    ideas: [
      { t: 'Eine Frage in die Runde', p: 'Frag deine Community etwas Persönliches oder zu deinem Thema.', ex: '„Mal ganz ehrlich: Was ist gerade deine grösste Herausforderung im Alltag? Schreib mir — ich lese wirklich jede Antwort."' },
      { t: 'Diese-oder-jene-Umfrage', p: 'Eine einfache Entweder-oder-Frage mit dem Umfrage-Sticker.', ex: '„Team Frühaufsteherin oder Team Nachteule? Ich bin eindeutig Erstes — verrat mir deins!"' },
      { t: 'Eine lustige, private Frage', p: 'Etwas Leichtes, das nichts mit Business zu tun hat.', ex: '„Wichtige Grundsatzfrage am Montag: Nutella mit oder ohne Butter? Es gibt nur eine richtige Antwort."' },
      { t: 'Fünf Dinge, die man nicht über dich weiss', p: 'Kleine private Fakten, die dich menschlich machen.', ex: '„5 Dinge, die die wenigsten über mich wissen: Ich höre meine Musik viel zu laut. Ich lese jeden Abend. Und ich hasse Kälte abgrundtief."' },
      { t: 'Frag nach Empfehlungen', p: 'Lass deine Community dir was empfehlen — Bücher, Serien, Rezepte.', ex: '„Ich brauche eine neue Serie für die Abende. Was schaust du gerade und kannst es nicht mehr aufhören? Her damit!"' },
      { t: 'Ein Bilderrätsel oder eine Schätzfrage', p: 'Lass die Menschen mitraten.', ex: '„Errätst du, wo dieses Foto entstanden ist? Kleiner Tipp: Es ist einer meiner Lieblingsorte zum Auftanken."' },
      { t: 'Deine Lieblings-Sache und warum', p: 'Teil etwas, das du liebst, und frag nach dem Lieblings-Gegenstück.', ex: '„Mein Lieblingsessen könnte ich jeden Tag essen. Und deins? Ich sammle gerade Ideen fürs Wochenende."' },
      { t: 'Ein „Frag mich alles"', p: 'Öffne die Bühne für Fragen deiner Community.', ex: '„Heute mal andersrum: Frag mich, was du schon immer wissen wolltest — über mich, mein Thema, meinen Alltag. Ich beantworte alles ehrlich."' },
      { t: 'Zeig zwei Optionen und lass abstimmen', p: 'Beteilige deine Community an einer echten Entscheidung.', ex: '„Ich kann mich nicht entscheiden: Soll ich beim nächsten Mal über Thema A oder Thema B sprechen? Du entscheidest mit!"' },
      { t: 'Ein Wochenrückblick zum Mitreden', p: 'Teil dein Highlight der Woche und frag nach ihrem.', ex: '„Mein Highlight diese Woche: ein langer Spaziergang ganz ohne Handy. Was war deins? Erzähl mir davon."' },
      { t: 'Feiere deine Community', p: 'Zeig Reaktionen, Antworten oder markiere Menschen, die mitmachen.', ex: '„Ich bin gerade so berührt von euren Antworten von gestern. Ihr seid der Grund, warum ich das hier so liebe. Danke."' },
    ],
  },
  {
    num: 6, icon: '❤️', accent: 'orange', anlass: 'Nähe',
    title: 'Hinter den Kulissen deines Business',
    subtitle: 'Menschen lieben es, mitgenommen zu werden. Zeig, wie du arbeitest, wie dein Weg wirklich aussieht — das macht dein Business greifbar, lange bevor du etwas verkaufst.',
    ideas: [
      { t: 'Wie ein Arbeitstag bei dir wirklich aussieht', p: 'Nimm deine Community mit durch einen Tag — ehrlich, mit allen Ecken.', ex: '„Ihr denkt, mein Tag sieht aus wie auf den perfekten Fotos? Weit gefehlt. Hier ist mein echter Tag — zwischen Calls und Wäscheberg."' },
      { t: 'Woran du gerade arbeitest', p: 'Gib einen Einblick in ein Projekt, ohne schon zu verkaufen.', ex: '„Ich bastle gerade an etwas, das mir richtig Freude macht. Verrate noch nicht, was — aber ich nehm euch mit auf dem Weg dahin."' },
      { t: 'Wie du dich organisierst', p: 'Zeig dein System — Kalender, Notizen, Tools.', ex: '„Ohne mein System wäre ich verloren. So plane ich meine Woche, damit trotz vier Kindern nichts hinten runterfällt."' },
      { t: 'Ein Blick auf dein Team oder deine Community', p: 'Zeig die Menschen, mit denen du arbeitest — die Verbindung dahinter.', ex: '„Das Schönste an dem, was ich mache, sind die Frauen, die den Weg mit mir gehen. Diese Verbindung hätte ich früher nie erwartet."' },
      { t: 'Eine Investition, die du in dich gemacht hast', p: 'Zeig, dass du selbst in dein Wachstum investierst.', ex: '„Ich hab vor Kurzem in mich selbst investiert — und obwohl es Überwindung gekostet hat, war\'s die beste Entscheidung. Wachstum kostet Mut."' },
      { t: 'Was du an deiner Arbeit am meisten liebst', p: 'Der emotionale Kern deines Business.', ex: '„Was ich am meisten liebe? Diese Momente, in denen jemand sagt: \'Wegen dir hab ich\'s endlich angepackt.\' Dafür mach ich das."' },
      { t: 'Dein grösster Learning-Moment als Unternehmerin', p: 'Etwas, das dich beruflich weitergebracht hat.', ex: '„Mein grösstes Learning: Ich muss nicht alles allein machen. Als ich das verstanden hab, wurde plötzlich alles leichter."' },
      { t: 'Wie du mit schwierigen Tagen umgehst', p: 'Zeig, dass es auch bei dir Durchhänger gibt — und wie du damit umgehst.', ex: '„Auch ich hab Tage, an denen ich am liebsten alles hinschmeissen würde. Was mir hilft: kurz rausgehen, durchatmen, eine Sache nach der anderen."' },
      { t: 'Ein Meilenstein, den du gefeiert hast', p: 'Ein Erfolg — auch ein kleiner —, den du mit deiner Community teilst.', ex: '„Kleiner Moment, grosse Freude: Diese Woche ist etwas passiert, worauf ich lange hingearbeitet hab. Ich musste es einfach mit euch teilen."' },
      { t: 'Wie du Familie und Business unter einen Hut bringst', p: 'Der ehrliche Blick auf deine Vereinbarkeit.', ex: '„Vereinbarkeit klingt immer so schön. In echt heisst das: Ich arbeite in den Lücken, die der Tag mir lässt — und hab damit meinen Frieden gemacht."' },
      { t: 'Was dich an deiner eigenen Entwicklung überrascht', p: 'Zeig, wie du über dich selbst hinausgewachsen bist.', ex: '„Die Frau, die vor zwei Jahren angefangen hat, hätte sich das hier nie zugetraut. Manchmal überrasche ich mich selbst am meisten."' },
    ],
  },
  {
    num: 7, icon: '📨', accent: 'petrol', anlass: 'Einladung',
    title: 'Die dezente Einladung',
    subtitle: 'Jetzt kommt der Teil, vor dem sich viele drücken: dein Angebot sichtbar machen. Aber Achtung — auch hier steht nicht das Produkt im Fokus, sondern die Veränderung, die du ermöglichst.',
    ideas: [
      { t: 'Für wen das Richtige ist, was du machst', p: 'Beschreib deine Wunschperson so genau, dass sie sich erkennt.', ex: '„Das hier ist für dich, wenn du seit Monaten viel gibst und trotzdem das Gefühl hast, auf der Stelle zu treten. Genau da hol ich dich ab."' },
      { t: 'Für wen es NICHT das Richtige ist', p: 'Grenz dich ehrlich ab — das schafft Vertrauen und zieht die Richtigen an.', ex: '„Ehrlich? Wenn du auf ein Wunder über Nacht hoffst, bin ich nicht die Richtige für dich. Wenn du bereit bist, dranzubleiben, dann schon."' },
      { t: 'Die Veränderung, die möglich ist', p: 'Zeig das Ergebnis, nicht das Produkt — den Zustand danach.', ex: '„Stell dir vor, du gehst abends ins Bett, ohne das Gefühl, wieder nichts geschafft zu haben. Genau dahin arbeiten wir gemeinsam."' },
      { t: 'Eine ehrliche Kundenstimme', p: 'Teil eine Rückmeldung — mit dem Weg dahinter, nicht nur dem Lob.', ex: '„Eine Kundin hat mir geschrieben: \'Ich hätte nie gedacht, dass sich so schnell was ändern kann.\' Genau für solche Nachrichten mach ich das."' },
      { t: 'Wie der erste Schritt mit dir aussieht', p: 'Nimm die Hürde raus, indem du zeigst, wie einfach der Einstieg ist.', ex: '„Du musst nicht gleich alles umkrempeln. Der erste Schritt ist ein ehrliches Gespräch — unverbindlich, ohne Verkaufsdruck. Schreib mir einfach."' },
      { t: 'Beantworte die häufigste Frage zu deinem Angebot', p: 'Räum einen typischen Zweifel aus dem Weg.', ex: '„Die Frage, die mir am häufigsten gestellt wird: \'Funktioniert das auch bei mir?\' Meine Antwort: Wenn du bereit bist, dann ja. Und hier ist, warum."' },
      { t: 'Erzähl von einem typischen Aha-Moment deiner Kundinnen', p: 'Zeig, was Menschen bei dir erleben — als Geschichte.', ex: '„Es gibt diesen einen Moment, den fast alle bei mir erleben: wenn sie merken, dass es nie am Produkt lag, sondern an ihrer Positionierung."' },
      { t: 'Zeig, was du gerade anbietest — beiläufig', p: 'Erwähne dein Angebot als selbstverständlichen Teil deines Alltags.', ex: '„Gerade sind ein paar Plätze frei, um mit mir zu arbeiten. Kein Druck — aber wenn du schon länger überlegst, ist jetzt ein guter Moment."' },
      { t: 'Der Unterschied zwischen jetzt handeln und weiter warten', p: 'Mach den Unterschied fühlbar — mit Wärme, nicht mit Angst.', ex: '„Du kannst in einem Jahr an genau demselben Punkt stehen. Oder du fängst heute an. Ich sag dir das, weil ich dir diesen Umweg ersparen will."' },
      { t: 'Eine Einladung mit klarem nächsten Schritt', p: 'Sag konkret, was jemand tun soll, der Interesse hat.', ex: '„Wenn dich das anspricht, schreib mir einfach das Wort \'START\' in die Antwort — dann schicke ich dir alle Infos ganz in Ruhe."' },
      { t: 'Zeig einen Blick in dein Angebot', p: 'Gib einen ehrlichen Einblick, was Menschen bei dir erwartet.', ex: '„Ein kleiner Blick hinter die Kulissen von dem, was wir gemeinsam machen: kein Zaubertrick, sondern klare Schritte, die zu deinem Leben passen."' },
      { t: 'Warum jetzt der richtige Zeitpunkt ist (wenn er\'s ist)', p: 'Nur, wenn es echt ist — ein ehrlicher Grund, warum gerade jetzt.', ex: '„Ich starte im nächsten Monat mit einer kleinen Gruppe. Klein, weil ich mit jeder wirklich arbeiten will. Wenn du dabei sein willst, meld dich."' },
    ],
  },
  {
    num: 8, icon: '❤️', accent: 'teal', anlass: 'Nähe',
    title: 'Die kleinen Extras',
    subtitle: 'Vier Ideen für Tage, an denen du kaum Zeit hast. Eine Slide, ein Satz — reicht auch.',
    ideas: [
      { t: 'Ein Zitat, das dich gerade begleitet', p: 'Teil einen Satz, der dir wichtig ist — mit deinem Gedanken dazu.', ex: '„Dieser Satz begleitet mich gerade: \'Etwas ändern statt es hinnehmen.\' Für mich ist das kein Spruch, sondern eine Entscheidung."' },
      { t: 'Ein Gruss mit Substanz', p: 'Kein blosses „Hallo" — sondern ein Gruss mit einem kleinen Gedanken.', ex: '„Bevor du in den Tag startest: Du musst heute nicht alles schaffen. Nur das, was wirklich zählt. Der Rest kann warten."' },
      { t: 'Eine ehrliche Ein-Wort-Stimmung', p: 'Sag mit einem Wort, wie\'s dir geht — und lad zum Mitmachen ein.', ex: '„Meine Stimmung heute in einem Wort: dankbar. Und deine? Antworte mir mit einem Wort."' },
      { t: 'Ein Reminder an deine Community', p: 'Ein kurzer, warmer Zuspruch, der genau die Richtige erreicht.', ex: '„Falls dir das heute keiner sagt: Du machst das gut. Auch wenn\'s sich gerade nicht so anfühlt. Dranbleiben lohnt sich."' },
    ],
  },
];

// ---------------------------------------------------------------------------
// HTML-RENDERING
// ---------------------------------------------------------------------------
let counter = 0;
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const lines = (n) => Array.from({ length: n }, () => '<div class="fill-line"></div>').join('');

function renderIdea(idea) {
  counter += 1;
  return `
    <div class="idea">
      <div class="idea-head">
        <span class="idea-num">${counter}</span>
        <h3 class="idea-title">${esc(idea.t)}</h3>
      </div>
      <p class="idea-prompt">${esc(idea.p)}</p>
      <div class="idea-ex"><span class="ex-label">Beispiel</span> ${esc(idea.ex)}</div>
      <div class="idea-fill"><span class="fill-label">Deine Idee</span>${lines(2)}</div>
    </div>`;
}

function renderChapter(ch) {
  return `
    <section class="chapter accent-${ch.accent}">
      <div class="chapter-divider">
        <div class="ch-num">Kapitel ${ch.num}</div>
        <div class="ch-icon">${ch.icon}</div>
        <h2 class="ch-title">${esc(ch.title)}</h2>
        <span class="ch-anlass">${ch.anlass}</span>
        <p class="ch-sub">${esc(ch.subtitle)}</p>
      </div>
      <div class="ideas">
        ${ch.ideas.map(renderIdea).join('')}
      </div>
    </section>`;
}

const speicherRows = Array.from({ length: 10 }, () =>
  '<tr><td class="sp-idea"></td><td class="sp-anlass"></td><td class="sp-when"></td></tr>').join('');

const html = `<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Philosopher:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap');

:root {
  --petrol: #12828c;
  --teal: #29556d;
  --creme: #f1ecdd;
  --orange: #dc822e;
  --ink: #29556d;
  --paper: #ffffff;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

@page {
  size: A4;
  margin: 18mm 16mm 16mm 16mm;
}
@page :first { margin: 0; }

html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }

body {
  font-family: 'Source Sans 3', system-ui, sans-serif;
  color: var(--ink);
  font-size: 11pt;
  line-height: 1.55;
}

h1, h2, h3, .ch-num, .idea-num, .cover-kicker { font-family: 'Philosopher', Georgia, serif; }

/* ---------- COVER ---------- */
.cover {
  width: 210mm; height: 297mm;
  background: var(--petrol);
  color: var(--creme);
  display: flex; flex-direction: column;
  justify-content: center; align-items: center;
  text-align: center; padding: 30mm 24mm;
  page-break-after: always;
  position: relative;
}
.cover-kicker {
  text-transform: uppercase; letter-spacing: 4px;
  font-size: 12pt; color: var(--orange); margin-bottom: 14mm; font-weight: 700;
}
.cover h1 {
  font-size: 46pt; line-height: 1.08; font-weight: 700; margin-bottom: 8mm;
}
.cover .cover-num { color: var(--orange); }
.cover-sub {
  font-size: 15pt; font-weight: 300; max-width: 130mm; line-height: 1.5;
  border-top: 2px solid rgba(241,236,221,0.35);
  padding-top: 8mm; margin-top: 4mm;
}
.cover-foot {
  position: absolute; bottom: 20mm; left: 0; right: 0;
  font-size: 10pt; letter-spacing: 2px; text-transform: uppercase; color: rgba(241,236,221,0.7);
}

/* ---------- FLOW PAGES ---------- */
.page-break { page-break-before: always; }

.lead h1 {
  font-size: 26pt; color: var(--petrol); margin-bottom: 6mm; line-height: 1.15;
}
.lead h2 {
  font-size: 18pt; color: var(--orange); margin: 10mm 0 4mm;
}
.lead p { margin-bottom: 4mm; }
.lead .intro-quote {
  background: var(--creme); border-left: 5px solid var(--orange);
  padding: 6mm 7mm; margin: 6mm 0; font-size: 12pt; border-radius: 0 3mm 3mm 0;
}
.lead ol, .lead ul { margin: 0 0 4mm 6mm; }
.lead li { margin-bottom: 2.5mm; }

/* ---------- EXERCISES ---------- */
.exercise { page-break-before: always; }
.exercise h2 { font-size: 22pt; color: var(--petrol); margin-bottom: 3mm; }
.exercise .ex-intro { margin-bottom: 6mm; }
.q { font-weight: 600; margin: 6mm 0 2mm; color: var(--teal); }
.fill-line {
  border-bottom: 1.4px solid #c9c2ad; height: 8mm; margin-bottom: 1mm;
}
.result-box {
  background: var(--creme); border: 2px dashed var(--orange);
  border-radius: 3mm; padding: 6mm; margin-top: 8mm; font-size: 13pt; text-align: center;
}
.result-box .rb-line { display: inline-block; border-bottom: 1.6px solid var(--teal); min-width: 45mm; margin: 0 2mm; }

table.mix { width: 100%; border-collapse: collapse; margin: 6mm 0; }
table.mix th, table.mix td { border: 1px solid #d8d2c0; padding: 3.5mm 4mm; text-align: left; font-size: 10.5pt; }
table.mix th { background: var(--petrol); color: var(--creme); font-family: 'Philosopher', serif; }
table.mix tr:nth-child(even) td { background: #faf8f1; }

/* ---------- CHAPTERS ---------- */
.chapter { page-break-before: always; }
.chapter-divider {
  border-radius: 4mm; padding: 9mm 9mm 8mm; color: #fff; margin-bottom: 7mm;
  page-break-after: avoid;
}
.accent-petrol .chapter-divider { background: var(--petrol); }
.accent-teal   .chapter-divider { background: var(--teal); }
.accent-orange .chapter-divider { background: var(--orange); }
.ch-num { font-size: 11pt; letter-spacing: 3px; text-transform: uppercase; opacity: 0.85; }
.ch-icon { font-size: 22pt; margin: 1mm 0; }
.ch-title { font-size: 24pt; line-height: 1.12; margin-bottom: 2mm; }
.ch-anlass {
  display: inline-block; font-size: 9pt; letter-spacing: 2px; text-transform: uppercase;
  background: rgba(255,255,255,0.22); padding: 1.5mm 4mm; border-radius: 10mm; margin-bottom: 3mm;
}
.ch-sub { font-size: 11pt; font-weight: 300; line-height: 1.5; max-width: 155mm; opacity: 0.97; }

.idea {
  page-break-inside: avoid;
  border-bottom: 1px solid #e7e1d0;
  padding: 5mm 0 5.5mm;
}
.idea:last-child { border-bottom: none; }
.idea-head { display: flex; align-items: baseline; gap: 4mm; margin-bottom: 1.5mm; }
.idea-num {
  flex: 0 0 auto; font-size: 13pt; font-weight: 700; color: #fff;
  width: 9mm; height: 9mm; border-radius: 50%; text-align: center; line-height: 9mm;
}
.accent-petrol .idea-num { background: var(--petrol); }
.accent-teal   .idea-num { background: var(--teal); }
.accent-orange .idea-num { background: var(--orange); }
.idea-title { font-size: 13.5pt; color: var(--teal); line-height: 1.2; }
.idea-prompt { margin: 0 0 2.5mm 13mm; font-size: 10.5pt; }
.idea-ex {
  margin: 0 0 3mm 13mm; background: var(--creme); border-left: 4px solid var(--orange);
  padding: 3mm 4mm; font-size: 10pt; font-style: italic; border-radius: 0 2mm 2mm 0; line-height: 1.45;
}
.idea-ex .ex-label {
  font-style: normal; font-family: 'Philosopher', serif; color: var(--orange);
  font-size: 8.5pt; letter-spacing: 1.5px; text-transform: uppercase; display: block; margin-bottom: 1mm;
}
.idea-fill { margin-left: 13mm; }
.fill-label {
  font-size: 8.5pt; letter-spacing: 1.5px; text-transform: uppercase; color: #a99f83;
  display: block; margin-bottom: 2mm; font-family: 'Philosopher', serif;
}

/* ---------- BONUS / SPEICHER / OUTRO ---------- */
.bonus { page-break-before: always; }
.bonus h2 { font-size: 22pt; color: var(--petrol); margin-bottom: 5mm; }
.step { background: #faf8f1; border-radius: 3mm; padding: 5mm 6mm; margin-bottom: 4mm; border-left: 5px solid var(--petrol); page-break-inside: avoid; }
.step h3 { font-size: 13pt; color: var(--teal); margin-bottom: 1.5mm; }
.golden { background: var(--teal); color: var(--creme); border-radius: 3mm; padding: 6mm 7mm; margin-top: 6mm; font-size: 11.5pt; }
.golden strong { color: var(--orange); }

table.speicher { width: 100%; border-collapse: collapse; margin-top: 5mm; }
table.speicher th, table.speicher td { border: 1px solid #d8d2c0; padding: 4.5mm 4mm; }
table.speicher th { background: var(--petrol); color: var(--creme); font-family: 'Philosopher', serif; text-align: left; font-size: 10.5pt; }
table.speicher .sp-idea { width: 55%; }

.outro { page-break-before: always; text-align: center; padding-top: 30mm; }
.outro h2 { font-size: 26pt; color: var(--petrol); margin-bottom: 8mm; }
.outro p { max-width: 150mm; margin: 0 auto 5mm; font-size: 12pt; }
.outro .big { font-size: 15pt; color: var(--orange); font-family: 'Philosopher', serif; font-style: italic; }

/* ---------- BRIDGE (Von der Story zum Ja) ---------- */
.bridge-steps { counter-reset: bstep; margin: 5mm 0; }
.bridge-step { display: flex; gap: 4mm; margin-bottom: 4mm; page-break-inside: avoid; }
.bridge-badge { flex: 0 0 auto; width: 9mm; height: 9mm; border-radius: 50%; background: var(--teal); color: #fff; font-family: 'Philosopher', serif; font-weight: 700; text-align: center; line-height: 9mm; font-size: 12pt; }
.bridge-step .bs-body { flex: 1; }
.bridge-step h3 { font-size: 12.5pt; color: var(--teal); margin-bottom: 1mm; }
.reveal { background: var(--creme); border-left: 5px solid var(--orange); border-radius: 0 3mm 3mm 0; padding: 6mm 7mm; margin-top: 6mm; font-size: 11.5pt; }
.reveal strong { color: var(--orange); }

/* ---------- NEXT STEPS / OFFERS ---------- */
.next-steps { page-break-before: always; }
.next-steps h2 { font-size: 22pt; color: var(--petrol); margin-bottom: 3mm; }
.next-steps > p { margin-bottom: 6mm; }
.offer-card { border-radius: 4mm; padding: 7mm 7mm 6mm; margin-bottom: 6mm; page-break-inside: avoid; }
.offer-primary { background: var(--petrol); color: var(--creme); }
.offer-far { background: #faf8f1; border: 1.5px solid #d8d2c0; color: var(--ink); }
.offer-tag { display: inline-block; font-size: 8.5pt; letter-spacing: 2px; text-transform: uppercase; font-family: 'Philosopher', serif; padding: 1.5mm 4mm; border-radius: 10mm; margin-bottom: 3mm; }
.offer-primary .offer-tag { background: var(--orange); color: #fff; }
.offer-far .offer-tag { background: var(--petrol); color: var(--creme); }
.offer-card h3 { font-family: 'Philosopher', serif; font-size: 19pt; line-height: 1.15; margin-bottom: 2mm; }
.offer-primary h3 { color: #fff; }
.offer-far h3 { color: var(--teal); }
.offer-price { font-family: 'Philosopher', serif; font-size: 13pt; margin-bottom: 3mm; }
.offer-primary .offer-price { color: #ffe4c4; }
.offer-far .offer-price { color: var(--orange); }
.offer-card p { font-size: 10.8pt; margin-bottom: 3mm; line-height: 1.5; }
.offer-link { font-family: 'Philosopher', serif; font-size: 11pt; word-break: break-all; }
.offer-primary .offer-link { color: #fff; }
.offer-primary .offer-link strong { color: var(--orange); }
.offer-far .offer-link strong { color: var(--petrol); }

/* ---------- BRIDGE KIT ---------- */
.formula { background: var(--teal); color: var(--creme); border-radius: 3mm; padding: 5mm 6mm; margin: 4mm 0 5mm; text-align: center; font-family: 'Philosopher', serif; font-size: 12.5pt; }
.kit-h { font-size: 13.5pt; color: var(--orange); margin: 7mm 0 3mm; font-family: 'Philosopher', serif; }
.bridge-kit { list-style: none; margin: 0 0 4mm; }
.bridge-kit li { background: var(--creme); border-left: 4px solid var(--orange); border-radius: 0 2mm 2mm 0; padding: 3.5mm 5mm; margin-bottom: 2.5mm; font-size: 10.8pt; page-break-inside: avoid; }
.bridge-kit li em { font-style: normal; font-weight: 700; color: var(--teal); }
.bridge-ex { border: 1px solid #e0d9c6; border-radius: 2mm; padding: 4mm 5mm; margin-bottom: 3mm; font-size: 10.5pt; page-break-inside: avoid; line-height: 1.5; }
.bridge-ex strong { color: var(--petrol); }
.bridge-ex em { color: var(--orange); font-style: normal; font-weight: 700; }
.fill-block { margin: 5mm 0; }
</style>
</head>
<body>

<div class="cover">
  <div class="cover-kicker">Dein Ideen-Vorrat für Instagram-Stories</div>
  <h1><span class="cover-num">90</span> Storyideen<br>für Networkerinnen</h1>
  <div class="cover-sub">Sichtbar werden, ohne ständig dein Produkt zu pushen.</div>
  <div class="cover-foot">Workbook zum Ausfüllen</div>
</div>

<div class="lead">
  <h1>Bevor du loslegst — lies das kurz</h1>
  <p>Kennst du das Gefühl, wenn du dich beim Freundinnen-Treffen fast schon entschuldigst, bevor du überhaupt was von deinem Business erzählst? Dieses kurze, betretene Schweigen, weil alle denken „jetzt kommt sie wieder mit ihrem Produkt um die Ecke"? Ich kenne das. Und ich sag dir jetzt mal ganz ehrlich: Genau das ist der Grund, warum so viele Networkerinnen stundenlang posten und trotzdem niemand kauft.</p>
  <div class="intro-quote">Das Problem ist nicht, dass du zu wenig über dein Produkt sprichst. Das Problem ist, dass du <strong>fast nur</strong> darüber sprichst.</div>
  <p>Deine Menschen kaufen nämlich nicht als Erstes dein Produkt. Sie kaufen zuerst dich. Deine Geschichte, dein Warum, das Gefühl, dass du sie verstehst und dass sie dir vertrauen können. Erst dann — irgendwann viel später — interessiert sie, was du eigentlich anbietest.</p>
  <p>Dieses Workbook dreht genau das um. Statt „Was kann ich heute über mein Produkt posten?" fragst du dich ab jetzt: „Über welchen Moment aus meinem Leben, welche Meinung, welchen ehrlichen Gedanken kann ich heute sprechen — sodass die richtigen Menschen sich bei mir wiederfinden?"</p>
  <p>Und keine Sorge: Das heisst nicht, dass du nie wieder verkaufst. Im Gegenteil. Du verkaufst danach besser, weil die Menschen dir dann schon vertrauen. Aber dazu kommen wir ganz am Schluss.</p>

  <h2>So nutzt du dieses Workbook</h2>
  <p>Du musst es nicht von vorne bis hinten durcharbeiten. Nimm es wie einen Vorrat im Schrank.</p>
  <ol>
    <li><strong>Starte mit den zwei Übungen</strong> auf den nächsten Seiten. Sie geben dir das Fundament: dein Thema und den richtigen Mix. Das sind die 20 Minuten, die alles andere leichter machen.</li>
    <li><strong>Dann blättere durch die 90 Ideen.</strong> Sie sind in 8 Anlässe sortiert. Such dir raus, was heute zu dir passt — nicht nach Reihenfolge, sondern nach Bauchgefühl.</li>
    <li><strong>Zu jeder Idee findest du:</strong> den Impuls, ein kurzes Beispiel aus der Network-Welt und eine leere Zeile für deine eigene Version.</li>
    <li><strong>Fülle die leeren Zeilen aus, wann immer dir was einfällt.</strong> So baust du dir mit der Zeit deinen eigenen Ideen-Speicher — und stehst nie wieder morgens vor der Story-Kamera und weisst nicht, was du sagen sollst.</li>
  </ol>
  <p>Ein Tipp noch: Schreib die Ideen so auf, wie du sie einer guten Freundin am Telefon erzählen würdest. Nicht poliert, nicht geschäftlich. Genau das ist es, was am Ende zieht.</p>
</div>

<div class="exercise">
  <h2>Übung 1: Finde dein Thema</h2>
  <p class="ex-intro">Das hier ist die wichtigste Seite im ganzen Workbook. Denn der eigentliche Grund, warum sich Networkerinnen ständig hinter ihrem Produkt verstecken, ist simpel: Sie haben nie festgelegt, <strong>womit sie eigentlich konkret helfen.</strong> Ohne Thema bleibt nur das Produkt zum Reden übrig. Dein Thema ist nicht dein Produkt — es ist das Problem, bei dem du deinen Menschen hilfst, und für das dein Produkt am Ende nur <em>eine</em> Lösung ist.</p>

  <div class="q">1. Was hat dich selbst zu deinem Produkt gebracht? Welches Problem wolltest du lösen?</div>
  ${lines(2)}
  <div class="q">2. Worüber fragen dich Menschen um Rat — auch ohne dass es ums Produkt geht?</div>
  ${lines(2)}
  <div class="q">3. Wenn du einen Nachmittag lang etwas erklären dürftest, das dir leichtfällt und anderen schwer — was wäre das?</div>
  ${lines(2)}
  <div class="q">4. Welche Veränderung sollen die Menschen erleben, die mit dir arbeiten? (Nicht das Produkt — das Ergebnis in ihrem Leben.)</div>
  ${lines(2)}

  <div class="result-box">
    <strong>Jetzt bring es auf einen Satz:</strong><br><br>
    Ich helfe <span class="rb-line"></span> dabei,<br><br>
    <span class="rb-line"></span> zu erreichen.
  </div>
  <p style="margin-top:6mm;">Dieser Satz ist ab jetzt deine Brille. Jede Story-Idee wird stärker, wenn du sie durch diese Brille anschaust.</p>
</div>

<div class="exercise">
  <h2>Übung 2: Der richtige Mix</h2>
  <p class="ex-intro">Gute Stories über eine Woche gedacht bedienen immer drei Anlässe. Wenn einer fehlt, merkt man\'s sofort — dann wirkt dein Kanal entweder wie eine Dauerwerbesendung oder wie ein Tagebuch ohne Punkt.</p>
  <table class="mix">
    <tr><th>Anlass</th><th>Was er bewirkt</th><th>Wie oft</th></tr>
    <tr><td><strong>❤️ Nähe</strong> — du zeigst dich als Mensch</td><td>Menschen fangen an, dir zu vertrauen</td><td>oft</td></tr>
    <tr><td><strong>💡 Mehrwert</strong> — du gibst was zu deinem Thema mit</td><td>Menschen sehen: die weiss, wovon sie spricht</td><td>oft</td></tr>
    <tr><td><strong>📨 Einladung</strong> — du machst dein Angebot sichtbar</td><td>Menschen wissen, dass sie bei dir kaufen können</td><td>dezent, aber regelmässig</td></tr>
  </table>
  <p>Die meisten machen den Fehler, fast nur bei „Einladung" zu hängen — und wundern sich, dass keine Nähe entsteht. Dreh das Verhältnis um: Der grösste Teil deiner Stories baut Nähe und Mehrwert. Die Einladung darf dann selbstverständlich dazwischenliegen, ganz ohne Druck.</p>
  <p>Die 8 Ideen-Kapitel auf den nächsten Seiten sind genau nach diesem Prinzip aufgebaut. Am Symbol erkennst du, welchen Anlass ein Kapitel bedient: <strong>❤️ Nähe · 💡 Mehrwert · 📨 Einladung</strong>.</p>
</div>

<div class="exercise">
  <h2>Dein Story-Kompass — wann nimmst du welche Idee?</h2>
  <p class="ex-intro">90 Ideen sind viel — damit du morgens nicht ratlos davorstehst, hier zwei einfache Wegweiser. Der erste beantwortet „welche Idee heute?", der zweite „wie verteile ich das über die Woche?".</p>

  <h3 class="kit-h">1. Welche Idee passt zu heute?</h3>
  <p>Schau, wie dein Tag oder deine Stimmung gerade ist — und greif ins passende Kapitel.</p>
  <table class="mix">
    <tr><th>Wenn du heute …</th><th>… dann nimm eine Idee aus</th></tr>
    <tr><td>einen Moment erlebt hast (Kind, Kaffee, Chaos, ein Foto)</td><td>Kapitel 1 · 6 — Alltag &amp; hinter den Kulissen</td></tr>
    <tr><td>Lust hast, etwas beizubringen</td><td>Kapitel 3 — Mehrwert zu deinem Thema</td></tr>
    <tr><td>eine Meinung loswerden willst</td><td>Kapitel 4 — Haltung</td></tr>
    <tr><td>Reichweite &amp; Reaktionen willst</td><td>Kapitel 5 — Fragen &amp; Umfragen</td></tr>
    <tr><td>über dich &amp; deinen Weg erzählen magst</td><td>Kapitel 2 — deine Geschichte</td></tr>
    <tr><td>gerade ein Angebot oder freie Plätze hast</td><td>Kapitel 7 — die Einladung (+ Brücke)</td></tr>
    <tr><td>platt bist und kaum Zeit hast</td><td>Kapitel 8 — die kleinen Extras (1 Slide)</td></tr>
  </table>

  <h3 class="kit-h">2. Wie verteilst du das über die Woche?</h3>
  <p>Die wichtigste Regel: <strong>Das Verhältnis muss über die Woche stimmen, nicht an einem einzelnen Tag.</strong> Du musst nicht jeden Tag alles abdecken. Grob als Faustregel: viel Nähe, ordentlich Mehrwert, dazwischen ab und zu eine Einladung mit Brücke. So ein Rhythmus könnte aussehen:</p>
  <table class="mix">
    <tr><th>Tag</th><th>Anlass</th><th>Woraus?</th></tr>
    <tr><td>Montag</td><td>💡 Mehrwert (+ Brücke zum Freebie)</td><td>Kapitel 3</td></tr>
    <tr><td>Dienstag</td><td>❤️ Nähe</td><td>Kapitel 1</td></tr>
    <tr><td>Mittwoch</td><td>❤️ Verbindung</td><td>Kapitel 5</td></tr>
    <tr><td>Donnerstag</td><td>💡 Haltung</td><td>Kapitel 4</td></tr>
    <tr><td>Freitag</td><td>❤️ Hinter den Kulissen (+ evtl. Einladung)</td><td>Kapitel 6 · 7</td></tr>
    <tr><td>Wochenende</td><td>❤️ Persönlich / kleine Extras</td><td>Kapitel 2 · 8</td></tr>
  </table>
  <p>Nimm das als Startpunkt, nicht als Gesetz. Sobald du ein Gefühl dafür hast, machst du deinen eigenen Rhythmus daraus.</p>
</div>

${chapters.map(renderChapter).join('')}

<div class="bonus">
  <h2>Bonus: So wird aus einer Idee eine Story, die verkauft</h2>
  <p>Eine Idee ist der Anfang. Damit daraus eine Story wird, die wirklich etwas bewirkt, hilft dieser einfache Vierklang. Du musst ihn nicht bei jeder Story anwenden — aber je öfter, desto besser.</p>
  <div class="step"><h3>1. Hook — der erste Satz, der stoppt.</h3>Fang mit dem an, was dein Gegenüber gerade fühlt, nicht mit „Guten Morgen". Ein Gedanke, ein Schmerz, eine Frage.</div>
  <div class="step"><h3>2. Mittelteil — der echte Inhalt.</h3>Erzähl deine Geschichte, gib deinen Tipp, teile deinen Gedanken. Hier lebst du deinen Anlass aus (Nähe, Mehrwert oder Haltung).</div>
  <div class="step"><h3>3. Brücke — der Bezug zu deinem Thema.</h3>Verbinde das Erzählte mit dem, wofür du stehst. Ganz ohne Produkt: „Genau darum geht es mir." / „Das ist es, was ich meinen Menschen mitgeben will."</div>
  <div class="step"><h3>4. Nächster Schritt — eine klare Handlung.</h3>Was soll dein Gegenüber jetzt tun? Antworten, abstimmen, dir schreiben, mitmachen. Immer nur eine Sache.</div>
  <div class="golden"><strong>Die goldene Regel:</strong> Auf jede Einladung kommen mehrere Stories mit Nähe und Mehrwert. Wer nur einlädt, wirkt wie eine Dauerwerbesendung. Wer nie einlädt, wird nie gebucht. Der Mix macht\'s.</div>
</div>

<div class="bonus">
  <h2>Die Story-Brücke — so verkaufst du nebenbei aus jeder Story</h2>
  <p>Jetzt kommt der Trick, den die Frauen draufhaben, die mit Stories verkaufen, ohne dass es jemanden nervt: Sie erzählen eine ganz normale Story — irgendeine aus diesem Workbook — und hängen am Schluss eine kleine Brücke dran. Einen Satz, der überleitet, und einen klaren nächsten Schritt. Nicht bei jeder Story, aber bei den meisten. So wird aus „nur erzählen" ganz natürlich „nebenbei verkaufen".</p>

  <div class="formula">Deine Story &nbsp;→&nbsp; ein Brückensatz &nbsp;→&nbsp; ein klarer nächster Schritt (mit Link oder Keyword)</div>

  <p>Und wohin führt die Brücke? Am liebsten <strong>zu deinem kostenlosen Freebie</strong>. Warum nicht gleich zum Produkt? Weil „gratis" die kleinste Hürde ist — dein Gegenüber sagt viel eher Ja, du gewinnst einen Kontakt, und das Vertrauen wächst weiter, bis irgendwann von allein gekauft wird. Ein Freebie ist deine sanfteste Brücke. Hast du noch keins, führt die Brücke eben zu einem Gespräch in den DMs — auch das funktioniert.</p>

  <h3 class="kit-h">Dein Brücken-Baukasten — zum Freebie</h3>
  <ul class="bridge-kit">
    <li>„Falls du das kennst — ich hab dir genau dazu was gemacht. Kommentier <em>[WORT]</em> und ich schick's dir."</li>
    <li>„Genau darum geht's in meinem kostenlosen <em>[Freebie]</em>. Der Link ist in meiner Bio."</li>
    <li>„Wenn du da grad auch stehst: Ich hab was, das dir den ersten Schritt abnimmt. Schreib mir <em>[WORT]</em>."</li>
    <li>„Das ist übrigens der Grund, warum ich <em>[Freebie]</em> gemacht habe. Hol's dir gratis über den Link in meiner Bio."</li>
  </ul>

  <h3 class="kit-h">… und wenn die Story warm genug ist — zum Angebot</h3>
  <ul class="bridge-kit">
    <li>„Wenn du das wirklich angehen willst, begleite ich genau dabei. Schreib mir <em>[WORT]</em>, dann erzähl ich dir mehr."</li>
    <li>„Genau dafür gibt's <em>[dein Angebot]</em>. Alle Infos über den Link in meiner Bio."</li>
  </ul>

  <div class="fill-block">
    <span class="fill-label">Meine Brücke zu meinem Freebie</span>
    ${lines(2)}
  </div>

  <h3 class="kit-h">So sieht das in echt aus</h3>
  <div class="bridge-ex"><strong>Story „Ein ganz normaler Morgen":</strong> du erzählst von deiner ruhigen halben Stunde mit Kaffee am Küchentisch. <em>Brücke:</em> „Diese Ruhe am Morgen ist Gold wert. Wenn du auch mehr davon in deinen Tag willst — kommentier RUHE, ich schick dir meine kostenlose Mini-Anleitung."</div>
  <div class="bridge-ex"><strong>Story „Der grösste Fehler, den ich sehe":</strong> du erzählst den typischen Fehler bei deinem Thema. <em>Brücke:</em> „Genau diesen Fehler nehm ich dir in meinem Gratis-Guide ab. Der Link ist in meiner Bio."</div>
  <div class="bridge-ex"><strong>Story „Womit du gerade kämpfst":</strong> du zeigst dich ehrlich mit einer Herausforderung. <em>Brücke zum Gespräch:</em> „Wenn's dir grad ähnlich geht — schreib mir einfach. Manchmal hilft schon ein ehrliches Gespräch."</div>

  <div class="reveal">Wichtig bleibt nur eins: <strong>nicht bei jeder einzelnen Story</strong> die Brücke — sonst wird's zur Dauerwerbung. Ein paar Stories dürfen einfach nur Nähe sein. Aber trau dich, öfter die Brücke zu bauen, als du denkst. Solange sie aus einer echten Geschichte kommt und zu etwas Kostenlosem führt, nervt sie niemanden — im Gegenteil, sie hilft.</div>
</div>

<div class="bonus">
  <h2>Dein Ideen-Speicher</h2>
  <p>Immer, wenn dir zwischendurch eine Idee kommt — im Auto, unter der Dusche, beim Kochen — schreib sie hier rein. So gehst du nie wieder leer in den Tag.</p>
  <table class="speicher">
    <tr><th class="sp-idea">Idee</th><th>Anlass (❤️/💡/📨)</th><th>Wann posten?</th></tr>
    ${speicherRows}
  </table>
</div>

<div class="next-steps">
  <h2>Wie es jetzt weitergeht</h2>
  <p>Du hast jetzt einen Vorrat an Ideen, der dir nie wieder ausgeht. Aber Ideen allein bringen noch keine Kundinnen. Wenn du wirklich sichtbar werden und aus deinen Stories echte Anfragen machen willst, hab ich zwei Wege für dich — je nachdem, wie weit du gehen willst.</p>

  <div class="offer-card offer-primary">
    <span class="offer-tag">Wenn du's wirklich willst</span>
    <h3>Die Instagram-Kundenmaschine</h3>
    <div class="offer-price">333 CHF</div>
    <p>Hier lernst du das komplette System, mit dem aus Followern echte Kundinnen werden: dein glasklares Thema, deine Positionierung, deine Instagram-Strategie und dein eigenes Freebie, das dir wie von selbst Kontakte bringt. Kein Rätselraten mehr, warum niemand kauft — sondern ein Weg, den du Schritt für Schritt gehst. Genau das, worauf dieses Workbook Lust gemacht hat, in voller Tiefe.</p>
    <div class="offer-link">👉 <strong>mumlifebalance.thrivecart.com/instagram-kundenmaschine</strong></div>
  </div>

  <div class="offer-card offer-far">
    <span class="offer-tag">Der sanfte Einstieg · 39 CHF</span>
    <h3>Finde dein Thema als Network-Mama</h3>
    <p>Noch nicht bereit für den ganzen Weg? Dann starte mit dem ersten Baustein. Übung 1 hat den Funken gezündet — hier machst du daraus dein glasklares Thema, mit dem du dich abhebst. Klein anfangen ist auch anfangen.</p>
    <div class="offer-link">👉 <strong>mumlifebalance.thrivecart.com/thema-finden</strong></div>
  </div>
</div>

<div class="outro">
  <h2>Zum Schluss</h2>
  <p>Wenn du nur eine Sache aus diesem Workbook mitnimmst, dann diese: <strong>Menschen folgen und kaufen nicht wegen deines Produkts. Sie folgen und kaufen wegen dir.</strong> Wegen deiner Geschichte, deiner Haltung, dem Gefühl, dass du sie verstehst.</p>
  <p>Hör auf, dich hinter deinem Produkt zu verstecken. Zeig dich. Sprich über dein Thema, über dein Leben, über das, was dir wichtig ist. Die richtigen Menschen werden dich finden — und irgendwann fragen sie ganz von allein: „Was machst du eigentlich genau, und kann ich das auch haben?"</p>
  <p class="big">Genau dann hast du gewonnen.</p>
  <p>Du schaffst das. Und jetzt: leg los. 💛</p>
</div>

</body>
</html>`;

// ---------------------------------------------------------------------------
// BUILD
// ---------------------------------------------------------------------------
async function main() {
  await fs.mkdir(OUT_DIR, { recursive: true });
  await fs.writeFile(HTML_PATH, html, 'utf-8');
  console.log(`HTML geschrieben (${counter} Ideen) -> ${path.relative(REPO_ROOT, HTML_PATH)}`);

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none'],
  });
  try {
    const page = await browser.newPage();
    await page.goto('file://' + HTML_PATH, { waitUntil: 'networkidle0', timeout: 90000 });
    await page.evaluate(() => document.fonts.ready);
    await new Promise((r) => setTimeout(r, 1500));
    await page.pdf({
      path: PDF_PATH,
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
    });
    const stat = await fs.stat(PDF_PATH);
    console.log(`✓ PDF: ${path.relative(REPO_ROOT, PDF_PATH)} (${(stat.size / 1024).toFixed(0)} KB)`);
  } finally {
    await browser.close();
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
