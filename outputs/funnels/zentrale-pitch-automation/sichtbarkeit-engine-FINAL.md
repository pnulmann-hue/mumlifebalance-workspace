---
tags: [funnel, mba, pitch-automation, intern]
---

# 🚀 Sichtbarkeits-Engine — FINALE Bauversion (v1)

> **Erstellt:** 2026-07-14 · **Supersedes** [[variante-C-mailsequenz]] für den Sichtbarkeits-Pillar.
> **Entscheid Patricia 2026-07-14 (via /funnel):** Evergreen-System, jedes 0€-Freebie läuft durch **eine** Maschine, Ziel immer MBA, Signature als Downsell.
> **Modell = Variante C** (hoch ankern → Diagnose-Downsell), Julias 2026-Funnel-Logik: *„über allem steht 1 Kauf, alle Einstiege laufen zusammen."*
> INTERN. Blacklist-geprüft (keine Stakkato, kein „Stell dir vor", kein „6-stellig", kein Mentorin-Name, keine erfundenen Zahlen, Schweizer ss).

---

## Die 4 Entscheidungen, die diese Version festlegen

| Frage | Entscheid | Konsequenz im Bau |
|---|---|---|
| Dringlichkeit | **Sanft — MBA immer offen**, kein Deadline Funnel | Kein hartes „schliesst am [DATUM]". Weiche Pioneer-Dringlichkeit (997 solange Pioneer-Runde). Webinar = **optional**, Link-Swap später. |
| 0€-Brücke | **Passender Minikurs „Finde dein Thema" (39)** zuerst | Nie 0 → 997 kalt. Erst kleiner Kauf/Win. |
| Reihenfolge | Freebie → **39 → MBA 997 → Signature 333** | MBA ist Ziel, Signature ist Auffangnetz. |
| Downsell | **Alle 3 Signatures** als Selbst-Diagnose (nicht 1 geraten) | Downsell wird **geteilt** über alle Pillars. Nur die Brücke bleibt themen-spezifisch. |
| MBA-Track-Länge | **5 Mails, dann Loop** (Julia-Stil) | straff, hoher Druck, dann grosser Verteiler. |
| Umfang v1 | **Sichtbarkeits-Pillar komplett** als Vorlage | danach für Zeit/Mama-CEO + Produktwelt geklont (nur Brücke tauschen). |

---

## 🏗️ Was ist geteilt, was pillar-spezifisch?

```
  SICHTBARKEITS-FREEBIES (Bio-Check · Lead · Story · Starterguide · Von 0 auf echt · Potenzial-Test)
        │  je eigene Auslieferungs-Mail (Link unterschiedlich) → Tag: engine-sichtbarkeit-start
        ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  DIE EINE ENGINE-AUTOMATION (Trigger: engine-sichtbarkeit-start) │
  │                                                             │
  │  ▸ BRÜCKE (2 Mails) ......... pillar-spezifisch (Sichtbarkeit) │
  │  ▸ MBA-TRACK (5 Mails) ...... GETEILT über alle Pillars        │
  │  ▸ DOWNSELL (1 Mail) ........ GETEILT (3-Türen-Diagnose)       │
  │  ▸ → Loop / grosser Verteiler .. GETEILT                       │
  └─────────────────────────────────────────────────────────────┘
```

→ Für Pillar 2 (Zeit/Mama-CEO) & Pillar 3 (Produktwelt) baust du später **nur die 2 Brücken-Mails neu**. Der ganze Rest wird 1:1 wiederverwendet.

---

## ⚙️ Der ActiveCampaign-Aufbau (Klick-Plan)

**Baut auf dem auf, was schon da ist** (siehe [[umbau-plan]] · [[ac-ist-zustand]]) — nichts wird neu von Null gebaut.

### Trigger = dein bestehender Tag (kein neuer nötig!)
**Automation 72 „Automation 0€ Produkt"** (erstellt 14.7.) ist die zentrale Maschine. Trigger = **Tag 87 „Automation 0€ Produkt"**, den alle 0€-Leads schon bekommen. Keine Auslieferungs-Automation muss angefasst werden.

