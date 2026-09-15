---
tags: [misc, research, ki, externe-wissen]
---

# Webinar Florian Hübner (Mr. Tech) — 15.09.2026

**Live-Notizen von Patricia** (wird während des Webinars gefüllt)

---

## Rohnotizen

<!-- hier kommt rein, was Patricia im Chat schickt — unverändert -->

**Block 1 (Videogenerierung + Arbeitsweise):**
- Empfiehlt zur Video-Generierung: **Higgsfield**, **Nano Banana Pro**, **Kling Motion Control**
- Überarbeitet **alle seine Präsentationen mit Claude** — Ansage an Claude: *"maximaler Business-Impact"*
  → Patricias Randnotiz: das ist für meine Präsentationen sicher auch eine gute Empfehlung
- Sein Webinar läuft über **WebinarJam**
- Nennt **Claude als besten KI-Agenten**
- Zeigt live, wie er mit Claude baut:
  1. Präsentationen
  2. Webseiten für sein Angebot
  3. ein **Business-Dashboard** mit Infos zu den grossen Unternehmen, die für ihn relevant sind
  4. daraus automatisch **personalisierte Mail-Entwürfe pro Unternehmen**

**Block 2 — „Du brauchst einen KI-Marketingstrategie-Assistenten"**
- Seine Ansage an den Raum. Führt zum Angebot (Masterclass 49 € → Club 2.990 €).

**Block 3 — Der KI-Marketing-Blueprint, 4 Steps** *(Folie)*
> „So baust du eine skalierbare Umsatzmaschine mit KI:"
1. ✅ Zielgruppe definieren & Positionierung schärfen
2. ❌ (Virale) Contentformate festlegen
3. ❌ Storyline + Hook entwickeln
4. ❌ Monetarisierungswege skizzieren

Die Häkchen/Kreuze sind sein Verkaufsmittel — Schritt 1 „hast du schon", 2–4 fehlen.
→ Patricia hat alle vier. **Sein Blueprint hat keinen Schritt für Reichweite und
keinen fürs Messen** — genau dort sitzt aber ihr Engpass (Juli-Launch: 3 Verkäufe,
0 neue Leads).

**Block 4 — KI-getriebene Content-Produktion, Schritt 1: „Out-of-the-box Content"** *(Folie)*
- Zeigt seinen Custom GPT **„Viraler Content Assistent"** (von startup-creator.com):
  *„Gebe deine Content Strategie vor und lasse dir von mir viralen Content erstellen."*
- Ein Chat-Fenster: Strategie jedes Mal neu eintippen, Text kommt raus, selber kopieren.
- → Entspricht `/content`, aber ohne Datenanbindung und ohne Auslieferung.
- **Abschauen: die Haustür.** Ein benannter Assistent mit einem Feld statt 30 Skill-Namen.

**Block 5 — „Hook, Hook, Hook!"** *(Folie)*
> Step 1: Die Hook — der Moment, in dem alle hinschauen.
> „1 Sekunde, um jemandem das Gefühl zu geben: ‚WTF, das muss ich sehen!'"

Seine drei Fragen bei jedem Content:
- Was ist der **erste Satz**, der triggert?
- Was ist der **visuelle Einstieg**, der catcht?
- Was ist die **emotionale Reaktion**, die bleibt?

Seine Formel: **Hook = Schock + Relevanz + Neugier**

→ Frage 1 und 3 deckt Patricias letzter Check strenger ab.
→ **Frage 2 fehlt bei ihr komplett** — der Hook-Skill behandelt nur die erste
  *Zeile*, die Visual-QA prüft nur, ob nichts kaputt ist (Gesicht frei, Motiv frei,
  ABAB). Niemand fragt, ob das erste *Bild* den Daumen anhält. **Echte Lücke.**
→ „Schock" nicht übernehmen — das ist seine Marke („kontrovers"). Patricias
  gemessene Entsprechung: **Bekenntnis gewinnt** (vor Hot Take, vor Cliffhanger).

**Block 6 — „die Menschen neugierig machen aufs Ende"**
- Retention über eine offene Schleife. Sein Caption-/Video-Muster dazu aus der
  Recherche: „Schau bis zum Schluss! 😏", Hashtag `#feelsillegal`.
- 🚨 **Vorsicht:** Als *Hook-Familie* ist der Cliffhanger bei Patricia gemessen
  **letzter** — Bekenntnis > Hot Take > Cliffhanger. Die Ankündigung „bleib bis
  zum Schluss" ist ein Versprechen, dem niemand mehr glaubt.
