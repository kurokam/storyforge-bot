import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from ai import generate_story

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")]
    ]
    await update.message.reply_text(
        "🌍 Dil seç:\nChoose language:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def lang_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.replace("lang_", "")
    context.user_data["lang"] = lang

    keyboard = [
        [InlineKeyboardButton("👻 Korku", callback_data="korku")],
        [InlineKeyboardButton("🕵️ Gizem", callback_data="gizem")],
        [InlineKeyboardButton("😱 Gercek Olay", callback_data="gercek")],
        [InlineKeyboardButton("🧠 Psikolojik", callback_data="psikolojik")]
    ]

    text = "🎬 Hikâye türü seç:" if lang == "tr" else "🎬 Choose a story type:"
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get("lang", "tr")
    category = query.data

    loading_text = "⏳ Hikâye hazırlanıyor..." if lang == "tr" else "⏳ Generating story..."
    await query.edit_message_text(loading_text)

    try:
        result = generate_story(category, lang)
        await query.edit_message_text(result)
    except Exception as e:
        await query.edit_message_text(f"❌ AI hata verdi:\n{str(e)}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(lang_handler, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(category_handler))

    print("🤖 Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()