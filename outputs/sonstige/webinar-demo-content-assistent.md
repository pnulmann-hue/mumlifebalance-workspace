---
tags: [content, webinar]
---

# 🎬 Webinar-Live-Demo · Content-Assistent

**Datum:** 2026-05-15 (Fr) — Mai-Webinar „In 90 Min dein Mama-Leben mit KI-Assistenten umkrempeln"
**Dauer Demo-Block:** 10-12 Min
**Ziel:** Aha-Moment „Pain im Kopf der Zielgruppe → fertiger Post in Blotato — alles automatisch"

---

## 🛠 Vor dem Webinar (30 Min Setup-Pflicht)

### Browser-Tabs vorbereiten

1. **Tab 1 — Workspace-Editor** (VS Code / Finder)
   - Pfad: `C:\Users\pnulm\Desktop\Mein Business`
   - Sichtbar: `outputs/`, `scripts/`, `.claude/commands/`
2. **Tab 2 — Terminal** (Claude Code)
   - Working dir: Workspace-Root
   - Claude Code bereits gestartet
3. **Tab 3 — Telegram** (Desktop/Web)
   - Bot-Chat offen mit Push vom 9.5. (20 Hooks KW20)
4. **Tab 4 — Blotato**
   - Eingeloggt, Scheduled-Tab offen
   - M5 Mo 18.5. 19:30 sichtbar
5. **Tab 5 — Notion** (optional)
   - Wochenplanung-DB offen

### Test-Lauf vor Start (5 Min)

```bash
# Prüfen ob die wichtigen Files existieren:
ls outputs/freitag/2026-05-15-hooks.md
ls outputs/freitag/markt-analyse-KW20.md
ls outputs/karussells/render-2026-05-18/
ls outputs/montag/2026-05-18-pick.md
```

Alle 4 müssen da sein. Wenn nicht → Backup-Plan.

---

## 🎤 Live-Demo Drehbuch

### **Min 0-1 · Setup-Reveal**

> *„Das ist mein Content-Assistent. Drei Monitore, alles vernetzt, alles auf einem Konto: meinem."*

**Aktionen:**
- Bildschirm-Sharing starten
- Workspace-Struktur kurz zeigen (Editor mit Folder-Tree)
- Sagen: *„13 Slash-Commands sitzen hier drin. Das hier ist das Hirn von meinem ganzen Setup."*

### **Min 1-3 · Wochenfokus + Marktanalyse**

> *„Jeden Freitag um 8 Uhr läuft mein Bot AUTONOM. Hier ist was er heute Nacht gemacht hat."*

**Aktionen:**
- Editor öffnet `outputs/freitag/markt-analyse-KW20.md`
- Scroll durch die Pain Points (Mentoring + doTERRA)
- Editor öffnet `outputs/freitag/2026-05-15-hooks.md`
- Zeig die 20 Hooks (10 + 10)

**Was sagen:**
*„Diese Marktrecherche hat Claude über Nacht aus Reddit, Foren und LinkedIn rausgezogen. Wo stehen die Mamas in den Diskussionen, was tut ihnen weh, was wünschen sie sich? Und 20 Hook-Vorschläge daraus generiert — 10 für mein Mentoring-Profil, 10 für mein doTERRA-Profil."*

### **Min 3-5 · Telegram-Push zeigen**

> *„Damit ich nicht jeden Morgen Files öffnen muss, schickt er mir das Wichtigste via Telegram."*

**Aktionen:**
- Telegram öffnen (Tab 3)
- Den Push vom 9.5. (oder 15.5.) zeigen mit den 20 Hooks
- Kurz durchscrollen

**Was sagen:**
*„Egal wo ich bin — Spielplatz, Auto, Wartezimmer — ich kann auf dem Handy lesen, pick mir 5 pro Profil und der Rest läuft."*

**Backup:** Screenshot des Telegram-Pushes vorab in Tab 1 hinterlegen falls Telegram Web hängt.

### **Min 5-8 · Build live zeigen (Aha-Moment!)** ⭐

> *„Ich pick 5+5 und mein Skill baut den Rest. Schaut zu."*

**SICHERE VARIANTE — fertigen Build zeigen:**
- Editor öffnet `outputs/karussells/2026-05-18-mentoring-bio-produktkatalog.md`
- Cover-Hook + Slide-Texte kurz scrollen
- Editor öffnet Ordner `outputs/karussells/render-2026-05-18/mentoring-bio-produktkatalog/`
- Zeig die 10 PNG-Folien als Galerie (alle Slides nebeneinander)

