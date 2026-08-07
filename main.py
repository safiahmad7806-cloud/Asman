import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your Bot Token from BotFather (store in environment variable)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Target Channel or Group ID (store in environment variable)
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))

# Enable logging to monitor bot activity in the terminal
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a greeting when the command /start is issued."""
    await update.message.reply_text("Send me a video, photo, text message, or link, and I will post it to the channel!")

async def handle_media_and_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming videos, photos, links/text, and files, then posts them to the target group or channel."""
    msg = update.message
    caption = msg.caption or ""
    posted = False

    try:
        # Handle Video
        if msg.video:
            await context.bot.send_video(
                chat_id=TARGET_CHAT_ID,
                video=msg.video.file_id,
                caption=caption
            )
            posted = True

        # Handle Photo (pick the highest resolution available)
        elif msg.photo:
            await context.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=msg.photo[-1].file_id,
                caption=caption
            )
            posted = True

        # Handle Document/File (e.g., uncompressed videos/images)
        elif msg.document:
            await context.bot.send_document(
                chat_id=TARGET_CHAT_ID,
                document=msg.document.file_id,
                caption=caption
            )
            posted = True

        # Handle Plain Text & Links
        elif msg.text:
            await context.bot.send_message(
                chat_id=TARGET_CHAT_ID,
                text=msg.text
            )
            posted = True

        if posted:
            await msg.reply_text("✅ Message successfully posted to channel!")

    except Exception as e:
        logging.error(f"Failed to post message: {e}")
        await msg.reply_text(f"❌ Failed to post message. Error: {e}")

def main() -> None:
    """Start the bot."""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set")
    if not TARGET_CHAT_ID:
        raise ValueError("TARGET_CHAT_ID environment variable not set")
    
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    
    # Filter for videos, photos, documents, and text/links
    media_filter = filters.VIDEO | filters.PHOTO | filters.Document.ALL | filters.TEXT
    app.add_handler(MessageHandler(media_filter & ~filters.COMMAND, handle_media_and_text))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
