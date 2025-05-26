from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import logging
import re
from datetime import datetime

from keyboards.menu import main_menu, category_menu
from keyboards.catalog import car_tires, truck_tires, agro_tires
from database.db import insert_order
from config import MANAGER_CHAT_ID

form_router = Router()

class OrderForm(StatesGroup):
    name = State()
    phone = State()
    category = State()
    model = State()

VALID_MODELS = {
    "Легковые шины": [
        "Легковая шина Кама Breeze 185/65R14",
        "Легковая шина Кама Grant 175/70R13",
        "Легковая шина Nortec LT 600 205/75R16C",
        "Легковая шина Алтайшина Forward Professional 219 225/75R16C",
        "Легковая шина Kapsen PracticalMax H/P 215/65R16",
        "Легковая шина Taitong HS268 235/65R17",
        "Легковая шина Omskshina Я-467 185/75R16C",
        "Легковая шина Кама Euro-129 195/65R15",
        "Легковая шина Nortec WT 580 205/70R15C",
        "Легковая шина Алтайшина Forward Dinamic 232 205/65R15"
    ],
    "Грузовые шины": [
        "Грузовая шина Кама NR 201 10.00R20",
        "Грузовая шина Кама NT 202 215/75R17.5",
        "Грузовая шина Nortec TR 1260 12.00R20",
        "Грузовая шина Алтайшина ОИ-25 14.00-20",
        "Грузовая шина Kapsen HS918 315/80R22.5",
        "Грузовая шина Taitong TD 168 295/75R22.5",
        "Грузовая шина Omskshina ИД-304 11.00R22.5",
        "Грузовая шина Кама NU 301 315/70R22.5",
        "Грузовая шина Nortec TC 600 385/65R22.5",
        "Грузовая шина Алтайшина О-40БМ 12.00R20"
    ],
    "Сельхозшины": [
        "Сельхозшина Кама Ф-2А 15.5R38",
        "Сельхозшина Алтайшина Я-324 16.9R38",
        "Сельхозшина Nortec TA 02 13.6R38",
        "Сельхозшина Omskshina Ф-35 11.2R42",
        "Сельхозшина Кама Я-183 9.00-16",
        "Сельхозшина Алтайшина Ф-44 15.0/70-18",
        "Сельхозшина Nortec H-05 7.50-20",
        "Сельхозшина Kapsen AgriPro 12.4R28",
        "Сельхозшина Taitong AgriKing 13.6R24",
        "Сельхозшина Omskshina Ф-2АД 15.5-38"
    ]
}

@form_router.message(F.text == "📦 Оформить заказ")
async def start_order(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(OrderForm.name)

@form_router.message(OrderForm.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("Введите ваш номер телефона (например, +79991234567):")
    await state.set_state(OrderForm.phone)

@form_router.message(OrderForm.phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    cleaned_phone = re.sub(r'[^\d+]', '', phone)
    
    if not re.match(r'^\+\d{10,14}$', cleaned_phone):
        logging.warning(f"Некорректный номер телефона: {phone} (очищено: {cleaned_phone})")
        await message.answer(
            "Пожалуйста, введите корректный номер телефона в международном формате (например, +79991234567). "
            "Номер должен начинаться с '+' и содержать от 10 до 14 цифр."
        )
        return
    
    await state.update_data(phone=cleaned_phone)
    await message.answer("Выберите категорию шин:", reply_markup=category_menu)
    await state.set_state(OrderForm.category)

@form_router.message(OrderForm.category)
async def get_category(message: Message, state: FSMContext):
    if message.text not in ["Легковые", "Грузовые", "Сельхозтехника"]:
        await message.answer("Пожалуйста, выберите категорию из предложенных.")
        return
    
    category_mapping = {
        "Легковые": "Легковые шины",
        "Грузовые": "Грузовые шины",
        "Сельхозтехника": "Сельхозшины"
    }
    category = category_mapping.get(message.text)
    
    await state.update_data(category=category)
    
    if message.text == "Легковые":
        await message.answer("Выберите модель легковых шин:", reply_markup=car_tires)
    elif message.text == "Грузовые":
        await message.answer("Выберите модель грузовых шин:", reply_markup=truck_tires)
    elif message.text == "Сельхозтехника":
        await message.answer("Выберите модель сельхозшин:", reply_markup=agro_tires)
    
    await state.set_state(OrderForm.model)

@form_router.message(OrderForm.model, F.text.in_(sum(VALID_MODELS.values(), [])))
async def get_model(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    category = data.get("category")
    
    if message.text not in VALID_MODELS.get(category, []):
        logging.warning(f"Выбрана некорректная модель: {message.text} для категории {category}")
        await message.answer("Пожалуйста, выберите модель из предложенного списка.")
        return
    
    await state.update_data(model=message.text)
    data = await state.get_data()

    try:
        insert_order(
            user_id=message.from_user.id,
            user_name=data["name"],
            phone=data["phone"],
            vehicle_type=data["category"],
            model=data["model"]
        )
        logging.info(f"Заказ сохранён: user_id={message.from_user.id}, model={data['model']}")

        order_message = (
            f"📜 Новая заявка!\n\n"
            f"Имя: {data['name']}\n"
            f"Телефон: {data['phone']}\n"
            f"Категория: {data['category']}\n"
            f"Модель: {data['model']}\n"
            f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        await bot.send_message(chat_id=MANAGER_CHAT_ID, text=order_message)
        logging.info(f"Уведомление отправлено в чат {MANAGER_CHAT_ID}")

        await message.answer(
            f"Спасибо за заказ!\n\n"
            f"Имя: {data['name']}\n"
            f"Телефон: {data['phone']}\n"
            f"Категория: {data['category']}\n"
            f"Модель: {data['model']}",
            reply_markup=main_menu
        )
        await state.clear()
    except Exception as e:
        logging.error(f"Ошибка при сохранении заказа или отправке уведомления: {e}")
        await message.answer("Произошла ошибка при оформлении заказа. Попробуйте снова.")
        await state.clear()

@form_router.message(OrderForm.model, F.text == "Не нашли нужную вам шину?")
async def handle_not_found(message: Message, state: FSMContext):
    await message.answer(
        "Не нашли подходящую шину? Свяжитесь с нами, и мы подберём нужную вам модель!\n\n"
        "📞 Телефон: +7 (923) 718-91-49\n"
        "📧 Email: dessi@mail.ru\n"
        "📍 Адрес: ул. Попова, 183, Барнаул",
        reply_markup=main_menu
    )
    await state.clear()

@form_router.message(OrderForm.model, F.text == "⬅️ Назад к категориям")
async def back_to_category(message: Message, state: FSMContext):
    await state.update_data(category=None)
    await message.answer("Выберите категорию шин:", reply_markup=category_menu)
    await state.set_state(OrderForm.category)

@form_router.message(OrderForm.model, F.text.lower() == "отмена")
async def cancel_order_in_model_state(message: Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.id} отменил заказ на этапе выбора модели.")
    await state.clear()
    await message.answer(
        "Оформление заказа отменено. Хотите начать заново?",
        reply_markup=main_menu
    )

@form_router.message(OrderForm.model)
async def invalid_model(message: Message, state: FSMContext):
    logging.warning(f"Недопустимый ввод в состоянии модели: {message.text}")
    await message.answer("Пожалуйста, выберите модель из предложенного списка.")