"""Конфигурация приложения (заглушка).
Позже добавим загрузку .env и класс Settings со всеми полями."""
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(filename=".env"), override=False)

class Settings:
    # Инициализация настроек из переменных окружения для конфигурации приложения
    def __init__(self) -> None:
        self.ENV = os.getenv("ENV", "dev")

        # Токен Telegram бота и ключ OpenAI
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        
        # URL базы данных
        self.DATABASE_URL = os.environ.get("DATABASE_URL")

        # Настройки OpenAI
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        self.EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1536"))

settings = Settings()
