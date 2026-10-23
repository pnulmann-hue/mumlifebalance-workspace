# -*- coding: utf-8 -*-
"""Das letzte Modul jedes Signature-Kurses: die Einladung in die Mum Business Academy.

    python scripts/mba-modul/bauen.py
    # -> outputs/produkte/mba-modul/<kurs>.html (zum Einfügen ins </> HTML-Element in ThriveCart Learn)
    # -> outputs/produkte/mba-modul/vorschau.html (alle vier zum Ansehen)

Patricias Entscheid 23.10.2026: am Schluss jedes Signature-Kurses nur noch die MBA, Weg zum Kauf über
WhatsApp. Upgrade in den ersten zwei Monaten nach dem Kauf für 997 minus den bezahlten Kurs
(angerechnet werden nur Signature-Kurse). Easy KI ist einer der Kurse, kein Anhängsel am Schluss.

🚨 Alle Angaben direkt am Element (style="…"): ThriveCart Learn setzt bei p, ul und li die Abstände und
Aufzählungspunkte zurück (gemessen 22.10.2026, siehe CLAUDE.md). Deshalb keine <ul>, sondern Tabellen.
🚨 Die vier Kurskarten sind ein Flex-Raster (flex:1 1 240px), keine Tabelle: als 2×2-Tabelle ragte die rechte
Spalte am Handy über den Rand (23.10.2026). So rutschen sie unter 500 px untereinander.
"""
import html
import pathlib
import sys
import urllib.parse

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
ZIEL = ROOT / "outputs" / "produkte" / "mba-modul"
WHATSAPP = "41793591937"

NACHT, PETROL, ORANGE, CREME, GRAU = "#0c1c30", "#12828c", "#dc822e", "#f1ecdd", "#5c6b75"
SERIF = "'Philosopher',Georgia,serif"
SANS = "'Source Sans 3','Source Sans Pro',Arial,sans-serif"

KURSE = [
    ("ikm", "Instagram-Kundenmaschine",
     "Eine Instagram-Routine, aus der Gespräche werden: mit Kundschaft und mit neuen Leuten fürs Team."),
    ("ceo", "Mama-CEO",
     "Ein Wochenrhythmus, der mit Kindern funktioniert, und ein KI-Team, das dir den Adminkram abnimmt."),
    ("dpw", "Digitale Produktwelt",
     "Dein eigenes digitales Produkt neben dem Network, vom Workbook bis zur Kasse, die verkauft, während du offline bist."),
    ("ki", "Easy KI für Networkerinnen",
     "Deine KI wird zur Mitarbeiterin: mit deinem Wissen, eigenen Aufträgen und einem Helfer, der sich von selbst meldet."),
]

JAHR = [
    ("Zwei Live-Calls im Monat", "ein ganzes Jahr lang, für deine Fragen und deine Umsetzung"),
    ("PIA, deine KI-Mentorin", "sie kennt dein Business und hilft dir bei Bio, Hooks, Produkt und Funnel"),
    ("Die Telegram-Gruppe", "in der ich persönlich antworte"),
]


def karte(name, nutzen, schon_da):
    rand = PETROL if schon_da else "#e3dccb"
    marke = (f'<div style="display:inline-block;margin:0 0 10px 0;padding:3px 10px;border-radius:99px;'
             f'background:{PETROL};color:#fff;font:700 11px/1.4 {SANS};letter-spacing:1px;text-transform:uppercase;">'
             f'hast du schon</div>') if schon_da else ""
    return (f'<div style="flex:1 1 240px;box-sizing:border-box;'
            f'background:#fff;border:2px solid {rand};border-radius:14px;padding:18px 18px 16px;">'
            f'{marke}<div style="font:700 19px/1.3 {SERIF};color:{NACHT};margin:0 0 6px 0;">{html.escape(name)}</div>'
            f'<div style="font:400 15px/1.6 {SANS};color:{GRAU};margin:0;">{html.escape(nutzen)}</div></div>')


