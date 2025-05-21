from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from keyboards.menu import main_menu, category_menu
from keyboards.catalog import car_tires, truck_tires, agro_tires

router = Router()

@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Добро пожаловать в компанию Шинник! 🚗\n\n"
        "Вы можете оформить заказ или узнать информацию.",
        reply_markup=main_menu
    )

@router.message(F.text == "ℹ️ О компании")
async def about_company(message: Message):
    await message.answer(
        "Мы — компания, специализирующаяся на продаже качественных автомобильных шин.\n"
        "Мы предлагаем широкий ассортимент продукции для легковых, грузовых и сельскохозяйственных автомобилей."
    )

@router.message(F.text == "📞 Контакты")
async def contacts(message: Message):
    await message.answer(
        "Наши контакты:\n"
        "Телефон: +7 (923) 718-91-49\n"
        "Email: info@shinnik.com\n"
        "Адрес: ул. Попова, 183, Барнаул"
    )

@router.message(F.text == "🚗 Легковые")
async def car_category(message: Message):
    await message.answer("Выберите товар:", reply_markup=car_tires)

@router.message(F.text == "🚛 Грузовые")
async def truck_category(message: Message):
    await message.answer("Выберите товар:", reply_markup=truck_tires)

@router.message(F.text == "🚜 Сельхозтехника")
async def agro_category(message: Message):
    await message.answer("Выберите товар:", reply_markup=agro_tires)

@router.message(F.text == "⬅️ Назад")
async def back_to_main(message: Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu)

@router.message(F.text == "⬅️ Назад к категориям")
async def back_to_categories(message: Message):
    await message.answer("Выберите категорию шин:", reply_markup=category_menu)



