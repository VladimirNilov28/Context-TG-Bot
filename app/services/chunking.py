"""Сервис чанкинга текста (разделение текста на части)."""

from typing import List, Tuple


def count_tokens(text: str) -> int:
    """Грубая оценка токенов: количество слов. Позже заменим на tiktoken."""
    return len(text.split())


def split_text(
    text: str,
    chunk_size: int = 800,     # размер каждого куска в «токенах»
    chunk_overlap: int = 200,  # количество «токенов» перекрытия между кусками
) -> List[str]:
    """Режем текст на куски ~chunk_size с перекрытием chunk_overlap.
    Сейчас считаем «токены» как слова, чтобы не тянуть tiktoken.
    """
    # Разбиваем текст на слова
    words = text.split()
    if not words:
        return []

    chunks: List[str] = []
    # Начальная позиция для текущего куска
    start = 0
    # Шаг перемещения окна (с учетом перекрытия)
    step = max(1, chunk_size - chunk_overlap)

    while start < len(words):
        # Определяем конец текущего куска
        end = min(len(words), start + chunk_size)
        # Выбираем слова для текущего куска
        chunk_words = words[start:end]
        # Собираем слова обратно в текст и добавляем в результат
        chunks.append(" ".join(chunk_words))
        # Если достигли конца текста - выходим
        if end == len(words):
            break
        # Сдвигаем начальную позицию с учетом перекрытия
        start += step

    return chunks
