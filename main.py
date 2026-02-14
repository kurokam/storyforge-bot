import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from ai import generate_story
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from ai import generate_story
from collections import defaultdict
import time

USER_LIMIT = defaultdict(lambda: {"count": 0, "date": time.strftime("%Y-%m-%d")})
DAILY_LIMIT = 5

TOKEN = os.getenv("BOT_TOKEN")

async def story(update: Update, context:
uid = update.effective_user.id
today = time.strftime("%Y-%m-%d")

if USER_LIMIT[uid]["date"] != today:
    USER_LIMIT[uid] = {"count": 0, "date": today}

if USER_LIMIT[uid]["count"] >= DAILY_LIMIT:
    await update.message.reply_text(
        "❌ Günlük limit doldu.\n\n"
        "Sınırsız kullanım için:\n"
        "👉 https://t.me/seninlinkin"
    )
    return

USER_LIMIT[uid]["count"] += 1

 ContextTypes.DEFAULT_TYPE):
    kind = "horror"
    if context.args:
        kind = " ".join(context.args)

    await update.message.reply_text("🧠 Hikaye hazırlanıyor...")
    text = await generate_story(kind)
    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("story", story))
    app.run_polling()

if __name__ == "__main__":
    import os
    main()