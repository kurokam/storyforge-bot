import os
import time
from collections import defaultdict

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from ai import generate_story

TOKEN = os.getenv("BOT_TOKEN")

USER_LIMIT = defaultdict(lambda: {"count": 0, "date": time.strftime("%Y-%m-%d")})
DAILY_LIMIT = 5


async def story(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    kind = "korku"
    if context.args:
        kind = " ".join(context.args)

    await update.message.reply_text("🧠 Hikaye hazırlanıyor...")
    text = await generate_story(kind)
    await update.message.reply_text(text)


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN bulunamadı! Railway Variables'a ekle.")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("story", story))
    app.run_polling()


if __name__ == "__main__":
    main()