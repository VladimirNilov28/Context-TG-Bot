from aiogram import Router
from aiogram.types import Message

router = Router(name="echo")

@router.message()
async def echo_any(msg: Message):
    # просто подтверждаем получение, позже сюда добавим загрузку файлов
    await msg.answer("Принято. Для поиска используй /ask <вопрос>")
