---
tags: [tools, produkt]
---

# Startklar-Service — der Prüf-Dienst hinter der Werkstatt

Gibt der [Startklar-Werkstatt](../../outputs/produkte/instagram-startklar/04-arbeitsblaetter/startklar-werkstatt.html) die ausführliche Analyse. Die Werkstatt läuft auch ohne diesen Dienst — dann bleibt es beim sofortigen Formcheck im Browser.

## Was hier passiert

```
Käuferin tippt ihren Hook
   ↓
Formcheck im Browser          gratis, sofort, funktioniert offline
   ↓
POST /api/pruefen             mit Station, Eingabe, ihrem Thema und dem Formcheck-Ergebnis
   ↓
Claude Opus 5                 Systemtext = Patricias Regeln (lib/patricia-regeln.js)
   ↓
Antwort in Patricias Stimme + Überleitung zur Instagram-Kundenmaschine
```

Der Systemtext bleibt zwischen Anfragen identisch und wird deshalb zwischengespeichert — das drückt die Kosten auf etwa ein Zehntel für den Regelteil.

## Dateien

| Datei | Zweck |
|---|---|
| `api/pruefen.js` | Der Endpunkt. Herkunftsprüfung, Zugangscode, Zähler, Aufruf, Fehlerbehandlung. |
| `lib/patricia-regeln.js` | **Der Inhalt.** Haltung, Stimme, Verbote, Fachregeln, Stationen. Hier änderst du, wie das Tool klingt. |
| `vercel.json` · `package.json` | Deployment |
| `.env.example` | Vorlage für die Variablen |

## Einrichten

```bash
cd scripts/startklar-service && npm install
```

Dann `.env.example` nach `.env` kopieren und ausfüllen. Danach lokal testen:

```bash
npx vercel dev
```

Der Endpunkt läuft dann auf `http://localhost:3000/api/pruefen`. Zum Ausprobieren in der Werkstatt vorübergehend `DIENST_URL` in `startklar-werkstatt.html` auf diese Adresse setzen.

## Deployen

```bash
cd scripts/startklar-service && npx vercel --prod
```

Danach im Vercel-Projekt unter Settings → Environment Variables setzen:

| Variable | Wert |
|---|---|
| `ANTHROPIC_API_KEY` | dein Schlüssel |
| `ZUGANGSCODES` | Komma-Liste, z.B. `STARTKLAR-A1,STARTKLAR-A2` |
| `MAX_PRUEFUNGEN` | optional, Standard 150 |
| `ERLAUBTE_HERKUNFT` | optional, weitere Adressen |

Zum Schluss die Adresse in `startklar-werkstatt.html` eintragen:

```js
const DIENST_URL = "https://<dein-projekt>.vercel.app/api/pruefen";
```

## Zugangscodes

Ohne `ZUGANGSCODES` ist der Dienst offen — nur für deine eigenen Tests brauchbar, sonst zahlt jeder Fremde auf deine Rechnung mit.

Für den Verkauf: Codes in ThriveCart mit der Kauf-Mail ausliefern und in die Liste eintragen. Sammelcodes pro Monat (`STARTKLAR-2026-09`) sind der einfachste Anfang; wenn einer öffentlich wird, tauschst du ihn aus.

## Obergrenze

Die harte Grenze pro Code braucht einen KV-Speicher (Vercel KV oder Upstash Redis). Sind `KV_REST_API_URL` und `KV_REST_API_TOKEN` gesetzt, zählt der Dienst mit und stoppt bei `MAX_PRUEFUNGEN` mit einer freundlichen Meldung. Ohne KV läuft alles normal, nur ohne Grenze — für den Start mit wenigen Käuferinnen vertretbar, spätestens beim Bewerben über Anzeigen nachrüsten.

## Kosten

Rund 1,5 Rappen pro Prüfung mit Claude Opus 5. Ein kompletter Durchgang durch alle sechs Stationen liegt bei etwa 10 Rappen, eine Vielnutzerin mit 100 Prüfungen bei rund 1.50 CHF. Bei 39 CHF Verkaufspreis ist das unter einem Prozent.

Der Formcheck davor kostet nichts und fängt die einfachen Fehler ab, bevor eine Anfrage rausgeht.

## Was noch offen ist

- [ ] `npm install` und ein echter Testlauf mit deinem Schlüssel — der Aufruf ist geschrieben und syntaktisch geprüft, aber noch nie live gelaufen
- [ ] Deployen und `DIENST_URL` eintragen
- [ ] Zugangscodes in ThriveCart einrichten
- [ ] KV-Speicher für die Obergrenze, bevor Anzeigen laufen
