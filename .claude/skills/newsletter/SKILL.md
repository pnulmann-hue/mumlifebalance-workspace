---
name: newsletter
description: >-
  Plant und schreibt, was per Mail an die Liste geht: den wöchentlichen Newsletter,
  eine Aktion mit Frist oder eine ganze Launch-Strecke, für Mentoring und doTERRA.
  Entscheidet, welche Mails es braucht, schreibt sie und legt sie als Entwurf in
  ActiveCampaign an. Dran bei /newsletter, „schreib mir den Newsletter“, „was schicke
  ich diese Woche an die Liste“, „Mail an alle“, „Launch-Mails“, „48-Stunden-Aktion“,
  auch wenn das Wort Newsletter nicht fällt.
---

# /newsletter — vom Monatsplan zum fertigen Entwurf in ActiveCampaign

**Aufruf:** `/newsletter` · `/newsletter aktion <angebot>` · `/newsletter launch <angebot>` ·
`/newsletter auswerten`

## Wofür dieser Skill da ist

Am Ende steht eine Mail, die Patricia nur noch lesen und abschicken muss. Die Liste bekommt
sonst keine Post: Die Automationen erreichen nur, wer gerade in einem Ablauf steht, und das
ist die kleine Minderheit. Dieser Skill schliesst die Lücke, und er sorgt dafür, dass die
nächste Launch-Mail nicht aus dem Nichts kommt.

**Zuständig ist je Auftrag einer:** Dieser Skill entscheidet, welche Mails es braucht und
wie viele. `/copywriting` schreibt den Text. `/funnel` baut Tags, Listen und Automationen.

## Vorher lesen

| Datei | Wofür |
|---|---|
| `context/newsletter-regeln.md` | **alle Regeln**: Weiche, Takt, Mail-Aufbau, Hebel, Betreff, Messen. Immer ganz lesen |
| `context/brand-voice.md` · `context/ki-phrasen-blackliste.md` | wie sie schreibt, was nie vorkommt |
| `outputs/monatsplaene/<JJJJ-MM>-mentoring.md` bzw. `-doterra.md` | Monatsthema, Angebot, was gerade läuft |
| `context/active-funnels.json` · `context/link-uebersicht.md` | Angebote, Preise, Links. Nie aus dem Gedächtnis |
| `context/kundinnen-geschichten.md` | echte Fälle, nur mit Freigabe |
| `outputs/newsletter/newsletter-protokoll.md` | was zuletzt beworben wurde und wie es lief |

Bei doTERRA zusätzlich: `context/doterra/energie-story-profil.md`, die Monatsaktion und die
letzte Ausgabe aus `outputs/newsletter/` als Vorbild.

Fertige Launch-Gerüste liegen im Launch-Themenbuch (`reference/**/themen/launch.md`,
Abschnitt 17). Von dort kommt nur der Aufbau, die Sätze schreibt sie selbst.

## Der Ablauf

1. **Profil klären:** Mentoring oder doTERRA. Eine Mail geht nie an beide Listen.
2. **Die Weiche stellen:** Launch, Aktion oder Normalbetrieb, abgelesen aus dem Monatsplan
   und den Regeln. Sag in einem Satz, was du gewählt hast und warum. Läuft ein Launch, pausiert
   der Normalbetrieb.
3. **Angebot vorschlagen:** eines, passend zum Monatsthema, und nicht dasselbe oder derselbe
   Preisbereich wie zuletzt. Nenne die letzten drei Mails aus dem Protokoll zur Begründung.
4. **Eine Frage an Patricia:** *„Was war diese Woche bei dir los, das dazu passt?“* Ihre
   Antwort wird der Einstieg. Mehr fragst du nicht, ausser ein Preis oder eine Frist ist unklar.
5. **Schreiben:** `/copywriting` mit Briefing aufrufen (Profil, Stufe, Angebot, Link, Hebel,
   ihre Szene). Die Betreffzeile ist der Hook der Mail und läuft durch den Hook-Skill.
6. **Prüfen**, bevor Patricia es sieht (siehe unten). Was durchfällt, schreibst du um.
7. **Zeigen und auf ihr Okay warten:** Betreffzeilen und Text im Chat.
8. **Ablegen:** Datei unter `outputs/newsletter/`, Eintrag in `_INDEX.md`, Zeile im Protokoll.
9. **Entwurf anlegen:** `mcp__activecampaign__create_campaign`, Liste vorher mit
   `list_lists` bestätigen, Absender `info@mumlifebalance.ch`. Das HTML kommt aus dem Gerüst
   in `scripts/startklar/mails-bauen.py`, importiert wie in
   `scripts/ki-kurs/masterclass-mails-bauen.py`, nie neu getippt.