**Tags (alle vorhanden — angelegt 2026-07-14):**
| Tag | ID | Wann gesetzt | Zweck |
|---|---|---|---|
| Automation 0€ Produkt | **87** | von allen 0€-Auslieferungen (nicht doTERRA) | **Trigger** der Engine |
| Engine Minikurs gekauft | **88** | Kauf „Finde dein Thema" 39 | überspringt Rest der Brücke |
| mba-kauf | **79** | Kauf MBA | **Exit** aus der ganzen Engine |
| Engine Pitch ohne Kauf | **89** | Ende ohne Kauf | ab in grossen Verteiler |

> `stufe:kunde-signature` weggelassen — Signature-Kauf am Downsell-Ende wird über das AC-Kauf-Ziel des jeweiligen 333ers abgefangen (existiert bereits).

### doTERRA — sauber getrennt ✅
Bestätigt Patricia 14.7.: der „0€ doTERRA Energiekick" (Automation 70) setzt Tag 87 **nicht**. doTERRA landet also gar nicht erst in der Engine. Der Ausstiegs-Schritt unten bleibt als **optionales Sicherheitsnetz** drin, ist aber kein Muss.

### Flow (klickst du 1× zusammen — ich liefere Klick-Anleitung)
```
TRIGGER: Tag 87 "Automation 0€ Produkt" hinzugefügt
  │
  ├─ (optional) SCHRITT 0: wenn Liste "doTERRA Interessenten" (18) → BEENDEN
  ├─ ZIEL (gilt ganze Automation): Tag "mba-kauf" (79) → Automation SOFORT beenden
  │
  ▼ BRÜCKE (themen-neutral — gilt für alle Mentoring-Freebies)
  Mail E1 (Wert)              — warten 2 Tage
  WENN Tag "Engine Minikurs gekauft" (88) → springe zu MBA-Track   (Käuferin, kein 39-Pitch mehr)
  Mail E2 (Minikurs 39)      — warten 3 Tage
  │
  ▼ MBA-TRACK (5 Mails)
  Mail M1 (Wende-Story → MBA) — warten 2 Tage
  Mail M2 (alles aus 1 Hand)  — warten 1 Tag
  Mail M3 (Einwände)          — warten 1 Tag
  Mail M4 (für wen · Beweis)  — warten 1 Tag
  Mail M5 (Pioneer sanft)     — warten 2 Tage
  │
  ▼ DOWNSELL
  Mail D1 (3 Türen)           — warten 2 Tage
  WENN 333-Kauf-Ziel erreicht → Ende (ab in Loop-Verteiler)
  │
  ▼ ENDE
  Tag "Engine Pitch ohne Kauf" (89) setzen → grosser Verteiler
```

**Anti-Doppel-Regel (dein Kernanliegen):** Holt jemand ein 2. Sichtbarkeits-Freebie, während sie schon in der Engine ist → nur Asset ausliefern, **keinen** `engine-sichtbarkeit-start`-Tag erneut. In der jeweiligen Auslieferung als erste Bedingung: *„wenn schon in Engine ODER Kundin → Tag nicht setzen."*

---

## ✉️ Die Mails (baufertig, deine Stimme)

Links: **MBA = https://mumlifebalance.ch/mba/** ✅ eingesetzt. Offen: `https://mumlifebalance.thrivecart.com/thema-finden/` (Finde dein Thema 39) · `https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/` · `https://mumlifebalance.thrivecart.com/mama-ceo/` · `https://mumlifebalance.thrivecart.com/digitale-produktwelt/` (ThriveCart-Checkouts). Kundenstimme M2 ✅ echt eingesetzt (freigegeben). Jede Mail im Design `context/mail-design-onlinebusiness.html`, **1 CTA pro Mail**.

---

### BRÜCKE

#### Mail E1 · Tag 0 · Warum ich Network von Anfang an anders gedacht hab
**Betreff A:** Warum ich Network von Anfang an anders gedacht hab
**Betreff B:** Niemand wacht morgens auf und will ätherische Öle
**Preheader:** Der Gedanke, auf dem mein ganzes Business steht.

Schön, dass du da bist. Ich fang gleich mit dem an, worauf bei mir alles aufbaut.

Ich hab Network von Anfang an anders gedacht. Nicht das klassische „ich verkauf dir Produkt XY, und hier noch schnell eine Produktparty, und da noch ein Katalog". Das klingt vielleicht komisch aus dem Mund von einer, die selber im Network ist — aber lies mal kurz weiter, dann verstehst du, was ich meine.

