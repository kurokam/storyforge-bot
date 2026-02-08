import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from users import inc_use
from ads import get_ad
from ai import generate_story

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 StoryForge AI\n\n"
        "Gerçek AI ile Shorts hikâyeleri üretirim:\n"
        "/horror → Anime Horror\n"
        "/mystery → Gizem Dosyası\n"
        "/scam → Dolandırıcılık Hikâyesi\n"
    )

async def horror(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_ai(update, "anime horror")

async def mystery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_ai(update, "mystery")

async def scam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_ai(update, "scam awareness")

async def send_ai(update: Update, kind: str):
    user_id = update.message.from_user.id
    count = inc_use(user_id)

    await update.message.reply_text("🧠 Hikâye hazırlanıyor...")

    content = await generate_story(kind)
    await update.message.reply_text(content)

    if count % 3 == 0:
        ad = get_ad(count)
        await update.message.reply_text(f"📢 Sponsor:\n{ad}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("horror", horror))
    app.add_handler(CommandHandler("mystery", mystery))
    app.add_handler(CommandHandler("scam", scam))
    app.run_polling()

if __name__ == "__main__":
    main()
