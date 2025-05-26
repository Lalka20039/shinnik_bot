from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import logging
import re
from datetime import datetime  # Для времени заказа

from keyboards.menu import main_menu
from keyboards.catalog import category_keyboard, car_tires, truck_tires, agro_tires
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
        "Легковая шина Forward Safari 510",
        "Легковая шина Кама Breeze 185/65R14",
        "Легковая шина Cordiant Comfort 2 205/55R16"
    ],
    "Грузовые шины": [
        "Грузовая шина Кама-310 12.00R20",
        "Грузовая шина Кама 10.00R20 И-281 У-4",
        "Грузовая шина Кама NT 202 215/75R17.5"
    ],
    "Сельхозшины": [
        "Сельхозшина Кама 15.5R38 Ф-2А",
        "Сельхозшина Алтайшина 15.5-38 Ф-2АД",
        "Сельхозшина Волтаир Я-324 16.9R38"
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
    await message.answer("Выберите категорию шин:", reply_markup=category_keyboard)
    await state.set_state(OrderForm.category)

@form_router.message(OrderForm.category)
async def get_category(message: Message, state: FSMContext):
    if message.text not in ["Легковые шины", "Грузовые шины", "Сельхозшины"]:
        await message.answer("Пожалуйста, выберите категорию из предложенных.")
        return
    
    await state.update_data(category=message.text)
    
    if message.text == "Легковые шины":
        await message.answer("Выберите модель легковых шин:", reply_markup=car_tires)
    elif message.text == "Грузовые шины":
        await message.answer("Выберите модель грузовых шин:", reply_markup=truck_tires)
    elif message.text == "Сельхозшины":
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

        # Отправка уведомления менеджеру
        order_message = (
            f"📜 Новая заявка!\n\n"f"Имя: {data['name']}\n"
            f"Телефон: {data['phone']}\n"
            f"Категория: {data['category']}\n"
            f"Модель: {data['model']}\n"
            f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        await bot.send_message(chat_id=MANAGER_CHAT_ID, text=order_message)
        logging.info(f"Уведомление отправлено в чат {MANAGER_CHAT_ID}")

        # Подтверждение пользователю
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

@form_router.message(OrderForm.model, F.text == "⬅️ Назад к категориям")
async def back_to_category(message: Message, state: FSMContext):
    await state.update_data(category=None)
    await message.answer("Выберите категорию шин:", reply_markup=category_keyboard)
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

@form_router.message(F.text.lower() == "отмена")
async def cancel_order(message: Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.id} отменил заказ.")
    await state.clear()
    await message.answer(
        "Оформление заказа отменено. Хотите начать заново?",
        reply_markup=main_menu
    )