Stell dir vor, du gehst an eine Hochzeit. Du hast ein richtig geiles violettes Kleid, nur die passenden Schuhe fehlen. Du läufst durch die Stadt und weisst ganz genau, was du brauchst. Und jetzt sag mir ehrlich: gehst du in den Laden, wo im Schaufenster lauter Krimskrams liegt und man gar nicht sieht, was es drin überhaupt gibt? Nein. Du gehst dorthin, wo im Schaufenster sofort klar ist — hier gibt es Schuhe.

In gewisser Weise ist jede Kundin wie diese Frau, die ihre Schuhe sucht. Denn niemand wacht morgens auf und denkt „shit, ich brauch jetzt unbedingt ätherische Öle" oder „krass, ich sollte mal die neue Gesichtscreme von Ringana bestellen". So ticken wir Menschen einfach nicht. Wir suchen insgeheim immer nach einer Lösung für unser Problem, auch wenn wir das Problem bewusst noch gar nicht in Worte fassen. Wir wollen keinen Shake — wir wollen uns endlich wieder heiss im Bikini fühlen, so wie vor den Kindern.

Verstehst du, worauf ich hinaus will? Dein Produkt ist nie das Thema. Das Problem deiner Kundin ist das Thema, und dein Produkt ist bloss das Werkzeug dahinter.

Und weil das die Grundlage von absolut allem ist, was danach kommt — von deiner Bio über deine Posts bis zu deinem Angebot — fangen wir genau da an. Ich hab dir einen kleinen Kurs gebaut, der dich in unter zwei Stunden zu deinem Thema führt: „Finde dein Thema als Network-Mama", für 39 Franken, weniger als ein Familien-Znacht auswärts. Wenn du magst, ist das dein erster Schritt.

Liebe Grüsse
Patricia

**CTA-Button:** Mein Thema finden für 39 CHF → https://mumlifebalance.thrivecart.com/thema-finden/

---

#### Mail E2 · Tag 2 · Zweit-Kontakt: dein Thema finden (39)
**Betreff A:** Du brauchst kein neues Logo. Du brauchst ein Thema.
**Betreff B:** 3 Fragen, die dir dein Thema zeigen
**Preheader:** Der erste Schritt, damit die richtige Frau sich meldet.

Vor zwei Tagen hab ich dir erzählt, warum dein Produkt nie das Thema ist, sondern immer das Problem deiner Kundin. Heute zeig ich dir, wie du deins findest, damit du nicht ewig im Kopf danach suchst.

Nimm dir fünf Minuten und beantworte diese drei Fragen ehrlich:

1. Wofür kommen Leute jetzt schon zu dir, ganz ohne dass du etwas verkaufst?
2. Was hast du selber durchgemacht und für dich gelöst?
3. Worüber kannst du zehn Minuten reden, ohne Notizen?

Die Schnittmenge aus den dreien ist dein Thema. Schreib es auf, bevor der Alltag dich wieder schluckt.

Wenn du das nicht alleine zusammenpuzzeln willst, hab ich dir genau dafür einen kleinen Kurs gebaut: „Finde dein Thema als Network-Mama". In unter zwei Stunden hast du dein Thema schwarz auf weiss, für 39 Franken — weniger als ein Familien-Znacht auswärts.

Liebe Grüsse
Patricia

**CTA-Button:** Mein Thema finden für 39 CHF → https://mumlifebalance.thrivecart.com/thema-finden/

---

### MBA-TRACK (5 Mails · geteilt über alle Pillars)

#### Mail M1 · Tag 4 · Wende-Story → das grosse Bild (MBA)
**Betreff A:** Ich war mit meiner Tochter im Wellness, als die Mail kam
**Betreff B:** „Zahlungseingang." — und ich hatte gar nichts gemacht
**Preheader:** Das war kein Zufall. Das war ein System.

Ich sass mit meiner Tochter im Wellness, das Handy eigentlich weg, und dann kam diese Mail rein: Zahlungseingang. Jemand hatte über mein Instagram-Profil einfach gekauft, während ich im Bademantel lag. Mega puff, ich konnte es kaum fassen.

