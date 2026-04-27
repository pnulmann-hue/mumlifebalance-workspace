-- Kochbot-RAG: Supabase-Schema fuer die Rezeptdatenbank
-- Einmalig im Supabase SQL Editor ausfuehren.

-- 1. pgvector-Erweiterung aktivieren
create extension if not exists vector;

-- 2. Documents-Tabelle (ein Eintrag pro Chunk)
create table if not exists documents (
  id            bigserial primary key,
  source_file   text     not null,
  source_folder text     not null check (source_folder in ('rezepte', 'kochwissen')),
  chunk_index   int      not null,
  content       text     not null,
  metadata      jsonb    not null default '{}'::jsonb,
  embedding     vector(1536),
  created_at    timestamptz not null default now(),
  unique (source_file, chunk_index)
);

create index if not exists documents_embedding_idx
  on documents using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

create index if not exists documents_source_file_idx on documents (source_file);
create index if not exists documents_source_folder_idx on documents (source_folder);

-- 3. RPC-Funktion fuer Vector-Search
create or replace function match_documents (
  query_embedding  vector(1536),
  match_threshold  float default 0.3,
  match_count      int   default 5,
  filter_folder    text  default null
)
returns table (
  id            bigint,
  source_file   text,
  source_folder text,
  chunk_index   int,
  content       text,
  metadata      jsonb,
  similarity    float
)
language sql stable
as $$
  select
    d.id,
    d.source_file,
    d.source_folder,
    d.chunk_index,
    d.content,
    d.metadata,
    1 - (d.embedding <=> query_embedding) as similarity
  from documents d
  where (filter_folder is null or d.source_folder = filter_folder)
    and 1 - (d.embedding <=> query_embedding) > match_threshold
  order by d.embedding <=> query_embedding
  limit match_count;
$$;
