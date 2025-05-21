from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

car_tires = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Легковая шина Forward Safari 510"), KeyboardButton(text="Легковая шина Кама Breeze 185/65R14")],
        [KeyboardButton(text="Легковая шина Cordiant Comfort 2 205/55R16")],
        [KeyboardButton(text="⬅️ Назад к категориям"), KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)

truck_tires = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Грузовая шина Кама-310 12.00R20"), KeyboardButton(text="Грузовая шина Кама 10.00R20 И-281 У-4")],
        [KeyboardButton(text="Грузовая шина Кама NT 202 215/75R17.5")],
        [KeyboardButton(text="⬅️ Назад к категориям"), KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)

agro_tires = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сельхозшина Кама 15.5R38 Ф-2А"), KeyboardButton(text="Сельхозшина Алтайшина 15.5-38 Ф-2АД")],
        [KeyboardButton(text="Сельхозшина Волтаир Я-324 16.9R38")],
        [KeyboardButton(text="⬅️ Назад к категориям"), KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)

category_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Легковые шины")],
        [KeyboardButton(text="Грузовые шины")],
        [KeyboardButton(text="Сельхозшины")],
        [KeyboardButton(text="⬅️ Назад"), KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)