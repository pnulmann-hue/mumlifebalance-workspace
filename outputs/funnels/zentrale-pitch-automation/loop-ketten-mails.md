---
tags: [funnel, mba, pitch-automation, intern]
---

# 🔁 Loop 2–6 — Mail-Texte (Julias Endlos-Kette)

## 📍 Die FINALE Kette (bestätigt Patricia 2026-07-22) — Julia-Reihenfolge

Julias Prinzip: eine Automation = ein Produkt · Käufer fliegen raus · Nicht-Käufer fallen in die nächste · endlos. **Webinar direkt nach dem MBA-Pitch** (Julias „Automation 02"). Jeder Loop übergibt am Ende per Tag an den nächsten.

| Loop | Automation | Produkt | Trigger-Tag | Status |
|---|---|---|---|---|
| **1** | **72** „Automation 0€ Produkt" | Brücke 39 → MBA-Track → Downsell | **87** | ✅ **LIVE** |
| **2** | NEU | 🎥 Webinar → MBA **997** | **89** „Engine Pitch ohne Kauf" | zu bauen |
| **3** | **73** (schon gebaut!) | Expertin **97** | **90** „Loop 3 Start" — Trigger **von 89 → 90 umhängen** | gebaut, umhängen |
| **4** | prüfen: #56 od. neu | Digitale Produktwelt **333** | Tag „Loop 4 Start" (Ende Loop 3) | zu bauen/prüfen |
| **5** | prüfen: #62 od. neu | Mama-CEO **333** | Tag „Loop 5 Start" (Ende Loop 4) | zu bauen/prüfen |
| **6** | NEU | MBA-Re-Pitch | Tag „Loop 6 Start" (Ende Loop 5) | zu bauen |
| → | Dauer-Newsletter + Launch-Pitches | — | — | — |

### Übergabe-Mechanik pro Loop (Julia)
1. **Käufer-Exit** („Springen zu" ans Ende): hat sie das Produkt (oder MBA 79) → raus.
2. **Ende für Nicht-Käufer:** Tag „Loop N+1 Start" setzen → nächster Loop startet.
3. **Ausschluss beim Eintritt:** hat MBA (79) → sofort beenden (MBA-Käuferin = null Mails). Plus: nie das eigene Produkt pitchen.

### ✅ Bestätigte Architektur-Entscheidungen (Patricia, 2026-08-02)
- **D1 Drei-Türen (Downsell) fliegt raus** aus Loop 1 — die Einzel-Loops pro Signature-Kurs ersetzen ihn (fokussierter, bessere Conversion, keine Doppel-Pitches). Jeder Signature-Kurs (Expertin · IKM · DPW · Mama-CEO) kriegt eine eigene Loop.
- **Ein konvergierender Motor, mehrere Eingänge:** 0€ + Minikurs → Loop 1 Start · Signature-Käuferin → direkt Loop 2 (Webinar) · MBA-Käuferin → nichts. Umsetzung über zusätzliche Trigger (Minikurs-/Signature-Kauf-Tags) + bestehende Ausschluss-Sprünge. **TODO:** Minikurs-/Signature-Kauf-Tag-Namen aus AC ziehen.
- **Voice-Pflicht ALLER Mails: Reichweitenherz-Layer** — innerer Monolog in „…", harte Cuts, konkrete Mama-Szenen, Schweizer ss, kein KI-Sprech, Blacklist gewinnt (kein Nicht/Sondern!), keine erfundenen Zahlen, kein Julia-Name. Die 5 Webinar-Mails sind schon so gebaut; die 8 Loop-1-Mails sind noch im flacheren Ton → Upgrade offen.

### 📦 Webinar-Loop-Mails gebaut (2026-08-02) — `mails/mail-W1..W5-*.html`
| Datei | Betreff | CTA → |
|---|---|---|
| W1 Einladung | „Ich hab mich zwei Stunden vor die Kamera gesetzt" | Replay-Seite |
| W2 Einladung | „Lohnt sich die knappe Stunde überhaupt?" | Replay-Seite |
| W3 Einladung (letzte) | „Ich nehm das Video bald wieder runter" | Replay-Seite |
| W4 Pitch | „Falls du beim Video gedacht hast: genau das will ich" | ThriveCart 997 |
| W5 Pitch | „Wissen hast du eigentlich genug" | ThriveCart 997 |

### 📦 Kaskaden-Mails gebaut (2026-08-02) — Reichweitenherz-Voice, blacklist-sauber
Alle als HTML in `mails/`, Header-Fallback drin, echte Umlaute, Schweizer ss, kein Julia-Name, kein Nicht/Sondern:
- **Loop 3 Expertin (97):** `mail-L3-expertin-1..3` (upgraded Voice → ersetzt die alten in Automation 73)
- **Loop 4 DPW (333):** `mail-L4-dpw-1..3`
- **Loop 5 Mama-CEO (333):** `mail-L5-mamaceo-1..3`
- **Loop 6 IKM (333):** `mail-L6-ikm-1..3` — ✅ auf **echten Kursinhalt** umgeschrieben (Quelle: `outputs/produkte/claude-als-networkerin/downloads/instagram-kundenmaschine-wissensgrundlage.txt`): „warum bei dir, nicht bei Frau XY" · Schaufenster/grüne Schuhe · eigenes Thema statt Produkt-Pushen · Profil-Fundament.
- **Loop 7 MBA-Re-Pitch:** `mail-L7-mba-repitch-1..3` (1→/mba/ · 2+3→ThriveCart 997)

### 🔒 Ausschluss-Matrix (VERBINDLICH für JEDEN Loop — Patricia 2026-08-02)
Jeder Loop startet mit einem **„Springen zu Ende"-Goal** (feuert laufend → Kauf mitten im Loop = sofort raus). Zwei Prinzipien ausnahmslos: **(1) MBA-Käuferin (79) = null Mails aus dem ganzen Funnel. (2) Wer den gepitchten Kurs schon hat, kriegt dessen Mails nie.**

| Loop | Pitcht | „Springen zu Ende" wenn Tag |
|---|---|---|
| 2 Webinar | MBA | **79** |
| 3 Expertin | Expertin 97 | **79** · 51 · 39 (IKM-Käuferin raus) |
| 4 DPW | DPW 333 | **79** · 44 |
| 5 Mama-CEO | Mama-CEO 333 | **79** · 71 |
| 6 IKM | IKM 333 | **79** · 39 |
| 7 Re-Pitch | MBA | **79** |

**Entscheidung Patricia 2026-08-02: KEIN Signature-Skip.** Volle Kaskade — jede Nicht-MBA-Käuferin sieht alle Signatures (ausser dem eigenen), dann finaler MBA-Re-Pitch. So sieht sie, was in den anderen Kursen steckt, bevor Loop 7 nochmal die MBA anbietet. Es gilt NUR die Ausschluss-Matrix oben (MBA raus + eigenes Produkt raus).

**Mehrwert-Prinzip (Patricia):** jede Mail führt mit Story/Tipp vor dem Pitch (nie nackter Verkauf); nach Loop 7 → Dauer-Newsletter für die laufende Beziehung.

### 🔧 Nächste Bau-Schritte (frische Sitzung)
1. **Loop 2 Webinar bauen** (Trigger 89 · 3 Einladung + 2 Pitch → Replay-Seite/997-Checkout · Exit 79 · Ende → Tag 90).
2. **Loop 3 (Expertin, 73) umhängen:** Trigger von 89 → 90. (Rest steht schon.)
3. **Loop 3 Ende:** Tag „Loop 4 Start" ergänzen.
4. **Loop 4 DPW + Loop 5 Mama-CEO:** erst bestehende Funnels #56/#62 prüfen (Inhalt + Blacklist), dann einhängen ODER frisch bauen wie Expertin.
5. **Loop 6 MBA-Re-Pitch** bauen → dann Newsletter.
6. ~~AC-Live-Mails neu pasten (Header-Fallback + M5-Preisversion).~~ ✅ **erledigt 2026-08-02** — alle 8 Loop-1-Mails (E1·E2·M1–M5·D1) haben den Handy-Header-Fallback `background-color:#12828c` direkt in AC bekommen; M5 zusätzlich auf die neue Webinar-/997-Version + Betreff „So kommst du zum Pioneer-Preis der Academy" + Preheader „997 statt 1347 — über einen Weg." umgestellt.

> Loop 1 liegt bewusst komplett in *einer* Automation (72), weil „Läuft: Einmal" das Doppel-Problem löst. Ab Loop 2 = eigene Automationen mit Übergabe-Tags.

---

> Fortsetzung von [[sichtbarkeit-engine-FINAL]]. Wer Loop 1 ohne Kauf durchlaufen hat, kriegt am Ende Tag `Engine Pitch ohne Kauf` (89) — der startet Loop 2. Danach läuft sie durch 3 → 4 → 5 → 6, je 1 Produkt, 3–5 Mails, 1–2 Tage Abstand.
> **2 Schutzregeln pro Kette (Julia-Pflicht):** (1) Produkt-Kauf-Ziel → raus. (2) „schon in anderer Kette? → überspringen" (kein Doppel).
> Blacklist-geprüft: keine Stakkato, kein „Kennst du das", kein „6-stellig", kein Mentorin-Name, keine erfundenen Zahlen, Schweizer ss, Kundenebene geschlechtsneutral.
> Links: Expertin `…/expertin/` · DPW `…/digitale-produktwelt/` · Mama-CEO `…/mama-ceo/` · MBA `mumlifebalance.ch/mba/` · Webinar `https://mumlifebalance.ch/mba-webinar-replay` (nimmt Patricia noch auf).

---

## LOOP 2 — Expertin statt Verkäuferin (97) · 3 Mails
**Status:** ✅ in AC gebaut (Automation 73), noch **inaktiv**.
**Trigger:** Tag 89 „Engine Pitch ohne Kauf" · **Läuft:** Einmal
**Exit-Ziel am Ende** („Springen zu", Position = *unter Position des Kontakts*):
> Tag besteht **Expertin** (51) **ODER** Tag besteht **mba-kauf** (79) **ODER** Tag besteht **Instagram-Kundenmaschine** (39) → raus

### ✅ Umgesetzt (2026-07-22)
- **Loop 1 Bridge-Skip erweitert:** „Springen zu M1" feuert jetzt bei **Thema finden (41) ODER Expertin (51) ODER IKM (39) ODER mama-ceo-kauf (71) ODER digitale Produktwelt grosser Kurs (44)** → jede Kurs-Käuferin überspringt E1+E2.
- **Loop 1 MBA-Exit:** Tag 79 am Ende → MBA-Käuferin kriegt aus Loop 1 nichts.
- **Loop 2 Exit:** Expertin(51)/MBA(79)/IKM(39).
- **Replay-Seite:** mumlifebalance.ch/mba-webinar-replay (Vimeo + Pioneer-997/48h-CTA).

### ⏳ Offen (Review-Findings)
- **Loop 3–6:** je Start-Check „hat MBA (79)? → beenden" (MBA-Käuferin = null Mails), plus produkt-eigener Exit.
- **Preis-Konsistenz:** MBA-Salespage zeigt jetzt **1347** (Pioneer-Phase vorbei). → Loop-1-Mail **M5** verspricht aber „Pioneer 997 solange Runde läuft" = Widerspruch. Empfehlung: 997 wird zum **Webinar-Angebot** (48h nach Replay), M5 auf 1347 + Webinar-Weg umstellen.
- **Pioneer-997-Checkout:** damit die 48h real sind, braucht die Replay-CTA einen **997-Checkout/ThriveCart-Coupon** (Salespage zeigt 1347). Link fehlt noch.
- **D1-Downsell:** IKM-Käuferin sieht dort noch die IKM-Tür → owned-Tür ausblenden (Feinschliff).

### 🚨 Ausschluss-Regel (Patricia 2026-07-15) — gilt für JEDEN Loop
Ein Loop darf nie an jemanden gehen, die den Inhalt schon hat:
- **MBA-Käuferinnen (79)** werden aus **allen** Loops ausgeschlossen — sie haben alles.
- **IKM-Käuferinnen (39)** kriegen **kein** „Expertin" (97) — Positionierung/Thema steckt schon in der Instagram-Kundenmaschine.
- Analog beim Bauen von Loop 4/5: DPW-Käuferin (44) nicht Loop 4, Mama-CEO-Käuferin (71) nicht Loop 5.

**Kauf-Tags (verifiziert — NICHT die „Automation …"-Tags, die nur Pitch-Funnels starten!):**
| Produkt | Kauf-Tag | ❌ nicht verwechseln mit |
|---|---|---|
| Finde dein Thema (39) | **41** „Thema finden" | 46 „Automation Finde dein Thema" |
| Expertin (97) | **51** „Expertin" | 50 „Automation Expertin statt Verkäuferin" |
| Instagram-Kundenmaschine (333) | **39** | 47 „Automation IG Kundenmaschine" |
| Mama-CEO (333) | **71** | — |
| Digitale Produktwelt (333) | **44** | — |
| MBA | **79** „mba-kauf" | — |

### Mail 2-1
**Betreff A:** Fühlst du dich manchmal wie eine Verkäuferin?
**Betreff B:** Der Unterschied zwischen pushen und empfohlen werden
**Preheader:** Warum die Leute bei den einen kaufen — und bei den anderen wegscrollen.

Ich frag dich mal ganz direkt: fühlst du dich manchmal wie eine Verkäuferin, die ihren Leuten etwas andrehen muss? Dieses leicht schlechte Gewissen, wenn du zum dritten Mal dasselbe Produkt zeigst und trotzdem niemand reagiert?

Das kenn ich. Und der Grund ist nicht, dass du zu wenig pushst, sondern dass du als Verkäuferin auftrittst statt als die, die etwas wirklich versteht. Menschen kaufen nicht bei der, die am lautesten anbietet, sondern bei der, der sie zutrauen, dass sie ihr Problem besser kennt als sie selbst.

Ein Tipp für diese Woche: hör auf, dein Produkt zu zeigen, und zeig stattdessen, dass du das Problem deiner Leute in Worte fassen kannst, bevor sie es selber können. Genau da kippt es von „die will mir was verkaufen" zu „die versteht mich".

Wie du von der Verkäuferin zur gefragten Expertin wirst — mit deiner Geschichte und deiner Positionierung — steckt in „Expertin statt Verkäuferin", für 97 Franken.

Liebe Grüsse
Patricia

**CTA-Button:** Expertin werden statt verkaufen → https://mumlifebalance.thrivecart.com/expertin/

### Mail 2-2
**Betreff A:** „Seit ich das geändert hab, geht mein Account ab"
**Betreff B:** Nicht das Produkt hat verkauft — die Haltung
**Preheader:** Was sich ändert, wenn du aufhörst zu pitchen.

Eine Frau, mit der ich gearbeitet hab, hat mir nach ein paar Wochen geschrieben: seit sie ihre Positionierung angepasst hat, geht ihr Account ab. Sie hat nicht mehr Produkte gezeigt als vorher, sie hat nur aufgehört, wie eine Verkäuferin zu klingen.

Der Punkt ist: solange du über dein Produkt redest, bist du eine von hunderten, die dasselbe anbieten. Sobald du über das Problem redest, das du löst, bist du die Einzige, die genau so spricht, wie deine Leute denken.

In „Expertin statt Verkäuferin" bauen wir genau das auf — deine Story, deine Nische und deine drei Kernbotschaften, mit denen du sofort erkennbar wirst. Danach musst du nicht mehr überreden, weil sich die Richtigen von selbst melden.

97 Franken, und du klingst nie wieder wie ein Katalog.

Liebe Grüsse
Patricia

**CTA-Button:** Zur Expertin-Positionierung → https://mumlifebalance.thrivecart.com/expertin/

### Mail 2-3
**Betreff A:** Bevor du weiterscrollst
**Betreff B:** Der günstigste Weg raus aus dem Verkäuferinnen-Gefühl
**Preheader:** Kleiner Schritt, grosse Wirkung.

Ich lass das Thema gleich ruhen, aber einen Gedanken geb ich dir noch mit.

Das Verkäuferinnen-Gefühl verschwindet nicht, indem du dich mehr überwindest. Es verschwindet, wenn du so klar weisst, wofür du stehst, dass du gar nicht mehr das Gefühl hast, etwas andrehen zu müssen — weil du nur noch teilst, was du ohnehin verstehst.

Genau das kriegst du in „Expertin statt Verkäuferin" für 97 Franken. Wenn's grad passt, ist das ein kleiner Schritt mit grosser Wirkung. Wenn nicht, auch gut, dann meld ich mich mit dem nächsten Thema.

Liebe Grüsse
Patricia

**CTA-Button:** Ja, ich will das ändern → https://mumlifebalance.thrivecart.com/expertin/

---

## LOOP 3 — MBA-Webinar (Replay) · 3 Einladung + 2 Pitch = 5 Mails
**Exit:** Tag `mba-kauf` (79) · **Ende:** Tag → startet Loop 4. Webinar-Link = `https://mumlifebalance.ch/mba-webinar-replay` (sobald aufgenommen).

### Mail 3-1 · Einladung
**Betreff A:** Ich hab das ganze System in ein Video gepackt
**Betreff B:** Einmal alles zusammen — in unter einer Stunde
**Preheader:** Wie die vier Teile bei dir ineinandergreifen.

Ich hab dir in den letzten Wochen immer wieder einzelne Stücke gezeigt — dein Thema, deine Positionierung, dein eigenes Produkt, dein KI-System. Jetzt hab ich das Ganze einmal am Stück aufgenommen, damit du siehst, wie die Teile bei dir zusammenspielen.

Es ist ein Video von unter einer Stunde, kostenlos, in dem ich dir zeige, wie aus „ich verzettel mich" ein System wird, das auch dann weiterläuft, wenn du gerade Mama bist.

Wenn du eine ruhige halbe Stunde findest, schau es dir an. Es macht Klick.

Liebe Grüsse
Patricia

**CTA-Button:** Video jetzt ansehen → https://mumlifebalance.ch/mba-webinar-replay

### Mail 3-2 · Einladung
**Betreff A:** Die drei Dinge, die im Video Klick machen
**Betreff B:** Warum es nicht an dir liegt, dass es stockt
**Preheader:** Kurz, warum sich das Anschauen lohnt.

Falls du noch überlegst, ob sich die knappe Stunde lohnt — hier die drei Dinge, die im Video Klick machen:

- warum du dich verzettelst, obwohl du fleissig bist (es liegt nicht an dir, sondern an der fehlenden Reihenfolge)
- wie du mit wenigen Stunden pro Woche trotzdem regelmässig verkaufst
- wie ein KI-System dir den Hintergrundkram abnimmt, im Business und im Haushalt

Ich zeig dir das nicht theoretisch, sondern so, wie ich es selber mit vier Kindern und rund 18 Stunden Woche mache.

Schau es dir an, solange du dran denkst.

Liebe Grüsse
Patricia

**CTA-Button:** Zum Video → https://mumlifebalance.ch/mba-webinar-replay

### Mail 3-3 · Einladung (letzte)
**Betreff A:** Noch nicht geschaut?
**Betreff B:** Das Video läuft noch die nächsten Tage
**Preheader:** Danach nehm ich es wieder offline.

Kurze Erinnerung: das Video, in dem ich dir das ganze System zeige, läuft noch die nächsten Tage. Danach nehm ich es wieder offline, weil ich es nur ab und zu öffne.

Wenn dich das Thema „Business, das neben der Familie läuft" auch nur ein bisschen anzieht, ist das die knappste und ehrlichste Stunde, die ich dir dazu geben kann.

Mach es dir kurz gemütlich und schau rein.

Liebe Grüsse
Patricia

**CTA-Button:** Jetzt ansehen, bevor es weg ist → https://mumlifebalance.ch/mba-webinar-replay

### Mail 3-4 · Pitch
**Betreff A:** Und wenn du sagst „genau das will ich"
**Betreff B:** Der nächste Schritt nach dem Video
**Preheader:** Alles zusammen, in der richtigen Reihenfolge.

Wenn du das Video geschaut und dabei gedacht hast „genau das will ich" — dann ist die Mum Business Academy dein nächster Schritt.

Da ist alles drin, was im Video zusammenspielt: dein Thema, dein eigenes Produkt, dein KI-System, der Weg zu planbarem Einkommen — und zweimal im Monat ein Live-Call mit mir und mit Expertinnen, damit du nie stecken bleibst.

Das ist der Unterschied zwischen „ich hab ein gutes Video gesehen" und „ich hab es umgesetzt": die Reihenfolge und die Begleitung.

Liebe Grüsse
Patricia

**CTA-Button:** Die Academy ansehen → https://mumlifebalance.ch/mba/

### Mail 3-5 · Pitch
**Betreff A:** Was dich wirklich aufhält
**Betreff B:** Nicht das Wissen fehlt dir
**Preheader:** Sondern der Rahmen, es zu tun.

Ganz ehrlich: dir fehlt wahrscheinlich nicht das Wissen. Du hast schon Kurse, schon Ideen, schon vieles im Kopf. Was fehlt, ist der Rahmen, in dem du es endlich der Reihe nach umsetzt — und jemand, den du fragen kannst, wenn es hakt.

Genau das ist die Academy. Nicht noch ein Video zum Wegspeichern, sondern der Ort, an dem du es tust, mit Begleitung. Zum Pioneer-Preis von 997 statt 1347, solange die Runde für dich offen ist.

Wenn du bereit bist, den ersten Schritt selber zu machen, zeig ich dir den Rest.

Liebe Grüsse
Patricia

**CTA-Button:** Pioneer-Platz sichern → https://mumlifebalance.ch/mba/

---

## LOOP 4 — Digitale Produktwelt (333) · 3 Mails
**Exit:** Kauf „Digitale Produktwelt" · **Ende:** Tag → startet Loop 5

### Mail 4-1
**Betreff A:** Dein Wissen verkauft — auch wenn du grad am Spielplatz bist
**Betreff B:** Warum du dein Können in ein Produkt packen solltest
**Preheader:** Einmal erstellen, immer wieder verkaufen.

Du hast dir über die Jahre Wissen aufgebaut — über dein Thema und über das, was du selber durchgemacht und gelöst hast. Im Moment tauschst du dieses Wissen gegen Zeit: du erklärst es in DMs, in Gesprächen, immer wieder von vorne.

Es geht auch anders. Du packst dein Wissen einmal in ein digitales Produkt, und das verkauft dann auch, wenn du grad am Spielplatz stehst oder schläfst. Kein Lager, kein Versand, keine Provisionsgrenze.

Wie aus deinem Können ein Produkt wird, das Menschen wirklich kaufen — Schritt für Schritt — zeig ich dir in der Digitalen Produktwelt, für 333 Franken.

Liebe Grüsse
Patricia

**CTA-Button:** Eigenes Produkt aufbauen → https://mumlifebalance.thrivecart.com/digitale-produktwelt/

### Mail 4-2
**Betreff A:** „Aber ich hab doch schon ein Network"
**Betreff B:** Warum ein eigenes Produkt dein Network stärker macht
**Preheader:** Das eine schliesst das andere nicht aus.

Vielleicht denkst du: ich bin doch im Network, wozu ein eigenes Produkt? Genau darum. Dein eigenes Produkt macht dich unabhängiger von der Provisionslogik und zieht Menschen an, die zuerst dich und dein Thema kennenlernen — und dann interessiert sie oft auch, womit du sonst arbeitest.

Das eine schliesst das andere nicht aus, im Gegenteil: dein Produkt ist die Tür, durch die die Richtigen zu dir kommen.

In der Digitalen Produktwelt bauen wir dein erstes Produkt so auf, dass es zu dir und deinem Thema passt. 333 Franken, einmal erstellt, immer wieder verkauft.

Liebe Grüsse
Patricia

**CTA-Button:** Zur Digitalen Produktwelt → https://mumlifebalance.thrivecart.com/digitale-produktwelt/

### Mail 4-3
**Betreff A:** Der Gedanke, den die meisten wegschieben
**Betreff B:** „Wer soll das ausgerechnet von mir kaufen?"
**Preheader:** Genau das klären wir zuerst.

Der Gedanke, der die meisten von einem eigenen Produkt abhält, ist: „wer soll das ausgerechnet von mir kaufen?" Verständlich — und genau deshalb fangen wir nicht beim Produkt an, sondern bei der Frage, welches konkrete Problem du für wen löst.

Wenn das steht, ist das Produkt fast der einfachste Teil. In der Digitalen Produktwelt gehen wir das der Reihe nach durch, damit du am Ende nicht irgendwas gebaut hast, sondern etwas, das gebraucht wird.

333 Franken. Wenn's grad passt, ist das dein Sprung in eigenes, planbares Einkommen.

Liebe Grüsse
Patricia

**CTA-Button:** Jetzt starten → https://mumlifebalance.thrivecart.com/digitale-produktwelt/

---

## LOOP 5 — Mama-CEO (333) · 3 Mails
**Exit:** Kauf „Mama-CEO" · **Ende:** Tag → startet Loop 6

### Mail 5-1
**Betreff A:** Du weisst genau, was du tun müsstest
**Betreff B:** Und kommst dann doch nie dazu
**Preheader:** Es liegt nicht an deiner Disziplin.

Du weisst genau, was du fürs Business tun müsstest — und dann ist der Tag vorbei, die Kinder brauchen dich, der Haushalt ruft, und du hast wieder nichts geschafft. Und abends das leise „ich sollte doch...".

Das ist keine Frage der Disziplin. Du hast vier Hände voll zu tun. Die Frage ist, wie das Business trotzdem läuft, ohne dass du mehr Stunden im Tag hast — und die Antwort ist ein System, das den Hintergrundkram für dich übernimmt.

Genau das baust du in Mama-CEO auf: die Struktur und das KI-System, das dir Admin im Business und im Haushalt abnimmt, damit dein Business in deine Stunden passt. 333 Franken.

Liebe Grüsse
Patricia

**CTA-Button:** Zeit fürs Business schaffen → https://mumlifebalance.thrivecart.com/mama-ceo/

### Mail 5-2
**Betreff A:** Mein KI-Team arbeitet, während ich Mama bin
**Betreff B:** Wie ich mit rund 18 Stunden Woche keinen Monat ohne Verkauf hab
**Preheader:** Kein Hexenwerk — ein System.

Ich sag dir ehrlich, wie das bei mir läuft: ich hab nicht mehr Zeit als du. Vier Kinder, rund 18 Stunden Business pro Woche, der Rest ist Familie. Trotzdem gibt es keinen Monat mehr ohne Verkauf, weil im Hintergrund ein KI-System läuft, das mir den ganzen Kleinkram abnimmt.

Das ist kein Hexenwerk, und du musst keine Technikerin sein. Es ist eine Handvoll Bausteine, die zusammen dafür sorgen, dass du dich um die Menschen kümmerst und das System um den Rest.

In Mama-CEO installieren wir genau dieses System bei dir. 333 Franken — und du kriegst deine Abende zurück.

Liebe Grüsse
Patricia

**CTA-Button:** Mein KI-System aufbauen → https://mumlifebalance.thrivecart.com/mama-ceo/

### Mail 5-3
**Betreff A:** Die Lösung ist nicht „mehr schaffen"
**Betreff B:** Sondern weniger selber machen
**Preheader:** Der letzte Gedanke zum Thema Zeit.

Ein letzter Gedanke zum Thema Zeit, dann lass ich dich in Ruhe. Die Lösung für „ich komm nicht dazu" ist nicht, noch mehr in den Tag zu quetschen. Es ist, weniger selber zu machen und den Rest an ein System abzugeben, das nicht müde wird.

Das ist der ganze Kern von Mama-CEO — nicht noch eine To-Do-Liste, sondern weniger auf deiner Liste. 333 Franken.

Wenn dich das „ich sollte doch..." abends nervt, ist das dein Ausweg.

Liebe Grüsse
Patricia

**CTA-Button:** Raus aus dem Hamsterrad → https://mumlifebalance.thrivecart.com/mama-ceo/

---

## LOOP 6 — MBA Re-Pitch · 3 Mails
**Exit:** Tag `mba-kauf` (79) · **Ende:** → Dauer-Newsletter + Launch-Pitches an die ganze Liste.

### Mail 6-1
**Betreff A:** Erinnerst du dich an die Academy?
**Betreff B:** Alles, was ich dir einzeln gezeigt hab — an einem Ort
**Preheader:** Der rote Faden, der alles verbindet.

In den letzten Wochen hab ich dir viele einzelne Wege gezeigt — dein Thema, deine Positionierung, dein eigenes Produkt, dein KI-System. Jeder davon bringt dich weiter. Aber der rote Faden, der alles in die richtige Reihenfolge bringt, ist die Mum Business Academy.

Da ist alles drin, aufeinander aufgebaut, plus zweimal im Monat ein Live-Call, damit du nie alleine feststeckst. Statt dir die Teile mühsam einzeln zusammenzukaufen, hast du sie hier an einem Ort — und jemanden, der mitgeht.

Wenn du das Verzetteln satt hast, ist das dein Zuhause.

Liebe Grüsse
Patricia

**CTA-Button:** Die Academy ansehen → https://mumlifebalance.ch/mba/

### Mail 6-2
**Betreff A:** Was nach ein paar Wochen anders ist
**Betreff B:** Von „paar hundert im Monat" zu planbar
**Preheader:** Kein Wunder, sondern Reihenfolge.

Stell dir vor, wo du in ein paar Wochen stehst, wenn du drin bist: dein Thema ist klar, dein erstes eigenes Produkt nimmt Form an, dein KI-System läuft, und du weisst jeden Morgen, was dran ist — statt an zehn Ecken gleichzeitig zu ziehen.

Das ist kein Wunder und kein Zufall, sondern einfach die richtige Reihenfolge plus Begleitung. Genau dafür gibt es die Academy.

Zum Pioneer-Preis von 997 statt 1347, solange die Runde für dich offen ist.

Liebe Grüsse
Patricia

**CTA-Button:** Pioneer-Platz sichern → https://mumlifebalance.ch/mba/

### Mail 6-3
**Betreff A:** Ich lass dich damit erstmal in Ruhe — versprochen
**Betreff B:** Der ehrliche letzte Anstoss
**Preheader:** Danach nur noch, wenn du willst.

Ich schreib dir zu dem Thema erstmal nicht mehr so oft, versprochen. Aber diesen einen ehrlichen Anstoss geb ich dir noch mit.

Du liest meine Mails seit Wochen. Irgendwas in dir will das, sonst wärst du längst weg. Der einzige Unterschied zwischen „ich denk drüber nach" und „bei mir läuft's" ist die Entscheidung, den ersten Schritt selber zu machen. Niemand kommt und macht ihn für dich — aber wenn du ihn machst, geh ich mit dir den ganzen Rest.

Die Academy steht offen, zum Pioneer-Preis, solange die Runde läuft.

Liebe Grüsse
Patricia

**CTA-Button:** Ja, ich mach den Schritt → https://mumlifebalance.ch/mba/

---

## 🔗 Verwandte Notizen
- [[sichtbarkeit-engine-FINAL]]
- [[blueprint]]
