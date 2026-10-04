---
tags: [plan, content, hooks]
---

# Die eigene Hook-Maschine — Plan (04.10.2026)

**Anlass:** Webinar „automatisiertes KI-System“ von Maxi Raabe (@iam.maxiraabe, Produkt *apeli.ai*,
Hook-Agent „Luma“). Patricia hat 169 Folien abfotografiert und will etwas Eigenes in der Art aufbauen,
weil die bisherigen Ergebnisse nicht befriedigen.

---

## 1 · Was er tatsächlich zeigt

Seine „revolutionäre KI“ besteht laut eigener Folie aus **drei Bausteinen**:

| Baustein | Was er meint | Haben wir das? |
|---|---|---|
| **1 · Master-Prompt** (10+ Seiten: Rolle, Formatregeln, Schritte, Feedbackschleifen, Grenzen) | eine sehr lange, feste Anweisung | ✅ **Ja.** Der Hook-Skill hat 1'235 Zeilen, 16 Teile, Verbote, Prüfskript |
| **2 · Kontext** („kennt dich, dein Business, deine Zielgruppe, ihre Wünsche, Ängste, Einwände“) | Profil, das man einmal in 5 Minuten ausfüllt | ✅ **Ja, tiefer.** `brand-voice.md`, `patricia-vollprofil.md`, `kern-painpoint.md`, Interview Herbst 2026 |
| **3 · Wissensdatenbank** („2'000 virale Posts aus 300 Nischen, 1'000 Beispiele“) | Beispiele mit Ergebnis, aus denen die KI lernt | 🟡 **Daten ja, verdrahtet nein** — siehe unten |

Dahinter: ein Sprachmodell wie Claude. Der Rest des Webinars ist Verkauf (ab Folie ~120:
„Schritt 3 Verkaufen“, Werbepartnerschaften, ManyChat-Kurs).

**Was man ihm nicht glauben muss:** die 8-Sekunden-Goldfisch-Studie (längst widerlegt, von Microsoft
nie so gemessen) · „95 % vor der Konkurrenz“ · „Fehleranfälligkeit null“. Der Vergleich ChatGPT gegen
Luma ist ein Vergleich *ohne Kontext* gegen *mit Kontext* — das hat Patricia schon seit Monaten.

**Was stimmt und brauchbar ist:**
- Drei Hook-Elemente: **Musterbruch · Neugier-Lücke · Emotion** (deckt sich mit Teil 2/7 des Hook-Skills).
- Seine Hooks klingen **konkret mit Zahlen und Gegenständen** („Haus kostet 380'000. Makler sagt
  Schnäppchen. ChatGPT fand 11 Mängel.“) — eine Mini-Geschichte in drei Zeilen.
- Ein CTA mit Gegenleistung („Kommentiere KI und ich schick dir die 7 Prompts“) brachte bei ihm
  8× mehr Follower. Das ist bei uns die Keyword-Regel.

**Der eigentliche Unterschied zu uns ist Baustein 3** — und dort liegt Patricias Vorteil, weil ihre
Datenbank aus **ihrem eigenen Publikum** stammen kann, nicht aus 300 fremden Nischen.

---

## 2 · Was wir schon haben (Stand heute nachgezählt)

| Quelle | Umfang | Was fehlt |
|---|---|---|
| `outputs/cockpit/abgleich/gepostet-voll.json` | **552 eigene Beiträge** mit Reichweite, Saves, Shares, Faktor zum eigenen Median; 392 davon reif und aus der jetzigen Ausrichtung | Hook-Etiketten (Familie, Angle, Frage ja/nein …) |
| `outputs/apify-runs/competitors-*.json` | täglicher Scrape von ~10 Konten, rund 1'100 Beiträge | normiert auf den Median des jeweiligen Kontos (gibt es schon im Reiter „Ideen von anderen“) |
| `outputs/apify-runs/discovery-*` | 24 Läufe, Top-Creator je Nische | nicht ausgewertet nach Hooks |
| `context/hook-formel-testlog.md` | Turnier-Fahrplan, 6 Ergebnisse | wird von Hand gepflegt und ist seit KW25 stehen geblieben |

### Erster Befund aus den eigenen 392 Beiträgen (Caption-Anfang, nicht Bild-Hook)

**Oben** (14- bis 27-facher Median): *„Ich liebe Empfehlungsmarketing. Wirklich. Meine Gesichtscreme?
Meine Shakes?“* · *„Wenn du bei jedem Treffen im Dorf überlegst, ob du die Person neben dir …“* ·
*„Ich hab mein Auto nicht abgestellt. Es ist einfach losgerollt.“* · *„Heute hab ich meine
Network-Produkte im Wert von über 500 Franken weggeschmissen.“* · *„Mit 22 war mein Traum: Ich will
einfach nur Mama sein.“*

**Unten** (unter 0,2-facher Median): *„Diese 3 Sätze sabotieren deine Umsetzung im Networkmarketing“* ·
*„Das leere Dokument. Jeden Abend wieder.“* · *„Kommentier STANDBEIN, dann schick ich dir …“* als
erste Zeile.

| Merkmal | Beiträge | Median-Faktor |
|---|---:|---:|
| Frage in der ersten Zeile | 36 | **1,22** |
| ohne Frage | 356 | 0,75 |
| Reel | 316 | 0,97 |
| Karussell/Bild | 76 | 0,61 |

