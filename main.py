import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from ai import generate_story

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")


def split_story_and_scenes(text: str):
    parts = {"main": text, "scenes": None}
    try:
        if "SAHNELER" in text:
            before, after = text.split("SAHNELER", 1)
            parts["main"] = before.strip()
            parts["scenes"] = "SAHNELER" + after.strip()
    except Exception:
        pass
    return parts


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["👻 Korku Hikayesi"],
        ["🏚 Terkedilmiş Mekan"],
        ["🕯 Paranormal Olay"],
        ["😱 Gerçek Hikaye"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🎬 Faceless YouTube Shorts AI Bot'a hoş geldin!\n\n"
        "Aşağıdan hikâye türü seç 👇",
        reply_markup=reply_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    mapping = {
        "👻 Korku Hikayesi": "korku",
        "🏚 Terkedilmiş Mekan": "terk edilmis mekan",
        "🕯 Paranormal Olay": "paranormal olay",
        "😱 Gerçek Hikaye": "gercek hayattan korku"
    }

    kind = mapping.get(text)

    if not kind:
        await update.message.reply_text("Lütfen menüden bir seçenek seç.")
        return

    await update.message.reply_text("⏳ Hikâye hazırlanıyor...")

    result = await generate_story(kind)
    parts = split_story_and_scenes(result)

    await update.effective_user.send_message(parts["main"])

    if parts["scenes"]:
        await update.effective_user.send_message(
            "🎬 CapCut için otomatik sahne promptları:\n\n" + parts["scenes"]
        )


if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("BOT_TOKEN ortam değişkeni tanımlı değil!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot çalışıyor...")
    app.run_polling()