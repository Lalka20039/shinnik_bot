import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from config import TOKEN, DEFAULT_PROPERTIES
from handlers.client import router as client_router
from handlers.form import form_router
from database.db import create_table

async def on_startup(bot: Bot, webhook_url: str):
    await bot.set_webhook(webhook_url)
    logging.info(f"Webhook установлен: {webhook_url}")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logging.info("Webhook удалён")

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler()
        ]
    )

    create_table()

    bot = Bot(token=TOKEN, default=DEFAULT_PROPERTIES)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(client_router)
    dp.include_router(form_router)

    # Настройка вебхуков
    webhook_path = "/webhook"
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{webhook_path}"
    app = web.Application()
    request_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    request_handler.register(app, path=webhook_path)
    setup_application(app, dp, bot=bot)

    dp.startup.register(lambda: on_startup(bot, webhook_url))
    dp.shutdown.register(lambda: on_shutdown(bot))

    # Запуск веб-сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv('PORT', 8080)))
    await site.start()

    try:
        await asyncio.Event().wait()  # Держим приложение запущенным
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
