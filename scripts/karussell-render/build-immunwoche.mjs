#!/usr/bin/env node
/**
 * Immunwoche-Teilnehmerzettel Tag 2-5 + Gesamt-PDF.
 *
 *   node build-immunwoche.mjs
 *
 * Erzeugt in outputs/freebies/immunwoche-2026-09/:
 *   tag2.html … tag5.html   + je ein PDF
 *   immunwoche-komplett.html + PDF (alle 5 Tage)
 *
 * Layout: Fliesssatz auf A4 mit @page-Rand und Puppeteer-Fusszeile.
 * Dadurch muss keine Seite von Hand ausbalanciert werden.
 */
import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(__dirname, '../../outputs/freebies/immunwoche-2026-09');

// ---------------------------------------------------------------- Bausteine

const esc = s => String(s);
const P = (...abs) => abs.map(a => `<p>${a}</p>`).join('\n');

const block = (nr, titel, intro, inhalt) => `
<section class="block">
  <h2><span class="nr">${nr}</span> ${titel}</h2>
  ${intro ? `<p class="intro">${intro}</p>` : ''}
  ${inhalt}
</section>`;

const kacheln = items => `
<div class="zahlen">
  ${items.map(([z, t]) => `<div class="zahl-kachel"><b>${z}</b><span>${t}</span></div>`).join('\n  ')}
</div>`;

const irrtuemer = items => items.map(([f, r]) => `
<div class="irrtum">
  <div class="falsch"><span class="kopf">Der Irrtum</span><p>${f}</p></div>
  <div class="richtig"><span class="kopf">Was wirklich stimmt</span><p>${r}</p></div>
</div>`).join('\n');

const irrtumBlock = (nr, titel, items) => `
<section class="block">
  <h2><span class="nr">${nr}</span> ${titel}</h2>
  ${irrtuemer(items)}
</section>`;

const schritte = items => `
<div class="schritte">
  ${items.map(([b, s]) => `<div class="schritt"><span class="haken">✓</span><div><b>${b}</b><span>${s}</span></div></div>`).join('\n  ')}
</div>`;

const merksatz = t => `<div class="merksatz"><p>${t}</p></div>`;

const beiMir = t => `
<div class="beimir">
  <span class="label">Bei mir läuft das so</span>
  ${P(...t)}
</div>`;

const oele = (titel, rezept, text, warnung) => `
<div class="oele">
  <span class="label">${titel}</span>
  <p class="rezept">${rezept}</p>
  <p>${text}</p>
  ${warnung ? `<p class="warnung">⚠️ ${warnung}</p>` : ''}
</div>`;

const quellen = gruppen => `
<div class="quellenblock">
  <span class="label">Woher die Angaben stammen</span>
  ${gruppen.map(([k, v]) => `<p><span class="gruppe">${k}</span> ${v}</p>`).join('')}
</div>`;

const morgen = t => `<p class="morgen"><span>Morgen</span> ${t}</p>`;

const vergleich = (kopf, zeilen) => `
<div class="tab-huelle">
  <table class="vergleich">
    <thead><tr>${kopf.map(k => `<th>${k}</th>`).join('')}</tr></thead>
    <tbody>
      ${zeilen.map(z => `<tr>${z.map((c, i) => `<td${i === 0 ? ' class="mittel"' : ''}>${c}</td>`).join('')}</tr>`).join('\n      ')}
    </tbody>
  </table>
</div>`;

// ---------------------------------------------------------------- Inhalt

