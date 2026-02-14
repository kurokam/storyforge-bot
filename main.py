import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from ai import generate_story

TOKEN = os.getenv("BOT_TOKEN")

AVAILABLE_TYPES = {
    "horror": "Horror",
    "mystery": "Mystery",
    "true": "True Story",
    "psychological": "Psychological"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎬 Storyforge Bot\n\n"
        "Use this command in group or private chat:\n\n"
        "/story horror abandoned hospital at night\n"
        "/story mystery strange phone call\n"
        "/story true creepy neighbor story\n"
        "/story psychological paranoia in a small town\n"
    )
    await update.message.reply_text(text)

async def story_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "⚠️ Please specify a type.\n\n"
            "Example:\n"
            "/story horror abandoned hospital"
        )
        return

    story_type_key = context.args[0].lower()
    topic = " ".join(context.args[1:]) if len(context.args) > 1 else ""

    if story_type_key not in AVAILABLE_TYPES:
        await update.message.reply_text(
            "❌ Invalid type.\n\nAvailable types:\n"
            "horror\nmystery\ntrue\npsychological"
        )
        return

    await update.message.reply_text("⏳ Generating your story...")

    try:
        result = generate_story(AVAILABLE_TYPES[story_type_key], topic)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ AI error:\n{str(e)}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("story", story_command))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()