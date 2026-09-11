// Startklar — Lektions-Folien Modul 1 ("Dein Profil steht")
// Inhalte 1:1 aus 03-canva-briefing/modul-01.md. Sprechnotizen -> Notizen-Ansicht.
import pptxgen from "pptxgenjs";

const P = { petrol:"2F6F6F", blau:"1E3A4C", orange:"D6832F", creme:"F1ECDD",
            text:"33413F", weiss:"FFFFFF", muted:"7A8B88", tint:"EAF1F0", cremetint:"F7F3E8" };
const HEAD = "Cambria", BODY = "Calibri";
const W = 13.3, H = 7.5, MX = 0.75;

const pres = new pptxgen();
pres.defineLayout({ name:"MLB", width:W, height:H });
pres.layout = "MLB";

const notes = (s,t)=>{ if(t) s.addNotes(t); };

// kleines Telefon-Icon (zuverlaessig, kein Emoji)
function phoneIcon(s, x, y, h, col){
  const w = h*0.52;
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius:0.06, fill:{color:col}, line:{type:"none"} });
  s.addShape(pres.ShapeType.roundRect, { x:x+w*0.12, y:y+h*0.13, w:w*0.76, h:h*0.62, rectRadius:0.02, fill:{color:P.weiss}, line:{type:"none"} });
  s.addShape(pres.ShapeType.ellipse, { x:x+w*0.42, y:y+h*0.83, w:w*0.16, h:w*0.16, fill:{color:P.weiss}, line:{type:"none"} });
}
function chip(s, x, y, txt, fill, tcol, w){
  s.addText(txt, { x, y, w:w||2.4, h:0.42, isTextBox:true, shape:pres.ShapeType.roundRect, rectRadius:0.09,
    fill:{color:fill}, color:tcol, fontFace:BODY, fontSize:12, bold:true, align:"center", valign:"middle", charSpacing:2, margin:0 });
}

