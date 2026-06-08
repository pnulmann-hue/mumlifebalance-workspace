---
tags: [produkt, launch, mba, challenge, intern]
---

# MBA-Launch als PIA-Challenge — Bauplan

**Erstellt:** 2026-06-08 · **Entscheidung:** Webinar raus, **5-Tage-PIA-Challenge** rein. Challenge die letzte Schulwoche vor den Ferien (Ferienstart **5.7.**). Modell: **ein Morgen-Impuls von Patricia reicht** — Bot + PIA tragen den Rest.

> Ersetzt das Webinar-Modell (siehe [[challenge-vs-webinar-entscheidung]]). Webinar-Assets werden teils recycelt (Cart-Logik + Cart-Mails), nicht weggeworfen.

---

## 1. Timeline (Ferienstart 5.7.)

| Phase | Zeitraum | Was |
|---|---|---|
| **Build** | 8.–24.6. | PIA-Challenge-MVP + Challenge-Bot + Anmeldeseite + Tages-Content |
| **Bewerben** | 15.–28.6. | Reichweite + Warteliste → Challenge-Anmeldungen sammeln |
| **Testrunde** | 24.–26.6. | PIA mit Patricia + 1-2 Pilot-Mamas durchspielen (Qualitäts-Gate) |
| **🔥 Challenge** | **Mo 29.6.–Fr 3.7.** | 5 Tage, Telegram-Gruppe, Morgen-Impuls-Modell |
| **Cart** | **Fr 3.7. (Finale) → So 6.7. 23:59** | Pioneer 997, tight post-Challenge-Close (Vorschlag) |
| **Programmstart** | Mitte August (nach Ferien) | Kurse sofort zugänglich, Live-Calls starten frisch nach den Ferien |

→ 3 Wochen Vorlauf ab heute. Cart läuft async (Mails + Seite) — braucht Patricia nicht live, auch wenn Ferien anfangen.

### Kohorten-Logik (Mama-CEO-Pilot → MBA)
- Die **Mama-CEO-Pilot-Ladys (5 Mamas) schliessen Mama-CEO im Juni/Juli ab**.
- **Ab Ende Juli** wechseln sie in die **MBA** (mit den 2 Calls/Monat).
- **Erster MBA-Live-Call: nach den Sommerferien** (Mitte/Ende August).
- → Im ersten MBA-Call sitzen **beide Gruppen zusammen**: die Pilot-Ladys + die neuen Bootcamp-Käuferinnen (Cart Anfang Juli). Eine warme Gründungs-Kohorte.
- **Bonus für den Pitch:** Die Pilot-Ladys liefern bis dahin **frische echte Erfolgsgeschichten** als Social Proof fürs Bootcamp-Finale.

---

## 2. Das Morgen-Impuls-Modell (Patricias Tagesaufwand = 1 Sprachnotiz)

Identisch zum Story-Bot, den wir am 8.6. getestet haben:

```
Morgens: Patricia schickt 1 Sprachnotiz („heute geht's um X, mein Impuls dazu…")
   ↓
Bot: macht daraus die Tagesaufgabe + Mehrwert-Nachricht → postet in die Challenge-Gruppe
   ↓
Teilnehmerin: chattet mit PIA → bekommt IHR personalisiertes Ergebnis (Bio / Hooks / …)
   ↓
Teilnehmerin: teilt ihren Win in der Gruppe → Community-Effekt
   ↓
Abends (optional): Bot schickt kurze „heute geschafft?"-Erinnerung
```

Patricia ist **nicht** den ganzen Tag live. Empfohlen: 1× live-Moment an **Tag 1** (Kick-off) + **Tag 5** (Finale/Pitch) — der Rest läuft über Bot + PIA.

---

## 3. Die 5-Tage-Challenge (gleiches Thema wie MBA — Pflicht-Regel)

**Versprechen:** „In 5 Tagen vom Gefühl ‚ich verzettel mich' zu deinem ersten klaren Business-Schritt — neben der Familie. Mit PIA, deiner KI-Mentorin, an deiner Seite."

| Tag | Mission | PIA generiert für die Teilnehmerin | Vorgeschmack auf |
|---|---|---|---|
| **1** (live Kick-off) | Dein Thema klar | **Ihre Bio / Positionierung** (Bio-Check-Logik) | Instagram-Kundenmaschine |
| **2** | Sichtbar werden | **3 Hooks für ihr Thema** | Instagram-Kundenmaschine |
| **3** | Zeit schaffen | **Mini-Wochenstruktur / KI-Impuls** | Mama-CEO |
| **4** | Dein Angebot | **Erste Angebots-Idee** | Digitale Produktwelt |
| **5** (live Finale) | Dein roter Faden | **Ihr roter Faden** → Brücke zur MBA | = MBA |

**Build-Priorität:** **Tag 1 (Bio) + Tag 2 (Hooks)** sind der erlebbare Kern und werden zuerst gebaut. Tag 3-5 können leichter sein (PIA-Impuls + Reflexions-Task), falls die Zeit knapp wird.

---

## 4. PIA-Challenge-Scope (fokussierter MVP)

