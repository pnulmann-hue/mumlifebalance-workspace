# /kurse-sync — Patricias Kurs-Wissen aktualisieren

Wenn Patricia einen neuen Kurs in `context/Kurse/aktuelle kurse/` ablegt (oder bestehende Kurse um neue Lektionen erweitert), ruft sie diesen Command auf. Claude synct die neue Expertise in `context/patricia-expertise.md`.

---

## Ablauf

### Schritt 1: Bestandsaufnahme

1. Lies `context/patricia-expertise.md` (Teil 1 + 2).
2. Scanne den Ordner `context/Kurse/aktuelle kurse/` auf Unterordner.
3. Liste alle Kurse auf, die du in der expertise.md **nicht** findest (neue Kurse) UND alle Kurse, die **zusätzliche Lektionen** haben (mtimes prüfen — wenn neuer als das letzte Update von expertise.md, neu).

### Schritt 2: Nachfrage bei Patricia

Zeige ihr:
- Welche neuen Kurse gefunden wurden (Liste)
- Welche bestehenden Kurse neue Lektionen haben
- Wie viele Transkripte insgesamt analysiert werden müssten

Frage: „Soll ich alle durchgehen, oder soll ich einen priorisieren?"

### Schritt 3: Analyse pro neuem Kurs

Nutze einen **Explore-Agent** für jede Kurs-Analyse (parallel wenn mehrere). Prompt-Template:

```
Analysiere den Kurs `[Kursname]` in `context/Kurse/aktuelle kurse/[Kursname]/Transkripte/`.
Alle .txt-Files durchgehen (nicht .vtt).

Extrahiere:

TEIL 1 — Lehrinhalte:
- Kern-Claim / Versprechen
- 3-5 zentrale Methoden/Konzepte mit Namen
- Typische Beispiele/Stories
- Konkrete Tipps/Regeln/Frameworks

TEIL 2 — Brand Voice:
- Neue typische Phrasen (falls in Patricias Expertise-Datei noch nicht vorhanden)
- Neue Metaphern
- Neue Beispiel-Situationen

Liefere max. 800 Wörter Synthese. Zitate wo möglich.
```

### Schritt 4: Integration in `patricia-expertise.md`

Erweitere die Datei:
- **Teil 1** um den neuen Kurs (als neues `### Kurs N: Name` mit den extrahierten Inhalten)
- **Synthese-Tabelle** aktualisieren wenn neue gemeinsame Konzepte auftauchen
- **Teil 2** nur ergänzen wenn WIRKLICH neue Sprachmuster auftauchen (nicht Duplikate)

### Schritt 5: Bestätigung

Zeige Patricia:
- Welche neuen Methoden/Konzepte dazugekommen sind (kurze Liste)
- Welche neuen Phrasen/Metaphern jetzt im System sind (falls neue)
- Link zur aktualisierten expertise.md

### Schritt 6: Memory aktualisieren

Wenn neue zentrale Methoden dazukommen, ergänze `memory/project_content-engine.md` mit den neuen Kurs-Namen.

---

## Regeln

1. **Immer backup machen** vor dem Write: Kopiere die alte `patricia-expertise.md` nach `context/_archiv/patricia-expertise-YYYY-MM-DD.md` falls Rollback nötig.
2. **Keine Dubletten** — wenn eine Methode/Phrase schon in expertise.md steht, nicht nochmal hinzufügen.
3. **Quelle zitieren** bei jeder neuen Methode (Kurs-Name + Lektion-Nummer).
4. **Patricias Sprache bewahren** — Extrahiere ihre ORIGINAL-Zitate, nicht umformulieren.
5. **Speed**: Bei einem einzelnen neuen Kurs soll der Command in <5 Minuten durch sein.

---

$ARGUMENTS
