# keyboards/category.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопка для оформления заказа
order_button = KeyboardButton(text="Оформить заказ")

# Кнопки для выбора категории шин
category_buttons = [
    [order_button],  # Кнопка оформления заказа
    [KeyboardButton(text="Легковые шины")],
    [KeyboardButton(text="Грузовые шины")],
    [KeyboardButton(text="Сельхозшины")]
]

category_keyboard = ReplyKeyboardMarkup(
    keyboard=category_buttons,  # передаем список кнопок
    resize_keyboard=True
)

# Кнопки для выбора моделей легковых шин
car_tires_buttons = [
    [KeyboardButton(text="Michelin X-Ice")],
    [KeyboardButton(text="Continental ContiWinterContact")]
]
car_tires = ReplyKeyboardMarkup(keyboard=car_tires_buttons, resize_keyboard=True)

# Кнопки для выбора моделей грузовых шин
truck_tires_buttons = [
    [KeyboardButton(text="Bridgestone M729")],
    [KeyboardButton(text="Kama NR-201")]
]
truck_tires = ReplyKeyboardMarkup(keyboard=truck_tires_buttons, resize_keyboard=True)

# Кнопки для выбора моделей сельхозшин
agro_tires_buttons = [
    [KeyboardButton(text="BKT TR-135")],
    [KeyboardButton(text="Alliance 347")]
]
agro_tires = ReplyKeyboardMarkup(keyboard=agro_tires_buttons, resize_keyboard=True)










