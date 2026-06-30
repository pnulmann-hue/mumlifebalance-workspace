---
tags: [produkt, mba, architektur, thrivecart]
---

# MBA — Academy-Architektur auf ThriveAcademy

> Erarbeitet 2026-06-30 (Modus 3 /produkt) nach Analyse von Patricias eigenem Jahres-Setting auf Skool (Elevate).
> **Korrigiert 2026-06-30** nach Recherche: ThriveAcademy (Launch Mai 2026) ist **community-first**, nicht der alte „Learn"-Kurs-Player. Quellen unten.
> Schwester-Datei: [[11-willkommens-modul-und-callplan]] (Onboarding-Skript + Umsetzerinnen-Call-12-Monatsplan).

---

## 0. Was ThriveAcademy ist (Stand Juni 2026)

ThriveAcademy ist seit **Mai 2026** live und ein **community-first LMS** — die Logik ist umgedreht: *„deine Community ist das Produkt, alles andere lebt darin."* Damit ist es ein direkter **Skool-Konkurrent** und kann fast alles, was Patricias Elevate-Setting kann — Kurse, Community-Feed, Q&A, Gamification/Leaderboard — an EINEM Ort.

**Hierarchie:** `Community → Spaces → Courses → Module/Lektionen`

### Die 6 Space-Typen (= Skool-Bereiche)

| Space | Funktion | Skool-Gegenstück (Elevate) |
|---|---|---|
| **Announcements** | nur Admin sendet, Mitglieder reagieren/kommentieren | „News & Updates" |
| **Q&A** | strukturierter Fragen-Austausch, beste Antworten gepinnt | „Euer Austausch" |
| **Course Community** | Diskussion direkt unter jeder Lektion | Skool-Lektions-Kommentare |
| **Resource Hub** | durchsuchbare Vorlagen-/Datei-Bibliothek | Roadmap/Downloads |
| **Quiz Hub** | alle Quizze gesammelt | (hat Elevate nicht) |
| **Lounge** | intimerer Bereich für bestimmte Segmente | engerer Austausch |

