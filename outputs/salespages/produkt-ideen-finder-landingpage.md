---
tags: [produkt, salespage]
---

# Landingpage — Produkt-Ideen-Finder (0€-Tool · Opt-in)

> Schlanke Freebie-Opt-in-Page (analog Freischaufeln), nicht die lange Verkaufsseite. Voice: Patricia (Küchentisch, ss, kein Stakkato, network-positiv, keine verbotenen Wörter, keine erfundenen Zahlen). Quelle: [[02-marktrecherche-salespage-vorrat]] · [[00-spec]]. Ziel: E-Mail-Opt-in → Tool → 39er.

---

## BLOCK 1 — Hero
**H1:** Neugierig, womit du neben deinem Network schneller was verdienen könntest?

**Subline:** In 5 Minuten zeigt dir mein kostenloser Produkt-Ideen-Finder, welches eigene kleine Produkt wirklich zu dir und deinem Network passt — ganz ohne dass du dafür fremde Leute anschreiben musst.

🔘 **Jetzt starten — kostenlos**

---

## BLOCK 2 — Pain (Kennst du das?)
Du bist im Network, weil du ans Produkt glaubst und dir ein Stück Freiheit aufbauen willst — nur geht das Ganze quälend langsam, Rang für Rang, und am Monatsende rechnest du heimlich nach, ob wirklich mehr reinkommt, als du reinsteckst.

Und dann ist da noch dieser Teil, den eigentlich keine mag: das ständige Anschreiben, die halben Bekannten mit „Heyy, wie geht's dir?", die Partys, bei denen drei aus Höflichkeit zusagen und am Ende doch nichts hängen bleibt. Irgendwann sagst du lieber gar nicht mehr, was du eigentlich machst.

---

## BLOCK 3 — Der leisere Weg
Network ist ein Marathon, und das ist völlig okay. Aber wer früher etwas Eigenes in der Hand haben will, baut sich neben dem Network ein kleines eigenes Produkt auf — eins, das DIR gehört und in das dein Network-Produkt einfach als ein Teil der Lösung reinfliesst.

Du gibst dabei nichts auf, du stellst nur ein zweites Standbein daneben. Und das Verrückte ist: Genau dafür steckt in dir längst eine Idee — du siehst sie nur noch nicht.

---

## BLOCK 4 — Was der Produkt-Ideen-Finder für dich macht
- Er kitzelt aus dir heraus, was du eigentlich schon alles kannst — auch wenn du gerade denkst, du hast „nichts Besonderes".
- Er gibt dir 1–3 konkrete Ideen für dein eigenes kleines Produkt, mit deinem Network-Produkt clever eingebaut.
- Und er zeigt dir den einen ersten Schritt, den du sofort gehen kannst.

---

## BLOCK 5 — So funktioniert's
1. Du beantwortest ein paar einfache Fragen — dauert keine 5 Minuten.
2. Der Finder verwandelt deine Antworten in deine ganz persönliche Produktidee.
3. Du bekommst dein Ergebnis und deinen nächsten Schritt direkt zugeschickt.

---

## BLOCK 6 — Über mich
Ich bin Patricia, vierfache Mama aus der Schweiz — und ich weiss genau, wie sich das anfühlt.

Von 2018 bis Ende 2022 war ich selbst im Network. Nur: Auf Instagram hat mein Produkt niemanden interessiert, und die Menschen, die mich kannten, waren längst schon meine Kundinnen. Ich hab viel zu viel Arbeit gegen viel zu wenig Verdienst getauscht — und irgendwann hingeschmissen. Damit gehörte ich zur grossen Mehrheit, denn fast alle, die je mit Network anfangen, hören irgendwann wieder auf.

2023 hab ich mich trotzdem entschieden, nochmal ein Business zu starten. Aber nicht nach dem Motto „dann verkauf ich halt ein anderes Network-Produkt", sondern auf der Grundlage von genau den Fragen, die dir mein Ideen-Finder gleich stellt. Mein Network-Produkt ist erst später einfach dazugekommen, und es war nie mein Hauptfokus.

Und weisst du, was das Verrückte ist? Genau dadurch hat sich mein Network sogar weiterentwickelt — heute hab ich ein eigenes Team und verdiene dort regelmässig. Aber eben nicht nur dort. Und genau das macht mich ein Stück weit unabhängiger.

---

## BLOCK 7 — Finaler CTA
**H2:** Bereit für deine Idee?

Schau einfach mal, was rauskommt — kostenlos, unverbindlich, in 5 Minuten. Vielleicht hältst du gleich den Anfang von etwas in der Hand, das nicht nur dein Instagram, sondern dein ganzes Business verändert.

🔘 **Meinen Produkt-Ideen-Finder starten**

---

## Deploy-Hinweise
- WordPress-Seite (Draft) via `/wp`, Brand: Creme #f1ecdd + Philosopher (Headings) + Source Sans 3 (Body) + Petrol-Akzent (Buttons). Inline-Styles (WAF blockt `<style>`-dichte POSTs — [[reference_wordpress-waf-lp-deploy]]).
- Opt-in: E-Mail → ActiveCampaign (neue Liste + Tag `produkt-ideen-finder-lead`) → „Jetzt starten" führt zum Tool.
- Slug-Vorschlag: `mumlifebalance.ch/produkt-ideen-finder`.
- ⚠️ Tool selbst (Vercel-KI-App) muss noch gebaut werden — bis dahin CTA-Link = Platzhalter.

## 🔗 Verwandte Notizen
- [[00-spec]] · [[01-kommunikation-aga-leitfaden]] · [[02-marktrecherche-salespage-vorrat]]