// ---------- Slide-Typen ----------
function modultitel(d){
  const s = pres.addSlide(); s.background = { color:P.blau };
  s.addText(d.kicker, { x:MX, y:2.2, w:W-2*MX, h:0.5, isTextBox:true, color:P.orange, fontFace:BODY, fontSize:16, bold:true, charSpacing:4 });
  s.addText(d.title, { x:MX, y:2.7, w:W-2*MX, h:1.5, isTextBox:true, color:P.weiss, fontFace:HEAD, fontSize:54, bold:true });
  s.addText(d.sub, { x:MX, y:4.25, w:W-2*MX, h:0.6, isTextBox:true, color:P.creme, fontFace:BODY, fontSize:20, italic:true });
  notes(s,d.note); return s;
}
function titel(d){
  const s = pres.addSlide(); s.background = { color:P.weiss };
  s.addText(d.num, { x:9.2, y:0.4, w:3.6, h:3.2, isTextBox:true, color:P.tint, fontFace:HEAD, fontSize:200, bold:true, align:"right", valign:"top", margin:0 });
  chip(s, MX, 0.85, "LEKTION "+d.lekt, P.petrol, P.weiss, 2.1);
  s.addText(d.title, { x:MX, y:1.7, w:8.6, h:2.6, isTextBox:true, color:P.blau, fontFace:HEAD, fontSize:38, bold:true, valign:"top" });
  if(d.sub) s.addText(d.sub, { x:MX, y:4.5, w:9.2, h:1.6, isTextBox:true, color:P.muted, fontFace:BODY, fontSize:19, italic:true, valign:"top" });
  notes(s,d.note); return s;
}
function lernen(d){
  const s = pres.addSlide(); s.background = { color:P.weiss };
  s.addText("WAS DU LERNEN WIRST", { x:MX, y:0.75, w:W-2*MX, h:0.5, isTextBox:true, color:P.petrol, fontFace:BODY, fontSize:16, bold:true, charSpacing:3 });
  let y = 2.0;
  d.items.forEach((t,i)=>{
    s.addShape(pres.ShapeType.ellipse, { x:MX, y:y, w:0.62, h:0.62, fill:{color:P.orange}, line:{type:"none"} });
    s.addText(String(i+1), { x:MX, y:y, w:0.62, h:0.62, isTextBox:true, color:P.weiss, fontFace:HEAD, fontSize:22, bold:true, align:"center", valign:"middle", margin:0 });
    s.addText(t, { x:MX+0.95, y:y-0.05, w:W-2*MX-1.1, h:0.9, isTextBox:true, color:P.text, fontFace:BODY, fontSize:20, valign:"middle" });
    y += 1.25;
  });
  notes(s,d.note); return s;
}
function inhalt(d){
  const s = pres.addSlide(); s.background = { color:P.weiss };
  s.addText(d.header.toUpperCase(), { x:MX, y:0.75, w:W-2*MX, h:0.5, isTextBox:true, color:P.petrol, fontFace:BODY, fontSize:16, bold:true, charSpacing:3 });
  if(d.title) s.addText(d.title, { x:MX, y:1.3, w:W-2*MX, h:1.0, isTextBox:true, color:P.blau, fontFace:HEAD, fontSize:34, bold:true });
  let y = d.title ? 2.6 : 1.9;
  d.items.forEach((it,i)=>{
    if(it.num){
      s.addShape(pres.ShapeType.ellipse, { x:MX, y:y, w:0.55, h:0.55, fill:{color:P.petrol}, line:{type:"none"} });
      s.addText(String(i+1), { x:MX, y:y, w:0.55, h:0.55, isTextBox:true, color:P.weiss, fontFace:HEAD, fontSize:20, bold:true, align:"center", valign:"middle", margin:0 });
    }
    const tx = it.num ? MX+0.9 : MX;
    const runs = [];
    if(it.label) runs.push({ text:it.label+"  ", options:{ bold:true, color:P.orange } });
    if(it.text) runs.push({ text:it.text, options:{ color:P.text } });
    s.addText(runs, { x:tx, y:y-0.05, w:W-tx-MX, h:it.big?1.2:0.85, isTextBox:true, fontFace:BODY, fontSize:it.big?22:19, valign:"middle" });
    y += it.big?1.35:1.0;
  });
  if(d.foot) s.addText(d.foot, { x:MX, y:H-1.1, w:W-2*MX, h:0.6, isTextBox:true, color:P.muted, fontFace:BODY, fontSize:15, italic:true });
  notes(s,d.note); return s;
}
function zitat(d){ // Platzhalter-Satz
  const s = pres.addSlide(); s.background = { color:P.weiss };
  s.addText(d.header.toUpperCase(), { x:MX, y:0.85, w:W-2*MX, h:0.5, isTextBox:true, color:P.petrol, fontFace:BODY, fontSize:16, bold:true, charSpacing:3 });
  s.addText(d.quote, { x:MX, y:2.1, w:W-2*MX, h:2.0, isTextBox:true, color:P.blau, fontFace:HEAD, fontSize:34, bold:true, italic:true, valign:"top" });
  if(d.sub) s.addText(d.sub, { x:MX, y:4.6, w:W-2*MX, h:1.2, isTextBox:true, color:P.text, fontFace:BODY, fontSize:19, valign:"top" });
  notes(s,d.note); return s;
}
function handy(d){
  const s = pres.addSlide(); s.background = { color:P.blau };
  phoneIcon(s, MX, 0.8, 1.15, P.orange);
  s.addText("JETZT AM HANDY MIT", { x:MX+1.0, y:0.8, w:W-2*MX-1.0, h:0.6, isTextBox:true, color:P.orange, fontFace:BODY, fontSize:20, bold:true, charSpacing:3, valign:"middle" });
  s.addText(d.sub, { x:MX+1.0, y:1.35, w:W-2*MX-1.0, h:0.6, isTextBox:true, color:P.creme, fontFace:BODY, fontSize:18, italic:true, valign:"middle" });
  let y = 2.5;
  d.steps.forEach((t,i)=>{
    s.addText(String(i+1), { x:MX, y:y, w:0.5, h:0.5, isTextBox:true, color:P.blau, fill:{color:P.creme}, fontFace:HEAD, fontSize:16, bold:true, align:"center", valign:"middle", shape:pres.ShapeType.ellipse, margin:0 });
    s.addText(t, { x:MX+0.8, y:y-0.05, w:W-MX-0.8-MX, h:0.7, isTextBox:true, color:P.weiss, fontFace:BODY, fontSize:16.5, valign:"middle" });
    y += Math.max(0.7, 0.55 + (t.length>70?0.3:0));
  });
  notes(s,d.note); return s;
}
function aufgabe(d){
  const s = pres.addSlide(); s.background = { color:P.weiss };
  s.addShape(pres.ShapeType.roundRect, { x:MX, y:1.5, w:W-2*MX, h:4.3, rectRadius:0.12, fill:{color:P.tint}, line:{type:"none"} });
  s.addText("DEINE AUFGABE", { x:MX+0.6, y:2.0, w:W-2*MX-1.2, h:0.5, isTextBox:true, color:P.orange, fontFace:BODY, fontSize:17, bold:true, charSpacing:3 });
  s.addText(d.text, { x:MX+0.6, y:2.6, w:W-2*MX-1.2, h:1.8, isTextBox:true, color:P.blau, fontFace:HEAD, fontSize:26, bold:true, valign:"top" });
  chip(s, MX+0.6, 4.85, "WERKSTATT · Station „"+d.station+"“", P.orange, P.weiss, 4.6);
  notes(s,d.note); return s;
}
function ausblick(d){
  const s = pres.addSlide(); s.background = { color:P.weiss };
  s.addText("ALS NÄCHSTES", { x:MX, y:2.7, w:W-2*MX, h:0.5, isTextBox:true, color:P.petrol, fontFace:BODY, fontSize:16, bold:true, charSpacing:3 });
  s.addText(d.text, { x:MX, y:3.25, w:W-2*MX, h:1.6, isTextBox:true, color:P.blau, fontFace:HEAD, fontSize:30, bold:true, valign:"top" });
  notes(s,d.note); return s;
}
function abschluss(d){
  const s = pres.addSlide(); s.background = { color:P.blau };
  chip(s, MX, 0.9, "MODUL 1 · ABGESCHLOSSEN", P.orange, P.weiss, 3.6);
  s.addText(d.title, { x:MX, y:1.7, w:W-2*MX, h:1.2, isTextBox:true, color:P.weiss, fontFace:HEAD, fontSize:46, bold:true });
  s.addText(d.text, { x:MX, y:3.1, w:W-2*MX, h:1.6, isTextBox:true, color:P.creme, fontFace:BODY, fontSize:20, valign:"top" });
  chip(s, MX, 5.0, "WERKSTATT · Station „"+d.station+"“", P.petrol, P.weiss, 4.6);
  notes(s,d.note); return s;
}

