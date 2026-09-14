---
tags: [plan, automation, monatsplan]
---

# Monatsabschluss-Automatik — am Letzten ist der nächste Monat geplant

**Erstellt:** 2026-09-14 · **Auftrag von Patricia:** Am vorletzten Tag des Monats
holt ein Task automatisch alle Zahlen, trägt sie nach, schlägt Recycling-Posts
fixfertig im Cockpit vor — und legt die Fragen hin, die es braucht, um den
nächsten Monat samt allen Wochen anzulegen. **Ziel: am letzten Tag des Monats
ist der Folgemonat durchgeplant.**

**Erster Testlauf:** 29./30. September 2026, von Hand begleitet.
**Gebaut wird:** nach dem Startklar-Launch (ab 22.9.).

---

## Das Design in drei Phasen

### Phase A — vollautomatisch, 29. des Monats morgens

Läuft ohne Patricia. Ein Scheduled Task, Muster wie `cockpit-daten-abgleich`.

| Schritt | Quelle | Ziel |
|---|---|---|
| Instagram-Zahlen aller Posts des Monats | Graph API (steht seit 14.9.) | `outputs/instagram-insights/` + Notion Content-DB |
| Follower-Stand beide Profile | Graph API | Notion Reichweiten-Tracking |
| Umsatz des Monats | ThriveCart `/transactions` (**noch zu bauen**) | Notion Kennzahlen |
| Listen, Öffnungsraten | ActiveCampaign MCP | Notion Reichweiten |
| Top-Performer erkennen + Recycling bauen | aus den IG-Zahlen | Cockpit als fertige Reel-Entwürfe |
| Vormonats-Diagnose schreiben | alles oben | `outputs/monatsplaene/` + Telegram |
| Die acht Fragen vorbereiten | `/monatsplan` | Telegram + Notion-Aufgabe |

### Phase B — zehn Minuten mit Patricia, 29./30.

Sie liest die Diagnose, beantwortet die acht Fragen im Chat. Mehr nicht.

### Phase C — automatisch nach den Antworten

**Vier Ebenen, eine Entscheidung.** Patricia legt den Monatsfokus fest, alles
darunter leitet sich ab. Sie plant Wochen und Tage **nicht mehr einzeln**.

#### Ebene 1 — Monatsfokus

Genau **eine der drei Produkttreppen** trägt den Monat:

| Säule | Treppe (aus `active-funnels.json`) |
|---|---|
| Sichtbarkeit / Instagram | Freebie → Finde dein Thema 39 → Expertin 97 → Instagram-Kundenmaschine 333 |
| Zeit / Struktur | Freebie → Minikurs → Mama-CEO |
| Digitale Produktwelt | Freebie → Minikurs → Digitale Produktwelt |

Alle drei münden in die MBA. Das 1:1 „Aus Nebenbei wird Business" (777) läuft
quer dazu und passt in jeden Monat.

#### Ebene 2 — Wochenthemen innerhalb der Säule

Jede Woche ein eigenes Thema aus derselben Säule, mit dem passenden Produkt
der Treppe. **Beworben wird abwechselnd**, nicht jede Woche dasselbe:

| | Schwerpunkt der Woche | typischer Aufruf |
|---|---|---|
| KW 1 | Einstieg ins Thema | Leadmagnet, Keyword |
| KW 2 | Vertiefung | Minikurs |
| KW 3 | das grosse Versprechen | grosser Kurs, in Stories |
| KW 4 | Zusammenführung | MBA oder 1:1, nur in Stories |

Das ist ein Vorschlag, kein Zwang — der Task legt ihn hin, Patricia verschiebt
ihn, wenn es gerade anders passt. **Feste Regel bleibt:** kein Programm und
kein Preis im Feed, Verkauf läuft über Stories und Mails.

Gefüllt werden je Woche die vier Felder, die `/story`, `/freitag-hooks` und
`/cockpit` auslesen: `Fokus der Woche`, `🎯 Wochen-Hauptprodukt`,
`📅 Sales-Pattern`, `Wochen-CTA`. Die Vorlage fragt sie seit dem 14.9. ab —
vorher tat sie das nicht, deshalb standen sie fast überall leer und die
Content-Skills mussten raten. **Eine Woche ohne diese vier Felder ist für die
Assistenten wertlos.**

