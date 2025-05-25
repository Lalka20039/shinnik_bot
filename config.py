import os
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Получение токена из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

# Настройки бота
DEFAULT_PROPERTIES = DefaultBotProperties(parse_mode=ParseMode.HTML)

# Путь к базе данных
DATABASE_PATH = "database/shinnik.db"

# Проверка токена
if not TOKEN or not isinstance(TOKEN, str):
    raise ValueError("BOT_TOKEN не установлен или не является строкой. Установите переменную окружения BOT_TOKEN.")