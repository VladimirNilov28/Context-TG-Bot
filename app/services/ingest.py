"""Пайплайн загрузки: текст -> чанки -> эмбеддинги -> БД."""

from typing import Optional, Tuple, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_session
from app.db.models import Document, Chunk, Embedding
from app.services.chunking import split_text, count_tokens
from app.services.embeddings import get_embedding


def ingest_text(
    source: str,
    text: str,
    mime: str = "text/plain",
    chunk_size: int = 800,
    chunk_overlap: int = 200,
    model: Optional[str] = None,
) -> Tuple[int, List[int]]:
    """Сохраняет текст в БД: создаёт Document, Chunk-ки и Embedding-и.

    Возвращает:
      (document_id, [chunk_id, ...])
    """
    model = model or settings.EMBEDDING_MODEL

    chunks = split_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    if not chunks:
        raise ValueError("Пустой текст: нечего загружать")

    with get_session() as s:  # type: Session
        # 1) документ
        doc = Document(source=source, mime=mime, meta={})
        s.add(doc)
        s.flush()  # чтобы получить doc.id

        # 2) чанки
        chunk_ids: List[int] = []
        for idx, c in enumerate(chunks):
            ch = Chunk(
                document_id=doc.id,
                content=c,
                token_count=count_tokens(c),
                chunk_order=idx,
            )
            s.add(ch)
            s.flush()  # чтобы получить ch.id
            chunk_ids.append(ch.id)

            # 3) эмбеддинг
            vec = get_embedding(c)  # list[float] длиной settings.EMBEDDING_DIM
            emb = Embedding(
                chunk_id=ch.id,
                embedding=vec,   # pgvector.sqlalchemy принимает list[float]
                model=model,
            )
            s.add(emb)

        # commit сделает get_session()
        return doc.id, chunk_ids