- ✅ Was dagegen trägt: die Schleife **im** Beitrag — eine Frage in Sekunde 3, die
  in Sekunde 25 beantwortet wird, ohne sie anzukündigen. Das nutzt sie bisher wenig.

---

## Verdichtet

### Kernthesen

### Tools

### Workflows / Automatisierungen

### Prompts

#### 🔹 Prompt 1 — Instagram-Analyse über Claude in Chrome

**So wie er es im Webinar gezeigt hat** (Claude in Chrome, eingeloggtes Instagram
offen, Profil-Ansicht):

> analysiere meine letzten 50 posts und gib mir handlungsempfehlungen.
> ich brauch 5 mega virale skripte.

Sein Mechanismus dahinter: Claude sieht den Browser mit, liest die sichtbaren
Beiträge samt Zahlen aus und leitet daraus Muster ab. Kein Export, kein Tool
dazwischen.

---

**Patricias Fassung** — dasselbe, aber mit ihren Regeln und ihrem Markenwissen.
Zu benutzen mit *Claude in Chrome*, wenn Instagram eingeloggt und das Profil
offen ist:

```text
Du siehst mein Instagram-Profil im Browser.

SCHRITT 1 — Daten holen
Geh meine letzten 50 Beiträge durch. Scroll so weit, bis du wirklich 50 hast,
und öffne die Insights, wo sie erreichbar sind. Trag pro Beitrag zusammen:
Datum · Format (Reel/Karussell/Bild) · die erste Zeile des Hooks · Thema ·
CTA-Art (Share / Keyword / Speichern / kein CTA) · Aufrufe · Likes ·
Kommentare · Speicherungen · geteilt.
Sag mir ehrlich, welche Zahlen du NICHT sehen konntest — rate nichts dazu.

SCHRITT 2 — Muster erkennen
Vergleiche Top-10 gegen Flop-10. Ich will keine Wetterbericht-Zusammenfassung,
sondern was die Gewinner GEMEINSAM haben und den Verlierern fehlt. Schau auf:
- Format (Reel vs. Karussell vs. Bild)
- Hook-Art (Bekenntnis · Zeitanker · Hot Take · Frage · Zahl)
- Bewusstseinsstufe: stellt der Hook IHRE Frage oder gibt er schon MEINE Antwort?
- Post-Job: Reichweite · Autorität · Story · Sales
- CTA-Art und ob der CTA überhaupt zum Job passte
- Thema: Mama-Alltag vs. Business-intern vs. Öle
- Cover: Foto mit mir · Lifestyle-Foto · Typo-Template, und welche Farbe
Nenne mir 3 Muster, die ich vorher nicht gesehen habe. Keine Binsen.

SCHRITT 3 — Handlungsempfehlungen
Maximal 5. Jede in dieser Form:
„Hör auf mit X → mach stattdessen Y → weil in meinen eigenen Zahlen [konkreter
Beleg aus Schritt 1]."
Was du nicht belegen kannst, lässt du weg.

SCHRITT 4 — 5 Skripte
Schreib mir 5 Reel-Skripte, die auf genau diesen Mustern aufbauen.
Pro Skript: Hook (die gesprochene erste Zeile, wortwörtlich) · 20-40 Sek
Sprechtext · Titelbild-Text · Caption · CTA.

REGELN, die über allem stehen:
- Meine Stimme: wie ein Anruf bei einer Mama-Freundin. Ganze Sätze mit
  Konjunktionen, kein Stakkato, Schweizer ss statt ß, echte Umlaute.
- Nur MEINE Zahlen und MEINE Szenen. Nichts erfinden — keine Einnahmen,
  keine Teamgrössen, keine Ergebnisse, die ich nicht genannt habe.
- Die Gegenspielerin ist der Job, nicht das Network.
- Keine Netzwerkaufbau-Tipps („besser recruiten") — mein Thema ist das eigene.
- Bei doTERRA keine Heilversprechen, immer „bei mir war es so".
- Der Hook nennt nie die Lösung.
- Mindestens 3 verschiedene Angles über die 5 Skripte, nicht fünfmal derselbe.
- 3 der 5 sind Lead-Posts mit Keyword-CTA (je ein anderes Keyword),
  2 sind reine Reichweiten-Posts mit Share-CTA. (3+2-Regel seit 15.09.2026)

Am Schluss: sag mir in einem Satz, was dir an meinem Profil am meisten im Weg
steht.
```

**🚨 Wichtig — der bessere Weg für die Zahlen:**
Was Claude im Browser sieht, ist nur, was Instagram gerade anzeigt. Reichweite,
Speicherungen und Geteilt-Zahlen holt `scripts/instagram-insights/holen.py`
direkt über die Meta-API — **exakt statt abgelesen**. Ideal ist die Kombination:
Zahlen aus dem Skript, Hooks/Cover/Kommentar-Stimmung über den Browser.

