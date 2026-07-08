import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Настройка логирования
logging.basicConfig(level=logging.INFO)
#Возьмите токен у телеграммбота @BotFather
TOKEN = "Введите ваш токен"

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ==================== КЛАВИАТУРЫ ====================

def get_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👋 Привет"), KeyboardButton(text="Как дела?")],
            [KeyboardButton(text="📊 Информация"), KeyboardButton(text="❓ Помощь")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выбери кнопку или напиши сообщение..."
    )
    return keyboard


def get_inline_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👋 Приветствие", callback_data="hello")],
        [InlineKeyboardButton(text="Как дела?", callback_data="how_are_you")],
        [InlineKeyboardButton(text="Информация о боте", callback_data="info")]
    ])
    return keyboard


# ==================== ХЕНДЛЕРЫ ====================

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я эхо-бот с удобным управлением.\n\n"
        "Используй кнопки ниже:",
        reply_markup=get_reply_keyboard()
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "✅ Доступные возможности:\n\n"
        "• Нажимай на кнопки внизу\n"
        "• Пиши любые сообщения — я их повторю\n"
        "• Используй inline-кнопки под сообщениями\n\n"
        "Бот создан для демонстрации возможностей aiogram.",
        reply_markup=get_reply_keyboard()
    )


@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(
        f"🤖 <b>Информация о боте</b>\n\n"
        f"• Библиотека: aiogram 3.x\n"
        f"• Язык: Python\n"
        f"• Пользователь: {message.from_user.full_name}\n"
        f"• ID: <code>{message.from_user.id}</code>",
        parse_mode="HTML",
        reply_markup=get_inline_menu()
    )


# Обработка Inline кнопок
@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    if callback.data == "hello":
        await callback.message.answer("Привет! Рад тебя видеть 👋")
    elif callback.data == "how_are_you":
        await callback.message.answer("Отлично, спасибо! А как твои дела? 😊")
    elif callback.data == "info":
        await callback.message.answer("Это демонстрационный бот для портфолио.")

    await callback.answer()


# ==================== ОСНОВНОЙ ОБРАБОТЧИК ====================

@dp.message()
async def message_handler(message: types.Message):
    text = message.text.strip() if message.text else ""

    # Специальная обработка кнопок
    if text == "👋 Привет":
        await message.answer("Привет! Очень рад тебя видеть 👋")

    elif text == "Как дела?":
        await message.answer("Всё отлично, спасибо! А как у тебя дела? 😊")

    elif text == "📊 Информация":
        await cmd_info(message)

    elif text == "❓ Помощь":
        await cmd_help(message)

    elif text.lower() in ["пока", "до свидания", "goodbye"]:
        await message.answer("До встречи! Хорошего дня! 👋")

    else:
        # Обычное эхо для остальных сообщений
        await message.answer(f"Ты написал: {message.text}")


async def main():
    print("🚀 Бот успешно запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
