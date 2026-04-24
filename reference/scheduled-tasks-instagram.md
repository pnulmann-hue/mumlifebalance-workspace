# Scheduled Tasks — Instagram Content-System

Konfigurationen für die beiden automatischen Tasks.
Wenn Remote Triggers verfügbar sind: `/schedule` in Claude Code verwenden und diese Prompts einfügen.

---

## Canva-Ordner-IDs

| Ordner | ID |
|---|---|
| Instagram Karussells | `FAHG78rHy1g` |
| Posting Queue | `FAHG7yBZfpE` |
| Gepostete Beiträge | `FAHG7-zV3Cw` |

## Blotato Instagram Account-ID

`[NOCH EINTRAGEN]` — In Blotato Dashboard nachschaün oder `blotato_list_accounts` ausführen.

---

## Task 1: Wöchentliche Karussells

- **Name:** wöchentliche-karussells
- **Schedule:** Montag 07:00 (Cron: `3 7 * * 1`)
- **Modell:** Sonnet

### Prompt:

```
Erstelle 10 Instagram-Karussell-Entwürfe für diese Woche.

SCHREIBREGELN:
- Echte Umlaute (ä, ö, ü, ss)
- Direkt, motivierend, nahbar
- Hook nicht in der Caption wiederholen
- Echter Mehrwert auf jeder Slide

Schritt 1: Kontext laden
- Lies context/brand-voice.md für meine Stimme
- Lies context/hook-framework.md für Hook-Regeln
- Lies context/caption-formeln.md für Caption-Strukturen

Schritt 2: Themen recherchieren
- Recherchiere über WebSearch nach aktuellen Trends in:
  Network Marketing, Instagram-Strategie für Mamas, KI im Solopreneur-Business, digitale Produkte, Mama-Business, Stressbewältigung

Schritt 3: 10 Karussells erstellen
Pro Karussell eine eigene Datei in outputs/karussells/ mit dem Format YYYY-MM-DD-nr.md:
- Cover-Slide: Headline (Hook aus hook-framework.md) + Subtext + "Swipe -->"
- Slide 2-6: Headline + Erklärungstext mit echtem Mehrwert
- CTA-Slide: "Speicher dir das." + CTA (aus caption-formeln.md CTA-Varianten)
- Caption: Basierend auf caption-formeln.md + 5-10 Hashtags

Meine Zielgruppe: Mamas im Network Marketing, die ihr Business themenbasiert aufbauen wollen, Instagram strategisch nutzen möchten und offen für KI-Unterstützung sind.

Kernbotschaft: Du brauchst kein perfektes Setup — du brauchst ein System, das zu deinem Mama-Leben passt, und den Mut, dein Expertenthema sichtbar zu machen.
```

---

## Task 2: Instagram Posting Queue

- **Name:** instagram-posting-queue
- **Schedule:** Täglich 12:00 (Cron: `3 12 * * *`)
- **Modell:** Sonnet

### Prompt:

```
Du bist meine Instagram-Posting-Automatisierung.
Prüfe meinen Canva-Ordner "Posting Queue" und plane neue Beiträge über Blotato ein.

1. Ordner prüfen
   list-folder-items mit folder_id FAHG7yBZfpE
   Wenn leer: nichts tun, Session beenden.

2. Für jedes Design:
   a) Kommentare lesen (list-comments) = Caption
      Falls kein Kommentar: Slide-Texte lesen (get-design-content) + Caption generieren
      Lies context/brand-voice.md und context/caption-formeln.md für Stil und Struktur
   b) Design als PNG exportieren (export-design)
   c) Post über Blotato einplanen:
      accountId: [BLOTATO-ACCOUNT-ID-EINTRAGEN]
      platform: instagram
      scheduledTime: Morgen 14:00 Uhr (ISO 8601 + Zeitzone Europe/Zurich)
   d) Design verschieben nach "Gepostete Beiträge"
      folder_id: FAHG7-zV3Cw

Wichtig:
- Nur Designs, KEINE Unterordner
- Max 3 Posts pro Tag
- Bei Fehler: Design in Queue lassen + Fehler loggen
```

---

_Zuletzt aktualisiert: 2026-04-15_