#### Ebene 3 — Tage mit Aufgaben

Für jeden Werktag des Monats ein Tagesplaner-Eintrag mit `Tagesfokus`, dazu
die Aufgaben mit Datum in der Aufgaben-DB. Zusammengesetzt aus:

- **Hauptbrocken nach Wochentag** (steht fest): Mo Wochen-Content · Di doTERRA
  · Mi Business-Struktur · Do Produktentwicklung · Fr Newsletter + Weiterbildung
- **Monatliche Fixpunkte:** doTERRA-Newsletter + Bestellung am 1., Mums
  Bestellung + PO9 am 10., Backoffice-Check um den 20.
- **Vorlagen-Aufgaben** aus der Aufgaben-DB (Status „Vorlage") auf die Wochen verteilt
- **Produktarbeit aus dem Monatsfokus** — was gebaut, aufgenommen, geschrieben
  werden muss, in Halbtagen geschnitten
- **Ferien und reduzierte Wochen** aus der Energie-Lage-Antwort

⚠️ **Ehrlich zur Tagesplanung:** Ein Monat im Voraus auf Tage verteilt hält
nie ganz. Deshalb plant der Task **Halbtage, keine Stunden**, und markiert
jeden Tag mit höchstens einem Hauptbrocken plus zwei kleineren Aufgaben. Was
verschoben wird, zieht der nächste Wochenblick nach. Ein zu enges Gerüst wird
sonst nach zehn Tagen ignoriert — und dann ist es schlechter als keins.

#### Ebene 4 — Dateien

`outputs/monatsplaene/JJJJ-MM.md`, getrennt nach Mentoring und doTERRA.

---

## Recycling — welche Posts und wie

**Auswahl** (alles muss zutreffen):
- Reichweite über dem Monatsdurchschnitt des Profils
- mindestens 4 Wochen alt (Patricias bestehende Repost-Regel)
- noch nie recycelt — Abgleich über die Relation `Recycling Content` in der
  Content-DB
- höchstens 2 pro Profil und Monat

**Was im Cockpit landet** — ein fertiger Reel-Entwurf, den sie nur freigibt:
- `videourl` aus dem Graph-API-Feld `media_url` des Originals
- `name`, `hook`, Original-Caption zum Vergleich
- **neue Caption**, nicht die alte — mit anderem Einstieg, damit es kein
  Doppelposting ist
- `datum` bleibt leer, das setzt Patricia
- `textfrei: false` — muss durch ihre Freigabe

⚠️ **`media_url` ist zeitlich begrenzt gültig.** Wenn die Adresse im Cockpit
abläuft, bevor sie das Reel baut, ist das Video weg. Erster Lauf zeigt, wie
lange sie hält; falls zu kurz, wird die Datei heruntergeladen und als Asset
ans Artifact gehängt.

---

## Was noch gebaut werden muss

1. **ThriveCart-Umsätze** — `/transactions` in `scripts/cockpit/thrivecart-holen.py`
   ergänzen. Einziger Endpunkt, der noch fehlt. ~1 Std.
   → **Von Patricia bestätigt: wird gebaut.**
2. **Monatslauf** — `scripts/monatsabschluss/` mit den Schritten aus Phase A. ~2 Std.
3. **Notion-Schreiber** — Kennzahlen, Reichweiten, Content-Performance
   nachtragen. Zuordnung Post → Notion-Eintrag über das Veröffentlichungsdatum. ~1 Std.
4. **Wochen-Anleger** — aus dem beantworteten Interview die 4–5
   Wochenplanungen erzeugen, inklusive der Produkt-Rotation über die Wochen. ~1 Std.
5. **Tages-Anleger** — für jeden Werktag einen Tagesplaner-Eintrag mit
   Tagesfokus plus die datierten Aufgaben. Braucht die Hauptbrocken-Rotation,
   die monatlichen Fixpunkte und die Vorlagen-Aufgaben. ~1,5 Std.
6. **Scheduled Task** anlegen, Cron `0 7 29 * *`.

---

## Entscheidungen (alle von Patricia bestätigt, 14.9.)

### 1. Welche doTERRA-Zahl gilt? — GEKLÄRT

**`Gewinn doTERRA` = Primärbonus + Sekundärbonus.** Patricia wusste das, mir
war beim ersten Abgleich nur der Primärbonus aufgefallen — daher die
scheinbare Abweichung.

Der Sekundärbonus läuft in Kalenderwochen und wird dem Monat zugeordnet, in
dem er ausbezahlt wurde. An vier Monaten auf den Rappen belegt:

| Monat | Primär | + Sekundär | = | Notion |
|---|---|---|---|---|
| Januar | 806.13 | KW 1–5 (266.65) | 1'072.78 | 1'072.78 ✓ |
| Februar | 510.66 | KW 6–8 (41.85) | 552.51 | 552.51 ✓ |
| März | 437.51 | KW 10–13 (145.54) | 583.05 | 583.05 ✓ |
| April | 494.58 | KW 14–18 (87.28) | 581.86 | 581.86 ✓ |

Fehlende Wochen (KW 9, 17) hatten schlicht keinen Sekundärbonus.

**Der Automatismus rechnet künftig selbst.** Rechenweg dokumentiert in
`context/doterra/backoffice/provisionen-2026.txt`.

⚠️ **Mai und Juni sind Ausreisser** — dort steht in Notion weniger als der
Primärbonus allein (Lücke je rund 42), die Zahl kam also aus einer anderen
Quelle. Nach der Formel müsste es heissen: **Mai 474.41 · Juni 460.17 · Juli
474.75**. Ob die drei Werte korrigiert werden, ist noch offen — es hebt den
Jahresstand an.

### 2. Wann kommt die doTERRA-Provision? — ENTSCHIEDEN (Patricia, 14.9.)

Sie wird immer erst Mitte des Folgemonats abgerechnet. Am 29.9. steht die
September-Zahl nirgends — heute, am 14.9., fehlt sogar noch der August.

**Entschieden: kein zweiter Lauf, doTERRA läuft im Hauptlauf hinterher.**

Umgesetzt wird das nicht als starre „minus zwei Monate"-Regel, sondern so:
**Der Task liest die komplette Provisionsübersicht und trägt jeden Monat nach,
der im Backoffice steht und in Notion noch fehlt** — jeweils in seine eigene
Monatszeile. Am 29.9. holt er damit den August, wenn er bis dahin abgerechnet
ist, und sonst eben erst am 29.10. Kein Monat fällt durch, keine Zahl landet
in der falschen Zeile, und niemand muss sich merken, ab wann welcher Monat da
ist.

Praktisch heisst das: **doTERRA hinkt im laufenden Monatsbericht immer ein bis
zwei Monate hinterher.** Steht so im Bericht, damit die Lücke nicht wie ein
Umsatzeinbruch aussieht.

Der doTERRA-Teil kommt aus dem Back Office über den Browser und braucht eine
aktive Anmeldung. Läuft er ins Leere, meldet der Task das, statt still nichts
zu tun.

---

## Grenzen, die bleiben

- **Der Task läuft nur bei offener App.** Ist sie am 29. zu, läuft er beim
  nächsten Start nach.
- **Das doTERRA-Instagram-Profil fehlt noch.** Die Seite *Mama.energise* war im
  Meta-Freigabe-Dialog nicht dabei, und @patricia_ulmann hängt nicht als
  Professional-Account an ihr. Bis das steht, liefert Phase A nur Mentoring-Zahlen.
- **Rückwirkende Follower-Stände gibt es nicht.** Die Lücken Februar bis August
  in der Reichweiten-DB bleiben leer.
- **Die acht Fragen beantwortet niemand ausser Patricia.** Der Task legt sie
  hin, mehr nicht — Strategie wird nicht erfunden.

---

## 🔗 Verwandte Notizen

- [[2026-09-13-content-maschine]]
- [[../outputs/instagram-insights/_INDEX|Instagram-Zahlen]]
