---
tags: [content, launch, intern]
---

# 🚀 Launch-Modus für Content-Skills

**Single Source of Truth dafür, wie alle Content-Skills sich während eines Launches an Julia Trosts Launchplan ausrichten — und wie Feed, Story und Mail zusammenspielen.**

Pflicht-Check zu Session-Start in: `/freitag-hooks`, `/montag`, `/karussell`, `/reels`, `/story`.

---

## 1. Läuft gerade ein Launch?

Lies `context/active-funnels.json`. Ein Launch ist aktiv, wenn ein Funnel ein `launch_window` hat, dessen Zeitraum (von `aufwaerm_start_datum`/`aufwaerm_start` bis `cart_close_datum`) das **heutige Datum** umschliesst — oder sein `phase_marker` in einer Launch-Phase steht.

- **Aktuell aktiv:** MBA-Launch (Funnel-ID `mba`) · Aufwärmen ab 12.6. · Webinar Mi 24.6. · Cart 24.6.–5.7.2026 · Launch-Fenster **12.6.–6.7.2026**.
- **Vor der Aufwärmphase** eines anstehenden Launches (heute < `aufwaerm_start_datum`) → noch **KEIN Produkt-/Webinar-/Anmelde-Push** in Content oder Stories, auch wenn der Wochenfokus den Launch schon nennt. Nur Reichweite + echte Verbindung, weicher Engagement-CTA. Der Teaser/Verkauf beginnt erst MIT der Aufwärmphase (Sneak-Peak-Tag). Beispiel: MBA-Aufwärmphase startet 12.6. → am 8.–11.6. noch reine Reichweite, kein MBA/Webinar.
- **Kein Launch aktiv** → normale Wochenlogik (Monatsplan + 5-Typen-Formel + Reichweiten-Mix). Diese Datei ist dann nicht relevant.

---

## 2. Was im Launch-Modus IMMER gelesen wird (= Julia-Trost-Launchplan)

1. **Launch-Kalender** des aktiven Launches — Tag-für-Tag-Phasen (Aufwärmen → Pre-Launch/Secret-Offer → Webinar → Cart-Open → Pioneer-Ende → Final → Cart-Close). Aktuell: `outputs/produkte/mba-launch/launch-kalender-juli-2026.md`.
2. **Story-Drehbuch** des Launches: `outputs/produkte/[slug]/story-plan.json` + `story-plan-tag-fuer-tag.md`. Aktuell unter `outputs/produkte/mba-launch/`.
3. **Julia-Launch-Story-Bausteine:** `context/julia-launch-story-bausteine.md` (Struktur 1:1, Stimme = Patricia).
4. **Julia-Launch-Käufertypen:** `context/julia-launch-kaeufertypen.md`.
5. **Julia-Launch-Methode (intern, Struktur-Quelle):** `reference/julia-trost/9. Launchen.pdf` + `reference/julia-trost/Transkripte Videocalls/_sortiert/Launchen/` (Pre-Launch-Phase · Launch-Phase · „Vorlagen Story LML"). **Niemals „Julia" namentlich im Kunden-Output.**
6. **Launch-Monatsplan** (Content-Skelett): `outputs/content-monat/[YYYY-MM].md`.

→ Die aktuelle **Launch-Phase aus dem Kalender** bestimmt die emotionale Tonalität der Woche (Aufwärmen ruhig → Webinar-Hype → Live-Energie → Endspurt-Dankbarkeit). Sie bestimmt **nicht**, ob im Feed verkauft wird (siehe Punkt 3).

---

## 3. Rollenverteilung Feed ↔ Story ↔ Mail (PFLICHT)

- **Feed (Reels · Karussells · Posts) = programm-frei.** Reichweite + Emotion + Mehrwert + Pull zum **kostenlosen Webinar/Replay** UND **zur Story**. NIE Programme/Kursnamen/Preise/Cart im Feed — auch nicht im Launch (siehe Memory `feedback_keine-programme-im-feed`). Launch-CTAs im Feed = „kostenloses Webinar / Link in Bio" oder „mehr in meinen Stories", NIE „kauf / Cart / Preis / Pioneer".
- **Story = Verkaufsmotor.** Trägt nach Julia-Drehbuch (`story-plan.json` hat Vorrang) den Pitch, Preis (z.B. 83/Monat, Raten), Cart, Secret Offer, Countdown, Social Proof, Käufertyp-Rotation. Details: `.claude/commands/story.md` → MBA-LAUNCH-MODUS.
- **Mail = Funnel-Strecke** (Webinar-Einladung → Confirmation → Sales → No-Show). Aktuell gebaut: `outputs/produkte/mba-launch/webinar-mails/` (AC #596–#609).

### Feed ↔ Story Interlock (der entscheidende Punkt)
Wenn ein Feed-Post „mehr in meinen Stories" verspricht, MUSS die Story dieses Tages das Versprochene liefern.
- Beim Bau eines Feed-Posts mit Story-Verweis (in `/freitag-hooks`, `/montag`, `/karussell`, `/reels`): den `story-plan.json`-Eintrag **desselben Tages** gegenchecken — passt der Story-Verweis zu dem, was die Story an dem Tag tut?
- Im `/story`-Build: wissen, dass der Feed an diesem Tag auf die Story zieht → die Story muss den Verkauf/CTA tatsächlich tragen.

---

## 4. Was jeder Skill im Launch konkret tut

| Skill | Im Launch-Modus |
|---|---|
| **/freitag-hooks** | Hooks der Launch-Woche emotional auf die Launch-Phase (Kalender) ausrichten · **programm-frei** · Feed-CTA = Webinar/Replay/Story-Pull (kein Cart/Preis-Pitch im Feed) · ≥2 Reichweiten-Posts bleibt, ausser der Kalender sagt explizit anders |
| **/montag** · **/karussell** · **/reels** | Beim Bau die Launch-Phase + den programm-freien Feed-Rahmen anwenden · Story-Verweis-CTAs gegen `story-plan.json` gegenchecken (Interlock) |
| **/story** | Eigener Launch-Modus, `story-plan.json` hat Vorrang (siehe story.md). **Hier liegt der Verkauf.** |

---

## 🔗 Verwandte Notizen
- [[julia-launch-story-bausteine]]
- [[julia-launch-kaeufertypen]]
- [[reichweiten-formel-mama-identity]]
- [[content-formel-5-typen]]
