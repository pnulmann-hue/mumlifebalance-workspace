# Post-Mai-Launch TODOs (ab Mo 1.6.2026)

Anlegt: 2026-05-06 (während Mai-Launch-Setup)
Status: PENDING — anschauen nach erstem Live-Call der Pilot-Kohorte (Do 4.6.)

---

## 1. AC-Vollautomatisierung via Composio (oder Alternative)

**Problem:** AC's Public API erlaubt KEIN Erstellen von Automations + Templates. Patricia hat den Mai-Launch deshalb hybrid gemacht (CLI-Claude baute 14 Campaign-Drafts via API, Patricia klickte 2 Automations + Goal-Step manuell zusammen).

**Ziel post-Mai:** Bei zukünftigen Launches (Herbst-Selbstlerner-Evergreen, doTERRA-Energie-Kur, alle Q3+Q4-Funnels) soll Claude Code die kompletten AC-Automations selbst bauen können — Templates, Steps, Trigger, Goals.

**Optionen:**

| Option | Aufwand | Kosten | Risiko |
|---|---|---|---|
| **Composio** (kommerzielles MCP) | 1-2h Setup | ~30 EUR/Monat | gering |
| **Zapier-MCP** | 30 Min Setup | Zapier-Plan vorausgesetzt (~20 EUR/Mo) | gering, aber Zapier-abhängig |
| **Eigenes Reverse-Engineering** der AC-internen API | 4-6h | gratis | hoch (kann jederzeit kaputt gehen) |
| **Make.com mit Webhooks** | 1-2h | Make-Plan (~15 EUR/Mo) | gering |

**Empfehlung:** Composio anschauen + bei Mentorin nachfragen welches Tool sie nutzt. Bei Mentorin gleicher Stack = Plan A.

---

## 2. Was wir aus dem Mai-Launch lernen

Während/nach dem Launch (KW 21-22) checken:
- [ ] Hat das hybride Setup gehalten? (Drafts → manuelle Automation → Live-Versand)
- [ ] Wo sind die Schmerzpunkte? (was hätte automatisch gehen sollen?)
- [ ] Welche Mail-Tools fehlen wirklich? (z.B. „Test-Versand an dich selbst", „Letzte 5 Anmeldungen check", „Open-Rate live nach Mail 6")

Diese Liste während der Launch-Woche pflegen → ist die Basis fürs Post-Mai-MCP-Upgrade.

---

## 3. MCP-Erweiterungen die SCHON GEHEN würden (kein Composio nötig)

Falls Patricia keinen Composio-Subscribe will, kann ich (Web-Claude) das eigene MCP minimal erweitern:

- [ ] `list_forms` + `get_form_details` — Form 55 inspecten
- [ ] `list_segments` + `create_segment` — für „Liste 2 MINUS Form-55"-Filter
- [ ] `add_contact_to_list` — Bulk-Aktionen
- [ ] `set_contact_field` — Custom-Field-Updates für Personalisation

Bringt aber NICHTS für Templates + Automations — die fehlen weiterhin.

---

## 4. Wenn alles sauber läuft: doTERRA-Funnel automatisieren

Sobald AC-Voll-Automation steht (Composio/Zapier), kann der gleiche Workflow für doTERRA-Energie-Kur, Bio-Check-Bot, etc. laufen — alle Patricias 7 aktiven Funnels.

→ Dann ist Patricia der erste Mompreneur in der Schweiz mit komplett claude-getriebener Funnel-Architektur. 🎯
