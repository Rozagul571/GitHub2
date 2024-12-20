import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN

async def on_startup(dispatcher: Dispatcher):
    print("Bot ishga tushdi!")

async def send_main_menu(message: Message):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏠 Qurilmalar"), KeyboardButton(text="🔐 Xavfsizlik")],
            [KeyboardButton(text="⚡️ Elektr sarfi"), KeyboardButton(text="🔌 Rozetkalar")],
            [KeyboardButton(text="🌡 Temperatura"), KeyboardButton(text="⚙️ Sozlamalar")]
        ],
        resize_keyboard=True
    )
    await message.answer("Asosiy menyu:", reply_markup=main_menu)

async def send_settings(message: Message):
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Tezkor buyrug'lar", callback_data='fast_commands')],
        [InlineKeyboardButton(text="Home", callback_data='home')]
    ])
    await message.answer("Sozlamalar:", reply_markup=inline_kb)

async def main():
    # Bot ob'ektini yaratish
    bot = Bot(token=BOT_TOKEN)

    # Dispatcher ob'ektini yaratish
    dp = Dispatcher(storage=MemoryStorage())

    # Xabar handlerlarini ro'yxatdan o'tkazish
    dp.message.register(send_main_menu, Command(commands=["start"]))
    dp.message.register(send_settings, lambda message: message.text == "⚙️ Sozlamalar")

    # Botni ishga tushirish
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == '__main__':
    asyncio.run(main())
