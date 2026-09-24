---
tags: [content, karussell, mentoring]
---

# Warum dir vor allem Leute aus deinem eigenen Network folgen

**Profil:** Mentoring · **Typ:** `edukativ` · **Funnel:** MOF · **Job-Säule:** A Autorität + D Sales
**Keyword:** `BIO` · **Cover:** Dunkelblau (Template) · **Folien:** 10
**Kern:** Patricias Gedanke vom 22.09.2026 — Kommentare aus dem eigenen Network sind kein Umsatz.
**Renders:** `renders/2026-09-22-network-folgt-dir-nur-dein-network/01.png` … `10.png`

## Die zehn Folien

| # | Inhalt |
|---|---|
| 1 | Cover · „Drei Jahre stand in meiner Bio der Firmenname" (Bekenntnis) |
| 2 | Kommentare hattest du trotzdem — schau nach, von wem |
| 3 | Fast alle davon sind im selben Network · gutes Gefühl ≠ Umsatz |
| 4 | Geld verdienst du bei denen, die das Produkt noch nicht haben |
| 5 | Das Beispiel · Lieblingshose kneift, Bikini zuunterst in der Schublade |
| 6 | Warum soll sie bei dir kaufen? Du erzählst dasselbe wie alle |
| 7 | Bio vorher · „Beraterin bei [Firma]" |
| 8 | Bio nachher · „Für Mamas ab 35, die ihre Bikinifigur zurückwollen" |
| 9 | Die Bio allein macht es nicht · Beiträge · Story · Highlights · Link |
| 10 | CTA · Kommentier BIO |

🚨 **Folie 9 kam auf Patricias Einwand dazu:** Ein Karussell, das nur die Bio behandelt,
verfehlt, was sie im Kurs lehrt — das Zusammenspiel aus Beiträgen, Story, Highlights und
Link. Ton bewusst ohne Vorwurf („die Bio allein macht es nicht" statt „du verstehst
Instagram nicht").

🚨 **„Fast alle" statt „95 %":** Patricia hat 95 % gesagt, es ist aber eine Einschätzung
und keine Messung. Nach der Regel gegen erfundene Zahlen steht dort eine Formulierung
ohne Pseudo-Präzision. Falls sie die Zahl belegen kann, darf sie zurück.

## Caption

Schau dir mal an, wer unter deinen letzten Beiträgen kommentiert hat.

Wenn es dir geht wie mir früher, dann sind das fast alles Frauen aus deinem eigenen Network. Die haben das Produkt längst. Die kaufen es nicht bei dir, die verkaufen es selbst.

Es fühlt sich trotzdem gut an, weil überhaupt etwas zurückkommt. Nur verdienst du damit nichts.

Geld verdienst du bei den anderen: bei Menschen, die dein Produkt noch nicht haben und ein Problem, das du für sie lösen kannst. Die Mama, deren Lieblingshose seit den Kindern kneift und deren Bikini zuunterst in der Schublade liegt. Die sucht keine Beraterin. Die sucht jemanden, der ihr Problem kennt.

Und die findet dich nur, wenn auf deinem Profil ihr Problem steht statt deiner Firma.

Im Karussell siehst du beide Varianten nebeneinander.

Kommentier **BIO**, dann schaut mein Bio-Check sich deine an und sagt dir, was schon greift und was noch nach Beraterin klingt.

**BIO** ⬇️

Hi, ich bin Patricia, Mama von vier Kindern. 2023 hab ich mein Network im Hybridmodell aufgebaut. Bei mir lernst du, wie du mit deinem Thema auf Insta sichtbar wirst, wie du digitale Produkte passend zum Network entwickelst, und wie du das Ganze in deinen Mama-Alltag packst.

#mamabusiness #mamaimnetworkmarketing #onlinebusinessmama #expertenbusiness #mumpreneur

## 🚨 Sicherheitsrand 10 % (gemessen 22.09.2026)

Instagram zeigt 4:5 im **Feed vollständig**. Im **Profil-Raster** fallen seitlich 3,1 %
weg, bei einem **1:1-Zuschnitt** oben und unten je **135 px = 10 %**.

Deshalb hat jede Folie oben und unten **150 px Rand**, das Cover 160/150. Damit bleibt
auch bei 1:1 alles sichtbar. Gilt für jedes weitere Karussell — der Wert steckt in
`scripts/karussell-render/folien.mjs`.

## Neu erzeugen

```
node scripts/karussell-render/folien.mjs \
  outputs/karussells/renders/2026-09-22-network-folgt-dir-nur-dein-network/folien.json \
  outputs/karussells/renders/2026-09-22-network-folgt-dir-nur-dein-network
```

## 🚨 Der Freigabe-Knopf rendert die Folien NEU (gefunden 22.09.2026)

Im Cockpit liegt dieses Karussell als **Text** (`slides` mit `headline`/`body`/`layout`).
Der Knopf „Für Blotato freigeben" ruft `slideJpeg()` und **zeichnet jede Folie aus diesen
Texten neu** — Screenshots, Bio-Karten und Markierungen aus den PNGs hier sind dabei weg.

**Deshalb:** Texte im Cockpit prüfen und freigeben, aber die **Bilder kommen aus
`renders/`**. Nach der Text-Freigabe legt Claude die echten PNGs als
`freigaben/<id>/bilder/slide-NN` ab — denselben Weg hat am 21.09. schon
`kw39-kar-d-di-a` genommen.
