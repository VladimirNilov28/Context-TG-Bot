"""One-off сид данных: 1 документ, 2 чанка, 2 эмбеддинга."""
from sqlalchemy import text
from app.db.session import get_session
from app.core.config import settings

def unit(idx: int, dim: int) -> list[float]:
    """Единичный вектор по координате idx (0-based)."""
    v = [0.0] * dim
    v[idx] = 1.0
    return v

def to_literal(vec: list[float]) -> str:
    """Формат для pgvector: '[0,0.1,0.2,...]'."""
    return "[" + ",".join(str(x) for x in vec) + "]"

def main() -> None:
    dim = settings.EMBEDDING_DIM
    v1 = unit(0, dim)   # [1, 0, 0, ...]
    v2 = unit(1, dim)   # [0, 1, 0, ...]

    with get_session() as s:
        # 1) документ
        doc_id = s.execute(
            text("INSERT INTO documents(source, mime) VALUES (:src,:mime) RETURNING id"),
            {"src": "seed_demo.txt", "mime": "text/plain"},
        ).scalar_one()

        # 2) два чанка
        ch1 = s.execute(
            text("""INSERT INTO chunks(document_id, content, token_count, chunk_order)
                    VALUES (:d,:c,:t,:o) RETURNING id"""),
            {"d": doc_id, "c": "Hello world", "t": 2, "o": 0},
        ).scalar_one()

        ch2 = s.execute(
            text("""INSERT INTO chunks(document_id, content, token_count, chunk_order)
                    VALUES (:d,:c,:t,:o) RETURNING id"""),
            {"d": doc_id, "c": "Vector search demo", "t": 3, "o": 1},
        ).scalar_one()

        # 3) эмбеддинги (используем CAST из строкового литерала)
        s.execute(
            text("""INSERT INTO embeddings(chunk_id, embedding, model)
                    VALUES (:cid, CAST(:vec AS vector(:dim)), :model)"""),
            {"cid": ch1, "vec": to_literal(v1), "dim": dim, "model": "seed/unit"},
        )
        s.execute(
            text("""INSERT INTO embeddings(chunk_id, embedding, model)
                    VALUES (:cid, CAST(:vec AS vector(:dim)), :model)"""),
            {"cid": ch2, "vec": to_literal(v2), "dim": dim, "model": "seed/unit"},
        )

        # 4) счётчики
        counts = s.execute(
            text("""SELECT
                        (SELECT count(*) FROM documents) AS docs,
                        (SELECT count(*) FROM chunks)    AS chunks,
                        (SELECT count(*) FROM embeddings) AS embs""")
        ).mappings().one()

    print(f"✅ seeded: documents={counts['docs']}, chunks={counts['chunks']}, embeddings={counts['embs']}")

if __name__ == "__main__":
    main()
