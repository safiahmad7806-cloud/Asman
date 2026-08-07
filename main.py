import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your NEW Bot Token from BotFather inside quotes
BOT_TOKEN = os.getenv(8501592088:AAEdyVB18kZLgzAfklsdDk0lvxj-uxHcmaQ)

# Target Channel or Group ID (Keep the quotes around numerical IDs)
TARGET_CHAT_ID = os.getenv(-1002912706519)

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

    try:
        # Handle Video
        if msg.video:
            await context.bot.send_video(
                chat_id=TARGET_CHAT_ID,
                video=msg.video.file_id,
                caption=caption
            )

        # Handle Photo (pick the highest resolution available)
        elif msg.photo:
            await context.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=msg.photo[-1].file_id,
                caption=caption
            )

        # Handle Document/File (e.g., uncompressed videos/images)
        elif msg.document:
            await context.bot.send_document(
                chat_id=TARGET_CHAT_ID,
                document=msg.document.file_id,
                caption=caption
            )

        # Handle Plain Text & Links
        elif msg.text:
            await context.bot.send_message(
                chat_id=TARGET_CHAT_ID,
                text=msg.text
            )

        await msg.reply_text("✅ Message successfully posted to channel!")

    except Exception as e:
        logging.error(f"Failed to post message: {e}")
        await msg.reply_text(f"❌ Failed to post message. Error: {e}")

def main() -> None:
    """Start the bot."""
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
        
