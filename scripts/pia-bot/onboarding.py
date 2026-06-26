"""Onboarding-Fragen für PIA — das Kurzprofil jeder Teilnehmerin.

6 Fragen, Network-spezifisch (Firma, Thema/Transformation, Zielgruppe, Lebensphase,
Business-Stand). Werden nacheinander gestellt; jede Antwort landet unter ihrem `key`
im Profil. PIA nutzt das Profil dann für Bio, Hooks etc.

Bewusst kurz + warm gehalten — Mamas mit wenig Zeit, kein Formular-Gefühl.
"""

# Reihenfolge = Abfrage-Reihenfolge. key = Profil-Feld.
FRAGEN = [
    {
        "key": "name",
        "frage": """Schön, dass du da bist. 💛 Ich bin PIA, deine KI-Mentorin für die nächsten 5 Tage.

Bevor wir loslegen, lern ich dich kurz kennen — nur 6 Fragen, du kannst auch per Sprachnotiz antworten.

<b>Frage 1:</b> Wie heisst du? (nur dein Vorname reicht)""",
    },
    {
        "key": "firma",
        "frage": """<b>Frage 2:</b> Bei welcher Network-Firma bist du? (z.B. doTERRA, Forever, Ringana, PM … — oder „noch keine / kommt noch“)""",
    },
    {
        "key": "thema",
        "frage": """<b>Frage 3:</b> Wofür brennst du? Was möchtest du deinen Leuten eigentlich ermöglichen?

<i>Denk dabei nicht ans Produkt, sondern an die Veränderung — z.B. „dass Mamas wieder durchschlafen“, „dass Frauen sich in ihrer Haut wohlfühlen“, „mehr Selbstbestimmung neben der Familie“. Was ist dein Herzensthema?</i>""",
    },
    {
        "key": "zielgruppe",
        "frage": """<b>Frage 4:</b> Wen willst du erreichen? Beschreib mir deine Wunsch-Leserin in 1-2 Sätzen.

<i>z.B. „erschöpfte Mamas zwischen 30 und 45, die abends keine Kraft mehr haben“ oder „Frauen, die etwas Eigenes aufbauen wollen, aber nicht wissen wie“.</i>""",
    },
    {
        "key": "lebensphase",
        "frage": """<b>Frage 5:</b> Und du selbst — wo stehst du gerade im Leben?

<i>Kinder? Wie viel Zeit hast du am Tag fürs Business? Arbeitest du noch nebenbei? Erzähl einfach kurz.</i>""",
    },
    {
        "key": "stand",
        "frage": """<b>Frage 6 (letzte):</b> Wo stehst du mit deinem Business?

<i>Ganz am Anfang? Schon eine Weile dabei, aber es läuft nicht so richtig? Hast du schon Follower oder Anfragen? Sag's mir ehrlich — dann kann ich dich richtig abholen.</i>""",
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
        ("firma", "Firma"),
        ("thema", "Dein Thema"),
        ("zielgruppe", "Deine Leute"),
        ("lebensphase", "Deine Lebensphase"),
        ("stand", "Business-Stand"),
    ]
    zeilen = [f"<b>{label}:</b> {profil[key]}" for key, label in felder if profil.get(key)]
    return "\n".join(zeilen) if zeilen else "(noch leer)"
