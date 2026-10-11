# -*- coding: utf-8 -*-
"""Erzeugt je Skill eine Anleitung.md (Kundendokument) + eine interne Weitergabe-Übersicht."""
import os, io

ROOT = r"C:\Users\pnulm\Desktop\Mein Business"
SKILLS = os.path.join(ROOT, ".claude", "skills")

DATEI = {
 "brand-voice.md": "Deine Stimme: wie du schreibst, welche Wörter du nie benutzt, zwei bis drei echte Textbeispiele von dir.",
 "patricia-vollprofil.md": "Wer du bist: Werte, deine Geschichte, für wen du arbeitest, was du niemals sagen würdest.",
 "business-info.md": "Deine Positionierung: was du anbietest, für wen, was dich unterscheidet.",
 "patricia-expertise.md": "Dein Fachwissen: woraus du Mehrwert schöpfst, damit nichts erfunden wird.",
 "patricia-freebies.md": "Deine Gratis-Angebote mit Inhalt — damit im Text darauf Bezug genommen werden kann.",
 "active-funnels.json": "Deine aktiven Angebote und Freebies mit Link, Preis und Stichwort.",
 "hook-framework.md": "Deine Hook-Regeln: welche Einstiege funktionieren, welche verboten sind.",
 "caption-formeln.md": "Deine Caption-Baupläne und Handlungsaufforderungen.",
 "ki-phrasen-blackliste.md": "Formulierungen, die nach KI klingen und deshalb nie vorkommen dürfen.",
 "manychat-keywords.md": "Deine Stichwörter und was sie auslösen.",
 "content-formel-5-typen.md": "Deine Beitragstypen und wie sie sich über die Woche verteilen.",
 "job-saeulen.md": "Welchen Job ein Beitrag hat: Autorität, Geschichte, Reichweite oder Verkauf.",
 "reels-framework.md": "Deine Reel-Regeln: Länge, Aufbau, was in den ersten drei Sekunden passiert.",
 "reichweitenherz-voice-layer.md": "Sprachliche Kniffe, die deine Texte lebendig machen.",
 "hook-master-liste.md": "Dein Vorrat an bewährten Roh-Hooks zum Zuschneiden.",
 "meal-planning-bot.md": "Dein Koch-Briefing: Personenzahl, Vorlieben, Unverträglichkeiten, Einkaufsladen.",
 "videoschnitt-regeln.md": "Deine Schnittregeln: welcher Take gewinnt, wie viel Luft vor einem Satz, was unantastbar ist.",
}

S = {}
def add(n, titel, vogel, kann, dateien, dienste, skripte, ersetzen, aufruf, ampel, grund):
    S[n] = dict(titel=titel, vogel=vogel, kann=kann, dateien=dateien, dienste=dienste,
                skripte=skripte, ersetzen=ersetzen, aufruf=aufruf, ampel=ampel, grund=grund)

MARKE = ["brand-voice.md", "ki-phrasen-blackliste.md"]
PROFIL = ["patricia-vollprofil.md", "business-info.md"]

add("caption", "Caption-Schreiber",
 "Schreibt dir eine fertige Instagram-Caption in deiner Stimme — mit Zeitanker, einer echten Zahl und genau einer Handlungsaufforderung.",
 ["Caption aus einer groben Idee oder einem Hook bauen", "Bestehende Caption überarbeiten", "Handlungsaufforderung auf dein Stichwort setzen"],
 MARKE + ["caption-formeln.md", "patricia-expertise.md", "patricia-freebies.md"], [], [],
 ["In `brand-voice.md` deine eigene Stimme und deine Wortverbote eintragen",
  "In `caption-formeln.md` deine Caption-Baupläne hinterlegen",
  "Dein Kommentar-Stichwort setzen — im Skill steht als Beispiel eines von mir"],
 "Schreib mir eine Caption zu diesem Hook: ...", "gelb",
 "Enthält meine Beispiel-Stichwörter und Verweise auf meine Kontextdateien.")