Spaces lassen sich in **Space-Kategorien** gruppieren („Gebäude mit Räumen").

### Gamification (= Skool-Leaderboard)
3 Presets: **Light Touch · Engagement Booster · Gamified Mastery** (Punkte, Badges, Leaderboard, Community-Rollen). → für MBA-Pioneer **Engagement Booster** (motiviert ohne Punkte-Zirkus).

### Commerce
Dein **bestehender ThriveCart-Checkout** meldet Käuferinnen **automatisch** in die Community an (Product-to-Access-Mapping). **Space-Unlock-Rules** gating nach: Zahlung · Kurs-Abschluss · Quiz-Score · XP-Level · Tags · Zeit (= Drip).

---

## 1. Zwei harte Fakten, die die Planung steuern

### A) Kosten — neu ein eigenes Abo (nicht mehr „gratis im ThriveCart")
Der alte „Learn" war im ThriveCart-Kauf enthalten. **ThriveAcademy ist ein separates Monatsabo:**

| Plan | Preis (jährlich) | Mitglieder | für MBA relevant |
|---|---|---|---|
| **Starter** | ~37 $/Mt (≈444 $/J) | bis 2'000 | ✅ **reicht für Pioneer + lange danach** |
| Growth | ~67 $/Mt (≈804 $/J) | bis 10'000 | erst bei grosser Skalierung |
| Scale | ~97–127 $/Mt | unbegrenzt | nicht nötig |

→ **Empfehlung: Starter.** 2'000 Mitglieder sind für die Pioneer-Runde mehr als genug. **To-do Patricia:** genauen Preis im eigenen ThriveCart-Account prüfen — evtl. Sonderkondition für bestehende Besitzer.

### B) Was weiterhin FEHLT: Kalender / Live-Events
ThriveAcademy hat **keinen** nativen Kalender und **kein** Live-Event-Feature. Heisst:
- **Live-Calls weiterhin über Zoom.**
- **Call-Aufzeichnungen** als „Course" in die Community (Elevate-Muster, s. Abschnitt 4).
- **Termin-Reminder** über den **Announcements-Space** + **AC-Reminder-Mail** + gepinnter Post.

Ebenfalls (noch) nicht: native Mobile-App, Zapier/API innerhalb der Academy, In-Community-Rechnungsverwaltung.

---

## 2. Die MBA als EINE Community (fast 1:1 dein Elevate)

```
COMMUNITY: „Mum Business Academy"
│
├── 📣 Announcements (Space)        → du sendest: Wochen-Impuls, Call-Reminder, News
│
├── 📚 KURSE (Space-Kategorie mit Course-Spaces)
│     ├── 🎯 Start hier — Deine MBA-Landkarte   (Willkommens-Kurs, Pflicht oben)
│     ├── 🤖 PIA — deine KI-Mentorin             (Tool-Kurs: Login + Befehle)
│     ├── 📱 Instagram-Kundenmaschine            (Phase 1, existiert)
│     ├── ⏰ Mama-CEO                            (Phase 2, existiert)
│     ├── 🚀 Digitale Produktwelt               (Phase 3, existiert)
│     └── 🤝 Die Umsetzerinnen — Call-Aufzeichnungen (datiertes Archiv)
│
├── 🙋 Q&A (Space)                  → strukturierte Fragen, beste Antworten gepinnt
├── 💬 Lounge (Space)               → Vorstellung, Erfolge, Austausch, Off-Topic
└── 🎁 Resource Hub (Space)         → Vorlagen, Swipe-Files, Downloads
```

**Gamification:** Engagement Booster aktiv. **Onboarding:** der Willkommens-Kurs steht oben + 1 fixierter Announcement „Starte hier".

> **Das löst das Elevate-Problem:** Bei Elevate liegen 21 Kacheln flach nebeneinander und neue Leute fragen „wo fang ich an?". Bei uns führt der Willkommens-Kurs + die feste Kurs-Reihenfolge + ein Pin-Announcement die Mama an die Hand.

---

## 3. Der rote Faden — die Member-Journey

Das Salespage-Versprechen: *„den ganzen Weg in der richtigen Reihenfolge — und jemanden, der mit dir dranbleibt."* Die 4 Phasen:

```
PHASE 0 — ANKOMMEN        → Willkommens-Kurs (20 Min)
   ↓   "Ich weiss, wo ich bin und was als Erstes dran ist."
PHASE 1 — SICHTBAR WERDEN → Instagram-Kundenmaschine
   ↓   "Fremde Frauen schreiben MICH an."
PHASE 2 — ZEIT & STRUKTUR → Mama-CEO
   ↓   "Mein Business läuft in wenigen fokussierten Stunden."
PHASE 3 — EIGENES ANGEBOT → Digitale Produktwelt
   ↓   "Ich habe ein Einkommen, das mir gehört."
DURCHGEHEND — DRANBLEIBEN → PIA (täglich) + Calls (2×/Monat) + Q&A/Lounge (Di & Do von dir)
```

**Reihenfolge-Begründung:** erst Schaufenster (Sichtbarkeit), dann Motor (Zeit/Struktur), dann die grösste Stufe (eigenes Angebot). Empfohlener Pfad, **kein Drip-Zwang** — wer schon sichtbar ist, springt zu Mama-CEO.

**Umsetzung in ThriveAcademy:** Space-Unlock-Rules können den Pfad sanft führen (z.B. zeitbasierter Drip), müssen aber nicht hart sperren. Für Pioneer: **alles offen lassen**, Reihenfolge nur empfehlen.

---

## 4. Die Umsetzerinnen-Call-Kurs (der Elevate-Clou)

In Elevate ist „LIVE Calls" innen eine Liste **datierter Lektionen** nach Jahr gruppiert (`24. Juni 16 Uhr – Q&A → Video`). Jede neue Aufzeichnung kommt als Lektion dazu → lebendiges Archiv + Salespage-Beweis („über ein Jahr Begleitung").

