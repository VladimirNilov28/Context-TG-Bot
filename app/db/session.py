"""Сессия БД (заготовка). Здесь позже создадим engine и Session."""
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создаем движок БД с настройками подключения
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    future=True  # Использование нового стиля SQL Alchemy 2.0
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

@contextmanager
def get_session():
    """Контекстный менеджер: with get_session() as s: ..."""
    # Создаем новую сессию
    session = SessionLocal()
    try:
        yield session
        session.commit()  # Фиксируем изменения при успешном выполнении
    except Exception:
        session.rollback()  # Откатываем изменения при ошибке
        raise
    finally:
        session.close()  # Закрываем сессию в любом случае