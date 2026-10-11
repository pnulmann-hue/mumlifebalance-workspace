"""
Macht die Kurs-Handouts aus Google Drive auffindbar — als Register, nicht als Kopie.

`fremdwissen-indexieren.py` erfasst die **PDFs** aus `reference/` (1'917
Wegweiser). Die Google-Docs-Handouts derselben Kurse liegen aber in Drive und
waren bisher nur ueber ihren Dateinamen zu finden. Wer „Preisanker" suchte, fand
nichts — obwohl es in einem der Cheatsheets steht.

🚨 **Wegweiser, kein Inhalt.** Je Abschnitt steht hier die Ueberschrift und eine
kurze Zeile zum Wiedererkennen, dazu der Link. Damit findet Patricia die Stelle
und schlaegt sie im Original nach, so wie man ein Buchregister benutzt. Ganze
Absaetze gehoeren nicht hierher — das waere eine Kopie fremder Arbeit, und das
Repo ist oeffentlich.

🚨 **Alles hier ist als fremd gekennzeichnet** und erscheint im Cockpit orange
umrandet. Was hier steht, darf nie in einem Kundendokument landen.

Die Daten kommen ueber den Drive-Connector herein (`read_file_content`) und
werden hier eingetragen; ein Skript kommt an Drive nicht heran.

Aufruf:
  python scripts/cockpit/fremdwissen-drive.py [zielordner]
"""
import json
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
DOC = "https://docs.google.com/document/d/%s/edit"
DATEI = "https://drive.google.com/file/d/%s/view"
BLATT = "https://docs.google.com/spreadsheets/d/%s/edit"

# So kurz, dass es ein Wegweiser bleibt und keine Kopie wird.
ZEILE = 110

# --------------------------------------------------------------------------
# Die Dokumente.  titel -> (link, [(abschnitt, erkennungszeile), …])
# --------------------------------------------------------------------------
DOKUMENTE = {}


def dok(titel, link, abschnitte):
    DOKUMENTE[titel] = (link, abschnitte)


dok("Storytelling-Checkliste", DOC % "1lhetSSXTJHFnHpntUBZg4Qng6b1kjo_h-UGd5YppfFA", [
    ("1. Fang mit einem Knall an", "Hook oder Szene zuerst, klingen wie eine Sprachnachricht statt wie eine Vorlesung"),
    ("2. Sprich eine Person an", "durchgehend du statt ihr, Ton wie unter Freundinnen"),
    ("3. Werde visuell konkret", "Uhrzeit, Ort, Geräusch, Gefühl — plus Vergleiche und Metaphern"),
    ("4. Rhythmus", "kurze und lange Sequenzen mischen, Formate und Tonlage wechseln"),
    ("5. Serien für Bindung", "wiederkehrende Formate als Routine, Erwartung aufbauen"),
    ("6. Persönlichkeit statt Fachsprech", "eigene Sprachmuster, echte Erlebnisse"),
    ("7. Interaktion einbauen", "Umfrage, Quiz, Schieber — konkrete Fragen statt allgemeiner"),
    ("8. Selbstbewusst auftreten", "Haltung zeigen, Leaderin statt Bitte-buch-mich"),
    ("9. Verkauf als natürlicher Teil", "Story führt zum Produkt, Alltag mit Nutzen verknüpfen"),
])

dok("Hook-Checkliste", DOC % "1VmX0zN7tgn3VmG79BrmSfDBez60-rXEImbwvJeCt5Kw", [
    ("Zielklarheit", "spricht die Hook ein konkretes Ziel der Zielgruppe an"),
    ("Neugier und Spannung", "Werkzeug NICHT in der Hook nennen — Ergebnis statt Tool"),
    ("Emotionaler Trigger", "Dringlichkeit, Erleichterung, Erstaunen, Identifikation"),
    ("Struktur und Aufbau", "ein bis zwei knackige Sätze, Zahlen, Vergleiche oder Fragen"),
    ("No-Gos", "kein Clickbait ohne Substanz, keine Buzzwords, kein Allgemeinplatz"),
    ("GPT-Prompt für 20 Hooks", "Lückentext-Prompt, abgestimmt auf Nische und Content-Ziel"),
])

dok("Preisstrategie-Cheatsheet", DOC % "1bsUgKSKJRAsvsHk5PTRiT3SSo4GN6ZtfAmGgx1wYX8k", [
    ("Grundlagen", "Produktpreis ist nicht der persönliche Wert, Mini-Preise können strategisch sein"),
    ("Strategische Preisstruktur", "Staffelung Mini / Mittel / Signature / Gross / 1:1"),
    ("Preislogik", "psychologische Preise, Preisanker setzen, Preis-Wirrwarr vermeiden"),
    ("Kommunikation", "Transformation vor Umfang, Preiserklärung ohne Rechtfertigung"),
])

