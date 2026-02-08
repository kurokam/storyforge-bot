import os
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

USERS = {}  # {user_id: {"lang": "tr", "premium_until": date}}

def is_premium(user_id):
    user = USERS.get(user_id)
    if not user:
        return False
    return user.get("premium_until", datetime.date.today()) >= datetime.date.today()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 StoryForge AI\n\n"
        "Dil seç:\n"
        "/tr Türkçe\n"
        "/en English\n\n"
        "Premium: /premium"
    )

async def set_tr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USERS.setdefault(update.effective_user.id, {})["lang"] = "tr"
    await update.message.reply_text("Dil Türkçe olarak ayarlandı 🇹🇷")

async def set_en(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USERS.setdefault(update.effective_user.id, {})["lang"] = "en"
    await update.message.reply_text("Language set to English 🇬🇧")

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💎 StoryForge Premium\n\n"
        "Basic: 199 TL / ay\n"
        "Pro: 399 TL / ay (Sınırsız)\n\n"
        "Ödeme: https://shopier.com/ODEME_LINKIN\n\n"
        "Ödeme yaptıysan: /odeme_bildirim"
    )

async def horror(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_premium(uid):
        await update.message.reply_text("❌ Premium üye değilsin. /premium")
        return

    lang = USERS.get(uid, {}).get("lang", "tr")
    if lang == "tr":
        content = (
            "HOOK: Bu dosya 17 yıl kilitli kaldı...\n\n"
            "SCRIPT: Karanlık bir arşivde File-X...\n\n"
            "CAPCUT: 1) Karanlık koridor 2) Kırmızı dosya 3) Siluet"
        )
    else:
        content = (
            "HOOK: This file was sealed for 17 years...\n\n"
            "SCRIPT: In a dark archive, File-X...\n\n"
            "CAPCUT: 1) Dark hallway 2) Red file 3) Shadow figure"
        )

    await update.message.reply_text(content)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tr", set_tr))
    app.add_handler(CommandHandler("en", set_en))
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(CommandHandler("horror", horror))
    app.run_polling()

if __name__ == "__main__":
    main()
