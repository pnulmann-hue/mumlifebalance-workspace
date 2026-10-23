"""Öl-App — was Produkte, Themen und Tipps gemeinsam brauchen: Zugang und die geteilten Bausteine."""
import pathlib
import sys
from typing import List

from pydantic import BaseModel

WS = pathlib.Path(__file__).resolve().parents[2]


def env(name):
    for z in (WS / ".env").read_text(encoding="utf-8").splitlines():
        if z.startswith(name + "="):
            return z.split("=", 1)[1].strip().strip('"')
    sys.exit(f"❌ {name} fehlt in .env")


class Buchstelle(BaseModel):
    quelle: str      # Titel der Quelle, genau wie im Auszug
    wo: str          # Seite oder Kapitel, genau wie im Auszug
    kern: str        # was dort steht, in eigenen Worten, 1–3 Sätze


class Rezept(BaseModel):
    titel: str
    zutaten: List[str]
    anleitung: str
    quelle: str
