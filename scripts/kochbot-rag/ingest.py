#!/usr/bin/env python3
"""
Kochbot-RAG Ingest

Liest alle PDFs aus rezepte/ und kochwissen/, chunkt sie, erzeugt
Embeddings via OpenAI und schreibt sie in die Supabase-Tabelle `documents`.

Idempotent: bereits ingestete Dateien werden uebersprungen (geprueft via source_file).
Mit --force werden bestehende Eintraege geloescht und neu erzeugt.

Aufruf (lokal, wo die PDFs liegen):
    cd scripts/kochbot-rag
    pip install -r requirements.txt
    cp .env.example .env   # und Werte einsetzen
    python ingest.py
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from supabase import create_client
import tiktoken


load_dotenv()

ROOT = Path(__file__).resolve().parent.parent.parent
FOLDERS: list[tuple[str, Path]] = [
    ("rezepte", ROOT / "rezepte"),
    ("kochwissen", ROOT / "kochwissen"),
]

EMBED_MODEL = "text-embedding-3-small"
EMBED_DIMS = 1536
CHUNK_TOKENS = 800
OVERLAP_TOKENS = 150
EMBED_BATCH = 100  # OpenAI erlaubt bis zu 2048 Inputs/Request, 100 ist sicherer Default


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"[FEHLER] {name} fehlt in .env")
    return value


openai_client = OpenAI(api_key=require_env("OPENAI_API_KEY"))
supabase = create_client(require_env("SUPABASE_URL"), require_env("SUPABASE_SERVICE_KEY"))
encoding = tiktoken.get_encoding("cl100k_base")


def extract_text(pdf_path: Path) -> str:
    try:
        reader = PdfReader(str(pdf_path))
        pages = [(page.extract_text() or "").strip() for page in reader.pages]
        return "\n\n".join(p for p in pages if p)
    except Exception as exc:
        print(f"  [WARN] PDF nicht lesbar ({pdf_path.name}): {exc}")
        return ""


def chunk_text(text: str) -> list[str]:
    tokens = encoding.encode(text)
    chunks: list[str] = []
    step = CHUNK_TOKENS - OVERLAP_TOKENS
    for start in range(0, len(tokens), step):
        chunk = encoding.decode(tokens[start : start + CHUNK_TOKENS]).strip()
        if chunk:
            chunks.append(chunk)
        if start + CHUNK_TOKENS >= len(tokens):
            break
    return chunks


def embed_batch(texts: list[str]) -> list[list[float]]:
    response = openai_client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [item.embedding for item in response.data]


def already_ingested(source_file: str) -> bool:
    res = (
        supabase.table("documents")
        .select("id")
        .eq("source_file", source_file)
        .limit(1)
        .execute()
    )
    return len(res.data) > 0


def delete_existing(source_file: str) -> None:
    supabase.table("documents").delete().eq("source_file", source_file).execute()


def ingest_pdf(folder: str, pdf_path: Path, force: bool) -> tuple[int, int]:
    """Returns (chunks_inserted, chunks_skipped)."""
    source_file = pdf_path.name

    if already_ingested(source_file):
        if not force:
            print(f"  [SKIP] {source_file} (schon in DB — --force ueberschreibt)")
            return (0, 1)
        delete_existing(source_file)

    text = extract_text(pdf_path)
    if not text.strip():
        print(f"  [SKIP] {source_file} (leer)")
        return (0, 1)

    chunks = chunk_text(text)
    if not chunks:
        print(f"  [SKIP] {source_file} (keine Chunks)")
        return (0, 1)

    inserted = 0
    for batch_start in range(0, len(chunks), EMBED_BATCH):
        batch = chunks[batch_start : batch_start + EMBED_BATCH]
        embeddings = embed_batch(batch)
        rows = [
            {
                "source_file": source_file,
                "source_folder": folder,
                "chunk_index": batch_start + i,
                "content": batch[i],
                "embedding": embeddings[i],
                "metadata": {"path": str(pdf_path.relative_to(ROOT))},
            }
            for i in range(len(batch))
        ]
        supabase.table("documents").insert(rows).execute()
        inserted += len(rows)

    print(f"  [OK]   {source_file}: {inserted} Chunks")
    return (inserted, 0)


def main() -> int:
    parser = argparse.ArgumentParser(description="PDFs in Supabase-Rezeptdatenbank embedden")
    parser.add_argument("--force", action="store_true", help="Bestehende Eintraege loeschen + neu erzeugen")
    parser.add_argument("--folder", choices=["rezepte", "kochwissen"], help="Nur einen Ordner verarbeiten")
    args = parser.parse_args()

    targets = [(f, p) for f, p in FOLDERS if not args.folder or f == args.folder]

    total_inserted = 0
    total_skipped = 0
    total_pdfs = 0

    for folder, path in targets:
        if not path.exists():
            print(f"[INFO] {folder}/ existiert nicht unter {path} — uebersprungen")
            continue

        pdfs = sorted(path.rglob("*.pdf"))
        print(f"\n[{folder}] {len(pdfs)} PDFs in {path}")
        total_pdfs += len(pdfs)

        for pdf in pdfs:
            ins, skip = ingest_pdf(folder, pdf, args.force)
            total_inserted += ins
            total_skipped += skip

    print(
        f"\n[FERTIG] {total_pdfs} PDFs angesehen — "
        f"{total_inserted} Chunks neu eingespielt, {total_skipped} Dateien uebersprungen"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
