"""Entry point: проверка соединения с БД (дым-тест)."""
from sqlalchemy import text
from app.db.session import engine, get_session


def main() -> None:
    # Проверяем подключение напрямую к базе данных через engine
    with engine.connect() as conn:
        # Получаем версию PostgreSQL
        version = conn.execute(text("SELECT version()")).scalar()
        print("✅ DB version:", version)

    # Проверяем работу через SQLAlchemy ORM сессию
    with get_session() as s:
        # Подсчитываем количество документов в таблице
        count = s.execute(text("SELECT count(*) FROM documents")).scalar()
        print("📄 documents =", count)


if __name__ == "__main__":
    # Точка входа при запуске файла напрямую
    main()