add("hooks", "Hook & Kundensprache",
 "Alles über die erste Zeile an einem Ort: wie deine Wunschkundin denkt, welche Formeln bei ihr funktionieren, welche gesperrt sind, und der Check, durch den jeder Hook muss.",
 ["Zehn Hooks über mehrere Angles zu einem Thema", "Bewusstseinsstufe bestimmen und den Hook danach ausrichten",
  "22 Formeln und 10 Reveal-Frameworks zuschneiden", "Bestehende Hooks prüfen und reparieren",
  "Hook-Muster rotieren, damit nicht alles gleich klingt"],
 ["kern-painpoint.md", "hook-master-liste.md", "reichweitenherz-voice-layer.md", "ki-phrasen-blackliste.md"], [],
 ["Das Prüfskript scripts/content/hook-pruefen.py"],
 ["`kern-painpoint.md` mit dem Schmerz deiner eigenen Zielgruppe füllen — das ist das Herz",
  "Themen-Pool und Antagonist-Figuren auf deine Nische umschreiben",
  "Die Testdaten im Skill sind meine — deine eigenen erst sammeln, dann eintragen",
  "Das Prüfskript mitkopieren und die Wortlisten darin anpassen"],
 "Mach mir zehn Hooks zum Thema ... für ...", "rot",
 "Enthält zugekauftes Kurswissen mehrerer Coaches und meine eigenen Testzahlen.")

add("content", "Content-Maschine",
 "Schreibt den kompletten Content für eine Woche oder einen Monat — Marktcheck, Hooks, Reels, Karussells, Captions, Design-Bauplan und den passenden Story-Bogen. Liest deine Planung und baut alles darauf auf.",
 ["Marktcheck: was beschäftigt deine Zielgruppe gerade, mit Zitat und Quelle",
  "Hooks über den Hook-Skill, geprüft und auf deine Sprache zugeschnitten",
  "Fertige Reels und Karussells samt Captions",
  "Story-Bogen, der an die Beiträge anknüpft",
  "Dreh-Liste zum Abfilmen an ein, zwei Tagen (beim Monat)",
  "Läuft auf Wunsch automatisch als geplanter Auftrag"],
 MARKE + PROFIL + ["caption-formeln.md", "patricia-expertise.md", "patricia-freebies.md",
                   "active-funnels.json", "job-saeulen.md", "content-formel-5-typen.md"],
 ["Optional: Planungs-Datenbank", "Optional: Auto-Posting-Dienst", "Optional: Messenger für die Benachrichtigung"],
 ["Der Hook-Skill (wird mitgeliefert oder ersetzt)", "Optional: Render- und Schnitt-Programme"],
 ["Alle Kontextdateien mit deinen eigenen Inhalten füllen — ohne sie wird der Output generisch",
  "Deine Angebote und Stichwörter eintragen, sonst wird auf meine verwiesen",
  "Die Ordnerpfade zu deinem Bildmaterial anpassen",
  "Datenbank-Kennungen und Posting-Zugänge ersetzen oder die Abschnitte streichen",
  "Die Testzahlen im Skill sind meine — deine eigenen erst sammeln, dann eintragen"],
 "Bau mir den Content für nächste Woche", "rot",
 "Hängt an meinen Zugängen, Datenbank-Kennungen und Testdaten; stützt sich auf den Hook-Skill mit zugekauftem Kurswissen.")

add("visuals", "Design-Bauplan",
 "Sagt dir Folie für Folie, was in deine Design-Vorlage kommt. Erzeugt selbst keine Bilder — du arbeitest mit deiner Vorlage und echten Fotos.",
 ["Bauplan für Karussell-Folien", "Cover-Vorschlag", "Standbild für ein Reel"],
 [], ["Ein Design-Programm deiner Wahl"], [],
 ["Beim ersten Aufruf fragt der Skill nach deinem Marken-Setup: Farben, Schriften, Vorlagen. Einmal beantworten."],
 "Mach mir den Bauplan für ein Karussell zu ...", "gruen",
 "Fragt das Marken-Setup selbst ab, keine privaten Daten fest verdrahtet.")

