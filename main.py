import os
import json
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
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

AD_MESSAGE = "\n\n🔥 Created with Storyforge AI Bot"

async def story_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=code)] for name, code in CATEGORIES]
    await update.message.reply_text(
        "🎬 Choose a story category:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category_map = {
        "cat_horror": "Horror",
        "cat_mystery": "Mystery",
        "cat_true": "True Story",
        "cat_psychological": "Psychological",
    }

    context.user_data["category"] = category_map.get(query.data)

    keyboard = [[InlineKeyboardButton(name, callback_data=code)] for name, code in DURATIONS]
    await query.edit_message_text(
        "⏱️ Choose duration:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def duration_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    duration_map = {
        "dur_30s": "30s",
        "dur_60s": "60s",
        "dur_90s": "90s",
    }

    duration = duration_map.get(query.data)
    category = context.user_data.get("category")

    await query.edit_message_text("⏳ Generating content...")

    result = generate_story(category, duration) + AD_MESSAGE

    context.user_data["last_result"] = result

    await query.edit_message_text(result[:4000])

    keyboard = [
        [
            InlineKeyboardButton("⬇️ Download TXT", callback_data="download_txt"),
            InlineKeyboardButton("⬇️ Download JSON", callback_data="download_json"),
        ]
    ]

    await query.message.reply_text(
        "Download format:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def download_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    content = context.user_data.get("last_result", "")

    if query.data == "download_txt":
        filename = "story.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        await query.message.reply_document(InputFile(filename))

    elif query.data == "download_json":
        filename = "story.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({"content": content}, f, indent=2)
        await query.message.reply_document(InputFile(filename))

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("story", story_menu))
    app.add_handler(CallbackQueryHandler(category_handler, pattern="^cat_"))
    app.add_handler(CallbackQueryHandler(duration_handler, pattern="^dur_"))
    app.add_handler(CallbackQueryHandler(download_handler, pattern="^download_"))

    print("🤖 Pro Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()