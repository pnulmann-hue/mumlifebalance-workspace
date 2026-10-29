"""HTML-Bloecke fuer Upsell (Instagram-Kundenmaschine 199) und Downsell (Startklar 39) nach der Tool-Workshop-Kasse.

    python scripts/salespage-design/tool-workshop-funnel-bloecke.py

Schreibt je Waehrung eine Datei nach outputs/salespages/tool-workshop-checkout/. Der Inhalt kommt in ThriveCart
in ein HTML-Element oben auf der Upsell- bzw. Downsell-Seite; die Knoepfe darunter bleiben ThriveCarts eigene.
Alle Stile stehen am Element, weil ThriveCart Listen und Absaetze zuruecksetzt (siehe CLAUDE.md, Produktionsseite).
Upsell-Texte aus Patricias bestehender Upsell-Seite der Kundenmaschine, ohne „nicht …, sondern“.
"""
import pathlib

ZIEL = pathlib.Path(__file__).resolve().parents[2] / "outputs/salespages/tool-workshop-checkout"
F = {"tinte": "#0c1c30", "blau": "#29556d", "petrol": "#12828c", "orange": "#dc822e", "creme": "#f1ecdd", "weiss": "#fbf8f0", "grau": "#4f5d68"}
SERIF = "font-family:'Philosopher',Georgia,serif;"
FONT = ""  # Kasse laedt keine Fremdschriften, Georgia springt ein (wie im Kassen-Block)
MOCKUP_IKM = "https://assets.thrivecart.com/user_assets/DKLHT16M/uploads/images/mockup-1768988410.JPG"


def haken(punkte):
    li = "".join(
        f'<li style="margin:0 0 10px;padding-left:30px;position:relative;font-size:17px;line-height:1.45;list-style:none;">'
        f'<span style="position:absolute;left:0;top:0;color:{F["orange"]};font-weight:800;">✓</span>{p}</li>' for p in punkte)
    return f'<ul style="list-style:none;padding:0;margin:0 0 20px;">{li}</ul>'


def preis(alt, neu, unter):
    streich = (f'<span style="font-size:17px;color:#d5e0e6;">Normalerweise <s>{alt}</s></span><br>' if alt else "")
    return (f'<div style="background:{F["blau"]};color:#fff;border-radius:16px;padding:20px 22px;text-align:center;margin:0 0 18px;">'
            f'{streich}<span style="{SERIF}font-size:44px;line-height:1.1;color:#fff;">{neu}</span><br>'
            f'<span style="font-size:15px;letter-spacing:.06em;text-transform:uppercase;color:#f3c38f;font-weight:700;">{unter}</span></div>')


def rahmen(inhalt):
    return (FONT + f'<div style="font-family:\'Source Sans 3\',\'Source Sans Pro\',\'Segoe UI\',Arial,sans-serif;color:{F["tinte"]};'
            f'max-width:680px;margin:0 auto;background:{F["creme"]};border-radius:22px;padding:28px 22px;">{inhalt}</div>')


def pille(text):
    return (f'<p style="margin:0 0 14px;text-align:center;"><span style="display:inline-block;background:{F["orange"]};color:#fff;'
            f'font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;border-radius:999px;padding:7px 16px;">{text}</span></p>')


def titel(text):
    return f'<h2 style="{SERIF}font-size:32px;line-height:1.15;color:{F["blau"]};text-align:center;margin:0 0 18px;">{text}</h2>'


def absatz(text, extra=""):
    return f'<p style="margin:0 0 14px;font-size:17px;line-height:1.6;{extra}">{text}</p>'