add("karussell", "Karussell-Assistent",
 "Plant, baut und repariert Instagram-Karussells: Folien-Plan, Hooks nach deinen Regeln, Prüfung ob dein Feed-Rhythmus noch stimmt.",
 ["Karussell-Konzept aus einer Idee", "Aus vorhandenem Material ein Karussell bauen", "Zehn Hook-Varianten",
  "Kritik an einem bestehenden Karussell mit drei Fixes", "Wochenplan mit mehreren Ideen"],
 MARKE + PROFIL + ["hook-framework.md", "caption-formeln.md", "job-saeulen.md", "content-formel-5-typen.md", "active-funnels.json"],
 ["Optional: Planungs-Datenbank", "Optional: Auto-Posting-Dienst"], [],
 ["Alle Kontextdateien mit deinen Inhalten füllen",
  "Datenbank-Kennungen im Skill durch deine eigenen ersetzen oder den Abschnitt streichen",
  "Deine Feed-Optik beschreiben: Farben, wann Foto, wann Vorlage"],
 "Mach mir ein Karussell zum Thema ...", "gelb",
 "Enthält meine Datenbank-Kennungen und meine Feed-Regeln.")

add("reels", "Reel-Assistent",
 "Plant Reels mit sekundengenauem Briefing: Hook, Bildfolge, was du genau sagst, Caption und Handlungsaufforderung.",
 ["Reel-Konzept aus einer Idee", "Aus vorhandenen Clips die Schnittreihenfolge", "Zehn Hook-Varianten",
  "Kritik an einem Reel mit drei Fixes", "Wochenplan mit mehreren Reel-Ideen"],
 MARKE + PROFIL + ["reels-framework.md", "hook-framework.md", "caption-formeln.md", "content-formel-5-typen.md"], [], [],
 ["Kontextdateien mit deinen Inhalten füllen",
  "In `reels-framework.md` deine Posting-Zeiten und deine Hashtags eintragen"],
 "Mach mir ein Reel zum Thema ...", "gelb",
 "Verweist auf mein Vollprofil und meine Reel-Regeln.")

add("story", "Story-Begleiter",
 "Täglicher Begleiter für Instagram-Stories. Jede Sequenz bekommt eine Handlungsaufforderung, und über die Woche werden alle Käufertypen bedient.",
 ["Tagesplan mit drei bis fünf Slides", "Kompletter Verkaufstag während eines Launches", "Aus einer rohen Idee eine Story-Struktur",
  "Ein-Slide-Tag für wenig Zeit", "Story-Serie über mehrere Tage"],
 MARKE + PROFIL + ["caption-formeln.md", "active-funnels.json", "content-formel-5-typen.md"], ["Optional: Planungs-Datenbank"], [],
 ["Kontextdateien mit deinen Inhalten füllen",
  "Deine Angebote in `active-funnels.json` eintragen",
  "Datenbank-Kennung im Skill ersetzen oder den Abschnitt streichen"],
 "Was poste ich heute in die Story?", "gelb",
 "Enthält meine Datenbank-Kennung und Verweise auf mein Bildmaterial.")

add("blog", "Blog-Schreiber",
 "Schreibt einen suchmaschinen-optimierten Blogartikel zu deinem Monatsthema — und daraus gleich Stories, Karussell, Reel und Newsletter.",
 ["Artikel-Konzept", "Kompletter Artikel", "Bestehenden Artikel aktualisieren", "Aus einem Artikel weiteren Content ableiten"],
 MARKE + PROFIL + ["hook-framework.md", "active-funnels.json"], ["Website mit Blog", "Optional: Planungs-Datenbank"], [],
 ["Kontextdateien füllen",
  "Deine Website-Adresse und deine internen Links im Skill ersetzen",
  "Datenbank-Kennungen ersetzen oder streichen"],
 "Schreib mir den Blogartikel zum Monatsthema", "gelb",
 "Enthält meine Domain, meine internen Links und Datenbank-Kennungen.")

add("salespage", "Sales-Page-Texter",
 "Führt ein Interview zu deinem Angebot und liefert dir dreizehn fertige Textblöcke zum Einsetzen in deine Verkaufsseite.",
 ["Interview zu Angebot, Zielgruppe, Verwandlung, Modulen", "Dreizehn Textblöcke zum Kopieren", "Häufige Fragen samt Antworten"],
 PROFIL, ["Ein Checkout-Anbieter deiner Wahl"], [],
 ["`patricia-vollprofil.md` durch dein eigenes Profil ersetzen",
  "Im Skill-Text wird eine fremde Methodik namentlich genannt — vor der Weitergabe entfernen"],
 "Bau mir die Sales-Page für mein Angebot ...", "rot",
 "Nennt im Titel eine fremde Methodik namentlich. Muss vor der Weitergabe raus.")

