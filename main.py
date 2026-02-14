import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from ai import generate_story

TOKEN = os.getenv("BOT_TOKEN")

CATEGORIES = [
    ("Horror", "cat_horror"),
    ("Mystery", "cat_mystery"),
    ("True Story", "cat_true"),
    ("Psychological", "cat_psychological"),
]

DURATIONS = [
    ("30s", "dur_30s"),
    ("60s", "dur_60s"),
    ("90s", "dur_90s"),
]

async def story_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=code)] for name, code in CATEGORIES]
    await update.message.reply_text(
        "🎬 Choose a story category:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category_code = query.data
    category_map = {
        "cat_horror": "Horror",
        "cat_mystery": "Mystery",
        "cat_true": "True Story",
        "cat_psychological": "Psychological",
    }

    category = category_map.get(category_code)
    context.user_data["category"] = category

    keyboard = [[InlineKeyboardButton(name, callback_data=code)] for name, code in DURATIONS]
    await query.edit_message_text(
        f"⏱️ Category: {category}\nChoose duration:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def duration_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    duration_code = query.data
    duration_map = {
        "dur_30s": "30s",
        "dur_60s": "60s",
        "dur_90s": "90s",
    }

    duration = duration_map.get(duration_code)
    category = context.user_data.get("category", "Horror")

    await query.edit_message_text("⏳ Generating your story...")

    try:
        result = generate_story(category, duration)
        await query.edit_message_text(result)
    except Exception as e:
        await query.edit_message_text(f"❌ AI error:\n{str(e)}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("story", story_menu))
    app.add_handler(CallbackQueryHandler(category_handler, pattern="^cat_"))
    app.add_handler(CallbackQueryHandler(duration_handler, pattern="^dur_"))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()