// Startklar — Modul 2 „Du kannst posten". Inhalte 1:1 aus 03-canva-briefing/modul-02.md.
import { deck } from "./folien-lib.mjs";
const d = deck();

d.modultitel({ kicker:"STARTKLAR · MODUL 2", title:"Du kannst posten", sub:"5 Lektionen · rund 46 Minuten",
  note:"Ziel: Am Ende hat sie ein Reel, ein Karussell und eine Story hochgeladen — echt auf ihrem Profil. Abgrenzung: hier geht es um BEDIENUNG, nicht um Strategie. Was sie inhaltlich sagt, gehört in die Instagram-Kundenmaschine." });

// L2.1
d.titel({ num:"2.1", lekt:"2.1", title:"Die drei Sorten Beitrag — in normaler Sprache",
  note:"Bevor wir irgendwas hochladen, sortieren wir kurz. Wenn du weisst, wofür welches Format da ist, hörst du auf, dich zu fragen, ob du das jetzt als Story oder als Beitrag machen sollst." });
d.lernen({ items:["Was ein Reel von einem normalen Beitrag unterscheidet","Warum Stories nach 24 Stunden weg sind und das ein Vorteil ist","Wo dein Beitrag landet, wenn dich noch niemand kennt"] });
d.inhalt({ header:"Die drei Formate", items:[
  {label:"Reel", text:"kurzes Video. Wird auch Leuten gezeigt, die dir nicht folgen. Dein Weg zu neuen Menschen."},
  {label:"Beitrag / Karussell", text:"Bilder zum Durchwischen. Bleiben auf deinem Profil stehen. Dein Beweis, dass du etwas kannst."},
  {label:"Story", text:"verschwindet nach 24 Stunden. Sehen fast nur Leute, die dir folgen. Dein Gespräch mit denen, die schon da sind."}],
  note:"Merk dir das so: Reels holen neue Leute rein. Beiträge überzeugen die, die dich gerade entdeckt haben. Stories machen aus Zuschauerinnen Kundinnen. Alle drei brauchst du, aber in dieser Reihenfolge." });
d.inhalt({ header:"Was das für dich heisst", items:[
  {text:"Wenn dich noch niemand kennt, sind Reels dein Hebel."},
  {text:"Wenn dich jemand kennt, entscheiden deine Stories."}],
  note:"Das ist auch der Grund, warum wir gleich mit dem Reel anfangen und nicht mit dem schönen Karussell, an dem du zwei Stunden basteln könntest." });
d.ausblick({ text:"Jetzt dein erstes Reel. Wir nehmen es zusammen auf." });

// L2.2
d.titel({ num:"2.2", lekt:"2.2", title:"Dein erstes Reel — und ja, du bist drauf",
  note:"Das ist der Punkt, an dem die meisten aussteigen. Also machen wir es so einfach wie irgend möglich. Du sagst einen Satz in die Kamera. Mehr nicht." });
d.lernen({ items:["Aufnehmen direkt in Instagram oder vorher mit der Handykamera","Text auf dein Video legen","Cover, Titel, hochladen"] });
d.zitat({ header:"Dein Übungs-Reel", quote:"„Ich bin [Name] und ich zeig dir hier, wie du als Mama zu mehr [dein Thema] kommst.“",
  sub:"Sieben Sekunden Video, ein Satz — entschieden wird in den ersten zwei bis dreien. Das ist kein Meisterwerk. Das ist dein erster Klick.",
  note:"Nimm es einmal auf. Wenn es dir nicht gefällt, nimmst du es ein zweites Mal auf. Nach dem dritten Mal wird es nicht mehr besser, es wird nur steifer." });