**In ThriveAcademy:** Kurs „🤝 Die Umsetzerinnen" mit 2 Modulen:
- **Modul A — Experten-/Themen-Calls** (1×/Monat, mit Q&A)
- **Modul B — Reine Q&A-Calls** (1×/Monat)

Pro Call eine Lektion: Titel = `[Datum] [Uhrzeit] — [Thema]`, Inhalt = Zoom-Aufzeichnung + 2–3 Zeilen „darum ging's" + ggf. Download. **Kein Drip** auf diesem Kurs — alle Aufnahmen frei. Die **Course-Community** unter jeder Call-Lektion fängt Nachfragen auf.

12-Monats-Themenplan: [[11-willkommens-modul-und-callplan]].

---

## 5. PIA-Einbettung in den Lernweg

PIA ist dein Killer-USP (= was bei Elevate „ARIA"/„Claude" als Kachel sind, nur deine eigene). Sie darf nicht isoliert danebenstehen, sondern dockt an **jedem Punkt** an: „Lern es im Kurs → setz es sofort mit PIA um."

| Phase / Kurs | Was die Mama lernt | PIA-Befehl |
|---|---|---|
| Onboarding | Wo steh ich, mein Thema | `/onboarding` (Profil → PIA kennt ihre Stimme) |
| Insta-KuMa — Positionierung | Experten-Satz | `/positionierung` |
| — Schaufenster | Bio + Highlights | `/bio` |
| — Content | Hooks, Captions, Posts | `/hooks` · `/post` · `/woche` |
| — Leads | Freebie/Lead-Magnet | `/leadmagnet` |
| Mama-CEO — Struktur | Power-Slots, Hütchen, Notion | (manuell; PIA als Sparring) |
| Digitale Produktwelt | Produkttreppe + Funnel | `/produkt` · `/funnel` · `/salespage` |

> Jede relevante Lektion endet mit einem **„Jetzt mit PIA"-Block**: *„Du hast's gelernt — jetzt lass PIA es mit dir machen. Tipp `/hooks` und du hast in 2 Minuten 10 Hooks in deiner Stimme."*

**PIA-Kurs (Position 2):** 3 Lektionen — (1) Was PIA ist + Login (E-Mail+Passwort, [[project_pia-login-email-passwort]]) · (2) Dein erstes `/onboarding` · (3) Alle Befehle als Mama-Cheatsheet.

---

## 6. ✅ ENTSCHEIDUNG (30.6.2026): Voll ThriveAcademy-Community

**Patricia hat entschieden: die MBA-Community läuft komplett in ThriveAcademy** — kein separates Telegram für die bezahlte MBA. Alles an EINEM Ort wie ihr Elevate-Setting.

**Was bleibt unverändert (das eigentliche Versprechen):**
- 2 Live-Calls pro Monat (Zoom, Aufzeichnungen als Kurs).
- **Patricia ist Di & Do persönlich da** — neu im **Q&A-Space** der Academy statt in Telegram.
- Ein ganzes Jahr Begleitung.

**Was sich ändert:**
- Community-Austausch, Q&A, Vorstellung, Erfolge → **ThriveAcademy-Spaces** (Q&A + Lounge + Announcements).
- **Steckbrief + Salespage angepasst:** „begleitete Telegram-Gruppe" → „begleitete Community direkt in der Academy" (Di & Do bleibt). Erledigt in den MD-Quellen; HTML/WP-Deploys + Mails siehe To-do-Liste unten.

> ⚠️ **Abgrenzung:** Die **Bootcamp-Telegram-Gruppe** (laufende 0€-Challenge 29.6.–3.7.) bleibt bestehen — die Entscheidung betrifft nur die bezahlte MBA.