// ---------- Inhalt Modul 1 ----------
modultitel({ kicker:"STARTKLAR · MODUL 1", title:"Dein Profil steht", sub:"5 Lektionen · rund 38 Minuten",
  note:"Ziel des Moduls: Am Ende hat sie ein eingerichtetes Business-Profil mit getippter Bio, angelegten Highlights, Profilbild, Link und Zwei-Faktor-Schutz. Überprüfbar, indem man ihr Profil aufmacht." });

// L1.1
titel({ num:"1.1", lekt:"1.1", title:"Neues Konto oder dein altes umbauen?", sub:"Am Ende dieser Lektion hast du dich entschieden — und die Entscheidung ist gemacht, nicht aufgeschoben.",
  note:"Wir fangen ganz vorne an. Die allererste Frage, die mir jede Networkerin stellt, ist die hier, und meistens hängt sie zwei Wochen daran fest. Wir klären das jetzt in acht Minuten und dann ist es erledigt." });
lernen({ items:["Wann ein neues Konto der bessere Weg ist","Was mit deinen alten Urlaubsbildern passiert","Warum du deine bestehenden Follower nicht verlierst"],
  note:"Ich zeig dir gleich beide Wege auf meinem Handy. Und ich sag dir ehrlich dazu, was ich selber gemacht hab und warum." });
