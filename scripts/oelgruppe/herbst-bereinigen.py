"""Einmalig 05.11.2026, zweiter Durchgang: Beitrag 1 unter die 1024 Zeichen bringen, die Telegram bei einem Bild
zulässt, und die zwei Treffer aus texte-pruefen.py beheben."""
import pathlib

P = pathlib.Path(__file__).resolve().parents[2] / "outputs/telegram-posts/herbst-2026/herbst-2026-alle-beitraege.md"
t = P.read_text(encoding="utf-8")

ERSATZ = [
 ("📍 *Der Duftstreifen-Test:*\nEinen Tropfen auf ein Papier geben, 10 Minuten warten, nochmals riechen. Dein Riecher weiss es meistens besser als das Etikett.\n\n", ""),
 ("\n\nLagern: kühl, dunkel, gut verschlossen. Eine Schublade oder eine Holzkiste reicht völlig.", ""),
 ("🌌 *Kennst du das, dass du immer um dieselbe Zeit mitten in der Nacht wach liegst?*",
  "🌌 *Immer um dieselbe Zeit mitten in der Nacht wach?*"),
 ("In der Organuhr-Lehre steht der Dickdarm nicht nur fürs Körperliche, sondern auch dafür, Altes gehen zu lassen.",
  "In der Organuhr-Lehre steht der Dickdarm auch dafür, Altes gehen zu lassen."),
]
for alt, neu in ERSATZ:
    assert t.count(alt) == 1, alt
    t = t.replace(alt, neu)
P.write_text(t, encoding="utf-8")
print(len(ERSATZ), "Stellen ersetzt")
