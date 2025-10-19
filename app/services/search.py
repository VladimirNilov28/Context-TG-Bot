"""Сервис поиска похожих чанков по вектору (cosine)."""

from typing import List, Dict, Any
from sqlalchemy import text
from app.db.session import get_session
from app.core.config import settings
from app.services.embeddings import ensure_dim

def search_similar(query_vector: list[float], top_k: int = 5) -> List[Dict[str, Any]]:
    qvec = ensure_dim(query_vector, settings.EMBEDDING_DIM)

    sql = text("""
        WITH q AS (
            SELECT CAST(:arr AS double precision[]) AS a
        )
        SELECT
            c.id AS chunk_id,
            c.content AS content,
            (e.embedding <=> (SELECT a FROM q)::vector) AS distance
        FROM embeddings e
        JOIN chunks c ON c.id = e.chunk_id
        ORDER BY e.embedding <=> (SELECT a FROM q)::vector
        LIMIT :k
    """)

    with get_session() as s:
        # На маленьких датасетах расширим поиск; можно дропнуть индекс на время dev
        s.execute(text("SET ivfflat.probes = 20"))
        rows = s.execute(sql, {"arr": qvec, "k": int(top_k)}).mappings().all()

        # Фолбэк на случай странного плана: отключим индексы и повторим
        if not rows:
            s.execute(text("SET enable_indexscan = off"))
            s.execute(text("SET enable_bitmapscan = off"))
            rows = s.execute(sql, {"arr": qvec, "k": int(top_k)}).mappings().all()

    return [dict(r) for r in rows]
