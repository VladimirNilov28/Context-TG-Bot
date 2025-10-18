"""Базовый класс ORM-моделей (заготовка).
Позже здесь появятся: Document, Chunk, Embedding."""
from sqlalchemy.orm import declarative_base

Base = declarative_base()