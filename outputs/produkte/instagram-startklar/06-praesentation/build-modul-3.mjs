// Startklar — Modul 3 „Sauber starten". Inhalte 1:1 aus 03-canva-briefing/modul-03.md.
import { deck } from "./folien-lib.mjs";
const d = deck();

d.modultitel({ kicker:"STARTKLAR · MODUL 3", title:"Sauber starten", sub:"2 Lektionen · rund 17 Minuten",
  note:"Ziel: Sie kennt die fünf Fehler, die Networkerinnen auf Instagram teuer zu stehen kommen, und hat ihre ersten fünf Beiträge geplant. Abgrenzung: Routine, Statistiken lesen und DM-Gespräche sind bewusst NICHT drin — die gehören in die Instagram-Kundenmaschine." });

// L3.1
d.titel({ num:"3.1", lekt:"3.1", title:"Fünf Sachen, die du als Networkerin bleiben lässt",
  note:"Diese fünf Punkte hab ich in meinem ersten Network alle selber gemacht. Drei Jahre lang. Es hat nicht funktioniert, und ich hab aufgehört. Deshalb erzähl ich dir das jetzt, bevor du dieselbe Runde drehst." });
d.lernen({ items:["Was nicht in deine Bio gehört","Warum Preise im Beitrag dich Anfragen kosten","Wo bei deiner Firma die Regeln stehen"] });
d.inhalt({ header:"Die fünf Fallen", items:[
  {num:true, text:"Firmenname in Bio und Username — dann bist du eine von tausend"},
  {num:true, text:"Produktbilder als Hauptinhalt — du wirst zum Katalog"},
  {num:true, text:"Preise und Bestellinfos im Beitrag — das Gespräch fällt weg, das dich verkaufen lässt"},
  {num:true, text:"Fremde ungefragt anschreiben — inzwischen auch technisch kaum noch möglich"},
  {num:true, text:"Aussagen über Wirkung und Verdienst — bei jeder Firma ein Regelverstoss"}],
  note:"Punkt fünf ist der, der Konten kostet. Was du über Produkte und über Einkommen sagen darfst, steht bei deiner Firma in den Richtlinien. Lies sie einmal. Es dauert zwanzig Minuten und erspart dir viel." });
d.inhalt({ header:"Was du stattdessen tust", items:[
  {text:"Dein Thema steht vorne. Das Produkt kommt später und im Gespräch."},
  {label:"Weil:", text:"Menschen folgen dir wegen dem, was du löst."}],
  note:"Meine Kundinnen kaufen nicht das Produkt. Sie kaufen die Frau, die abends wieder schläft. Das Produkt ist nur das Werkzeug dazu." });
d.aufgabe({ text:"Prüf dein Profil gegen die fünf Punkte.", station:"Network-Fallen" });
d.ausblick({ text:"Letzte Lektion: dein Plan für die erste eigene Woche." });

// L3.2
d.titel({ num:"3.2", lekt:"3.2", title:"Deine ersten fünf Beiträge — heute geplant, diese Woche gepostet",
  note:"Du hast jetzt alles, was du brauchst. Damit du nicht am Montag vor dem leeren Handy sitzt, planen wir die erste Woche jetzt gemeinsam durch." });
d.lernen({ items:["Die fünf Beiträge, mit denen jede anfängt","An welchen Tagen du postest","Wie du vorproduzierst, wenn du Zeit hast"] });
d.inhalt({ header:"Deine fünf Startbeiträge", items:[
  {num:true, text:"Wer bist du — Reel, sieben Sekunden, dein Gesicht"},
  {num:true, text:"Warum dieses Thema — dein Wendepunkt, ehrlich und kurz"},
  {num:true, text:"Ein Tipp, der sofort hilft — Karussell mit fünf Folien"},
  {num:true, text:"Ein Blick in deinen Alltag — Reel, ungeschminkt"},
  {num:true, text:"Wobei du hilfst — Karussell, mit einer Einladung zum Schreiben"}],
  note:"Beitrag zwei ist der, vor dem du dich drücken wirst. Er ist auch der, der am meisten bringt. Menschen bleiben wegen deiner Geschichte, nicht wegen deiner Tipps." });
d.inhalt({ header:"Der Wochenplan", items:[
  {label:"Mo · Mi · Fr:", text:"ein Beitrag"},
  {label:"Di · Do:", text:"eine Story mit Umfrage"},
  {label:"Wochenende:", text:"frei. Wirklich frei."}],
  note:"Fünf Beiträge in der Woche musst du nicht schaffen. Drei reichen völlig, wenn sie regelmässig kommen. Und am Wochenende ist Pause, weil du sonst in vier Wochen aufhörst." });
d.inhalt({ header:"Vorproduzieren", items:[
  {text:"Wenn du zwei ruhige Stunden hast: nimm alle Reels der Woche hintereinander auf. Ein Outfit, ein Licht, fünf Videos."}],
  note:"Ich mach das montags in dreissig Minuten für die ganze Woche. Einmal anziehen, einmal Haare machen, dann alles hintereinander weg. Das ist der einzige Trick, mit dem das neben Kindern funktioniert." });
d.abschluss({ kicker:"KURS ABGESCHLOSSEN", title:"Geschafft.", text:"Dein Profil steht, du kannst posten und du hast einen Plan für die nächste Woche. Das war der schwerste Teil, und er ist erledigt.", station:"Startplan",
  note:"Und jetzt mal ganz ehrlich: du hast in einer Woche mehr gemacht als die meisten in einem halben Jahr. Du bist nicht schneller als die anderen. Du hast angefangen. Der Rest ist Wiederholung." });
d.inhalt({ header:"Wie es weitergeht", items:[
  {label:"Ideen fehlen?", text:"Das liegt an deinem Thema. Dafür: „Finde dein Thema als Network-Mama in 60 Minuten“."},
  {label:"Kundinnen gewinnen?", text:"Dann ist die Instagram-Kundenmaschine dein nächster Schritt."}],
  note:"Was ich dir hier bewusst nicht gezeigt hab: wie du dranbleibst, welche Zahlen du liest und wie aus einem Kommentar ein Gespräch wird, das in einem Kauf endet. Das steckt in der Instagram-Kundenmaschine. Aber erst mal: poste vier Wochen. Kein Druck." });

await d.pres.writeFile({ fileName:"outputs/produkte/instagram-startklar/06-praesentation/startklar-modul-3.pptx" });
console.log("OK Modul 3");