const TAGE = [
  {
    nr: 2, wochentag: 'Dienstag', slug: 'tag2',
    titel: 'Schlaf',
    unter: 'Der Hebel, den fast alle unterschätzen — und die überzeugendste Studie der ganzen Woche.',
    kern: 'Dein Immunsystem macht seine wichtigste Arbeit, während du nichts tust.',
    body: [
      block('01', 'Was nachts wirklich passiert', '',
        P(
          'Tagsüber ist dein Immunsystem im Einsatz. Nachts baut es um — und das sind zwei völlig verschiedene Dinge.',
          'Im Tiefschlaf fährt dein Stresshormon Cortisol herunter. Erst dann hat dein Körper überhaupt Ruhe für Reparatur. Gleichzeitig werden deine Immunzellen <b>klebriger</b> — und Kleben ist genau das, was sie können müssen, um einen Erreger festzuhalten. Bei zu wenig Schlaf lässt diese Klebkraft messbar nach.',
          'Und dein Immunsystem <b>lernt</b> im Schlaf, ganz ähnlich wie dein Gehirn. Was es tagsüber an Erregern kennengelernt hat, wird nachts abgespeichert. Deshalb fällt die Antwort auf eine Impfung schwächer aus, wenn jemand in den Nächten davor schlecht geschlafen hat.'
        )),
      block('02', 'Die Zahl, die alles sagt', 'Eine Untersuchung, die man so heute kaum mehr machen dürfte — und gerade deshalb ist sie so aussagekräftig.',
        P(
          '164 gesunde Erwachsene trugen sieben Nächte lang ein Messarmband. Danach bekamen <b>alle die gleiche Menge Erkältungsviren direkt in die Nase</b> und wurden in Quarantäne beobachtet.',
          'Wer <b>sechs Stunden oder weniger</b> geschlafen hatte, wurde rund <b>viermal so oft</b> wirklich krank wie die, die mehr als sieben Stunden schliefen. Und das unabhängig von Alter, Gewicht, Jahreszeit, Stress und Rauchen.',
          'Das ist so überzeugend, weil alle demselben Virus in derselben Menge ausgesetzt waren. Der einzige Unterschied war der Schlaf davor.'
        )),
      block('03', 'Warum du abends nicht runterkommst', 'Das ist kein Charakterfehler und keine fehlende Disziplin.',
        P(
          'Dein Cortisol soll abends fallen. Wenn dein Tag aber durchgetaktet war und du erst um neun zur Ruhe kommst, ist dein System noch im Alarmmodus — und der lässt sich nicht auf Knopfdruck ausschalten. Müde und trotzdem wach ist genau das.',
          'Zwei Dinge, die du in der Hand hast: <b>Koffein</b> bleibt lange. Von einem Espresso um drei Uhr nachmittags ist um neun Uhr abends noch rund die Hälfte in dir. Und <b>Licht</b> — helles Deckenlicht und der Bildschirm sagen deinem Körper, dass noch Tag ist.',
          'Und das Schlafzimmer darf kühl sein. Rund 18 Grad sind angenehmer, als die meisten denken — dein Körper muss zum Einschlafen seine Temperatur senken.'
        )),
      irrtumBlock('04', 'Die drei häufigsten Irrtümer', [
        ['„Ich brauche halt nur fünf Stunden."',
         'Echte Kurzschläferinnen gibt es, aber sie sind sehr selten. Viel häufiger hat man sich an ein Defizit gewöhnt und merkt nicht mehr, wie es sich mit genug Schlaf anfühlt.'],
        ['„Am Wochenende hole ich das nach."',
         'Etwas holst du nach, aber nicht alles — und die Regelmässigkeit ersetzt es nicht. Dein Körper arbeitet mit einem Rhythmus, nicht mit einem Konto.'],
        ['„Ein Glas Wein hilft mir beim Einschlafen."',
         'Beim Einschlafen ja. Beim Durchschlafen nicht: Alkohol drückt genau den Tiefschlaf weg, in dem die Reparatur passiert. Du schläfst schneller ein und wachst weniger erholt auf.'],
      ]),
      block('05', 'Die Zahlen für heute', '', kacheln([
        ['4×', 'so oft wurden Menschen krank, die sechs Stunden oder weniger schliefen — bei gleicher Virusmenge.'],
        ['7 Std', 'war in der Untersuchung die Schwelle, ab der das Risiko deutlich sank.'],
        ['6 Std', 'nach dem Espresso ist noch die Hälfte des Koffeins in dir. Der Kaffee um drei wirkt um neun noch.'],
        ['18°', 'im Schlafzimmer. Zum Einschlafen muss dein Körper seine Temperatur senken — das geht in einem warmen Raum schlechter.'],
      ])),
      beiMir([
        'Beim Schlaf geht es vor allem um mich — genug Schlaf ist bei mir das A und O. Mich nimmt es viel schneller, wenn ich zu knapp schlafe, und das merke ich sofort an der Geduld mit den Kindern.',
        'Darum habe ich mein Abendritual. Ich öle mich abends ein oder gönne mir ein Ölbad und fahre bewusst runter. Die Kinder haben übrigens alle einen eigenen Diffuser — den lassen wir gern mit ihren Lieblingsölen laufen. Das lieben sie, und es ist für sie das Signal, dass der Tag jetzt zu Ende geht.',
      ]),
      oele('🌙 Diffuser „Schlaf gut"',
        '4 Tropfen Lavendel · 2 Tropfen Wilde Orange',
        'Abends in den Diffuser. Fürs Ölbad: bis zu 7 Tropfen in einem halben Becher Sahne oder 20 ml Milch verrühren und dann erst ins Wasser geben — sonst schwimmt das Öl obenauf. Oder Lavendel und Weihrauch verdünnt auf Nacken und Fusssohlen.'),
      block('06', 'Was du heute tun kannst', 'Such dir eins aus. Nicht alle vier.', schritte([
        ['Koffein-Schluss um 14 Uhr.', 'Der einzelne Hebel, den fast niemand nutzt — und der am selben Abend wirkt.'],
        ['Eine halbe Stunde früher ins Bett.', 'Nicht zwei. Eine halbe. Das schaffst du, zwei Stunden schaffst du nicht.'],
        ['Diffuser an, Deckenlicht aus.', 'Kleine Lampen statt grosses Licht sagen deinem Körper, dass der Tag vorbei ist.'],
        ['Fenster auf, bevor du ins Bett gehst.', 'Kühl und frisch schläft es sich messbar besser.'],
      ])),
      merksatz('Du kannst dein Immunsystem nicht zwingen, schneller zu arbeiten. Aber du kannst ihm die Nacht geben, in der es arbeitet.'),
      morgen('Bewegung und frische Luft — und warum nicht die Kälte krank macht.'),
    ],
  },

  {
    nr: 3, wochentag: 'Mittwoch', slug: 'tag3',
    titel: 'Bewegung und frische Luft',
    unter: 'Warum deine Abwehr eine Pumpe braucht, die du selbst bist — und was die Heizung damit zu tun hat.',
    kern: 'Dein Blut hat ein Herz, das es pumpt. Deine Lymphe hat nur dich.',
    body: [
      block('01', 'Die Lymphe hat keine Pumpe', '',
        P(
          'Deine Immunzellen sitzen nicht still. Sie patrouillieren — durch das Blut, vor allem aber durch das <b>Lymphsystem</b>, ein zweites Leitungsnetz, das durch deinen ganzen Körper läuft und in dem die Abwehrzellen unterwegs sind.',
          'Und dieses Netz hat <b>kein eigenes Herz</b>. Es bewegt sich nur, wenn deine Muskeln sich anspannen und du tief atmest. Wer den ganzen Tag sitzt, lässt die Patrouille im Grunde stehen.',
          'Das ist der eigentliche Grund, warum Bewegung hier hingehört — nicht Kalorien, nicht Figur. Es ist der Antrieb für ein System, das keinen eigenen hat.'
        )),
      block('02', 'Was Bewegung messbar bringt', 'Und gleich danach die gute Nachricht für alle, die Angst haben, Sport mache anfällig.',
        P(
          'In einer Untersuchung gingen Frauen fünfmal pro Woche 45 Minuten zügig spazieren, 15 Wochen lang. Ihre <b>Krankheitstage mit Erkältungssymptomen halbierten sich</b> im Vergleich zur Gruppe, die nichts änderte. Quer über mehrere Studien liegt der Effekt bei 25 bis 50 Prozent weniger Symptomtagen.',
          'Das Bemerkenswerte daran: Es war Spazierengehen. Kein Trainingsplan, kein Studio, keine Ausrüstung.',
          '<b>Und die Entwarnung:</b> Nach einer anstrengenden Einheit sinkt die Zahl der Immunzellen im Blut kurz ab. Das wurde jahrzehntelang als „offenes Fenster" gedeutet — als wäre man danach schutzlos. Eine grosse Übersichtsarbeit hat das widerlegt: Die Zellen verschwinden nicht, sie werden in die <b>Gewebe umverteilt</b>, wo sie patrouillieren. Es ist erhöhte Wachsamkeit, nicht Schwäche.'
        )),
      block('03', 'Die Heizung ist das eigentliche Problem', 'Jetzt beginnt die Zeit, in der wir wieder drinnen sitzen. Und drinnen verändert sich etwas, das kaum jemand auf dem Schirm hat.',
        P(
          'Kalte Luft kann fast keine Feuchtigkeit halten. Wenn sie hereinkommt und du sie aufheizt, fällt die Luftfeuchtigkeit im Raum auf <b>rund 20 Prozent</b> — trockener als in manchen Wüstenregionen.',
          'Das hat zwei Folgen. Erstens werden die <b>Flimmerhärchen</b> in deinen Atemwegen langsam. Das sind die feinen Härchen, die Erreger normalerweise nach oben und hinaus befördern. Bei trockener Luft schaffen sie das nicht mehr gut — deine erste Mauer von gestern wird also durchlässiger.',
          'Zweitens trocknen die winzigen Tröpfchen in der Luft schneller aus, und die Erreger darin bleiben länger in der Schwebe.',
          'Der Zielbereich sind <b>40 bis 60 Prozent</b> Luftfeuchtigkeit. Und das wichtigste Werkzeug dafür ist kostenlos: <b>Stosslüften</b>. Fenster ganz auf, wenige Minuten, am besten Durchzug. Ein gekipptes Fenster tauscht kaum Luft aus, kühlt dafür die Wände aus.'
        )),
      irrtumBlock('04', 'Die drei häufigsten Irrtümer', [
        ['„Kälte macht krank."',
         'Nicht die Kälte. Es ist das Drinnensitzen: mehr Menschen auf engem Raum, weniger Luftwechsel und trockene Heizungsluft, die deine Schleimhäute austrocknet. Draussen in der Kälte steckt sich kaum jemand an.'],
        ['„Nach dem Sport bin ich anfälliger."',
         'Das war jahrzehntelang die Lehrmeinung und gilt heute als widerlegt. Die Immunzellen verschwinden nach dem Training nicht — sie ziehen in die Gewebe um und patrouillieren dort.'],
        ['„Ich kippe das Fenster, das reicht."',
         'Ein gekipptes Fenster tauscht kaum Luft, kühlt aber die Wand daneben aus. Fünf Minuten ganz offen bringen mehr als eine Stunde gekippt — und kosten weniger Heizung.'],
      ]),
      block('05', 'Die Zahlen für heute', '', kacheln([
        ['50 %', 'weniger Krankheitstage bei fünfmal 45 Minuten zügigem Gehen pro Woche. Kein Studio nötig.'],
        ['8000', 'Schritte pro Tag — meine eigene Zielmarke. Erreichbar, ohne dass der Tag sich darum drehen muss.'],
        ['20 %', 'Luftfeuchtigkeit hat ein normal geheizter Raum im Winter. Das ist Wüstenniveau.'],
        ['40–60 %', 'wären der Zielbereich. Stosslüften, Wäsche drinnen trocknen, Pflanzen — alles hilft.'],
      ])),
      beiMir([
        'Jetzt kommt die Zeit, in der wir wieder mehr drinnen hocken — und damit mehr in den Keimen. Ich bewege mich täglich und schaue, dass ich auf rund 8000 Schritte komme.',
        'Abends drehe ich mit meinem Mann meist noch eine kleine Runde ums Dorf, und das ist Gold: Wir reden mal ungestört, ich schlafe besser, und es tut der Psyche gut. Dazu dreimal die Woche Krafttraining. Und ganz simpel: Stosslüften und die Bettwäsche auslüften.',
      ]),
      oele('🍃 Diffuser „Saubere Luft"',
        '2 Tropfen Eukalyptus · 2 Tropfen Teebaum · 2 Tropfen Zitrone',
        'In den Diffuser für die Wohnräume. Morgens mag ich die Aromadusche: ein bis zwei Tropfen Pfefferminze oder Zitrone in die Duschecke tröpfeln — nicht direkt unter den Strahl, sonst ist es sofort weg.'),
      block('06', 'Was du heute tun kannst', '', schritte([
        ['Fünf Minuten stosslüften.', 'Morgens nach dem Aufstehen, Fenster ganz auf. Das ist die billigste Massnahme der ganzen Woche.'],
        ['Eine Runde nach dem Abendessen.', 'Zehn Minuten reichen. Es zählt für die Schritte, für den Kopf und für den Schlaf.'],
        ['Die Treppe statt den Lift.', 'Muskelanspannung ist der Antrieb deines Lymphsystems. Jedes Mal zählt.'],
        ['Bettwäsche auslüften.', 'Fenster auf, Decke zurückschlagen, während du frühstückst.'],
      ])),
      merksatz('Es braucht kein Trainingsprogramm. Es braucht, dass du dich zwischendurch bewegst und die Fenster aufmachst.'),
      morgen('Die Rituale und die Öle konkret — und welches Ritual tatsächlich das wirksamste ist.'),
    ],
  },

  {
    nr: 4, wochentag: 'Donnerstag', slug: 'tag4',
    titel: 'Die Rituale und die Öle',
    unter: 'Warum zwanzig Sekunden am Morgen mehr bringen als jeder gute Vorsatz — und wo die Öle wirklich hingehören.',
    kern: 'Was jeden Tag passiert, schlägt das, was du dir vornimmst.',
    body: [
      block('01', 'Warum kleine Rituale halten und grosse Vorsätze nicht', '',
        P(
          'Ein Vorsatz braucht jeden Tag eine Entscheidung. Und Entscheidungen sind genau das, wovon eine Mama am Morgen schon zu viele trifft.',
          'Ein Ritual braucht keine. Es hält, wenn es an etwas andockt, das <b>ohnehin jeden Tag passiert</b>: nach dem Zähneputzen, bevor du den Kaffee eingiesst, wenn du die Schuhe der Kinder hinstellst. Der Anker macht die Arbeit, nicht deine Disziplin.',
          'Und es muss <b>kurz</b> sein. Zwanzig Sekunden sind so kurz, dass dein Kopf gar nicht erst anfängt zu verhandeln.'
        )),
      block('02', 'Das langweiligste Ritual ist das wirksamste', 'Ich sage das ganz ehrlich, auch wenn es sich nicht spannend verkauft.',
        P(
          'Eine Auswertung von 26 Studien mit insgesamt <b>161 659 Teilnehmenden</b> hat sich angeschaut, was regelmässiges Händewaschen mit Seife bringt. Ergebnis: rund <b>26 Prozent weniger Infekte der oberen Atemwege</b>, rund 22 Prozent weniger der unteren. Vorsichtigere Auswertungen kommen auf etwa 14 Prozent.',
          'Zum Vergleich: Das ist mehr, als in dieser ganzen Woche irgendein Nahrungsergänzungsmittel geschafft hat. Vitamin C verkürzt eine Erkältung um acht Prozent. Händewaschen verhindert jede vierte.',
          'Und daher kommen die zwanzig Sekunden: So lange braucht Seife, um ihre Arbeit zu tun. Nicht drei Sekunden unter den Hahn halten.'
        )),
      block('03', 'Was ätherische Öle überhaupt sind', 'Für alle, die noch keine haben — hier fängt es an.',
        P(
          'Eine Pflanze kann nicht weglaufen. Wenn sie von Pilzen, Bakterien oder Insekten angegriffen wird, muss sie sich an Ort und Stelle wehren — und das macht sie <b>chemisch</b>. Sie bildet Duftstoffe, die Angreifer fernhalten oder abtöten.',
          'Genau das steckt in so einem Fläschchen: <b>die Abwehrchemie der Pflanze, hochkonzentriert.</b> Das ist der ganze Zauber, und es erklärt beides auf einmal — warum diese Stoffe überhaupt gegen Keime wirken können, und warum sie so stark sind, dass man sie verdünnen muss.',
          'Ätherisch heisst übrigens nur, dass sie sich verflüchtigen. Es sind keine fetten Öle wie Olivenöl, sondern leichte Moleküle, die in die Luft übergehen — deshalb riecht man sie überhaupt, und deshalb funktioniert ein Diffuser.'
        )),
      block('04', 'Warum Öle überhaupt etwas tun — die Chemie', 'Das ist der Teil, den ich am wichtigsten finde. Öle wirken nicht, weil sie gut riechen. Sie wirken, weil ihre Moleküle etwas können.',
        P(
          '<b>Erstens: Sie kommen überhaupt an.</b> Unsere Zellen sind von einer Doppelschicht aus Fettbausteinen umgeben, der Zellmembran. Sie entscheidet, was hinein darf und was draussen bleibt. Ätherische Öle sind <b>lipophil</b>, also fettlöslich — und genau deshalb können ihre Moleküle diese Membran mühelos durchdringen. Das ist der ganze Grund, warum überhaupt etwas passiert, das über den Duft hinausgeht.',
          '<b>Zweitens: Sie docken an echte Rezeptoren an.</b> Und zwar an dieselben, an denen auch Medikamente ansetzen. Drei Beispiele, die gut untersucht sind:',
          '<b>Beta-Caryophyllen</b> — ein Sesquiterpen, das in Copaiba, schwarzem Pfeffer und Nelke steckt. Es bindet direkt an die <b>CB2-Rezeptoren</b> des körpereigenen Endocannabinoid-Systems. Diese Rezeptoren sitzen vor allem auf <b>Immunzellen</b> und steuern Entzündung und Schmerz. Über sie kann Beta-Caryophyllen entzündungsfördernde Botenstoffe, die Zytokine, herunterfahren — ohne die berauschende Wirkung, die man von Cannabis kennt. Copaiba ist das stärkste bekannte natürliche Vorkommen dieses Stoffes.',
          '<b>Linalool</b> — der Hauptstoff im Lavendel. Er erhöht die Aktivität der <b>GABA-Rezeptoren</b> im Gehirn. GABA ist der körpereigene Bremser: Wo GABA wirkt, werden Stressreaktionen gedämpft. Das ist derselbe Ansatzpunkt, den auch Beruhigungsmittel nutzen — nur viel sanfter.',
          '<b>1,8-Cineol und Alpha-Pinen</b> — in Eukalyptus und Rosmarin. Sie wirken auf die Atemwege und auf die Wachheit. Eucalyptus radiata besteht typischerweise zu <b>65 bis 75 Prozent</b> aus Cineol — also zum grössten Teil aus diesem einen Stoff.',
          '<b>Drittens: Sie greifen in Entzündungsprozesse ein.</b> Weihrauch besteht zu <b>30 bis 60 Prozent aus Alpha-Pinen</b> — ein Stoff, dem in Laboruntersuchungen entzündungshemmende Eigenschaften zugeschrieben werden. ⚠️ Dazu gehört eine Ehrlichkeit, die du sonst nirgends liest: Die <i>bekannteste</i> entzündungshemmende Wirkung des Weihrauchs geht auf die <b>Boswelliasäuren</b> zurück — und die stecken im Harz, <b>nicht im ätherischen Öl</b>. Wer beides in einen Topf wirft, wird zu Recht korrigiert.',
          '<b>Viertens: Sie senken messbar Stresshormone.</b> Linalool und Linalylacetat aus dem Lavendel können die <b>Cortisolausschüttung über die Hypothalamus-Hypophysen-Nebennieren-Achse</b> reduzieren. Auch Weihrauch wirkt regulierend auf die Cortisolproduktion. Das ist keine Stimmungssache — das ist eine messbare Hormonachse.',
          '<b>Fünftens: Sie greifen Keime direkt an.</b> Und zwar mechanisch, nicht mystisch. <b>Carvacrol und Thymol</b> aus dem Oregano destabilisieren die Zellwände von Bakterien. <b>Terpinen-4-ol</b> aus dem Teebaum zerstört die Zellmembran von Pilzen — deshalb wird Teebaumöl seit jeher bei Fusspilz und Nagelpilz eingesetzt. <b>Citral</b> aus dem Zitronengras hemmt Enzyme, die Mikroben zum Wachsen brauchen. Und <b>Leptospermone</b> aus dem Manuka wirken sogar gegen Bakterien, die auf herkömmliche Antibiotika nicht mehr ansprechen.'
        )),
      block('05', 'Und warum das Vorsorge ist', 'Jetzt setzt sich alles zusammen — das ist die Antwort auf „warum regelmässig".',
        P(
          'Keiner dieser Wege ist ein einzelnes dramatisches Ereignis. Niemand reibt sich einmal die Fusssohlen ein und ist danach geschützt. Vorsorge heisst hier etwas anderes, und zwar drei Dinge gleichzeitig:',
          '<b>Du hältst die Entzündungslast niedrig.</b> Über die CB2-Rezeptoren und den NF-κB-Schalter wird die Entzündungsreaktion gedämpft, bevor sie chronisch wird. Ein Körper, der nicht ständig auf niedriger Flamme entzündet ist, hat mehr übrig, wenn wirklich etwas kommt.',
          '<b>Du hältst den Cortisolspiegel unten.</b> Und das ist der bestbelegte Hebel überhaupt: Eine Auswertung von über <b>300 Studien</b> zeigt, dass chronischer Stress die Abwehr messbar dämpft — die Zellen und die Antikörperseite. Wer den Stresspegel senkt, senkt genau das, was die Abwehr am zuverlässigsten schwächt.',
          '<b>Du senkst die Keimlast, wo du sie erreichst.</b> Auf der Haut, in der Nase, an den Händen. Nicht im ganzen Raum — aber dort, wo du das Öl tatsächlich hinbringst.',
          'Dazu kommt etwas, das jede Mama vom Einschlafritual ihrer Kinder kennt: <b>Ein Duft, der immer mit Runterfahren verknüpft war, löst das Runterfahren irgendwann selbst aus.</b> Dein Körper lernt die Verknüpfung, und nach ein paar Wochen reicht der Geruch.'
        )),
      block('06', 'Was die Studien am Menschen zeigen', 'Ich sage bewusst dazu, wo die Forschung stark ist und wo sie noch dünn ist.',
        P(
          '<b>Angst und Anspannung.</b> Eine grosse Auswertung von <b>44 randomisierten kontrollierten Studien mit über 3400 Teilnehmenden</b> (Tan und Kollegen, 2023) zeigt: Inhalation ätherischer Öle senkte sowohl die akute Anspannung als auch die grundsätzliche Ängstlichkeit gegenüber Kontrollgruppen. Zusätzlich verbesserten sich <b>Herzfrequenz und systolischer Blutdruck</b> — zwei körperliche Marker, die man nicht einbilden kann.',
          '<b>Schlaf.</b> In einer kontrollierten Studie (Samadi und Kollegen, 2021) inhalierten <b>80 Menschen, die wegen einer Depression in Behandlung waren und zusätzlich schlecht schliefen</b>, entweder Lavendelöl oder Mandelöl als Kontrolle. Beide Gruppen starteten mit vergleichbaren Werten — danach war die Schlafqualität in der Lavendelgruppe <b>deutlich besser</b>.',
          '<b>Die Gesamtschau.</b> Zwei grosse Übersichtsarbeiten von 2024 fassen zusammen, dass ätherische Öle in Labor- und Tierstudien Bakterien, Pilze und teilweise Viren hemmen, oxidativen Stress senken und Entzündungsprozesse steuern können.',
          'Das ist mehr belastbare Forschung, als die meisten vermuten — und es wird laufend mehr. Genau deshalb rede ich bei Ölen über Wirkstoffe und nicht über Wohlfühlduft.'
        )),
      block('07', 'Wenn du noch gar keine Öle hast', 'Die häufigste Frage — und sie hat eine einfache Antwort. Du musst nicht auswählen.',
        P(
          'Das Problem am Anfang ist nicht, dass es zu wenig Auswahl gäbe. Es ist, dass es zu viel ist. Und wer sich drei Fläschchen einzeln zusammensucht, merkt nach zwei Wochen, dass genau das fehlt, was er nicht gekauft hat.',
          'Deshalb gibt es die <b>zehn Basis-Öle</b> als fertiges Set. Diese zehn decken zusammen ab, was in einem Haushalt tatsächlich vorkommt — nicht nur in der Immunwoche, sondern das ganze Jahr. Hier steht, was jedes einzelne tut und <b>warum</b> es das tut.'
        )),
      vergleich(['Zum Runterkommen', 'Was es tut', 'Der Stoff dahinter'], [
        ['<b>Lavendel<br><span style="font-weight:400;color:#63747b">Beruhigung, Haut, Schlaf</span></b>',
         'Beruhigt die Nerven, hilft beim Einschlafen, entzündungshemmend und hautberuhigend bei Reizungen, Verbrennungen, Insektenstichen.',
         '<b>Linalool</b> und <b>Linalylacetat</b> sind die beiden Hauptstoffe — die internationale Norm schreibt 25–38 % bzw. 25–45 % vor. Linalool erhöht die Aktivität der GABA-Rezeptoren, des körpereigenen Bremssystems.'],
        ['<b>Weihrauch<br><span style="font-weight:400;color:#63747b">Zellschutz, Entzündung, Haut</span></b>',
         'Zellschützend und regenerierend, unterstützt die Wundheilung, wirkt beruhigend und schmerzlindernd. Das „Königsöl“ im Set.',
         '<b>Alpha-Pinen</b> macht 30 bis 60 Prozent des Weihrauchöls aus. ⚠️ Die bekannten Boswelliasäuren stecken im Harz, <b>nicht im ätherischen Öl</b> — ein häufiger Irrtum.'],
        ['<b>Pfefferminze<br><span style="font-weight:400;color:#63747b">Kühlung und Klarheit</span></b>',
         'Kühlend und erfrischend, bei Spannungsgefühl in Kopf und Nacken, bei Übelkeit, für Wachheit.',
         '<b>Menthol</b> aktiviert die Kälterezeptoren — daher das Frischegefühl. Das Arzneibuch verlangt für Pfefferminzöl mindestens 44 Prozent freie Alkohole, berechnet als Menthol.']
       ]),
      block('08', 'Und drei zum Reinigen', 'Die andere Hälfte — hier geht es um Keime, Haut und Frische.',
        vergleich(['Einzelöl', 'Was es tut', 'Der Stoff dahinter'], [
          ['<b>Teebaum<br><span style="font-weight:400;color:#63747b">das Reinigungsöl</span></b>',
           'Stark antibakteriell, hautklärend. Bei kleinen Wunden, Unreinheiten, Schuppen, Fusspilz, Zeckenbiss.',
           '<b>Terpinen-4-ol</b> zerstört die Zellmembran von Pilzen und Bakterien. Die internationale Norm für Teebaumöl verlangt <b>30 bis 48 Prozent</b> davon — sie heißt sogar „Melaleuca, terpinen-4-ol type“.'],
          ['<b>Oregano<br><span style="font-weight:400;color:#63747b">das stärkste im Set</span></b>',
           'Das kraftvollste Öl der zehn. Bei Warzen, Nagelpilz, im Fussbad, im Winter zusammen mit Zitrone und On Guard.',
           '<b>Carvacrol</b> ist je nach Herkunft mit 50 bis 80 Prozent der Hauptstoff, dazu <b>Thymol</b>. Beide destabilisieren die Zellwände von Bakterien — genau deshalb ist es ein „heisses“ Öl.'],
          ['<b>Zitrone<br><span style="font-weight:400;color:#63747b">der Allrounder</span></b>',
           'Frisch, reinigend, stimmungsaufhellend. Im Wasser, im Haushalt, im Kuchen, bei Halskratzen mit Honig.',
           '<b>Limonen</b> macht typischerweise rund 70 Prozent des Zitronenöls aus — antimikrobiell und stark antioxidativ. ⚠️ Macht die Haut lichtempfindlich: nach dem Auftragen nicht in die Sonne.']
         ])),
      block('09', 'Weihrauch — Öl oder Harz?', 'Der häufigste Irrtum beim Weihrauch, und einer, bei dem du mit dem richtigen Satz sofort auffällst.',
        P(
          'Weihrauch gilt als das entzündungshemmende Öl schlechthin. Die Studien, auf die sich das stützt, wurden aber fast alle mit <b>Boswelliasäuren</b> gemacht — und die sind im <b>ätherischen Öl gar nicht drin</b>.',
          'Der Grund ist reine Physik. Bei der Wasserdampfdestillation gehen nur die <b>leichten</b> Moleküle mit dem Dampf über. Boswelliasäuren sind gross und schwer und bleiben im Harz zurück. Im Öl landet dafür das <b>Alpha-Pinen</b>, 30 bis 60 Prozent davon.',
          'Und genau deshalb gibt es dafür ein <b>eigenes Produkt</b>: Die <b>Weihrauch Mikroperlen-Kapseln</b> enthalten laut Herstellerbogen Weihrauch<b>harzextrakt</b> (<i>Boswellia serrata</i>) <b>und</b> ätherisches Weihrauchöl (<i>Boswellia sacra</i>) — mit einer standardisierten Konzentration von <b>60 Prozent AKBA</b>, also Acetyl-11-Keto-beta-Boswelliasäure.',
          'Praktisch heißt das: <b>Das Öl und die Kapsel machen nicht dasselbe.</b> Wer die Wirkung aus den Studien sucht, braucht das Harz. Wer ein Öl für Haut, Ruhe und die Abendroutine will, nimmt das Fläschchen. Beides ist Weihrauch, aber es sind zwei verschiedene Dinge.'
        )),
      block('10', 'Und die vier fertigen Mischungen', 'Die musst du nicht selbst zusammenstellen — sie sind schon gemischt.',
        vergleich(['Mischung', 'Was sie tut', 'Was drin ist und warum'], [
          ['<b>On Guard</b><br><span style="font-weight:400;color:#63747b">die schützende Mischung</span>',
         'Das Immunwoche-Öl schlechthin. Für die Morgenroutine, als Mundspülung, im Diffuser, als Haushaltsreiniger.',
         'Wild Orange, <b>Nelke</b> (Eugenol), <b>Zimt</b> (Zimtaldehyd), <b>Eukalyptus</b> und <b>Rosmarin</b> (beide 1,8-Cineol). Eine Kombination aus vier verschiedenen antimikrobiellen Wirkstoffklassen.'],        ['<b>Air</b><br><span style="font-weight:400;color:#63747b">die Atemwegsmischung</span>',
         'Schleimlösend und befreiend. Abends im Diffuser bei verstopfter Nase oder Husten, verdünnt auf Brust und Rücken.',
         'Acht Öle: Lorbeer, <b>Eukalyptus</b>, Pfefferminze, Teebaum, Zitrone, Kardamom, Kampferbaum (<i>Cinnamomum camphora</i>) und Ravensara. Der Wirkstoff ist <b>1,8-Cineol</b> — er verflüssigt Sekret und treibt die Flimmerhärchen an.'],        ['<b>ZenGest</b><br><span style="font-weight:400;color:#63747b">die Verdauungsmischung</span>',
         'Nach dem Essen auf den Bauch, bei Übelkeit unterwegs, bei Blähungen und Krämpfen.',
         'Laut Herstellerbogen: Pfefferminze, Koriandersamen, <b>Ingwer</b> (Gingerole), Kümmel, Kardamom, <b>Fenchel und Sternanis</b> (Anethol) — krampflösend auf die glatte Muskulatur im Magen-Darm-Bereich.'],        ['<b>Deep Blue</b><br><span style="font-weight:400;color:#63747b">die lindernde Mischung</span>',
         'Bei Verspannungen, Muskel- und Gelenkschmerzen, Kopfschmerzen, nach dem Sport.',
         'Zwölf Öle: Japanische Minze, Rosmarin, Kopaiva, Anis, Orangenminze, Pfefferminze, Blauer Eukalyptus, Teebaum, Strohblume, Blauer Rainfarn, Kamille und <b>Wintergrün</b>. Das Wintergrün enthält <b>Methylsalicylat</b> — chemisch aus derselben Familie wie der Aspirin-Wirkstoff. ⚠️ Nicht bei kleinen Kindern, nicht bei Blutverdünnern.'],
        ])),
      block('11', 'Warum genau diese zehn — und nicht drei', '',
        P(
          'Schau dir die rechte Spalte noch einmal an. Da stehen <b>Linalool, Alpha-Pinen, Eugenol, Zimtaldehyd, 1,8-Cineol, Terpinen-4-ol, Carvacrol, Thymol, Limonen, Menthol, Gingerole, Anethol und Methylsalicylat.</b>',
          'Das sind <b>dreizehn verschiedene Wirkstoffklassen</b> in zehn Fläschchen. Jede greift an einer anderen Stelle an: an Rezeptoren, an Zellwänden von Keimen, an Entzündungsschaltern, an der Schleimproduktion, an Nervenenden.',
          'Genau das ist der Grund, warum ein Set mehr ist als die Summe seiner Teile: <b>Du deckst nicht ein Problem ab, sondern eine ganze Bandbreite.</b> Und du merkst erst beim Benutzen, welches davon deins wird.',
          'Für diese Woche brauchst du vor allem <b>On Guard, Air, Lavendel und Zitrone</b>. Die anderen sechs wirst du trotzdem benutzen — nur an Tagen, an denen es nicht um Erkältung geht.'
        )),
      oele('🛡️ Sicherheit — das Wichtigste in einem Block',
        'Immer verdünnen · Zitrusöle nicht vor die Sonne · heisse Öle mit Respekt',
        'Ein bis zwei Tropfen auf einen Teelöffel Trägeröl reichen völlig — Mandel-, Jojoba- oder Kokosöl. Nie in die Augen und nicht in die Ohren. Zitrusöle wie Zitrone und Bergamotte machen die Haut lichtempfindlich, also nach dem Auftragen einige Stunden nicht in die Sonne. Bei Schwangerschaft, Asthma, Epilepsie oder bei Säuglingen vorher mit der Ärztin sprechen.',
        '„Heisse" Öle sind Oregano, Zimt, Nelke und Thymian — stark verdünnen, nicht bei kleinen Kindern.'),
      block('12', 'Der botanische Name — nimm dein Fläschchen in die Hand', 'Ein Detail, das fast niemand beachtet, und das dir sofort sagt, was du da hast.',
        P(
          'Dreh dein Lavendel-Fläschchen um. Unter dem Namen steht <b><i>Lavandula angustifolia</i></b>. Das ist kein Zierrat, das ist die Auskunft darüber, welche Pflanze wirklich drin ist.',
          '<b>Warum das zählt:</b> Es gibt über vierzig Lavendelarten. <i>Lavandula angustifolia</i> ist der echte Lavendel — sanft, und der mit Abstand am besten untersuchte. Daneben gibt es <b>Lavandin</b>, eine Kreuzung aus echtem Lavendel und Speiklavendel. Lavandin ist deutlich ertragreicher und günstiger, riecht intensiver und enthält <b>mehr Kampfer</b>. Es wirkt dadurch anders — und ist nichts, was man einem kleinen Kind auf die Haut gibt.',
          'Steht auf einem Fläschchen nur „Lavendelöl", weisst du nicht, welches der beiden du gekauft hast. Und der Preisunterschied ist erheblich: Echter Lavendel kostet ein Mehrfaches von Lavandin.',
          '<b>Zwei Ausnahmen, damit du nicht stutzig wirst:</b> Bei <b>Mischungen</b> steht kein botanischer Name — in Air stecken sieben Pflanzen, da gibt es keinen einzelnen. Und beim <b>Weihrauch</b> steht nur <i>Boswellia</i> ohne Artnamen, weil dort mehrere Boswellia-Arten zusammenkommen. Beides ist korrekt so, kein Mangel.'
        )),
      irrtumBlock('13', 'Die vier häufigsten Irrtümer', [
        ['„Ich muss erst mal alles umstellen."',
         'Nein. Ein einziger Anker reicht. Wer diese Woche fünf Dinge gleichzeitig anfängt, macht in zwei Wochen wieder null. Wer eins anfängt, macht in zwei Wochen eins.'],
        ['„Mehr Tropfen wirken besser."',
         'Verdünnen ist keine Sparmassnahme und macht nichts schwächer. Ätherische Öle sind so konzentriert, dass unverdünnt vor allem die Haut reagiert — besonders bei Kindern.'],
        ['„Ätherische Öle sind einfach netter Duft."',
         'Das ist der grösste Irrtum überhaupt. In einem Fläschchen steckt die Abwehrchemie einer Pflanze — Moleküle, die an körpereigene Rezeptoren andocken, Entzündungsschalter beeinflussen und Zellwände von Keimen destabilisieren. Der Duft ist der Nebeneffekt, nicht der Mechanismus.'],
        ['„Öle statt der Basics."',
         'Andersrum. Erst Schlaf, Teller, Bewegung und Seife — dann die Öle als das, was die Routine trägt. Wer es umdreht, wundert sich, dass nichts passiert.'],
      ]),
      block('14', 'Die Zahlen für heute', '', kacheln([
        ['26 %', 'weniger Infekte der oberen Atemwege durch regelmässiges Händewaschen mit Seife.'],
        ['161 659', 'Menschen wurden dafür ausgewertet, über 26 Studien. Das ist eine sehr solide Grundlage.'],
        ['300+', 'Studien zeigen zusammengefasst: Dauerstress dämpft die Abwehr messbar. Das ist der Hebel, an dem ein Ritual ansetzt.'],
        ['32 %', 'mehr Sekretabfluss durch bestimmte Öl-Bestandteile — in Arzneimittel-Dosierung, nicht im Diffuser.'],
        ['20 Sek', 'braucht Seife, um zu wirken. Und genauso lang dauert die Morgenroutine mit dem Stick.'],
        ['44', 'randomisierte Studien mit über 3400 Menschen zeigen: Inhalation senkt Anspannung — messbar an Puls und Blutdruck.'],
        ['65–75 %', 'des Eucalyptus radiata sind 1,8-Cineol. Kein Spurenstoff — der Hauptbestandteil.'],
        ['13', 'verschiedene Wirkstoffklassen stecken in den zehn Basis-Ölen. Deshalb ein Set und nicht drei Fläschchen.'],
      ])),
      beiMir([
        'Das ist mein Lieblingsteil — die kleinen Rituale, genau wie im Reel: die zwanzig Sekunden am Morgen.',
        'Mein Favorit gerade ist der neue On Guard Stick mit Echinacea. Sekundenschnell aufgetragen, kein Verdünnen nötig, ideal für unterwegs und für die Schule. Es geht aber genauso mit On Guard verdünnt oder mit dem Stronger-Roller, der für die Kinder schon fertig verdünnt ist. On Guard ist die schützende Mischung aus Wilder Orange, Nelke, Zimt, Eukalyptus und Rosmarin — die steckt auch im Home Essentials Kit drin.',
        'Bei uns läuft das so: Schuhe an, Stick auf die Fusssohlen, Tür auf. Niemand muss daran denken, es gehört einfach dazu.',
      ]),
      oele('⭐ Immun-Roller (10 ml)',
        '3 Tropfen On Guard · 2 Tropfen Oregano · 3 Tropfen Lemon, aufgefüllt mit Trägeröl',
        'Morgens auf die Fusssohlen einreiben. Für unterwegs ist der fertige Stick praktischer, aber selbst gemischt ist er günstiger.',
        'Oregano ist ein „heisses" Öl — gut verdünnen und <b>nicht bei Kleinkindern</b> anwenden. Für die Kinder den On Guard Stick oder den Stronger-Roller nehmen.'),
      block('15', 'Was du heute tun kannst', 'Eins davon. Und dann sieben Tage lang dasselbe.', schritte([
        ['Wähl deinen Anker.', 'Nach dem Zähneputzen? Bevor der Kaffee läuft? Wenn du die Schuhe anziehst? Entscheide es jetzt, nicht morgen früh.'],
        ['Leg das Öl dorthin.', 'An den Anker, nicht ins Badezimmerregal. Was du nicht siehst, machst du nicht.'],
        ['Zwanzig Sekunden Hände waschen.', 'Mit Seife, und wirklich zwanzig. Einmal innerlich bis zwanzig zählen fühlt sich lang an — das ist der Punkt.'],
        ['Gib den Kindern ihr eigenes.', 'Ein eigener Stick oder ein eigener Diffuser macht aus deiner Regel ihre Sache.'],
      ])),
      quellen([
        ['Fachzeitschrift', 'enjoils — „Wie wirken ätherische Öle auf Zell- und Molekülebene? Die Chemie der Aromatherapie“ (Frühling 2025) und „Wissenschaftlich beleuchtete Pflanzenkraft“ (Winter 2025/26).'],
        ['Bücher', 'Maria L. Schasteen, „Duftmedizin“ und der Ratgeber „Erkältung“ · Eliane Zimmermann / Sabrina Herber, „Aromatherapie für Kinder“ · Monika Werner, „Praxis Aromatherapie“ · dazu mein eigenes Handbuch „Mama wird Hausapothekerin“.'],
        ['Produktangaben', 'dōTERRA Produktinformationsseiten (Stand 2023 bis 2026) zu Lavender, Tea Tree, Peppermint, Lemon, Oregano, Frankincense, On Guard, Air, ZenGest, Deep Blue und den Weihrauch Mikroperlen-Kapseln — nachzulesen auf media.doterra.com.'],
        ['Normen', 'ISO 4730 (Teebaumöl, Terpinen-4-ol-Typ) · ISO 3515 (Lavendelöl) · Europäisches Arzneibuch (Pfefferminzöl). Daher stammen die Prozentangaben zu den Inhaltsstoffen.'],
        ['Studien', 'Gertsch u.a., PNAS 2008 (Beta-Caryophyllen am CB2-Rezeptor) · Tan u.a., Frontiers in Public Health 2023 (44 kontrollierte Studien, 3419 Teilnehmende) · Samadi u.a. 2021 (Lavendel und Schlaf) · Segerstrom &amp; Miller, Psychological Bulletin 2004 (Stress und Immunsystem) · Pezantes-Orellana u.a., Frontiers in Medicine 2024 · Vora u.a., Journal of Ethnopharmacology 2024 · Metaanalyse zur Händehygiene über 26 Studien.'],
        ['Zum Schluss', 'Ätherische Öle sind Pflege und Vorsorge, kein Ersatz für ärztlichen Rat. Bei Fieber, Atemnot oder wenn es länger dauert, geh zur Ärztin.'],
      ]),
      merksatz('Nicht das perfekte Ritual gewinnt. Das gewinnt, das du auch am Donnerstag noch machst, wenn der Morgen schon schiefgegangen ist.'),
      morgen('Wenn es doch mal kommt — ruhig der Reihe nach.'),
    ],
  },

  {
    nr: 5, wochentag: 'Freitag', slug: 'tag5',
    titel: 'Wenn es doch mal kommt',
    unter: 'Ruhig der Reihe nach: was im Körper passiert, was in den ersten 24 Stunden zählt, welche Hausmittel wirklich etwas bringen — und woran du merkst, dass es kein Hausmittel mehr ist.',
    kern: 'Fieber ist nicht der Feind. Fieber ist die Feuerwehr.',
    body: [
      block('01', 'Was du spürst, ist nicht der Erreger', 'Erinnerst du dich an das Haus von Dienstag? Jetzt wird es wichtig.',
        P(
          'Fieber, Halsweh, Gliederschmerzen, Müdigkeit — das ist nicht der Virus, der dir wehtut. <b>Das ist deine eigene Feuerwehr bei der Arbeit.</b> Dein Körper fährt die Temperatur hoch, weil viele Erreger sich bei Wärme schlechter vermehren und deine Abwehrzellen dabei schneller arbeiten.',
          'Auch die Müdigkeit hat einen Grund. Eine Immunantwort ist <b>teuer</b>. Dein Körper zieht die Energie von überall ab, wo sie gerade nicht gebraucht wird — und sagt dir damit sehr deutlich, was er jetzt will.',
          'Das ändert die ganze Haltung: Ruhe ist nicht das, was übrig bleibt, wenn nichts anderes hilft. <b>Ruhe ist die Behandlung.</b>'
        )),
      block('02', 'Und jetzt das Wichtigste: Krank sein ist nicht schlimm', 'Bevor wir über Öle reden, über Wickel und über Zink — dieser Satz gehört an den Anfang.',
        P(
          'Eine ganze Woche lang ging es hier darum, wie du dein Immunsystem stark hältst. Da entsteht schnell der Eindruck, ein Infekt sei ein Versagen. Als hättest du etwas falsch gemacht, wenn dein Kind im November trotzdem mit einer Rotznase heimkommt.',
          '<b>Genau umgekehrt.</b> Ein Infekt ist der Moment, in dem das ganze System einmal zeigt, was es kann. Es lernt dabei — jede überstandene Erkältung hinterlässt Gedächtniszellen, die beim nächsten Mal schneller da sind. Kinder machen in den ersten Lebensjahren sechs bis zwölf Infekte pro Jahr durch, und das ist keine Panne, das ist der Lehrplan.',
          'Was ich mit dieser Woche meine, ist deshalb etwas anderes: Ein gut versorgter Körper wird nicht seltener krank, weil er unverwundbar wäre. Er wird <b>schneller wieder gesund</b>, und er kommt mit weniger Wucht durch die Sache. Das ist das realistische Versprechen, und es ist ein gutes.',
          'Also: kein schlechtes Gewissen, wenn es einen erwischt. <b>Die Frage ist nie, ob du krank wirst. Die Frage ist, wie du damit umgehst.</b>'
        )),
      block('03', 'Halsweh — Symptom oder Ursache?', 'Diese Frage kommt oft, und die Antwort ist genauer, als man denkt.',
        P(
          'Halsweh ist ein <b>Symptom</b>, das stimmt. Aber die genaue Antwort ist noch interessanter — und sie passt zu allem, was du gerade gelesen hast.',
          'Rund <b>80 Prozent</b> aller akuten Halsschmerzen kommen von einem Virus, nur etwa 15 bis 30 Prozent von Bakterien. Das ist aber noch nicht der Punkt. Der Punkt ist: <b>Der Schmerz selbst kommt nicht vom Erreger.</b>',
          'Wenn Zellen in deiner Rachenschleimhaut angegriffen werden, schüttet dein Körper Entzündungsbotenstoffe aus — vor allem Prostaglandine und Bradykinin. Und diese Stoffe machen die Nervenenden in deinem Hals <b>überempfindlich</b>. Deshalb tut plötzlich schon das Schlucken von Speichel weh, was du sonst tausendmal am Tag machst, ohne es zu merken.',
          'Also: <b>Das Halsweh ist die Feuerwehr, nicht das Feuer.</b> Genau wie das Fieber. Und daraus folgt etwas sehr Praktisches — du hast zwei Möglichkeiten, damit umzugehen.'
        )),
      block('04', 'Zwei Wege, mit Beschwerden umzugehen', 'Beide sind legitim. Sie machen nur etwas ganz Verschiedenes, und das sollte man wissen.',
        vergleich(['Der Weg', 'Wie er wirkt', 'Was das bedeutet'], [
          ['<b>Abschalten</b><br><span style="font-weight:400;color:#63747b">betäubende Lutschtablette, Schmerzmittel</span>',
           'Unterbricht die Weiterleitung im Nerv oder blockiert die Botenstoffe, die den Schmerz machen. Du merkst weniger.',
           'Schnell und stark — dafür arbeiten Magen, Leber und Nieren mit, und du spürst nicht mehr, wie es dir tatsächlich geht.'],
          ['<b>Mitarbeiten</b><br><span style="font-weight:400;color:#63747b">Cineol aus Eukalyptus, Honig, Wärme, Ruhe</span>',
           'Unterstützt genau das, was dein Körper ohnehin tut: Sekret abtransportieren, Schleimhaut beruhigen, Entzündung regulieren, zur Ruhe kommen.',
           'Sanfter und langsamer — dafür arbeitest du <b>mit</b> deinem Körper statt gegen sein Signal, und du bleibst im Kontakt damit, wie es dir geht.'],
        ])),
      block('05', 'Warum ich lieber mitarbeite', 'Das ist meine Haltung — und sie hat Gründe, keine Ideologie.',
        P(
          '<b>Erstens: Cineol treibt an, was dein Körper ohnehin macht.</b> Deine Atemwege reinigen sich selbst, über die Flimmerhärchen und das Sekret. Genau dort setzt Cineol an — es macht den Schleim dünner und die Härchen schneller. Das ist keine Unterdrückung, das ist Rückenwind für einen Vorgang, der sowieso läuft.',
          '<b>Zweitens: Die Terpene greifen an derselben Stelle an wie ein Entzündungshemmer</b> — bei den Botenstoffen, die deine Nerven überempfindlich machen. Beta-Caryophyllen über die CB2-Rezeptoren, Weihrauch über den NF-κB-Schalter. Sanfter, ja. Aber ohne die Belastung für Magen und Nieren, die ein Schmerzmittel mit sich bringt.',
          '<b>Drittens: Ein Öl kann mehreres gleichzeitig.</b> Ein Medikament ist ein Wirkstoff für eine Aufgabe. In Air stecken acht Öle mit mehreren Wirkstoffklassen — schleimlösend, beruhigend, antimikrobiell, öffnend. Das ist Breite statt Präzision, und bei einer Erkältung, die auf vielen Ebenen gleichzeitig nervt, ist Breite oft genau das Richtige.',
          '<b>Viertens, und für mich das Wichtigste: Du schläfst besser.</b> Wer nachts wegen Husten wach liegt, nimmt sich genau das weg, was seine Abwehr am dringendsten braucht. Ein Öl, das dich durchschlafen lässt, arbeitet an der Stelle, die zählt.',
          'Und damit das klar ist: Es gibt Situationen, in denen ein Medikament das Richtige ist. Welche das sind, steht weiter hinten bei den Warnzeichen — darüber entscheidest du nicht mit einem Fläschchen, sondern mit einem Anruf.'
        )),
      block('06', 'Was die Öle im Infekt tatsächlich tun', 'Jetzt wird die Chemie von gestern konkret — denn im Infekt setzen die Öle an einer ganz anderen Stelle an als bei der Vorsorge.',
        P(
          '<b>Sie machen den Schleim dünner und die Flimmerhärchen schneller.</b> Das ist der stärkste Effekt und der am besten untersuchte. <b>Eucalyptus radiata besteht typischerweise zu 65 bis 75 Prozent aus 1,8-Cineol</b> — das ist kein Spurenstoff, das ist der Hauptbestandteil. Cineol verflüssigt festsitzendes Sekret und lässt die Flimmerhärchen schneller schlagen.',
          'Und jetzt schliesst sich der Kreis zu Mittwoch: Genau diese Härchen legt trockene Heizungsluft lahm. Was am Mittwoch das Problem war, wird hier wieder in Gang gebracht.',
          '<b>Sie dämpfen die Entzündung, die den Schmerz macht.</b> Erinnerst du dich an die Botenstoffe, die deine Nerven im Hals überempfindlich machen? Genau da greifen die Terpene ein. <b>Beta-Caryophyllen</b> aus Copaiba fährt über die CB2-Rezeptoren entzündungsfördernde Zytokine herunter, <b>Weihrauch</b> hemmt den NF-κB-Schalter. Das ist derselbe Angriffspunkt wie bei einem Entzündungshemmer — nur sanfter und schwächer.',
          '<b>Sie senken die Keimlast dort, wo du sie hinbringst.</b> Das ist gut untersucht: Pfefferminzöl zeigt Wirkung selbst gegen Keime, die auf Antibiotika nicht mehr ansprechen, und Zitronenöl gilt seit den Arbeiten von Dr. Valnet als starkes Antiseptikum. Praktisch heisst das: auf der Haut, als Gurgelwasser, in der Raumluft, auf Türklinken und Griffen — überall dort, wo das Öl wirklich hinkommt.',
          '<b>Und sie machen es erträglich.</b> Das klingt nach wenig und ist es nicht. Wer nachts wegen Husten nicht schläft, verlängert seinen Infekt — weil genau der Schlaf fehlt, den die Abwehr braucht. Ein Öl, das dich schlafen lässt, arbeitet also indirekt an der Ursache.'
        )),
      block('07', 'Die ersten 24 Stunden — das kleine Zeitfenster', 'Hier entscheidet sich mehr als in den drei Tagen danach. Und genau hier mache ich selbst am meisten.',
        P(
          'Du kennst dieses Gefühl: ein Kratzen im Hals, dieses leicht flaue Ziehen, und du weisst einfach, dass da was kommt. <b>Das ist der Moment, in dem gehandelt wird</b>, nicht übermorgen, wenn es dich schon flachgelegt hat.',
          '<b>Zink wirkt nur in diesem Fenster.</b> Eine Auswertung von 26 Studien mit 2375 Personen fand: Die Erkältung wird etwa einen Tag kürzer — aber ausdrücklich nur, wenn innerhalb der <b>ersten 24 Stunden</b> begonnen wird. Wer erst am dritten Tag anfängt, kann es sich sparen. Das macht aus einer mittelmässigen Zahl einen sehr klaren Handlungsauftrag.',
          '<b>Vitamin C</b> verkürzt eine Erkältung um rund acht Prozent — von sieben Tagen also etwa einen halben. Vorbeugen tut es nicht, und die Brausetablette nach Ausbruch ist auch keine Rettung. Zusammen mit dem Zink und im richtigen Moment genommen, ist es trotzdem ein sinnvoller Baustein.',
          '<b>Dazu die Kapsel.</b> Für „heisse" Öle wie Oregano und On Guard gibt es die Leerkapsel — Öle hinein, mit Trägeröl auffüllen, schlucken. So gehen sie durch, ohne Mund und Speiseröhre zu reizen. Das ist meine Standardantwort auf das erste Kratzen.',
          'Und das Unspektakulärste zuerst: <b>an dem Abend früher ins Bett.</b> Was du hier an Schlaf hineinsteckst, holst du dir später als Tage zurück.'
        )),
      block('08', 'Warum der Diffuser mehr ist als Duft', 'Das ist bei mir das Gerät, das am meisten läuft — und dafür gibt es vier ziemlich handfeste Gründe.',
        P(
          '<b>Erstens: Er macht die Luft feucht.</b> Ein Ultraschall-Diffuser vernebelt vor allem Wasser. Genau das brauchen deine Schleimhäute, damit der Sekretfilm flüssig bleibt und die Flimmerhärchen überhaupt arbeiten können. Trockene Heizungsluft legt sie lahm — und sie stehen bei einem Infekt sowieso schon unter Druck.',
          '<b>Zweitens: Der Weg ist kürzer als bei allem anderen.</b> Was du einatmest, kommt als feiner Nebel direkt in die Nase, in den Rachen, in die Bronchien — dorthin, wo es kratzt und sitzt. Keine Verdauung dazwischen, kein Umweg über die Leber.',
          '<b>Drittens: Er nimmt Keime aus der Raumluft.</b> Wenn eines der Kinder krank im Bett liegt und die anderen im selben Zimmer schlafen, ist das der Unterschied. Verneblete ätherische Öle senken die Keimlast in der Luft — dazu gibt es Untersuchungen, und es ist auch die Anwendung, die am wenigsten Aufwand macht.',
          '<b>Viertens: Er läuft, während alle schlafen.</b> Das ist der Punkt, den ich am meisten schätze. Ein Wickel braucht deine Hände, ein Roller braucht einen wachen Moment — der Diffuser macht seine Arbeit die ganze Nacht, ohne dass jemand aufstehen muss. Und über den Geruchssinn geht es zusätzlich direkt ins limbische System, also dorthin, wo Anspannung sitzt.',
          '<b>Was bei mir hineinkommt:</b> Air, wenn Nasen laufen und gehustet wird. On Guard, wenn etwas im Anmarsch ist oder eines krank ist und die anderen es nicht kriegen sollen. Lavendel, wenn Unruhe das grössere Problem ist als der Husten. Fünf bis sechs Tropfen, mit Wasser bis zur Fülllinie.'
        )),
      oele('🫁 Air für die Atemwege',
        'Fünf bis sechs Tropfen in den Diffuser, oder verdünnt auf Brust und Rücken',
        'Am besten abends, wenn der Husten sonst den Schlaf stört. Für ganz kleine Kinder nimmst du stattdessen Lavendel in Kokosöl.'),
      block('09', 'Die Hausmittel von früher — mit Öl darin', 'Wickel, Bad, Kompresse: Das hat schon deine Grossmutter gemacht. Die Öle machen es stärker, nicht anders.',
        vergleich(['Was', 'Wie', 'Wofür'], [
          ['<b>Brustwickel</b>', 'Zitrone und On Guard gut verdünnt, warmes Tuch auf die Brust, ein trockenes darüber, 20 bis 30 Minuten.', 'Unterstützt die Atemwege. Wärme und Dampf arbeiten zusammen.'],
          ['<b>Zwiebelsäckchen</b>', 'Gehackte Zwiebel kurz erwärmt in ein Tuch, mit On Guard verdünnt dazu, auf die Brust.', 'Bei zähem Husten. Das alte Hausmittel, verstärkt.'],
          ['<b>Brustbalsam</b>', 'Air in Kokosöl. Bei ganz kleinen Kindern stattdessen Lavendel in Kokosöl.', 'Löst den Husten, beruhigt, erleichtert das Atmen.'],
          ['<b>Wadenwickel</b>', '3 bis 5 Tropfen in einen Liter kühles Wasser, Tücher darin tränken, um die Waden. <b>Nur bei warmen Füssen</b> — bei Schüttelfrost oder kalten Beinen niemals.', 'Bei hohem Fieber, wenn der Leidensdruck gross ist.'],
          ['<b>Dampf-Inhalation</b>', 'Ein bis zwei Tropfen in eine Schüssel mit warmem Wasser, Handtuch über den Kopf, Augen zu. <b>Nicht bei kleinen Kindern</b> — Verbrühungsgefahr.', 'Bei verstopfter Nase und Nebenhöhlen.'],
          ['<b>Gurgeln</b>', 'Ein Tropfen On Guard oder Teebaum in warmem Wasser, gurgeln, ausspucken. Morgens und abends.', 'Bei Halskratzen, direkt dort, wo es wehtut.'],
        ])),
      block('10', 'Das Rücken-Protokoll — mein Ritual bei kranken Kindern', 'Vier Fläschchen, fünf Minuten, und danach wird geschlafen. Das ist das, was ich am meisten mache.',
        P(
          'Die Methode kommt aus <b>Symphony of the Cells</b>, kurz SOC. Dahinter steckt eine einfache Idee: Die Öle kommen in einer festgelegten Reihenfolge auf den Rücken, entlang der Wirbelsäule, wo sehr viele Nervenbahnen zusammenlaufen. Du musst dabei nicht massieren, verteilen reicht.',
          '<b>Das Basis-Protokoll, so wie ich es mache:</b>'
        ) + schritte([
          ['Trägeröl grosszügig auf den ganzen Rücken.', 'Fraktioniertes Kokosöl. Grosszügig heisst wirklich grosszügig — das ist die Grundlage, auf der alles andere verteilt wird.'],
          ['Weihrauch, 2 bis 3 Tropfen.', 'Auf den Rücken geben und verteilen. Den Rest, der an der Hand bleibt, auf die Fusssohlen streichen.'],
          ['Teebaum, 2 bis 3 Tropfen.', 'Gleiches Vorgehen. Erst verteilen, dann der Rest an die Füsse, bevor das nächste Öl kommt.'],
          ['Lavendel, 2 bis 3 Tropfen.', 'Zum Schluss. Danach Pyjama an, Decke drüber, Licht aus.'],
        ]) + P(
          'Das Protokoll ist <b>schon für die Kleinsten geeignet</b> und wird bei Erkältung, Fieber, Grippe, Halsschmerzen, Kopf- und Ohrenschmerzen, Pseudokrupp und zur Immunstärkung eingesetzt.',
          'Bei uns ist der verlässlichste Teil daran der <b>Schlaf</b>. Nach dem Protokoll schlafen meine Kinder tief und durch — und am nächsten Morgen ist es meistens schon deutlich weniger schlimm. Manchmal eben doch nicht, dann geht es halt seinen Weg. Wie viel davon die Öle sind und wie viel die zehn Minuten Ruhe und Berührung, kann ich dir ehrlich nicht sagen. Bei einem kranken Kind ist mir das auch herzlich egal.'
        )),
      block('11', 'Beschwerde für Beschwerde', 'Damit du im Ernstfall nicht überlegen musst. Alles verdünnt, alles aus dem Starterset.',
        vergleich(['Wo es zwickt', 'Welches Öl', 'Wie'], [
          ['<b>Kopfschmerzen</b>', 'Pfefferminze, Lavendel, Weihrauch', 'Verdünnt auf Schläfen und Nacken, nicht zu nah an die Augen. Dazu eine kühle Kompresse auf die Stirn und viel trinken.'],
          ['<b>Schnupfen, verstopfte Nase</b>', 'Air, Pfefferminze, Zitrone', 'In den Diffuser oder trocken inhalieren. Air auf den Nasenrücken und die Nebenhöhlen, verdünnt.'],
          ['<b>Halskratzen</b>', 'Teebaum, Zitrone, On Guard, Oregano', 'Ein Tropfen auf einen Teelöffel Honig, langsam lutschen. Oder gurgeln. Oder verdünnt aussen an den Hals.'],
          ['<b>Husten</b>', 'Air, Pfefferminze', 'Diffuser am Abend, Brustbalsam vor dem Schlafen. In den Händen verreiben und tief einatmen geht immer und überall.'],
          ['<b>Ohrenschmerzen</b>', 'Teebaum, Lavendel', 'Verdünnt <b>um</b> das Ohr herum und hinter dem Ohr den Hals hinunter. <b>Niemals in den Gehörgang.</b> Dazu ein warmes Körnerkissen.'],
          ['<b>Fieber</b>', 'Pfefferminze, Zitrone', 'Verdünnt auf die Fusssohlen oder entlang der Wirbelsäule. Oder ein paar Tropfen in kühles Wasser und damit Stirn, Nacken und Füsse kühlen.'],
        ])),
      block('12', 'Was nicht geht', 'Kurz und unmissverständlich, weil hier tatsächlich etwas passieren kann.',
        P(
          '<b>Nichts ins Ohr.</b> Kein Öl in den Gehörgang, auch nicht verdünnt, auch nicht auf Watte. Aussen herum ja, hinein nein.',
          '<b>Nichts unverdünnt auf Schleimhäute.</b> Nicht in die Nase, nicht pur auf den Rachen, nicht in die Augen. Falls doch etwas ins Auge kommt: mit Pflanzenöl auswischen, nie mit Wasser — Wasser verteilt es nur.',
          '<b>Kein Menthol und kein Kampfer bei Säuglingen und Kleinkindern</b>, vor allem nicht im Gesicht oder unter der Nase. Das kann bei kleinen Kindern zu Atemproblemen führen. Deshalb steht in den Kinder-Empfehlungen überall Lavendel statt Pfefferminze.',
          '<b>Oregano ist ein heisses Öl.</b> Immer gut verdünnen, nie bei Kleinkindern auf die Haut, und in der Kapsel mit Trägeröl. Für Kinder gibt es den On Guard Stick.',
          'Und generell: <b>weniger und dafür öfter</b>, lieber stärker verdünnt auf grösserer Fläche. Das ist die Regel, mit der du fast nichts falsch machen kannst.'
        )),
      block('13', 'Was tatsächlich hilft — ehrlich sortiert', 'Von gut belegt nach schwach belegt. Ich lasse nichts weg, aber ich sage dazu, wie sicher es ist.',
        P(
          '<b>Honig bei Husten.</b> Das am besten belegte Hausmittel überhaupt. Eine grosse Übersichtsarbeit zeigt: Honig lindert Häufigkeit und Stärke der Hustenanfälle bei Kindern und verbessert den Schlaf — besser als keine Behandlung, und ähnlich gut wie manche rezeptfreien Hustensäfte. Ein Teelöffel, langsam gelutscht. <b>Aber erst ab einem Jahr</b>, für Säuglinge ist Honig gefährlich.',
          '<b>Zink in den ersten 24 Stunden.</b> Rund einen Tag kürzer, siehe oben. Die Forschenden selbst stufen die Sicherheit dieser Aussage als niedrig ein — einen Versuch wert, kein Wunder.',
          '<b>Feuchte Luft und Trinken.</b> Klingt banal, ist aber genau das, was deine Flimmerhärchen und deine Schleimhäute brauchen, um den Erreger wieder hinauszubefördern.',
          '<b>Öle im Diffuser und auf der Haut.</b> Für die schleimlösende Wirkung von Cineol gibt es gute Belege, für die entzündungsdämpfende Wirkung der Terpene ebenfalls. Für den Rücken-Ablauf mit Weihrauch, Teebaum und Lavendel gibt es keine Studie — das ist Erfahrungswissen, und ich sage das auch so.',
          '<b>Ruhe.</b> Das Mittel ohne Nebenwirkung, ohne Kosten und mit der besten Datenlage. Und trotzdem das, was am seltensten genommen wird.'
        )),
      block('14', 'Woran du merkst, dass es kein Hausmittel mehr ist', 'Der wichtigste Abschnitt dieser Woche. Nicht zum Ängstigen, sondern zum Einordnen.',
        P(
          'Die allermeisten Erkältungen sind nach sieben bis zehn Tagen vorbei und brauchen nichts ausser Geduld. Es gibt aber Punkte, an denen du nicht mehr selbst herumprobierst, sondern anrufst:',
          '<b>Atemnot oder schnelle, angestrengte Atmung.</b> Immer.<br><b>Hohes Fieber, das mehrere Tage nicht runtergeht</b> — oder Fieber bei einem Säugling.<br><b>Es wird besser und dann plötzlich wieder deutlich schlechter.</b> Das ist ein klassisches Warnzeichen.<br><b>Steifer Nacken, starke Kopfschmerzen, Verwirrtheit.</b><br><b>Ein Kind, das nicht mehr trinkt</b> oder auffällig teilnahmslos wird.',
          '<b>Und speziell beim Hals:</b> starke Schmerzen nur auf einer Seite · Beläge auf den Mandeln zusammen mit hohem Fieber und geschwollenen Lymphknoten, aber <b>ohne</b> Husten · wenn Schlucken kaum mehr möglich ist oder Speichel aus dem Mund läuft. Das erste ist der typische Hinweis auf eine bakterielle Angina — und die gehört abgeklärt, nicht mit Honig behandelt.',
          'Und ganz grundsätzlich: Du kennst dein Kind und dich selbst. Wenn dein Gefühl sagt, dass etwas anders ist als sonst, dann ist das ein guter Grund anzurufen — auch wenn nichts auf dieser Liste steht.'
        )),
      irrtumBlock('15', 'Die vier häufigsten Irrtümer', [
        ['„Ich muss das wegdrücken, damit ich funktioniere."',
         'Das ist der verbreitetste Reflex — und er kostet dich meistens Tage. Die Müdigkeit im Infekt ist kein Störsignal, sondern eine Aufforderung. Wer sie zweimal überhört, liegt am Ende länger flach als die, die einen Nachmittag früher aufgehört hat.'],
        ['„Fieber muss sofort runter."',
         'Fieber ist Teil der Abwehr, nicht die Krankheit. Man senkt es, wenn der Leidensdruck gross ist oder das Kind nicht mehr trinkt — nicht wegen der Zahl auf dem Thermometer. Im Zweifel bei der Kinderärztin nachfragen.'],
        ['„Ein Antibiotikum hilft schneller."',
         'Eine Erkältung wird von Viren ausgelöst. Antibiotika wirken gegen Bakterien und richten hier nichts aus, ausser dass sie deiner Darmflora schaden — genau der, um die es am Montag ging.'],
        ['„Richtig schwitzen kuriert es aus."',
         'Schwitzen bringt den Erreger nicht heraus. Was hilft, ist unspektakulärer: trinken, ruhen, feuchte Luft.'],
      ]),
      block('16', 'Die Zahlen für heute', '', kacheln([
        ['24 Std', 'hast du Zeit, damit Zink noch etwas bringt. Danach kannst du es dir sparen.'],
        ['80 %', 'aller akuten Halsschmerzen kommen von einem Virus. Ein Antibiotikum richtet dort nichts aus.'],
        ['7–10', 'Tage dauert eine normale Erkältung. Geduld ist meistens die ganze Behandlung.'],
        ['6–12', 'Infekte pro Jahr sind bei kleinen Kindern normal. Das ist kein Versagen, das ist der Lehrplan.'],
        ['ab 1 Jahr', 'darf Honig gegeben werden. Für Säuglinge ist er gefährlich — ein echtes Risiko, keine Vorsichtsregel.'],
        ['65–75 %', 'des Eucalyptus radiata sind 1,8-Cineol — der Stoff, der Sekret löst und die Flimmerhärchen antreibt.'],
        ['8', 'Öle stecken in Air — Lorbeer, Eukalyptus, Pfefferminze, Teebaum, Zitrone, Kardamom, Kampferbaum und Ravensara.'],
      ])),
      beiMir([
        'Wenn ich merke, dass etwas kommt, mache ich es noch am selben Tag: Vitamin C und Zink, eine Kapsel mit On Guard und Oregano, und abends früher ins Bett. Dieses Zeitfenster lasse ich nicht verstreichen.',
        'Der Diffuser läuft bei uns die halbe Erkältungszeit. Air, wenn Nasen laufen und gehustet wird. On Guard, wenn etwas im Anmarsch ist oder eines krank ist und die anderen es nicht kriegen sollen. Und wenn Unruhe das grössere Thema ist als der Husten, dann Lavendel.',
        'Bei kranken Kindern mache ich das Rücken-Protokoll: Trägeröl, Weihrauch, Teebaum, Lavendel. Danach schlafen sie tief und durch, und am nächsten Morgen ist es meistens schon weniger schlimm. Und wenn doch nicht, dann ist das auch in Ordnung.',
      ]),
      block('17', 'Was du heute tun kannst', '', schritte([
        ['Leg deine Herbst-Basis griffbereit.', 'An einen Ort, den du im Halbschlaf findest. Nicht ganz hinten im Schrank.'],
        ['Stell den Diffuser dorthin, wo geschlafen wird.', 'Nicht ins Wohnzimmer, wo er tagsüber hübsch aussieht. Er soll nachts arbeiten.'],
        ['Kauf ein Glas guten Honig und leg Zink bereit.', 'Damit du beim ersten Kratzen nicht erst einkaufen gehen musst — dann ist das Fenster nämlich schon halb zu.'],
        ['Merk dir die Warnzeichen.', 'Atemnot, Fieber beim Säugling, Verschlechterung nach Besserung. Der Rest ist meistens Geduld.'],
        ['Und nimm dir vor, beim nächsten Mal wirklich zu ruhen.', 'Ruhe ist die Behandlung, nicht die Belohnung fürs Durchhalten.'],
      ])),
      `<div style="display:flex;flex-direction:column;gap:7mm">` +
      merksatz('Du musst eine Erkältung nicht bekämpfen. Du musst deinem Körper die Bedingungen geben, unter denen er sie selbst erledigt.') +
      `<div class="abschluss">
        <span class="label">Das war die Woche</span>
        <p>Alles, was ich dir diese Woche gezeigt habe, startet mit einer Handvoll Basis-Öle — genau die stecken im Home Essentials Kit. Wenn du wirklich starten willst, mache ich das nicht als Warenkorb: Du bekommst dein Kit, meinen einseitigen Routine-Plan und mich ein paar Wochen an deiner Seite. Ich nehme diese Runde nur eine Handvoll Frauen. Magst du dabei sein? Schreib mir. 🤍</p>
        <p class="danke">Danke, dass du dabei warst. — Patricia</p>
      </div></div>`,
    ],
  },
];

