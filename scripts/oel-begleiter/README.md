# 🌿 Öl-Begleiter — 7-Tage-Sample-Companion (Telegram)

Ein **Mehrbenutzer-Telegram-Bot**, der Menschen, die von Patricia ätherische
Öl-Pröbchen (Samples) bekommen haben, **7 Tage lang durchs Ausprobieren begleitet** —
jeden Morgen eine kleine, machbare Etappe. Löst das „Sample liegt ungenutzt in der
Schublade"-Problem und führt am Ende sanft zur eigenen kleinen Hausapotheke.

Anders als der Story-Bot (nur Patricia) ist der Öl-Begleiter für **viele Testerinnen
gleichzeitig** offen — jede chattet privat, hat ihr eigenes Profil und ihren eigenen
7-Tage-Fortschritt.

## Das Besondere: echtes Companion-Wissen, keine erfundenen Fakten

Das Öl-Wissen kommt **nicht** aus dem Modell-Allgemeinwissen, sondern aus **derselben
Wissensbasis wie der doTERRA-Companion** (`doterra-bot.vercel.app`) — der Supabase-
Tabelle `documents` mit `category="product"` (Enjoils-Hefte + Produktwissen). Vor jeder
Etappe holt der Bot das echte Produktwissen zu den Ölen der Testerin und baut die
Etappe nur daraus. Fehlt die Anbindung, macht der Bot bewusst **keine** konkreten
Wirkungs-Aussagen (statt zu erfinden). Siehe `companion_kb.py`.

## Der 7-Tage-Bogen

| Tag | Thema |
|-----|-------|
| 1 | Ankommen & richtig testen (riechen, verdünnen, Diffuser, Sicherheit) |
| 2 | Frische & Energie am Morgen |
| 3 | Fokus im Alltags-Chaos |
| 4 | Ruhe & Runterkommen am Abend |
| 5 | Ein Wohlfühl-Moment nur für dich |
| 6 | Öle im Familien-Alltag |
| 7 | Rückblick + Mini-Routine + sanfte Brücke zur Hausapotheke |

## Ablauf für die Testerin

1. `/start` → Onboarding (5 Fragen: Name, welche Pröbchen, Wunsch, Alltag, Erfahrung —
   Text oder Sprachnotiz)
2. Sofort **Tag 1**; danach jeden Morgen (Default 08:00) automatisch die nächste Etappe
3. `/heute` = heutige Etappe abrufen · `/weiter` = nächste vorziehen
4. Freie Fragen zu ihren Ölen jederzeit (nur aus dem Companion-Wissen beantwortet)

## Architektur

| Datei | Zweck |
|-------|-------|
| `bot.py` | Telegram-Handler, Onboarding-Flow, Voice, **täglicher Auto-Push** (JobQueue) |
| `onboarding.py` | 5 Onboarding-Fragen |
| `store.py` | Profile pro Userin als JSON in `data/users/`, 7-Tage-Fortschritt |
| `begleiter_brain.py` | Claude-Generatoren für die 7 Etappen + freie Fragen |
| `companion_kb.py` | Zugriff auf die Companion-Wissensbasis (Supabase, `category=product`) |
| `knowledge.py` | Voice-/Compliance-Wissen aus `context/` (Stil-Layer) |
| `transcribe.py` | optionale Sprachnotiz-Transkription (Whisper) |
| `config.py` | Env + Setup-Check |

## Eingebaute Regeln

- Freundin-Voice, kein Stakkato, Schweizer „ss", keine KI-Floskeln, keine erfundenen Zahlen
- **doTERRA-Compliance:** keine Heilversprechen, „bei mir war"-Frame, Sicherheit als Fürsorge
- **Öl-Aussagen nur aus dem Companion-Wissen** — sonst neutrale Sinnes-/Ritual-Sprache
- doTERRA-Ölnamen korrekt (Air, On Guard, Deep Blue, Adaptiv …)

## Setup

```bash
cd scripts/oel-begleiter
cp .env.example .env      # Werte eintragen
pip install -r requirements.txt
python config.py          # Setup-Check
python companion_kb.py "Lavendel, Zitrone"   # KB-Anbindung testen (optional)
python bot.py             # Bot starten
```

### Env-Variablen

| Variable | Pflicht | Zweck |
|----------|---------|-------|
| `OEL_BOT_TOKEN` | ✅ | **Eigener** BotFather-Bot (nicht Story-/PIA-Bot) |
| `ANTHROPIC_API_KEY` | ✅ | Etappen-Texte |
| `SUPABASE_URL` | ⭐ | Companion-Wissensbasis (dieselbe wie doterra-bot) |
| `SUPABASE_SERVICE_KEY` | ⭐ | dazu (oder `SUPABASE_SERVICE_ROLE_KEY`) |
| `OPENAI_API_KEY` | – | nur für Sprachnotizen |
| `OEL_ADMIN_CHAT_ID` | – | `/admin`-Statistik für Patricia |
| `OEL_SEND_HOUR` / `OEL_TIMEZONE` | – | Push-Zeit (Default 08:00 Europe/Zurich) |
| `OEL_PATRICIA_KONTAKT` | – | Tag-7-Brücke (Default: „schreib HAUSAPOTHEKE") |

⭐ = ohne Supabase läuft der Bot, macht aber keine konkreten Öl-Aussagen.

## Deploy (Railway, wie PIA)

Als **Worker** (`Procfile`: `worker: python bot.py`). Bot pollt Telegram und pusht
täglich. Alle Env-Variablen als Railway-Variablen hinterlegen.

> ⚠️ **Sandbox-Hinweis:** In der Web-Claude-Sandbox persistiert `.env` nicht zwischen
> Sessions, und `data/` (Profile) ist ephemer. Für echten Betrieb auf Railway (oder
> lokal bei Patricia) laufen lassen — dann bleiben Profile + Fortschritt erhalten.
