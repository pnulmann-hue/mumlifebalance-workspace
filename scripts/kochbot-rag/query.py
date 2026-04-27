#!/usr/bin/env python3
"""
Kochbot-RAG Query

Durchsucht die Supabase-Rezeptdatenbank via Vector-Similarity.
Wird sowohl von der CLI als auch vom /mealplan-Slash-Command aufgerufen.

CLI-Beispiele:
    python query.py "Quark Pancakes proteinreich"
    python query.py "Sauerteig falten" --folder kochwissen --top 8
    python query.py "Zucchini verarbeiten" --format json

Standard-Output ist Text (gut lesbar fuer Claude).
JSON-Output ist fuer Skript-Integration.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client


load_dotenv()

EMBED_MODEL = "text-embedding-3-small"


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"[FEHLER] {name} fehlt in .env (scripts/kochbot-rag/.env)")
    return value


openai_client = OpenAI(api_key=require_env("OPENAI_API_KEY"))
supabase = create_client(require_env("SUPABASE_URL"), require_env("SUPABASE_SERVICE_KEY"))


def search(query: str, top: int, threshold: float, folder: str | None) -> list[dict]:
    embedding = (
        openai_client.embeddings.create(model=EMBED_MODEL, input=query)
        .data[0]
        .embedding
    )
    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": embedding,
            "match_threshold": threshold,
            "match_count": top,
            "filter_folder": folder,
        },
    ).execute()
    return response.data or []


def print_text(query: str, results: list[dict]) -> None:
    if not results:
        print(f"Keine Treffer fuer: {query}")
        return
    print(f"\n{len(results)} Treffer fuer: {query}\n")
    for i, r in enumerate(results, 1):
        score = r.get("similarity", 0.0)
        print(f"--- {i}. [{r['source_folder']}] {r['source_file']} (Score {score:.2f}) ---")
        content = r["content"]
        if len(content) > 1200:
            content = content[:1200] + "..."
        print(content)
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Kochbot-Rezeptdatenbank durchsuchen")
    parser.add_argument("query", help="Suchanfrage (frei formuliert, z.B. 'protein quark fruehstueck')")
    parser.add_argument("--top", type=int, default=5, help="Wie viele Treffer (default 5)")
    parser.add_argument("--threshold", type=float, default=None, help="Cosine-Threshold (default 0.3 oder MATCH_THRESHOLD aus .env)")
    parser.add_argument("--folder", choices=["rezepte", "kochwissen"], default=None, help="Nur in einem Ordner suchen")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    threshold = args.threshold
    if threshold is None:
        threshold = float(os.environ.get("MATCH_THRESHOLD", "0.3"))

    results = search(args.query, args.top, threshold, args.folder)

    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_text(args.query, results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
