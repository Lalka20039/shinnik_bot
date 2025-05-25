import asyncio
import logging
import os
from functools import partial
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from config import TOKEN, DEFAULT_PROPERTIES
from handlers.client import router as client_router
from handlers.form import form_router
from database.db import create_table

async def on_startup(bot: Bot, webhook_url: str):
    try:
        await bot.set_webhook(webhook_url)
        logging.info(f"Webhook установлен: {webhook_url}")
    except Exception as e:
        logging.error(f"Ошибка при установке вебхука: {e}")

async def on_shutdown(bot: Bot):
    try:
        await bot.delete_webhook()
        logging.info("Webhook удалён")
    except Exception as e:
        logging.error(f"Ошибка при удалении вебхука: {e}")

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

    # Регистрация startup и shutdown с использованием functools.partial
    dp.startup.register(partial(on_startup, webhook_url=webhook_url))
    dp.shutdown.register(partial(on_shutdown))

    # Запуск веб-сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv('PORT', 8080)))
    await site.start()

    try:
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())