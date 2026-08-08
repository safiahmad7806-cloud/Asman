import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Read from environment variables (set these in your shell/host, not in code)
BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Send me a video, photo, text message, or link, and I will post it to the channel!")

async def handle_media_and_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    caption = msg.caption or ""
    posted = False

    try:
        if msg.video:
            await context.bot.send_video(chat_id=TARGET_CHAT_ID, video=msg.video.file_id, caption=caption)
            posted = True
        elif msg.photo:
            await context.bot.send_photo(chat_id=TARGET_CHAT_ID, photo=msg.photo[-1].file_id, caption=caption)
            posted = True
        elif msg.document:
            await context.bot.send_document(chat_id=TARGET_CHAT_ID, document=msg.document.file_id, caption=caption)
            posted = True
        elif msg.text:
            await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=msg.text)
            posted = True

        if posted:
            await msg.reply_text("✅ Message successfully posted to channel!")

    except Exception as e:
        logging.error(f"Failed to post message: {e}")
        await msg.reply_text(f"❌ Failed to post message. Error: {e}")

def main() -> None:
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set")
    if not TARGET_CHAT_ID:
        raise ValueError("TARGET_CHAT_ID environment variable not set")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    media_filter = filters.VIDEO | filters.PHOTO | filters.Document.ALL | filters.TEXT
    app.add_handler(MessageHandler(media_filter & ~filters.COMMAND, handle_media_and_text))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