// ---------------------------------------------------------------- Layout

const CSS = `
@page { size: A4; margin: 0; }

:root {
  --creme:#f1ecdd; --papier:#faf7ef; --petrol:#12828c; --tief:#29556d;
  --orange:#dc822e; --rost:#a8432a; --tinte:#1d3742; --leise:#63747b; --linie:#d6cdb6;
}
* { box-sizing:border-box; margin:0; padding:0; }
html { background:var(--creme); -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body { font-family:"Source Sans 3",system-ui,sans-serif; color:var(--tinte); background:var(--creme);
       font-size:11pt; line-height:1.58; }

h1,h2,h3 { font-family:Philosopher,Georgia,serif; font-weight:700; line-height:1.15; }

/* Jede Seite ist ein eigener, randlos beiger Kasten — dadurch kein weisser Rand. */
.seite {
  width:210mm; min-height:297mm; padding:17mm 18mm 13mm;
  background:var(--creme); page-break-after:always;
  display:flex; flex-direction:column; gap:7mm;
}
.seite:last-child { page-break-after:auto; }

.seitenfuss {
  margin-top:auto; padding-top:5mm; border-top:.5pt solid var(--linie);
  font-size:8.6pt; color:var(--leise); display:flex; justify-content:space-between; gap:6mm;
}
.seitenfuss b { color:var(--petrol); font-weight:700; }

.titel { border-bottom:2.5pt solid var(--petrol); padding-bottom:4mm; page-break-after:avoid; }
.eyebrow { font-size:8.5pt; letter-spacing:.18em; text-transform:uppercase; font-weight:700;
           color:var(--petrol); display:block; margin-bottom:2.5mm; }
h1 { font-size:26pt; margin-bottom:2.5mm; }
.unterzeile { font-size:11.4pt; color:var(--leise); max-width:140mm; }

.kernsatz { background:var(--petrol); color:#f7f4ec; padding:6mm 7mm; border-radius:1.5mm;
            page-break-inside:avoid; }
.kernsatz p { font-family:Philosopher,Georgia,serif; font-size:15.5pt; line-height:1.3; }

.block { display:flex; flex-direction:column; gap:3.6mm; page-break-inside:avoid; }
h2 { font-size:17.5pt; color:var(--tief); display:flex; align-items:baseline; gap:3mm;
     page-break-after:avoid; margin-bottom:1mm; }
h2 .nr { font-size:10pt; color:var(--orange); font-family:"Source Sans 3",sans-serif; font-weight:700; }
.block p { max-width:none; }
.intro { color:var(--leise); font-size:10.8pt; }
b, strong { font-weight:600; color:var(--tief); }

.zahlen { display:grid; grid-template-columns:1fr 1fr; gap:3.5mm; }
.zahl-kachel { background:var(--papier); border-left:2.5pt solid var(--orange); border-radius:1mm;
               padding:4mm 4.5mm; page-break-inside:avoid; display:flex; flex-direction:column; gap:1mm; }
.zahl-kachel b { font-family:Philosopher,Georgia,serif; font-size:19pt; color:var(--tief); line-height:1; }
.zahl-kachel span { font-size:10pt; line-height:1.48; }

.irrtum { display:grid; grid-template-columns:1fr 1fr; gap:0 6mm; padding:3.4mm 0;
          border-bottom:.5pt solid var(--linie); page-break-inside:avoid; }
.irrtum:first-of-type { border-top:.5pt solid var(--linie); }
.irrtum + .block { margin-top:6.5mm; }
.irrtum .falsch, .irrtum .richtig { display:flex; flex-direction:column; gap:1.5mm; }
.irrtum .kopf { font-size:8.5pt; letter-spacing:.09em; text-transform:uppercase; font-weight:700; }
.irrtum .falsch .kopf { color:var(--rost); }
.irrtum .richtig .kopf { color:var(--petrol); }
.irrtum p { font-size:10.2pt; line-height:1.5; }

.schritte { display:flex; flex-direction:column; }
.schritt { display:grid; grid-template-columns:9mm 1fr; gap:3mm; padding:3.2mm 0;
           border-bottom:.5pt solid var(--linie); align-items:baseline; page-break-inside:avoid; }
.schritt:first-of-type { border-top:.5pt solid var(--linie); }
.schritt .haken { color:var(--orange); font-size:13pt; font-weight:700; }
.schritt b { font-size:11pt; font-weight:600; display:block; margin-bottom:.8mm; color:var(--tinte); }
.schritt span { font-size:10.2pt; color:var(--leise); line-height:1.5; }

.merksatz { background:var(--papier); border:.5pt solid var(--petrol); border-left:3pt solid var(--petrol);
            border-radius:1mm; padding:5.5mm 6mm; page-break-inside:avoid; }
.merksatz p { font-family:Philosopher,Georgia,serif; font-size:13pt; line-height:1.35; color:var(--tief); }

.beimir { background:var(--papier); border:.5pt solid var(--linie); border-top:2pt solid var(--tief);
          border-radius:1mm; padding:5.5mm 6mm; page-break-inside:avoid;
          display:flex; flex-direction:column; gap:2.8mm; }
.beimir .label { font-size:8.5pt; letter-spacing:.1em; text-transform:uppercase; font-weight:700; color:var(--tief); }
.beimir p { font-size:10.7pt; line-height:1.56; }

.oele { background:var(--papier); border:.5pt solid var(--petrol); border-radius:1mm;
        padding:5.5mm 6mm; page-break-inside:avoid;
        display:flex; flex-direction:column; gap:2.8mm; }
.oele .label { font-family:Philosopher,Georgia,serif; font-size:13pt; color:var(--petrol); }
.oele .rezept { font-weight:600; color:var(--tief); font-size:11pt; }
.oele p { font-size:10.5pt; line-height:1.55; }
.oele .warnung { color:var(--rost); font-size:9.8pt; border-top:.5pt dotted var(--linie); padding-top:2.5mm; }
.oele .warnung b { color:var(--rost); }

.tab-huelle { border:.5pt solid var(--linie); border-radius:1mm; overflow:hidden; page-break-inside:avoid; }
table.vergleich { border-collapse:collapse; width:100%; background:var(--papier); }
table.vergleich th { text-align:left; font-size:8.5pt; letter-spacing:.08em; text-transform:uppercase;
                     font-weight:700; color:var(--leise); padding:3.5mm 4mm; background:var(--creme);
                     border-bottom:.5pt solid var(--linie); }
table.vergleich td { padding:3.8mm 4.2mm; border-bottom:.5pt solid var(--linie); font-size:10.2pt;
                     line-height:1.5; vertical-align:top; }
table.vergleich tr:last-child td { border-bottom:none; }
table.vergleich td.mittel { font-weight:600; color:var(--tief); width:31%; }

.quellenblock { background:var(--papier); border:.5pt solid var(--linie); border-left:2.5pt solid var(--tief);
  border-radius:1mm; padding:5mm 5.5mm; page-break-inside:avoid; display:flex; flex-direction:column; gap:2.4mm; }
.quellenblock .label { font-family:'IBM Plex Mono',monospace; font-size:8pt; letter-spacing:.12em;
  text-transform:uppercase; font-weight:600; color:var(--tief); }
.quellenblock p { font-size:9.2pt; line-height:1.45; color:var(--leise); }
.quellenblock .gruppe { font-weight:700; color:var(--tief); }

.morgen { border-top:.5pt solid var(--linie); padding-top:4mm; font-size:10.4pt; color:var(--leise);
          page-break-inside:avoid; }
.morgen span { font-family:Philosopher,Georgia,serif; color:var(--orange); font-size:12pt; margin-right:2mm; }

.abschluss { background:var(--petrol); color:#f7f4ec; border-radius:1.5mm; padding:6mm 6.5mm;
             page-break-inside:avoid; display:flex; flex-direction:column; gap:3mm; }
.abschluss .label { font-size:8.5pt; letter-spacing:.12em; text-transform:uppercase; font-weight:700; opacity:.75; }
.abschluss p { font-size:10.8pt; line-height:1.55; }
.abschluss .danke { font-family:Philosopher,Georgia,serif; font-size:13pt; opacity:.9; }
`;