dok("Feed Content Spickzettel", DOC % "120jrKkupF2VFnsAd4p91Lhw4i4LPFUnViaIZoszRki0", [
    ("Die 3 Formate im Feed", "Reels für Reichweite, Karussells für Vertrauen, Rest nur ergänzend"),
    ("Instagram Storys", "täglich etwas, nicht täglich sprechen; Untertitel von Hand statt automatisch"),
    ("Story-Aufbau", "Einleitung mit Hook, Hauptteil als Story, Schluss mit CTA und Link"),
    ("Die Beitragsarten P I E", "Persönlichkeit, Inspiration, Expertise — gleichmässig verteilt"),
    ("Was guten Content ausmacht", "Problemlösung, Story first, kein Hochglanz, Verbindung vor Perfektion"),
])

dok("So kommst du auf Produktideen", DOC % "17KChMPofX-tR82SekFSKeiVpCq215fOUUy-XRxfBeoE", [
    ("1. Content-Analyse", "was läuft gut — daraus einen Mini-Kurs schneiden"),
    ("2. Community-Feedback", "gezielte Story-Fragen nach Herausforderungen und Wünschen"),
    ("3. Transformation splitten", "grosse Kurse zerlegen, 1:1 in Kurs oder Template wandeln"),
    ("4. Eigene Routinen dokumentieren", "was du täglich tust, als Mini-Kurs oder Checkliste verpacken"),
    ("5. Das nächste Level denken", "was braucht jemand NACH dem aktuellen Produkt"),
    ("Reflexionsfragen und Action-Step", "fünf Fragen, dann fünf Produktideen notieren"),
])

dok("Prompts für KI-Tools", DOC % "1Qd9xfkhxc5l00ioNT4jLwbBVhlw_da1DnX6eMwJYIKw", [
    ("Prompt: Tool als Artifact zum Testen", "HTML-Tool direkt in Claude, ohne Backend"),
    ("Prompt: Tool als Netlify-ZIP", "Dateistruktur, netlify.toml, Function mit API-Key aus der Umgebung"),
    ("Technische Fallen", "CORS, Content-Type-Header, kein web_search, Retry bei 529 und 503"),
])

dok("Checkliste: Macht dein Content den Unterschied",
    DOC % "19idty_Z4g-f2YDEqngrWdTkZqLa-8W-4yx4k0vo65uY", [
    ("Mehrwert", "hilfreiche Info oder Aha-Moment, und zeigt der Beitrag wie Zusammenarbeit aussieht"),
    ("Klarheit und Catchiness", "Mehrwert auf den ersten Blick, Botschaft in drei Sekunden erfassbar"),
    ("Relevanz für die Zielgruppe", "echtes Problem, und die Sprache der Zielgruppe statt der eigenen"),
    ("Story und Persönlichkeit", "echte Person statt nur Textgrafiken, eigene Haltung sichtbar"),
    ("Transformation und Lösung", "Brücke von Problem A zu Lösung B, Glaubenssatz auflösen"),
    ("Kontext und Verständlichkeit", "konkret und realistisch umsetzbar, und warum gerade jetzt"),
])

dok("Checkliste: So baust du deine Beiträge auf",
    DOC % "1Y3Ng0trZScKWdwZ4XMSE2yCdAFWo-UoGKxWKsN-Ovqk", [
    ("Cover-Slide", "kurze Headline mit Zahl oder Ergebnis, Werkzeug NICHT nennen, Schrift lesbar"),
    ("Einleitung auf Slide 2", "warum relevant, persönlicher Einstieg, zwei bis drei Sätze"),
    ("Mehrwert-Slides", "drei bis fünf Punkte, je Punkt eine Slide, Bulletpoints statt Fliesstext"),
    ("Letzte Slide als CTA", "Kommentar-Stichwort oder Link, klare Aufforderung"),
    ("Caption", "nicht das Karussell wiederholen — Story, Kundenbeispiel oder ein zusätzlicher Schritt"),
])

