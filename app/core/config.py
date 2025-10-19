"""Загрузка настроек приложения из переменных окружения/.env (детерминированно)."""
import os
from pathlib import Path
from dotenv import load_dotenv

APP_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = APP_DIR / ".env"
load_dotenv(ENV_PATH, override=False)

class Settings:
    def __init__(self) -> None:
        self.ENV = os.getenv("ENV", "dev")
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        # В локалке host=localhost:5433, в Docker — db:5432
        self.DATABASE_URL = os.environ["DATABASE_URL"]

        # Эмбеддинги
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        self.EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1536"))
        self.USE_FAKE_EMBEDDINGS = os.getenv("USE_FAKE_EMBEDDINGS", "true").lower() in {"1", "true", "yes"}

settings = Settings()
