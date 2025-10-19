"""Сервис эмбеддингов: фейковый детерминированный и задел на OpenAI."""
from typing import Iterable, List
import hashlib
import numpy as np
from app.core.config import settings


def ensure_dim(vec: Iterable[float], dim: int | None = None) -> List[float]:
    dim = dim or settings.EMBEDDING_DIM
    v = list(map(float, vec))
    if len(v) != dim:
        raise ValueError(f"Vector length {len(v)} != {dim}")
    return v


def _fake_embed(text: str, dim: int) -> List[float]:
    """Детерминированный эмбеддинг на основе хэша текста."""
    # Получаем 8 байт для seed из blake2b, чтобы seed поместился в uint64
    seed = int.from_bytes(hashlib.blake2b(text.encode("utf-8"), digest_size=8).digest(), "big", signed=False)
    rng = np.random.default_rng(seed)
    v = rng.normal(0.0, 1.0, size=dim).astype(np.float32)

    # Нормализуем до единичной длины (лучше для cosine)
    norm = float(np.linalg.norm(v))
    if norm == 0.0:
        return [0.0] * dim
    v = v / norm
    return v.tolist()


# На будущее: реальный вызов (оставим заглушкой, подключим позже)
def _openai_embed(text: str, dim: int) -> List[float]:
    raise RuntimeError("OpenAI embeddings disabled. Set USE_FAKE_EMBEDDINGS=false and implement real backend.")


def get_embedding(text: str) -> List[float]:
    """Возвращает эмбеддинг текста как list[float] длиной settings.EMBEDDING_DIM."""
    dim = settings.EMBEDDING_DIM
    if settings.USE_FAKE_EMBEDDINGS:
        return _fake_embed(text, dim)
    # позже переключим сюда реальную модель
    return _openai_embed(text, dim)

def to_pgvector_literal(vec: List[float]) -> str:
    """Converts a vector to a pgvector literal format."""
    return f"[{','.join(map(str, vec))}]"
