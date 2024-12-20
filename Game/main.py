import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Global o'zgaruvchilar
user_games = {}

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men bilan o'yin o'ynashga tayyormisiz? 😊\n"
        "Men bir son o'ylayman, siz esa uni topishga harakat qilasiz.\n"
        "O'yinni boshlash uchun /game yozing!"
    )

# /game komandasi
async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_games[user_id] = random.randint(1, 100)  # 1 dan 100 gacha son o'ylash
    await update.message.reply_text(
        "Men 1 dan 100 gacha son o'yladim. Uni topishga harakat qiling! 😊\n"
        "Sonni kiritishingiz mumkin."
    )

# Foydalanuvchi son kiritganda
async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_games:
        await update.message.reply_text(
            "O'yinni boshlash uchun /game yozing!"
        )
        return

    try:
        user_guess = int(update.message.text)  # Foydalanuvchi kiritgan son
    except ValueError:
        await update.message.reply_text("Iltimos, faqat son kiriting!")
        return

    secret_number = user_games[user_id]

    if user_guess < secret_number:
        await update.message.reply_text("Men o'ylagan sondan kattaroq son yozing!")
    elif user_guess > secret_number:
        await update.message.reply_text("Men o'ylagan sondan kichikroq son yozing!")
    else:
        await update.message.reply_text(
            f"Tabriklayman! 🎉 Siz to'g'ri topdingiz! Men {secret_number} sonini o'ylagan edim.\n"
            "Yana o'ynashni xohlaysizmi? /game yozing!"
        )
        del user_games[user_id]  # O'yinni tugatish

# Asosiy bot konfiguratsiyasi
if __name__ == "__main__":
    app = ApplicationBuilder().token("8083671056:AAGgA1uRzobDDjmpvz8MlYLef0fQDpMRa_A").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("game", game))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess))

    print("Bot ishga tushdi...")
    app.run_polling()
