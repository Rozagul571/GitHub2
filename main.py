import asyncio
import re
import uuid
import os
from asyncio import wait_for
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import yt_dlp
from pathlib import Path
from os.path import join

folder_name = 'video'
BASE_DIR = Path(__file__).parent
DATA_DIR = join(BASE_DIR, folder_name)

TOKEN = '7585580064:AAEOfa5TteGDwuEkwv-TyqGSWwYPu0QjMoY'
bot = Bot(token=TOKEN)

YOUTUBE_URL_PATTERN = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton(text="Video yuklash", callback_data="video")],
        [InlineKeyboardButton(text="Musiqa yuklash", callback_data="music")],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        "Assalom Alekum! Men IBOS research markazida yaratilgan odamlar uchun xizmat qiluvchi bot hisoblanaman. content tipini tanlang?", reply_markup=keyboard
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "video":
        await choosing_video(update, context, update.effective_chat.id)
    elif query.data == "music":
        await download_music(update, context)

async def get_valid_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_message = update.message.text
        if re.match(YOUTUBE_URL_PATTERN, user_message):
            return user_message
        else:
            await update.message.reply_text("YouTube havolasini yuboring.")

async def choosing_video(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id:int) -> None:
    await context.bot.send_message(chat_id=chat_id, text= 'Video formati tanlandi iltimos linkni yuboring')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        url = await get_valid_link(update, context)
        a = uuid.uuid4()
        if not Path(DATA_DIR).exists():
            os.mkdir(DATA_DIR)

        file_url = os.path.join(DATA_DIR, f'{a}.mp4')
        ydl_opts = {
            'outtmpl': file_url,
            'format': 'mp4',
            'quiet': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                await asyncio.to_thread(ydl.download, [url])

            info = await get_video_info_async(url)
            await send_youtube_video(context, update.effective_chat.id, file_url, info["title"])
        except Exception as e:
            await update.message.reply_text(f"Xatolik yuz berdi: {e}")

async def download_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("work")
    if update.message and update.message.text:
        print("work inner")
        url = await get_valid_link(update, context)
        a = uuid.uuid4()
        if not Path(DATA_DIR).exists():
            os.mkdir(DATA_DIR)

        file_url = os.path.join(DATA_DIR, f'{a}.mp3')
        ydl_opts = {
            'outtmpl': file_url,
            'format': 'mp3',
            'quiet': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                await asyncio.to_thread(ydl.download, [url])

            info = await get_video_info_async(url)
            await send_youtube_video(context, update.effective_chat.id, file_url, info["title"])
        except Exception as e:
            await update.message.reply_text(f"Xatolik yuz berdi: {e}")






async def get_video_info_async(url):
    ydl_opts = {'quiet': True, 'no_warnings': True}
    return await asyncio.to_thread(yt_dlp.YoutubeDL(ydl_opts).extract_info, url, False)


async def send_youtube_video(context: ContextTypes.DEFAULT_TYPE, chat_id: int, file_url: str, name: str):
    try:
        with open(file_url, 'rb') as video_file:
            await context.bot.send_video(chat_id=chat_id, video=video_file, caption=name)
        os.remove(file_url)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Xatolik yuz berdi: {e}")


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    application.add_handler(CallbackQueryHandler(handle_callback))

    application.run_polling()


if __name__ == '__main__':
    main()
