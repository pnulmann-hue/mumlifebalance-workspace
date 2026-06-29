---
tags: [produkt, mama-ceo, saeule-4]
---

# Säule 4 — Du delegierst den Adminkram (Wochen 5-6)

> **Versprechen am Ende der Säule:** „Ich hab jetzt zwei KI-Mitarbeiter, die mir den Adminkram abnehmen — einen fürs Business und einen fürs Zuhause. Mein Morgenbriefing kommt von der KI, mein Haushalts-Mental-Load liegt nicht mehr in meinem Kopf, und ich weiss genau, was ich selbst mache und was die Maschine übernimmt."
>
> **🎯 Kern-Payoff:** In Säule 3 hast du dein Notion-Business-Brain gebaut. Jetzt setzen wir Helfer drauf, die da reinschauen und dir Arbeit abnehmen — ohne dass du programmieren können musst. Das Versprechen ist nicht „werde Tech-Nerd", sondern „hör auf, Sachen selbst zu machen, die eine gut gebriefte KI dir abnehmen kann". Und das Wichtigste lernst du gleich zu Beginn: KI ist kein Zauber, sondern eine Praktikantin, die nur so gut ist wie dein Auftrag.
> **Die zwei Bots sind Zwillinge:** Der **Cockpit-Bot** liest deine Notion-Business-Planung und sagt dir morgens, was im Business dran ist. Der **Haushalts-Helfer-Bot** liest deine Haushalts-Liste (dein Brain Dump aus Säule 2) und sagt dir morgens, was zu Hause dran ist — Wäsche, Zahnarzt-Termin, Kind muss früher los. Gleiche Mechanik, einmal Business, einmal Familie.
> **🪜 3 Stufen — jede Mentee nimmt einen Win mit, AUCH ohne Claude Code (Patricia-Entscheidung 2026-06-25):** Stufe 0 = die Notion-Liste allein (Mental Load ist raus, manuell nutzbar) · Stufe 1 = der Bot in **Claude Cowork** (Desktop-App, Notion per Connector verbinden, kein Code) · Stufe 2 = automatischer Telegram-Bot via Claude Code (für die, die mehr wollen). **Niemand muss Claude Code anfassen.**
> **6 Lektionen · ~85 Min Video · Arbeitsblatt + Live-Call 3 (Ende W6, Bot-Bau-Werkstatt · 120 Min)**
> **2 Boni im Preis:** Cockpit-Bot-System-Prompt + Haushalts-Helfer-Bot-System-Prompt · **2 Extra-Boni:** Kochassistent-System-Prompt + Gratis-Chat-One-Shot-Prompt (fertige Vorlagen zum Anpassen)

---

## Anknüpfung an Säule 1–3 (roter Faden — wichtig für Konsistenz)

Säule 4 baut direkt auf dem auf, was die Mentee bis hierher erarbeitet hat. Diese Begriffe greifen wir wörtlich wieder auf:

- **Notion-Business-Brain** (aus S3) — der Ort, in den der Cockpit-Bot morgens reinschaut. Ohne S3 kein Cockpit-Bot, deshalb haben wir es zuerst gebaut.
- **Tagesplaner + Aufgaben** (aus S3 L3.4/3.5) — genau das liest der Cockpit-Bot fürs Morgenbriefing.
- **6 Lebens-Bereiche** (aus S3) — die Brille, durch die der Bot deine Woche sortiert.
- **4-Filter „Automatisieren"** (aus S2 L2.4) — die Aufgaben, die du dort als „automatisieren" markiert hast, kriegen hier ihren Helfer.
- **5 CEO-Aufgaben „nur du"** (aus S1 L1.4) — die Grenze, was du NIE an eine KI abgibst (Vision, Entscheidungen, Brand, Beziehungen, Reflexion). Kommt in L4.6 als Mensch-vs-Maschine-Linie zurück.
- **Hütchen-Inventar / Brain Dump** (aus S2 L2.3) — das ist die direkte Quelle für deinen Haushalts-Helfer-Bot in L4.5. Deine ganzen „muss ich noch"-Sachen (Staubsaugen montags, Frühlingskleider raussuchen Ende März) wandern in eine Notion-Haushalts-Liste, aus der der Bot dich täglich erinnert.

---

## 🪜 Das Tool-Stufen-Modell (verbindlich — gilt für Cockpit-Bot UND Haushalts-Bot)

Beide Bots laufen nach demselben 3-Stufen-Modell. So nimmt **jede** Mentee einen Win mit, egal wie tech-affin:

| Stufe | Tool | Was die Mentee tut | Win | Aufwand/Kosten |
|---|---|---|---|---|
| 🟢 **0** | **nur Notion** (+ Views) | Liste pflegen, „Kommende Termine"- + „nach Wochentag"-Ansicht öffnen | Mental Load ist raus dem Kopf, sie sieht was ansteht | null (Notion gratis) |
| 🟡 **1** | **Claude Cowork** (Desktop) | Notion per Connector verbinden, fertige Bot-Vorlage einfügen, fragen „Was ist heute dran?" | echter Bot, der ihr Notion liest — **kein Code, keine Installation im Terminal** | Claude Pro (~20-23 CHF/Mt) |
| 🔵 **2** | **Claude Code → Telegram** | gehosteten Bot bauen lassen, der automatisch morgens pusht | läuft von selbst, aufs Handy, auch wenn der Laptop zu ist | + Hosting ~5 CHF/Mt, mehr Aufwand |