### To-do: wo „Telegram" noch in Customer-Assets steht (vor Cart 3.7. anpassen)
- [x] `mba-produktsteckbrief.md` (intern)
- [x] `mba-salespage.md` (MD-Quelle)
- [ ] `mba-salespage.html` + `mba-wp-*.html` (deployte HTML-Versionen — gleiche Wort-Ersetzung)
- [ ] WP-Seite live (Slug `mba-webinar` / Salespage-Seite) — nach HTML-Update neu einspielen
- [ ] Cart-/Onboarding-Mails in `bootcamp-mails/` + `mba-onboarding-mails/` auf Telegram-Erwähnung prüfen

---

## 7. Setup-Schritte in ThriveAcademy (ohne Vorwissen)

1. **Einloggen** auf `lms.thrivecart.com` → Plan wählen (Starter) → genauen Preis prüfen.
2. **„New Community" anlegen:** Name „Mum Business Academy", Zugang = bezahlt.
3. **Spaces einrichten:** Announcements · Q&A · Lounge · Resource Hub + Space-Kategorie „Kurse".
4. **Kurse bauen** (die 6 aus Abschnitt 2). Die 3 bestehenden Kurse als Module/Lektionen einpflegen (Videos hoch/eingebettet).
5. **Reihenfolge fixieren:** Start-hier + PIA oben.
6. **Gamification** = Engagement Booster.
7. **Commerce verknüpfen:** bestehendes ThriveCart-Produkt → Product-to-Access-Mapping → Auto-Enrollment.
8. **Anrechnung Einzelkurs-Käuferinnen:** über Coupon/Preis-Anpassung im ThriveCart-Checkout.
9. **Cover-Bilder** pro Kurs (Brand-Look) + Community-Branding (Logo, Petrol/Creme).
10. **Zoom-Calls** terminieren → Aufzeichnungen in die Umsetzerinnen-Kurs.

*(Ich kann jeden dieser Schritte live mit dir über Chrome machen.)*

---

## 8. Skool vs. ThriveAcademy — soll Patricia wechseln?

| Kriterium | Skool | ThriveAcademy |
|---|---|---|
| Alles-in-einem (Kurs+Community+Gamification) | ✅ | ✅ (neu seit Mai 2026) |
| Checkout/Verkauf integriert | ❌ extern | ✅ ist DER Checkout |
| Kalender/Live-Events | ✅ | ❌ (Zoom extern) |
| Kosten | ~99 $/Mt | ~37 $/Mt (Starter) |
| Du hast den Checkout schon | — | ✅ ThriveCart läuft eh |

**Empfehlung Pioneer-Runde: ThriveAcademy.** Günstiger, Checkout + Kurs + Community aus einer Hand, fast voller Skool-Funktionsumfang. Einzige Lücke = Live-Kalender, die du mit Zoom + Announcements schliesst. Der einzige Grund für Skool wäre, wenn dir der native Kalender + die ausgereiftere Community wichtiger sind als die Checkout-Integration und der Preis — für deine Lage überwiegt ThriveAcademy klar.

---

## Quellen (Recherche 2026-06-30)
- [Introducing ThriveAcademy – Communities](https://thrivecart.com/blog/introducing-thriveacademy-communities/)
- [Building Your ThriveAcademy Community (Helpdesk)](https://support.thrivecart.com/help/building-your-thrive-academy-community/)
- [Getting Started with ThriveAcademy (Helpdesk)](https://support.thrivecart.com/help/getting-started-with-thrive-academy/)
- [ThriveCart Launches ThriveAcademy (Pressemitteilung, 19.5.2026)](https://www.globenewswire.com/news-release/2026/05/19/3297821/0/en/ThriveCart-Launches-ThriveAcademy-A-New-Learning-Platform-That-Puts-Community-at-the-Center-of-Every-Course.html)

## 🔗 Verwandte Notizen
- [[11-willkommens-modul-und-callplan]] · [[mba-produktsteckbrief]] · [[mba-salespage]]
- [[project_mba-plattform-thrivecart-academy]] · [[project_pia-login-email-passwort]] · [[feedback_KRITISCH-mba-bundle-struktur]]
