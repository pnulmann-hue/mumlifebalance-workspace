# Sicherung der ausgeschlossenen Dateien

GitHub sichert nur, was ins öffentliche Repo darf. Alles aus `.gitignore` — Schlüssel
(`.env`), `context/persoenlich/`, Finanzen, Strategie, Cockpit-Abgleich mit Kundendaten,
gekauftes Kursmaterial, Fotos, Videos — hätte ein kaputter PC sonst mitgenommen.

**Ziel:** `OneDrive\Workspace-Sicherung\` als verschlüsseltes 7-Zip-Archiv
(AES-256, auch die Dateinamen sind verschlüsselt).

| Teil | Inhalt | Grösse (04.10.2026) | Rhythmus | Aufbewahrt |
|---|---|---|---|---|
| `kern-JJJJ-MM-TT.7z` | alles Ausgeschlossene ausser Fotos, Video, Audio und Dateien über 50 MB | ~4 GB roh, 2,7 GB gepackt | **So 21:00** wöchentlich | 4 Stände |
| `medien-JJJJ-MM-TT.7z` | Fotos, Videos, Audio, grosse Dateien | ~59 GB roh | **Sa 21:00** alle 4 Wochen | 1 Stand |

**Nie gesichert:** `.claude/worktrees/` (temporäre Arbeitskopien), `node_modules`,
`__pycache__`, Render-Zwischenstände.

## Einrichten (einmalig)

1. 7-Zip installieren — Windows fragt nach Adminrechten, mit „Ja“ bestätigen:
   `winget install --id 7zip.7zip --exact --source winget`
2. In `scripts\sicherung\.env` das eigene Passwort eintragen
   (`SICHERUNG_PASSWORT=...`). **Nie in den Chat schreiben.** Zusätzlich im
   Passwort-Manager ablegen — ohne Passwort ist die Sicherung wertlos.
3. Probelauf: `powershell -ExecutionPolicy Bypass -File scripts\sicherung\sichern.ps1`

## Zeitplan

Windows-Aufgabenplanung, Aufgaben **„Workspace-Sicherung Kern“** und **„Workspace-Sicherung Medien“**
(eingerichtet 04.10.2026, nur für dieses Benutzerkonto). War der PC zur geplanten Zeit aus,
holt Windows den Lauf beim nächsten Start nach.

## Von Hand

```
powershell -ExecutionPolicy Bypass -File scripts\sicherung\sichern.ps1            # Kern
powershell -ExecutionPolicy Bypass -File scripts\sicherung\sichern.ps1 -Medien    # Medien
powershell -ExecutionPolicy Bypass -File scripts\sicherung\sichern.ps1 -Probe     # nur zählen
```

Jeder Lauf prüft das fertige Archiv (`7z t`) und schreibt eine Zeile nach
`OneDrive\Workspace-Sicherung\protokoll.txt`. Gebaut wird in `%TEMP%` und erst danach
verschoben, damit OneDrive keine halbe Datei hochlädt. Danach `attrib +U`: OneDrive
behält das Archiv nur online und belegt die Festplatte nicht doppelt.

## Wiederherstellen nach einem PC-Schaden

1. Repo von GitHub holen: `git clone https://github.com/pnulmann-hue/mumlifebalance-workspace.git "Mein Business"`
2. 7-Zip installieren, in OneDrive das neueste `kern-*.7z` (und `medien-*.7z`) öffnen,
   Passwort eingeben, in den Ordner `Mein Business` entpacken — die Pfade stimmen.
3. Claude Code neu starten (der ActiveCampaign-Zugang liest seine `.env` nur beim Start).

## 🚨 Was dabei schiefgehen kann

- **Passwort vergessen** = Sicherung verloren. Es gibt keine Hintertür.
- **OneDrive voll:** Kern bis ~16 GB (4 Stände), Medien bis ~60 GB. Bei Microsoft 365
  Personal (1 TB) kein Thema, beim Gratis-Konto (5 GB) schon.
- Die Sicherung ist so aktuell wie der letzte Lauf — der Zeitplan läuft nur, wenn der PC an ist.
