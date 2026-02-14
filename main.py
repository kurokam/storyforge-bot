import os
import time
from collections import defaultdict

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from ai import generate_story

# Railway Variables içine BOT_TOKEN eklediğinden emin ol
TOKEN = os.getenv("BOT_TOKEN")

# Günlük ücretsiz kullanım limiti
USER_LIMIT = defaultdict(lambda: {"count": 0, "date": time.strftime("%Y-%m-%d")})
DAILY_LIMIT = 5


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hoş geldin!\n\n"
        "Bu bot, YouTube Shorts için viral korku/gizem hikayeleri üretir.\n\n"
        "Kullanım:\n"
        "/story korku\n"
        "/story gizem\n"
        "/story komplo\n\n"
        "Günde 5 ücretsiz üretim hakkın var."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Komutlar:\n\n"
        "/story <konu>  → Hikaye üretir\n"
        "/start         → Tanıtım\n"
        "/help          → Yardım\n\n"
        "Örnek:\n"
        "/story korku"
    )


async def story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    today = time.strftime("%Y-%m-%d")

    if USER_LIMIT[uid]["date"] != today:
        USER_LIMIT[uid] = {"count": 0, "date": today}

    if USER_LIMIT[uid]["count"] >= DAILY_LIMIT:
        await update.message.reply_text(
            "❌ Günlük ücretsiz limit doldu.\n\n"
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
        raise RuntimeError("❌ BOT_TOKEN bulunamadı! Railway Variables'a ekle.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("story", story))

    print("🤖 Bot calisiyor...")
    app.run_polling()


if __name__ == "__main__":
    main()