Das Verrückte daran ist, dass das kein Glück war. Das passiert, seit bei mir vier Dinge zusammenspielen — mein Thema, eine Positionierung, die sofort verstanden wird, ein Angebot, das wirklich passt, und ein KI-System, das im Hintergrund weiterläuft, auch wenn ich gerade Mama bin. Seitdem gibt es bei mir keinen Monat mehr ohne Verkauf, mit 18 Stunden Arbeit pro Woche und vier Kindern.

Ein Stück davon kannst du sofort mitnehmen: ein einziger Beitrag pro Woche, der ein echtes Problem deiner Wunschkundin löst, bringt dir mehr als zehn Produktbilder. Fang genau da an.

Wie diese vier Teile ineinandergreifen — und wie du sie der Reihe nach bei dir aufbaust — steckt komplett in der Mum Business Academy. Schau sie dir in Ruhe an.

Liebe Grüsse
Patricia

**CTA-Button:** Die Academy ansehen → https://mumlifebalance.ch/mba/

---

#### Mail M2 · Tag 6 · MBA — alles aus einer Hand + Beweis
**Betreff A:** Fünf Kurse zusammenstückeln oder einmal richtig
**Betreff B:** Was drin ist, wenn du nicht mehr alleine puzzeln willst
**Preheader:** Die Mum Business Academy — und warum sie alles abdeckt.

„Wo soll ich überhaupt anfangen?" — diese Frage kriege ich fast täglich. Und ich versteh sie gut, weil du an zehn Ecken gleichzeitig ziehst: Thema, Posten, eigenes Produkt, Zeit, Technik. Da verzettelt man sich.

Genau dafür gibt es die Mum Business Academy. Da ist alles drin, in der richtigen Reihenfolge:

- dein Thema und deine Positionierung, damit die richtigen Frauen sich melden
- dein eigenes digitales Produkt, Schritt für Schritt aufgebaut
- dein KI-System, das dir den Adminkram im Business und im Haushalt abnimmt
- der Weg von „paar hundert Franken" zu echtem, planbarem Einkommen
- dazu zweimal im Monat ein Live-Call mit mir und mit Expertinnen, damit du nie stecken bleibst

Eine Teilnehmerin hat es so gesagt: *„Mir wurde auf einmal klar, wie ich mein Business immer angeschaut habe — immer von mitten drin, statt aus einer anderen Perspektive. Ich hatte das grosse Ganze nie richtig gesehen."* Genau das passiert hier: du siehst zum ersten Mal das ganze Bild.

Das ist kein weiterer Kurs, der in deiner Mediathek verstaubt. Das ist der Rahmen, in dem du es endlich umsetzt.

Liebe Grüsse
Patricia

**CTA-Button:** Die Academy ansehen → https://mumlifebalance.ch/mba/

---

#### Mail M3 · Tag 7 · Einwände (Mediathek voller Kurse · keine Zeit · zu teuer)
**Betreff A:** „Ich hab schon so viele Kurse gekauft und nichts umgesetzt"
**Betreff B:** Der ehrliche Grund, warum die anderen Kurse nichts gebracht haben
**Preheader:** Es lag nicht an dir.

Ich weiss, was manche gerade denkt, weil sie es mir schreibt: „Patricia, ich hab schon so viele Kurse gekauft und die liegen alle halb angeschaut rum. Warum sollte das hier anders sein?"

Ehrliche Antwort: weil die meisten Kurse dir *ein* Puzzleteil geben und dich dann alleine lassen. Du lernst Reels, aber nicht dein Thema. Du lernst dein Thema, aber nicht, wie du die Zeit dafür findest. Und weil das nächste Teil fehlt, bleibt alles liegen — nicht weil du zu wenig kannst, sondern weil dir der rote Faden und jemand zum Nachfragen gefehlt haben.

Genau das ist in der Academy anders. Die Teile bauen aufeinander auf, in der Reihenfolge, in der du sie brauchst. Und zweimal im Monat sitzt du im Live-Call und kannst fragen, bis es sitzt. Kein Alleine-lassen.

Und wenn dein Kopf gerade sagt „ich hab doch gar keine Zeit für noch einen Kurs" — dann ist das kein Gegenargument, sondern der Grund. Denn ein grosser Teil hier ist genau das: dir mit KI den Hintergrundkram abzunehmen, damit dein Business in deine Stunden passt und nicht umgekehrt.

