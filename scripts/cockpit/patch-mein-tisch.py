"""Mein Tisch — die neue Startseite des Cockpits (08.10.2026).

Patricia am 08.10.2026, nach dem Screenshot eines „CEO Table" aus einem
fremden Kurs: *„Visuell gefällt mir das mega"* · *„logisch meine farben
einbauen. eine übersicht mit aufgaben business und vielleicht privat? dann
hat sie eine übersicht mit all ihren KI Helfern ... die sie direkt abrufen
kann"* · *„ne wir nennen sie einfach pia"* · Cover-Vorschau *„das muss nicht
auf die startseite"*.

Übernommen ist der **Aufbau**, nicht die Optik der Vorlage: dunkler Verlauf in
ihren Farben (Dunkelblau → Petrol), helle Karten, kleine Etiketten, Pillen-
Knöpfe, alles auf einem Bildschirm. Vier Karten plus eine Helferinnen-Leiste:

| Karte | Daten | gehört |
|---|---|---|
| PIA | fragt `sample`, trägt Aufgaben/Termine selbst ein | Verlauf nur lokal |
| Aufgaben Business/Privat | `daten/aufgaben`, neues Feld `bereich` | Patricia |
| Kalender + Tag | `daten/termine` (NEU) + Jahresplan + Beiträge + fällige Aufgaben | Patricia |
| Content-Kalender | `alleBeitraege()`, nächste 14 Tage | wie bisher |
| KI-Helferinnen | fest im Code, nach Academy-Säulen | — |

🚨 **`daten/termine` gehört Patricia.** Der tägliche Abgleich darf es nie
schreiben — gehört in die Liste der geschützten Dokumente.

🚨 **PIA führt nur zwei Dinge aus: Aufgabe anlegen, Termin anlegen.** Beides
ist mit einem Klick wieder weg. Sie plant nichts ein, gibt nichts frei und
löscht nichts. Eine Antwort, die nach Erledigung klingt, steht nur da, wenn
der Eintrag wirklich in der Liste liegt.

🚨 **Fällt die neue Seite um, springt die alte ein** (`try/catch` um
`renderTisch`). Eine tote Startseite heisst: Patricia kommt an gar nichts.

    python scripts/cockpit/patch-mein-tisch.py [--datei <pfad>]
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
MARKE = "---------- Mein Tisch (08.10.2026) ----------"

# ---------------------------------------------------------------- Schriften
FONT_ALT = "<title>Mum Life Balance Cockpit</title>\n"
FONT_NEU = (
    "<title>Mum Life Balance Cockpit</title>\n"
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700'
    '&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">\n'
)
VAR_ALT = [
    ('    --display: Georgia, "Iowan Old Style", "Times New Roman", serif;\n',
     '    --display: "Philosopher", Georgia, "Times New Roman", serif;\n'),
    ('    --body: "Trebuchet MS", "Segoe UI", Tahoma, sans-serif;\n',
     '    --body: "Source Sans 3", "Segoe UI", Tahoma, sans-serif;\n'),
]

# ---------------------------------------------------------------- CSS
CSS_ANKER = "</style>\n\n<div class=\"shell\">"
CSS = r"""
  /* ---------- Mein Tisch (08.10.2026) ----------
     Aufbau nach dem „CEO Table", Farben von Mum Life Balance: der Verlauf
     geht von Dunkelblau nach Petrol, die Karten bleiben hell. Lila kommt
     nicht vor — das waren die Farben der Vorlage, nicht ihre. */
  main.ti-main {
    background:
      radial-gradient(1100px 520px at 88% -8%, rgba(220,130,46,0.20), transparent 60%),
      linear-gradient(140deg, #0c1c30 0%, #173a52 50%, #12828c 100%);
    background-attachment: fixed;
    min-height: 100vh;
  }
  .ti-kopf { display: flex; gap: 18px; align-items: flex-end; flex-wrap: wrap;
             color: #fbf8f1; margin-bottom: 20px; }
  .ti-label { display: inline-block; font-size: 11px; letter-spacing: 0.14em;
              text-transform: uppercase; background: rgba(251,248,241,0.14);
              color: #fbf8f1; padding: 4px 11px; border-radius: 999px; }
  .ti-kopf h1 { font-family: var(--display); font-weight: 400; font-size: 34px;
                margin: 10px 0 2px; color: #fbf8f1; line-height: 1.15; }
  .ti-kopf p { margin: 0; opacity: 0.88; font-size: 14px; }
  .ti-zahlen { margin-left: auto; display: flex; gap: 8px; flex-wrap: wrap; }
  .ti-zahl { border: 1px solid rgba(251,248,241,0.28); background: rgba(251,248,241,0.10);
             color: #fbf8f1; border-radius: 999px; padding: 7px 14px; cursor: pointer;
             font-size: 13px; }
  .ti-zahl b { font-family: var(--display); font-size: 17px; margin-right: 5px; }
  .ti-zahl.du b { color: #f3b679; }
  .ti-zahl:hover { background: rgba(251,248,241,0.20); }

  .ti-grid { display: grid; gap: 16px; grid-template-columns: repeat(4, minmax(0, 1fr));
             align-items: start; }
  @media (max-width: 1500px) { .ti-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  @media (max-width: 820px) {
    .ti-grid { grid-template-columns: 1fr; }
    .ti-kopf h1 { font-size: 26px; }
    .ti-zahlen { margin-left: 0; }
  }
  .ti-spalte { display: flex; flex-direction: column; gap: 16px; min-width: 0; }
  .ti-karte { background: var(--surface); color: var(--ink); border-radius: 18px;
              padding: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.18); min-width: 0; }
  .ti-voll { margin-top: 16px; }
  .ti-chip { display: inline-block; font-size: 10.5px; letter-spacing: 0.12em;
             text-transform: uppercase; font-weight: 700; background: #12828c;
             color: #fff; padding: 4px 10px; border-radius: 6px; margin-bottom: 12px; }
  .ti-chip.o { background: #dc822e; }
  .ti-kartekopf { display: flex; align-items: flex-start; gap: 8px; flex-wrap: wrap; }
  .ti-kartekopf .ti-seg { margin-left: auto; }

  .ti-btn { border: 0; border-radius: 999px; padding: 6px 13px; font: inherit;
            font-size: 12.5px; cursor: pointer; background: var(--teal-soft);
            color: var(--teal); font-weight: 600; text-decoration: none;
            display: inline-block; line-height: 1.3; }
  .ti-btn:hover { filter: brightness(0.94); }
  .ti-btn.voll { background: var(--ink); color: var(--surface); }
  .ti-btn.orange { background: var(--orange-soft); color: var(--orange); }
  .ti-btn[disabled] { opacity: 0.45; cursor: not-allowed; }

  .ti-seg { display: inline-flex; flex-wrap: wrap; background: var(--surface-2);
            border-radius: 999px; padding: 3px; gap: 2px; margin-bottom: 12px; }
  .ti-seg button { border: 0; background: none; border-radius: 999px; padding: 5px 11px;
                   font: inherit; font-size: 12.5px; cursor: pointer; color: var(--ink-soft); }
  .ti-seg button[aria-pressed="true"] { background: var(--surface); color: var(--ink);
                   font-weight: 600; box-shadow: 0 1px 3px rgba(0,0,0,0.12); }
  .ti-seg .n { font-size: 11px; opacity: 0.7; margin-left: 3px; }

  /* Kalender */
  .ti-kalkopf { display: flex; align-items: center; justify-content: space-between;
                background: #0c1c30; color: #fbf8f1; border-radius: 12px;
                padding: 8px 10px; margin-bottom: 10px; }
  .ti-kalkopf b { font-family: var(--display); font-weight: 400; font-size: 16px;
                  text-transform: capitalize; }
  .ti-pfeil { border: 1px solid rgba(251,248,241,0.35); background: none; color: #fbf8f1;
              width: 28px; height: 28px; border-radius: 8px; cursor: pointer;
              font-size: 16px; line-height: 1; }
  .ti-kalgrid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px;
                text-align: center; }
  .ti-wt { font-size: 11px; color: var(--ink-soft); padding: 4px 0; }
  .ti-tag { border: 0; background: none; border-radius: 9px; padding: 5px 0 3px;
            font: inherit; font-size: 13px; cursor: pointer; color: var(--ink);
            display: flex; flex-direction: column; align-items: center; gap: 2px;
            font-variant-numeric: tabular-nums; }
  .ti-tag:hover { background: var(--surface-2); }
  .ti-tag.fremd { color: var(--ink-soft); opacity: 0.55; }
  .ti-tag.heute { font-weight: 700; color: var(--teal); }
  .ti-tag.gewaehlt { background: var(--ink); color: var(--surface); }
  .ti-punkte { display: flex; gap: 2px; height: 5px; }
  .ti-punkte i, .ti-legende i { width: 5px; height: 5px; border-radius: 50%;
                                display: inline-block; }
  .pt-termin { background: var(--orange); }
  .pt-beitrag { background: var(--teal); }
  .pt-aufgabe { background: var(--crit); }
  .ti-legende { display: flex; gap: 12px; flex-wrap: wrap; font-size: 11px;
                color: var(--ink-soft); margin-top: 10px; }
  .ti-legende i { margin-right: 5px; vertical-align: middle; }

  /* Zeilen */
  .ti-zeile { display: grid; grid-template-columns: 50px 1fr auto; gap: 8px;
              align-items: baseline; padding: 7px 0; border-top: 1px solid var(--line);
              font-size: 13.5px; }
  .ti-zeile:first-child { border-top: 0; }
  .ti-zeile.klick { cursor: pointer; }
  .ti-zeile.klick:hover .ti-was { color: var(--teal); }
  .ti-zeit { font-size: 12px; color: var(--ink-soft); font-variant-numeric: tabular-nums; }
  .ti-was { min-width: 0; overflow-wrap: break-word; }
  .ti-klein { font-size: 11px; color: var(--ink-soft); }
  .ti-weg { border: 0; background: none; color: var(--ink-soft); cursor: pointer;
            font-size: 14px; padding: 0 4px; border-radius: 6px; }
  .ti-weg.scharf { background: var(--crit); color: #fff; font-size: 11px; padding: 2px 6px; }
  .ti-leer { color: var(--ink-soft); font-size: 13px; font-style: italic; padding: 6px 0; }
  .ti-form { display: grid; gap: 6px; margin-top: 12px; padding-top: 12px;
             border-top: 1px dashed var(--line-strong); }
  .ti-form .reihe { display: flex; gap: 6px; flex-wrap: wrap; }
  .ti-form input, .ti-form select, .ti-feld {
    min-width: 0; background: var(--ground); color: var(--ink);
    border: 1px solid var(--line); border-radius: 9px; padding: 7px 9px; font: inherit;
    font-size: 13px; }
  .ti-form input[type="text"] { flex: 1 1 160px; }
  .ti-form input:focus, .ti-form select:focus, .ti-feld:focus {
    border-color: var(--teal); outline: none; }

  /* Aufgaben */
  .ti-af { display: grid; grid-template-columns: 20px 1fr; gap: 8px; padding: 7px 0;
           border-top: 1px solid var(--line); font-size: 13.5px; align-items: start; }
  .ti-af input { margin-top: 3px; accent-color: var(--teal); }
  .ti-af .meta { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 3px; }
  .ti-af.fertig .txt { text-decoration: line-through; color: var(--ink-soft); }
  .ti-gruppe { font-size: 10.5px; letter-spacing: 0.1em; text-transform: uppercase;
               color: var(--ink-soft); margin: 12px 0 2px; display: flex;
               justify-content: space-between; }
  .ti-gruppe.rot { color: var(--crit); }
  .ti-mini { font-size: 11px; padding: 1px 7px; border-radius: 999px;
             background: var(--surface-2); color: var(--ink-soft); }
  .ti-mini.rot { background: rgba(179,71,51,0.12); color: var(--crit); }
  .ti-mini.hoch { background: var(--orange-soft); color: var(--orange); }

  /* Content */
  .ti-post { display: grid; grid-template-columns: 46px 1fr; gap: 10px; padding: 11px 0;
             border-top: 1px solid var(--line); }
  .ti-post:first-of-type { border-top: 0; }
  .ti-datum { text-align: center; line-height: 1.1; color: var(--ink-soft); font-size: 11px;
              text-transform: uppercase; }
  .ti-datum b { display: block; font-family: var(--display); font-size: 22px;
                color: var(--ink); font-weight: 400; }
  .ti-post h4 { margin: 4px 0 2px; font-family: var(--display); font-weight: 400;
                font-size: 15px; line-height: 1.3; }
  .ti-post .hook { font-size: 12.5px; color: var(--ink-soft); display: -webkit-box;
                   -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
  .ti-knoepfe { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
  .ti-stand { font-size: 11.5px; }
  .ti-stand.gut { color: var(--good); }
  .ti-stand.warn { color: var(--orange); }
  .ti-stand.info { color: var(--teal); }

  /* PIA */
  .ti-pia-kopf { display: flex; gap: 10px; align-items: center; margin-bottom: 12px; }
  .ti-pia-kopf .ti-ava { flex-basis: 40px; height: 40px; font-size: 17px; }
  .ti-pia-kopf b { font-family: var(--display); font-size: 18px; font-weight: 400; display: block; }
  .ti-verlauf { display: flex; flex-direction: column; gap: 8px; max-height: 360px;
                overflow-y: auto; padding: 2px; }
  .ti-msg { border-radius: 12px; padding: 9px 11px; font-size: 13.5px; line-height: 1.5;
            white-space: pre-wrap; overflow-wrap: break-word; }
  .ti-msg.ich { background: var(--surface-2); align-self: flex-end; max-width: 88%; }
  .ti-msg.pia { background: var(--teal-soft); border-left: 3px solid var(--teal); }
  .ti-msg .wer { display: block; font-size: 10px; letter-spacing: 0.12em;
                 text-transform: uppercase; color: var(--ink-soft); margin-bottom: 3px;
                 white-space: normal; }
  .ti-pia-eingabe { display: flex; gap: 6px; margin-top: 10px; align-items: flex-end; }
  .ti-pia-eingabe textarea { flex: 1; min-height: 44px; resize: vertical; }

  /* Helferinnen */
  .ti-helfergrid { display: grid; gap: 8px;
                   grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); }
  .ti-h { display: flex; gap: 9px; align-items: center; text-align: left;
          border: 1px solid var(--line); background: var(--ground); border-radius: 12px;
          padding: 9px; cursor: pointer; font: inherit; color: var(--ink); min-width: 0; }
  .ti-h:hover { border-color: var(--teal); }
  .ti-h[aria-expanded="true"] { border-color: var(--teal); box-shadow: inset 0 0 0 1px var(--teal); }
  .ti-ava { flex: 0 0 32px; height: 32px; border-radius: 50%; display: flex;
            align-items: center; justify-content: center; font-family: var(--display);
            font-size: 14px; color: #fff; background: #12828c; }
  .ti-ava.o { background: #dc822e; }
  .ti-ava.n { background: #29556d; }
  .ti-h .t { min-width: 0; }
  .ti-h b { display: block; font-size: 13px; line-height: 1.2; }
  .ti-h small { display: block; font-size: 11.5px; color: var(--ink-soft); line-height: 1.3; }
  .ti-detail { margin-top: 12px; background: var(--ground); border-radius: 14px;
               padding: 14px; border: 1px solid var(--line); }
  .ti-detail h3 { margin: 0 0 4px; font-family: var(--display); font-weight: 400; font-size: 18px; }
  .ti-detail p { margin: 0 0 10px; font-size: 13px; color: var(--ink-soft); }
  .ti-detail textarea { width: 100%; min-height: 84px; resize: vertical; }
  .ti-befehl { font-family: ui-monospace, Consolas, monospace; font-size: 12px;
               background: var(--surface-2); padding: 2px 7px; border-radius: 6px; }
  .ti-antwort { white-space: pre-wrap; background: var(--surface); border: 1px solid var(--line);
                border-radius: 10px; padding: 11px 12px; font-size: 13.5px; line-height: 1.55;
                margin-top: 10px; max-height: 420px; overflow-y: auto; }
"""

# ---------------------------------------------------------------- JS
JS_ANKER = "  function renderUebersicht(main) {"
JS = r"""  /* =========================================================
     Mein Tisch — die Startseite (08.10.2026)
     Siehe Kopf von scripts/cockpit/patch-mein-tisch.py.
     ========================================================= */
  var termine = null;            // daten/termine — gehoert PATRICIA
  var tiTag = null;              // gewaehlter Tag im Kalender
  var tiMonat = null;            // "2026-10"
  var tiAfBereich = "Business";
  var tiHelfer = null;           // welche Helferin aufgeklappt ist
  var tiSaeule = "Instagram";
  var tiAntwort = {};            // Helferin -> {laeuft|text|fehler}
  var tiEingabe = {};            // Helferin -> getippter Auftrag
  var piaLaeuft = false;
  var piaEntwurf = "";
  var piaVerlauf = [];
  try { piaVerlauf = JSON.parse(localStorage.getItem("mlb:pia-verlauf") || "[]") || []; } catch (e) {}

  /* Nach den Saeulen der Mum Business Academy (Patricia, 08.10.2026).
     `schnell`: antwortet direkt hier ueber `sample`. Ohne `schnell` braucht
     sie den Workspace — dann gibt es nur den Befehl fuer Claude Code. */
  var TI_SAEULEN = ["Instagram", "Produkte", "Mama-CEO", "KI", "Privat"];
  var HELFERINNEN = [
    { id: "content", s: "Instagram", name: "Content-Planerin", befehl: "/content woche",
      was: "schreibt deine ganze Instagram-Woche: Marktcheck, Hooks, Reels, Karussells, Captions, Story-Bogen — und legt alles hier ins Cockpit." },
    { id: "hooks", s: "Instagram", name: "Hook-Schreiberin", befehl: "/hooks", schnell: true,
      was: "findet erste Zeilen aus mindestens drei Blickwinkeln, mit Kundensprache und dem letzten Check.",
      auftrag: "Schreibe acht Hooks aus mindestens drei verschiedenen Angles. Je Hook eine Zeile, darunter klein der Angle. Die Lösung kommt nie im Hook." },
    { id: "reels", s: "Instagram", name: "Reel-Regisseurin", befehl: "/reels", schnell: true, format: "reel",
      was: "plant ein Reel: Cover-Hook, Sprechtext, was im Bild passiert.",
      auftrag: "Schlage ein Reel vor: Cover-Hook (höchstens acht Wörter), Sprechtext für 30 bis 45 Sekunden in gesprochener Sprache, was im Bild zu sehen ist, und eine Caption-Idee." },
    { id: "karussell", s: "Instagram", name: "Karussell-Gestalterin", befehl: "/karussell", schnell: true, format: "karussell",
      was: "baut ein Karussell Folie für Folie, mit Typ und Funnel-Stufe.",
      auftrag: "Schlage ein Karussell vor: Typ (Listicle, Story, Edukativ oder Kontrovers), Folie für Folie Überschrift und Text, am Schluss eine Caption-Idee." },
    { id: "story", s: "Instagram", name: "Story-Begleiterin", befehl: "/story", schnell: true, format: "story",
      was: "macht aus deinem Tag eine Story-Sequenz mit Aufruf.",
      auftrag: "Schlage eine Story-Sequenz mit sechs bis acht Frames vor: Frame für Frame der Text, mindestens ein Frame mit Frage oder Umfrage, am Schluss ein Aufruf." },
    { id: "caption", s: "Instagram", name: "Caption-Texterin", befehl: "/caption", schnell: true,
      was: "schreibt die fertige Caption mit genau einem Keyword-Aufruf.",
      auftrag: "Schreibe eine fertige Caption nach dem hinterlegten Aufbau, mit genau einem Keyword-Aufruf und fünf Hashtags." },
    { id: "blog", s: "Instagram", name: "Blog-Autorin", befehl: "/blog",
      was: "schreibt den Blogartikel zum Monatsthema und macht Storys, Karussell und Mail daraus." },
    { id: "produkt", s: "Produkte", name: "Produkt-Kreiererin", befehl: "/produkt", schnell: true,
      was: "entwickelt Produkttreppe, Module, Preis-Staffel und Launch.",
      auftrag: "Hilf beim Produkt: Idee schärfen, Transformation vorher und nachher, Stufe in der Produkttreppe, Module grob, nächster Schritt. Erfinde keine Preise und keine Zahlen." },
    { id: "copywriting", s: "Produkte", name: "Verkaufstexterin", befehl: "/copywriting", schnell: true,
      was: "schreibt Verkaufsseite, Mail-Strecke oder VSL nach Julias Pipeline.",
      auftrag: "Schreibe den gewünschten Verkaufstext. Keine Geld-zurück-Garantie, nichts erfinden. Fehlen Angaben, nenne sie in der ersten Zeile." },
    { id: "funnel", s: "Produkte", name: "Funnel-Strategin", befehl: "/funnel",
      was: "baut Freebie, Seite, Mails und Pitch zu einer Kette — mit ActiveCampaign und ManyChat." },
    { id: "ads", s: "Produkte", name: "Werbe-Expertin", befehl: "/facebook-ads",
      was: "plant, textet und wertet Meta-Anzeigen aus." },
    { id: "strategie", s: "Mama-CEO", name: "Business-Strategin", befehl: "/strategie",
      was: "liest deine echten Zahlen und sagt, was gerade der Engpass zu 40'000 ist." },
    { id: "monatsplan", s: "Mama-CEO", name: "Monatsplanerin", befehl: "/monatsplan",
      was: "legt Säule, Produkte und Hauptbotschaft für den nächsten Monat fest." },
    { id: "jahresplan", s: "Mama-CEO", name: "Jahresplanerin", befehl: "/jahresplan",
      was: "hält Launches und Vorhaben übers Jahr zusammen und findet Überschneidungen." },
    { id: "pia", s: "KI", name: "PIA für Kundinnen", link: "https://pia.mumlifebalance.ch",
      was: "deine KI-Mentorin für die Frauen in der Academy — Bio, Hooks, Leadmagnet, Fahrplan." },
    { id: "bildeditor", s: "KI", name: "Bild-Editor", link: BILDEDITOR,
      was: "Story, Reel-Cover und Karussell-Folien mit deinen Fotos bauen und herunterladen." },
    { id: "videoschnitt", s: "KI", name: "Cutterin", befehl: "/videoschnitt",
      was: "schneidet dein Rohmaterial nach deinen Regeln und baut Hook und Untertitel." },
    { id: "handy", s: "KI", name: "Handy-Abholerin", befehl: "/handy",
      was: "holt neue Fotos und Videos aus dem Album Content-Inbox." },
    { id: "garten", s: "Privat", name: "Garten-Beraterin", befehl: "/garten",
      was: "Beetplan, Aussaat und Mondkalender fürs Appenzellerland." },
    { id: "mealplan", s: "Privat", name: "Kochassistentin", befehl: "/mealplan",
      was: "Wochenplan, Einkaufsliste nach Migros-Aktionen, Spontan-Kochen." },
    { id: "basteln", s: "Privat", name: "Bastel-Helferin", befehl: "/basteln",
      was: "findet Ideen aus deinem eigenen Material, mit Nummern und Dateien." },
    { id: "berufswahl", s: "Privat", name: "Berufswahl-Kompass", befehl: "/berufswahl",
      was: "fragt nach Tätigkeiten statt nach Berufen und sammelt über Monate." }
  ];

  function tiPad(n) { return (n < 10 ? "0" : "") + n; }
  function tiIso(d) { return d.getFullYear() + "-" + tiPad(d.getMonth() + 1) + "-" + tiPad(d.getDate()); }
  function tiTagLang(iso) {
    var d = new Date(iso + "T12:00:00");
    return isNaN(d) ? iso : d.toLocaleDateString("de-CH", { weekday: "long", day: "numeric", month: "long" });
  }
  function tiBereich(a) { return a.bereich === "Privat" ? "Privat" : "Business"; }

  function tmSpeichern() {
    termine.updatedAt = new Date().toISOString();
    lsSet("termine", termine);           // sofort — siehe Datenverlust vom 24.09.
    clearTimeout(saveTimers.termine);
    saveTimers.termine = setTimeout(function () {
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }
      db.doc("daten/termine").set(termine)
        .then(function () { setSaveState("gespeichert", "on"); })
        .catch(function () { setSaveState("nur lokal gespeichert", "off"); });
    }, 500);
  }
  function tiAfSpeichern() {
    aufgaben.updatedAt = new Date().toISOString();
    lsSet("aufgaben", aufgaben);         // sofort, afSpeichern wartet 700 ms
    afSpeichern();
  }
  function tiTerminNeu(t) {
    if (!termine) termine = { items: [] };
    if (!termine.items) termine.items = [];
    termine.items.push({ id: uid("tm"), datum: t.datum, zeit: t.zeit || "",
                         titel: t.titel, bereich: t.bereich === "Privat" ? "Privat" : "Business",
                         quelle: t.quelle || "Cockpit" });
    tmSpeichern();
  }
  function tiAufgabeNeu(a) {
    if (!aufgaben) aufgaben = { items: [] };
    if (!aufgaben.items) aufgaben.items = [];
    aufgaben.items.unshift({ id: uid("af"), aufgabe: a.text, datum: a.datum || "",
      prio: a.prio || "Mittel", status: "Geplant", notiz: a.notiz || "", erledigt: false,
      bereich: a.bereich === "Privat" ? "Privat" : "Business", quelle: a.quelle || "Cockpit",
      fuerClaude: !!a.fuerClaude });
    tiAfSpeichern();
  }

  function tiKopieren(text, knopf) {
    var ok = false;
    try {
      var ta = document.createElement("textarea");
      ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      ok = document.execCommand("copy");
      document.body.removeChild(ta);
    } catch (e) {}
    var alt = knopf.textContent;
    knopf.textContent = ok ? "Kopiert" : "Bitte von Hand markieren";
    setTimeout(function () { knopf.textContent = alt; }, 2200);
  }

  /* Zwei Klicks zum Loeschen, der zweite verfaellt — kein confirm() im
     Artifact-Rahmen. */
  function tiWegKnopf(beiZweitem) {
    var b = document.createElement("button");
    b.className = "ti-weg"; b.textContent = "×"; b.title = "entfernen";
    var scharf = false;
    b.onclick = function (ev) {
      ev.stopPropagation();
      if (!scharf) {
        scharf = true; b.classList.add("scharf"); b.textContent = "sicher?";
        setTimeout(function () { scharf = false; b.classList.remove("scharf"); b.textContent = "×"; }, 6000);
        return;
      }
      beiZweitem();
    };
    return b;
  }

  /* Was an einem Tag liegt — eine Stelle fuer Punkte im Kalender und
     die Tagesliste, sonst zeigt der Punkt etwas anderes als die Liste. */
  function tiAmTag(iso, beitraege) {
    var r = { termine: [], laeuft: [], beitraege: [], aufgaben: [] };
    ((termine && termine.items) || []).forEach(function (t) { if (t.datum === iso) r.termine.push(t); });
    ((jahresplan && jahresplan.eintraege) || []).forEach(function (e) {
      if (!e.start || e.bereich === "Ferien") return;
      var ende = e.ende || e.start;
      if (e.start <= iso && ende >= iso) r.laeuft.push(e);
    });
    beitraege.forEach(function (b) { if (datumVon(b) === iso) r.beitraege.push(b); });
    ((aufgaben && aufgaben.items) || []).forEach(function (a) {
      if (!a.erledigt && a.datum === iso) r.aufgaben.push(a);
    });
    return r;
  }

  function renderTisch(main) {
    var jetzt = new Date();
    var heute = tiIso(jetzt);
    if (!tiTag) tiTag = heute;
    if (!tiMonat) tiMonat = tiTag.slice(0, 7);
    var beitraege = offeneBeitraege();

    var raus = beitraege.filter(function (b) {
      return !istDraussen(b) && istFertig(b) && !zeitpunktVorbei(b);
    });
    var deins = 0;
    beitraege.forEach(function (b) {
      // Ohne Datum ist nichts eine Aufgabe (Lehre vom 24.09.2026).
      if (istDraussen(b) || !datumVon(b)) return;
      (wasFehlt(b) || []).forEach(function (f) { if (f.wer === "du") deins++; });
    });
    var afOffen = ((aufgaben && aufgaben.items) || []).filter(function (a) { return !a.erledigt; });
    var faellig = afOffen.filter(function (a) { return a.datum && a.datum < heute; }).length;

    var stunde = jetzt.getHours();
    var gruss = stunde < 11 ? "Guten Morgen" : (stunde < 18 ? "Hallo" : "Guten Abend");

    main.innerHTML =
      '<div class="ti">' +
        '<header class="ti-kopf"><div>' +
          '<span class="ti-label">Mein Tisch</span>' +
          '<h1>' + esc(gruss) + ', Patricia</h1>' +
          '<p>' + esc(tiTagLang(heute)) + ' · PIA führt, du entscheidest.</p>' +
        '</div><div class="ti-zahlen">' +
          '<button class="ti-zahl" data-gehe="fertig"><b>' + raus.length + '</b>kann raus</button>' +
          '<button class="ti-zahl du" data-gehe="woche"><b>' + deins + '</b>wartet auf dich</button>' +
          '<button class="ti-zahl" data-gehe="aufgaben"><b>' + faellig + '</b>überfällig</button>' +
          // 🚨 Kein Umsatz auf der Startseite (Patricia, 08.10.2026): sie zeigt
          // das Cockpit Kundinnen. Umsatz steht unter Mama-CEO → Zahlen.
        '</div></header>' +
        '<div class="ti-grid">' +
          '<section class="ti-spalte"><div class="ti-karte" id="ti-pia"></div></section>' +
          '<section class="ti-spalte"><div class="ti-karte" id="ti-af"></div></section>' +
          '<section class="ti-spalte"><div class="ti-karte" id="ti-kal"></div>' +
                                     '<div class="ti-karte" id="ti-tag"></div></section>' +
          '<section class="ti-spalte"><div class="ti-karte" id="ti-content"></div></section>' +
        '</div>' +
        '<div class="ti-karte ti-voll" id="ti-helfer"></div>' +
      '</div>';

    Array.prototype.forEach.call(main.querySelectorAll("[data-gehe]"), function (b) {
      b.onclick = function () { activeTab = b.getAttribute("data-gehe"); render(); };
    });

    tiPia(main.querySelector("#ti-pia"), heute, beitraege);
    tiAufgaben(main.querySelector("#ti-af"), heute);
    tiKalender(main.querySelector("#ti-kal"), heute, beitraege);
    tiTagliste(main.querySelector("#ti-tag"), beitraege);
    tiContent(main.querySelector("#ti-content"), heute, beitraege);
    tiHelferinnen(main.querySelector("#ti-helfer"));
  }

  /* ---------- PIA ---------- */
  function piaMerken(wer, text) {
    piaVerlauf.push({ wer: wer, text: text, zeit: new Date().toISOString() });
    piaVerlauf = piaVerlauf.slice(-30);
    try { localStorage.setItem("mlb:pia-verlauf", JSON.stringify(piaVerlauf)); } catch (e) {}
  }

  function tiPia(el, heute, beitraege) {
    el.innerHTML =
      '<div class="ti-pia-kopf"><span class="ti-ava o">P</span><div><b>PIA</b>' +
      '<span class="ti-klein">' + (sampler ? "deine Assistentin · am Handy: ins Feld tippen, dann das 🎤 auf der Tastatur"
                                          : "gerade nicht verbunden") + '</span></div>' +
      (piaVerlauf.length ? '<button class="ti-btn" id="pia-neu" style="margin-left:auto">Neu</button>' : '') +
      '</div><div class="ti-verlauf" id="pia-verlauf"></div>' +
      '<div class="ti-pia-eingabe"><textarea class="ti-feld" id="pia-text" rows="2" ' +
      'placeholder="z.B. Morgen 14 Uhr Zahnarzt mit L. · Aufgabe: Aufzeichnung in die Mails · Was steht heute an?"></textarea>' +
      '<button class="ti-btn voll" id="pia-los"' + (piaLaeuft || !sampler ? " disabled" : "") + '>' +
      (piaLaeuft ? "…" : "Senden") + '</button></div>';

    var vl = el.querySelector("#pia-verlauf");
    if (!piaVerlauf.length) {
      vl.innerHTML = '<div class="ti-msg pia"><span class="wer">PIA</span>' +
        'Sag mir, was ansteht. Ich trage Aufgaben und Termine ein und sage dir, was heute wichtig ist. ' +
        'Freigeben, einplanen und löschen bleibt bei dir.</div>';
    }
    piaVerlauf.forEach(function (m) {
      var d = document.createElement("div");
      d.className = "ti-msg " + (m.wer === "ich" ? "ich" : "pia");
      d.innerHTML = '<span class="wer">' + (m.wer === "ich" ? "Du" : "PIA") + '</span>';
      d.appendChild(document.createTextNode(m.text));
      vl.appendChild(d);
    });
    if (piaLaeuft) {
      var w = document.createElement("div");
      w.className = "ti-msg pia"; w.textContent = "denkt nach …";
      vl.appendChild(w);
    }
    vl.scrollTop = vl.scrollHeight;

    var ta = el.querySelector("#pia-text");
    ta.value = piaEntwurf;
    ta.oninput = function () { piaEntwurf = ta.value; };
    ta.onkeydown = function (ev) {
      if (ev.key === "Enter" && !ev.shiftKey) { ev.preventDefault(); piaSenden(heute, beitraege); }
    };
    el.querySelector("#pia-los").onclick = function () { piaSenden(heute, beitraege); };
    var neu = el.querySelector("#pia-neu");
    if (neu) neu.onclick = function () {
      piaVerlauf = [];
      try { localStorage.removeItem("mlb:pia-verlauf"); } catch (e) {}
      render();
    };
  }

  function piaLage(heute, beitraege) {
    var z = [];
    var bis = new Date(heute + "T12:00:00"); bis.setDate(bis.getDate() + 7);
    var bisIso = tiIso(bis);
    z.push("TERMINE (nächste 7 Tage):");
    ((termine && termine.items) || []).filter(function (t) { return t.datum >= heute && t.datum <= bisIso; })
      .sort(function (a, b) { return (a.datum + a.zeit) < (b.datum + b.zeit) ? -1 : 1; })
      .forEach(function (t) { z.push("- " + t.datum + " " + (t.zeit || "") + " " + t.titel + " [" + (t.bereich || "Business") + "]"); });
    ((jahresplan && jahresplan.eintraege) || []).forEach(function (e) {
      var ende = e.ende || e.start;
      if (e.start && e.start <= bisIso && ende >= heute && e.bereich !== "Ferien")
        z.push("- Vorhaben " + e.start + " bis " + ende + ": " + e.name);
    });
    z.push("OFFENE AUFGABEN:");
    ((aufgaben && aufgaben.items) || []).filter(function (a) { return !a.erledigt; })
      .sort(function (a, b) { return (a.datum || "9999") < (b.datum || "9999") ? -1 : 1; })
      .slice(0, 40).forEach(function (a) {
        z.push("- " + (a.datum || "ohne Datum") + " [" + tiBereich(a) + ", " + (a.prio || "Mittel") + "] " + a.aufgabe);
      });
    z.push("BEITRÄGE (nächste 7 Tage):");
    beitraege.filter(function (b) { var d = datumVon(b); return d && d >= heute && d <= bisIso; })
      .forEach(function (b) { z.push("- " + datumVon(b) + " " + b.format + " " + kartenProfil(b.obj) + ": " + (b.titel || "") + " — " + tpStand(b).text); });
    return z.join("\n");
  }

  function piaSenden(heute, beitraege) {
    var text = (piaEntwurf || "").trim();
    if (!text || piaLaeuft || !sampler) return;
    piaMerken("ich", text);
    piaEntwurf = ""; piaLaeuft = true; render();
    var tag = new Date(heute + "T12:00:00");
    var p =
      "Du bist PIA, die Assistentin von Patricia Ulmann (Mum Life Balance, Mentorin für Network-Mamas, vierfache Mama, Appenzellerland). " +
      "Du sprichst sie mit du an, warm, kurz und klar, Schweizer Rechtschreibung mit ss, keine Emojis.\n\n" +
      "Heute ist " + WOCHENTAGE[tag.getDay()] + ", " + heute + ".\n\n" + piaLage(heute, beitraege) + "\n\n" +
      "Will sie, dass etwas gebaut, geschrieben, geprüft oder geändert wird (Karussell, Mail, Seite, Auswertung), " +
      "leg es als Auftrag an Claude an — Claude sieht offene Aufträge beim nächsten Start in Claude Code. Sag ihr das so.\n" +
      "Was du tun darfst: Aufgaben, Termine und Aufträge an Claude anlegen. Sonst nichts — du gibst nichts frei, planst nichts ein, löschst nichts. " +
      "Wenn sie etwas anderes will, sag ihr in einem Satz, wo sie das im Cockpit macht oder welchen Befehl sie in Claude Code gibt.\n" +
      "Termin = etwas mit Datum, an dem sie irgendwo sein muss oder das zu einer Uhrzeit stattfindet. Aufgabe = etwas, das sie erledigen muss. " +
      "Rechne Angaben wie morgen, Freitag, nächste Woche in ein Datum JJJJ-MM-TT um. Ohne Angabe bleibt das Datum leer. " +
      "Bereich: Privat bei Familie, Kinder, Haushalt, Arzt, Garten, Freizeit; sonst Business. " +
      "Steht schon eine sehr ähnliche Aufgabe in der Liste, lege sie trotzdem an und sag es ihr in einem Satz. " +
      "Erfinde nichts dazu. Fragt sie etwas, antworte aus der Lage oben; was dort nicht steht, weisst du nicht.\n\n" +
      "IHRE NACHRICHT\n" + text + "\n\n" +
      'Antworte als JSON: {"aktionen": [{"art": "aufgabe", "text": "...", "datum": "", "bereich": "Business", "prio": "Mittel"}, ' +
      '{"art": "termin", "titel": "...", "datum": "JJJJ-MM-TT", "zeit": "HH:MM oder leer", "bereich": "Privat"}, ' +
      '{"art": "claude", "text": "der Auftrag in einem klaren Satz", "datum": ""}], "antwort": "was du ihr sagst"}. ' +
      "prio ist Hoch, Mittel, Tief oder Quick Win. Keine Aktion nötig: leere Liste.";
    // 🚨 Erst die Antwort holen, dann getrennt eintragen. Bis 08.10.2026 lief
    // beides in einem Block, und jeder Fehler hiess „(Fehler)" — ob Claude
    // nicht antwortete oder das Eintragen umfiel, war nicht zu unterscheiden.
    var antwort = null;
    sampler.json(p, { cache: false }).then(function (r) {
      antwort = (r && typeof r === "object" && !Array.isArray(r)) ? r : { antwort: String(r || "") };
    }, function (e) {
      console.error("PIA: Claude hat nicht geantwortet", e);
      var grund = (e && (e.code || e.name || e.message)) || "unbekannt";
      var klartext = {
        not_granted: "Du hast PIA die Erlaubnis nicht gegeben. Lade das Cockpit neu und tippe beim Nachfragen auf Erlauben.",
        rate_limited: "Gerade zu viele Anfragen. Versuch es in ein paar Minuten nochmal.",
        session_expired: "Du bist bei Claude abgemeldet. Melde dich neu an und lade das Cockpit neu.",
        sampling_disabled: "In diesem Konto ist das Fragen aus dem Cockpit ausgeschaltet.",
        invalid_json: "Die Antwort kam in der falschen Form zurück. Schick die Nachricht einfach nochmal."
      }[grund];
      piaMerken("pia", (klartext || "Claude hat nicht geantwortet (" + grund + ").") +
        " Eingetragen habe ich nichts.");
    }).then(function () {
      if (!antwort) return;
      var r = antwort;
      var gemacht = [], schief = 0;
      (Array.isArray(r.aktionen) ? r.aktionen : []).forEach(function (a) {
       try {
        if (!a || typeof a !== "object") return;
        a.text = a.text == null ? "" : String(a.text);
        a.titel = a.titel == null ? "" : String(a.titel);
        a.datum = a.datum == null ? "" : String(a.datum);
        a.zeit = a.zeit == null ? "" : String(a.zeit);
        if (a.art === "aufgabe" && (a.text || "").trim()) {
          tiAufgabeNeu({ text: a.text.trim(), datum: /^\d{4}-\d{2}-\d{2}$/.test(a.datum || "") ? a.datum : "",
                         bereich: a.bereich, prio: AF_PRIO.indexOf(a.prio) >= 0 ? a.prio : "Mittel", quelle: "PIA" });
          gemacht.push("✓ Aufgabe: " + a.text.trim());
        } else if (a.art === "claude" && (a.text || "").trim()) {
          tiAufgabeNeu({ text: a.text.trim(), datum: /^\d{4}-\d{2}-\d{2}$/.test(a.datum || "") ? a.datum : "",
                         bereich: "Business", prio: "Mittel", quelle: "PIA", fuerClaude: true });
          gemacht.push("✓ Auftrag an Claude: " + a.text.trim());
        } else if (a.art === "termin" && (a.titel || "").trim() && /^\d{4}-\d{2}-\d{2}$/.test(a.datum || "")) {
          tiTerminNeu({ titel: a.titel.trim(), datum: a.datum,
                        zeit: /^\d{1,2}:\d{2}$/.test(a.zeit || "") ? a.zeit : "", bereich: a.bereich, quelle: "PIA" });
          gemacht.push("✓ Termin " + fmtDate(a.datum) + (a.zeit ? " " + a.zeit : "") + ": " + a.titel.trim());
        }
       } catch (e) { console.error("PIA: Eintrag fiel um", a, e); schief++; }
      });
      // Was eingetragen wurde, steht wörtlich da — nicht nur PIAs Satz dazu.
      piaMerken("pia", String(r.antwort || "Erledigt.") +
        (gemacht.length ? "\n\n" + gemacht.join("\n") : "") +
        (schief ? "\n\n" + schief + " Eintrag liess sich nicht anlegen — sag es mir bitte nochmal anders." : ""));
    }).catch(function (e) {
      console.error("PIA:", e);
      piaMerken("pia", "Beim Eintragen ist etwas schiefgegangen (" +
        ((e && (e.message || e.code)) || "unbekannt") + "). Schau unter Aufgaben nach, was schon drin ist.");
    }).then(function () { piaLaeuft = false; render(); });
  }

  /* ---------- Aufgaben ---------- */
  function tiAufgaben(el, heute) {
    var alle = (aufgaben && aufgaben.items) || [];
    var zahl = { Business: 0, Privat: 0 };
    alle.forEach(function (a) { if (!a.erledigt) zahl[tiBereich(a)]++; });
    var hier = alle.filter(function (a) { return tiBereich(a) === tiAfBereich; });
    var offen = hier.filter(function (a) { return !a.erledigt; }).sort(function (a, b) {
      return (a.datum || "9999") < (b.datum || "9999") ? -1 : 1;
    });
    var ueber = offen.filter(function (a) { return a.datum && a.datum < heute; });
    var heuteL = offen.filter(function (a) { return a.datum === heute; });
    var spaeter = offen.filter(function (a) { return !a.datum || a.datum > heute; });
    var fertig = hier.filter(function (a) { return a.erledigt; }).sort(function (a, b) {
      return (a.erledigt_am || "") > (b.erledigt_am || "") ? -1 : 1;
    }).slice(0, 3);

    el.innerHTML = '<div class="ti-kartekopf"><span class="ti-chip">Aufgaben</span>' +
      '<div class="ti-seg">' + ["Business", "Privat"].map(function (k) {
        return '<button data-b="' + k + '" aria-pressed="' + (k === tiAfBereich) + '">' + k +
               '<span class="n">' + zahl[k] + '</span></button>';
      }).join("") + '</div></div><div id="ti-afl"></div>';
    Array.prototype.forEach.call(el.querySelectorAll("[data-b]"), function (b) {
      b.onclick = function () { tiAfBereich = b.getAttribute("data-b"); render(); };
    });

    var box = el.querySelector("#ti-afl");
    function gruppe(titel, liste, rot, max) {
      if (!liste.length) return;
      var g = document.createElement("div");
      g.className = "ti-gruppe" + (rot ? " rot" : "");
      g.innerHTML = "<span>" + esc(titel) + "</span><span>" + liste.length + "</span>";
      box.appendChild(g);
      liste.slice(0, max || 50).forEach(function (a) { box.appendChild(tiAfZeile(a, heute)); });
      if (max && liste.length > max) {
        var m = document.createElement("button");
        m.className = "ti-btn"; m.style.marginTop = "6px";
        m.textContent = "alle " + liste.length + " ansehen";
        m.onclick = function () { activeTab = "aufgaben"; render(); };
        box.appendChild(m);
      }
    }
    gruppe("Überfällig", ueber, true, 5);
    gruppe("Heute", heuteL, false);
    gruppe("Später oder ohne Datum", spaeter, false, 6);
    gruppe("Zuletzt erledigt", fertig, false);
    if (!offen.length && !fertig.length) box.innerHTML = '<div class="ti-leer">Nichts offen.</div>';

    var f = document.createElement("form");
    f.className = "ti-form";
    f.innerHTML = '<div class="reihe"><input type="text" name="t" placeholder="Neue Aufgabe (' + tiAfBereich + ')"></div>' +
      '<div class="reihe"><input type="date" name="d"><select name="p">' +
      AF_PRIO.map(function (p) { return '<option' + (p === "Mittel" ? " selected" : "") + '>' + p + '</option>'; }).join("") +
      '</select><button class="ti-btn voll" type="submit">Hinzufügen</button></div>';
    f.onsubmit = function (ev) {
      ev.preventDefault();
      var t = f.t.value.trim();
      if (!t) return;
      tiAufgabeNeu({ text: t, datum: f.d.value, prio: f.p.value, bereich: tiAfBereich });
      render();
    };
    el.appendChild(f);
  }

  function tiAfZeile(a, heute) {
    var z = document.createElement("div");
    z.className = "ti-af" + (a.erledigt ? " fertig" : "");
    var cb = document.createElement("input");
    cb.type = "checkbox"; cb.checked = !!a.erledigt; cb.title = "erledigt";
    cb.onchange = function () {
      a.erledigt = cb.checked;
      a.erledigt_am = cb.checked ? heute : "";
      tiAfSpeichern(); render();
    };
    var r = document.createElement("div");
    var meta = "";
    if (a.datum) {
      var ueber = !a.erledigt && a.datum < heute;
      var tage = ueber ? Math.round((new Date(heute) - new Date(a.datum)) / 86400000) : 0;
      meta += '<span class="ti-mini' + (ueber ? " rot" : "") + '">' +
        (ueber ? "seit " + tage + (tage === 1 ? " Tag" : " Tagen") : fmtDate(a.datum)) + '</span>';
    }
    if (a.prio === "Hoch" || a.prio === "Quick Win") meta += '<span class="ti-mini hoch">' + esc(a.prio) + '</span>';
    if (a.fuerClaude) meta += '<span class="ti-mini hoch">für Claude</span>';
    else if (a.quelle === "PIA") meta += '<span class="ti-mini">von PIA</span>';
    r.innerHTML = '<div class="txt">' + esc(a.aufgabe || "(ohne Text)") + '</div>' +
      (meta ? '<div class="meta">' + meta + '</div>' : "");
    z.appendChild(cb); z.appendChild(r);
    return z;
  }

  /* ---------- Kalender ---------- */
  function tiKalender(el, heute, beitraege) {
    var p = tiMonat.split("-"), y = +p[0], m = +p[1] - 1;
    var erster = new Date(y, m, 1);
    var start = new Date(y, m, 1 - ((erster.getDay() + 6) % 7));
    var name = erster.toLocaleDateString("de-CH", { month: "long", year: "numeric" });
    var h = '<div class="ti-kalkopf"><button class="ti-pfeil" data-s="-1" aria-label="Voriger Monat">‹</button>' +
      '<b>' + esc(name) + '</b><button class="ti-pfeil" data-s="1" aria-label="Nächster Monat">›</button></div>' +
      '<div class="ti-kalgrid">' + ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"].map(function (w) {
        return '<span class="ti-wt">' + w + '</span>';
      }).join("");
    for (var i = 0; i < 42; i++) {
      var d = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i);
      var iso = tiIso(d);
      var am = tiAmTag(iso, beitraege);
      var cls = "ti-tag" + (d.getMonth() !== m ? " fremd" : "") + (iso === heute ? " heute" : "") +
                (iso === tiTag ? " gewaehlt" : "");
      h += '<button class="' + cls + '" data-tag="' + iso + '">' + d.getDate() + '<span class="ti-punkte">' +
        ((am.termine.length || am.laeuft.some(function (e) { return e.start === iso; })) ? '<i class="pt-termin"></i>' : "") +
        (am.beitraege.length ? '<i class="pt-beitrag"></i>' : "") +
        (am.aufgaben.length ? '<i class="pt-aufgabe"></i>' : "") + '</span></button>';
    }
    h += '</div><div class="ti-legende"><span><i class="pt-termin"></i>Termin</span>' +
      '<span><i class="pt-beitrag"></i>Beitrag</span><span><i class="pt-aufgabe"></i>Aufgabe fällig</span></div>';
    el.innerHTML = h;
    Array.prototype.forEach.call(el.querySelectorAll("[data-s]"), function (b) {
      b.onclick = function () {
        var n = new Date(y, m + (+b.getAttribute("data-s")), 1);
        tiMonat = n.getFullYear() + "-" + tiPad(n.getMonth() + 1);
        render();
      };
    });
    Array.prototype.forEach.call(el.querySelectorAll("[data-tag]"), function (b) {
      b.onclick = function () {
        tiTag = b.getAttribute("data-tag");
        tiMonat = tiTag.slice(0, 7);
        render();
      };
    });
  }

  function tiTagliste(el, beitraege) {
    var am = tiAmTag(tiTag, beitraege);
    var zeilen = [];
    am.termine.forEach(function (t) {
      zeilen.push({ zeit: t.zeit || "", text: t.titel, klein: t.bereich === "Privat" ? "privat" : "",
                    weg: function () {
                      termine.items = termine.items.filter(function (x) { return x.id !== t.id; });
                      tmSpeichern(); render();
                    } });
    });
    am.laeuft.forEach(function (e) {
      zeilen.push({ zeit: e.start === tiTag ? "Start" : "läuft", text: e.name, klein: "Jahresplan",
                    gehe: function () { activeTab = "launches"; render(); } });
    });
    am.beitraege.forEach(function (b) {
      var o = b.obj, fr = freigabeVon(b) || {};
      zeilen.push({ zeit: fr.zeit || (o.blotato || {}).zeit || vorgabeZeit(b.art, kartenProfil(o)),
                    text: b.format + " · " + (b.titel || ""),
                    klein: (kartenProfil(o) === "doterra" ? "doTERRA · " : "") + tpStand(b).text,
                    gehe: function () { springeZuBeitrag(b); } });
    });
    am.aufgaben.forEach(function (a) {
      zeilen.push({ zeit: "", text: "☐ " + a.aufgabe, klein: tiBereich(a) === "Privat" ? "privat" : "",
                    gehe: function () { tiAfBereich = tiBereich(a); render(); } });
    });
    zeilen.sort(function (a, b) {
      var za = /^\d/.test(a.zeit) ? a.zeit : (a.zeit ? "00" : "99");
      var zb = /^\d/.test(b.zeit) ? b.zeit : (b.zeit ? "00" : "99");
      return za < zb ? -1 : (za > zb ? 1 : 0);
    });

    el.innerHTML = '<span class="ti-chip o">' + esc(tiTagLang(tiTag)) + '</span><div id="ti-tagl"></div>';
    var box = el.querySelector("#ti-tagl");
    if (!zeilen.length) box.innerHTML = '<div class="ti-leer">Nichts eingetragen.</div>';
    zeilen.forEach(function (z) {
      var d = document.createElement("div");
      d.className = "ti-zeile" + (z.gehe ? " klick" : "");
      d.innerHTML = '<span class="ti-zeit">' + esc(z.zeit) + '</span><span class="ti-was">' + esc(z.text) +
        (z.klein ? '<br><span class="ti-klein">' + esc(z.klein) + '</span>' : "") + '</span>';
      if (z.gehe) d.onclick = z.gehe;
      if (z.weg) d.appendChild(tiWegKnopf(z.weg)); else d.appendChild(document.createElement("span"));
      box.appendChild(d);
    });

    var f = document.createElement("form");
    f.className = "ti-form";
    f.innerHTML = '<div class="reihe"><input type="time" name="z" aria-label="Uhrzeit">' +
      '<input type="text" name="t" placeholder="Termin am ' + esc(fmtDate(tiTag)) + '"></div>' +
      '<div class="reihe"><select name="b"><option>Business</option><option>Privat</option></select>' +
      '<button class="ti-btn voll" type="submit">Eintragen</button></div>';
    f.onsubmit = function (ev) {
      ev.preventDefault();
      var t = f.t.value.trim();
      if (!t) return;
      tiTerminNeu({ titel: t, datum: tiTag, zeit: f.z.value, bereich: f.b.value });
      render();
    };
    el.appendChild(f);
  }

  /* ---------- Content-Kalender ---------- */
  function tiContent(el, heute, beitraege) {
    var bis = new Date(heute + "T12:00:00"); bis.setDate(bis.getDate() + 14);
    var bisIso = tiIso(bis);
    var liste = beitraege.filter(function (b) {
      var d = datumVon(b); return d && d >= heute && d <= bisIso;
    }).sort(function (a, b) {
      return datumVon(a) < datumVon(b) ? -1 : (datumVon(a) > datumVon(b) ? 1 : 0);
    });
    var ohne = beitraege.filter(function (b) { return !datumVon(b); }).length;

    el.innerHTML = '<span class="ti-chip">Content-Kalender · 14 Tage</span><div id="ti-cl"></div>';
    var box = el.querySelector("#ti-cl");
    if (!liste.length) box.innerHTML = '<div class="ti-leer">In den nächsten zwei Wochen ist nichts geplant.</div>';
    liste.forEach(function (b) {
      var d = datumVon(b), dt = new Date(d + "T12:00:00");
      var s = tpStand(b), o = b.obj;
      var p = document.createElement("div");
      p.className = "ti-post";
      p.innerHTML = '<div class="ti-datum">' + WOCHENTAGE[dt.getDay()].slice(0, 2) + '<b>' + dt.getDate() + '</b>' +
        dt.toLocaleDateString("de-CH", { month: "short" }) + '</div><div>' +
        '<span class="ti-mini">' + esc(b.format) + '</span> ' +
        '<span class="ti-mini">' + (kartenProfil(o) === "doterra" ? "doTERRA" : "Mentoring") + '</span> ' +
        '<span class="ti-stand ' + s.art + '">' + esc(s.text) + '</span>' +
        '<h4>' + esc(b.titel || b.format) + '</h4>' +
        (b.hook && b.hook !== b.titel ? '<div class="hook">' + esc(b.hook) + '</div>' : "") +
        '<div class="ti-knoepfe"></div></div>';
      var k = p.querySelector(".ti-knoepfe");
      var an = document.createElement("button");
      an.className = "ti-btn voll"; an.textContent = "In der Woche ansehen";
      an.onclick = function () { springeZuBeitrag(b); };
      k.appendChild(an);
      if (!istDraussen(b) && istFertig(b) && !zeitpunktVorbei(b)) {
        var fr = document.createElement("button");
        fr.className = "ti-btn orange"; fr.textContent = "Freigeben";
        fr.onclick = function () { activeTab = "fertig"; render(); };
        k.appendChild(fr);
      }
      var be = document.createElement("a");
      be.className = "ti-btn"; be.href = BILDEDITOR; be.target = "_blank"; be.rel = "noopener";
      be.textContent = "Im Bild-Editor bauen";
      k.appendChild(be);
      box.appendChild(p);
    });
    if (ohne) {
      var v = document.createElement("div");
      v.className = "ti-klein"; v.style.marginTop = "10px";
      v.textContent = ohne + (ohne === 1 ? " Beitrag liegt" : " Beiträge liegen") + " ohne Datum im Vorrat.";
      el.appendChild(v);
    }
  }

  /* ---------- Helferinnen ---------- */
  function tiHelferinnen(el) {
    var zahl = {};
    HELFERINNEN.forEach(function (h) { zahl[h.s] = (zahl[h.s] || 0) + 1; });
    el.innerHTML = '<div class="ti-kartekopf"><span class="ti-chip">Meine KI-Helferinnen</span>' +
      '<div class="ti-seg">' + TI_SAEULEN.map(function (k) {
        return '<button data-s="' + k + '" aria-pressed="' + (k === tiSaeule) + '">' + k +
               '<span class="n">' + (zahl[k] || 0) + '</span></button>';
      }).join("") + '</div></div><div class="ti-helfergrid" id="ti-hg"></div><div id="ti-hd"></div>';
    Array.prototype.forEach.call(el.querySelectorAll("[data-s]"), function (b) {
      b.onclick = function () { tiSaeule = b.getAttribute("data-s"); tiHelfer = null; render(); };
    });
    var grid = el.querySelector("#ti-hg");
    HELFERINNEN.filter(function (h) { return h.s === tiSaeule; }).forEach(function (h, i) {
      var b = document.createElement("button");
      b.className = "ti-h";
      b.setAttribute("aria-expanded", tiHelfer === h.id ? "true" : "false");
      var farbe = h.link ? " n" : (i % 2 ? " o" : "");
      b.innerHTML = '<span class="ti-ava' + farbe + '">' + esc(h.name.charAt(0)) + '</span>' +
        '<span class="t"><b>' + esc(h.name) + '</b><small>' +
        (h.link ? "öffnet sich daneben" : (h.schnell ? "antwortet auch hier" : esc(h.befehl))) + '</small></span>';
      b.onclick = function () { tiHelfer = tiHelfer === h.id ? null : h.id; render(); };
      grid.appendChild(b);
    });
    var h = HELFERINNEN.filter(function (x) { return x.id === tiHelfer; })[0];
    if (h) tiHelferDetail(el.querySelector("#ti-hd"), h);
  }

  function tiHelferDetail(box, h) {
    var d = document.createElement("div");
    d.className = "ti-detail";
    var an = tiAntwort[h.id] || {};
    if (h.link) {
      d.innerHTML = '<h3>' + esc(h.name) + '</h3><p>' + esc(h.was) + '</p>' +
        '<a class="ti-btn voll" href="' + esc(h.link) + '" target="_blank" rel="noopener">Öffnen</a>';
      box.appendChild(d);
      return;
    }
    d.innerHTML = '<h3>' + esc(h.name) + '</h3><p>' + esc(h.was) + '</p>' +
      '<textarea class="ti-feld" placeholder="Was brauchst du? z.B. Thema, Angebot, Stichworte"></textarea>' +
      '<div class="ti-knoepfe">' +
      (h.schnell ? '<button class="ti-btn voll" data-a="fragen"' + (sampler && !an.laeuft ? "" : " disabled") + '>' +
                   (an.laeuft ? "schreibt …" : "Hier fragen") + '</button>' : "") +
      '<button class="ti-btn" data-a="befehl">Befehl kopieren</button></div>' +
      '<p class="ti-klein" style="margin:8px 0 0">' +
      (h.schnell ? "Hier antwortet sie mit deinem Markenwissen. Soll das Ergebnis gleich ins Cockpit, " +
                   "kopier den Befehl und gib ihn in Claude Code ein."
                 : "Sie braucht deinen ganzen Workspace. Kopier den Befehl und gib ihn in Claude Code ein.") +
      ' <span class="ti-befehl">' + esc(h.befehl) + '</span></p>';
    var ta = d.querySelector("textarea");
    ta.value = tiEingabe[h.id] || "";
    ta.oninput = function () { tiEingabe[h.id] = ta.value; };
    var fb = d.querySelector('[data-a="fragen"]');
    if (fb) fb.onclick = function () { tiFragen(h); };
    var bb = d.querySelector('[data-a="befehl"]');
    bb.onclick = function () {
      var t = (tiEingabe[h.id] || "").trim();
      tiKopieren(h.befehl + (t ? " " + t : ""), bb);
    };
    if (an.fehler) {
      var e = document.createElement("p");
      e.className = "ti-klein"; e.style.color = "var(--crit)"; e.style.marginTop = "8px";
      e.textContent = "Das hat nicht geklappt (" + an.fehler + ").";
      d.appendChild(e);
    }
    if (an.text) {
      var r = document.createElement("div");
      r.className = "ti-antwort"; r.textContent = an.text;
      d.appendChild(r);
      var k = document.createElement("div");
      k.className = "ti-knoepfe";
      var kp = document.createElement("button");
      kp.className = "ti-btn"; kp.textContent = "Kopieren";
      kp.onclick = function () { tiKopieren(an.text, kp); };
      var ik = document.createElement("button");
      ik.className = "ti-btn"; ik.textContent = "In den Ideenkasten";
      ik.onclick = function () {
        inDenIdeenkasten(an.text, h.s === "Instagram" ? "Content" : h.s, h.name);
        ik.disabled = true; ik.textContent = "Liegt im Ideenkasten";
      };
      k.appendChild(kp); k.appendChild(ik);
      d.appendChild(k);
    }
    box.appendChild(d);
  }

  function tiFragen(h) {
    var txt = (tiEingabe[h.id] || "").trim();
    if (!txt) { toast("Schreib zuerst rein, was du brauchst."); return; }
    if (!sampler) { toast("Hier kann ich gerade nicht schreiben — kopier den Befehl."); return; }
    tiAntwort[h.id] = { laeuft: true };
    render();
    var p = "Du bist die " + h.name + " im Team von Patricia Ulmann. Deine Aufgabe: " + h.was +
      "\nHier ist alles, was du über ihre Marke, ihre Zielgruppe und ihre Regeln wissen musst:\n\n" +
      wissenText(h.format || "") +
      "\n\nHalte dich streng an Ton, Hookregeln und Verbote. Erfinde keine Zahlen, keine Kundinnen und keine Szenen aus ihrem Leben. " +
      "Schweizer Rechtschreibung mit ss.\n\n" + (h.auftrag || "") +
      "\n\nPATRICIAS AUFTRAG\n" + txt +
      '\n\nAntworte als JSON: {"antwort": "dein Ergebnis als Text, Absätze mit Zeilenumbruch"}';
    sampler.json(p, { modelTier: "complex" }).then(function (r) {
      tiAntwort[h.id] = { text: (r && (r.antwort || r.text)) || "(leer zurückgekommen)" };
    }).catch(function (e) {
      tiAntwort[h.id] = { fehler: (e && e.code) || "Fehler" };
    }).then(function () { render(); });
  }

"""

# ---------------------------------------------------------------- Einhaengen
ERSETZUNGEN = [
    # Startseite: neue Seite, alte als Rueckfall
    ('    if (activeTab === "uebersicht") renderUebersicht(main);\n',
     '    main.classList.toggle("ti-main", activeTab === "uebersicht");\n'
     '    if (activeTab === "uebersicht") {\n'
     '      // Faellt die neue Seite um, steht die alte da - nie eine leere Startseite.\n'
     '      try { renderTisch(main); }\n'
     '      catch (e) { console.error(e); main.classList.remove("ti-main"); renderUebersicht(main); }\n'
     '    }\n'),
    ('    { id: "uebersicht", label: "Heute" },\n',
     '    { id: "uebersicht", label: "Mein Tisch" },\n'),
    # Laden
    ('  aufgaben = lsGet("aufgaben", null);\n',
     '  aufgaben = lsGet("aufgaben", null);\n'
     '  termine = lsGet("termine", null);\n'),
    # Aufgaben-Snapshot zeichnet auch den Tisch neu
    ('        lsSet("aufgaben", aufgaben);\n'
     '        if (activeTab === "aufgaben") render();\n',
     '        lsSet("aufgaben", aufgaben);\n'
     '        if (activeTab === "aufgaben" || activeTab === "uebersicht") render();\n'),
    # Termine aus der Datenbank — der neuere Stand gewinnt
    ('      db.doc("daten/aufgaben").onSnapshot(function (snap) {\n',
     '      db.doc("daten/termine").onSnapshot(function (snap) {\n'
     '        if (!snap.exists) return;\n'
     '        var d0 = snap.data() || {};\n'
     '        // Lokal neuer? Dann nicht ueberschreiben (Lehre vom 24.09.2026).\n'
     '        if (termine && termine.updatedAt && (!d0.updatedAt || d0.updatedAt < termine.updatedAt)) return;\n'
     '        termine = d0;\n'
     '        lsSet("termine", termine);\n'
     '        if (activeTab === "uebersicht") render();\n'
     '      }, function () {});\n'
     '      db.doc("daten/aufgaben").onSnapshot(function (snap) {\n'),
]


def patchen(t: str) -> str:
    if MARKE in t:
        print("Schon gepatcht — nichts zu tun.")
        return t
    def eins(alt, neu):
        nonlocal t
        assert alt in t, "Anker fehlt: " + alt[:70]
        assert t.count(alt) == 1, "Anker mehrdeutig: " + alt[:70]
        t = t.replace(alt, neu)
    eins(FONT_ALT, FONT_NEU)
    for alt, neu in VAR_ALT:
        assert t.count(alt) == 1, "Variable nicht eindeutig: " + alt
        t = t.replace(alt, neu)
    eins(CSS_ANKER, CSS.rstrip("\n") + "\n" + CSS_ANKER)
    eins(JS_ANKER, JS + JS_ANKER)
    for alt, neu in ERSETZUNGEN:
        eins(alt, neu)
    return t


def node_check(html: str) -> None:
    a = html.index("<script>\n(function () {")
    b = html.index("</script>", a)
    js = html[a + len("<script>"):b]
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        pfad = f.name
    r = subprocess.run(["node", "--check", pfad], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr)
        sys.exit("node --check ist durchgefallen — nichts geschrieben.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datei", default=str(ROOT / "outputs/cockpit/mlb-cockpit.html"))
    args = ap.parse_args()
    pfad = Path(args.datei)
    roh = pfad.read_bytes().decode("utf-8")
    crlf = "\r\n" in roh
    t = roh.replace("\r\n", "\n")
    neu = patchen(t)
    if neu == t:
        return
    node_check(neu)
    # 🚨 Erst fertig bauen und pruefen, dann schreiben — open(p,"w") leert die
    # Datei schon beim Oeffnen.
    pfad.write_bytes((neu.replace("\n", "\r\n") if crlf else neu).encode("utf-8"))
    print("Mein Tisch eingebaut:", pfad)


if __name__ == "__main__":
    main()
