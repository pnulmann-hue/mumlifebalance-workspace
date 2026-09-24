---
tags: [produkt, pia, idee, intern]
---

# Die Rollen-Hierarchie — geparkte Idee für PIA

**Notiert:** 2026-09-24 · **Herkunft:** Werbeanzeige, die Patricia auf dem Handy
mitgeschnitten hat (Bildschirmaufnahme vom 24.09.). Darin zeigt jemand ein
ausgebautes Dashboard, in dem **mehrere KI-Assistenten untereinander** stehen und
**oben ein „Master"** sitzt, der alle Befehle abruft.

**Patricias Satz dazu:**
> „was mir schon noch gefallen hat, dass sie ihre assistenten untereinander
> platziert hat und oben ihren Master hat der alle befehle abruft. aber das wäre
> bei uns ja eher was für pia"

---

## Warum das NICHT ins Cockpit gehört

Im Cockpit wäre es eine **zweite Bedienoberfläche für etwas, das es schon gibt.**
Patricias Assistenten sind die Skills — `/content`, `/reels`, `/karussell`,
`/story`, `/hormozi`, `/funnel`. Der „Master", der sie abruft, ist Claude Code
selbst: sie tippt `/content woche` und der Skill holt sich, was er braucht.

Eine Kachelwand im Cockpit würde daraus eine Liste von Knöpfen machen, die
dasselbe tun wie das Tippen — nur mit einem zusätzlichen Ort, an dem etwas
veralten kann. 🚨 **Das ist derselbe Fehler wie beim Tagesplan** (gestrichen
19.09.): zwei Ansichten auf dieselbe Sache laufen beim nächsten Umbau
auseinander, und man sucht jedes Mal, in welcher man gerade steht.

Dazu kommt: **im Cockpit ist der Engpass nicht die Bedienung, sondern die
Freigabe.** Am 16.09. lagen 27 fertige Beiträge da und keiner war frei.
Eine hübschere Befehlsleiste hätte daran nichts geändert.

---

## Warum es für PIA etwas taugt

Bei PIA ist die Lage umgekehrt. Die Mentee hat **keine Skills, keinen
`/`-Befehl und kein Gedächtnis über Sessions hinweg.** Sie sieht heute einen
Telegram-Chat, in dem sie `/bio`, `/hooks`, `/struktur`, `/leadmagnet` und
`/roterfaden` tippen kann — fünf Befehle, die sie sich merken muss, ohne zu
sehen, wie sie zusammenhängen.

Genau da ist die Bildidee stark: **die fünf Module untereinander als Kette, und
darüber die eine Stelle, die weiss, wo die Mentee gerade steht.**

| Ebene | Was sie tut |
|---|---|
| **oben: PIA selbst** | kennt das Mentee-Profil, weiss welcher Baustein fertig ist, schlägt den nächsten vor — statt fünf gleichberechtigter Befehle |
| **darunter: die Bausteine** | Bio · Hooks · Struktur · Leadmagnet · Roter Faden, jeder mit Zustand: offen · in Arbeit · fertig |
| **daneben: die Bibliothek** | was dabei herausgekommen ist (`mentee_library`), sichtbar wachsend |

**Der eigentliche Gewinn ist nicht die Optik, sondern der Zustand.** Ein Baustein,
dem man ansieht, dass er noch offen ist, wird angefangen. Ein Befehl in einer
Hilfe-Liste nicht.

---

## Was noch zu klären ist, bevor jemand das baut

1. **Wo lebt die Ansicht?** PIA ist heute ein Telegram-Bot (`scripts/pia-bot/`).
   Eine Kette mit Zuständen braucht eine Oberfläche — die geplante Next.js-App
   (siehe [[00-pia-architektur]], Abschnitt 2) wäre der Ort, Telegram nicht.
2. **Wer setzt „fertig"?** Am sinnvollsten die Mentee selbst, sonst steht ein
   Baustein auf fertig, mit dem sie nicht zufrieden war. 🚨 Ein automatisch
   gesetzter Zustand, den niemand bestätigt hat, ist derselbe stille Fehler wie
   eine Freigabe, die „abgelegt" meldet und nichts tut.
3. **Reihenfolge fest oder frei?** Bio vor Hooks ist inhaltlich richtig, aber
   eine gesperrte Kette bestraft die, die schon eine Bio hat. Vorschlagen ja,
   sperren nein.

**Nicht gebaut, bewusst.** Das steht hier, damit es beim nächsten PIA-Ausbau
auf dem Tisch liegt und nicht neu erfunden werden muss.

---

## 🔗 Verwandte Notizen

- [[00-pia-architektur]]
