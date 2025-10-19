"""Демо-ингест: сохраняем небольшой текст и печатаем счётчики."""
from sqlalchemy import text
from app.services.ingest import ingest_text
from app.db.session import get_session

DEMO_TEXT = """\
Embeddings demo. This is a short text to be split into chunks and embedded.
Vector search will use cosine distance to find the most relevant chunks.
"""

def main() -> None:
    doc_id, chunk_ids = ingest_text(source="demo.txt", text=DEMO_TEXT)

    with get_session() as s:
        counts = s.execute(
            text("""SELECT
                      (SELECT count(*) FROM documents)  AS docs,
                      (SELECT count(*) FROM chunks)     AS chunks,
                      (SELECT count(*) FROM embeddings) AS embs""")
        ).mappings().one()

    print(f"✅ ingest ok: doc_id={doc_id}, chunks={chunk_ids}")
    print(f"📊 totals: documents={counts['docs']}, chunks={counts['chunks']}, embeddings={counts['embs']}")

if __name__ == "__main__":
    main()
