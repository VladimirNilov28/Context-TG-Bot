import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from app.core.config import settings
from app.handlers import start as h_start
from app.handlers import help as h_help
from app.handlers import ask as h_ask
from app.handlers import echo as h_echo
from app.handlers import debug as h_debug
from app.handlers import upload as h_upload

async def on_startup(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Проверка бота"),
            BotCommand(command="help", description="Помощь"),
            BotCommand(command="ask", description="Поиск фрагментов"),
            BotCommand(command="debug", description="Диагностика"),
        ]
    )

async def main():
    if not settings.TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не задан в app/.env")
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(h_start.router)
    dp.include_router(h_help.router)
    dp.include_router(h_ask.router)
    dp.include_router(h_debug.router)
    dp.include_router(h_upload.router)
    dp.include_router(h_echo.router)
    
    await on_startup(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
