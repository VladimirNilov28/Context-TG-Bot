"""Entry point: дым-тест БД и поиска."""

from sqlalchemy import text
from app.db.session import engine, get_session
from app.core.config import settings
from app.services.search import search_similar


def main() -> None:
    # 1) Проверяем подключение
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version()")).scalar()
        print("✅ DB version:", version)

    # 2) Смотрим, есть ли данные для поиска
    with get_session() as s:
        n_docs = s.execute(text("SELECT count(*) FROM documents")).scalar()
        n_chunks = s.execute(text("SELECT count(*) FROM chunks")).scalar()
        n_emb = s.execute(text("SELECT count(*) FROM embeddings")).scalar()

    print(f"📊 counts -> documents={n_docs}, chunks={n_chunks}, embeddings={n_emb}")

    # 3) Если есть эмбеддинги — пробуем запрос похожести
    if n_emb and n_emb > 0:
        # Простейший запросный вектор: единичный вектор по первой координате.
        # В реале сюда подставляешь эмбеддинг вопроса.
        qvec = [1.0] + [0.0] * (settings.EMBEDDING_DIM - 1)
        top = search_similar(qvec, top_k=5)
        print("🔎 top matches:")
        for i, row in enumerate(top, 1):
            print(f"  {i:02d}. chunk_id={row['chunk_id']} dist={row['distance']:.6f}")
    else:
        print("ℹ️  Нет данных в embeddings — поиск пропущен. Загрузим документы позже.")


if __name__ == "__main__":
    main()
