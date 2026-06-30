---
tags: [produkt, mba, architektur, thrivecart]
---

# MBA — Academy-Architektur auf ThriveCart Academy

> Erarbeitet 2026-06-30 (Modus 3 /produkt) nach Analyse von Patricias eigenem Jahres-Setting auf Skool (Elevate).
> Diese Datei: **roter Faden + ThriveCart-Mapping + PIA-Einbettung**.
> Schwester-Datei: [[11-willkommens-modul-und-callplan]] (Onboarding-Skript + Umsetzerinnen-Call-12-Monatsplan).

---

## 0. Die Grundentscheidung: Was läuft wo?

ThriveCart Academy kann nur den **Classroom-Teil** von Skool (Kurse → Module → Lektionen + Fortschritt + Login). Es hat **keinen** Community-Feed, **keinen** Kalender, **kein** Leaderboard. Darum splitten wir bewusst auf — und das passt zu Patricias Plan (Community = Telegram, Calls = Zoom):

| Funktion | Skool (Elevate) | MBA-Lösung |
|---|---|---|
| Kurse + Lektionen + Fortschritt | Classroom | **ThriveCart Academy** |
| Community / Austausch / Q&A-Posts | Community-Feed | **Telegram-Gruppe** (Di & Do von Patricia betreut) |
| Live-Call-Termine | Calendar | **Zoom + fixer Wochentag** (Termin in Telegram angepinnt + Mail-Reminder über AC) |
| Call-Aufzeichnungen | „LIVE Calls"-Kachel | **„Kurs" in ThriveCart Academy** (datierte Lektionen, siehe unten) |
| KI-Tool | ARIA / Claude-Kachel | **PIA** (eigene Kachel + Einbettung in jeden Kurs) |
| Gamification | Leaderboard | **bewusst weglassen** in Runde 1 (Pioneer ist klein + persönlich → Telegram-Nähe ersetzt Punkte) |
| Onboarding | „Starte hier → Deine ersten 30 Tage"-Post | **Willkommens-Kurs** in ThriveCart (Pflicht-Kachel ganz oben) |

**Merksatz für Patricia:** ThriveCart hält die *Inhalte*, Telegram hält die *Menschen*, Zoom hält die *Live-Momente*, PIA hält die *Umsetzung*. Vier Tools, ein roter Faden.

---

## 1. Der rote Faden — die Member-Journey

Das Versprechen der Salespage: *„den ganzen Weg in der richtigen Reihenfolge — und jemanden, der mit dir dranbleibt."* Damit das kein leeres Wort bleibt, braucht die Academy eine **sichtbare Reihenfolge**, nicht nur eine Kachel-Sammlung. Das ist genau die Lücke, die Elevate hat (dort liegen 21 Kacheln flach nebeneinander, neue Mitglieder fragen im Feed „wo fange ich an?").

### Die 4 Phasen (= die 4 Etappen aus dem Steckbrief)

```
PHASE 0 — ANKOMMEN           → Willkommens-Kurs (Pflicht, 20 Min)
   ↓   "Ich weiss, wo ich bin und was als Erstes dran ist."

PHASE 1 — SICHTBAR WERDEN    → Instagram-Kundenmaschine
   ↓   "Fremde Frauen schreiben MICH an, statt dass ich jage."

PHASE 2 — ZEIT & STRUKTUR    → Mama-CEO
   ↓   "Mein Business findet in wenigen fokussierten Stunden statt."

PHASE 3 — EIGENES ANGEBOT    → Digitale Produktwelt
   ↓   "Ich habe ein Einkommen, das mir gehört."

DURCHGEHEND — DRANBLEIBEN    → PIA (täglich) + Umsetzerinnen-Calls (2×/Monat) + Telegram (Di & Do)
       "Ich setze um, statt nur zu lernen — nie allein."
```

### Warum diese Reihenfolge (und nicht die andere)

- **Sichtbar VOR Angebot:** Eine Mama braucht erst ein anziehendes Profil und Reichweite, sonst verkauft sie ihr digitales Angebot später ins Leere. Erst das Schaufenster, dann die Ware.
- **Zeit & Struktur in der Mitte:** Ohne Power-Slots und ein aufgeräumtes System kommt sie zwischen Phase 1 und 3 nicht ins Tun — Mama-CEO ist der Motor, der die anderen beiden überhaupt fahrbar macht.
- **Eigenes Angebot zuletzt:** Das ist der grösste Sprung (E→M / M→Z) und braucht Sichtbarkeit + Zeit als Fundament.

> ⚠️ **Wichtig — kein Zwang, aber klare Empfehlung.** Wie bei Elevate gilt: *„Am besten folgst du der Reihenfolge, du kannst aber auch dort starten, wo du gerade stehst."* Wer schon sichtbar ist, springt zu Mama-CEO. Die Reihenfolge ist der empfohlene Pfad, kein Drip-Gefängnis.

---

## 2. Die Classroom-Struktur in ThriveCart Academy