#### 🔹 Prompt 2 — dieselbe Logik auf den Konkurrenz-Scraper

**Patricias Idee (15.09., im Webinar):** Den Analyse-Prompt nicht aufs eigene
Profil richten, sondern auf die Konkurrenz-Accounts, die der Apify-Scraper
ohnehin täglich mitschneidet — Ziel: Skripte, die **Kommentare erzeugen** und
über das Keyword ins Freebie führen.

**Das ist umsetzbar, die Daten liegen schon da.** Stand 15.09.2026:
122 Tagesläufe seit 08.05., je Lauf 12 Beiträge pro Account. Über die Historie
zusammengeführt und nach Post-ID entdoppelt ergibt das:

| Account | unique Posts |
|---|---|
| digitalmamashift | 208 |
| alleinerziehend.erfolgreich | 152 |
| powerfrauenfocus | 110 |
| doterradachcommunity | 108 |
| katharina.lewald | 63 |
| oele_zauberland_mit_manuela | 60 |
| flowterra.community | 50 |
| oilistic.health | 48 |
| annabraun_coaching | 47 |

🚨 **Was der Scraper NICHT liefert:** Aufrufe, Speicherungen, geteilt. Das sind
private Insights, die kein Scraper sieht. Vorhanden sind pro Beitrag:
`caption` · `hashtags` · `likesCount` · **`commentsCount`** · `timestamp` ·
`type` (Reel/Karussell/Bild) · `url`.
→ Glücklicher Zufall: Für **dieses** Ziel reicht das genau, weil
Kommentar-Zahlen das Erfolgsmass sind.

```text
Analysiere die letzten 50 Beiträge dieser Konkurrenz-Accounts und leite daraus
10 Reel-Skripte für MICH ab.

DATENQUELLE
Alle Dateien outputs/apify-runs/competitors-*.json zusammenführen und nach
Post-ID entdoppeln. Pro Account die letzten 50 Beiträge nach timestamp.
Accounts: die aus context/competitor-watchlist.json mit profile == "mentoring"
(für doTERRA entsprechend "doterra").
Vorhanden: caption, hashtags, likesCount, commentsCount, timestamp, type, url.
Nicht vorhanden: Aufrufe, Speicherungen, geteilt — rechne nicht damit und
erfinde sie nicht.

SCHRITT 1 — messen statt schätzen
Kommentar-Rate = commentsCount / followersCount. Nach der sortieren, nicht nach
absoluten Likes — sonst gewinnt immer nur der grösste Account.
Zeig mir die Top-20 Beiträge nach Kommentar-Rate, mit Account, Datum, Format,
erster Caption-Zeile, Likes und Kommentaren.

SCHRITT 2 — warum kommentieren die Leute dort?
Geh die Top-20 durch und benenne den Auslöser. Unterscheide sauber:
- explizite Keyword-Aufforderung („kommentiere X")
- offene Frage am Schluss
- Meinungs-Spaltung / Hot Take
- Wiedererkennung, die zum Bekenntnis verleitet („bin ich die einzige, die…")
- Listen-/Vorlagen-Versprechen hinter dem Kommentar
- unecht: Gewinnspiel, Engagement-Bait, gekaufte Kommentare — als solche markieren
Sag mir, welcher Auslöser am häufigsten oben steht und welcher bei MEINER
Zielgruppe trotzdem nicht funktionieren würde.

SCHRITT 3 — Abgleich mit meinem Profil
Was davon habe ich in den letzten 8 Wochen selbst gemacht, was nicht?
Nenn mir die 3 grössten Lücken. Nur belegt — keine Vermutungen.

SCHRITT 4 — 10 Skripte
Pro Skript: Hook (gesprochene erste Zeile, wortwörtlich) · 20-40 Sek Sprechtext ·
Titelbild-Text · Caption · Keyword-CTA · das Freebie dahinter.
Das Keyword und das Freebie kommen aus context/active-funnels.json und
context/manychat-keywords.md — **nie erfinden**.
Gib bei jedem an, von welchem Muster aus Schritt 2 es abgeleitet ist.

REGELN, die über allem stehen:
- Meine Stimme: wie ein Anruf bei einer Mama-Freundin. Ganze Sätze mit
  Konjunktionen, kein Stakkato, Schweizer ss, echte Umlaute.
- Nur MEINE Zahlen und MEINE Szenen. Konkurrenz-Hooks sind Inspiration,
  nie 1:1 abgeschrieben — durch Blackliste und Hook-Check, Szene aus meinem Leben.
- Die Gegenspielerin ist der Job, nicht das Network.
- Keine Netzwerkaufbau-Tipps. Bei doTERRA keine Heilversprechen.
- Der Hook nennt nie die Lösung, und er nennt nie das Keyword —
  der CTA steht in der Caption, nicht im Hook.
- Mindestens 4 verschiedene Angles über die 10 Skripte.
- Vermerke bei jedem Skript, von welchem Konkurrenz-Post die Idee kommt (URL).
- Alle 10 sind Lead-Posts mit Keyword-CTA. Das ist so gewollt —
  keine Quote gegen Reichweiten-Posts rechnen, keine Rückfrage dazu.

Am Schluss: welchen Kommentar-Auslöser nutzen die anderen, den ich noch nie
probiert habe?
```

