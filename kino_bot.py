from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import re
import os

# TOKEN endi Render’dan olinadi
TOKEN = os.getenv("TOKEN")

movies = {}

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Assalomu alaykum, hush kelibsiz!")
    await update.message.reply_text("🎬 Kino kodini yozing")

# Kanal postlarini ushlash
async def channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post

    if not message:
        return

    text = message.caption or message.text
    if not text:
        return

    match = re.search(r'\d+', text)

    if match:
        code = match.group()

        file_id = None

        if message.video:
            file_id = message.video.file_id
        elif message.document:
            file_id = message.document.file_id

        if file_id:
            movies[code] = file_id
            print(f"Saqlandi: {code}")

# Foydalanuvchi yozsa
async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()

    if code in movies:
        await update.message.reply_video(movies[code])
    else:
        await update.message.reply_text("❌ Bunday kino topilmadi")

# App yaratish
app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POSTS, channel_post))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), user_message))

# Botni ishga tushirish
app.run_polling()