ThriveCart-Hierarchie: **Bundle → Kurse → Module (Lektionen-Gruppen) → Lektionen.** Eine Lektion = Video + Text + optional Download (Arbeitsblatt). Genau wie eine Skool-Lektion.

### Die Kachel-Reihenfolge (so sieht die Mama ihr Dashboard)

| # | Kachel (= „Kurs" in ThriveCart) | Typ | Funktion |
|---|---|---|---|
| 1 | **🎯 Start hier — Deine MBA-Landkarte** | Willkommens-Kurs | Onboarding, 20 Min. Details: [[11-willkommens-modul-und-callplan]] |
| 2 | **🤖 PIA — deine KI-Mentorin** | Tool-Kachel | Wie PIA andockt + Login + Befehls-Übersicht |
| 3 | **📱 Instagram-Kundenmaschine** | Kurs (existiert) | Phase 1 |
| 4 | **⏰ Mama-CEO** | Kurs (existiert) | Phase 2 |
| 5 | **🚀 Digitale Produktwelt** | Kurs (existiert) | Phase 3 |
| 6 | **🤝 Die Umsetzerinnen — Calls & Aufzeichnungen** | Call-Archiv-Kurs | Datierte Lektionen (s. u.) |
| 7 | **🎁 Bonus & Vorlagen** | Material-Kurs | Downloads, Swipe-Files, Vorlagen |

**Cover-Bilder:** Jede Kachel kriegt ein Brand-Cover (Petrol/Creme + Philosopher-Font), damit das Dashboard wie EINE Academy wirkt und nicht wie zusammengewürfelte Kurse. (Canva-Briefing folgt nach deiner Freigabe der Struktur.)

### Sortier-Trick gegen das Elevate-Problem

Bei Elevate steht „Werde Partner" als erste Kachel und der inhaltliche Einstieg geht unter. **Bei uns steht „Start hier" zwingend Position 1, PIA Position 2** — die Mama sieht zuerst, wo sie anfängt und wer ihr hilft, bevor sie irgendetwas anderes sieht. Reihenfolge ist Führung.

---

## 3. Die Umsetzerinnen-Call-Kachel (der Elevate-Clou)