**NICHT** das volle PIA-Tool (das ist die 25-36-Tage-Roadmap). Für die Challenge nur ein **teilnehmer-facing Slice**:

- **Kanal:** Telegram (PIA-Bot ODER ein Mode im bestehenden `content-companion`) — wiederverwendbar: Telegram-Integration, Claude-Integration, Whisper.
- **Was PIA kann (Challenge-Scope):** Onboarding-Kurzprofil (5-6 Fragen: Network-Firma, Thema, Zielgruppe, Lebensphase) → dann pro Tag 1 Generierung (Bio / Hooks / Struktur / Angebot).
- **Wissensbasis:** `patricia-vollprofil.md` (35-Fragen-Logik), `content-radar-*.md` (Hook-Patterns), `hook-framework.md`, Network-Spezifika aus `reference/aria-tool-mentee-konzept.md` (Compliance pro Firma, Crossline-Sprache).
- **Qualitäts-Gate:** vor Live-Gang Testrunde mit Patricia + 1-2 Mamas — PIA-Output muss in Patricia-Voice + Network-spezifisch + ohne erfundene Zahlen sein.
- **Doppelnutzen:** Das ist gleichzeitig **PIAs echter Beta-Test** (steht eh auf der MBA-Roadmap) → die Challenge validiert PIA mit echten Userinnen.

**Reuse-Inventur (laut PIA-Konzept ~70% vorhanden):** Telegram/Claude/Whisper aus `content-companion`, 35-Fragen-Interview, Content-Radar-Patterns, PNG-Render-Pipeline.

---

## 5. Anmeldung + Technik

- **Anmeldeseite:** die `mumlifebalance.ch/mba-webinar`-Seite (WP 3795) → **umbauen zur Challenge-Anmeldung** („Mama-Business-Challenge — 5 Tage, mit PIA").
- **AC:** neues Form + Tag `mba-challenge-anmeldung` (Tag `mba-webinar-anmeldung` 78 kann umgewidmet werden).
- **Gruppe:** Telegram-Challenge-Gruppe (Beitritt nach Anmeldung).
- **Cart:** ThriveCart wie geplant (Pioneer 997 → 1347), Webhook setzt `mba-kauf` (79).

---

## 6. Build-Sequenz (3 Wochen)

| Woche | Build |
|---|---|
| **KW24 (8.–14.6.)** | PIA-Challenge-Bot-Grundgerüst (Onboarding + Tag-1-Bio-Generierung) · Anmeldeseite umbauen · AC-Form/Tag |
| **KW25 (15.–21.6.)** | Tag-2-Hooks-Generierung · Challenge-Tages-Flow im Bot (Morgen-Impuls → Gruppe) · Tag 3-5 Tasks · Bewerben startet |
| **KW26 (22.–28.6.)** | Testrunde mit Patricia + 1-2 Mamas · Feinschliff PIA-Qualität · Cart-Mails auf Challenge anpassen · Anmeldungen sammeln |
| **KW27 (29.6.–3.7.)** | 🔥 Challenge live · Cart-Open Fr 3.7. |

---

## 7. Ehrlicher Rahmen (Risiken + Fallbacks)

- **Build ist ambitioniert.** PIA-MVP + Bot-Flow in 2 Wochen ist straff. **De-Risk:** Wir bauen Tag-1-Bio + Tag-2-Hooks zuerst (der Wow-Kern). Wenn die Zeit knapp wird, laufen Tag 3-5 mit leichteren PIA-Impulsen statt voller Generierung.
- **Fallback wenn PIA nicht rechtzeitig live ist:** Challenge läuft trotzdem — dann generiert PIA im Hintergrund und der Bot/Patricia liefert die Ergebnisse aus (statt Teilnehmerin-Self-Service). Die Challenge ist NICHT Geisel des Builds.
- **Kleine, warme Gruppe statt Masse.** Erwartung: Qualität + Wow, nicht die Blog-15%. Bei intimer Gruppe konvertiert ein echtes Erlebnis stark.
- **Programm startet nach Ferien** → kein Druck, während der Ferien live zu sein.

---

## 8. Was als Nächstes entschieden werden muss

1. **PIA-Scope:** alle 5 Tage mit Generierung — oder Kern Tag 1+2 (Bio+Hooks) + leichtere Tage 3-5? *(Empfehlung: Kern 1+2 fix bauen, 3-5 als Stretch)*
2. **Cart-Länge:** tight (Fr 3.7. → So 6.7., 3 Tage Flash) oder länger (bis ~13.7.)?
3. **Challenge-Name:** „Mama-Business-Challenge"? „5 Tage zum roten Faden"? (mit PIA als Aufhänger)
4. **Go für den Build?** → dann starte ich mit Bot-Grundgerüst + Anmeldeseite.

---

## 🔗 Verwandte Notizen
- [[challenge-vs-webinar-entscheidung]]
- [[../../../reference/aria-tool-mentee-konzept|PIA-Konzept]]
- [[../mama-ceo/08-funnel/webinar-mails/99-AC-SETUP-MBA|Webinar-Cart-Mails (recycelbar)]]
