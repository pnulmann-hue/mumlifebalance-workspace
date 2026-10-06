---
tags: [produkt, salespage, funnel]
---

# ThriveCart-Funnel KI-Kurs — Stand 06.10.2026

Eingerichtet über die ThriveCart-Oberfläche (die API ist **read-only**, jeder
Schreibversuch antwortet mit `method.invalid`).

---

## Was steht

### Produkt 52 · Easy KI für Networkerinnen · CHF 277 · `/ki-network/`

```
Cart page
  ↑ Upsell 11   Mum Business Academy – nach Easy KI (720)
      ↓ Downsell 4   Mum Business Academy – 6 Raten (nach Easy KI)
Success page
```

| | Upsell 11 | Downsell 4 |
|---|---|---|
| Preis | 720 einmalig | 6 × 120 = 720 |
| Liste | `Kunden` | `Kunden` |
| Tag | `mba-kauf` | `mba-kauf` |
| Kurs | None — die Academy läuft über ActiveCampaign | None |
| Erscheint | nach dem Kauf | nur wenn der Upsell abgelehnt wurde |

**Die Rechnung dahinter:** Die Academy kostet im Webinar 997. Wer vorher 277 für
den KI-Kurs bezahlt hat, zahlt 720 — zusammen genau 997. Damit ist das
Anrechnungs-Versprechen eingelöst, ohne dass etwas von Hand verrechnet wird.

### Produkt 48 · MBA webinar · CHF 997

Die **Instagram-Kundenmaschine ist als Upsell entfernt**. Sie ist Teil der
Academy — wer 997 bezahlt hatte, bekam sie zwei Sekunden später für 97
angeboten. Das lief live, seit wann ist unklar.

Geblieben: „Finde dein Thema" (25). Der ist kein Academy-Inhalt und darf dort
stehen.

---

## Offen

**Der Bump am KI-Kurs.** Zweimal angelegt (Finde dein Thema, CHF 25, nicht
vorangekreuzt), beide Male nach dem Speichern verschwunden. Vermutlich
unterbricht der Hinweis „This product does not have sales tax enabled" den
Speichervorgang.

🚨 **Folge:** „Finde dein Thema" hängt aktuell **nirgends** mehr am KI-Kurs. Als
Upsell wurde er entfernt, weil er Bump werden sollte.

