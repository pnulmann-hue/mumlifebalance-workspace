---
tags: [content, research]
---

# Marktcheck · Mentoring · KW46–KW49 (9.11.–4.12.2026)

/content Schritt 3, ein Lauf für vier Wochen. Profil **Mentoring** (@mumlifebalance_patricia_ulmann).
Stand 02.11.2026.

**Quellen, in dieser Reihenfolge gewichtet:**
1. **Julia Müller (@juliamueller._, Hauptreferenz)**: Markt-Radar vom 30.10.2026
   (`outputs/marktrecherche/radar/2026-10-30-juliamueller._.md`, 62 Reels, Median 5'017 Aufrufe) und ihre
   letzten zwölf Beiträge aus `outputs/apify-runs/competitors-2026-11-01.json`.
2. Übrige Kern-Nische aus demselben Scrape (Nikoleta Kolokytha, die Fühlbarmacherin, Julia Trost,
   powerfrauenfocus).
3. Eigene Zahlen: Radar des eigenen Kontos (30.10.), `gepostet.json` (heute frisch geholt),
   Hook-Maschine (`beispiele.py`).
4. Echte Kommentare aus der Nische (`outputs/marktrecherche/2026-10-04-nische-gedanken.md`, Abschnitt 5).
5. Websuche (DACH). Reddit liefert über die Websuche für DACH-Network-Themen fast nichts Verwertbares;
   die Treffer sind Ratgeber und ein Bericht über ein Reddit-Forum. Das steht so da, statt es zu füllen.

🚨 Die wöchentlichen `outputs/marktrecherche/KW*.md` sind bewusst **nicht** verwendet (0 Reddit-Posts gelesen).

---

## Treffer-Check (Schritt 2b)

`holen.py --anzahl 15` + `gepostet-bauen.py` am 02.11.2026, Median Mentoring **260**.

| Datum | Hook | Reichweite | Faktor | Kommentare | mögliche Folge-Punkte |
|---|---|---:|---:|---:|---|
| 22.10.2026 | „Mein Büro war vor zwei Jahren der Parkplatz vor der Musikschule.“ | 1'547 | **5,95×** | 0 (1 gespeichert) | nur **3 · 4 · 5** (keine Kommentare für 1 und 2) |

Alle anderen Beiträge der letzten 14 Tage liegen zwischen 51 und 468 (unter 2× Median).
Der Treffer ist am 9.11. **18 Tage** alt. KW45 ist schon gebaut und enthält keinen erkennbaren
Folge-Beitrag. → Vorschlag: **KW46 Montag** wird ein Folge-Reel (Punkt 4, häufigster Fehler), siehe
`auswahl.md`. Patricia entscheidet, ob das nach 18 Tagen noch zählt.

---

## Die vier Dimensionen (Pain · Wunsch · Ziel · Herausforderung)

### Pain

| # | Pain | chronisch/akut | Zitat | Quelle |
|---|---|---|---|---|
| P1 | Sie postet, die Leute schauen, und niemand meldet sich | **chronisch** | „Ich poste ständig, aber es passiert einfach nichts – keine neuen Follower.“ (~30 Beiträge, häufigster Gedanke der Nische) | `2026-10-04-nische-gedanken.md`, Gedanke 1 |
| P2 | Anschreiben fühlt sich falsch an | **chronisch** | „Die Namensliste war für mich der Horror.“ · „OMG ....der Horror jedes Networkers 🙈🙈“ (Kommentare) · Nikoleta 25.10.: „Falls dir gerade jemand gesagt hat, du sollst heute Abend deine Namensliste durchtelefonieren, und dir dabei der Magen zugeht: Mit dir ist alles in Ordnung.“ (10 Kommentare) | Nische-Kommentare; `competitors-2026-11-01.json` |
| P3 | Das Geld, das sie selbst reinsteckt | **akut** | Nikoleta 28.10.: „Mal eine unbequeme Frage: Wie viel von deinem Monatsumsatz kommt eigentlich von echten Kunden und wie viel davon hast du selbst bezahlt?“ (26 Kommentare, einer ihrer stärksten der Woche) | `competitors-2026-11-01.json` |
| P4 | Ihr Umfeld belächelt sie, Freundschaften leiden | **chronisch** | „Eine Freundin verlieren — das ist für viele der schlimmste Aspekt.“ | [selbststaendigkeit.de, Network Marketing Erfahrungen](https://selbststaendigkeit.de/online-geld-verdienen/network-marketing/network-marketing-erfahrungen/); Nische-Gedanke 6 „klar über Ø“ |
| P5 | Sie gibt der Methode recht und sich selbst die Schuld | **chronisch** | „Vielleicht sollte ich einfach aufhören – bringt eh nichts.“ · „Bei allen anderen läuft es, nur bei mir nicht“ | Nische-Gedanken 4 und 10 |

**Patricias eigene Lage passt dazu (belegt, eigene Zahlen):** Radar 30.10.: *„Das grösste Problem liegt
bei der Reaktion, nicht bei der Reichweite.“* Neun von zehn Top-Reels unter 1 % Rate; seit 20.08. 78 von
87 Beiträgen ohne Kommentar. Das ist dieselbe Erfahrung wie P1, nur bei ihr gemessen.

### Wunsch

| # | Wunsch | Zitat | Quelle |
|---|---|---|---|
| W1 | Dass die Leute von selbst kommen statt angeschrieben zu werden | Nikoleta: „So gewinnst du deinen ersten Partner über Instagram. 🎯 Ohne eine einzige Nachricht zu schicken.“ (Faktor 3,55) | Hook-Paket KW46 |
| W2 | Network nicht aufgeben, aber anders machen | Kommentar: „Der Offline Weg ist bei mir kläglich gescheitert. Das ist absolut nicht mein Weg.“ | Nische-Kommentare |
| W3 | Ein Jahr, das zur Familie passt | powerfrauenfocus 01.11.: „November muss nicht der Monat sein, in dem du noch mehr schaffst.“ (663 Likes, ihr stärkster Beitrag der letzten Tage) | `competitors-2026-11-01.json` |

### Ziel

| # | Ziel | Zitat | Quelle |
|---|---|---|---|
| Z1 | 2027 grösser und geplanter angehen | die Fühlbarmacherin 31.10.: „2027 wird es höchste Zeit, im Network Marketing wieder grösser zu denken als bis zum nächsten Instagram Beitrag👌“ (Schreibweise auf ss angepasst) · 30.10.: „Ich glaube, 2027 wird für uns Networker ein richtig spannendes Jahr⭐️“ | `competitors-2026-11-01.json` → das Jahresende-Thema läuft in der Nische schon an |
| Z2 | Ferien und Familie zuerst, Business danach | „Das Business passt sich also an das Leben an, nicht umgekehrt“ (Ratgeber Selbständige) · Schweizer Ratgeber beginnt die Jahresplanung mit dem Sammeln aller Schulferien | [sevdesk, Urlaub für Selbständige](https://sevdesk.de/blog/urlaub-fuer-selbststaendige/) · [familienleben.ch, Ferienbetreuung planen](https://www.familienleben.ch/leben/beruf/ferienbetreuung-in-der-schweiz-schulferien-planen-mit-plan-b-9816) |
| Z3 | Ein Business, das nicht an einer Firma hängt | Julia Müller 06.10. zum Ende von Tupperware in Deutschland: „Ich wünsche von Herzen allen Tupper-Vertriebspartnerin einen erfolgreichen Neustart …🖤“ (**259 Kommentare**, ihr meistkommentierter Beitrag im Scrape). Tupperware Deutschland hat den Geschäftsbetrieb eingestellt | `competitors-2026-11-01.json` · [Stuttgarter Zeitung, Rückzug nach Insolvenz](https://www.stuttgarter-zeitung.de/wirtschaft/rueckzug-nach-insolvenz-endgueltiges-aus-fuer-tupperware-in-deutschland-79027550.html) |

### Herausforderung

| # | Was immer wieder scheitert | Zitat | Quelle |
|---|---|---|---|
| H1 | Der Rat „mehr anschreiben, mehr posten“ bringt nichts | Nikoleta 27.10.: „Du kannst jeden Tag 20 Frauen anschreiben und trotzdem am Ende des Monats ohne neue Kunden oder Partner dastehen.“ | `competitors-2026-11-01.json` |
| H2 | Kurz vor dem Kauf: Angst, dass es wieder nicht klappt | „ich will eigentlich nicht noch mehr geld ausgeben“ · „schauen, wie weit sie selbst kommt“ · dahinter „die angst, dass es nicht klappt“ | `patricia-interview-2026-10.md` D3/D3b (echte Absagen) |
| H3 | Druck, „all in“ zu gehen | Julia Müller 31.10.: „Coaches sagen dazu: „Nimm einen Kredit auf, dann wirst du auch was dafür tun.“ Networker sagen: „Geh all in und kündige doch deinen Job.““ | `competitors-2026-11-01.json` — deckt sich mit Patricias Haltung C2 (kein Investitionsdruck) |

---

## Was Julia Müller zeigt (Hauptreferenz) — Mechanik ja, Wortlaut und Firmennamen nie

- **Der stärkste übertragbare Hebel:** ein kurzer Gegner ohne Firmennamen, „Stoppt den Network-Spam!!!“
  → Faktor 9,99, Rate 1,92 %. Ihr Kern (fremde Firmen beim Namen) ist für Patricia ausgeschlossen.
- **Zitat aus einer typischen Bio als Geständnis** trägt (Faktor 9,25).
- **Flops erreichen wenige, die aber stark antworten** (bis 4,11 %). Fachwörter im Hook („Duplikation“)
  bremsen die Reichweite.
- **Aktuell bei ihr:** Kontaktlisten vs. Community (22.10., 110 Kommentare), Duplikation als „Ketzerei“
  (24.10.), Investitionsdruck (31.10.). Das Jahresende-Thema hat sie noch nicht.

## Brücke zu den vier Wochenfoki

| KW | Fokus (Monatsplan) | trägt sich auf |
|---|---|---|
| KW46 Entdecken | „Ich könnte etwas verschenken, das mir neue Kontakte bringt, ohne dass ich jemanden anschreibe.“ | **P2 + W1 + H1**: die Nische hasst das Anschreiben, Patricias belegte Geschichte (Liste für den Mann → 30 Bestellungen in zwei Tagen → Gespräche mit fremden Mamas) ist genau die Gegenbewegung |
| KW47 Community | „Ich bin nicht die Einzige, bei der sich niemand meldet.“ | **P1 + P5** und Patricias eigene Zahl (fast 2'000 Leute, null Kommentare) als Spiegel |
| KW48 Anwärmen Neustart | „Was hat mir 2026 eigentlich gebracht, und was mache ich 2027 anders?“ | **Z1 + W3**: das Jahresende-Thema läuft in der Nische an, die Ferien-zuerst-Logik ist Patricias Einstieg |
| KW49 Einladung Neustart | „Ich will 2027 nicht wieder planlos anfangen.“ | **Z2 + H2 + H3**: planen ohne Druck, die Angst „klappt wieder nicht“ offen aussprechen |

**Nicht verwendet:** Firmennamen (Julia Müllers Kern), Einkommens-Zahlen anderer, Zukunftsprognosen,
Tupperware als Hook (eine Firma als Gegner ist gesperrt; das Thema darf höchstens in einer Caption als
Hintergrund vorkommen, Entscheid Patricia).