dok("Umsetzungs-Checkliste: Sichtbarkeit ohne Werbebudget",
    DOC % "1zPUyiyZszQdRNoBtaMGuAu9p5MAOrFD1OIv5oa922uk", [
    ("Reels gezielt nutzen", "Hook in sieben Sekunden, klarer CTA, Untertitel nur im Reel nicht in der Story"),
    ("Interaktion und Community-Nähe", "bei grossen und gleich grossen Accounts kommentieren, DMs als Gespräch"),
    ("Smarte Formate und Kooperationen", "Mini-Challenges in der Story, Live-Formate mit anderen"),
    ("Aktiv in anderen Netzwerken", "Facebook-Gruppen, Pinterest und YouTube zur Recherche, Threads testen"),
    ("Reminder", "Sichtbarkeit ist nicht Reichweite, sondern Menschen erreichen denen du heute hilfst"),
])

dok("Verkaufs-Checkliste: jeden einzelnen Tag verkaufen",
    DOC % "1t5vJlLSvR2xqsfryTHbaYGElsm_xp7ShnEM85Eezvbs", [
    ("Story-Verkäufe täglich", "mindestens eine Story pro Tag mit klarem CTA, auch bei wenig Energie"),
    ("Feedbeiträge mit Verkaufspotenzial", "jeder Beitrag endet mit Aufforderung, Konversion über Kommentare"),
    ("Automatisierung", "ManyChat übernimmt Kommentare und DMs"),
    ("Mehrstufig verkaufen", "Verkaufen als Prozess über Story, Feed, Mail, Podcast, Ads"),
    ("Über Mini- und 0-Euro-Produkte verkaufen", "Mini-Trainings als Sprungbrett und Vertrauensaufbau"),
    ("Story-Interaktion", "Quiz, Fragen, Umfragen — und persönlich auf Antworten reagieren"),
    ("Kommentar- und DM-Engagement", "kein Verkaufston, Gesprächsaufbau — Beziehungspflege treibt Verkäufe"),
    ("Kontinuierliche Präsenz", "nur wer präsent ist, bleibt im Kopf"),
])

dok("Wiederkehrendes Einkommen — Strategien im Überblick",
    DOC % "1MsONF4ZlzDhYB5INSoUq-_f0764cbRAmb3ymm--Z_cg", [
    ("Evergreen-Produkte verkaufen", "jederzeit buchbar, Verkauf automatisiert, keine Live-Elemente"),
    ("Funnel nutzen", "automatisiertes Mailsystem mit Verkaufslogik, Webinar als Einstieg"),
    ("Produkte logisch verknüpfen", "Upsells und Downsells nach dem Kauf, nächster Schritt automatisch"),
    ("Attraktive Ratenzahlungen", "Raten nicht überteuert, flexible Optionen, planbares Einkommen"),
    ("Membership oder Abo", "niedrigschwelliger Einstieg, mehrere Stufen, Schnupperphase"),
    ("Weiterentwicklung nach dem 1:1", "Anschluss-Angebot früh kommunizieren, 1:1 mit Membership verzahnen"),
])

dok("Produktkommunikation — Checkliste",
    DOC % "1eZcVztSARWxzIH-oN6DsVDdslVlTktcM_SHDYx0kOQ8", [
    ("Klarheit und Zielgruppe", "für wen, welches zentrale Problem, welches konkrete Ergebnis"),
    ("Nutzen statt Merkmale", "nicht fünf Videos und zwei PDFs, sondern was sich im Leben ändert"),
    ("Sprache und Verständlichkeit", "keine Begriffe aus der eigenen Bubble, alltagstauglich statt akademisch"),
    ("Emotionale Ansprache", "bildhafte Sprache, konkrete Vision die Verlangen auslöst"),
    ("Spezifisch statt vage", "drei Reels in drei Minuten statt viele Reels — Zahlen und Beispiele"),
    ("Emotional plus rational", "Wünsche ansprechen und zugleich Inhalte und Preis nennen"),
])
dok("Anleitung zur Erstellung von Mini-Kursen",
    DOC % "1Uf0rEHMNmCn18RekLTXfPvk1Lv84dr9TuCCAXeT1QAA", [
    ("Besonderheiten von Mini-Kursen", "spezifisch statt allgemein, ein schnelles konkretes Ergebnis, Low Price ohne Launch"),
    ("1. Zielgruppe analysieren", "Herausforderung, Ziel, und die Stationen dazwischen"),
    ("2. Mini-Kurs-Idee definieren", "der Kurs behandelt EINE Zwischenstation auf dem Weg zum Ziel"),
    ("3. Ideenquellen", "eigene Expertise, andere Anbieter, Community befragen, KI-Prompt"),
    ("4. Thema verfeinern und prüfen", "spezifisch genug, hoher Nutzen, zahlt jemand dafür, passt es zur Positionierung"),
    ("Typische Fehler", "Thema zu allgemein, zu viel Wissen in einem Kurs, kein Anschlussprodukt"),
])