Liebe Grüsse
Patricia

**CTA-Button:** Schau dir an, wie es aufgebaut ist → https://mumlifebalance.ch/mba/

---

#### Mail M4 · Tag 8 · Für wen — und für wen nicht
**Betreff A:** Für wen die Academy ist. Und für wen ehrlich nicht.
**Betreff B:** Ich bin nicht die Mentorin am Strand
**Preheader:** Damit du weisst, ob du richtig bist.

Damit du dir sicher bist, sag ich dir ehrlich, für wen die Academy *nicht* ist. Sie ist nicht für die, die zuhört, nickt und dann doch nichts macht und auf den grossen Zufall wartet. Da komm ich nicht weiter, und das wäre unfair, dir was anderes zu erzählen.

Sie ist für die Frau, die sagt: ich verdiene seit einer Weile ein paar hundert Franken im Monat, ich bin keine blutige Anfängerin, aber es geht einfach nicht voran — und ich will das endlich vergrössern. Für die, die bereit ist, den ersten Schritt selber zu machen. Niemand wird kommen und dich retten, ich auch nicht. Aber ich kann dir den ganzen Weg zeigen und zweimal im Monat mit dir am Call sitzen, wenn du ihn gehst.

Und weil du vielleicht denkst, ich erzähl dir das vom Liegestuhl aus: ich bin nicht die Mentorin am Strand mit sechsstelligem Einkommen. Ich bin die mit vier Kindern und 18 Stunden Wochenarbeit, bei der es keinen Monat ohne Verkauf mehr gibt, weil das System läuft. Genau dieses System kriegst du.

Liebe Grüsse
Patricia

**CTA-Button:** Ja, das bin ich → https://mumlifebalance.ch/mba/

---

#### Mail M5 · Tag 10 · Pioneer-Preis (sanfte Dringlichkeit) + P.S.
**Betreff A:** Warum die ersten Frauen weniger zahlen
**Betreff B:** Pioneer-Preis, solange die erste Runde läuft
**Preheader:** 997 statt 1347 — und warum.

Kurz und ehrlich: solange die erste Pioneer-Runde offen ist, kommst du für 997 Franken in die Mum Business Academy statt für 1347. Diesen Unterschied gibt es, weil die ersten Frauen mitgestalten und mir ehrliches Feedback geben — dafür sollen sie belohnt werden. Wenn die Runde voll ist, gilt der reguläre Preis.

Was du nach den ersten Wochen hast: dein Thema steht, dein erstes eigenes Produkt nimmt Form an, und dein KI-System läuft. Du arbeitest dann wieder mit Menschen, statt sechs Stunden am Tag Posts zu schreiben.

Wenn dich seit Wochen das Gefühl begleitet „ich will das endlich vergrössern" — das hier ist dein Moment, und der günstigere Einstieg gibt es nur, solange die Pioneer-Runde läuft.

Liebe Grüsse
Patricia

**P.S.** Ist das Geld gerade knapp? Den Satz „oh shit, wie viel hab ich noch auf dem Konto" kenn ich selber. Antworte mir, es gibt eine Ratenzahlung, dann finden wir einen Weg.

**CTA-Button:** Pioneer-Platz sichern (997 CHF) → https://mumlifebalance.ch/mba/

---

### DOWNSELL (geteilt · 3-Türen-Diagnose)

#### Mail D1 · Tag 12 · „Wo brennt's am meisten?"
> **AC-Reihenfolge:** Türen nach Einstiegs-Freebie sortieren — Sichtbarkeits-Leads sehen **Instagram-Kundenmaschine zuerst**, die anderen zwei darunter. So bleibt es relevant und deckt trotzdem ab, falls ein anderes Thema brennt.

**Betreff A:** Die ganze Academy ist dir gerade zu viel? Verständlich.
**Betreff B:** Dann starte mit dem, was dich JETZT am meisten drückt
**Preheader:** Ein Schritt reicht, um ins Rollen zu kommen.

Vielleicht ist die ganze Academy gerade ein zu grosser Brocken, zeitlich oder vom Budget. Das ist völlig okay. Lieber ein echter erster Schritt als wieder aufschieben.

Such dir die eine Tür aus, hinter der bei dir gerade der grösste Druck steht:

**→ Dir fehlen Kundinnen über Instagram?**
Die Instagram-Kundenmaschine bringt dir Thema, Positionierung und Strategie, damit sich die richtigen Frauen melden. 333 CHF. → https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/

**→ Dir fehlt vor allem die Zeit?**
Mama-CEO baut dir das KI-System, das dir den Hintergrundkram abnimmt, damit dein Business in deine Stunden passt. 333 CHF. → https://mumlifebalance.thrivecart.com/mama-ceo/

**→ Du willst dein Wissen zu einem eigenen Produkt machen?**
Die Digitale Produktwelt zeigt dir Schritt für Schritt, wie aus deinem Können ein verkaufbares Produkt wird. 333 CHF. → https://mumlifebalance.thrivecart.com/digitale-produktwelt/

Fang dort an, wo es am meisten weh tut. Den Rest holst du später nach — und wenn du dann alles zusammen willst, rechne ich dir den Kurs auf die Academy an.

Liebe Grüsse
Patricia

**CTA-Button:** Meinen Startpunkt wählen → [passender 333-LINK]

---

## 🔁 Danach — der Loop (grosser Verteiler)

Wer bis hier nichts gekauft hat → Tag `pitch-durchlaufen-kein-kauf` → **grosser Verteiler**. Kein Ende, sondern Dauerbeziehung (Julias „Funnel nach Funnel"):

- **Laufende Mehrwert-Mails** (Newsletter-Rhythmus)
- **Rotierende Angebote** im Wechsel Wert ↔ Pitch: „Expertin statt Verkäuferin" (97) · die zwei anderen Signatures · immer wieder zurück auf die MBA
- **Bei jedem MBA-Launch** / jeder Aktion: Pitch an die ganze Liste
- **Quartalsweise** Reaktivierung der Nicht-Öffner + Bereinigung (Zustellbarkeit + AC-Kosten schützen)

Kauft sie später etwas → steigt an der Stelle aus, kein Neustart von vorne.

---

## ✅ Wer macht was

| Aufgabe | Wer |
|---|---|
| Mail-Texte (oben, final) → als AC-Kampagnen-Entwürfe anlegen | **ich** (MCP) |
| Tags anlegen (`engine-sichtbarkeit-start`, `stufe:*`, `pitch-durchlaufen-kein-kauf`) | **ich** (MCP) |
| Engine-Flow zusammenklicken (Trigger/Wait/If/Goal) | **du** (1×, ich liefere Klick-Anleitung) |
| Auslieferungs-Automationen um „→ Tag engine-sichtbarkeit-start" ergänzen | **du** (1×) |
| MBA-Salespage-Link + 333-Checkout-Links final einsetzen | **du** (Links liefern) |
| Später: Webinar aufnehmen → `https://mumlifebalance.ch/mba/` optional auf Replay swappen | du + ich |
| Pillar 2 + 3: nur die 2 Brücken-Mails neu texten | **ich** |

---

## Status (Stand 2026-07-14)

- ✅ **Tags angelegt:** 87 (Trigger) · 88 · 79 · 89
- ✅ **Automation 72 „Automation 0€ Produkt" = leer** bestätigt → wird mit dieser Sequenz gefüllt
- ✅ **MBA-Link** eingesetzt (`https://mumlifebalance.ch/mba/`)
- ✅ **Mail E1 neu** (Schaufenster-Philosophie) · **Kundenstimme M2** echt + freigegeben
- ✅ **Go-live: jetzt** (Patricia 14.7.). Kein Konflikt mit dem laufenden Launch, weil die Engine dieselbe MBA zum selben Pioneer-Preis 997 pitcht — sie verstärkt den Launch, statt ihn zu unterbieten. Käuferinnen fliegen über Tag „mba-kauf" (79) sofort raus.
- ⏳ **Offen (du):** 3 ThriveCart-Links (Finde dein Thema 39 · IKM 333 · Mama-CEO 333 · DPW 333)

**Nächster Schritt:** Klick-Anleitung für den Automation-72-Flow (kommt sofort).

---

## 🔗 Verwandte Notizen

- [[blueprint]] · [[umbau-plan]] · [[variante-C-mailsequenz]] (Ursprung)
- [[funnel-landkarte]]
- [[active-funnels]] (`context/active-funnels.json`)
