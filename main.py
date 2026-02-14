from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from ai import generate_story

TOKEN = os.getenv("BOT_TOKEN")

async def story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kind = "horror"
    if context.args:
        kind = " ".join(context.args)

    await update.message.reply_text("🧠 Hikaye hazırlanıyor...")
    text = await generate_story(kind)
    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("story", story))
    app.run_polling()

if __name__ == "__main__":
    import os
    main()