add("produkt", "Produkt-Entwickler",
 "Begleitet dich von der Produktidee bis zum Launch: Produkttreppe, Validierung, Module, Preis-Staffel, Launch-Kalender, Funnel.",
 ["Produkttreppe über vier Stufen entwerfen", "Idee validieren bevor du sie baust", "Einzelprodukt mit Modulen und Arbeitsblättern",
  "Preis-Staffel", "Launch-Content-Kalender", "Funnel und Verkaufsseite"],
 MARKE + PROFIL + ["patricia-expertise.md", "patricia-freebies.md"], ["Optional: Produkt-Datenbank", "Optional: Design-Programm"], [],
 ["Kontextdateien füllen",
  "Dein Umsatzziel im Skill ersetzen — dort steht meines",
  "Produkt-Datenbank-Kennung ersetzen oder den Abschnitt streichen",
  "Im Skill-Text wird eine fremde Methodik namentlich genannt — vor der Weitergabe entfernen"],
 "Lass uns ein neues Produkt entwickeln", "rot",
 "Enthält mein Umsatzziel, meine Datenbank-Kennungen und eine fremde Methodik namentlich.")

add("funnel", "Funnel-Stratege",
 "Plant und baut komplette Funnel: Leadmagnet, Landingpage, Werbeanzeigen, Mailsequenz, Launch und Auswertung.",
 ["Funnel-Strategie", "Funnel bauen", "Werbeanzeigen mit vorheriger Schmerzpunkt-Analyse", "Launch steuern", "Bestehenden Funnel auswerten"],
 MARKE + PROFIL + ["manychat-keywords.md", "active-funnels.json", "patricia-expertise.md"],
 ["E-Mail-Marketing", "Chat-Automation", "Website", "Checkout-Anbieter"], [],
 ["Alle hinterlegten Zugänge sind meine — du brauchst deine eigenen",
  "`active-funnels.json` komplett durch deine Angebote ersetzen",
  "Alle Listen- und Automations-Nummern im Skill ersetzen"],
 "Lass uns einen Funnel planen", "rot",
 "Hängt komplett an meinen Zugängen und Listen-Nummern.")

add("hormozi", "Copywriting-Doktor",
 "Nimmt einen fertigen Text und überarbeitet ihn nach bekannten Verkaufs-Frameworks — ohne deine Stimme zu zerstören.",
 ["Text diagnostizieren und in zwei Varianten neu schreiben", "Zehn Hook-Varianten", "Angebot auf Wert prüfen",
  "Antwort auf eine Anfrage formulieren", "Langen Text in vier Durchgängen schärfen", "Werbeanzeige bauen", "Landingpage bauen"],
 MARKE + PROFIL + ["hook-framework.md", "caption-formeln.md"], [], [],
 ["Kontextdateien füllen — der Skill braucht deine Stimme, sonst klingt das Ergebnis nach Lehrbuch",
  "Der Skill verweist auf eine Wissensdatei mit zusammengefasster Fremdliteratur. Die gehört nicht mit weiter — ersetze sie durch deine eigenen Notizen."],
 "Überarbeite mir diesen Text: ...", "rot",
 "Stützt sich auf eine Wissensdatei aus fremder Literatur.")

add("monatsplan", "Monats-Strategie",
 "Schnürt einmal im Monat den Strategie-Rahmen: Schwerpunkt, drei Angebote, Hauptbotschaft, Ziele — und plant den Monats-Content vor.",
 ["Vormonat auswerten", "Acht Fragen zum neuen Monat", "Vier-Wochen-Briefing", "Dreh-Liste zum Abfilmen", "Newsletter und Blogartikel des Monats"],
 MARKE + PROFIL + ["content-formel-5-typen.md", "job-saeulen.md", "caption-formeln.md"], ["Optional: Planungs-Datenbank"], [],
 ["Kontextdateien füllen",
  "Datenbank-Kennungen ersetzen oder den Abschnitt streichen",
  "Deine eigenen Ziele eintragen — im Skill stehen meine"],
 "Lass uns den nächsten Monat planen", "gelb",
 "Enthält meine Ziele und Datenbank-Kennungen.")