const titelHtml = t => `<div class="titel">
    <span class="eyebrow">Immunwoche · Tag ${t.nr} von 5 · ${t.wochentag}</span>
    <h1>${t.titel}</h1>
    <p class="unterzeile">${t.unter}</p>
  </div>`;

const bausteine = t => [titelHtml(t), `<div class="kernsatz"><p>${t.kern}</p></div>`, ...t.body];

const seitenfuss = (n, von) =>
  `<div class="seitenfuss"><span>Immunwoche · ${von}</span>` +
  `<span><b>Mum Life Balance</b> · Seite ${n}</span></div>`;

const dokument = (titel, inhalt) => `<!-- generiert von build-immunwoche.mjs -->
<meta charset="utf-8">
<title>${titel}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap">
<style>${CSS}</style>
${inhalt}
`;

// ---------------------------------------------------------------- Render

await fs.mkdir(OUT, { recursive: true });
const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox', '--allow-file-access-from-files'] });

const MM = 96 / 25.4;
const SEITE_HOCH = 297 * MM;
const PADDING = (17 + 13) * MM;   // oben + unten aus .seite
const GAP = 7 * MM;
const FUSS_HOCH = 17 * MM;   // Fusszeile plus Sicherheitsmarge
const PLATZ = SEITE_HOCH - PADDING - FUSS_HOCH;

