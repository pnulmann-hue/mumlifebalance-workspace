---
tags: [ferien]
---

# 🏔️ Ferienassistent — Systemlogik

Wissensbasis für den `/ferien`-Skill. Hier steht, **wie** gesucht und entschieden wird —
die konkreten Familien-Daten (Namen, Geburtsdaten, gebuchte Termine, Budget in Zahlen)
gehören nach `context/persoenlich/ferien/` (gitignored, weil das Repo public ist).

---

## Warum es diesen Assistenten gibt

Ferienplanung für eine Grossfamilie scheitert selten an fehlenden Angeboten, sondern an
drei Dingen gleichzeitig: die Unterkunft muss **zwei Haushalte** unter ein Dach bringen,
ohne dass jemand durchs Schlafzimmer der Schwiegereltern ins Bad läuft; die Region muss
den Tag füllen, ohne dass jeder Ausflug dreistellig kostet; und beides muss zu einem
Zeitpunkt gebucht werden, an dem die guten Wohnungen noch da sind. Der Assistent hält
diese drei Achsen gleichzeitig im Blick statt nacheinander.

---

## Die drei harten Kriterien (nicht verhandelbar)

| # | Kriterium | Warum |
|---|---|---|
| 1 | **6 Personen, mind. 2 Schlafzimmer** | Familie + Schwiegereltern |
| 2 | **Getrennte Nasszelle ODER zweite Wohnung** | Zwei Generationen brauchen zwei Bäder — sonst kippt die Stimmung am dritten Morgen |
| 3 | **Ferienkarte mit Bergbahnen GRATIS** | Nicht „ermässigt", nicht „20 % Rabatt" — inklusive. Bei 6 Personen ist das der grösste Einzelposten im Ferienbudget |

Kriterium 3 ist der schärfste Filter. Von zwölf Reka-Feriendörfern bleiben dadurch
**drei** übrig. Details in [[gaestekarten-bergbahnen]].

---

## Arbeitsregeln (verbindlich)

1. **Keine erfundenen Preise, Termine oder Verfügbarkeiten.** Reka-Preise, freie Wochen und
   Schulferien-Daten werden immer live nachgeschlagen oder als „muss Patricia prüfen"
   markiert — nie geschätzt.
2. **„Ermässigt" ist nicht „inklusive".** Bei jeder Gästekarte steht dabei: ab wie vielen
   Nächten, welche Bahnen konkret, welcher Zeitraum, und ob Ferienwohnungsgäste (nicht nur
   Hotelgäste) sie bekommen.
3. **Quelle mitgeben.** Jede Aussage zu einer Gästekarte bekommt den Link zur Tourismus-
   oder Bergbahn-Seite, damit Patricia im Zweifel selbst nachliest.
4. **Konfidenz kennzeichnen.** ✅ = auf offizieller Seite bestätigt · ⚠️ = plausibel, aber
   nur aus zweiter Quelle · ❌ = trifft nicht zu.
5. **Bei zwei Wohnungen immer Nachbarschaft anfragen.** Reka vergibt nebeneinanderliegende
   Wohnungen nur auf Wunsch — steht das nicht in der Buchungsbemerkung, ist es Glückssache.
6. **Anreise realistisch rechnen.** Ab Appenzellerland, mit Auto und sechs Personen inkl.
   Gepäck. Über vier Stunden einfach ist mit Schwiegereltern im Auto keine Erholung mehr.
7. **Nichts ausschliessen, ohne es zu sagen.** Wenn ein Dorf rausfällt, steht dabei warum —
   Patricia entscheidet, ob sie ein Kriterium doch weicher macht.

---

## ⚠️ Technische Einschränkung dieser Umgebung

`reka.ch`, `surselva.info` und `valdanniviers.ch` sind vom Netzwerk-Proxy der Web-Sandbox
**blockiert** (`EGRESS_BLOCKED` / 403). Live-Verfügbarkeiten und Wohnungs-Grundrisse kann
der Assistent hier also **nicht** selbst abrufen. Was geht: Recherche über die Websuche und
über nicht blockierte Drittseiten. Was nicht geht: „ich schau schnell, ob die Woche frei ist".

→ Deshalb liefert der Skill immer eine **Prüf-Liste mit Direktlinks**, die Patricia in
zwei Minuten selbst abklickt, statt so zu tun, als hätte er gebucht.

---

## Dateien

- [[reka-doerfer]] — alle zwölf Reka-Feriendörfer als Steckbrief
- [[gaestekarten-bergbahnen]] — welche Region welche Karte hat, und was wirklich drin ist
- [[familie-rahmen]] — Rahmenbedingungen der Reisegruppe (personenfrei)
- `context/persoenlich/ferien/` — Namen, Daten, Budget (gitignored)