add("jahresplan", "Jahresplanung",
 "Hält alle Launches, Produkte und Kampagnen eines Jahres in einer Sicht — und warnt, wenn sich zwei Dinge in die Quere kommen.",
 ["Wo stehe ich heute", "Neuen Launch eintragen", "Monatsvorschau", "Konflikte finden"],
 ["active-funnels.json"], ["Optional: Planungs-Datenbank"], [],
 ["Die Jahresdatei wird beim ersten Lauf angelegt — sie startet leer",
  "Datenbank-Kennung ersetzen oder den Abschnitt streichen"],
 "Zeig mir meinen Jahresplan", "gelb",
 "Verweist auf meine Datenbank und meine Jahresdatei.")

add("cockpit", "Morgenbriefing",
 "Gibt dir morgens den Überblick über den Tag und auf Wunsch die Wochen-, Monats- oder Quartalssicht. Ruft bei Bedarf die anderen Skills auf.",
 ["Tagesbriefing", "Wochensicht", "Monatssicht", "Quartalssicht"],
 MARKE + PROFIL + ["active-funnels.json"], ["Planungs-Datenbank", "E-Mail-Marketing"], [],
 ["Alle Datenbank-Kennungen im Skill sind meine — ersetzen",
  "Die Verbindung zum E-Mail-Marketing braucht deinen eigenen Zugang"],
 "Gib mir das Briefing für heute", "rot",
 "Liest meine Datenbanken und meinen E-Mail-Zugang.")

add("wp", "Website-Helfer",
 "Erstellt und aktualisiert Seiten auf deiner Website, lädt Bilder hoch und pflegt Menüs — direkt über die Schnittstelle.",
 ["Seite als Entwurf anlegen", "Bestehende Seite aktualisieren", "Bild hochladen", "Seiten auflisten"],
 ["brand-voice.md"], ["WordPress-Website mit Schnittstellen-Zugang"], ["Kleines Hilfsprogramm zum Ansteuern"],
 ["Deine Domain statt meiner eintragen",
  "Eigenen Zugang anlegen und in einer Zugangsdatei hinterlegen",
  "Deine Markenfarben und Schriften ersetzen"],
 "Leg mir eine Seite für ... als Entwurf an", "rot",
 "Enthält meine Domain und braucht meinen Website-Zugang.")

add("videoschnitt", "Video-Rohschnitt",
 "Du sprichst dein Material in einem Stück in die Kamera, mit Versprechern und Wiederholungen. Der Skill macht daraus den Rohschnitt nach deinen Regeln, setzt Untertitel und Textebenen.",
 ["Material abtippen mit Wortzeitstempeln", "Schnittliste vorlegen und freigeben lassen", "Rohschnitt und Einzelclips",
  "Wortgenaue Untertitel", "Textebene und automatische Zooms"],
 ["videoschnitt-regeln.md"], [], ["Drei Schnitt-Programme, die mitgeliefert werden müssen"],
 ["`videoschnitt-regeln.md` mit deinen eigenen Schnittregeln füllen — das ist das Herz",
  "Die Programme im Ordner `scripts/videoschnitt/` müssen mitkopiert werden",
  "Einmalig die Abhängigkeiten installieren — steht in der README im Programm-Ordner"],
 "Schneide mir das Video in video/input/", "gelb",
 "Braucht die drei Programme mitgeliefert, sonst technisch sauber übertragbar.")

add("handy", "Material-Abholer",
 "Holt neue Fotos und Videos aus einem festen Album auf deinem Handy und sortiert sie ein. Auf dem Handy wird nichts gelöscht.",
 ["Videos und Fotos abholen", "Standbild je Video erzeugen, damit der Inhalt sichtbar ist", "Bericht schreiben, was neu ist"],
 [], ["Handy-Verbindung zum Rechner"], ["Ein Abhol-Programm"],
 ["Den Album-Namen auf deinen ändern",
  "Den Verbindungspfad zum Handy anpassen — meiner ist gerätespezifisch",
  "Das Programm aus `scripts/handy/` mitkopieren"],
 "Hol mein neues Material vom Handy", "gelb",
 "Pfade sind auf mein Gerät zugeschnitten, sonst übertragbar.")

