"""
Sucht in den Chats die Stellen, an denen eine Idee geaeussert wurde.

Ueber Monate sind in den Gespraechen Saetze gefallen wie „das waere noch geil"
oder „irgendwann sollten wir" — und dann ging es weiter. Dieses Skript holt
genau diese Stellen heraus, damit sie im Ideenkasten landen statt im Vergessen.

Es entscheidet **nicht**, was eine gute Idee ist. Es sammelt Kandidaten, die
danach jemand durchsieht. Ein Automat, der selbst aussortiert, wuerde genau die
halbfertigen Saetze wegwerfen, um die es hier geht.

Ausgeschlossen: alles Private. Berufswahl, Garten, Kochen, Basteln und
Gesundheit sind keine Business-Ideen und haben im Cockpit nichts verloren.

Aufruf:
  python scripts/cockpit/chat-ideen-sammeln.py [zielordner] [--alle]
"""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
CHATS = Path.home() / ".claude" / "projects"

# Wendungen, mit denen Patricia Ideen aeussert.
SIGNALE = [
    r"\bw[äa]re (?:noch )?(?:geil|cool|gut|super|toll|praktisch|hilfreich|mega)",
    r"\bk[öo]nnte man\b", r"\bk[öo]nnten wir\b", r"\bkann man (?:das )?(?:auch|noch)\b",
    r"\bidee\b", r"\bvielleicht sollten wir\b", r"\bsollten wir mal\b",
    r"\birgendwann\b.{0,40}\b(?:machen|bauen|angehen)\b",
    r"\bw[üu]nsche mir\b", r"\bich h[äa]tte gern\b", r"\bich will (?:noch|mal|irgendwann)\b",
    r"\bfehlt (?:noch|mir)\b", r"\bm[üu]sste man (?:noch|mal)\b",
    r"\bdas n[äa]chste mal\b", r"\bnoch offen\b", r"\bnoch nicht umgesetzt\b",
    r"\bauf die liste\b", r"\bmerk dir\b", r"\bnicht vergessen\b",
]
MUSTER = re.compile("|".join(SIGNALE), re.I)

# Themen, die nicht ins Business-Cockpit gehoeren.
PRIVAT = re.compile(
    r"berufswahl|schnupper|gymi|garten|beet|saatgut|rezept|mealplan|kochen|"
    r"basteln|stempel|plotter|arzt|blutwert|diagnose|therapie|kinderarzt|"
    r"zeugnis|schule|lehrer", re.I)

# Zu kurz ist kein Gedanke, zu lang ist ein Auftrag.
MIN, MAX = 40, 600


def nachrichten(datei):
    """Nur was Patricia geschrieben hat — meine eigenen Antworten sind keine
    Ideen von ihr."""
    try:
        roh = datei.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return
    for zeile in roh:
        try:
            d = json.loads(zeile)
        except ValueError:
            continue
        if d.get("type") != "user":
            continue
        m = d.get("message") or {}
        c = m.get("content")
        text = ""
        if isinstance(c, str):
            text = c
        elif isinstance(c, list):
            text = " ".join(b.get("text", "") for b in c
                            if isinstance(b, dict) and b.get("type") == "text")
        text = text.strip()
        if not text or text.startswith("<") or text.startswith("["):
            continue
        yield d.get("timestamp", ""), text


def saetze(text):
    """Den Text in Saetze zerlegen, damit ein Treffer nicht die ganze
    Nachricht mitschleppt."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ziel = Path(args[0]) if args else ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    dateien = sorted(CHATS.rglob("*.jsonl"))
    if not dateien:
        sys.exit("Keine Chat-Dateien unter %s" % CHATS)

    funde, gesehen = [], set()
    for f in dateien:
        for zeitpunkt, text in nachrichten(f):
            if PRIVAT.search(text):
                continue
            for satz in saetze(text):
                if not (MIN <= len(satz) <= MAX):
                    continue
                if not MUSTER.search(satz):
                    continue
                schluessel = re.sub(r"\W+", "", satz.lower())[:70]
                if schluessel in gesehen:
                    continue
                gesehen.add(schluessel)
                tag = (zeitpunkt or "")[:10]
                funde.append({"satz": satz, "datum": tag,
                              "chat": f.stem[:8]})

    funde.sort(key=lambda x: x["datum"], reverse=True)

    (ziel / "chat-ideen.json").write_text(json.dumps(
        {"kandidaten": funde, "stand": date.today().isoformat()},
        ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d Chat-Dateien durchsucht" % len(dateien))
    print("  %d Kandidaten gefunden" % len(funde))
    print("\nZum Durchsehen:")
    for k in funde[:25]:
        print("  %s  %s" % (k["datum"], k["satz"][:96]))
    print("\nAbgelegt in: %s" % (ziel / "chat-ideen.json"))


if __name__ == "__main__":
    main()
