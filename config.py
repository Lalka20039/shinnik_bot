import os
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Получение переменных из окружения
TOKEN = os.getenv("BOT_TOKEN")
MANAGER_CHAT_ID = os.getenv("MANAGER_CHAT_ID")  # ID менеджера или группы
ADMIN_KEY = os.getenv("ADMIN_KEY")  # Секретный ключ для админа

# Настройки бота
DEFAULT_PROPERTIES = DefaultBotProperties(parse_mode=ParseMode.HTML)

# Путь к базе данных
DATABASE_PATH = "database/shinnik.db"

# Проверка переменных
if not TOKEN or not isinstance(TOKEN, str):
    raise ValueError("BOT_TOKEN не установлен или не является строкой.")
if not MANAGER_CHAT_ID:
    raise ValueError("MANAGER_CHAT_ID не установлен.")
if not ADMIN_KEY:
    raise ValueError("ADMIN_KEY не установлен.")