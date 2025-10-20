# app/handlers/upload.py
from pathlib import Path
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatAction

from app.services.readers import read_txt, read_pdf
from app.services.ingest import ingest_text

router = Router(name="upload")

MAX_MB = 15  # мягкий лимит для dev

def _human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} {unit}"
        n /= 1024
    return f"{n:.1f} GB"

@router.message(F.document)
async def on_document(msg: Message):
    doc = msg.document
    size = doc.file_size or 0
    if size > MAX_MB * 1024 * 1024:
        await msg.answer(f"Файл слишком большой ({_human(size)}). Лимит ~{MAX_MB}MB.")
        return

    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)

    tmp_dir = Path("/tmp/uploads")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_dir / f"{doc.file_unique_id}_{doc.file_name or 'file'}"

    # скачать файл
    try:
        await msg.bot.download(doc, destination=tmp_path)
    except Exception as e:
        await msg.answer(f"Не удалось скачать файл: {e}")
        return

    # распарсить текст
    mime = (doc.mime_type or "").lower()
    try:
        if mime.startswith("text/") or tmp_path.suffix.lower() in {".txt", ".md", ".log"}:
            text = read_txt(tmp_path)
        elif mime == "application/pdf" or tmp_path.suffix.lower() == ".pdf":
            text = read_pdf(tmp_path)
        else:
            await msg.answer(f"Пока поддерживаю .txt и .pdf. Получил: {doc.mime_type or tmp_path.suffix}")
            return
    except Exception as e:
        await msg.answer(f"Ошибка чтения файла: {e}")
        return

    if not text.strip():
        await msg.answer("Текст не извлечён (пустой документ).")
        return

    # загрузка в БД
    try:
        doc_id, chunk_ids = ingest_text(
            source=doc.file_name or str(tmp_path.name),
            text=text,
            mime=mime or "application/octet-stream",
        )
    except Exception as e:
        await msg.answer(f"Ошибка при сохранении: {e}")
        return

    await msg.answer(f"✅ Загружено: document_id={doc_id}, чанков={len(chunk_ids)}. Теперь можно /ask.")