def baustein(kurs_id):
    name = next(n for k, n, _ in KURSE if k == kurs_id)
    karten = [karte(n, t, k == kurs_id) for k, n, t in KURSE]
    zeilen = "".join(karten)
    jahr = "".join(
        f'<tr><td valign="top" style="width:30px;padding:6px 0;font:700 18px/1.4 {SANS};color:{ORANGE};">✓</td>'
        f'<td style="padding:6px 0;font:400 16px/1.55 {SANS};color:{CREME};"><strong style="color:#fff;">{html.escape(t)}</strong>'
        f' – {html.escape(d)}</td></tr>' for t, d in JAHR)
    wa = "https://wa.me/%s?text=%s" % (WHATSAPP, urllib.parse.quote(
        f"Hallo Patricia, ich habe {name} gemacht und interessiere mich für die MBA."))
    return f"""<div style="max-width:760px;margin:0;font-family:{SANS};color:{NACHT};">
<div style="background:{CREME};border-radius:18px;padding:30px 26px;margin:0 0 18px 0;">
<div style="font:700 12px/1.4 {SANS};letter-spacing:2px;text-transform:uppercase;color:{ORANGE};margin:0 0 10px 0;">Wie es weitergeht</div>
<div style="font:700 30px/1.25 {SERIF};color:{NACHT};margin:0 0 14px 0;">Das war ein Stück. In der Mum Business Academy hängt alles zusammen.</div>
<p style="font:400 17px/1.7 {SANS};color:{NACHT};margin:0;">Du hast <strong>{html.escape(name)}</strong> durchgearbeitet. In der MBA bekommst du die anderen Teile dazu, und sie greifen ineinander: Sichtbarkeit, Struktur, dein eigenes Produkt und KI, die mitarbeitet.</p>
</div>
<div style="display:flex;flex-wrap:wrap;gap:14px;margin:0 0 18px 0;">{zeilen}</div>
<div style="background:{NACHT};border-radius:18px;padding:26px;margin:0 0 18px 0;">
<div style="font:700 21px/1.3 {SERIF};color:#fff;margin:0 0 12px 0;">Und ein ganzes Jahr Begleitung dazu</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="width:100%;">{jahr}</table>
</div>
<div style="border:2px solid {ORANGE};border-radius:18px;padding:26px;text-align:center;background:#fff;">
<div style="font:400 15px/1.5 {SANS};color:{GRAU};margin:0 0 4px 0;">Listenpreis <s>1347 CHF</s></div>
<div style="font:700 40px/1.15 {SERIF};color:{NACHT};margin:0 0 8px 0;">997 CHF</div>
<p style="font:400 16px/1.65 {SANS};color:{NACHT};margin:0 0 20px 0;">In den ersten zwei Monaten nach deinem Kauf – und <strong>{html.escape(name)}</strong> rechne ich dir voll an. Du zahlst nur die Differenz.</p>
<a href="{html.escape(wa)}" target="_blank" rel="noopener" style="display:inline-block;background:{ORANGE};color:#fff;text-decoration:none;font:700 17px/1.2 {SANS};padding:16px 30px;border-radius:99px;">Schreib mir auf WhatsApp →</a>
<p style="font:400 14px/1.6 {SANS};color:{GRAU};margin:14px 0 0 0;">Wir schauen zusammen, ob die MBA für dich passt, und ich sag dir deinen genauen Preis.</p>
</div>
</div>"""


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    teile = []
    for k, name, _ in KURSE:
        b = baustein(k)
        (ZIEL / f"{k}.html").write_text(b, encoding="utf-8")
        teile.append(f'<h1 style="font-family:Arial;font-size:14px;color:#888;margin:40px 0 10px">{html.escape(name)}</h1>{b}')
        print(f"{k}.html  ({len(b)} Zeichen)")
    (ZIEL / "vorschau.html").write_text(
        '<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@400;700&display=swap" rel="stylesheet">'
        '<title>MBA-Modul Vorschau</title></head><body style="margin:0;padding:16px;background:#f6f6f6">'
        + "".join(teile) + "</body></html>", encoding="utf-8")
    print("Vorschau:", ZIEL / "vorschau.html")


if __name__ == "__main__":
    main()