**Muster:** Gewinner sind **Ich-Bekenntnisse mit einem konkreten Gegenstand oder Ereignis**
(Gesichtscreme, Auto, 500 Franken, mit 22). Verlierer sind **Ratgeber-Listen und Du-Szenen ohne
Ereignis**. Genau dieses Muster ist es, das eine Datenbank dauerhaft und automatisch finden soll —
statt dass wir es einmal im Jahr von Hand entdecken.

⚠️ Vorbehalt: `anfang` ist die Caption, nicht zwingend der Text im Video, und Video-Stil und Thema
wirken mit. Deshalb Schritt 5 (saubere Tests).

⚠️ Auch die Gewinner haben **fast keine Saves** (0–3 bei 7'000 Reichweite). Reichweite haben wir
manchmal — was fehlt, ist der Grund zum Speichern. Ein Hook allein löst das nicht.

---

## 3 · Der Aufbau, Schritt für Schritt

**Regel aus der Skill-Ablage:** kein neuer Skill. Die Hook-Maschine wird ein **Modus des Hook-Skills**
plus ein Skript, damit `/content`, `/reels`, `/karussell` und das Cockpit automatisch davon profitieren.

### Schritt 1 · Hook-Datenbank bauen (≈ 1 Session)
`scripts/hooks/datenbank-bauen.py` →  `outputs/hooks/hook-datenbank.json`
- Je Beitrag: erste Zeile, Format, Konto, **Faktor zum Konto-Median**, Save- und Share-Rate.
- Eigene 552 + Konkurrenz (nur Konten mit Verkaufssignal, normiert) + Discovery-Läufe.
- **Etiketten** per Claude Haiku im Stapel: Hook-Familie · Angle · Bewusstseinsstufe · Frage ja/nein ·
  konkreter Gegenstand/Zahl ja/nein · Ich/Du-Perspektive · Länge.
- Ergebnis gleich als Bericht: *welche Etiketten gewinnen bei dir, welche bei der Konkurrenz.*
- Läuft danach mit im täglichen `cockpit-daten-abgleich` (neue Beiträge, sobald reif).

### Schritt 2 · Der Hook-Agent (≈ 1 Session)
Neuer Modus **„Maschine“** im Hook-Skill:
1. Thema + Profil + Ziel (Reichweite / Lead) rein.
2. Zieht aus der Datenbank die **15 stärksten eigenen und 15 stärksten fremden Hooks** mit ähnlichem
   Thema oder Etikett als Beispiele (das ist sein „Gehirn“, nur mit eigenen Zahlen).
3. Schreibt 20 Varianten über mindestens 3 Angles.
4. Prüft selbst: Blackliste (`texte-pruefen.py`), 5-Fragen-Check, Bindewort-Probe.
5. Liefert **5 Hooks** mit Begründung: *„ähnelt deinem Auto-Hook (11× Median): Ich-Ereignis mit
   Gegenstand“*.

### Schritt 3 · Der Bewerter (≈ ½ Session)
Ein zweiter Blick, der jeden Hook — auch einen selbst geschriebenen — gegen die Datenbank legt:
*„trägt 4 von 5 Gewinner-Merkmalen, nächster Verwandter: …“*. Kein Orakel, sondern ein Abgleich mit
dem, was bei ihr nachweislich lief. Nützlich vor allem für die A/B-Varianten der Freitagsproduktion.

### Schritt 4 · Die Schleife schliessen (≈ ½ Session)
Das, was sein System *nicht* zeigt: **lernen aus dem eigenen Ergebnis.**
- Jeder Beitrag im Cockpit trägt die Etiketten seines Hooks.
- Sobald er reif ist (7 Tage), landet das Ergebnis in der Datenbank.
- Einmal im Monat (in `/monatsplan`) ein automatischer Absatz: *welche Etiketten diesen Monat
  gewonnen haben* → `hook-formel-testlog.md` wird dadurch gepflegt statt vergessen.

### Schritt 5 · Sauber testen mit Probe-Reels (laufend)
Das Testlog nennt das Hauptproblem selbst: Video, Thema und Hook wurden gleichzeitig geändert.
Instagram hat dafür **Probe-Reels** (nur Nicht-Followern gezeigt): **dasselbe Video, zwei Hooks**,
beide als Probe-Reel — der Gewinner geht regulär raus. Damit wird ein Hook endlich isoliert messbar.

### Schritt 6 · Knopf im Cockpit (später)
Wenn 1–4 stehen, kommt die Maschine als Knopf auf die Wochenkarte („5 Hooks vorschlagen“), über den
Wissensbrief, der ohnehin schon in beiden Artifacts liegt. Die Datenbank geht als Auszug mit
(die 50 stärksten eigenen Hooks), nicht vollständig.

---

## 4 · Ehrliche Erwartung

- Die Maschine macht Hooks **treffsicherer und schneller** — sie macht aus einem schwachen Video
  oder einem Thema, das niemanden betrifft, keinen Einschlag. Der Testlog sagt: candid Video ist der
  Hebel Nummer eins.
- Der Nutzen wächst mit den Daten. Mit 392 reifen Beiträgen ist der Start gut; nach 3 Monaten
  Schleife weiss das System mehr über ihr Publikum als jede gekaufte KI.
- Kosten: Etikettieren aller Beiträge einmalig ein paar Franken (Haiku), danach Rappenbeträge.

## 5 · Reihenfolge-Empfehlung

**Schritt 1 zuerst.** Er beantwortet allein schon die Frage „warum sind die Ergebnisse nicht so toll“
mit ihren eigenen Zahlen, und alles andere baut darauf.

---

## 🔗 Verwandte Notizen

- [[hook-formel-testlog]]
- [[2026-09-24-notion-abloesen]]