inhalt({ header:"Die Entscheidungshilfe", items:[
  {label:"Neues Konto,", text:"wenn dein altes Profil voll mit Privatbildern ist und du dich dabei unwohl fühlst"},
  {label:"Umstellen,", text:"wenn du schon Menschen drauf hast, die dich mögen"},
  {label:"Im Zweifel: umstellen.", text:"Follower, die dich kennen, sind mehr wert als ein aufgeräumtes leeres Konto."}],
  note:"Die meisten Frauen wollen neu anfangen, weil sich das sauberer anfühlt. Und dann stehen sie bei null Followern und posten drei Wochen ins Leere, bis die Lust weg ist. Deine Tante, deine Nachbarin und die Mädels aus dem Turnverein sind deine ersten Zuschauerinnen, auch wenn sie nie kaufen. Nimm sie mit." });
handy({ sub:"Weg 1: neues Konto · Weg 2: bestehendes umbauen", steps:[
  "Instagram öffnen → Profil unten rechts",
  "Weg 1: oben auf den Namen tippen → „Konto hinzufügen“ → „Neues Konto erstellen“",
  "Weg 2: alte Beiträge durchgehen → Privates archivieren (drei Punkte → „Archivieren“). Archiviert ≠ gelöscht.",
  "Kurz zeigen, wo das Archiv liegt und wie man etwas zurückholt"],
  note:"Archivieren ist dein Freund. Du löschst nichts. Du legst es in eine Schublade, die nur du siehst. Wenn du es in einem halben Jahr zurückwillst, holst du es mit zwei Klicks zurück." });
aufgabe({ text:"Entscheide dich jetzt. Wenn du umstellst: archiviere alles, was nicht zu dir als Unternehmerin passt.", station:"Konto",
  note:"Mach das wirklich jetzt und nicht später. Später ist der Ort, an dem Instagram-Profile sterben." });
ausblick({ text:"Dein Name, dein Profilbild — und das Suchfeld, das fast niemand richtig nutzt." });

// L1.2
titel({ num:"1.2", lekt:"1.2", title:"Die zwei Namensfelder — und warum nur eines gefunden wird",
  note:"Hier verschenken neunzig Prozent der Networkerinnen ihre Sichtbarkeit, und zwar völlig unnötig, weil es zwei Minuten dauert das zu ändern." });
lernen({ items:["Der Unterschied zwischen @username und Name-Feld","Was ins Name-Feld gehört, damit dich Instagram findet","Welches Profilbild funktioniert"] });
inhalt({ header:"Das Prinzip", items:[
  {label:"@username", text:"= deine Adresse. Kurz, merkbar, ohne Zahlenwüste."},
  {label:"Name-Feld", text:"= dein Suchbegriff. Hier steht, wobei du hilfst."},
  {label:"Beispiel:", text:"@sandra.wellness  ·  Name-Feld: Sandra · Energie für Mamas ab 35"}],
  note:"Das Name-Feld ist das einzige Feld ausser dem Username, das Instagram durchsucht. Wenn da nur dein Vorname steht, findet dich genau niemand, der dich nicht schon kennt. Schreib dein Thema rein und deinen Namen." });
handy({ sub:"Profil bearbeiten → Name und Username setzen", steps:[
  "Profil → „Profil bearbeiten“",
  "Name-Feld tippen, Beispiel live eintippen",
  "Username ändern und die Warnung zeigen, dass man ihn nicht beliebig oft ändern kann",
  "Profilbild ändern: helles Bild, Gesicht gross genug (klein wie ein Daumennagel)"],
  note:"Beim Profilbild bitte kein Produktbild und kein Firmenlogo. Menschen kaufen bei Menschen. Nimm ein Bild, auf dem man dein Gesicht erkennt, wenn man das Handy auf Armlänge hält." });
aufgabe({ text:"Trag beides ein — Name-Feld und Username.", station:"Namensfelder" });
ausblick({ text:"Jetzt kommt der Teil, vor dem sich alle drücken: die Bio." });

// L1.3
titel({ num:"1.3", lekt:"1.3", title:"Vier Zeilen, die in zwei bis drei Sekunden entscheiden, ob jemand bleibt",
  note:"Du hast zwei bis drei Sekunden. In der Zeit entscheidet jemand, ob er dir folgt oder weiterwischt. Diese zwei bis drei Sekunden sind deine Bio." });
