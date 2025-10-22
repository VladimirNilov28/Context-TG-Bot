-- extensions
CREATE EXTENSION IF NOT EXISTS vector;

-- документы
CREATE TABLE IF NOT EXISTS documents (
  id           bigserial PRIMARY KEY,
  source       text,
  mime         text,
  meta         jsonb DEFAULT '{}'::jsonb,
  created_at   timestamptz NOT NULL DEFAULT now()
);

-- чанки
CREATE TABLE IF NOT EXISTS chunks (
  id           bigserial PRIMARY KEY,
  document_id  bigint NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  content      text   NOT NULL,
  token_count  int    NOT NULL,
  chunk_order  int    NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now()
);

-- эмбеддинги (384 под SentenceTransformers e5-small)
CREATE TABLE IF NOT EXISTS embeddings (
  id           bigserial PRIMARY KEY,
  chunk_id     bigint NOT NULL UNIQUE REFERENCES chunks(id) ON DELETE CASCADE,
  embedding    vector(384) NOT NULL,
  model        text   NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now()
);

-- векторный индекс (cosine)
CREATE INDEX IF NOT EXISTS idx_embeddings_cosine
  ON embeddings
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 16);

-- полезные индексы
CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(document_id, chunk_order);
CREATE INDEX IF NOT EXISTS idx_documents_created ON documents(created_at DESC);
