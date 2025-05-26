from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from handlers.form import OrderForm

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

@router.message(Command("контакты"))
async def contacts_command(message: Message):
    await message.answer(
        "Наши контакты:\n"
        "📞 Телефон: +7 (923) 718-91-49\n"
        "📧 Email: dessi@mail.ru\n"
        "📍 Адрес: ул. Попова, 183, Барнаул",
        reply_markup=main_menu
    )

@router.message(Command("заявка"))
async def start_order(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(OrderForm.name)

@router.message(F.text == "ℹ️ О компании")
async def about_company(message: Message):
    await message.answer(
        "🌟 *Компания Шинник — ваш надёжный партнёр на дороге!*\n\n"
        "Мы с гордостью предлагаем высококачественные шины для легковых автомобилей, грузовиков и сельхозтехники. "
        "Наша миссия — обеспечить ваш комфорт и безопасность, предоставляя продукцию от ведущих производителей. "
        "С нами вы получаете не только широкий выбор и доступные цены, но и профессиональную поддержку на каждом этапе. "
        "Доверяйте Шинник — и дорога всегда будет под контролем!\n\n"
        "Выберите действие:",
        reply_markup=main_menu
    )

@router.message(F.text == "📞 Контакты")
async def contacts(message: Message):
    await message.answer(
        "Наши контакты:\n"
        "📞 Телефон: +7 (923) 718-91-49\n"
        "📧 Email: dessi@mail.ru\n"
        "📍 Адрес: ул. Попова, 183, Барнаул",
        reply_markup=main_menu
    )

@router.message(F.text == "🛠 Категории шин")
async def show_categories(message: Message):
    await message.answer("Выберите категорию шин:", reply_markup=category_menu)

@router.message(F.text == "🚗 Легковые")
async def car_category(message: Message, state: FSMContext):
    await state.update_data(category="Легковые шины")
    await message.answer("Выберите модель легковых шин:", reply_markup=car_tires)
    await state.set_state(OrderForm.model)

@router.message(F.text == "🚛 Грузовые")
async def truck_category(message: Message, state: FSMContext):
    await state.update_data(category="Грузовые шины")
    await message.answer("Выберите модель грузовых шин:", reply_markup=truck_tires)
    await state.set_state(OrderForm.model)

@router.message(F.text == "🚜 Сельхозтехника")
async def agro_category(message: Message, state: FSMContext):
    await state.update_data(category="Сельхозшины")
    await message.answer("Выберите модель сельхозшин:", reply_markup=agro_tires)
    await state.set_state(OrderForm.model)

@router.message(F.text == "⬅️ Назад")
async def back_to_main(message: Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu)

@router.message(F.text == "⬅️ Назад к категориям")
async def back_to_categories(message: Message):
    await message.answer("Выберите категорию шин:", reply_markup=category_menu)