lernen({ items:["Die vier Zeilen und was in jede gehört","Wie du einen Zeilenumbruch hinbekommst, der auf dem Handy funktioniert","Dein Platzhalter-Satz für heute"] });
inhalt({ header:"Die vier Zeilen", items:[
  {num:true, text:"Wem hilfst du wobei?"},
  {num:true, text:"Warum ausgerechnet du? (deine Erfahrung, eine Zahl, dein Leben)"},
  {num:true, text:"Was gibt es hier zu holen?"},
  {num:true, text:"Was soll sie jetzt tun? (ein Pfeil nach unten auf den Link)"}],
  note:"Wenn du den Starter-Guide gelesen hast, kennst du diese vier Zeilen schon. Jetzt tippen wir sie wirklich ein, in der Version, die du heute hast, und nicht in der perfekten Version in drei Monaten." });
zitat({ header:"Dein Platzhalter-Satz", quote:"„Ich helfe [wem] dabei, [was], damit [welches Gefühl].“",
  sub:"Nimm die Version, die dir in zehn Minuten einfällt. Sie wird sich ändern. Das ist so vorgesehen.",
  note:"Und jetzt mal ganz ehrlich: dein Thema wird sich noch verschieben. Meins hat sich auch verschoben, von Mental Load zu dem, was ich heute mache. Deshalb halten wir uns hier nicht auf. Wenn du bei diesem Satz wirklich feststeckst, ist das ein eigenes Thema — dafür hab ich einen eigenen kurzen Kurs. Für heute reicht die grobe Version." });
handy({ sub:"Bio tippen — mit dem Zeilenumbruch-Trick", steps:[
  "Profil bearbeiten → Steckbrief",
  "Zeigen: die Eingabetaste im Feld macht je nach Handy nichts",
  "Trick: Text in der Notizen-App schreiben, Zeilenumbrüche setzen, kopieren, in die Bio einfügen",
  "Zeichenzahl im Blick behalten und zeigen, wie sie sich füllt",
  "Fertige Bio auf dem Profil anschauen"],
  note:"Der Notizen-Trick spart dir eine halbe Stunde Fluchen. Ich hab damals ewig gebraucht, bis mir das jemand gesagt hat." });
inhalt({ header:"Dein Bio-Check", items:[
  {text:"Bio steht? Dann lass sie durch meinen Bio-Check laufen. Du bekommst zurück, was schon zieht und was noch schwammig ist."}],
  foot:"Link im Kursbereich · auch in der Werkstatt bei Station „Bio“",
  note:"AUFNAHME-HINWEIS: nur die automatisierte Version nennen — KEINEN persönlichen Profilcheck per Sprachnachricht versprechen (der gehört zu „Expertin statt Verkäuferin“).\n\nSprechtext: Den Bio-Check hab ich sowieso für alle offen — du kriegst ihn hier gleich mit dazu. Schick deine Bio durch und schau, was zurückkommt. Und wenn was schwammig bleibt, liegt das fast immer am Thema, nicht an den Worten." });
aufgabe({ text:"Bio steht auf deinem Profil. Vorher durch die Werkstatt.", station:"Bio" });
ausblick({ text:"Als Nächstes bauen wir dein Schaufenster: Highlights und dein Link." });

// L1.4
titel({ num:"1.4", lekt:"1.4", title:"Dein Schaufenster in zwanzig Minuten",
  note:"Highlights sind die kleinen Kreise unter deiner Bio. Die meisten Networkerinnen haben da nichts drin oder ihren letzten Urlaub. Dabei ist das die Stelle, an der jemand nachschaut, ob du echt bist." });
lernen({ items:["Die fünf Ordner, die reichen","Wie du sie füllst, wenn du noch nie eine Story gepostet hast","Ein Link oder mehrere — ohne Zusatztool"] });
inhalt({ header:"Die fünf Ordner", items:[
  {label:"•", text:"Über mich"},{label:"•", text:"Mein Thema"},{label:"•", text:"Feedback"},
  {label:"•", text:"Gratis für dich"},{label:"•", text:"Mein Angebot"}],
  foot:"Mehr braucht am Anfang niemand. Wirklich niemand.",
  note:"Feedback ist am Anfang leer, und das ist völlig in Ordnung. Du legst den Ordner trotzdem an, damit du weisst, wo die erste Rückmeldung hingehört, wenn sie kommt. Und sie kommt." });
