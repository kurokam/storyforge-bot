import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from users import inc_use
from ads import get_ad

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 StoryForge AI\n\n"
        "Anime horror kısa hikâyeler üretirim.\n"
        "Bir sahne yaz, hikâyeni başlatayım 👇"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    prompt = update.message.text

    count = inc_use(user_id)

    story = f"🎬 Anime Horror Story:\n\n{prompt}\n\n" \
            f"— Karanlık bir şeyler kıpırdadı... (devamı gelir)"

    await update.message.reply_text(story)

    # Her 3 kullanımda 1 reklam
    if count % 3 == 0:
        ad = get_ad(count)
        await update.message.reply_text(f"📢 Sponsor:\n{ad}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