add("mealplan", "Kochassistent",
 "Plant Wochenessen für deine Familie, hilft beim Spontan-Kochen aus dem was da ist und schreibt die Einkaufsliste.",
 ["Wochenplan Mittag und Abend", "Was koche ich aus diesen Zutaten", "Einkaufsliste nach Laden sortiert",
  "Vorkochen und Projekte", "Rezept aus einem Foto archivieren"],
 ["meal-planning-bot.md"], ["Optional: eigene Rezept-Datenbank"], ["Optional: Abfrage-Programm für die Rezept-Datenbank"],
 ["`meal-planning-bot.md` komplett neu schreiben: Personenzahl, Vorlieben, Unverträglichkeiten, dein Einkaufsladen",
  "Die Rezept-Datenbank ist meine und wird nicht mitgeliefert — der Skill funktioniert auch ohne, schlägt dann aber keine Rezepte aus dem Bestand vor"],
 "Mach mir den Wochenplan", "gelb",
 "Braucht ein komplett neues Koch-Briefing. Meine Rezept-Datenbank bleibt hier.")

add("garten", "Gartenassistent",
 "Berater für deinen Garten: was jetzt ansteht, was neben was gepflanzt wird, was in deiner Höhenlage noch geht.",
 ["Was steht diese Woche an", "Beetplanung mit Mischkultur", "Aussaat- und Pflanzzeiten", "Fruchtfolge über Jahre"],
 [], ["Optional: Datenbank für Samen, Beete und Tagebuch"], [],
 ["Standort, Höhenlage und Klima ersetzen — meine Angaben passen nur zu meinem Garten",
  "Deine Beete und Dauerkulturen eintragen",
  "Datenbank-Kennungen ersetzen oder den Abschnitt streichen"],
 "Was steht diese Woche im Garten an?", "gelb",
 "Standortangaben sind meine, der Rest ist übertragbar.")

add("basteln", "Bastel-Assistent",
 "Hält Überblick über dein Bastelmaterial und schlägt nur Projekte vor, die du aus dem vorhandenen Bestand machen kannst.",
 ["Was schenke ich dieser Person", "Material per Foto erfassen", "Anlass rechtzeitig vorbereiten", "Verpackung bauen", "Bastel-Nachmittag planen"],
 [], [], ["Zwei Suchprogramme für den Materialbestand"],
 ["Die Inventar-Dateien sind meine — sie müssen durch deine ersetzt werden, sonst schlägt der Skill Material vor, das du nicht hast",
  "Der Pfad zu deinem digitalen Material muss angepasst werden",
  "Die Anlass-Liste mit Namen und Geburtstagen ist bei mir privat und wird nicht mitgeliefert"],
 "Was kann ich für ... basteln?", "gelb",
 "Inventar und Anlass-Liste sind privat. Die Systematik ist übertragbar.")

add("berufswahl", "Berufswahl-Kompass",
 "Begleitet einen Jugendlichen ohne klare Richtung über Monate. Fragt konsequent nach Tätigkeiten statt nach Berufen und sammelt Beobachtungen auf fünf Achsen.",
 ["Start-Gespräch", "Kurzer Impuls alle ein bis zwei Wochen", "Erlebnis nachbesprechen",
  "Richtungen zeigen, sobald genug Beobachtungen da sind", "Eltern-Auswertung zweimal im Jahr"],
 [], [], [],
 ["Alle Angaben zur Person liegen bei mir in einem privaten Ordner und werden nicht mitgeliefert — du legst sie neu an",
  "Die Bildungswege sind für die Schweiz beschrieben. Für ein anderes Land muss dieser Teil neu geschrieben werden"],
 "Lass uns die nächste Runde Fragen machen", "gelb",
 "Personendaten bleiben hier. Die Bildungswege sind schweizspezifisch.")

# prime: am 04.10.2026 durch /start ersetzt (Herkunft Kursmaterial, keine Anleitung)

