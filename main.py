import os
import time
from collections import defaultdict

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from ai import generate_story

TOKEN = os.getenv("BOT_TOKEN")

USER_LIMIT = defaultdict(lambda: {"count": 0, "date": time.strftime("%Y-%m-%d")})
DAILY_LIMIT = 5


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hoş geldin!\n\n"
        "YouTube Shorts için viral, faceless hikayeler üretirim.\n\n"
        "Menüden tür seçebilir ya da komut yazabilirsin:\n"
        "• /korku\n"
        "• /gizem\n"
        "• /komplo\n"
        "• /gercek\n"
        "• /karanlik\n\n"
        "Günde 5 ücretsiz hakkın var."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Komutlar:\n\n"
        "/korku     → Korku hikayesi\n"
        "/gizem     → Gizem hikayesi\n"
        "/komplo    → Komplo teorisi tarzı\n"
        "/gercek    → Gerçek olaylardan esinli\n"
        "/karanlik  → Karanlık sırlar\n\n"
        "Alternatif:\n"
        "/story <konu>\n"
        "Örnek: /story terk edilmiş hastane"
    )


async def _handle_story(update: Update, context: ContextTypes.DEFAULT_TYPE, kind: str):
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

    await update.message.reply_text(f"🧠 {kind.title()} hikayesi hazırlanıyor...")
    text = await generate_story(kind)
    await update.message.reply_text(text)


async def korku(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _handle_story(update, context, "korku")


async def gizem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _handle_story(update, context, "gizem")


async def komplo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _handle_story(update, context, "komplo")


async def gercek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _handle_story(update, context, "gerçek hikaye")


async def karanlik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _handle_story(update, context, "karanlık sırlar")


async def story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kind = "korku"
    if context.args:
        kind = " ".join(context.args)
    await _handle_story(update, context, kind)


def main():
    if not TOKEN:
        raise RuntimeError("❌ BOT_TOKEN bulunamadı! Railway Variables'a ekle.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))

    app.add_handler(CommandHandler("korku", korku))
    app.add_handler(CommandHandler("gizem", gizem))
    app.add_handler(CommandHandler("komplo", komplo))
    app.add_handler(CommandHandler("gercek", gercek))
    app.add_handler(CommandHandler("karanlik", karanlik))

    app.add_handler(CommandHandler("story", story))

    print("🤖 Bot calisiyor...")
    app.run_polling()


if __name__ == "__main__":
    main()