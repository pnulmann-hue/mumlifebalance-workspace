---
tags: [produkt]
---

# 07 · Stichwort-Automation NISCHE

Werte aus `00-bauplan.md`. Patricia 29.10.: Die Stichwort-Nachricht soll nicht mehr über ManyChat laufen.

## Der Ablauf

Kommentar **NISCHE** unter Reel oder Beitrag → Antwort im Kommentar → DM mit dem Nischengenerator → nach dem Ergebnis der Knopf zum Tool-Workshop.

**Antwort im Kommentar** (öffentlich, kurz):
> Schau in deine Nachrichten 💛

**Direktnachricht:**
> Hallo du! Hier ist dein Nischengenerator: https://mumlifebalance.ch/nischengenerator/
>
> Ein paar Fragen zu deiner Erfahrung und zu dem, was man dich immer wieder fragt. Danach hast du drei Themen mit deinem Experten-Satz und Ideen für dein erstes Gratis-Tool.
>
> Und wenn du das Tool gleich mit mir bauen willst: Am 10. und 11. November, jeweils um 19:00 Uhr, mache ich den Tool-Workshop, live, für 39 Franken oder 39 Euro: https://mumlifebalance.ch/tool-workshop/

## Wer die Nachricht schickt — drei Wege

| Weg | Stand | Was es braucht |
|---|---|---|
| **1 · Von Hand** | sofort möglich | DM-Text oben als Textbaustein in Instagram speichern (Einstellungen → Geschäftstools → Gespeicherte Antworten, Kürzel z. B. `/nische`). Bei rund 2'000 Followern gut machbar und persönlicher. |
| **2 · Eigener Dienst `kommentar-antwort`** | läuft, aber nur im Protokoll-Modus (`SCHARF` nicht gesetzt), Regeln nur für STIMME | Ohne **Meta-App-Review** antwortet er nur Konten mit App-Rolle, also keinen Fremden. Für NISCHE: Regel in `lib/entscheiden.mjs` ergänzen, Antworttext hinterlegen, App-Review bei Meta beantragen. Dauert erfahrungsgemäss Tage bis Wochen, für diesen Launch zu knapp. |
| **3 · ManyChat** | läuft | Patricia will weg davon. Bliebe die schnellste Brücke, falls es mehr als ein paar Dutzend Kommentare werden. |

**Empfehlung 🟠 ENTSCHEID:** Für diesen Launch Weg 1 (von Hand, mit gespeicherter Antwort). Parallel den App-Review für Weg 2 beantragen, damit der eigene Dienst beim nächsten Launch übernimmt.

**Seit 29.10. abends:** Der Link in der Antwort auf NISCHE ist die Anmeldeseite https://mumlifebalance.ch/nischengenerator/ (nicht das Tool direkt), damit sich jede über das Formular mit Bestätigung einträgt.
