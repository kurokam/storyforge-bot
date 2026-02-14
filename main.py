import os
import time
from collections import defaultdict

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

from ai import generate_story

TOKEN = os.getenv("BOT_TOKEN")

USER_LIMIT = defaultdict(lambda: {"count": 0, "date": time.strftime("%Y-%m-%d")})
DAILY_LIMIT = 5


def main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("😱 Korku", callback_data="korku"),
            InlineKeyboardButton("🕵️ Gizem", callback_data="gizem"),
        ],
        [
            InlineKeyboardButton("🧩 Komplo", callback_data="komplo"),
            InlineKeyboardButton("📜 Gerçek", callback_data="gercek"),
        ],
        [
            InlineKeyboardButton("🌑 Karanlık Sırlar", callback_data="karanlik"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hoş geldin!\n\n"
        "YouTube Shorts için viral hikayeler üretirim.\n\n"
        "Aşağıdan tür seç:",
        reply_markup=main_menu_keyboard()
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Menüden bir tür seç veya komut kullan:\n\n"
        "/korku\n"
        "/gizem\n"
        "/komplo\n"
        "/gercek\n"
        "/karanlik\n\n"
        "Ya da:\n"
        "/story <konu>"
    )


async def _handle_story(update: Update, context: ContextTypes.DEFAULT_TYPE, kind: str):
    uid = update.effective_user.id
    today = time.strftime("%Y-%m-%d")

    if USER_LIMIT[uid]["date"] != today:
        USER_LIMIT[uid] = {"count": 0, "date": today}

    if USER_LIMIT[uid]["count"] >= DAILY_LIMIT:
        await update.effective_user.send_message(
            "❌ Günlük ücretsiz limit doldu.\n\n"
            "Sınırsız kullanım için:\n"
            "👉 https://t.me/seninlinkin"
        )
        return

    USER_LIMIT[uid]["count"] += 1

    await update.effective_user.send_message(f"🧠 {kind.title()} hikayesi hazırlanıyor...")
    text = await generate_story(kind)
    await update.effective_user.send_message(text)


async def on_menu_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    kind_map = {
        "korku": "korku",
        "gizem": "gizem",
        "komplo": "komplo",
        "gercek": "gerçek hikaye",
        "karanlik": "karanlık sırlar",
    }

    kind = kind_map.get(query.data, "korku")
    await _handle_story(update, context, kind)


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
    app.add_handler(CommandHandler("story", story))

    app.add_handler(CallbackQueryHandler(on_menu_click))

    print("🤖 Bot calisiyor...")
    app.run_polling()


if __name__ == "__main__":
    main()