from aiogram import Router, F
from aiogram.types import Message

router = Router(name="start")

@router.message(F.text == "/start")
async def cmd_start(msg: Message):
    await msg.answer("Привет! Я бот для поиска по твоим документам.\nКоманды: /help, /ask <вопрос>")
