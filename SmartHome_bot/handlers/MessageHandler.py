from aiogram import types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class MessageHandler:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        self.register_handlers()

    def register_handlers(self):
        self.dp.message.register(self.send_main_menu, Command("start"))
        self.dp.message.register(self.send_main_menu, Command("menu"))
        self.dp.message.register(self.handle_settings, lambda msg: msg.text == "⚙️ Sozlamalar")

    async def send_main_menu(self, message: types.Message):
        main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        main_menu.add(types.KeyboardButton("🏠 Qurilmalar"), types.KeyboardButton("🔐 Xavfsizlik"))
        main_menu.add(types.KeyboardButton("⚡️ Elektr sarfi"), types.KeyboardButton("🔌 Rozetkalar"))
        main_menu.add(types.KeyboardButton("🌡 Temperatura"), types.KeyboardButton("⚙️ Sozlamalar"))
        await message.answer("Asosiy menyu:", reply_markup=main_menu)

    async def handle_settings(self, message: types.Message):
        inline_kb = InlineKeyboardMarkup(row_width=2)
        inline_kb.add(InlineKeyboardButton("Tezkor buyrug'lar", callback_data='fast_commands'))
        inline_kb.add(InlineKeyboardButton("Home", callback_data='home'))
        await message.answer("Sozlamalar:", reply_markup=inline_kb)
