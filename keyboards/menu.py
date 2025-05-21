from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Оформить заказ")],
        [KeyboardButton(text="ℹ️ О компании")],
        [KeyboardButton(text="📞 Контакты")]
    ],
    resize_keyboard=True
)

category_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚗 Легковые"), KeyboardButton(text="🚛 Грузовые")],
        [KeyboardButton(text="🚜 Сельхозтехника")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)