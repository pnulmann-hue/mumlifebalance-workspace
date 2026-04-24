# Canva-Klon — Master-Template zu fertigem Karussell

**Wenn Patricia ihr Master-Template gebaut hat, läuft ab hier alles automatisch.**

## Wie es funktioniert

1. **Input:** Ein Karussell-Briefing (aus `/karussell` oder Montags-Engine) mit:
   - Hook (Cover-Text)
   - Pro Folie: Zitat, Body, Script-Label, Hintergrund-Zahl
   - Foto-Wahl (welche Shots für Cover / Empathie / About-Me)
   - Caption + Hashtags + ManyChat-Keyword

2. **Was Claude macht:**
   - `search-designs` findet „Master-Karussell v1"
   - `create-design-from-candidate` → frischer Klon
   - `start-editing-transaction`
   - Für jeden Platzhalter ein `find_and_replace_text`:
     - `{{HOOK}}` → echter Hook-Text
     - `{{FOLIE_2_QUOTE}}` → echtes Zitat
     - ... usw. für alle ~25 Platzhalter
   - Für jeden Bild-Container ein `update_fill` mit dem gewählten Patricia-Shot aus Brand-Kit
   - `commit-editing-transaction`
   - `move-item-to-folder` → „Claude Designs"
   - Design umbenennen auf Karussell-Titel

3. **Output:** Editierbares Canva-Design in „Claude Designs", ready zum Feintunen oder direkt zum Posten

## Warum das funktioniert wo die UI-Automation scheiterte

- `find_and_replace_text` arbeitet **direkt auf der Canva-API** — kein Browser-UI-Klicken
- Platzhalter-Muster `{{HOOK}}` sind eindeutig und kollidieren nicht mit echtem Content
- `update_fill` kann Bilder in bestehenden Containern ersetzen ohne Layout-Chaos
- Font-Family bleibt wie im Master-Template (keine API-Font-Änderung nötig)
- **Geschwindigkeit:** ~30 API-Calls pro Karussell, ~90 Sekunden total

## Voraussetzungen

- Master-Template existiert in Canva (Titel: „Master-Karussell v1", Ordner: Claude Designs)
- Platzhalter-Text-Boxes mit den Konventionen aus `master-template-spec.md`
- Bild-Container mit ALT-Text-Namen (COVER_PHOTO, EMPATHIE_PHOTO, ABOUT_ME_PHOTO) oder via Position identifizierbar
- Brand-Kit-Fotos für Patricia verfügbar

## Nächster Schritt

Sobald Patricia „Master-Karussell v1" fertig hat:
1. Sag Claude: „Master ist fertig, probier den Klon-Flow"
2. Claude liest das Template (`get-design-content richtexts`), findet alle Platzhalter
3. Claude macht einen Test-Klon mit dem vorhandenen Briefing aus `outputs/samples/karussell-v3-preview.html`
4. Wenn Klon-Output passt → Integration in `/karussell` Command + Montags-Engine

Ab dann: Briefing rein, Canva-Design raus, vollautomatisch.
