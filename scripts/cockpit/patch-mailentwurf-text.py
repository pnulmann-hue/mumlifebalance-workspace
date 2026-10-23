"""
Mailentwürfe im Cockpit: Knopf „Text kopieren“, Notiz aufklappbar, und eigene
Fassungen zuerst.

  python scripts/cockpit/patch-mailentwurf-text.py <cockpit.html>

Anlass (21.10.2026, Story-Challenge-Mailreise): Patricia will jede Mail als
HTML UND als Text kopieren können. Die Dokumente in `mailentwuerfe` tragen
dafür das Feld `text` (scripts/story-challenge/mails-bauen.py).

🚨 Liegen zu einer Automation sowohl der AC-Abzug (quelle "activecampaign")
   als auch neue Fassungen von Claude, zeigte die Karte beide gemischt als
   „Neue Fassung“. Jetzt stehen nur die neuen oben; der heutige AC-Stand
   steht wie bisher darunter („Und das steckt heute in ActiveCampaign“).

Wiederholbar: erkennt eingesetzte Stellen und lässt sie stehen.
"""
import pathlib
import sys

pfad = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "outputs/cockpit/mlb-cockpit.html")
t = pfad.read_text(encoding="utf-8")


def ersetze(t, alt, neu, marke):
    if marke in t:
        print("  schon drin:", marke)
        return t
    assert t.count(alt) == 1, "Stelle nicht eindeutig gefunden: %r" % alt[:60]
    print("  eingesetzt:", marke)
    return t.replace(alt, neu)


t = ersetze(
    t,
    '    var neu = entwuerfeFuer(nummer);\n',
    '    var neu = entwuerfeFuer(nummer);\n'
    '    /* @@eigene-zuerst: neue Fassungen verdrängen den AC-Abzug oben */\n'
    '    var eigene = neu.filter(function (e) { return e.quelle !== "activecampaign"; });\n'
    '    if (eigene.length) neu = eigene;\n',
    "@@eigene-zuerst")

t = ersetze(
    t,
    "          (e.preheader ? '<button class=\"btn\" data-kopie=\"preheader\">Vorschautext kopieren</button>' : \"\") +\n",
    "          (e.preheader ? '<button class=\"btn\" data-kopie=\"preheader\">Vorschautext kopieren</button>' : \"\") +\n"
    "          /* @@text-kopieren */\n"
    "          (e.text ? '<button class=\"btn\" data-kopie=\"text\">Text kopieren</button>' : \"\") +\n"
    "          (e.betreff2 ? '<button class=\"btn\" data-kopie=\"betreff2\">Zweiten Betreff kopieren</button>' : \"\") +\n",
    "@@text-kopieren")

t = ersetze(
    t,
    "          '</div><iframe class=\"mentwurfvorschau\" sandbox=\"\" title=\"Vorschau der Mail\"></iframe></div>';\n",
    "          '</div>' +\n"
    "          /* @@notiz-aufklappen */\n"
    "          (e.notiz ? '<details class=\"mentwurfnotiz\"><summary>Notiz für dich</summary><pre class=\"mailtext\">' +\n"
    "            esc(e.notiz) + '</pre></details>' : \"\") +\n"
    "          (e.text ? '<details class=\"mentwurfnotiz\"><summary>Als Text lesen</summary><pre class=\"mailtext\">' +\n"
    "            esc(e.text) + '</pre></details>' : \"\") +\n"
    "          '<iframe class=\"mentwurfvorschau\" sandbox=\"\" title=\"Vorschau der Mail\"></iframe></div>';\n",
    "@@notiz-aufklappen")

t = ersetze(
    t,
    "  .mentwurfknoepfe { display: flex; flex-wrap: wrap; gap: 8px; padding: 10px 12px; }\n",
    "  .mentwurfknoepfe { display: flex; flex-wrap: wrap; gap: 8px; padding: 10px 12px; }\n"
    "  /* @@mentwurfnotiz-css */\n"
    "  .mentwurfnotiz { padding: 0 12px 10px; }\n"
    "  .mentwurfnotiz summary { cursor: pointer; font-size: 13px; font-weight: 600; color: var(--teal); }\n",
    "@@mentwurfnotiz-css")

pfad.write_text(t, encoding="utf-8")
print("  fertig:", pfad)