dok("Content-Ideen entwickeln — Spickzettel",
    DOC % "1AWZcR1e-VG8WxChFZHkeHxJ2RLuXmBqWarGDHMmsgBA", [
    ("Was Grundpfeiler sind", "nicht was kann ich gut, sondern was muss die Community verstehen um zu buchen"),
    ("Übung: die 5 Grundpfeiler finden", "Ziel der Kundin, Hürden davor, was das Angebot abdeckt, Themenblöcke bilden"),
    ("Beispiele für Grundpfeiler", "je drei Beispielsätze für Business-Coach, Mentorin für Mütter, Schlaf-Coach"),
    ("Grundpfeiler wiederverwenden", "dieselben Themen für Reels, Karussells, Stories und Mails"),
    ("Inhalte anderer nutzen", "quer denken statt kopieren — aus Hundetraining wird Content-Routine"),
    ("Deine Geschichte als Content", "welche Hürde gemeistert, was verworfen, was heute anders"),
])

dok("Checkliste: Verbindung aufbauen",
    DOC % "1SZ-3gTB0LqvbAbmF_18iuH7iK1EjzeZdreQd1tlyJuA", [
    ("Dienen statt verkaufen", "aus der Perspektive der Community posten, mit dem Ziel zu helfen"),
    ("Mehr geben als erwartet", "Reziprozität — Mini-Trainings, Vorlagen, Blick hinter die Kulissen"),
    ("Interaktion in Stories", "täglich Sticker, und auch ganz Persönliches teilen"),
    ("Mini-Kurse", "so gut liefern, dass die Community mehr will"),
    ("Kommentare und DMs", "auf jeden Kommentar reagieren, persönlich antworten, Small Talk ist okay"),
    ("Konversation statt Pitch", "Beziehung wachsen lassen, erst später verkaufen"),
    ("Gamification", "Quiz und Fun-Facts, Insider-Übungen als Community-Kitt"),
    ("Kontaktpunkte streuen", "Feed, Story, Mail, Podcast, Ads — jeder Punkt darf verkaufen"),
    ("Warum das alles", "Verbindung ist die Brücke vom Folgen zum Buchen"),
])

dok("Vermeide diese Wörter in Reels",
    DOC % "1tFsh3duP_mpff27mT3w10-JPJZcWNIJOFMgOADrEr64", [
    ("Mindset- und Persönlichkeits-Buzzwords", "Klarheit, Potenzial, Alignment — niemand sieht ein Bild dazu"),
    ("Emotionale Sammelbegriffe", "Angst, Stress, Überforderung ohne konkrete Situation dahinter"),
    ("Business- und Erfolgs-Buzzwords", "Sichtbarkeit, Reichweite, skalieren, Positionierung"),
    ("Unspezifische Zustände", "besser fühlen, selbstbewusster sein, dein Leben verändern"),
    ("Unspezifische Zeit- und Mengenangaben", "oft, viele, regelmäßig, bald — statt einer Zahl"),
    ("Unspezifische Verben", "verbessern, optimieren, transformieren, entwickeln"),
    ("Die goldene Regel", "wenn man es nicht filmen kann, ist es zu schwammig"),
    ("Nominalisierungen", "die Umsetzung, die Steigerung — machen Sprache schwer"),
    ("Passive Formulierungen", "es wird empfohlen — statt: poste drei Reels pro Woche"),
    ("Before/After-Beispiele", "je ein schlechter und ein guter Satz nebeneinander"),
])

def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    eintraege, zulang = [], []
    for titel, (link, abschnitte) in DOKUMENTE.items():
        for abschnitt, zeile in abschnitte:
            if len(zeile) > ZEILE:
                zulang.append((titel, abschnitt, len(zeile)))
            eintraege.append({
                "d": link,
                "t": titel + " · " + abschnitt,
                "a": zeile,
                "b": "Fremd · Drive",
            })

    if zulang:
        for t, a, n in zulang:
            print("  zu lang (%d Zeichen): %s · %s" % (n, t, a))
        sys.exit("Erkennungszeilen über %d Zeichen — das wird eine Kopie "
                 "statt eines Wegweisers." % ZEILE)

    heute = date.today().isoformat()
    (ziel / "fremd-drive.json").write_text(json.dumps(
        {"items": eintraege, "stand": heute}, ensure_ascii=False),
        encoding="utf-8")

    print("  %d Dokumente · %d Wegweiser" % (len(DOKUMENTE), len(eintraege)))
    print("\nAbgelegt in: %s" % (ziel / "fremd-drive.json"))


if __name__ == "__main__":
    main()
