"""Onboarding-Fragen für den Öl-Begleiter — das Kurzprofil jeder Testerin.

5 Fragen, sample-spezifisch (Name, welche Pröbchen, Wunsch/Gefühl, Alltag, Vorerfahrung).
Werden nacheinander gestellt; jede Antwort landet unter ihrem `key` im Profil. Der Bot
nutzt das Profil dann, um jede der 7 Etappen auf IHRE Öle + IHREN Wunsch zuzuschneiden.

Bewusst kurz + warm gehalten — Mamas mit wenig Zeit, kein Formular-Gefühl.
"""

# Reihenfolge = Abfrage-Reihenfolge. key = Profil-Feld.
FRAGEN = [
    {
        "key": "name",
        "frage": """Schön, dass du da bist. 🌿 Ich bin dein kleiner Öl-Begleiter — die nächsten 7 Tage entdecken wir zusammen deine Pröbchen, ganz in Ruhe, ein Öl nach dem anderen.

Bevor's losgeht, lern ich dich kurz kennen — nur 5 Fragen, du darfst auch per Sprachnotiz antworten.

<b>Frage 1:</b> Wie heisst du? (dein Vorname reicht)""",
    },
    {
        "key": "samples",
        "frage": """<b>Frage 2:</b> Welche Öl-Pröbchen hast du bekommen? Zähl einfach auf, was auf den Fläschchen steht — z.B. Lavendel, Zitrone, Pfefferminz, Wilde Orange, eine Mischung …

<i>Wenn du (noch) keine hast, schreib einfach „noch keine“ — dann zeig ich dir trotzdem, wie's geht.</i>""",
    },
    {
        "key": "wunsch",
        "frage": """<b>Frage 3:</b> Was wünschst du dir gerade am meisten?

<i>Zum Beispiel: mehr Ruhe am Abend, Energie am Morgen, Fokus im Chaos, oder einfach mal einen Wohlfühl-Moment nur für dich. Sag's mir in ein, zwei Sätzen.</i>""",
    },
    {
        "key": "alltag",
        "frage": """<b>Frage 4:</b> Wie sieht dein Alltag gerade aus?

<i>Kinder? Job nebenbei? Wie viel Zeit bleibt am Tag für dich? Erzähl einfach kurz — dann pass ich die Anwendungen an dein echtes Leben an, nicht an ein Wellness-Plakat.</i>""",
    },
    {
        "key": "erfahrung",
        "frage": """<b>Frage 5 (letzte):</b> Hattest du schon mal mit ätherischen Ölen zu tun, oder ist das ganz neu für dich?

<i>Ehrlich sagen ist völlig okay — dann hol ich dich genau da ab, wo du stehst. 💛</i>""",
    },
]


def frage_fuer_schritt(step: int) -> dict | None:
    """Gibt die Frage für den aktuellen Onboarding-Schritt (oder None wenn fertig)."""
    if 0 <= step < len(FRAGEN):
        return FRAGEN[step]
    return None


def ist_fertig(step: int) -> bool:
    return step >= len(FRAGEN)


def profil_zusammenfassung(profil: dict) -> str:
    """Kompakte Zusammenfassung des Profils (für /profil + Bestätigung)."""
    felder = [
        ("name", "Name"),
        ("samples", "Deine Pröbchen"),
        ("wunsch", "Dein Wunsch"),
        ("alltag", "Dein Alltag"),
        ("erfahrung", "Öl-Erfahrung"),
    ]
    zeilen = [f"<b>{label}:</b> {profil[key]}" for key, label in felder if profil.get(key)]
    return "\n".join(zeilen) if zeilen else "(noch leer)"