d.handy({ sub:"Reel aufnehmen und hochladen", steps:[
  "Plus-Symbol oben rechts → „Reel“",
  "Direkt in der App aufnehmen — oder mit der Handykamera aufnehmen und aus der Galerie hochladen (entspannter)",
  "Text hinzufügen: Schriftart, Grösse, Dauer einstellen",
  "Musik dazulegen und leise stellen, damit die Stimme vorne bleibt",
  "Cover wählen — Standbild aus dem Video oder Bild aus der Galerie",
  "Beschreibung tippen, „Teilen“ — danach zeigen, wo das Reel auf dem Profil landet"],
  note:"Beim Text achte darauf, dass er nicht ganz unten sitzt. Da liegt bei vielen Handys die Beschriftung drüber und dann liest ihn keiner." });
d.inhalt({ header:"Der Fehler, der Reichweite kostet", items:[
  {text:"Reel gelöscht und neu hochgeladen, weil ein Tippfehler drin war? Instagram fängt bei null an."},
  {label:"Merke:", text:"Der Text unter dem Video lässt sich nachträglich ändern — das Video selbst nicht."}],
  note:"Also lieber einen Tippfehler stehen lassen als löschen und neu hochladen. Kein Mensch ausser dir sieht den Tippfehler. Die Reichweite siehst du dagegen sofort." });
d.aufgabe({ text:"Ein Reel ist online. Deinen ersten Satz vorher durch die Werkstatt.", station:"Reel-Hook" });
d.ausblick({ text:"Als Nächstes: dein erstes Karussell, von Canva bis auf dein Profil." });

// L2.3
d.titel({ num:"2.3", lekt:"2.3", title:"Karussell bauen, ohne Designerin zu sein",
  note:"Ein Karussell sind mehrere Bilder, die man durchwischt. Klingt aufwendig, ist es nicht, sobald du einmal eine Vorlage hast." });
d.lernen({ items:["Das richtige Format in Canva anlegen","Sechs Folien in zwanzig Minuten","Als Bilder exportieren und hochladen"] });
d.inhalt({ header:"Die Karussell-Grundform", items:[
  {label:"Folie 1:", text:"eine Aussage, die hängen bleibt"},
  {label:"Folie 2–5:", text:"je ein Gedanke pro Folie"},
  {label:"Folie 6:", text:"was sie jetzt tun soll"}],
  foot:"Höchstens zehn Folien. Instagram lässt mehr zu, aber gelesen wird das nicht.",
  note:"Ein Gedanke pro Folie. Wenn du merkst, du schreibst einen zweiten Satz drauf, mach eine neue Folie draus. Und wenn es dann mehr als zehn sind, hast du zwei Karussells statt einem." });
d.handy({ sub:"Canva (am PC) bauen → aufs Handy → hochladen", steps:[
  "Canva öffnen, „Benutzerdefinierte Grösse“ → 1080 × 1350",
  "Hintergrundfarbe setzen, Schrift wählen, erste Folie tippen",
  "Folie duplizieren statt neu bauen — das ist der ganze Trick",
  "Herunterladen als PNG, alle Seiten",
  "Bilder aufs Handy bringen (Canva-App oder Cloud) — Dateinamen geben die Reihenfolge vor",
  "Instagram → Plus → Beitrag → „Mehrere auswählen“ → in der richtigen Reihenfolge antippen",
  "Hochladen, Ergebnis anschauen"],
  note:"Das Antippen bestimmt die Reihenfolge, nicht die Dateiliste. Wenn du falsch tippst, wischt sich dein Karussell rückwärts. Passiert jeder einmal." });
d.aufgabe({ text:"Ein Karussell ist online. Die Folien vorher durch die Werkstatt.", station:"Karussell" });
d.ausblick({ text:"Jetzt die Story — das Format, in dem später verkauft wird." });

// L2.4
d.titel({ num:"2.4", lekt:"2.4", title:"Stories: das Format, in dem später deine Kundinnen entstehen",
  note:"Stories sind ungeschminkt und verschwinden wieder. Genau deshalb sind sie am einfachsten. Du musst hier nichts abliefern." });
