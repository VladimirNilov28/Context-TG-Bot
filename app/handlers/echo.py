from aiogram import Router, F
from aiogram.types import Message

router = Router(name="echo")

@router.message(F.text)  # ← было @router.message()
async def echo_any(msg: Message):
    await msg.answer("Принято. Для поиска используй /ask <вопрос>")
