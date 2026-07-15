"""Zugriff auf die Companion-Wissensbasis (Kundenwissen) für den Öl-Begleiter.

Der doTERRA-Companion (doterra-bot.vercel.app) speichert das Produkt-/Öl-Wissen, auf
das Patricias Kundinnen Zugriff haben, in der Supabase-Tabelle `documents` mit
`category = "product"` (Enjoils-Hefte + Produktwissen). GENAU DIESES WISSEN nutzt der
Öl-Begleiter — damit er keine Öl-Fakten erfindet, sondern nur das weitergibt, was im
Companion steht.

Retrieval-Strategie (bewusst simpel + robust, wie der doterra-bot selbst es macht:
`.eq("category","product").ilike(...)`):
  Für jedes Öl aus dem Sample-Set der Testerin holen wir passende Produkt-Dokumente
  per Text-Match auf `content`. Die Treffer werden zu EINEM Wissens-Block verdichtet,
  den das Bot-Gehirn in den Prompt bekommt.

Fehlt die Supabase-Anbindung (z.B. .env nicht gesetzt in der Sandbox), degradiert das
Modul sauber: es gibt einen leeren Block zurück, und die Compliance-Regeln im
System-Prompt verbieten dem Bot, Öl-Wissen zu erfinden.

Benötigte ENV (dieselben wie beim Companion):
  SUPABASE_URL
  SUPABASE_SERVICE_KEY   (oder SUPABASE_SERVICE_ROLE_KEY)
"""

from __future__ import annotations

import logging
import os
import re

logger = logging.getLogger(__name__)

# Companion nutzt category="product" für das Kunden-Produktwissen.
PRODUCT_CATEGORY = "product"

# Wie viele Dokumente pro Öl + wie viel Text pro Dokument wir mitnehmen.
DOCS_PRO_OEL = 3
CHARS_PRO_DOC = 900
GESAMT_MAX_CHARS = 6000

_client = None
_checked = False


def _get_client():
    """Lazy Supabase-Client. None wenn nicht konfiguriert/installiert."""
    global _client, _checked
    if _checked:
        return _client
    _checked = True
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_SERVICE_KEY", "") or os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    if not url or not key:
        logger.info("Companion-KB: SUPABASE_URL / SERVICE_KEY fehlen — laufe ohne Kundenwissen.")
        return None
    try:
        from supabase import create_client
        _client = create_client(url, key)
        logger.info("Companion-KB: mit Supabase verbunden (documents, category=product).")
    except Exception as e:
        logger.warning(f"Companion-KB: Supabase-Client nicht verfügbar ({e}).")
        _client = None
    return _client


def verfuegbar() -> bool:
    return _get_client() is not None


# Öle-Namen aus der freien Sample-Angabe der Testerin herausziehen.
# Bekannte doTERRA-Öle + Mischungen (deutsche + englische Schreibweisen), damit wir
# gezielt suchen können statt den ganzen Fliesstext als Query zu nehmen.
BEKANNTE_OELE = [
    "Lavendel", "Lavender",
    "Zitrone", "Lemon",
    "Pfefferminz", "Pfefferminze", "Peppermint",
    "Wilde Orange", "Wild Orange", "Orange",
    "Weihrauch", "Frankincense",
    "Teebaum", "Melaleuca", "Tea Tree",
    "Oregano",
    "Zitronengras", "Lemongrass",
    "Eukalyptus", "Eucalyptus",
    "Rosmarin", "Rosemary",
    "Grapefruit",
    "Bergamotte", "Bergamot",
    "Copaiba",
    "Ingwer", "Ginger",
    "Kamille", "Roman Chamomile",
    "Muskatellersalbei", "Clary Sage",
    "Cedarwood", "Zedernholz",
    "Vetiver",
    "Weißtanne", "Weisstanne", "Douglas Fir", "Siberian Fir",
    # doTERRA-Mischungen (korrekte aktuelle Namen)
    "Balance", "Serenity", "Adaptiv", "On Guard", "OnGuard",
    "Air", "Deep Blue", "Easy Air", "DigestZen", "Zendocrine",
    "Motivate", "Cheer", "Console", "Peace", "Forgive", "Passion",
    "MetaPWR", "Smart & Sassy", "Slim & Sassy", "PastTense", "TerraShield",
]


def erkenne_oele(sample_text: str) -> list[str]:
    """Findet bekannte Öl-Namen in der freien Sample-Angabe. Fallback: leere Liste."""
    if not sample_text:
        return []
    gefunden: list[str] = []
    low = sample_text.lower()
    for oel in BEKANNTE_OELE:
        if oel.lower() in low and oel not in gefunden:
            gefunden.append(oel)
    return gefunden


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _hole_docs_fuer_oel(client, oel: str) -> list[dict]:
    try:
        resp = (
            client.table("documents")
            .select("content, source_file")
            .eq("category", PRODUCT_CATEGORY)
            .ilike("content", f"%{oel}%")
            .limit(DOCS_PRO_OEL)
            .execute()
        )
        return resp.data or []
    except Exception as e:
        logger.warning(f"Companion-KB: Abfrage für '{oel}' fehlgeschlagen ({e}).")
        return []


def hole_kundenwissen(sample_text: str, wunsch: str = "") -> str:
    """Baut den Companion-Wissens-Block für die Öle der Testerin.

    Gibt "" zurück, wenn keine Anbindung oder keine Treffer — dann arbeitet der Bot
    ohne erfundene Fakten weiter.
    """
    client = _get_client()
    if client is None:
        return ""

    oele = erkenne_oele(sample_text)
    if not oele:
        # Kein bekanntes Öl erkannt → generische Suche nach dem Wunsch, damit die
        # Testerin trotzdem echtes Companion-Wissen bekommt.
        oele = [wunsch] if wunsch else []
    if not oele:
        return ""

    seen_sources: set[str] = set()
    teile: list[str] = []
    gesamt = 0
    for oel in oele:
        for d in _hole_docs_fuer_oel(client, oel):
            src = d.get("source_file", "Companion")
            content = _clean(d.get("content", ""))
            if not content:
                continue
            key = f"{src}:{content[:60]}"
            if key in seen_sources:
                continue
            seen_sources.add(key)
            snippet = content[:CHARS_PRO_DOC]
            block = f"### {oel} — Quelle: {src}\n{snippet}"
            if gesamt + len(block) > GESAMT_MAX_CHARS:
                break
            teile.append(block)
            gesamt += len(block)
        if gesamt >= GESAMT_MAX_CHARS:
            break

    if not teile:
        return ""
    logger.info(f"Companion-KB: {len(teile)} Wissens-Blöcke für {oele} geladen.")
    return "\n\n".join(teile)


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    probe = sys.argv[1] if len(sys.argv) > 1 else "Lavendel, Zitrone, Wilde Orange"
    print(f"Verbunden: {verfuegbar()}")
    print(f"Erkannte Öle: {erkenne_oele(probe)}")
    block = hole_kundenwissen(probe, "Ruhe am Abend")
    print("\n--- Kundenwissen ---\n" + (block or "(leer — keine Anbindung/Treffer)"))
