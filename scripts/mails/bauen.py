#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut aus den Mail-Markdowns fertige HTML-Mails in Patricias Markenfarben.

Eine Quelle (die .md), eine Ausgabe je Mail. Wer eine Mail aendert, aendert die
Markdown und laesst das hier laufen — sonst laufen Text und HTML auseinander,
und irgendwann verschickt jemand die alte Fassung.

    python scripts/mails/bauen.py
"""
import io, os, re, sys, html

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASIS = os.path.join(WURZEL, "outputs/produkte/doterra-mama-energie")
ZIEL = os.path.join(BASIS, "mails")

# Markenfarben — dieselben wie auf der Verkaufsseite. Kein Braun, kein Gelb.
C = dict(creme="#f1ecdd", weiss="#ffffff", tinte="#0c1c30", tinte2="#14314f",
         petrol="#12828c", petrolhell="#dfe9e8", petrol2="#9ecdd0",
         orange="#dc822e", orangetief="#b4661f", orangesoft="#f7e2cd",
         rand="#e8c9a4", grau="#5c6b75", grau2="#3d5260")

QUELLEN = [
    (os.path.join(BASIS, "05-freebie-mails-kickstart.md"), "kickstart", "3-Tage-Energie-Kickstart"),
    (os.path.join(BASIS, "14-launch-mails-september.md"), "launch", "30-Tage-Energie-Routine"),
]


def mails_lesen(pfad, art):
    """Zerlegt die Markdown in einzelne Mails."""
    t = open(pfad, encoding="utf-8").read()
    kopf = r"^##\s*(?:📧\s*)?MAIL\s*(\d)" if art == "kickstart" else r"^##\s*Mail\s*(\d)"
    stellen = [(m.start(), m.group(1), m.group(0)) for m in
               re.finditer(kopf, t, re.M | re.I)]
    aus = []
    for i, (pos, nr, zeile) in enumerate(stellen):
        ende = stellen[i + 1][0] if i + 1 < len(stellen) else len(t)
        block = t[pos:ende]
        titel = t[pos:t.index("\n", pos)].lstrip("# ").strip()
        betreff = re.search(r"\*\*Betreff:\*\*\s*(.+)", block)
        pre = re.search(r"\*\*Preheader:\*\*\s*(.+)", block)
        # Der Rumpf beginnt nach dem ersten --- unter dem Preheader und geht bis
        # zur naechsten Mail. 🚨 NICHT beim naechsten --- abschneiden: Mail 3 hat
        # mittendrin eine Trennlinie, und damit fehlte die halbe Mail.
        teile = block.split("\n---\n", 1)
        rumpf = teile[1] if len(teile) > 1 else block
        zeilen = []
        for z in rumpf.split("\n"):
            s = z.strip()
            if s.startswith(">"):          # Redaktionshinweis, nicht fuer die Leserin
                continue
            if re.fullmatch(r"-{3,}", s):  # Trennlinie
                continue
            if s.startswith("## ") or s.startswith("# "):
                break                      # naechster Abschnitt
            zeilen.append(z)
        rumpf = "\n".join(zeilen)
        aus.append(dict(nr=nr, titel=titel,
                        betreff=(betreff.group(1).strip() if betreff else ""),
                        pre=(pre.group(1).strip() if pre else ""),
                        rumpf=rumpf.strip()))
    return aus


def inline(s):
    """**fett** → <strong>, *kursiv* → <em>, [text](url) → <a>."""
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
               rf'<a href="\2" style="color:{C["orangetief"]};font-weight:bold;">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", s)
    return s


def absatz(text, klein=False, kursiv=False):
    gr = "14px" if klein else "16px"
    farbe = C["grau"] if klein else C["tinte"]
    st = f"font-style:italic;" if kursiv else ""
    return (f'<p style="margin:0 0 18px 0;font-family:Arial,sans-serif;font-size:{gr};'
            f'color:{farbe};line-height:1.7;{st}">{inline(text)}</p>')


def knopf(text, url):
    return (f'<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:22px 0;">'
            f'<tr><td align="center">'
            f'<a href="{url}" style="display:inline-block;background-color:{C["orange"]};color:#ffffff;'
            f'font-family:Arial,sans-serif;font-size:15px;font-weight:bold;text-decoration:none;'
            f'padding:15px 34px;border-radius:100px;">{html.escape(text)} &#8594;</a>'
            f"</td></tr></table>")


def rumpf_bauen(rumpf):
    """Markdown-Absaetze → E-Mail-taugliches HTML."""
    aus = []
    for roh in re.split(r"\n\s*\n", rumpf):
        z = roh.strip()
        if not z or z.startswith(("|", "#", ">")):
            continue
        # Ein Absatz, der NUR aus einem Link-Pfeil besteht, wird ein Knopf
        # %CONFIRMLINK% ist der Bestaetigungslink, den ActiveCampaign in der
        # Opt-in-Mail selbst einsetzt
        m = re.fullmatch(r"\*\*→\s*\[([^\]]+)\]\((https?://[^)]+|%CONFIRMLINK%)\)\*\*", z)
        if m:
            aus.append(knopf(m.group(1), m.group(2)))
            continue
        # Aufzaehlungen als Liste, nicht als Absatzbrei
        if all(l.strip().startswith(("- ", "* ")) for l in z.split("\n") if l.strip()):
            punkte = "".join(
                f'<li style="margin:0 0 9px 0;">{inline(l.strip()[2:])}</li>'
                for l in z.split("\n") if l.strip())
            aus.append(f'<ul style="margin:0 0 18px 0;padding-left:22px;font-family:Arial,sans-serif;'
                       f'font-size:16px;color:{C["tinte"]};line-height:1.7;">{punkte}</ul>')
            continue
        z = z.replace("\n", " ")
        if z.startswith("*P.S.") or z.startswith("*p.s."):
            aus.append(absatz(z.strip("*"), klein=True, kursiv=True))
        elif z.startswith("*") and z.endswith("*") and len(z) > 80:
            # kursiver Hinweisblock
            aus.append(f'<table width="100%" cellpadding="0" cellspacing="0" border="0" '
                       f'style="margin:0 0 22px 0;"><tr><td style="background-color:{C["creme"]};'
                       f'border-radius:12px;padding:18px 22px;">'
                       f'<p style="margin:0;font-family:Arial,sans-serif;font-style:italic;'
                       f'font-size:14px;color:{C["grau2"]};line-height:1.7;">'
                       f'{inline(z.strip("*"))}</p></td></tr></table>')
        elif z.startswith("**") and z.rstrip().endswith("**") and len(z) < 90:
            aus.append(f'<p style="margin:26px 0 14px 0;font-family:Georgia,serif;font-size:20px;'
                       f'font-weight:bold;color:{C["petrol"]};line-height:1.4;">'
                       f'{html.escape(z.strip("*"))}</p>')
        elif z.startswith("Alles Liebe"):
            aus.append(absatz(z))
        elif z.strip() == "Patricia":
            aus.append(f'<p style="margin:0 0 24px 0;font-family:Georgia,serif;font-size:20px;'
                       f'color:{C["petrol"]};line-height:1.4;">Patricia</p>')
        else:
            aus.append(absatz(z))
    return "\n              ".join(aus)


def seite(m, badge, absender=False):
    # Die Opt-in-Mail geht ausserhalb jeder Kampagne raus — dort setzt AC die
    # Absenderadresse nicht von selbst darunter, also steht sie im Fuss.
    fuss_extra = (f'\n          <p style="margin:12px 0 0 0;font-family:Arial,sans-serif;font-size:11px;'
                  f'color:{C["petrol2"]};line-height:1.6;">Gesendet an %EMAIL% &middot; '
                  f'%SENDER-INFO-SINGLELINE%</p>') if absender else ""
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(m["betreff"])}</title>
</head>
<body style="margin:0;padding:0;background-color:{C['creme']};font-family:Arial,sans-serif;">
  <!-- Betreff:   {html.escape(m["betreff"])} -->
  <!-- Preheader: {html.escape(m["pre"])} -->
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{C['creme']};">
    <tr><td align="center" style="padding:30px 16px;">
      <table width="620" cellpadding="0" cellspacing="0" border="0" style="max-width:620px;width:100%;">

        <tr><td style="background-color:{C['tinte']};background:linear-gradient(135deg,{C['tinte']} 0%,{C['tinte2']} 60%,{C['petrol']} 100%);border-radius:16px 16px 0 0;padding:44px 40px;">
          <table cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;"><tr><td bgcolor="{C['orange']}" style="background-color:{C['orange']};border-radius:20px;padding:6px 14px;color:#ffffff;font-family:Arial,sans-serif;font-size:11px;font-weight:bold;letter-spacing:2px;line-height:1.5;text-transform:uppercase;">{html.escape(badge)}</td></tr></table>
          <h1 style="margin:18px 0 0 0;font-family:Georgia,serif;font-size:29px;font-weight:bold;color:{C['creme']};line-height:1.3;">{inline(m["betreff"])}</h1>
        </td></tr>

        <tr><td style="background-color:{C['weiss']};padding:40px;">
              {rumpf_bauen(m["rumpf"])}
        </td></tr>

        <tr><td style="background-color:{C['tinte']};border-radius:0 0 16px 16px;padding:26px 40px;text-align:center;">
          <p style="margin:0 0 6px 0;font-family:Arial,sans-serif;font-size:13px;font-weight:bold;color:{C['creme']};text-transform:uppercase;letter-spacing:1px;">Patricia Ulmann &middot; Mum Life Balance</p>
          <p style="margin:0;font-family:Arial,sans-serif;font-size:12px;color:{C['petrol2']};">Natürlich mehr Energie im Mama-Alltag</p>{fuss_extra}
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""


def main():
    os.makedirs(ZIEL, exist_ok=True)
    gesamt = 0
    for pfad, art, badge_basis in QUELLEN:
        if not os.path.exists(pfad):
            print("fehlt:", pfad); continue
        mails = mails_lesen(pfad, art)
        print(f"\n{os.path.basename(pfad)} — {len(mails)} Mails")
        for m in mails:
            tag = re.search(r"Tag (\d)", m["titel"])
            if art == "kickstart" and m["nr"] == "0":
                badge = f"{badge_basis} · Bestätigung"
            else:
                badge = f"{badge_basis} · {'Tag ' + tag.group(1) if tag else 'Mail ' + m['nr']}"
            datei = f"{art}-mail-{m['nr']}.html"
            # Mail 1 des Kickstarts ist von Hand gebaut und bleibt, wie sie ist
            # Mail 1 und 2 des Kickstarts sind aus Patricias AC-Fassung von Hand
            # gebaut (sie weicht von der Markdown ab) — nicht ueberschreiben.
            if datei in ("kickstart-mail-1.html", "kickstart-mail-2.html", "kickstart-mail-3.html"):
                print(f"  {datei:26s} übersprungen (von Hand gebaut)"); continue
            opt_in = art == "kickstart" and m["nr"] == "0"
            open(os.path.join(ZIEL, datei), "w", encoding="utf-8").write(seite(m, badge, absender=opt_in))
            print(f"  {datei:26s} {len(m['rumpf']):5d} Zeichen | {m['betreff'][:46]}")
            gesamt += 1
    print(f"\n{gesamt} Mails gebaut in {ZIEL}")


if __name__ == "__main__":
    main()