add("kurse-sync", "Wissens-Abgleich",
 "Holt neu abgelegtes Kurs-Wissen in deine zentrale Fachwissen-Datei, damit daraus später Content entstehen kann ohne dass etwas erfunden wird.",
 ["Neue Kursinhalte einlesen", "In die Fachwissen-Datei einarbeiten", "Alte Fassung wegsichern"],
 ["patricia-expertise.md"], [], [],
 ["Die Ordnerpfade auf deine Struktur anpassen", "Dateinamen der Fachwissen-Datei anpassen"],
 "Sync mein neues Kurs-Wissen", "gruen",
 "Reine Mechanik, nur Pfade anzupassen.")

add("freebies-sync", "Freebie-Abgleich",
 "Liest deine Gratis-Angebote ein und hält eine zentrale Datei aktuell, damit im Content inhaltlich darauf Bezug genommen werden kann.",
 ["Neue Freebies einlesen", "Inhalte zusammenfassen", "Zentrale Datei aktualisieren"],
 ["patricia-freebies.md", "manychat-keywords.md"], [], [],
 ["Ordnerpfade anpassen", "Deine eigenen Stichwörter eintragen"],
 "Sync meine Freebies", "gruen",
 "Reine Mechanik, nur Pfade und Stichwörter anzupassen.")

AMPEL_TXT = {
 "gruen": "🟢 Kann fast so wie er ist weitergegeben werden",
 "gelb": "🟡 Vor der Weitergabe müssen Platzhalter ersetzt werden",
 "rot": "🔴 Nicht ohne gründliche Bereinigung weitergeben",
}

def anleitung(name, d):
    L = []
    A = L.append
    A("---")
    A("tags: [skill, anleitung]")
    A("---")
    A("")
    A("# %s — Anleitung" % d["titel"])
    A("")
    A("## Was dieser Skill macht")
    A("")
    A(d["vogel"])
    A("")
    A("Konkret kann er:")
    A("")
    for k in d["kann"]:
        A("- %s" % k)
    A("")
    A("## Was du vorher brauchst")
    A("")
    if d["dateien"]:
        A("Der Skill liest dein Hintergrundwissen aus Textdateien. Lege sie in einem Ordner `context/` in deinem Projekt an:")
        A("")
        A("| Datei | Was hineingehört |")
        A("|---|---|")
        for f in d["dateien"]:
            A("| `%s` | %s |" % (f, DATEI.get(f, "Dein Hintergrundwissen zu diesem Thema.")))
        A("")
        A("> Die Dateien dürfen klein anfangen. Lieber drei ehrliche Sätze als eine leere Vorlage — der Skill arbeitet mit dem, was dasteht, und erfindet nichts dazu.")
        A("")
        A("> Die Dateinamen stammen aus meinem eigenen Aufbau. Du darfst sie umbenennen — dann musst du die Namen aber auch in der `SKILL.md` ändern, sonst findet der Skill deine Dateien nicht.")
        A("")
    else:
        A("Nichts. Der Skill fragt dich alles ab, was er wissen muss.")
        A("")
    if d["dienste"]:
        A("**Zugänge, die du brauchst:**")
        A("")
        for s in d["dienste"]:
            A("- %s" % s)
        A("")
    if d["skripte"]:
        A("**Hilfsprogramme, die mitkopiert werden müssen:**")
        A("")
        for s in d["skripte"]:
            A("- %s" % s)
        A("")
    A("## Installation")
    A("")
    A("**Schritt 1 — Ordner kopieren**")
    A("")
    A("Kopiere den kompletten Ordner `%s` an einen dieser beiden Orte:" % name)
    A("")
    A("```")
    A("~/.claude/skills/%s/               <- in jedem Projekt verfügbar" % name)
    A("DEIN-PROJEKT/.claude/skills/%s/    <- nur in diesem einen Projekt" % name)
    A("```")
    A("")
    A("Danach muss es so aussehen:")
    A("")
    A("```")
    A("%s/" % name)
    A("├── SKILL.md      <- das Herzstück, das Claude liest")
    A("└── Anleitung.md  <- diese Datei, nur für dich")
    A("```")
    A("")
    A("Die Datei muss `SKILL.md` heissen und im Ordner mit dem Skill-Namen liegen. Wird daran etwas geändert, findet Claude den Skill nicht.")
    A("")
    A("> Der Ordner `.claude` beginnt mit einem Punkt und ist deshalb oft unsichtbar. Unter Windows blendest du versteckte Elemente im Explorer unter „Ansicht“ ein, am Mac im Finder mit `Cmd + Shift + .`")
    A("")
    A("**Schritt 2 — Claude neu starten**")
    A("")
    A("Schliesse Claude Code komplett und öffne es neu. Skills werden beim Start eingelesen — ohne Neustart taucht der neue Skill nicht auf.")
    A("")
    A("**Schritt 3 — Platzhalter ersetzen**")
    A("")
    for e in d["ersetzen"]:
        A("- %s" % e)
    A("")
    A("## So rufst du ihn auf")
    A("")
    A("Entweder mit Schrägstrich und Namen:")
    A("")
    A("```")
    A("/%s" % name)
    A("```")
    A("")
    A("Oder du beschreibst einfach, was du willst — Claude erkennt selbst, dass dieser Skill passt:")
    A("")
    A("> „%s“" % d["aufruf"])
    A("")
    A("## Wenn etwas nicht klappt")
    A("")
    A("| Was du siehst | Woran es liegt | Was du tust |")
    A("|---|---|---|")
    A("| Skill wird nicht gefunden | Claude wurde nicht neu gestartet | Komplett schliessen und neu öffnen |")
    A("| Skill wird nicht gefunden | Datei heisst nicht genau `SKILL.md` | Umbenennen, Gross- und Kleinschreibung zählt |")
    A("| Skill wird nicht gefunden | Ordner liegt eine Ebene zu tief | `SKILL.md` muss direkt in `%s/` liegen |" % name)
    A("| Antworten klingen generisch | Kontextdateien sind leer | Die Dateien aus „Was du vorher brauchst“ füllen |")
    A("| Er erfindet Zahlen | Kein Fachwissen hinterlegt | Deine echten Zahlen in die Kontextdateien schreiben |")
    A("")
    return "\n".join(L) + "\n"