inhalt({ header:"Das Henne-Ei-Problem", items:[
  {text:"Für ein Highlight brauchst du eine Story. Für eine Story brauchst du Mut."},
  {label:"Lösung:", text:"Du postest fünf einfache Stories hintereinander und packst sie sofort in die Ordner."}],
  note:"Du kannst eine Story posten und sie in dem Moment ins Highlight legen, in dem sie noch keine drei Leute gesehen haben. Niemand merkt, dass du das an einem Nachmittag gemacht hast." });
handy({ sub:"Fünf Highlights anlegen · Cover setzen · Link eintragen", steps:[
  "Story posten (ganz simpel, ein Foto mit Text)",
  "Profil → „Neu“ unter der Bio → Story auswählen → Namen vergeben",
  "Cover setzen: einfarbiges Bild aus Canva oder aus der Galerie",
  "Highlight bearbeiten, um später Stories zu ergänzen",
  "Bio bearbeiten → Links → einen Link eintragen",
  "Zeigen: Instagram lässt mehrere Links direkt zu — ohne Zusatztool"],
  note:"Du brauchst am Anfang kein Linktree und nichts, was monatlich Geld kostet. Instagram lässt dich mehrere Links direkt eintragen. Fang damit an." });
aufgabe({ text:"Fünf Highlights angelegt, Link steht.", station:"Schaufenster" });
ausblick({ text:"Eine letzte Sache, bevor wir posten: dein Konto absichern." });

// L1.5
titel({ num:"1.5", lekt:"1.5", title:"Fünf Minuten, damit dir dein Konto nicht abhandenkommt",
  note:"Ich weiss, das ist der langweiligste Punkt im ganzen Kurs. Mach ihn trotzdem. Ich kenne mehrere Frauen, denen das Konto weggenommen wurde, und eine davon hatte tausend Followerinnen und kam nie wieder rein." });
lernen({ items:["Zwei-Faktor einschalten","Wiederherstellungscodes sichern","Woran du eine gefälschte Nachricht von „Instagram“ erkennst"] });
inhalt({ header:"Die drei Regeln", items:[
  {num:true, text:"Zwei-Faktor an, per App statt per SMS, wenn du die Wahl hast"},
  {num:true, text:"Codes ausdrucken oder in deinem Passwortmanager sichern"},
  {num:true, text:"Instagram schreibt dir nie per DM, dass dein Konto gelöscht wird"}],
  note:"Diese DMs sehen echt aus. Da steht: dein Konto verstösst gegen die Richtlinien, klick hier zur Prüfung. Du klickst nichts. Du meldest es und blockierst." });
handy({ sub:"Zwei-Faktor-Authentifizierung einschalten", steps:[
  "Einstellungen → Kontenübersicht → Passwort und Sicherheit → Zwei-Faktor",
  "Methode wählen (App bevorzugt), Codes sichern"],
  note:"Nimm die App-Variante, wenn du die Wahl hast — sie ist sicherer als SMS." });
abschluss({ title:"Dein Profil steht.", text:"Name, Bio, Highlights, Link, Sicherheit. Schau es dir jetzt einmal so an, wie es eine Fremde sieht.", station:"Profil-Check",
  note:"Geh raus aus deinem Profil, such dich selber über die Suche und schau dich an wie eine Fremde. Was siehst du in zwei bis drei Sekunden? Wenn du die Frage beantworten kannst, ist Modul eins erledigt." });
ausblick({ text:"Modul 2: jetzt posten wir. Reel, Karussell, Story — und ich zeig dir jedes einzeln." });

const OUT = "outputs/produkte/instagram-startklar/06-praesentation/startklar-modul-1.pptx";
await pres.writeFile({ fileName: OUT });
console.log("OK ->", OUT);
