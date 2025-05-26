from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

car_tires = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Легковая шина Кама Breeze 185/65R14"), KeyboardButton(text="Легковая шина Кама Grant 175/70R13")],
        [KeyboardButton(text="Легковая шина Nortec LT 600 205/75R16C"), KeyboardButton(text="Легковая шина Алтайшина Forward Professional 219 225/75R16C")],
        [KeyboardButton(text="Легковая шина Kapsen PracticalMax H/P 215/65R16"), KeyboardButton(text="Легковая шина Taitong HS268 235/65R17")],
        [KeyboardButton(text="Легковая шина Omskshina Я-467 185/75R16C"), KeyboardButton(text="Легковая шина Кама Euro-129 195/65R15")],
        [KeyboardButton(text="Легковая шина Nortec WT 580 205/70R15C"), KeyboardButton(text="Легковая шина Алтайшина Forward Dinamic 232 205/65R15")],
        [KeyboardButton(text="Не нашли нужную вам шину?")],
        [KeyboardButton(text="⬅️ Назад к категориям")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True
)

truck_tires = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Грузовая шина Кама NR 201 10.00R20"), KeyboardButton(text="Грузовая шина Кама NT 202 215/75R17.5")],
        [KeyboardButton(text="Грузовая шина Nortec TR 1260 12.00R20"), KeyboardButton(text="Грузовая шина Алтайшина ОИ-25 14.00-20")],
        [KeyboardButton(text="Грузовая шина Kapsen HS918 315/80R22.5"), KeyboardButton(text="Грузовая шина Taitong TD168 295/75R22.5")],
        [KeyboardButton(text="Грузовая шина Omskshina ИД-304 11.00R22.5"), KeyboardButton(text="Грузовая шина Кама NU 301 315/70R22.5")],
        [KeyboardButton(text="Грузовая шина Nortec TC 600 385/65R22.5"), KeyboardButton(text="Грузовая шина Алтайшина О-40БМ 12.00R20")],
        [KeyboardButton(text="Не нашли нужную вам шину?")],
        [KeyboardButton(text="⬅️ Назад к категориям")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True
)

agro_tires = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сельхозшина Кама Ф-2А 15.5R38"), KeyboardButton(text="Сельхозшина Алтайшина Я-324 16.9R38")],
        [KeyboardButton(text="Сельхозшина Nortec TA 02 13.6R38"), KeyboardButton(text="Сельхозшина Omskshina Ф-35 11.2R42")],
        [KeyboardButton(text="Сельхозшина Кама Я-183 9.00-16"), KeyboardButton(text="Сельхозшина Алтайшина Ф-44 15.0/70-18")],
        [KeyboardButton(text="Сельхозшина Nortec H-05 7.50-20"), KeyboardButton(text="Сельхозшина Kapsen AgriPro 12.4R28")],
        [KeyboardButton(text="Сельхозшина Taitong AgriKing 13.6R24"), KeyboardButton(text="Сельхозшина Omskshina Ф-2АД 15.5-38")],
        [KeyboardButton(text="Не нашли нужную вам шину?")],
        [KeyboardButton(text="⬅️ Назад к категориям")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True
)