def handy():
    """Kleines Handy aus HTML als Startklar-Mockup (es gibt kein Produktbild)."""
    zeile = lambda txt, an: (f'<div style="display:flex;align-items:center;gap:8px;background:#fff;border-radius:10px;padding:8px 10px;margin:0 0 7px;'
                             f'font-size:14px;font-weight:600;color:{F["tinte"]};"><span style="width:18px;height:18px;border-radius:50%;flex:none;'
                             f'background:{F["orange"] if an else F["creme"]};color:#fff;font-size:12px;line-height:18px;text-align:center;">{"✓" if an else ""}</span>{txt}</div>')
    return (f'<div style="background:{F["tinte"]};border-radius:16px;padding:22px 12px;margin:0 0 20px;text-align:center;">'
            f'<div style="display:inline-block;width:210px;background:#1d2d42;border-radius:30px;padding:10px;text-align:left;">'
            f'<div style="background:{F["creme"]};border-radius:22px;padding:22px 14px 16px;">'
            f'<div style="{SERIF}font-size:24px;line-height:1.1;color:{F["blau"]};margin:0 0 4px;">Startklar</div>'
            f'<div style="font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:{F["petrol"]};margin:0 0 12px;">Deine Werkstatt</div>'
            + zeile("Profil", True) + zeile("Bio", True) + zeile("Erstes Reel", False)
            + '</div></div></div>')


def upsell(w):
    return rahmen(
        pille("Juhuu, du bist beim Tool-Workshop dabei!")
        + titel("Und wenn die Kontakte kommen, was dann?")
        + absatz("Nach den zwei Abenden ist dein Tool online, und die ersten Leute füllen es aus. Genau dann kommt meistens die "
                 "nächste Frage: Wie wird aus diesen Kontakten Kundschaft, ohne dass ich mich aufdränge? Dafür ist die "
                 "Instagram-Kundenmaschine da.")
        + f'<div style="background:{F["tinte"]};border-radius:16px;padding:12px;margin:0 0 20px;">'
          f'<img src="{MOCKUP_IKM}" alt="Die Instagram-Kundenmaschine auf Laptop, Tablet und Handy" style="display:block;width:100%;height:auto;border-radius:10px;"></div>'
        + absatz("<strong>Du baust den ganzen Weg von der ersten Story bis zur Anfrage, in deinem Tempo, zwischen Kindern und Alltag.</strong>")
        + preis(f"333 {w}", f"199 {w}", "direkt nach deiner Anmeldung")
        + f'<p style="margin:0 0 8px;font-size:17px;font-weight:700;color:{F["blau"]};">Das baust du dir auf:</p>'
        + haken(["<strong>Klarheit:</strong> deine Rolle auf Instagram, deine Zielgruppe und deine Content-Säulen",
                 "<strong>Ideen ohne Kreativdruck:</strong> Content entlang deiner Säulen planen und KI sinnvoll nutzen",
                 "<strong>Storys und Beiträge:</strong> aus einer Idee mehrere Formate machen",
                 "<strong>Deine Routine im Mama-Alltag:</strong> von Reaktionen zu Gesprächen, ohne Druck",
                 "Telegram-Gruppe mit Antworten am Dienstag und Donnerstag",
                 "Dauerhafter Zugriff auf alles, mit allen Updates"])
        + absatz("Ist das für jede? Ehrlich gesagt nein. Aber es ist für jede Networkerin, die genug davon hat, alles allein "
                 "herauszufinden und trotzdem auf der Stelle zu treten.",
                 f"background:{F['weiss']};border-left:4px solid {F['petrol']};border-radius:10px;padding:12px 16px;font-style:italic;")
        + absatz(f"Regulär kostet die Instagram-Kundenmaschine 333 {w}. Die 199 {w} gelten hier, direkt nach deiner Anmeldung.",
                 "text-align:center;font-weight:700;margin:0;"))


def downsell(w):
    return rahmen(
        pille("Moment, eine Sache noch")
        + titel("Lieber erst mit einem kleinen Schritt anfangen?")
        + absatz("Dein Tool schickt Leute auf dein Profil. Mit Startklar verstehen sie dort sofort, wofür du stehst.")
        + handy()
        + haken(["Ein Profil, das sagt, wofür du stehst",
                 "Eine Bio, die zu deinem Thema passt",
                 "Dein erstes Reel"])
        + preis("", f"39 {w}", "einmalig, mit der Startklar-Werkstatt"))


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    for w, k in (("CHF", "chf"), ("€", "eur")):
        for name, fn in (("upsell", upsell), ("downsell", downsell)):
            html = fn(w)
            assert "sondern" not in html and "ß" not in html
            (ZIEL / f"{name}-block-{k}.html").write_text(html, encoding="utf-8")
            print("->", f"{name}-block-{k}.html", len(html))


if __name__ == "__main__":
    main()
