import os
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TOKEN = os.getenv ("8073072636:AAElMwu7DAySwJ6OiZZ2yC0Osb5istFi7vY")
DEFAULT_PROPERTIES = {"parse_mode=ParseMode.HTML"}
DATABASE = 'shinnik.db'


import asyncio
import logging
import sqlite3
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton