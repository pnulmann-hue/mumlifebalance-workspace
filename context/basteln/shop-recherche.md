---
tags: [basteln, recherche, tools]
---

# Shop- & Ideen-Recherche — was geht, was nicht

**Getestet am 2026-08-18.** Hier steht, wie ich zu einem Stempelset die Hersteller-Ideen dazuhole — und wo die Grenzen sind.

---

## ✅ Scrapbook Forever — funktioniert vollautomatisch

**Shop:** `scrapbookforever-shop.de` (epages) · Schweiz-Versand nur über Händler wie [bigtime.ch](https://bigtime.ch/de/181_scrapbook-forever) oder [Lilly-Art](https://www.lilly-art.ch)

**Der Schlüssel: die Artikelnummer** (`SF363`, `SF370` …) — steht auf der Set-Verpackung.

### Was ich pro Set bekomme
| Daten | Beispiel SF363 |
|---|---|
| Set-Name | SF Stamps Happy Birthday |
| Preis + Altpreis | 7,50 € (statt 15,50 €) |
| **Exakter Inhalt mit Massen** | „A6, 1 Textstempel (7,5 × 1,0 cm) + 7 Motivstempel (1,5 × 1,5 bis 6,5 × 9,5 cm)" |
| **Beispielkarten des Design-Teams** | 12 Bilder |

→ **Die Beispielkarten sind die Bastelideen, die du meinst.** Ich kann sie herunterladen, *ansehen* und die Technik beschreiben.

### Nutzung
```bash
node scripts/basteln/sf-lookup.mjs SF363
```
```bash
node scripts/basteln/sf-lookup.mjs SF363 SF370 SF353 --bilder
```
- ohne `--bilder`: Markdown-Block mit Bild-URLs
- mit `--bilder`: lädt die Beispielkarten nach `context/persoenlich/basteln-shopbilder/<SF-Nr>/` — **gitignored**, dann kann ich sie lesen und die Techniken ins Inventar schreiben

**Kategorien im Shop:** SF Stamps A6 (150 Sets!) · A7 · A8 · Lavinia · Der kleine Yogi · Stencil · Stanzen · Farben · Stifte · Papier und Folien

---

## 🟡 Mundart Stempel — geht, aber ohne Automatik

**Shop:** [mundartstempel.ch](https://www.mundartstempel.ch/de/) (Gambio) — Schweizer Laden, geführt von zwei Schwestern

- **URL-Muster:** `mundartstempel.ch/de/<ID>.html` (z.B. `/de/28445.html` = Holzstempel Möwe Broder)
- **Kein Artikelnummern-System wie bei SF** → ich kann nicht von der Verpackung auf die URL schliessen
- **Aber:** der Shop hat eine eigene Kategorie **„Anleitungen"** — dort liegen ihre Bastelideen
- **Weg:** du schickst mir ein Foto → ich suche im Shop nach dem Namen → hole Beschreibung + Bilder

→ Kein Skript, weil das Nummern-Mapping fehlt. Bei Bedarf baue ich einen Suchwort-Lookup.

---

## ❌ Facebook-Gruppe „Scrapbook Forever Ideen" — nicht durchsuchbar

**Ehrliche Antwort: nein, das kann ich nicht.** Drei Gründe:

1. **Login-Wall.** Gruppen-Inhalte sind für nicht eingeloggte Zugriffe unsichtbar. Weder mein interner Browser noch `curl` kommen rein.
2. **Keine Chrome-Verbindung.** Es *gäbe* einen Weg — die „Claude in Chrome"-Erweiterung würde deinen eingeloggten Browser nutzen. Geprüft: aktuell **kein Chrome verbunden**.
3. **Selbst mit Zugang würde ich es nicht massenhaft tun.** Automatisiertes Abgrasen einer Gruppe verstösst gegen Facebooks Regeln, und die Posts gehören anderen Bastlerinnen — deren Fotos landen nicht in deinem Archiv, schon gar nicht in einem öffentlichen Repo.

### Was stattdessen funktioniert — und zwar sofort

**Screenshot-Weg (empfohlen):**
1. Du siehst in der Gruppe eine Idee, die dich packt → Screenshot
2. Ab in einen Ordner (z.B. OneDrive `Basteln/Ideen-FB/`) oder direkt an mich
3. Ich lese das Bild aus, beschreibe die Technik, prüfe gegen dein Inventar und trage's in [[projekt-ideen]] ein

Das ist nicht mal umständlicher — du musst die Idee ja sowieso erst gut finden. Und **ich beschreibe die Technik in Worten**, statt fremde Fotos zu sammeln: „Aquarell-Hintergrund, Motiv gestanzt, mit Foam-Pads erhöht" ist für dich beim Nachbauen brauchbarer als das Bild allein.

**Facebooks „Gespeicherte Beiträge"** als Sammelstelle nutzen und wir gehen sie gemeinsam durch, wenn du Zeit hast.

---

## ⚖️ Urheberrecht — meine Regel

| Was | Wohin |
|---|---|
| Shop-Beschreibungen, Set-Inhalte, Masse | ✅ ins Inventar (Fakten) |
| Links zu Hersteller-Seiten | ✅ ins Inventar |
| **Meine** Beschreibung einer Technik | ✅ ins Inventar |
| Fremde Produktfotos & Beispielkarten | 🔒 nur `context/persoenlich/` (gitignored) |
| Posts anderer Bastlerinnen 1:1 | ❌ gar nicht |

**Warum so streng:** Dieses Repo ist öffentlich. Fremde Bastelfotos darin wären ein echtes Problem — und zwar deins, nicht meins.

---

## 🔗 Verwandte Notizen
- [[inventar-physisch]] — hier landen die erfassten Sets
- [[projekt-ideen]] — hier landen die ausgewerteten Ideen
- [[README]]