**Patricias Entscheid 15.09.2026:** Alle 10 sind Lead-Posts. Die frühere
3+1-Quote (3 Reichweite / 1 Lead pro Woche) gilt hier nicht.

#### 🔹 Prompt 3 — „Video-Nachbau-Tool" (Screenshot aus dem Webinar)

Patricias Notiz: *„er zeigt hier ein tool, wo er einfach den link eines profils
schicken kann und dann baut claude code den ganzen content nach für ihn.
die konkrete anleitung schickt er noch."*

**Was auf dem Screenshot tatsächlich steht** (Claude-Code-Fenster, seine Eingabe):

> „Ich brauch ein Tool: Ich will einen **Video-Link** einfügen.
> Und es soll mir das Video 1:1 nachbauen."

Claudes Antwort darauf, in drei Schritten:
1. **Video analysieren** — Link auswerten und beschreiben:
   Szenerie, Schnitte, Bewegungen, Dialoge, Effekte
2. **Prompt generieren** — mit dem *Seedance-Skill* einen Shot-by-Shot-Prompt
   für KI-Video-Generierung (Seedance 2.0, Luma o.ä.)
3. **Video neu generieren** — in ähnlichem Stil, „aber nicht pixel-perfect identisch"

Und die Einschränkung, die Claude selbst dazuschreibt:
> ❌ „Ich kann Copyrighted Videos nicht 1:1 klonen (rechtlich problematisch)"
> ✅ „Ich kann KI-generierte Neuvarianten erstellen (ähnlicher Stil, aber original)"

**Drei Dinge, die vor der Umsetzung geklärt sein müssen:**

1. **Video-Link ≠ Profil-Link.** Der Screenshot zeigt ein Tool für *ein* Video,
   nicht für einen ganzen Kanal. Ob er zusätzlich etwas auf Profil-Ebene gezeigt
   hat, steht noch aus — seine Anleitung kommt nach.
2. **Der Nachbau läuft über Seedance/Higgsfield.** Dazu gibt es bereits eine
   Entscheidung vom 09.06.2026: *„aktuell nichts für mich"* — KI-Fake-Videos
   beissen sich mit dem Brand-Manifest (Nahbar · Anti-Perfekt · Echt) und mit
   doTERRA-Compliance. Siehe `reference_seedance-higgsfield-tool`.
3. **Ein Artifact kann das nicht selbst.** Die Seite darf per CSP keine fremden
   Hosts abrufen und kann kein Video auswerten. Der Weg läuft — wie beim
   Wochenfokus — über Claude: Seite sammelt, Claude holt und arbeitet.

**Was davon für Patricia wirklich taugt: Schritt 1, nicht Schritt 3.**
Die Zerlegung eines Reels in *Hook-Art · Schnittrhythmus · Textebene ·
Bildwechsel · Länge · Kommentar-Auslöser* ist genau das Briefing, das `/reels`
und `/videoschnitt` brauchen — angewendet auf **ihr eigenes** Material.
Nicht nachbauen, sondern die **Mechanik** übernehmen. Deckt sich mit der Regel
*Hooks = Inspiration, nicht Copy-Paste*.

**Buildbar wäre daher:** ein Feld im Cockpit „Reel-Link → Mechanik zerlegen".
Patricia pflückt unterwegs Links, sie landen als Dokument in der
Artifact-Datenbank, Claude wertet sie aus und legt das Briefing in die
Wochen-Vorschau. → **Erst umsetzen, wenn seine Anleitung da ist.**

### Zahlen & Beispiele

### Sein Funnel / Verkaufsmechanik

---

## Für Patricia relevant

| Erkenntnis | Wo einsetzbar | Nächster Schritt |
|---|---|---|

---

## 🔗 Verwandte Notizen

- [[2026-09-15-florian-huebner-mr-tech-recherche]]
