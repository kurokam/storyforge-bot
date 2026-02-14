import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from ai import generate_story

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👻 Horror", callback_data="Horror")],
        [InlineKeyboardButton("🕵️ Mystery", callback_data="Mystery")],
        [InlineKeyboardButton("😱 True Story", callback_data="True Story")],
        [InlineKeyboardButton("🧠 Psychological", callback_data="Psychological")]
    ]

    await update.message.reply_text(
        "🎬 Storyforge Bot\n\nChoose a story type:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data
    await query.edit_message_text("⏳ Generating your story...")

    try:
        story = generate_story(category)
        await query.edit_message_text(story)
    except Exception as e:
        await query.edit_message_text(f"❌ AI error:\n{str(e)}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(category_handler))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()