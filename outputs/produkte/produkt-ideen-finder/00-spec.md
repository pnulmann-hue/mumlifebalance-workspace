---
tags: [produkt, funnel, tools]
---

# Produkt-Ideen-Finder — Leadmagnet-Spec (KI-Tool)

**Erstellt:** 2026-09-04 · **Typ:** 0€-Leadmagnet (KI-Web-App) · **Profil:** @mumlifebalance (Mentoring)

## Zweck & Funnel-Rolle
Kostenloses KI-Tool an der Spitze der „digitale Produktwelt"-Treppe. Verwandelt das Rohmaterial einer Network-Mama (ihr Network + was sie gelöst hat + überwundene Situationen + Interessen/Expertise) in **1–3 konkrete eigene Produktideen**, in die ihr Network-Produkt als *Teil der Lösung* eingebaut ist. Liefert den **Aha (die Idee)** — und pitcht den 39er-Kurs zum Umsetzen.

**Treppe:** 🎁 Produkt-Ideen-Finder → 💸 „Vom Network-Wissen zum eigenen Produkt" (39) → 👑 „…zur digitalen Produktwelt" (333) → MBA.

**Anti-Kannibalisierung (wichtig):** Das Gratis-Tool gibt NUR die **Idee**. Das „und so baust & verkaufst du sie" bleibt bewusst im 39er/333er. → Tool macht Lust, ersetzt den Kurs nicht.

**Herkunft:** schlanke Gratis-Version von „Bot 1: Produkt-Ideen-Finder" aus `02-ki-assistenten-konzept.md` (dort war er als Kurs-Bonus mit vollem Kurs-Gerüst gedacht — die Gratis-Version stoppt bewusst bei der Idee).

## Fragen-Flow (der Bot fragt nacheinander)
1. **Dein Network:** In welchem Network bist du — welche Produkte vertreibst du?
2. **Deine Lösung:** Was hast du selbst dank dieser Produkte gelöst oder verändert?
3. **Deine Geschichte:** Welche Schwierigkeiten oder Situationen hast du in deinem Leben überwunden (auch ausserhalb vom Network)?
4. **Deine Expertise:** Was sind deine Interessen und deine berufliche Erfahrung? Wofür fragen dich Leute immer wieder um Rat?
5. **Deine Leute:** Wem hilfst du am liebsten? (Zielgruppe — grob reicht)
6. **Ergebnis holen:** Deine E-Mail, damit ich dir deine Ideen + den ersten Schritt schicke. *(Lead-Capture)*

## Output (was das Tool zurückgibt)
Pro Idee (1–3 Stück):
- **Thema + Arbeitstitel** des eigenen digitalen Produkts
- **Für wen genau** (Zielgruppe)
- **Transformation** (Vorher → Nachher, in Kundensprache)
- **Wie dein Network-Produkt als Teil der Lösung reinkommt** (nie als Pitch, immer als ein Baustein)
- **Dein erster nächster Schritt**

**Abschluss-Slide (Brücke):** „Du hast jetzt deine Idee. Sie zu einem fertigen Produkt zu machen — Format, Aufbau, verkaufen —, das zeig ich dir Schritt für Schritt in meinem Minikurs ‚Vom Network-Wissen zum eigenen Produkt' 👉 [Link]."

## KI-System-Prompt (Kern — zum Bauen)
```
Du bist Patricias Produkt-Ideen-Finder für Network-Marketing-Mamas.
Deine Methode stammt aus ihrem Kurs (3 Quellen einer Produktidee:
Geschichte · Expertise · Community; + die Schlüsselfrage: „Welches
Problem hat mein Mensch, BEVOR er das Network-Produkt überhaupt braucht?").

Ziel: Aus den Antworten der Frau 1–3 konkrete Ideen für ihr EIGENES
digitales Produkt ableiten, in das ihr Network-Produkt als EIN Baustein
der Lösung eingebaut ist — nie als Hauptdarsteller, nie als Pitch.

Regeln:
- Denk in der LÖSUNG/im Thema, nie im Produkt. Die Kundin kauft nie das
  Produkt, sondern die Verwandlung.
- Sei konkret, nie vage. Jede Idee hat: Titel · für wen · Transformation
  (Vorher→Nachher) · wie das Network-Produkt als Teil der Lösung reinkommt
  · erster Schritt.
- Sprache: warm, direkt, Du-Form, Schweizer ss, wie eine gute Freundin.
  Nie „du musst" — lieber „du darfst/kannst".
- KEINE Heil- oder Wirkversprechen zu Gesundheitsprodukten. Produkte als
  Ritual/Unterstützung/Teil der Lösung, nie als Heilmittel.
- Keine erfundenen Zahlen/Studien.
- Gib am Ende NICHT den ganzen Bauplan (kein Inhaltsverzeichnis, keine
  Folien) — nur die Idee + ersten Schritt. Der Bau kommt im bezahlten Kurs.

Stopp nach der Idee + Brücken-Satz zum Minikurs.
```

## Funnel-Wiring
- **Keyword:** `IDEE` (ManyChat, Mentoring) → DM mit Tool-Link. In `manychat-keywords.md` ergänzen.
- **Landing:** WP-Seite `mumlifebalance.ch/produkt-ideen-finder` (via /wp, Bio-Check-Muster).
- **Lead-Capture:** E-Mail → ActiveCampaign (neue Liste + Tag `produkt-ideen-finder-lead`), Nurture-Automation → 39er-Pitch nach 1 Tag.
- **Register:** in `context/active-funnels.json` als neuen Funnel eintragen (profile mentoring, führt zu 39er → 333er → MBA).

## Technik
**Bio-Check-Zwilling** (wie `scripts/bio-check-bot/` + `Freischaufeln`): Vercel-KI-Web-App, Anthropic-API im Backend, AC-Integration fürs Lead-Capture. Als `scripts/produkt-ideen-finder-service/` (o.ä.) neu — oder Bio-Check-Repo klonen/anpassen.

## Content-Timing (September)
- **KW37** wärmt (Thema aus deinem Wissen)
- **KW38** = Tool live + Push (Lead-Post Keyword IDEE → Tool) — Unterthema „Womit anfangen — dein erstes digitales Produkt"
- **KW39** hält warm (verkaufen auch passiv)

## Compliance
Network-neutral (funktioniert für jedes Unternehmen, nicht nur doTERRA). Keine Heilversprechen. Produkt = Teil der Lösung. Freundin-Voice, ss, keine erfundenen Zahlen. Repo public → keine PV/Strategie ins committete File (nur Konzept).

## Nächste Schritte
1. ⬜ Name final (Arbeitstitel „Produkt-Ideen-Finder" — Alternativen sammeln)
2. ⬜ Fragen-Flow + System-Prompt mit Patricia finalisieren
3. ⬜ Test-Dialoge (3 verschiedene Network-Mama-Profile durchspielen)
4. ⬜ Vercel-App bauen (Bio-Check-Zwilling)
5. ⬜ AC-Liste + Tag + Nurture, ManyChat `IDEE`, WP-Landing
6. ⬜ Go-live für KW38

## 🔗 Verwandte Notizen
- [[02-ki-assistenten-konzept]] (Ursprungs-Konzept Bot 1)
- [[reference_kurswissen-digitale-produktwelt-nuggets]]
- [[reference_aga-bieschke-zielgruppenanalyse]]