**Was sagen:**
*„Was du gerade siehst — Hook, Slide-Texte, fertige Grafiken, Caption — hat 5 Minuten Build-Zeit gebraucht. Früher hab ich für ein Karussell drei Stunden gebraucht, alle Slides in Canva einzeln gebaut. Heute lass ich Claude das."*

**MUTIGE VARIANTE — live triggern:**
Wenn du dich sicher fühlst:
- Im Terminal tippen: kurze Bitte wie *„zeig mir die Caption von M5 in 100 Wörtern"*
- Claude tippt live → Aha-Moment

→ Aber nur wenn du's vorher 2x geübt hast. Sonst sicher fahren.

### **Min 8-10 · Schedule-Demo (Blotato)**

> *„Und jetzt landet das automatisch in Blotato."*

**Aktionen:**
- Tab 4 (Blotato) öffnen
- Scheduled-Posts-Tab
- Zeig den **M5 Post Mo 18.5. 19:30** mit Vorschaubild

**Was sagen:**
*„Das hier wird in 3 Tagen automatisch auf meinem Instagram gepostet. Ohne dass ich nochmal hinlange. Mein KI-Schreiber hat den Caption geschrieben, mein Render-Bot die Grafiken gebaut, mein Schedule-Bot's eingeplant. Ich hab nur einmal entschieden welcher Hook reinkommt."*

### **Min 10-12 · Die Brücke (Webinar-Pitch)**

> *„Das ist der Hebel. Ich entscheide morgens 15 Minuten was rausgeht. Mein KI-Mitarbeiter macht den Rest."*

**Was sagen:**
*„Und genauso läuft auch mein Kochassistent — der weiss was wir essen. Mein Garten-Bot — der erinnert mich an Sätaufgaben. Mein Morgen-Briefing — das mir um 7:30 sagt was heute zählt. Plus drei Kunden-Bots, die im Hintergrund für meine Mentees arbeiten."*

*„18 Stunden Woche. 4 Kinder. Vom Küchentisch im Appenzellerland. Kein Monat mehr ohne Verkauf. Das ist Mama-CEO 2026."*

→ Übergang zum Pitch oder zum nächsten Webinar-Block.

---

## ⚠️ Backup-Plan falls was schiefgeht

| Risiko | Fallback |
|---|---|
| Claude lädt langsam / hängt | Pre-rendered: `outputs/karussells/render-2026-05-18/` direkt im Editor zeigen statt live bauen |
| Telegram Web hängt | Screenshot der Hooks-Liste vorab in Editor offen |
| Blotato lädt nicht | Screenshot der Scheduled-Posts vorab |
| Du verhaspelst dich | Geh zurück auf „Das hier ist mein System" und zeig den Output statt zu erklären wie's gebaut wird |
| Kompletter Internet-Ausfall | Lokal die Files offen lassen — du kannst alles ohne Internet zeigen, ausser den Telegram-Push und Blotato |

---

## 🎯 Was du NICHT zeigen solltest

- ❌ Tiefe Tech-Details (Slash-Command-Code, Puppeteer-Render-Skript)
- ❌ Mehr als 3-4 Files öffnen (Verwirrung beim Zuschauer)
- ❌ Live tippen während du redest (zu unsicher, Risiko von Verhasplern)
- ❌ Den ganzen Render-Vorgang (zu langweilig, nichts zu sehen während Puppeteer läuft)
- ❌ Mehrere Skill-Files gleichzeitig erklären

**Fokus immer:** „Was reinkommt" (Wochenfokus + Pain Points) → „Was rauskommt" (fertige Posts in Blotato). Der Hebel dazwischen ist der Aha-Moment.

---

## 🧘 Mindset für den Demo-Block

- Du zeigst **kein Tutorial** — du zeigst **die Realität**
- Du **musst nicht alles erklären** — die Zuschauer sollen den Effekt sehen, nicht die Mechanik
- **Pausen sind OK** — zwischen Aktion und nächstem Satz 1-2 Sekunden atmen lassen
- Wenn was schiefgeht: *„Das ist mein Bot. Manchmal hängt er. Genau wie ihre Bots auch hängen werden — und genau deshalb zeig ich's euch ehrlich, nicht hochglanz."*

→ Authentizität schlägt Perfektion.

---

## ✅ Pflicht-Action 30 Min vor Webinar-Start

- [ ] Alle 5 Tabs offen + getestet
- [ ] Terminal-Schriftgröße hochgestellt (für Bildschirm-Sharing)
- [ ] Notifications stumm (keine privaten Telegram-Pop-ups)
- [ ] Wasser bereit
- [ ] Atmen.

**Du machst das nicht zum ersten Mal — du machst es zum ersten Mal vor Publikum. Das System läuft. Du musst nur drauf zeigen.**