In Elevate ist „LIVE Calls mit Julia" innen eine Liste **datierter Lektionen**, nach Jahr gruppiert:
```
2026
  04. Januar - Dein eigener GPT + Positionierung   (Video 1:02:05)
  14. Januar - Mein neuer Funnel
  27. Januar - Positionierung
  ...
```
Jeder Call wird nach der Aufzeichnung als neue Lektion eingehängt. So wächst die Kachel zu einem **lebendigen Aufzeichnungs-Archiv** — und ist gleichzeitig der Beweis auf der Salespage („über ein Jahr Begleitung").

**So bauen wir es in ThriveCart:**

- Kurs „🤝 Die Umsetzerinnen" mit **2 Modulen**:
  - **Modul A — Experten-/Themen-Calls** (1×/Monat, mit Q&A)
  - **Modul B — Reine Q&A-Calls** (1×/Monat)
- Pro Call eine Lektion: Titel = `[Datum] [Uhrzeit] — [Thema]`, Inhalt = Zoom-Aufzeichnung (eingebettet/Link) + 2–3 Zeilen „darum ging's" + ggf. Download.
- **Drip aus:** alle Aufzeichnungen frei zugänglich (anders als Kurs-Lektionen). Wer nicht live dabei war, schaut nach — exakt das Versprechen aus dem Steckbrief.

Der 12-Monats-Themenplan für Modul A steht in [[11-willkommens-modul-und-callplan]].

---

## 4. PIA-Einbettung in den Lernweg

PIA ist das, was bei Elevate „ARIA" + „Claude" als Kachel sind — nur ist PIA **deine eigene** KI-Mentorin und damit der Killer-USP. Sie darf nicht als isoliertes Tool danebenstehen, sondern muss an **jedem Punkt der Journey** andocken: „Lern es im Kurs → setz es sofort mit PIA um."

### PIA-Befehl ↔ Kurs-Modul-Matrix

| Phase / Kurs | Was die Mama lernt | PIA nimmt ihr ab (Befehl) |
|---|---|---|
| **Onboarding** | Wo stehe ich, was ist mein Thema | `/onboarding` → Profil-Setup, damit PIA in ihrer Stimme schreibt |
| **Instagram-Kundenmaschine** — Positionierung | Thema + Experten-Satz finden | `/positionierung` → Experten-Satz-Vorschläge |
| — Schaufenster | Bio + Highlights + gepinnte Posts | `/bio` → fertige Bio in ihrer Stimme |
| — Content | Hooks, Captions, Posts | `/hooks` · `/post` · `/woche` (ganze Content-Woche) |
| — Leads | Freebie / Lead-Magnet | `/leadmagnet` → Konzept + Outline |
| **Mama-CEO** — Struktur | Power-Slots, Hütchenmethode, Notion | (Umsetzung manuell; PIA als Sparrings-Partner für Wochenplan) |
| **Digitale Produktwelt** — Angebot | Produkttreppe + Funnel | `/produkt` · `/funnel` · `/salespage` → Entwürfe in ihrer Stimme |

> Jede relevante Kurs-Lektion endet mit einem **„Jetzt mit PIA"-Block**: *„Du hast's gelernt — jetzt lass PIA es mit dir machen. Tippe `/hooks` und du hast in 2 Minuten 10 Hooks in deiner Stimme."* So wird PIA vom Bonus zum täglichen Begleiter (= Dranbleiben-Versprechen).

### PIA-Kachel-Inhalt (Position 2 im Dashboard)

3 kurze Lektionen:
1. **Was PIA ist + Login** (E-Mail + Passwort — siehe [[project_pia-login-email-passwort]])
2. **Dein erstes Mal mit PIA** (`/onboarding` Schritt für Schritt)
3. **Alle PIA-Befehle auf einen Blick** (die Matrix oben als Mama-Sprache-Cheatsheet)

---

## 5. ThriveCart-Academy-Setup — die Schritte für Patricia (kein Vorwissen nötig)

Da du ThriveCart Academy noch nicht kennst — hier der konkrete Bau-Pfad. (Ich kann jeden Schritt mit dir live über Chrome machen, sobald die Struktur steht.)

1. **In ThriveCart → „Learn"/„Academy" aktivieren** (ist im ThriveCart-Account enthalten, kein Extra-Tool).
2. **Bundle anlegen:** „Mum Business Academy" — ein Bundle, das beim Kauf Zugang zu ALLEN Kursen unten freischaltet.
3. **7 Kurse anlegen** (die 7 Kacheln aus Abschnitt 2). Die 3 bestehenden Kurse (Insta-Kundenmaschine, Mama-CEO, Digitale Produktwelt) als Module + Lektionen einpflegen (Videos hochladen oder einbetten).
4. **Reihenfolge fixieren:** Kurse so sortieren, dass „Start hier" + PIA oben stehen.
5. **Cover-Bilder** pro Kachel hochladen (Brand-Look).
6. **Checkout mit dem Bundle verknüpfen** (hast du fürs Cart-Fenster eh schon — dann „grant access to bundle" einstellen).
7. **Anrechnungs-Logik:** Wer Insta-Kundenmaschine schon einzeln gekauft hat → manueller Gutschein/Preis-Anpassung (ThriveCart kann das über Coupons oder manuelles Konto-Gutschreiben).
8. **Telegram-Gruppe** als Community verlinken (Lektion im Willkommens-Kurs + im Onboarding-Mail).
9. **Zoom-Call-Reihe** terminieren, Aufzeichnungen nach jedem Call in die Umsetzerinnen-Kachel hängen.

> **ThriveCart-Grenzen, die du kennen musst (damit du nicht dagegen rennst):**
> - Kein Community-Feed → Telegram ist Pflicht-Ergänzung, kein „nice to have".
> - Kein nativer Kalender → fixer Call-Wochentag + Telegram-Pin + AC-Reminder-Mail.
> - Design ist schlichter als Skool → die Cover-Bilder machen den Marken-Look, nicht die Plattform.
> - Kein Leaderboard → in Pioneer-Runde bewusst verzichtbar; die kleine, enge Gruppe lebt von Telegram-Nähe.

---

## 6. Skool vs. ThriveCart Academy — soll Patricia wechseln?

Ehrliche Einordnung (Patricia ist ja selbst auf Skool und überlegt ThriveCart):

| Kriterium | Skool | ThriveCart Academy |
|---|---|---|
| Alles-in-einem (Kurs+Community+Calendar) | ✅ ja | ❌ nein (3 Tools) |
| Kosten | ~99 USD/Monat extra | im ThriveCart enthalten (kein Extra) |
| Checkout/Verkauf integriert | ❌ extern nötig | ✅ ist DER Checkout |
| Community-Gefühl/Gamification | ✅ stark | ❌ via Telegram nachbauen |
| Du hast es schon | Checkout läuft eh über ThriveCart | ✅ |

**Empfehlung für die Pioneer-Runde:** ThriveCart Academy nehmen. Gründe: (1) Checkout + Kurs aus einer Hand, keine Doppelkosten, (2) die Pioneer-Gruppe ist klein und lebt von **deiner persönlichen Telegram-Nähe** — da brauchst du kein Leaderboard, (3) du lernst die Plattform an einer überschaubaren Runde kennen. Wenn die Community auf 50+ wächst und das Telegram unübersichtlich wird, kannst du später immer noch über Skool/Circle für den Community-Teil nachdenken — der Kurs-Kern bleibt dann trotzdem ThriveCart.

---

## 🔗 Verwandte Notizen
- [[11-willkommens-modul-und-callplan]] — Onboarding-Skript + 12-Monats-Call-Plan
- [[mba-produktsteckbrief]] · [[mba-salespage]]
- [[project_mba-plattform-thrivecart-academy]] · [[project_pia-login-email-passwort]]
- [[feedback_KRITISCH-mba-bundle-struktur]]