10. **Zurücklesen:** Inhalt des Entwurfs in AC abrufen. Ist er leer, sag das und behebe es.

`/newsletter auswerten` holt Zugestellt, Öffnungen und Klicks aus AC, trägt sie im Protokoll
nach und nennt die eine Sache, die in der nächsten Mail anders werden soll.

## Regeln

Die inhaltlichen Regeln stehen in `context/newsletter-regeln.md`. Bewährt sich etwas Neues,
kommt es dorthin, nicht hierher. Für den Ablauf gilt:

- **Nichts verschicken und nichts einplanen.** Der Skill endet beim Entwurf, abschicken
  tut Patricia. Eine Mail lässt sich nicht zurückholen.
- **Nichts erfinden:** keine Szene, keine Zahl, keine Kundenstimme, kein Streichpreis. Fehlt
  etwas, steht dort ✏️ mit einer Frage. Sonst klingt die Mail nach einem Leben, das sie nicht hat.
- **Zwei Ebenen:** Patricias Kundinnen sind Mamas, deren Kundschaft nicht. „Deine Kundin“ ist
  in einer Du-Mail fast immer falsch.
- **Bei doTERRA keine Heilversprechen** und keine Einkommensversprechen. Die Liste verkauft
  über Vertrauen, Launches sind dort nicht vorgesehen.
- **Preis gegen die Kasse prüfen.** Eine Mail, die 199 verspricht, und eine Kasse, die 333
  abbucht, ist schlimmer als keine Aktion.
- **Keine Reaktivierungs- oder Abmelde-Mail vorschlagen.** Das ist entschieden.

## Prüfen vor dem Zeigen

```bash
python scripts/cockpit/texte-pruefen.py --datei <mail.md>
```

Danach von Hand, jede Frage mit Ja:

1. Stehen die fünf Elemente drin: Betreff · Titel · Link mehrfach · Aufruf im Imperativ · PS?
2. Hat sie nach dem Lesen etwas mitbekommen, auch wenn sie nichts kauft?
3. Ein Ziel: überall derselbe Link? Antwortet der Link wirklich (`curl -I`)?
4. Steht im Betreff kein Betrag und kommt nirgends „kaufen“ vor?
5. Gehört eine Frist dazu, stimmt sie auch auf der Zielseite, und läuft wirklich eine Aktion?
6. Ist jede Szene und jede Zahl von Patricia gesagt oder belegt? Was nicht, wird zu ✏️.

## Ausgabe

| Auftrag | Menge |
|---|---|
| **Normalbetrieb** | **1 Mail** mit **3 Betreffzeilen**, 1 Vorschautext, 1 Aufruf, 1 PS, als 1 AC-Entwurf |
| **Aktion** | 1–5 Mails je nach Dauer (Tabelle in den Regeln), je 3 Betreffzeilen |
| **Launch** | zuerst der **Plan mit mindestens 12 Mails** als Tabelle. Nach ihrem Okay die vier festen Mails, dann der Rest |

Datei `outputs/newsletter/JJJJ-MM-TT-<thema>.md`:

```markdown
---
tags: [content, newsletter, mentoring]
---

# Newsletter 4.11.2026 · <Thema>

**Profil · Liste:** … · **Weiche:** Normalbetrieb · **Angebot · Preis · Link:** … · **Hebel:** …

## Betreffzeilen
1. … ← Favorit
2. …
3. …

**Vorschautext:** …

## Mail
…

## Offen
✏️ …
```

Im Chat steht am Schluss: Link zum AC-Entwurf · was noch ✏️ ist · was sie vor dem Abschicken
prüfen muss (etwa Käuferinnen ausschliessen).

## Beispiel, von Patricia

Newsletter vom 29.9.2026, Einladung zur KI-Masterclass:

> **Betreff:** Warum deine KI-Texte nach niemandem klingen
>
> **Vorschautext:** Und was ich dir am Donnerstag, 8. Oktober, live zeige.
>
> kennst du das? Du tippst in ChatGPT oder Claude, worum es geht und für wen der Text ist,
> und zurück kommt etwas, das glatt klingt und nach irgendwem, nur nicht nach dir.
>
> Das liegt weder an dir noch an der KI. Ihr fehlen zwei Dinge. […]
>
> **Knopf:** Platz für die Masterclass sichern
>
> **P.S.** Wenn du bis dahin schon anfangen willst: Im Stimm-Check sammelst du in rund 15
> Minuten die sechs Angaben, die deine KI von dir braucht.

Daran lässt sich ablesen: Der Betreff nennt ihren Ärger und nicht das Angebot. Der Einstieg
geht ohne Anlauf mitten in die Szene. Die Mail erklärt etwas, das auch ohne Anmeldung hilft.
Es gibt einen Aufruf und ein PS, das noch einmal einen Grund liefert.
