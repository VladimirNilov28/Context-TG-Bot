from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.embeddings import get_embedding
from app.services.search import search_similar

router = Router(name="ask")

@router.message(Command("ask"))
async def cmd_ask(msg: Message):
    parts = (msg.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await msg.answer("Использование: /ask <вопрос>")
        return

    question = parts[1].strip()
    try:
        qvec = get_embedding(question)
        results = search_similar(qvec, top_k=5)
    except Exception as e:
        await msg.answer(f"Ошибка поиска: {e}")
        return

    await msg.answer(f"found={len(results)}")
    if not results:
        return

    lines = [
        f"{i+1}. id={r['chunk_id']} dist={r['distance']:.4f}\n{(r['content'] or '')[:400]}"
        for i, r in enumerate(results[:3])
    ]
    await msg.answer("\n\n".join(lines))
