"""ORM-модели: Document, Chunk, Embedding."""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    DateTime,
    func,
    Index,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# pgvector: тип столбца vector(N) для работы с векторными эмбеддингами
from pgvector.sqlalchemy import Vector


# База для ORM-моделей (современный стиль SQLAlchemy 2.x)
class Base(DeclarativeBase):
    pass


class Document(Base):
    """
    Модель документа - родительская сущность для чанков.
    Хранит метаданные исходного документа.
    """
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    source: Mapped[Optional[str]] = mapped_column(String, nullable=True)   # путь/URL/имя источника документа
    mime: Mapped[Optional[str]] = mapped_column(String, nullable=True)     # MIME-тип документа
    meta: Mapped[dict] = mapped_column(JSON, default=dict, server_default="{}")  # дополнительные метаданные в JSON
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # связь один-ко-многим с чанками, каскадное удаление
    chunks: Mapped[list["Chunk"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Document id={self.id} source={self.source!r}>"


class Chunk(Base):
    """
    Модель чанка - фрагмент текста документа.
    Связана с родительским документом и может иметь векторное представление (embedding).
    """
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    document_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)  # текстовое содержимое чанка
    token_count: Mapped[int] = mapped_column(Integer, nullable=False)  # количество токенов в чанке
    chunk_order: Mapped[int] = mapped_column(Integer, nullable=False)  # порядковый номер чанка в документе
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # связь многие-к-одному с документом
    document: Mapped["Document"] = relationship(back_populates="chunks")
    # связь один-к-одному с векторным представлением
    embedding: Mapped[Optional["Embedding"]] = relationship(
        back_populates="chunk",
        cascade="all, delete-orphan",
        uselist=False,
        passive_deletes=True,
    )

    # составной индекс для быстрого поиска чанков конкретного документа
    __table_args__ = (
        Index("idx_chunks_doc", "document_id", "chunk_order"),
    )

    def __repr__(self) -> str:
        return f"<Chunk id={self.id} doc={self.document_id} order={self.chunk_order}>"


class Embedding(Base):
    """
    Модель векторного представления чанка.
    Хранит эмбеддинги, полученные из языковой модели.
    """
    __tablename__ = "embeddings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    chunk_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("chunks.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # уникальный индекс обеспечивает связь 1:1 с чанком
        index=True,
    )
    # вектор фиксированной размерности (1536 - стандарт для многих языковых моделей)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536), nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)  # идентификатор использованной модели
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # связь один-к-одному с чанком
    chunk: Mapped["Chunk"] = relationship(back_populates="embedding")

    # векторный индекс создаётся отдельным SQL-скриптом 02_schema.sql (тип ivfflat)
    # его нельзя создать средствами ORM

    def __repr__(self) -> str:
        return f"<Embedding id={self.id} chunk={self.chunk_id}>"