gruppen = {"gruen": [], "gelb": [], "rot": []}
for name, d in S.items():
    if not os.path.isdir(os.path.join(SKILLS, name)):
        continue  # archiviert (reference/_archiv-skills/)
    p = os.path.join(SKILLS, name, "Anleitung.md")
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(anleitung(name, d))
    gruppen[d["ampel"]].append((name, d["titel"], d["grund"]))

U = ["---", "tags: [skill, uebersicht]", "---", "",
     "# Skills — Weitergabe-Status", "",
     "Interne Übersicht. **Gehört nicht mit in ein Kundenpaket.**", "",
     "Je Skill liegt im Ordner eine `Anleitung.md` — das ist das Kundendokument.", "",
     "Die Einstufung sagt, wie viel Bereinigung ein Skill braucht, bevor er das Haus verlässt.", ""]
for amp in ("gruen", "gelb", "rot"):
    U.append("## %s" % AMPEL_TXT[amp])
    U.append("")
    U.append("| Skill | Was es ist | Warum diese Einstufung |")
    U.append("|---|---|---|")
    for n, t, g in sorted(gruppen[amp]):
        U.append("| `%s` | %s | %s |" % (n, t, g))
    U.append("")
U += ["## Nicht in dieser Liste", "",
      "Die sieben Skills `chatgpt-ads`, `copywriting`, `facebook-ads`,",
      "`ki-salespage`, `minikurs-salespage`, `signature-kurs-salespage` und `skill-salespage`",
      "sind **zugekauftes Fremdmaterial**. Sie bekommen keine Weitergabe-Anleitung — eine",
      "Weitergabe wäre eine Weiterverteilung fremder Arbeit.", ""]
with io.open(os.path.join(SKILLS, "_WEITERGABE-STATUS.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(U))

print("Anleitungen geschrieben: %d" % len(S))
for amp in ("gruen", "gelb", "rot"):
    print("  %-6s %d" % (amp, len(gruppen[amp])))
fehlt = sorted(set(os.listdir(SKILLS)) - set(S) - {"_WEITERGABE-STATUS.md"})
print("ohne Anleitung: %s" % ", ".join(fehlt))
