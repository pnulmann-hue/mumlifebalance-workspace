---
tags: [moc, mealplan, ernaehrung]
---

# 🥗 Mealplan & Ernährung — Map of Content

Wochenplanung für 5-6 Personen + Patricias persönliche Ernährungsziele (MyBodyAdvice).

## 🧠 Briefing
- [[meal-planning-bot]] — Komplettes Briefing (Haushalt, Profil, Vorräte, Rezeptquellen, Coaching)
- Slash-Command: `/mealplan`

## 🗄️ Rezepte-Datenbank
- `scripts/kochbot-rag/` — Supabase RAG-Backend (~1900 Rezepte, gitignored)
- Workflow: `python scripts/kochbot-rag/query.py "<Anfrage>"` vor jeder Empfehlung
- Whitelist-Domains: Cookidoo, Marcel Paa, Streusel, Migusto, BettyBossi, Swissmilk, Fooby, etc.

## 📋 Wochenpläne
- Ordner: `outputs/mealplans/`
- Format: `YYYY-KW##-wochenplan.md` + `YYYY-KW##-wochenplan.html`
- Aktuell: KW18, KW19, KW21

## ⛔ Anti-Halluzinations-Regeln
- Nie aus dem Sprachmodell erfinden — IMMER Supabase oder Whitelist-URL
- Quelle in Format: `Quelle: [Dateiname.pdf | URL]`

## 🎯 Verwandte Bereiche
- [[MOC-Garten]] — Saisonale Zutaten + Gartenverarbeitung

#mealplan #ernaehrung #kochen