/** Misst jeden Baustein und packt sie greedy auf Seiten — kein Handbalancieren mehr. */
async function paginiere(teile) {
  const page = await browser.newPage();
  const mess = dokument('Messung', `<div class="seite" style="min-height:0">${teile.join('\n')}</div>`);
  const tmp = path.join(OUT, '_messung.html');
  await fs.writeFile(tmp, mess, 'utf8');
  await page.goto(pathToFileURL(tmp).href, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  const hoehen = await page.evaluate(() =>
    [...document.querySelector('.seite').children].map(c => c.getBoundingClientRect().height));
  await page.close();
  await fs.rm(tmp, { force: true });

  const seiten = [];
  let aktuell = [], hoehe = 0;
  teile.forEach((teil, i) => {
    const h = hoehen[i];
    const dazu = aktuell.length ? h + GAP : h;
    if (aktuell.length && hoehe + dazu > PLATZ) { seiten.push(aktuell); aktuell = []; hoehe = 0; }
    aktuell.push(teil);
    hoehe += aktuell.length === 1 ? h : h + GAP;
  });
  if (aktuell.length) seiten.push(aktuell);
  return seiten;
}

async function renderPdf(htmlPath, pdfPath) {
  const page = await browser.newPage();
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: pdfPath, format: 'A4', printBackground: true, preferCSSPageSize: true,
                   margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await page.close();
  const { size } = await fs.stat(pdfPath);
  console.log(`  ✓ ${path.basename(pdfPath)} (${(size / 1024).toFixed(0)} KB)`);
}

async function seitenHtml(t, startNr = 1) {
  const seiten = await paginiere(bausteine(t));
  const label = `Tag ${t.nr} · ${t.titel}`;
  return seiten.map((inhalt, k) =>
    `<div class="seite">\n  ${inhalt.join('\n  ')}\n  ${seitenfuss(startNr + k, label)}\n</div>`).join('\n');
}

const alleSeiten = [];
for (const t of TAGE) {
  const html = path.join(OUT, `${t.slug}.html`);
  const inhalt = await seitenHtml(t);
  alleSeiten.push(inhalt);
  await fs.writeFile(html, dokument(`Immunwoche Tag ${t.nr} — ${t.titel}`, inhalt), 'utf8');
  await renderPdf(html, path.join(OUT, `Immunwoche-Tag${t.nr}-${t.titel.replace(/[^A-Za-zÄÖÜäöü]+/g, '-').replace(/^-|-$/g, '')}.pdf`));
}

const gesamtHtml = path.join(OUT, 'immunwoche-tag2-5.html');
await fs.writeFile(gesamtHtml, dokument('Immunwoche Tag 2 bis 5', alleSeiten.join('\n')), 'utf8');
await renderPdf(gesamtHtml, path.join(OUT, 'Immunwoche-Tag2-bis-5.pdf'));

await browser.close();
console.log('Fertig.');
