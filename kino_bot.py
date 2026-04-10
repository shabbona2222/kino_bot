from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import re

TOKEN = "8622956333:AAF3XX19dkkGGy2O8eICIrn2OqEXcbtAfZs"

movies = {}

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Assalomu alaykum, hush kelibsiz!")
    await update.message.reply_text("🎬 Kino kodini yozing")

# Kanal postlarini ushlash
async def channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post

    text = message.caption or message.text
    if not text:
        return

    match = re.search(r'\d+', text)

    if match:
        code = match.group()

        if message.video:
            file_id = message.video.file_id
        elif message.document:
            file_id = message.document.file_id
        else:
            return

        movies[code] = file_id
        print(f"Saqlandi: {code}")

# Foydalanuvchi yozsa
async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()

    if code in movies:
        await update.message.reply_video(movies[code])
    else:
        await update.message.reply_text("❌ Bunday kino topilmadi")

app = ApplicationBuilder().token(TOKEN).build()

# ✅ START qo‘shildi
app.add_handler(CommandHandler("start", start))

# Kanal postlari
app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, channel_post))

# User yozsa
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), user_message))

app.run_polling()
