# Produktwelt-Companion

Geführter KI-Chat, der einer Network-/Onlinebusiness-Mama in **8 Stufen** ihre komplette Produktwelt baut —
von Thema/Nische bis zu Funnel und Salespage. Bonus im Kurs „Vom Networkwissen zur digitalen Produktwelt"
und in der MBA. **Vercel-Zwilling** zu `scripts/bio-check-bot` und `scripts/freischaufeln`.

Konzept-Spec (was er alles kann + Kurs-Abdeckung):
`outputs/produkte/vom-networkwissen-zur-digitalen-produktwelt/04-produktwelt-companion-MASTER.md`

## Aufbau

```
produktwelt-companion/
├── api/generate.js        # Chat-Relay → Claude (system-prompt + messages)
├── lib/system-prompt.md   # das Gehirn: Stimme, Methode, 8 Stufen
├── public/index.html      # Chat-Frontend in Patricias Brand
├── vercel.json · package.json · .env.example
```

## Die 8 Stufen

0 Onboarding · 1 Produkttreppe · 2 0€-Freebie · 3 Zusatzangebote · 4 Platzierung ·
5 Inhalte erstellen · 6 Funnel · 7 Salespage · 8 Übergabe.
Er arbeitet eine Stufe nach der anderen, liefert je ein konkretes Ergebnis und fragt „Passt das, oder ändern?".

## Lokal testen

```bash
cd scripts/produktwelt-companion
npm install
cp .env.example .env      # ANTHROPIC_API_KEY eintragen
npm run dev               # vercel dev → http://localhost:3000
```

## Deploy (Vercel)

1. `npm run deploy` (oder Projekt in Vercel mit diesem Ordner als Root verbinden).
2. In Vercel → Settings → Environment Variables: **ANTHROPIC_API_KEY** setzen.
3. Optional eigene Domain, z.B. `companion-produktwelt.mumlifebalance.ch`.
4. Danach als Lektion „Dein Produktwelt-Companion" im Kurs + MBA-Hub verlinken.

## Modell

Nutzt `claude-sonnet-4-5` (wie deine anderen Bots). Bei Bedarf in `api/generate.js` (`MODEL`) anpassen.

## Hinweise

- **Keine erfundenen Zahlen**, keine Heil-/Einkommensversprechen (im System-Prompt verankert).
- Wissensbasis ist v1 direkt im System-Prompt eingebettet. Für tieferes Grounding später eine
  `lib/wissensgrundlage.md` (Julia-Trost-Methode + Kurs-Lektionen) ergänzen und in `generate.js` anhängen.