**Die Texte** auf Upsell- und Downsell-Seite. Beide stehen noch auf der
ThriveCart-Vorlage („Neque Quaerat… Only $297… 40% OFF"). Fertige Texte unten.

---

## Die Texte

### Upsell-Seite

> Warte — eine Sache noch, und die gibt es nur hier.
>
> Du hast gerade gelernt, wie du deiner KI beibringst, wer du bist. Was ihr jetzt
> noch fehlt, ist der Inhalt. Genau der steckt in der Mum Business Academy.
>
> Instagram-Kundenmaschine: wie ein Beitrag aufgebaut sein muss, wie gute Hooks
> entstehen, wie aus einem Profil ein Angebot wird.
>
> Digitale Produktwelt: vom ersten Freebie über die Produkttreppe bis zum
> Verkauf. Der ganze Mechanismus.
>
> Mama-CEO: wie dein Business in deinen Alltag passt, mit vier Kindern und allem,
> was sonst noch ist.
>
> Dazu ein Jahr Begleitung in der Gruppe, jeden Monat ein Call mit mir und jeden
> Monat einer mit einer Expertin — KI, Finanzen als Frau und Mama, und was Mamas
> im Business sonst beschäftigt.
>
> Das ist die Komplettlösung: die Maschine hast du gerade gekauft, hier kommt
> alles dazu, was sie braucht.
>
> Vier Kurse zu 333 sind 1332. Die Academy kostet 997. Deine 277 von eben ziehe
> ich ab — du zahlst 720.

🔘 JA, ICH WILL ALLES · Nein danke, ich bleibe beim Kurs

### Downsell-Seite

> Dann lass mich dir sagen, warum ich dich nochmal frage.
>
> Ich bin von dem, was in der Academy steckt, so überzeugt, dass ich glaube: Jede
> Networkerin kann sich damit ein Business aufbauen, das wirklich rentiert. Nicht
> irgendwann. Mit dem, was da drin steht.
>
> Deshalb habe ich mir überlegt, wie ich es dir leichter machen kann. Und die
> Antwort war: in Raten.
>
> Sechs Monate, jeden Monat 120 Franken.
>
> Das sind zusammen genau dieselben 720. Keinen Franken mehr. Nur eben nicht
> alles auf einmal.

🔘 JA, SO MACHE ICH ES · Nein danke, ich bleibe beim Kurs

---

## 🚨 Befunde, die beim Einrichten herauskamen

**ActiveCampaign war abgehängt.** ThriveCart bekam auf `/api/3/tags` ein
**403 Forbidden** — der Schlüssel wurde am 13.09.2026 gewechselt, ThriveCart
hatte noch den alten. Die Integrations-Seite zeigte trotzdem „Connected":
**das heisst nur, dass Zugangsdaten hinterlegt sind, nicht dass sie gültig
sind.** Den echten Zustand sieht man nur, wenn man eine Automationsregel
aufmacht und die Tag-Liste ewig auf „Loading…" steht. Patricia hat den
Schlüssel am 06.10. neu eingetragen.
Kein Schaden entstanden: von 85 Transaktionen liegt keine nach dem 13.09.

**Das Formular übernimmt nur Getipptes.** Ein von aussen gesetzter Wert steht im
Feld, wird beim Speichern aber ignoriert. Der Upsell-Preis stand dadurch
zwischendurch auf **0.00** — ein Upsell, der die Academy verschenkt hätte.
Gefunden hat es die Gegenprobe über die API, nicht die Erfolgsmeldung des
Browsers. **Nach jedem Speichern gegenprüfen.**

**Die API zeigt Ratenpreise nicht an.** Bei Split-pay bleibt `payment_amount`
auf 0, obwohl der Wert gespeichert ist; nur `payment_rebills` kommt durch. Der
verlässliche Test ist ein kompletter Neuladen der Seite — steht der Wert danach
noch im Feld, ist er gespeichert. Ein Alarm darüber war ein Lesefehler, kein
Speicherfehler.

**Aufräumbedarf in den Listen:** drei Kopien der Instagram-Kundenmaschine
(#7, #8, #9), zwei „Untitled upsell" (#4, #6), ein „Untitled downsell" (#1).
Beim Verbinden eines Funnels ist leicht die falsche erwischt.

**Zahlendreher bei Produkt 48:** Die Preis-Option hiess „Ratenzahlung
(2x CHF 489.50)", abgebucht wurden **498.50**. Von Patricia am 06.10. korrigiert.

**Die Academy liegt nicht in ThriveCart Learn.** In der Kursauswahl stehen nur
„Mama.Energise Network Academy" und „Easy Mumlife Academy". Die Auslieferung
läuft über den Tag `mba-kauf` und die Automation in ActiveCampaign — deshalb
steht bei Upsell und Downsell als Kurs `None`.

---

## Die Nachkauf-Strecke — und warum keine neue Maschine gebaut wird

**Automation 85 „KI Kurs"** ist eine Kopie der Startklar-Automation: sie enthält
noch deren sieben Mails (Kampagnen 821–827), steht auf **inaktiv** und hat
`entered=0`. Deshalb ist nie eine Startklar-Mail an eine KI-Käuferin gegangen.

**Mail 0 ist geschrieben:** `scripts/ki-kurs/mails-bauen.py` → Willkommen, der
1. November, die beiden Call-Termine, die Telegram-Gruppe. Das Gerüst wird aus
`scripts/startklar/mails-bauen.py` **importiert**, nicht kopiert.

🚨 **Kein Zugangslink und kein Preis in Mail 0.** Die Rechnung schickt
ThriveCart selbst, den Kursbereich gibt es erst am 1. November. Der einzige
Klick ist die Gruppe — sie überbrückt die bis zu vier Wochen bis zum Start.

🚨 **Der Einladungslink steht in `scripts/ki-kurs/.env`,** und die Ausgabe unter
`outputs/produkte/ki-kurs/mails/` ist gitignored. Ein Einladungslink zu einer
**bezahlten** Gruppe ist funktional ein Zugangsschlüssel; das Repo ist public.

### Die Engine gibt es schon — falsch ist nur der Einstieg

Die Frage war, ob eine neue Serie gebaut werden soll, in der alle
Signature-Käuferinnen laufen, bis sie die MBA oder einen anderen Kurs kaufen.
**Genau das ist Automation 72 → Loop 2…7**, alle aktiv:

| Loop | Automation | pitcht | Ausstiegs-Goals |
|---|---|---|---|
| 1 | 72 „Automation 0€ Produkt" | Finde dein Thema **39** | MBA gekauft · Thema gekauft |
| 2 | 75 | Webinar → **MBA** | MBA gekauft |
| 3 | 73 | Expertin **97** | hat sie schon · MBA gekauft |
| 4 | 76 | Digitale Produktwelt **333** | hat sie schon · MBA gekauft |
| 5 | 77 | Mama-CEO **333** | hat sie schon · MBA gekauft |
| 6 | 78 | Instagram-Kundenmaschine **333** | hat sie schon · MBA gekauft |
| 7 | 79 | MBA Re-Pitch **997** | MBA gekauft |

Jeder Loop überspringt sich selbst, wenn das Produkt schon da ist, und endet
beim MBA. Eine zweite Serie daneben wäre dieselbe Maschine doppelt — und zwei
Serien, die beide pitchen, laufen beim nächsten Umbau auseinander.

🚨 **Tag 87 „Automation 0€ Produkt" führt in Loop 1 — und Loop 1 verkauft
„Finde dein Thema" für 39 an jemanden, der gerade 277 bezahlt hat.** Das ist
derselbe Abstiegs-Fehler, der bei der Startklar-Strecke schon einmal vermieden
wurde. Für Signature-Käuferinnen ist der richtige Einstieg **Loop 2** (der
MBA-Pitch über das Webinar), mit Abstand nach dem zweiten Call.

⚠️ **Ungeprüft:** worauf die Goals „MBA gekauft" genau schauen. Die v3-API gibt
Segment-Bedingungen nicht heraus (404 auf `segments/<id>/conditions`). Es gibt
den Tag **79 `mba-kauf`**, und genau den setzen der neue Upsell und Downsell —
das muss aber **im Browser** gegengeprüft werden, bevor die Strecke scharf
geht. Sonst bekommt eine Kundin, die den MBA gerade im Upsell gekauft hat,
Wochen später die MBA-Pitch-Serie.

---

## 🔗 Verwandte Notizen

- [[ki-kurs-checkout-texte]]
- [[textbloecke]]