**Wichtig fürs Verständnis (Connector = der „Stecker"):** Notion lässt sich mit Claude Cowork **und** Claude Code verbinden, weil beide *Connectors (MCP)* unterstützen — Notion liefert den fertigen Connector, in Cowork klickst du ihn in den Einstellungen einmal ein (Notion-Login bestätigen, du gibst frei welche Seiten er sehen darf). Der **nackte Gratis-Chat** kann das nicht, der sieht nur, was man reinkopiert (→ dafür der Gratis-Chat-One-Shot-Prompt als Notlösung).

**Stufe 0 ehrlich abgegrenzt:** Reines Notion kann **Termine/Geburtstage/Schule** über einen Datums-Filter zeigen und Wiederkehrendes **nach Wochentag/Rhythmus gruppieren** — aber NICHT automatisch rechnen „welche wiederkehrende Aufgabe ist genau heute dran". Genau dieses „Heute-Denken" ist der Mehrwert von Stufe 1 (der Bot). Stufe 0 = organisiert & sichtbar; Stufe 1 = der Bot denkt das „heute" für dich.

**Was Patricia selbst nutzt:** ihr Cockpit-Bot läuft auf **Stufe 2** (Claude Code + Railway + Telegram) — das zeigt sie im Kurs als Ausblick, baut es aber nicht mit den Mentees nach.

---

## Säulen-Übersicht (Modul-Header in ThriveCart)

**Modul-Titel:**
```
Säule 4 — Du delegierst den Adminkram
```

**Modul-Untertitel:**
```
Wochen 5-6 · 6 Lektionen · ca. 85 Min Video · 3 Stufen (auch ohne Code) · fertige Bot-Vorlagen
```

**Modul-Beschreibung:**
```
In Säule 3 hast du dein Business-Brain in Notion aufgebaut. Jetzt setzen wir Helfer drauf — KI-Mitarbeiter, die da reinschauen und dir Arbeit abnehmen, im Business und zu Hause.

Und keine Sorge: du musst dafür nichts programmieren können und kein Tech-Genie sein. Du lernst zuerst die eine Sache, die wirklich zählt — wie du einer KI einen guten Auftrag gibst — und danach baust du Schritt für Schritt zwei Helfer, die ab sofort für dich mitdenken.

Am Ende dieser 2 Wochen:
✓ Du verstehst, warum KI kein Zauber ist, sondern eine Praktikantin, die nur so gut ist wie dein Auftrag — und warum „KI bringt mir nichts" fast immer am Input liegt
✓ Du hast deinen Business-Brief geschrieben — das einmal festgehaltene Wissen, das jeder deiner Bots braucht
✓ Du hast deinen Cockpit-Bot gebaut — dein persönliches Business-Morgenbriefing, das in dein Notion schaut und dir sagt, was heute dran ist
✓ Du hast deinen Haushalts-Helfer-Bot gebaut — der deine ganze „muss ich noch"-Liste trägt und dich morgens erinnert, was zu Hause und für die Kinder ansteht
✓ Du weisst glasklar, was die KI macht und was deins bleibt — die Grenze zwischen Mensch und Maschine

Live-Call 3 (Ende W6): Bot-Bau-Werkstatt · 120 Min · wir bauen gemeinsam, und wer irgendwo hängt, kriegt hier seine Lösung.
```

**Modul-Downloads (für die ganze Säule)** — Bot-Vorlagen + Anleitungen in `bonus-vorlagen-saeule-4/`:
- 📋 **Arbeitsblatt Säule 4** → `04-arbeitsblaetter/mama-ceo-arbeitsblatt-saeule-4.docx`
- ✍️ **Bonus 5 · Business-Brief-Erarbeiten-Prompt** → L4.3 (erarbeiten mit Claude, Output = 1 Dokument)
- 🖥 **Bonus 6 · Cowork einrichten** (einmalige Setup-Anleitung) → L4.4
- 🌅 **Bonus 1 · Cockpit-Bot-Vorlage** → L4.4
- 🏠 **Bonus 2 · Haushalts-Helfer-Bot-Vorlage** → L4.5
- 🍳 **Bonus 3 · Kochassistent-Vorlage** (Extra) → L4.5
- 💬 **Bonus 4 · Gratis-Chat-One-Shot** (Extra) → L4.2/L4.4
- ⚙️ **Bonus 7 · Claude-Code-Anleitung** (Stufe 2) → L4.4-Ausblick + L4.6

---

# 🎬 LEKTION 4.1 — KI-Mythos vs. Realität · Input ist alles

**Status:** ⚠️ NEU bauen (9 Folien)
**Material:** Patricias eigene KI-Erfahrung — „warum meine Bots funktionieren ist nicht Magie, sondern guter Input". Brand-Voice: nahbar, anti-Tech-Angst, „du musst nichts können".

## ThriveCart-Setup

**Lektion-Titel:**
```
4.1 · KI-Mythos vs. Realität — warum „KI bringt mir nichts" am Input liegt
```

**Video-Datei:** `saeule-04-lektion-4-1.mp4` (ca. 10 Min)

**Beschreibungstext:**
```
„Ich hab ChatGPT probiert, aber es bringt mir nichts." Diesen Satz hör ich ständig. Und fast immer liegt es nicht an der KI, sondern daran, wie man mit ihr redet.

In dieser Lektion räumen wir mit dem grössten Mythos auf: dass KI ein Zauberkasten ist, der auf Knopfdruck dein Business macht. Ist sie nicht. Sie ist eine richtig gute Praktikantin — und eine Praktikantin ohne Einarbeitung liefert eben Mist.

Du lernst:
→ Warum „Müll rein, Müll raus" die wichtigste KI-Regel überhaupt ist
→ Warum meine 13 Helfer funktionieren — und es nichts mit Programmieren zu tun hat
→ Die 3 Dinge, die jeder gute KI-Auftrag braucht (Kontext, klare Aufgabe, Beispiel)
→ Den Fahrplan für Säule 4: zwei KI-Mitarbeiter, einer fürs Business und einer fürs Zuhause

Das hier ist die wichtigste Lektion der ganzen Säule, weil alles andere darauf aufbaut. Wenn du das verstehst, ist der Rest nur noch umsetzen.
```

## Folien-Plan (9 Folien)

| # | Folie | Inhalt | Sprechnotizen |
|---|---|---|---|
| 1 | **Titel** | „4.1 · KI-Mythos vs. Realität — Input ist alles" | „Willkommen in Säule 4, dem Teil, auf den ich mich am meisten freue, weil hier deine KI-Mitarbeiter entstehen. Aber bevor wir irgendwas bauen, müssen wir über die eine Sache reden, die fast jede Mama falsch macht, wenn sie mit KI startet." |
| 2 | **„KI bringt mir nichts"** | Frau frustriert vor ChatGPT · Sprechblase: „Ich hab's probiert, war nutzlos" | „Hand aufs Herz, vielleicht hast du es selbst schon gedacht: ich hab ChatGPT mal aufgemacht, irgendwas gefragt, und das Ergebnis war so allgemein und unbrauchbar, dass ich es wieder zugemacht hab. Das kenn ich, und ich verspreche dir, es liegt fast nie an der KI." |
| 3 | **Der Mythos: KI als Zauberkasten** | Durchgestrichen: Knopf drücken → fertiges Business · daneben: Realität | „Der grösste Irrtum ist, dass KI ein Zauberkasten ist, wo du auf einen Knopf drückst und dein halbes Business kommt fertig raus. So funktioniert das nicht, und wer das erwartet, ist enttäuscht. Die Wahrheit ist viel beruhigender, weil sie bedeutet, dass DU am Steuer bleibst." |
| 4 | **KI ist eine Praktikantin** | Bild: motivierte Praktikantin · „schnell, fleissig, aber weiss nichts über dich" | „Stell dir KI lieber als Praktikantin vor. Sie ist superschnell, sie wird nie müde, und sie beschwert sich nie. Aber sie weiss am ersten Tag absolut nichts über dich, dein Business und deine Kundinnen. Und genau wie eine echte Praktikantin liefert sie nur dann was Brauchbares, wenn du sie vernünftig einarbeitest." |
| 5 | **Müll rein, Müll raus** | Pfeil: vager Auftrag → vages Ergebnis · klarer Auftrag → brauchbares Ergebnis | „Daraus folgt die wichtigste KI-Regel überhaupt: Müll rein, Müll raus. Wenn du vage fragst, kriegst du Vages zurück, und wenn du genau sagst was du brauchst und wer du bist, kriegst du was Brauchbares. Dein Ergebnis ist immer nur so gut wie dein Auftrag, und das ist eine gute Nachricht, weil du den Auftrag in der Hand hast." |
| 6 | **Warum meine Helfer funktionieren** | Patricia-Frame: „13 Helfer, solo, mit 4 Kindern — kein Tech-Studium" | „Ich sag dir mal ganz ehrlich, warum bei mir so viele KI-Helfer laufen: nicht weil ich programmieren kann oder ein Tech-Genie bin, ich bin Mama von vier Kindern und hab mir das alles selbst beigebracht. Es funktioniert, weil ich gelernt hab, gute Aufträge zu geben. Das kannst du genauso lernen, und genau das machen wir in dieser Säule." |
| 7 | **3 Dinge für jeden guten Auftrag** | 1. Kontext (wer bin ich) · 2. Klare Aufgabe (was genau) · 3. Beispiel (wie solls aussehen) | „Ein guter KI-Auftrag hat immer drei Zutaten. Erstens Kontext, also wer bist du und für wen arbeitest du. Zweitens eine klare Aufgabe, nicht ‚mach mir Content', sondern ‚schreib mir drei Story-Ideen zum Thema X für Mamas im Network'. Und drittens ein Beispiel, damit sie deinen Stil trifft. Diese drei Dinge bauen wir in den nächsten Lektionen Stück für Stück auf." |
| 8 | **Der Fahrplan für Säule 4** | 2 Bot-Karten: 🌅 Cockpit-Bot (Business-Morgenbriefing) · 🏠 Haushalts-Helfer-Bot (Mental Load zu Hause) | „Und das ist unser Fahrplan: wir bauen zwei KI-Mitarbeiter, die im Grunde Zwillinge sind. Den Cockpit-Bot, der morgens in dein Notion-Business schaut und dir sagt was dran ist, und den Haushalts-Helfer, der genauso deine Haushalts-Liste im Kopf behält und dir morgens sagt, was zu Hause ansteht, Wäsche, Zahnarzt, Kind früher in die Schule. Einer fürs Business, einer fürs Zuhause, weil der Adminkram an beiden Orten an dir zerrt." |
| 9 | **Arbeitsblatt + nächste Lektion** | „📋 Notier deinen letzten frustrierenden KI-Versuch" · „Nächste Lektion: 4.2 — womit du arbeitest" | „Im Arbeitsblatt schreibst du kurz auf, wo dich KI bisher genervt hat, denn am Ende der Säule schaust du nochmal drauf und siehst den Unterschied. In der nächsten Lektion klären wir kurz, womit du überhaupt arbeitest, damit du nicht in der Auswahl hängenbleibst. Bis gleich." |

## Arbeitsblatt-Sektion 4.1

```
LEKTION 4.1 · KI-Mythos vs. Realität — Input ist alles

▸ Dein bisheriger KI-Frust (ehrlich)
Wo hat KI dir bisher „nichts gebracht"? Was hast du gefragt?
[3 Linien]
→ Am Ende von Säule 4 schaust du nochmal drauf — du wirst sofort sehen, woran's lag.

▸ Die 3 Zutaten merken
Schreib in eigenen Worten auf, was ein guter KI-Auftrag braucht:
1. Kontext = _______________________________
2. Klare Aufgabe = _______________________________
3. Beispiel = _______________________________

▸ Was nervt dich am meisten — Business-Adminkram oder Haushalts-Mental-Load?
☐ Eher Business (Briefing, Planung, Überblick) → freu dich auf den Cockpit-Bot
☐ Eher Zuhause (was steht an, Termine, Haushalt im Kopf) → freu dich auf den Haushalts-Helfer
☐ Beides gleich → perfekt, wir bauen beide

WAS DU NACH LEKTION 4.1 HAST
✓ Du verstehst KI als Praktikantin, nicht als Zauberkasten
✓ Du kennst die Regel „Müll rein, Müll raus"
✓ Du kennst die 3 Zutaten für jeden guten Auftrag
✓ Du kennst den Fahrplan: 2 KI-Mitarbeiter (Business + Zuhause) in dieser Säule
```

---

# 🎬 LEKTION 4.2 — Womit du arbeitest: die 3 Stufen (Cowork ist dein Freund)

**Status:** ✅ bestehende Basis (modul-02-lektion-2-3.pptx) · **Folien-Plan hier neu im Säule-4-Stil spezifiziert** · Datei `saeule-04-lektion-4-2.pptx`
**Material:** Patricias Tool-Stack + Patricia-Entscheidung 2026-06-25. **Wichtig für Mentees: Komplexität rausnehmen + jede kriegt einen Win.** Diese Lektion lehrt das **Tool-Stufen-Modell** (siehe Referenzblock oben): Stufe 0 = Notion allein · Stufe 1 = **Claude Cowork** (Desktop, Notion per Connector, kein Code — der Weg für Nicht-Techies) · Stufe 2 = Claude Code/Telegram (Profi, automatisch). Kernbotschaft: der nackte Gratis-Chat reicht fürs Business nicht (zu statisch), aber **niemand muss Claude Code installieren** — Cowork ist der bequeme Mittelweg.

## ThriveCart-Setup

**Lektion-Titel:**
```
4.2 · Womit du arbeitest — Projekt oder Claude Code (nicht der nackte Chat)
```

**Video-Datei:** `saeule-04-lektion-4-2.mp4` (ca. 10 Min)

**Beschreibungstext:**
```
Wenn du dich einliest, stösst du auf ChatGPT, Claude, Cowork, Claude Code — und fängst vor lauter Auswahl gar nicht erst an. Das räumen wir hier auf, in einfachen Worten, mit einem klaren 3-Stufen-Modell. Und das Beste: du nimmst auf jeder Stufe einen Win mit, auch wenn du nie etwas installierst.

Die wichtigste Erkenntnis vorweg: der nackte Gratis-Chat reicht fürs Business nicht, weil er zu statisch ist und dich jedes Mal vergisst. Aber du musst dafür auch kein Programmierer-Tool anfassen — für die meisten ist Claude Cowork genau richtig.

Du lernst:
→ Die 3 Stufen: Stufe 0 (nur Notion) · Stufe 1 (Claude Cowork) · Stufe 2 (Claude Code, automatisch)
→ Warum der nackte Chat fürs Business nicht taugt — und was du stattdessen nimmst
→ Claude Cowork: dein Bot ohne Code — Notion einmal verbinden, fertig
→ Was ein „Connector" ist (das, was Claude mit deinem Notion reden lässt) — einfach erklärt
→ Was das ungefähr kostet — und dass Stufe 0 gratis ist

Am Ende weisst du genau, auf welcher Stufe du startest und womit du in 4.4 und 4.5 baust.
```

## Folien-Plan (10 Folien)

| # | Folie | Inhalt | Sprechnotizen |
|---|---|---|---|
| 1 | **Titel** | „4.2 · Womit du arbeitest — die 3 Stufen" | „In dieser Lektion klären wir, womit du überhaupt arbeitest, und ich halt das ganz einfach. Ich zeig dir drei Stufen, und das Schöne ist: auf jeder nimmst du was mit, auch wenn du nie irgendwas installierst. Du musst nur wissen, auf welcher du starten willst." |
| 2 | **Der nackte Chat reicht nicht** | durchgestrichen: normales Chatfenster · „vergisst dich jedes Mal, zu statisch fürs Business" | „Das Erste, was du wissen musst: das normale Gratis-Chatfenster, wo du was reintippst und morgen ist alles weg, das reicht fürs Business auf Dauer nicht. Es ist zu statisch und vergisst dich jedes Mal. Du willst was, das dein Wissen behält und in dein Notion schaut, und dafür zeig ich dir die drei Stufen." |
| 3 | **Die 3 Stufen auf einen Blick** | Tabelle: 🟢 Stufe 0 Notion · 🟡 Stufe 1 Cowork · 🔵 Stufe 2 Claude Code | „Stufe null ist nur dein Notion, ganz ohne Bot. Stufe eins ist Claude Cowork, ein Bot ohne Code. Stufe zwei ist Claude Code, der automatische Profi-Bot. Du fängst da an, wo du dich wohlfühlst, und kannst jederzeit eine Stufe höher. Niemand muss bis Stufe zwei, ganz im Gegenteil." |
| 4 | **Stufe 0: Notion allein ist schon ein Win** | Notion-Liste + Ansichten „Kommende Termine" / „nach Wochentag" | „Stufe null heisst: du hast deine Liste in Notion, mit ein paar fertigen Ansichten, und machst sie einfach auf. Du siehst, welche Termine kommen und was an welchem Tag dran ist. Kein Bot, kein Abo, gar nichts. Allein dass das Zeug aus deinem Kopf raus und an einem Ort ist, ist schon die halbe Miete." |
| 5 | **Stufe 1: Claude Cowork — dein Bot ohne Code** | Cowork-Desktop-App · „Notion verbinden + Vorlage rein + fragen" | „Stufe eins ist mein Liebling für die meisten von euch: Claude Cowork. Das ist eine App auf deinem Computer mit Knöpfen, kein Terminal, kein Programmieren. Du verbindest einmal dein Notion, fügst meine fertige Bot-Vorlage ein, und ab dann fragst du ‚was ist heute dran' und kriegst deine Antwort aus deinem echten Notion. So einfach ist das." |
| 6 | **Was ist ein „Connector"?** | Bild: Stecker zwischen Claude und Notion · „einmal einstecken, du gibst frei was er sieht" | „Kurz zum Wort Connector, weil's wichtig ist: stell dir das wie einen Stecker vor. Notion liefert den Stecker, und in Cowork klickst du ihn einmal ein, loggst dich bei Notion ein und sagst, welche Seiten Claude sehen darf. Ab dann reden die zwei miteinander. Genau das kann der nackte Gratis-Chat nicht, deshalb brauchst du Cowork oder Claude Code dafür." |
| 7 | **Stufe 2: Claude Code (Ausblick)** | „der automatische Bot, schickt aufs Handy, läuft auch wenn Laptop zu" · kein Muss | „Stufe zwei ist Claude Code, damit baust du einen Bot, der von selbst läuft und dir morgens aufs Handy schreibt, auch wenn dein Laptop zu ist. So läuft meiner. Das ist die Profi-Stufe, braucht etwas mehr und ist ausdrücklich kein Muss. Ich zeig's dir in 4.4 als Ausblick, aber die allermeisten bleiben glücklich auf Stufe eins." |
| 8 | **Was kostet das?** | Stufe 0 gratis · Stufe 1 Cowork ~20-23/Mt (Claude Pro) · Stufe 2 + Hosting ~5/Mt | „Zum Geld, ganz ehrlich: Stufe null ist gratis. Für Cowork brauchst du ein Claude-Pro-Abo, etwa zwanzig bis dreiundzwanzig Franken im Monat, das ist weniger als ein Mittagessen auswärts und nimmt dir Stunden ab. Nur die Profi-Stufe kostet später noch ein bisschen Hosting obendrauf, aber dazu kommen wir in 4.4." |
| 9 | **Eins nach dem anderen** | Warnung: nicht 5 Tools parallel · „eine Stufe, zwei Bots, dann weiterschauen" | „Ein Rat aus Erfahrung: fang nicht mit fünf Sachen gleichzeitig an. Wähl eine Stufe, bau damit deine zwei Helfer aus dieser Säule, gewöhn dich dran, und erst wenn das sitzt, schaust du dir die nächste an. Sonst verzettelst du dich, und das ist genau das Hamsterrad, aus dem wir dich rausholen." |
| 10 | **Arbeitsblatt + nächste Lektion** | „📋 Wähle deine Stufe + leg den Zugang an" · „Nächste Lektion: 4.3 — dein Business-Brief" | „Im Arbeitsblatt entscheidest du jetzt, auf welcher Stufe du startest, und legst, falls nötig, deinen Zugang an, damit du in 4.4 sofort bauen kannst. In der nächsten Lektion schreiben wir deinen Business-Brief, das Herzstück, das jeder deiner Helfer braucht. Bis gleich." |

## Arbeitsblatt-Sektion 4.2

```
LEKTION 4.2 · Womit du arbeitest — die 3 Stufen

▸ Auf welcher Stufe startest du? (du kannst später jederzeit höher)
☐ 🟢 Stufe 0 — nur Notion (gratis, kein Bot, ich nutze die Ansichten)
☐ 🟡 Stufe 1 — Claude Cowork (Bot ohne Code) ← Empfehlung für die meisten
☐ 🔵 Stufe 2 — Claude Code/Telegram (automatisch, später)

▸ Wenn Stufe 1 (Cowork): Zugang bereit?
☐ Claude-Pro-Abo aktiv (~20-23 CHF/Mt)
☐ Claude Desktop-App installiert (Mac/Windows)
☐ Notion-Connector eingesteckt (einmal: Notion-Login bestätigt + Seiten freigegeben)

▸ Gut zu wissen (häkchen wenn verstanden)
☐ Der nackte Gratis-Chat reicht fürs Business nicht (zu statisch)
☐ „Connector" = der Stecker, der Claude mit meinem Notion reden lässt
☐ Ich gebe selbst frei, welche Notion-Seiten der Bot sehen darf
☐ Ich muss NICHT Claude Code anfassen — Cowork reicht

▸ Mein Vorsatz
„Ich bleib erstmal auf EINER Stufe und bau meine 2 Bots, bevor ich was Neues anschaue." ☐

WAS DU NACH LEKTION 4.2 HAST
✓ Du kennst die 3 Stufen und weisst, wo du startest
✓ Du verstehst: nackter Chat = zu statisch · Cowork = Bot ohne Code
✓ Du weisst, was ein Connector ist und dass du Notion damit verbindest
✓ Dein Zugang für deine Stufe ist bereit
```

---

# 🎬 LEKTION 4.3 — Dein Business-Brief schreiben (das Bot-Wissen)

**Status:** ✅ bestehende Basis (modul-02-lektion-2-4.pptx) · **Folien-Plan hier neu im Säule-4-Stil spezifiziert** · Datei `saeule-04-lektion-4-3.pptx`
**Material:** Patricias eigener Business-Brief als abstrahiertes Beispiel. Dies ist die Fundament-Lektion — der Business-Brief ist der Kontext (Zutat 1 aus L4.1), den jeder Bot bekommt.

## ThriveCart-Setup

**Lektion-Titel:**
```
4.3 · Dein Business-Brief — das Wissen, das jeder Bot braucht
```

**Video-Datei:** `saeule-04-lektion-4-3.mp4` (ca. 12 Min)

**Beschreibungstext:**
```
Erinnerst du dich an die 3 Zutaten aus Lektion 4.1? Kontext, klare Aufgabe, Beispiel. Heute bauen wir die erste und wichtigste: den Kontext. Wir nennen ihn deinen Business-Brief.

Das ist ein kurzes Dokument, in dem steht, wer du bist, für wen du arbeitest, was du anbietest und wie du klingst. Du schreibst es EINMAL — und ab dann kriegt es jeder deiner Bots, damit keiner mehr allgemeinen Einheitsbrei ausspuckt, sondern klingt wie DU.

Du lernst:
→ Warum ohne Business-Brief jeder Bot austauschbar bleibt
→ Die 6 Bausteine deines Business-Briefs (in einfachen Worten)
→ Der schnelle Weg: lass ihn dir von Claude im Gespräch erarbeiten (fertiger Prompt, Bonus 5) — am Ende hast du EIN Dokument
→ Wie du deine eigene Stimme einfängst, damit die KI nicht nach Roboter klingt
→ Wohin damit pro Tool: Gratis-Chat (jedes Mal rein) · Projekt (1× hochladen) · Cowork (1× in die Bot-Anweisung) · Claude Code (als Datei)

Ich zeig dir meinen eigenen Business-Brief als Beispiel, dann siehst du genau, wie deiner aussehen darf.

📋 Lektion 4.3 im Arbeitsblatt: dein eigener Business-Brief, Baustein für Baustein
```

## Folien-Plan (10 Folien)

| # | Folie | Inhalt | Sprechnotizen |
|---|---|---|---|
| 1 | **Titel** | „4.3 · Dein Business-Brief" | „Jetzt bauen wir das Herzstück deiner ganzen KI-Arbeit, und das ist nicht ein Bot, sondern ein kurzes Dokument, das alle deine Bots klüger macht. Ich nenne es den Business-Brief, und wenn der einmal steht, wird alles andere leicht." |
| 2 | **Warum jeder Bot dasselbe Wissen braucht** | Visual: 2 Bots greifen auf 1 gemeinsames Wissens-Dokument zu | „Stell dir vor, du holst dir zwei Praktikantinnen ins Haus. Du würdest doch nicht jeder einzeln und jeden Tag neu erklären, wer du bist und was du machst. Genau deshalb schreibst du dein Wissen einmal auf, und jede neue KI kriegt dasselbe Dokument. Du briefst einmal, nicht zehnmal." |
| 3 | **Ohne Brief: Einheitsbrei** | Vergleich: generischer KI-Text vs. Patricia-Text | „Ohne diesen Brief klingt jede KI gleich, nämlich nach allgemeinem Internet-Einheitsbrei, und das spüren deine Leserinnen sofort. Mit dem Brief klingt sie wie du, mit deiner Sprache, deinen Themen, deiner Haltung. Das ist der Unterschied zwischen ‚nutzlos' und ‚meine beste Mitarbeiterin'." |
| 4 | **Die 6 Bausteine** | 6 Kacheln: 1 Wer bin ich · 2 Wer ist meine Kundin · 3 Was biete ich an · 4 Meine Themen · 5 Meine Stimme · 6 Was der Bot NICHT tun soll | „Dein Business-Brief hat sechs Bausteine. Erstens: wer bin ich. Zweitens: wer ist meine Kundin. Drittens: was biete ich an, also deine Produkte. Viertens: über welche Themen rede ich. Fünftens: wie klinge ich, deine Stimme. Und sechstens, ganz wichtig: was soll der Bot NICHT tun, deine Tabus. Diese sechs füllst du gleich im Arbeitsblatt aus." |
| 5 | **Baustein 1-3: dein Fundament** | Wer bin ich (Mama, Network, Thema) · Kundin (konkret, nicht „alle") · Angebot (Gratis/Mini/Gross aus S3) | „Die ersten drei Bausteine kennst du eigentlich schon aus den letzten Säulen. Wer du bist, deine Kundin so konkret wie möglich, nicht ‚alle Frauen', und dein Angebot, das du in Säule 3 als Gratis-, Mini- und grosses Produkt schon sortiert hast. Du schreibst hier nur zusammen, was du längst weisst." |
| 6 | **Baustein 4-6: dein Charakter** | Themen (deine Überthemen aus S3) · Stimme (wie redest du) · Tabus (was nie) | „Die zweiten drei geben dem Bot deinen Charakter. Deine Überthemen aus der Jahres-Strategie, deine Stimme, also redest du eher locker oder seriös, per du oder per Sie, und deine Tabus, zum Beispiel keine übertriebenen Versprechen, keine Fremdwörter, was auch immer dir wichtig ist. Damit hat die KI Leitplanken." |
| 7 | **Stimme einfangen: gib Beispiele** | „Häng 2-3 deiner echten Texte an" → Bot lernt deinen Ton | „Der beste Trick für deine Stimme ist erstaunlich einfach: häng zwei, drei deiner echten Texte an den Brief, eine Caption, eine Nachricht, irgendwas das nach dir klingt. Die KI liest das und ahmt deinen Ton nach. Du musst deine Stimme nicht beschreiben können, du musst sie nur zeigen." |
| 7b 🆕 | **Der einfachere Weg: lass dich interviewen (Buch-Technik)** | Visual: KI stellt Fragen, Mama antwortet → fertiger Brief. „Bonus 5: Business-Brief-Erarbeiten-Prompt" | „Und jetzt mein Lieblings-Trick, den ich selbst die ganze Zeit benutze: du musst dieses Blatt gar nicht alleine ausfüllen. Sag der KI einfach, sie soll tun, als würde sie ein Buch über dich und dein Business schreiben, und sie soll dir so lange und so vertieft Fragen stellen, bis sie wirklich alle Infos von dir hat. Dann sitzt du nicht vor einem leeren Blatt, sondern beantwortest einfach eine Frage nach der anderen, und am Schluss spuckt sie dir deinen fertigen Business-Brief aus. Genau diesen Prompt hab ich dir als Bonus dazugelegt, du musst ihn nur reinkopieren." |
| 8 | **Mein Business-Brief als Beispiel** | Screenshot/abstrahiert: Patricias Brief (Mama, Network + Online, vierstellig-ehrlich, Anti-Bali, Schweizer Ton) | „Ich zeig dir jetzt meinen eigenen Business-Brief, damit du ein Gefühl kriegst. Du siehst, das ist nichts Hochgestochenes, sondern in normalen Worten: wer ich bin, für wen ich da bin, wie ich rede und was bei mir nie vorkommt. Genau so grob und ehrlich darf deiner auch sein." |
| 9 | **Arbeitsblatt + nächste Lektion** | „📋 Schreib deinen Business-Brief (6 Bausteine)" · „Nächste Lektion: 4.4 — Cockpit-Bot bauen" | „Im Arbeitsblatt schreibst du jetzt deinen Business-Brief, Baustein für Baustein, und du legst ihn als Notiz ab, wo du ihn immer findest. Den brauchst du in der nächsten Lektion sofort, denn da bauen wir deinen ersten echten Bot, den Cockpit-Bot. Bis gleich." |

## Arbeitsblatt-Sektion 4.3

```
LEKTION 4.3 · Dein Business-Brief schreiben

Schreib jeden Baustein in 2-4 Sätzen. Kein Roman — Stichworte reichen.
Diesen Brief kopierst du später in jeden deiner Bots.

▸ Baustein 1 — Wer bin ich
(Name, Mama von …, im Network mit …, mein Thema ist …)
[3 Linien]

▸ Baustein 2 — Wer ist meine Kundin (so konkret wie möglich)
[3 Linien]

▸ Baustein 3 — Was biete ich an (aus Säule 3: Gratis / Mini / Gross)
🎁 Gratis: _______________  💶 Mini: _______________  💎 Gross: _______________

▸ Baustein 4 — Meine Themen (deine Überthemen aus der Jahres-Strategie)
1. _______________  2. _______________  3. _______________

▸ Baustein 5 — Meine Stimme (locker/seriös, du/Sie, typische Wörter von mir)
[2 Linien]

▸ Baustein 6 — Was der Bot NIE tun soll (deine Tabus)
[2 Linien]

▸ Stimm-Beispiele anhängen
Welche 2-3 eigenen Texte hängst du an, damit der Bot deinen Ton trifft?
1. _______________  2. _______________  3. _______________

▸ Wo legst du den Business-Brief ab? (z.B. eigene Notion-Seite „Business-Brief")
_______________________________

WAS DU NACH LEKTION 4.3 HAST
✓ Dein Business-Brief steht — das Wissen für jeden Bot
✓ Du hast 2-3 Stimm-Beispiele zum Anhängen
✓ Der Brief liegt griffbereit für die nächsten Lektionen
```

---

# 🎬 LEKTION 4.4 — Deinen Cockpit-Bot bauen (Live-Demo)

**Status:** ⚠️ NEU bauen (13 Folien)
**Material:** Patricias echter Cockpit-Bot (live auf Railway = Stufe 2) — **für Mentees nach dem 3-Stufen-Modell aufbereitet:** Stufe 0 = Notion-Ansichten (Business-Planung sichtbar, kein Bot) · Stufe 1 = der Bot in **Claude Cowork** (Notion per Connector verbinden, fertige Vorlage rein, fragen — kein Code), das ist der Standard, den jede im Live-Call bauen kann · Stufe 2 = der echte Telegram-Bot via Claude Code (ehrlich erklärt, was er braucht/kostet), nur Ausblick „wer mehr will".

> **Patricia-Entscheidung 2026-06-25:** Cockpit-Bot wird als 3-Stufen-Modell gelehrt, **Stufe 1 = Claude Cowork** (nicht „Projekt"), weil Cowork sauber Notion verbindet und für Nicht-Techies gemacht ist. Niemand muss Claude Code anfassen — das hält das „du musst nichts können"-Versprechen.

## ThriveCart-Setup

**Lektion-Titel:**
```
4.4 · Dein Cockpit-Bot — dein persönliches Morgenbriefing
```

**Video-Datei:** `saeule-04-lektion-4-4.mp4` (ca. 15 Min)

**Beschreibungstext:**
```
Stell dir vor, du machst morgens den Laptop auf und statt selbst in Notion zu wühlen, fragst du deinen Bot „was ist heute dran?" — und kriegst deinen Tagesfokus, deine drei wichtigsten Aufgaben und einen kurzen Überblick. Genau das bauen wir jetzt.

Dein Cockpit-Bot ist dein persönliches Morgenbriefing. Er schaut in dein Notion-Business-Brain aus Säule 3, kennt deinen Business-Brief aus 4.3 und sortiert dir den Tag. Und das Beste: du brauchst dafür kein Hosting und keinen Code.

Du lernst:
→ Wie du mit der fertigen Vorlage (Bonus) in wenigen Minuten dein Morgenbriefing baust
→ Wie der Bot deine Notion-Woche bekommt (ganz einfach reinkopieren oder verbinden)
→ Wie du ihn jeden Morgen nutzt, damit du nie wieder planlos vor dem Tag stehst
→ Und als ehrlicher Ausblick: wie die Profi-Variante als automatischer Telegram-Bot läuft — was sie braucht, was sie kostet, und warum sie kein Muss ist

Ich bau den Bot live vor deinen Augen. Du baust einfach mit.

📋 Lektion 4.4 im Arbeitsblatt: dein Cockpit-Bot eingerichtet + 3 Tage getestet
```

## Folien-Plan (13 Folien)

| # | Folie | Inhalt | Sprechnotizen |
|---|---|---|---|
| 1 | **Titel** | „4.4 · Dein Cockpit-Bot — dein Morgenbriefing" | „Jetzt wird's konkret, denn wir bauen deinen ersten echten KI-Mitarbeiter. Ich nenne ihn den Cockpit-Bot, weil er dir morgens das Cockpit zeigt, also alles was heute wichtig ist, auf einen Blick." |
| 2 | **Was er für dich tut** | 3 Zeilen: morgens fragen → Tagesfokus + 3 Hauptaufgaben + kurzer Überblick | „Was dieser Bot macht, ist einfach erklärt: du fragst ihn morgens ‚was ist heute dran', und er gibt dir deinen Tagesfokus, deine drei wichtigsten Aufgaben und einen kurzen Überblick über die Woche. Du musst nicht mehr selbst in Notion wühlen und dich verlieren, er macht das für dich." |
| 3 | **Warum wir Säule 3 gebraucht haben** | Pfeil: Notion-Business-Brain (S3) → Cockpit-Bot liest Tagesplaner + Aufgaben | „Jetzt zahlt sich Säule 3 aus. Dein Cockpit-Bot kann nur deshalb wissen was heute dran ist, weil du dein Notion-Business-Brain aufgebaut hast, mit Wochenplan, Tagesplaner und Aufgaben. Der Bot ist die Stimme, die dir vorliest, was in deinem Brain steht. Ohne das Brain kein Briefing." |
| 4 | **3 Stufen — wir bauen Stufe 1 (Cowork)** | 🟢 Stufe 0 Notion-Ansicht · 🟡 Stufe 1 Cowork (kein Code) · 🔵 Stufe 2 Claude Code/Telegram | „Erinnerst du dich an die drei Stufen aus 4.2? Stufe null wäre einfach dein Notion aufmachen. Wir bauen jetzt Stufe eins, deinen Bot in Claude Cowork, ganz ohne Code. Und für die, die irgendwann mehr wollen, gibt's Stufe zwei mit Claude Code, der automatisch aufs Handy schickt. Für neunzig Prozent reicht Stufe eins völlig, also fangen wir da an." |
| 5 | **Stufe 1: was der Bot braucht** | 2 Inputs: dein Business-Brief (4.3) + dein Notion (in Cowork per Connector verbunden) | „Dein Cockpit-Bot braucht genau zwei Dinge. Erstens deinen Business-Brief aus der letzten Lektion, damit er dich kennt. Und zweitens dein Notion, das du in Cowork einmal per Connector verbindest, dann liest er deine Wochenplanung direkt, du musst nichts mehr reinkopieren. Genau das machen wir jetzt zusammen." |
| 6 | **Die fertige Vorlage (Bonus)** | Karte: „Cockpit-Bot-System-Prompt — fertig, du passt nur deinen Kontext an" | „Damit du nicht bei null anfängst, hast du von mir eine fertige Vorlage als Bonus. Das ist der komplette System-Prompt, also die Bedienungsanleitung für den Bot, und du musst nur deinen Namen und deinen Kontext eintragen. Den Link zum Download findest du gleich hier in der Lektion." |
| 7 | **Live-Demo Schritt 1: Cowork + Notion verbinden** | Bildschirm: Cowork öffnen · Notion-Connector einstecken · Vorlage einfügen | „So, jetzt bau ich ihn live in Cowork, und du baust einfach mit, pausier wo du musst. Schritt eins: ich öffne Cowork, gehe in die Einstellungen und stecke den Notion-Connector ein, also einmal bei Notion einloggen und die Seiten freigeben. Dann füge ich meine fertige Vorlage ein. Du siehst, ich tippe nichts Kompliziertes, ich klicke und kopiere." |
| 8 | **Live-Demo Schritt 2: Business-Brief rein** | Business-Brief einfügen (Notion ist schon verbunden) | „Schritt zwei: ich gebe ihm noch meinen Business-Brief, damit er weiss wer ich bin. Mein Notion ist ja jetzt verbunden, also muss ich nichts mehr reinkopieren, er schaut von selbst rein. Damit hat der Bot alles, was er braucht." |
| 9 | **Live-Demo Schritt 3: testen** | Eingabe: „Was ist heute mein Fokus?" → Bot-Antwort mit Tagesfokus + 3 Aufgaben | „Und Schritt drei, der schönste: ich frag ihn ‚was ist heute mein Fokus', und schau dir das an, er gibt mir meinen Tagesfokus, meine drei Hauptaufgaben und einen kurzen Wochenblick. Wie geil ist das denn. Genau das hast du gleich auch." |
| 10 | **So nutzt du ihn jeden Morgen** | Routine: Laptop auf → Bot fragen → loslegen (30 Sek statt Notion-Wühlen) | „Im Alltag sieht das dann so aus: Laptop auf, Bot fragen, loslegen. Dreissig Sekunden statt zehn Minuten in Notion verlieren. Einmal pro Woche wirfst du ihm deine neue Wochenseite rein, und der Rest läuft. So fühlt sich Mama-CEO an einem normalen Morgen an." |
| 11 | **Stufe 2: so läuft der automatische Telegram-Bot** | Patricia-Telegram-Bot: Server läuft 24/7 → pusht um 6:30 von selbst · was es braucht: Telegram-Bot-Anmeldung + ein Ort wo er läuft (Hosting) + etwas Code · **gleicher Prompt wie eben — nichts neu schreiben** | „Und für die, die irgendwann Blut lecken, zeig ich dir ehrlich, wie die Profi-Variante läuft. Das ist ein Bot, der Tag und Nacht auf einem kleinen Server liegt und mir jeden Morgen um halb sieben von selbst eine Telegram-Nachricht schickt, ohne dass ich irgendwas anklicke. Dafür braucht es drei Dinge: du meldest deinen Bot kostenlos bei Telegram an, du brauchst einen Ort wo er rund um die Uhr läuft, das nennt man Hosting, und du brauchst ein bisschen Code, der die Verbindung macht. Und ganz wichtig, damit dir nicht graut: deinen Bot-Prompt von eben nimmst du eins zu eins mit, du schreibst nichts Neues. Der Prompt ist das Rezept und bleibt gleich, Claude Code baut nur die Hülle drumherum. Cowork ist der Herd zu Hause, Claude Code ist die Lieferung an die Haustür." |
| 12 | **Stufe 2: Kosten + Claude Code führt dich durch** | Hosting ~5 CHF/Monat + ggf. KI-Kosten · Claude Code schreibt den Code · Hinweis: KEIN Muss, sei dir Aufwand + Kosten bewusst | „Und jetzt das Wichtige, weil ich ehrlich bleibe: dieses Hosting kostet etwa fünf Franken im Monat, dazu kommen je nach Nutzung ein paar Franken KI-Kosten. Den Code musst du nicht selbst schreiben, das macht Claude Code für dich, und es führt dich Schritt für Schritt durch alles, du musst es nur wollen. Aber sei dir bewusst: das ist mehr Aufwand und kostet etwas, und es ist ausdrücklich kein Muss für dieses Programm. Stufe eins trägt dich weit, also fang da an und bau das hier nur, wenn du irgendwann Lust drauf hast." |
| 13 | **Arbeitsblatt + nächste Lektion** | „📋 Cockpit-Bot bauen + 3 Tage testen" · „Nächste Lektion: 4.5 MASTERY — Haushalts-Helfer" | „Im Arbeitsblatt baust du jetzt deinen Cockpit-Bot mit der Vorlage und testest ihn drei Tage lang jeden Morgen. In der nächsten Lektion, der MASTERY, bauen wir seinen Zwilling fürs Zuhause: deinen Haushalts-Helfer, der dir morgens sagt, was an Haushalt und Familie ansteht, damit das nicht mehr alles in deinem Kopf liegt. Bis gleich." |

## Arbeitsblatt-Sektion 4.4

```
LEKTION 4.4 · Dein Cockpit-Bot bauen

▸ Bau-Checkliste (mach das WÄHREND des Videos, pausier wo nötig)
☐ Schritt 1: Cowork geöffnet + Notion-Connector eingesteckt + Vorlage (Bonus) eingefügt
☐ Schritt 2: Business-Brief (aus 4.3) reingegeben
☐ Schritt 3: Notion verbunden (Bot liest die Wochenplanung direkt)
☐ Schritt 4: Getestet mit „Was ist heute mein Fokus?"
☐ Der Bot hat mir Tagesfokus + 3 Aufgaben ausgegeben ✓
(Stufe 0 ohne Bot: einfach die Notion-Ansicht „Diese Woche" öffnen — auch ein Win.)

▸ Mein Cockpit-Bot heisst: _______________________________
   (gib ihm einen Namen — macht's persönlich)

▸ 3-Tage-Test
Tag 1: gefragt? ☐  hilfreich? ☐  Datum: ____
Tag 2: gefragt? ☐  hilfreich? ☐  Datum: ____
Tag 3: gefragt? ☐  hilfreich? ☐  Datum: ____
Was würdest du am Bot noch verbessern? _______________________________

▸ Stufe 2 — nur falls dich der Ehrgeiz packt (KEIN Muss)
☐ Mir ist klar: automatischer Telegram-Bot = Hosting (~5 CHF/Mt) + etwas Code (Claude Code macht's)
☐ Interessiert mich später → in Live-Call 3 ansprechen

WAS DU NACH LEKTION 4.4 HAST
✓ Dein Cockpit-Bot läuft (Stufe 1, ohne Hosting)
✓ Er liest deine Notion-Woche + kennt deinen Business-Brief
✓ Du hast ihn 3 Tage im echten Morgen getestet
✓ Du weisst, wie die automatische Telegram-Variante läuft — inkl. Aufwand + Kosten, ohne Druck
```

---

# 🌟 LEKTION 4.5 MASTERY — Dein Haushalts-Helfer-Bot (Live-Demo)

**Status:** ⚠️ NEU bauen (14 Folien · MASTERY)
**Material:** Patricia-O-Ton 2026-06-12 — der Haushalts-Helfer/Mental-Load-Bot trägt die **Brain-Dump-Liste** (= Hütchen-Inventar aus Säule 2), strukturiert in **wiederkehrend** (Staubsaugen montags) + **datiert** (Frühlingskleider raussuchen letzter Freitag im März) + **Familien-Termine** (Zahnarzt, Kind früher in die Schule). Bot erinnert täglich: „Montag — heute dran: Wäsche, Kind Zahnarzt, Kind früher Schule (Wald)." Liste lebt in einer **eigenen Notion-Haushalts-DB**. Der Bot ist der **Heim-Zwilling des Cockpit-Bots** (gleiche Mechanik, andere Liste).

> **Patricia-Entscheidung 2026-06-12:** L4.5 baut live den Haushalts-Helfer-Bot (Mental-Load), nicht den Kochassistenten. Brain-Dump-Liste in eigener Notion-Haushalts-DB (wiederkehrend + datiert), Bot liest sie wie der Cockpit-Bot Notion liest. Der **Kochassistent** bleibt eine optionale Erweiterung als Extra-Bonus (kurz am Ende erwähnt, Vorlage liegt bei).
>
> **⚙️ Bau-Voraussetzung:** Das Notion-Master-Template (aus Säule 3, `3637078e-8b7e-8121-9f95-d2b377b283a7`) braucht eine zusätzliche **Haushalts-DB** mit Feldern: Aufgabe · Rhythmus (z.B. wöchentlich montags / monatlich / jährlich) · festes Datum (für saisonale Sachen) · Bereich (Haushalt / Familie / Termin) · erledigt. Diese DB muss Patricia noch ins Template aufnehmen (analog Tagesplaner/Aufgaben).

## ThriveCart-Setup

**Lektion-Titel:**
```
4.5 · MASTERY · Dein Haushalts-Helfer — der Mental Load raus aus deinem Kopf
```

**Video-Datei:** `saeule-04-lektion-4-5.mp4` (ca. 28 Min · MASTERY)

**Beschreibungstext:**
```
🌟 Die MASTERY-Lektion von Säule 4 — und die, auf die ich mich am meisten freue. Denn jetzt bauen wir den Zwilling deines Cockpit-Bots, nur diesmal nicht fürs Business, sondern für all das, was du als Mama im Kopf mit dir rumträgst: Wäsche, Zahnarzt-Termine, Kind muss früher los, Frühlingskleider raussuchen, Geburtstagsgeschenk besorgen.

Dieser Mental Load ist riesig, und das Schlimmste daran ist, dass er unsichtbar in deinem Kopf liegt und dich auch nachts nicht loslässt. Genau das holen wir jetzt raus und geben es deinem Haushalts-Helfer-Bot.

Was wir gemeinsam machen:
→ Deine „muss ich noch"-Liste aus Säule 2 in eine Notion-Haushalts-Liste bringen
→ Sie sortieren in wiederkehrend (Staubsaugen montags), datiert (Kleider raus Ende März) und Familien-Termine
→ Den Bot mit der fertigen Vorlage (Bonus) bauen und mit deiner Liste verbinden
→ Ihn live testen: „Was ist heute zu Hause dran?" → und er sagt dir's, jeden Morgen

Plan dir 30 Minuten ein und bau einfach mit. Am Ende hast du den Mental Load nicht mehr nur im Kopf, sondern in einem Helfer, der dich erinnert.

📋 Lektion 4.5 im Arbeitsblatt: deine Haushalts-Liste + dein Haushalts-Helfer-Bot + erste Tests
```

## Folien-Plan (14 Folien)

| # | Folie | Inhalt | Sprechnotizen |
|---|---|---|---|
| 1 | **Titel** | „4.5 · MASTERY · Dein Haushalts-Helfer-Bot" | „Willkommen zur MASTERY von Säule 4, und die ist mir besonders wichtig, weil sie zeigt, dass Mama-CEO nicht am Schreibtisch aufhört. Wir bauen jetzt den Zwilling deines Cockpit-Bots, nur diesmal für dein Zuhause, nämlich deinen Haushalts-Helfer." |
| 2 | **Der unsichtbare Mental Load** | Mama-Kopf voller Zettel: Wäsche · Zahnarzt · Geschenk · Kleider · Elternabend | „Mal ganz ehrlich: was wir Mamas im Kopf mit uns rumtragen, ist riesig. Wann muss die Wäsche, wer hat wann Zahnarzt, wann muss ich die Frühlingskleider raussuchen, das Geburtstagsgeschenk, der Elternabend. Das Schlimme ist, dass dieser Mental Load unsichtbar in deinem Kopf liegt und dich auch abends nicht loslässt. Genau den holen wir jetzt raus." |
| 3 | **Der Zwilling des Cockpit-Bots** | 2 Bots nebeneinander: 🌅 Cockpit (Business) · 🏠 Haushalts-Helfer (Zuhause) · „gleiche Mechanik" | „Das Schöne ist: du kannst schon alles, was du dafür brauchst. Der Haushalts-Helfer funktioniert genau wie dein Cockpit-Bot, er liest eine Liste und sagt dir morgens, was dran ist. Der Cockpit-Bot macht das fürs Business, der Haushalts-Helfer fürs Zuhause. Zwei Zwillinge, einmal Arbeit, einmal Familie." |
| 4 | **Was er für dich tut** | Beispiel-Antwort: „Montag — heute dran: Wäsche machen · Kind hat Zahnarzt 14 Uhr · Kind muss früher in die Schule (Wald)" | „So sieht das dann aus: du fragst morgens ‚was ist heute zu Hause dran', und er sagt dir zum Beispiel: Montag, heute Wäsche machen, das Kind hat um zwei Zahnarzt, und das andere muss früher los, weil Waldtag. Alles, was sonst in deinem Kopf herumschwirrt, kommt jetzt einmal am Morgen klar auf den Tisch." |
| 5 | **Die Quelle: dein Brain Dump aus Säule 2** | Pfeil: Hütchen-Inventar (S2) → Haushalts-Liste | „Und jetzt zahlt sich Säule 2 aus. Erinnerst du dich an dein Hütchen-Inventar, deinen grossen Brain Dump, wo alles rausgekommen ist, was du mit dir rumträgst? Genau das ist die Quelle. Diese ganzen ‚muss ich noch'-Sachen bringen wir jetzt in eine Liste, aus der dein Bot dich erinnert." |
| 6 | **Zwei Sorten Aufgaben + Termine** | 3 Zeilen: 🔁 wiederkehrend (Staubsaugen montags) · 📅 datiert (Kleider raus letzter Fr im März) · 👨‍👩‍👧 Familien-Termine (Zahnarzt, Schule) | „Deine Haushalts-Sachen sind von zwei Sorten, plus die Termine. Es gibt das Wiederkehrende, das immer am gleichen Tag dran ist, zum Beispiel Staubsaugen montags. Es gibt das Datierte, das einmal an einem bestimmten Tag kommt, zum Beispiel Frühlingskleider raussuchen am letzten Freitag im März. Und es gibt die Familien-Termine wie Zahnarzt oder Waldtag. Alle drei kommen in deine Liste." |
| 7 | **Wo die Liste lebt: Notion** | Notion-Haushalts-DB als eigene Liste · „wie dein Business in Notion lebt, lebt dein Haushalt jetzt auch dort" | „Und wo lebt diese Liste? In Notion, genau dort, wo schon dein Business-Brain liegt. Du legst dir eine eigene Haushalts-Liste an, mit Feldern für den Rhythmus, also montags oder monatlich, und für feste Daten. So wie dein Business in Notion ein Zuhause hat, kriegt jetzt auch dein Haushalt eins, und beide Bots schauen da rein." |
| 8 | **Live-Demo Schritt 1: Haushalts-Liste füllen** | Bildschirm: Notion-Haushalts-DB, Beispiele eintragen (aus Hütchen) | „So, jetzt bauen wir live, und du baust mit, pausier wo du musst. Schritt eins: ich öffne meine Haushalts-Liste in Notion und trage ein paar Sachen aus meinem Brain Dump ein. Wäsche, Rhythmus wöchentlich. Bäder putzen, mittwochs. Kleider wechseln, festes Datum Ende März. Du füllst deine eigene Liste mit dem, was bei dir ansteht." |
| 9 | **Live-Demo Schritt 2: Bot bauen (in Cowork)** | Bildschirm: Haushalts-Helfer-Vorlage (Bonus) in Cowork einfügen · Notion ist schon verbunden | „Schritt zwei: ich nehme die fertige Haushalts-Helfer-Vorlage, die du als Bonus hast, und setze sie in Cowork ein. Mein Notion ist von Lektion 4.4 schon verbunden, also liest er die Haushalts-Liste direkt. Das ist exakt dieselbe Mechanik wie beim Cockpit-Bot, du kannst das also schon — nur eine andere Liste, eine andere Vorlage." |
| 10 | **Live-Demo Schritt 3: testen** | Eingabe „Was ist heute zu Hause dran?" → Bot-Antwort mit Tagesliste | „Schritt drei, der schöne: ich frag ihn ‚was ist heute zu Hause dran', und schau, er gibt mir meine Haushalts-Sachen für heute plus die Termine der Kinder. Wie geil ist das denn, das musste ich vorher alles selbst im Kopf haben, und jetzt sagt's mir mein Helfer." |
| 11 | **So nutzt du beide Bots morgens** | Routine: Cockpit-Bot (Business) + Haushalts-Helfer (Zuhause) = ganzer Tag auf einen Blick | „Im Alltag fragst du morgens beide kurz: den Cockpit-Bot, was im Business dran ist, und den Haushalts-Helfer, was zu Hause dran ist. In zwei Minuten hast du deinen ganzen Tag klar vor dir, Business und Familie, ohne dass irgendwas nur noch in deinem Kopf liegt. Das ist für mich gelebter Mama-CEO." |
| 12 | **Stufe 2: auch hier automatisch möglich** | wie beim Cockpit: automatischer Telegram-Push via Claude Code · „kein Muss" | „Und ganz kurz, weil's die gleiche Logik ist wie beim Cockpit-Bot: auch deinen Haushalts-Helfer kannst du später als automatischen Telegram-Bot bauen, der dir morgens von selbst schreibt. Das braucht wieder etwas Technik und Hosting, ist also Stufe zwei und kein Muss. Für den Anfang reicht es völlig, dass du ihn fragst." |
| 13 | **Extra-Bonus: dein Kochassistent** | Karte: 🍳 Kochassistent (Wochenplan · Spontan-Koch · Einkaufsliste) — gleiche Mechanik, Vorlage liegt bei | „Und weil das ‚was koch ich heute' auch so ein Klassiker ist, hab ich dir noch einen Extra-Bonus dazugepackt: eine Vorlage für einen Kochassistenten. Der läuft nach genau demselben Prinzip, du gibst ihm deine Familie als Kontext, und er macht dir Wochenpläne, Spontan-Ideen und Einkaufslisten. Bau ihn dir, wann immer du Lust hast, du kannst das jetzt ja schon." |
| 14 | **Arbeitsblatt + nächste Lektion** | „📋 Haushalts-Liste + Haushalts-Helfer bauen + testen" · „Nächste Lektion: 4.6 — Mensch vs. KI" | „Im Arbeitsblatt bringst du jetzt deine Brain-Dump-Sachen in deine Haushalts-Liste und baust deinen Haushalts-Helfer mit der Vorlage. In der letzten Lektion von Säule 4 ziehen wir dann die Linie: was macht die KI, und was bleibt immer deins. Bis gleich." |

## Arbeitsblatt-Sektion 4.5

```
LEKTION 4.5 · MASTERY · Dein Haushalts-Helfer-Bot

▸ Schritt 1: Hol deinen Brain Dump aus Säule 2 raus
Nimm dein Hütchen-Inventar — alle „muss ich noch"-Sachen rund um Haushalt + Familie.

▸ Schritt 2: Sortier sie in 3 Sorten
🔁 WIEDERKEHREND (immer am gleichen Tag/Rhythmus)
| Aufgabe | Rhythmus (z.B. montags / monatlich) |
| _______________________ | ____________ |
| _______________________ | ____________ |
| _______________________ | ____________ |

📅 DATIERT (einmal an einem festen Datum, z.B. saisonal)
| Aufgabe | Datum |
| _______________________ | ____________ |
| _______________________ | ____________ |

👨‍👩‍👧 FAMILIEN-TERMINE (Arzt, Schule, Anlässe)
| Termin | Wann |
| _______________________ | ____________ |
| _______________________ | ____________ |

▸ Schritt 3: In Notion eintragen
☐ Haushalts-Liste in Notion angelegt (Felder: Aufgabe · Rhythmus · Datum · Bereich · erledigt)
☐ Wiederkehrende Sachen eingetragen
☐ Datierte Sachen eingetragen
☐ Familien-Termine eingetragen

▸ Schritt 4: Bot bauen (WÄHREND des Videos)
☐ Haushalts-Helfer-Vorlage (Bonus) in Cowork eingesetzt
☐ Notion verbunden (Bot liest die Haushalts-Liste direkt — Connector aus 4.4)
☐ Getestet mit „Was ist heute zu Hause dran?"
☐ Der Bot hat mir Haushalt + Termine für heute ausgegeben ✓
(Stufe 0 ohne Bot: Notion-Ansicht „Kommende Termine" + „nach Wochentag" öffnen.)

▸ Mein Haushalts-Helfer heisst: _______________________________

▸ Extra-Bonus Kochassistent — will ich den auch bauen?
☐ Ja, jetzt gleich  ☐ Später  (Vorlage liegt im Bonus-Bereich)

WAS DU NACH LEKTION 4.5 HAST · 2. KI-MITARBEITER LÄUFT
✓ Dein Mental Load liegt in einer Notion-Haushalts-Liste, nicht mehr nur im Kopf
✓ Dein Haushalts-Helfer-Bot erinnert dich täglich an Haushalt + Familien-Termine
✓ Du hast morgens jetzt zwei Helfer: Cockpit (Business) + Haushalts-Helfer (Zuhause)
✓ Du hast die Kochassistent-Vorlage als Extra-Bonus in der Hand
```

---

# 🎬 LEKTION 4.6 — KI-Wochenplan: Mensch vs. Maschine

**Status:** ⚠️ NEU bauen (9 Folien)
**Material:** Patricias Wochen-KI-Verteilung + Rückgriff auf 5 CEO-Aufgaben (S1 L1.4). Brücke zu Säule 5 (Mama-CEO-Matrix).

## ThriveCart-Setup

**Lektion-Titel:**
```
4.6 · KI-Wochenplan — was macht die KI, was bleibt deins
```

**Video-Datei:** `saeule-04-lektion-4-6.mp4` (ca. 10 Min)

**Beschreibungstext:**
```
Du hast jetzt zwei KI-Mitarbeiter. Die grosse Frage ist: welche Arbeit gibst du ihnen, und welche behältst du? Denn wer alles an die KI abgibt, verliert seine Stimme — und wer nichts abgibt, bleibt im Hamsterrad.

In dieser Lektion ziehst du eine klare Linie zwischen Mensch und Maschine. Du schaust dir deine Woche an und entscheidest pro Aufgabe: macht das die KI, oder bleibt das bei mir?

Du lernst:
→ Die einfache Regel, was zur KI darf und was nicht
→ Warum deine 5 CEO-Aufgaben aus Säule 1 immer deins bleiben
→ Wie du deinen KI-Wochenplan baust — Aufgabe für Aufgabe
→ Den Ausblick auf Säule 5, wo aus dieser Linie deine Mama-CEO-Matrix wird

Am Ende weisst du nicht nur, DASS KI dir hilft, sondern genau WO — und wo du als Mensch unersetzlich bist.

📋 Lektion 4.6 im Arbeitsblatt: dein KI-Wochenplan (Mensch vs. Maschine)
```

## Folien-Plan (9 Folien)

| # | Folie | Inhalt | Sprechnotizen |
|---|---|---|---|
| 1 | **Titel** | „4.6 · KI-Wochenplan — Mensch vs. Maschine" | „Letzte Lektion von Säule 4, und hier ziehen wir die wichtigste Linie überhaupt: was macht ab jetzt die KI, und was bleibt immer deins. Denn beides falsch zu machen kostet dich, und ich zeig dir wie du's richtig aufteilst." |
| 2 | **Du hast jetzt 2 Mitarbeiter** | Rückblick: 🌅 Cockpit-Bot · 🏠 Haushalts-Helfer · „wie teilst du die Arbeit?" | „Schau, was du in den letzten Lektionen aufgebaut hast: einen Cockpit-Bot fürs Business und einen Haushalts-Helfer fürs Zuhause. Zwei Mitarbeiter, die nie müde werden. Die Frage ist jetzt nur noch, welche Arbeit du ihnen gibst, ohne dass du dich selbst überflüssig machst." |
| 3 | **Die zwei Fehler** | links: alles abgeben (Stimme weg) · rechts: nichts abgeben (Hamsterrad) | „Es gibt zwei Fehler. Der eine ist, alles an die KI abzugeben, dann klingt dein Business austauschbar und deine Kundinnen spüren, dass keine echte Frau mehr dahintersteht. Der andere ist, aus Stolz oder Angst gar nichts abzugeben, dann bleibst du im Hamsterrad aus Säule 2. Die Kunst liegt in der Mitte." |
| 4 | **Die einfache Regel** | 2 Spalten: KI = Wiederholbares + Vorbereitendes · DU = Beziehung + Entscheidung + Stimme | „Und die Regel dafür ist erstaunlich einfach. Die KI macht alles, was wiederholbar oder vorbereitend ist, also Recherche, erste Entwürfe, Pläne, Listen, Zusammenfassungen. Und du machst alles, wo es um Beziehung, Entscheidung und deine Stimme geht. Die KI bereitet vor, du entscheidest und gibst den letzten Schliff." |
| 5 | **Was zur KI darf** | grüne Liste: Recherche · erste Entwürfe · Wochen-/Essenspläne · Listen · Zusammenfassungen · Morgenbriefing | „Konkret darf zur KI: Recherche, erste Entwürfe von Texten, deine Wochenplanung und deine Essensplanung, Listen aller Art, Zusammenfassungen von langen Sachen, und natürlich dein Morgenbriefing. All das, was Zeit frisst, aber nicht zwingend dein Herzblut braucht." |
| 6 | **Was deins bleibt: die 5 CEO-Aufgaben** | rote Liste = 5 CEO-Aufgaben aus S1: Vision/Strategie · Entscheidungen · Brand/Stimme · Beziehungen · Reflexion | „Und was bleibt immer deins? Genau die fünf CEO-Aufgaben aus Säule 1. Deine Vision und Strategie, deine Entscheidungen, deine Brand und deine Stimme, deine Beziehungen zu den Kundinnen, und deine Reflexion. Das ist der Kern, warum dich Menschen buchen, und den gibst du nie an eine Maschine ab." |
| 7 | **Dein KI-Wochenplan** | Wochen-Grid: pro Aufgabe ein Stempel 🤖 KI oder 🙋 ich | „Jetzt machen wir's konkret für deine Woche. Du nimmst deine Aufgaben und stempelst hinter jede entweder ‚KI' oder ‚ich'. Das Morgenbriefing kriegt KI, das Kundengespräch kriegst du, der erste Caption-Entwurf KI, die finale Stimme du. So siehst du auf einen Blick, wo dir Stunden geschenkt werden." |
| 8 | **Vorschau Säule 5** | Pfeil: aus „Mensch vs. KI" → Mama-CEO-Matrix (ich · KI · System · raus) | „Und das hier ist erst der Anfang, denn in Säule 5 bauen wir diese Linie zur vollen Mama-CEO-Matrix aus. Da kommen noch zwei Felder dazu: was kann ein System ohne KI übernehmen, und was darf einfach ganz weg. Aber das Fundament, Mensch gegen Maschine, das legst du hier." |
| 9 | **Arbeitsblatt + Säule 4 komplett** | „📋 Dein KI-Wochenplan" · „Säule 4 abgeschlossen — Live-Call 3 (Bot-Bau-Werkstatt)" | „Im Arbeitsblatt baust du jetzt deinen KI-Wochenplan und stempelst jede Aufgabe. Damit hast du Säule 4 abgeschlossen: zwei KI-Mitarbeiter laufen, und du weisst genau wo Mensch aufhört und Maschine anfängt. Wir sehen uns im Live-Call 3, der Bot-Bau-Werkstatt, wo wir gemeinsam an deinen Bots feilen. Ich freu mich drauf." |

## Arbeitsblatt-Sektion 4.6

```
LEKTION 4.6 · KI-Wochenplan — Mensch vs. Maschine

▸ Die Regel in deinen Worten
KI macht: _______________________________
Ich mache: _______________________________

▸ Deine 5 CEO-Aufgaben — bleiben IMMER deins (Häkchen zur Erinnerung)
☐ Vision & Strategie  ☐ Entscheidungen  ☐ Brand & Stimme
☐ Beziehungen  ☐ Reflexion & Zahlen

▸ Dein KI-Wochenplan — stempel jede Aufgabe
Nimm 10-12 typische Aufgaben deiner Woche. Schreib hinter jede 🤖 (KI) oder 🙋 (ich).
| Aufgabe | 🤖 KI / 🙋 ich |
| _______________________ | ____ |
| _______________________ | ____ |
| _______________________ | ____ |
| _______________________ | ____ |
| _______________________ | ____ |
| _______________________ | ____ |
| _______________________ | ____ |
| _______________________ | ____ |
(weiter auf der Rückseite)

▸ Dein grösster „Aha"
Welche Aufgabe gibst du ab heute an die KI ab, die du bisher selbst gemacht hast?
_______________________________

WAS DU NACH LEKTION 4.6 HAST · SÄULE 4 KOMPLETT
✓ Du kennst die Regel: KI bereitet vor, du entscheidest
✓ Deine 5 CEO-Aufgaben bleiben geschützt deins
✓ Dein KI-Wochenplan steht — jede Aufgabe gestempelt
✓ Du hast Säule 4 abgeschlossen: 2 KI-Mitarbeiter + klare Mensch-Maschine-Linie
✓ Du bist bereit für Säule 5 (Mama-CEO-Matrix)
```

---

## 🎁 Die 4 Bonus-Vorlagen — Spezifikation für den Bau

Alle werden als sauberer Text geliefert. Die Mentee fügt sie in **Claude Cowork** als Bot-Anweisung ein (oder in Claude Code, Stufe 2). Platzhalter in `[eckigen Klammern]` ersetzt sie mit eigenem Kontext. **Compliance:** keine Heilversprechen, keine erfundenen Zahlen, kein Mentor-Name.

**Bonus 1 (Cockpit) + Bonus 2 (Haushalts-Helfer)** sind im Preis enthalten und werden in L4.4/L4.5 gebaut. **Bonus 3 (Kochassistent)** ist ein Extra-Bonus zum Selber-Bauen. **Bonus 4 (Gratis-Chat-One-Shot)** ist die Notlösung für alle, die kein Pro-Abo/Cowork wollen — einmal reinwerfen, Tag sortiert.

### Bonus 1 — Cockpit-Bot-System-Prompt (für L4.4, Stufe 1)

```
ROLLE
Du bist mein persönlicher Cockpit-Bot — mein Morgenbriefing-Assistent.
Dein Job ist, mir jeden Morgen in 30 Sekunden Klarheit zu geben, was heute dran ist.

MEIN KONTEXT
[Hier füge ich meinen Business-Brief aus Lektion 4.3 ein.]

WAS DU BEKOMMST
Ich gebe dir meine aktuelle Notion-Woche (Wochenfokus, Tagesplaner, Aufgaben, Ziele).
Wenn etwas fehlt, frag kurz nach, statt zu raten.

WAS DU TUST, wenn ich „Was ist heute dran?" frage:
1. Nenne mir meinen TAGESFOKUS in einem Satz.
2. Liste meine 3 WICHTIGSTEN AUFGABEN heute (Money-Making + Termine zuerst).
3. Gib mir einen kurzen WOCHENBLICK (1-2 Sätze: wo stehe ich, was kommt noch).
4. Schliesse mit EINEM motivierenden, ehrlichen Satz — kein Kitsch.

REGELN
- Halte dich kurz und konkret, keine Romane.
- Sprich mich mit DU an, warm und direkt, wie eine gute Freundin.
- Erfinde keine Termine oder Zahlen — nur was in meiner Notion-Woche steht.
- Wenn ein Tag voll ist, hilf mir priorisieren, statt alles gleich wichtig zu machen.
- [Meine Tabus aus dem Business-Brief gelten auch hier.]
```

### Bonus 2 — Haushalts-Helfer-Bot-System-Prompt (für L4.5, Stufe 1)

```
ROLLE
Du bist mein persönlicher Haushalts-Helfer — der Zwilling meines Cockpit-Bots,
nur für zu Hause. Dein Job ist, mir jeden Morgen zu sagen, was an Haushalt und
Familie heute dran ist, damit das nicht mehr alles in meinem Kopf liegt.

MEIN KONTEXT
Wir sind eine Familie mit [Anzahl] Kindern.
Besonderheiten der Woche: [z.B. Mann Mo-Do auswärts, Mittwoch alle zu Hause].

WAS DU BEKOMMST
Ich gebe dir meine Notion-Haushalts-Liste. Darin stehen 3 Sorten Einträge:
- WIEDERKEHREND mit Rhythmus (z.B. „Wäsche – montags", „Bäder – mittwochs")
- DATIERT mit festem Datum (z.B. „Frühlingskleider raussuchen – letzter Freitag im März")
- FAMILIEN-TERMINE mit Datum/Uhrzeit (z.B. „Kind Zahnarzt – Mo 14 Uhr", „Waldtag – Mo")
Wenn etwas fehlt, frag kurz nach, statt zu raten.

WAS DU TUST, wenn ich „Was ist heute zu Hause dran?" frage:
1. Liste die WIEDERKEHRENDEN Aufgaben, die heute nach Rhythmus dran sind.
2. Liste DATIERTE Sachen, die heute (oder diese Woche) fällig sind — rechne dabei
   Datumsregeln wie „letzter Freitag im März" korrekt aus.
3. Liste die FAMILIEN-TERMINE von heute (mit Uhrzeit).
4. Gib einen kurzen Ausblick: was kommt diese Woche noch Wichtiges.

REGELN
- Halte dich kurz und konkret, eine klare Tagesliste, keine Romane.
- Sprich mich mit DU an, warm und alltagsnah.
- Erfinde keine Aufgaben oder Termine — nur was in meiner Liste steht.
- Wenn heute nichts ansteht, sag mir das ehrlich („heute zu Hause nichts Fixes").
```

### Bonus 3 — Kochassistent-System-Prompt (Extra-Bonus, in L4.5 erwähnt)

```
ROLLE
Du bist mein persönlicher Kochassistent.
Dein Job ist, mir das tägliche „was koch ich heute" abzunehmen — mit Wochenplänen,
Spontan-Ideen aus dem was da ist, und sortierten Einkaufslisten.

MEINE FAMILIE (Kontext)
Wir sind [Anzahl] Personen, davon [Anzahl] Kinder.
Wir essen gern: [Lieblingsessen / Stil, z.B. proteinreich, frisch].
Kommt NIE auf den Tisch: [no-gos / Allergien].
Besonderheiten: [z.B. eigenes Brot, schnelle Gerichte unter der Woche].

DEINE 3 AUFGABEN
1. WOCHENPLAN: Wenn ich frage, gib mir einen Plan (Mittag/Abend nach Wunsch),
   passend zu meiner Familie und meinem Stil.
2. SPONTAN-KOCH: Wenn ich dir Zutaten nenne, schlag mir 1-2 konkrete Gerichte vor —
   mit Mengen für meine Personenzahl.
3. EINKAUFSLISTE: Auf Wunsch gib mir die Liste zum Plan, sortiert nach
   Kategorien (Gemüse, Milchprodukte, …) oder nach Laden.

REGELN
- Frag nach, wenn dir Infos fehlen (z.B. wie viele Tage, Mittag oder Abend).
- Keine ausgefallenen Spezialzutaten, die ich im normalen Laden nicht kriege —
  ausser ich frage ausdrücklich danach.
- Wenn ich sage „das mögen wir nicht", merk es dir für nächste Vorschläge.
- Sprich mich mit DU an, locker und alltagsnah.
```

### Bonus 4 — Gratis-Chat-One-Shot-Prompt (Stufe 0,5 · ohne Abo/Connector)

Für alle, die (noch) kein Pro-Abo oder Cowork wollen: einmal in ein leeres Gratis-Chatfenster (ChatGPT oder Claude) kopieren und die eigene Liste darunter einfügen.

```
Du bist mein Tagesassistent. Unten kommt meine Liste (Business-Woche und/oder
Haushalt + Familien-Termine). Sag mir bitte für HEUTE
(Datum: [heute eintragen], Wochentag: [Wochentag eintragen]):
1. Meine 3 wichtigsten Aufgaben (Money-Making + Termine zuerst)
2. Was an Haushalt/Familie heute dran ist
3. Was diese Woche noch Wichtiges kommt (1-2 Sätze)
Halte dich kurz, sprich mich mit DU an, erfinde nichts — nur was in meiner Liste steht.

MEINE LISTE:
[hier deine Notion-Woche bzw. Haushalts-Liste reinkopieren]
```

> Grenze ehrlich: Das ist eine Einmal-Nutzung ohne Gedächtnis und ohne Notion-Anbindung — du kopierst jedes Mal neu rein. Für „läuft mit" → Cowork (Stufe 1).

---

## 📋 Zusammenfassung: was Patricia produzieren muss für Säule 4

> **✅ STAND 2026-06-25 — bereits gebaut:** Master (3-Stufen/Cowork) · 4 Bonus-Vorlagen (`bonus-vorlagen-saeule-4/`) · Arbeitsblatt (`04-arbeitsblaetter/mama-ceo-arbeitsblatt-saeule-4.docx`, validiert) · ThriveCart-Setup (`13-thrivecart-saeule-4-setup.md`) · Notion Mentee-Haushalts-DB im Master-Template (`a52526bf-4d9a-48e6-9f64-5cce1239b66e`) + Beispielzeilen + 3 Stufe-0-Views · 3 Stufe-0-Views auf Patricias eigener DB (`caf1c565-...`).
> **✅ 6 PPTX gebaut 2026-06-25** — `03-praesentationen/saeule-4/`, Säule-3-Brand-Look, Sprechnotizen pro Folie. **Säule 4 ist damit komplett produziert** (nur noch aufnehmen).

### Videos (6 Lektionen, ~85 Min total) — ✅ PPTX gebaut
| # | Datei (PPTX) | Status |
|---|---|---|
| 4.1 | `03-praesentationen/saeule-4/01-lektion-4-1.pptx` | ✅ 9 Folien |
| 4.2 | `.../02-lektion-4-2.pptx` | ✅ 10 Folien |
| 4.3 | `.../03-lektion-4-3.pptx` | ✅ 10 Folien (inkl. Buch-Technik) |
| 4.4 | `.../04-lektion-4-4.pptx` | ✅ 13 Folien — Live-Demo Cockpit-Bot (Cowork) |
| 4.5 MASTERY | `.../05-lektion-4-5.pptx` | ✅ 14 Folien — Live-Demo Haushalts-Helfer (Cowork) |
| 4.6 | `.../06-lektion-4-6.pptx` | ✅ 9 Folien |

→ **6 PPTX im einheitlichen Säule-4-Brand-Look** (python-pptx, Creme F1ECDD/Navy/Petrol/Orange wie Säule 3, ✓-Häkchen, Sprechnotizen pro Folie).
→ ⚠️ Visuelles Rendern lokal nicht möglich (kein LibreOffice) — Inhalts-QA bestanden (Folienzahl + Titel + Notizen). Patricia: beim ersten Öffnen kurz durchklicken, ob Textmengen passen.
→ **Aufnahme-Hinweis:** L4.4 + L4.5 sind Live-Demos mit Screenshare (Bot bauen). Patricia braucht ihren Bildschirm + **Claude Cowork** + Notion + die Vorlagen offen.

### Notion-Master-Template erweitern (Bau-Voraussetzung für L4.5)
Das bestehende Master-Template (`3637078e-8b7e-8121-9f95-d2b377b283a7`) braucht eine zusätzliche **Haushalts-DB**: Aufgabe · Bereich · Rhythmus · Wochentag · Fixes Datum · Wer · Notiz · Erledigt. Daraus liest der Haushalts-Helfer-Bot. **+ 3 Stufe-0-Views** (📅 Kommende Termine · 🗓 nach Wochentag · 🔁 nach Rhythmus). Prototyp existiert als Patricias eigene DB (`caf1c565-9c66-46bb-ae03-73d029b91d87`).

### Arbeitsblatt (1 .docx-Datei)
`mama-ceo-arbeitsblatt-saeule-4.docx` — 6 Lektions-Sektionen wie oben: KI-Frust-Check + 3 Zutaten · **Stufen-Entscheidung (Notion / Cowork / Claude Code)** · Business-Brief (6 Bausteine) · Cockpit-Bot-Bau-Checkliste (Cowork) + 3-Tage-Test · Haushalts-Liste sortieren (wiederkehrend/datiert/Termine) + Haushalts-Helfer-Bau · KI-Wochenplan (Mensch-vs-Maschine-Stempel).

### 4 Bonus-Vorlagen (als Download-Dateien)
- 🌅 **Cockpit-Bot-System-Prompt** (im Preis) → Download bei L4.4
- 🏠 **Haushalts-Helfer-Bot-System-Prompt** (im Preis) → Download bei L4.5
- 🍳 **Kochassistent-System-Prompt** (Extra-Bonus) → Download bei L4.5
- 💬 **Gratis-Chat-One-Shot-Prompt** (Extra-Bonus, Stufe 0,5) → für alle ohne Abo
- → alle als `.md`/`.txt` exportieren (Spezifikationen oben)

### ThriveCart-Setup-File
`13-thrivecart-saeule-4-setup.md` — Säulen-Header + 6 Beschreibungstexte (copy-paste-ready) + Upload-Checkliste (6 Videos · 1 Arbeitsblatt · 3 Bot-Vorlagen) — analog zu `13-thrivecart-saeule-3-setup.md`. **Noch zu bauen.**

---

## ❓ Offene Fragen an Patricia (vor PPTX-Bau zu klären)

| Lektion | Frage | Status |
|---|---|---|
| **4.2** | Tool-Modell = **3 Stufen** (0 Notion · 1 Claude Cowork · 2 Claude Code). Nackter Chat zu statisch · Cowork = Nicht-Techie-Weg mit Connector · jede nimmt einen Win mit. | ✅ geklärt 2026-06-25 (Patricia) |
| **4.4** | Cockpit-Bot 3-Stufen: **Stufe 1 = Claude Cowork** (statt „Projekt"), Stufe 2 = Telegram via Claude Code (Hosting + Kosten ehrlich). | ✅ geklärt 2026-06-25 |
| **4.4** | Ads-Performance-Diagnose im Cockpit-Bot-Prompt → bewusst WEGGELASSEN (Bot erinnert nur an die Notion-Planung). | ✅ geklärt 2026-06-12 |
| **4.5** | MASTERY = Haushalts-Helfer-Bot (Mental-Load, Brain-Dump aus S2, Notion-Haushalts-DB), Stufe 1 Cowork. Kochassistent = Extra-Bonus. | ✅ geklärt 2026-06-12 |
| **4.5** | Notion-Master-Template um Haushalts-DB + 3 Stufe-0-Views erweitern. Patricias eigene DB = Prototyp. | ⏳ noch anlegen |
| **alle** | Wie bei Säule 3: visuelles PPTX-Rendern lokal nicht möglich (kein LibreOffice) — Inhalts-QA per python-pptx, Patricia klickt einmal durch. | ℹ️ wie gehabt |

---

## 🔗 Verwandte Notizen

- `outputs/produkte/mama-ceo/01-inhaltsverzeichnis-v4-FINAL-5-saeulen.md` — verbindliche 5-Säulen-Outline (Säule 4 = Zeilen 110-127)
- `outputs/produkte/mama-ceo/10-saeule-3-MASTER.md` — Notion-Business-Brain (das der Cockpit-Bot liest) · Format-Vorlage
- `outputs/produkte/mama-ceo/10-saeule-1-MASTER.md` — 5 CEO-Aufgaben (Mensch-vs-Maschine-Grenze in L4.6)
- `outputs/produkte/mama-ceo/10-saeule-2-MASTER.md` — 4-Filter „Automatisieren" + Hütchen-Inventar (Adminkram-Quelle)
- `context/patricia-vollprofil.md` — Section 4 (KI-Stack) als Beweis-Material + Brand-Voice
- Memory: `project_cockpit-bot-live.md` — Patricias echter Cockpit-Bot (Stufe-2-Referenz für L4.4)
- `scripts/cockpit-bot/` — Quellcode des echten Bots (intern, NICHT in Customer-Material)
- `context/meal-planning-bot.md` + `scripts/kochbot-rag/` — Patricias /mealplan-Logik (Stoff-Quelle für L4.5, vereinfacht)
- Memory: `feedback_KRITISCH-mama-ceo-outline-verbindlich.md` · `project_mama-ceo-modulbau.md`
- Compliance: Familien-Notfall-Bezüge nur abstrakt · keine Heilversprechen in Bot-Vorlagen