d.lernen({ items:["Text, Sticker, Umfrage","Wie du einen Link in die Story bekommst","Warum Umfragen dir mehr bringen als schöne Bilder"] });
d.inhalt({ header:"Die vier Sticker, die reichen", items:[
  {label:"Umfrage", text:"zwei Antworten, ein Tipp genügt"},
  {label:"Frage-Box", text:"sie schreibt dir"},
  {label:"Quiz", text:"sie rät, du löst auf"},
  {label:"Link", text:"sie kommt auf deine Seite"}],
  note:"Jeder Tipp auf einen Sticker ist ein Signal an Instagram, dass deine Story interessant war. Und jede Antwort in der Frage-Box ist ein Gespräch, das du sonst nie gehabt hättest." });
d.handy({ sub:"Story posten mit Text, Umfrage und Link", steps:[
  "Plus → „Story“ oder von oben links am Profilbild",
  "Foto aus der Galerie, Text drauf, Farbe und Hintergrund zeigen",
  "Sticker-Symbol → Umfrage einbauen",
  "Link-Sticker einbauen und den Linktext ändern",
  "Posten, dann die eigene Story anschauen",
  "Zeigen, wo man sieht, wer die Story gesehen und wer abgestimmt hat"],
  note:"Schau dir immer an, wer abgestimmt hat. Das sind die Menschen, die dich schon interessant finden. Die schreibst du später an, wenn du soweit bist." });
d.aufgabe({ text:"Eine Story mit Umfrage ist gepostet. Die Frage vorher durch die Werkstatt.", station:"Story" });
d.ausblick({ text:"Zum Abschluss von Modul 2 räumen wir auf: Caption, Hashtags, Musik, Cover." });

// L2.5
d.titel({ num:"2.5", lekt:"2.5", title:"Was zählt und was du getrost weglassen kannst",
  note:"Hier räumen wir mit ein paar Sachen auf, an denen du sonst Stunden verlierst. Ich sag dir für jede einzelne, wie viel Aufmerksamkeit sie verdient." });
d.lernen({ items:["Wie viel Text unter dein Bild gehört","Wie viele Hashtags heute noch etwas bringen","Wann Musik hilft und wann sie stört"] });
d.inhalt({ header:"Die Rangliste", items:[
  {num:true, text:"Der erste Satz unter dem Beitrag — hier fällt die Entscheidung"},
  {num:true, text:"Das Cover deines Reels — dein Profil ist eine Auslage"},
  {num:true, text:"Musik — nur als Untermalung, nie über deiner Stimme"},
  {num:true, text:"Hashtags — höchstens fünf, thematisch, ganz am Ende"}],
  note:"Hashtags waren vor Jahren mal ein Hebel. Heute sind sie eine Einordnung und kein Wachstums-Motor. Fünf reichen. Nimm die, die dein Thema beschreiben, und nicht die, die am grössten sind." });
d.inhalt({ header:"Der erste Satz", items:[
  {text:"Nur die ersten ein bis zwei Zeilen werden angezeigt. Alles danach liest nur, wer auf „mehr“ tippt."}],
  note:"Dein wichtigster Satz gehört ganz nach oben. Instinktiv schreibst du ihn ans Ende, und da liest ihn keiner. Fang nie mit „Guten Morgen ihr Lieben“ an. Das kostet dich deine besten zwei Zeilen." });
d.abschluss({ kicker:"MODUL 2 · ABGESCHLOSSEN", title:"Du hast gepostet.", text:"Reel, Karussell, Story — alles drei erledigt. Vor einer Woche wusstest du nicht, wo du drücken sollst.", station:"Caption",
  note:"Wie geil ist das denn. Vor einer Woche wusstest du nicht, wo du drücken sollst, und jetzt sind drei Sachen von dir online. Das war der schwerste Teil." });
d.ausblick({ text:"Modul 3: die fünf Fallen, die du als Networkerin vermeidest — und dein Plan für Woche eins." });

await d.pres.writeFile({ fileName:"outputs/produkte/instagram-startklar/06-praesentation/startklar-modul-2.pptx" });
console.log("OK Modul 2");
