import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your actual Bot Token from BotFather
BOT_TOKEN = 8501592088:AAEdyVB18kZLgzAfklsdDk0lvxj-uxHcmaQ

# Target Channel or Group (Use @channel_username or numerical ID like -100xxxxxxxxxx)
TARGET_CHAT_ID = -1002912706519

# Enable logging to monitor bot activity in the terminal
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a greeting when the command /start is issued."""
    await update.message.reply_text("Send me a video, and I will post it to the channel!")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming videos and posts them to the target group or channel."""
    video = update.message.video
    caption = update.message.caption or ""  # Retain original caption if present

    try:
        # Option A: Send as a new post using the video file ID (Faster & saves bandwidth)
        await context.bot.send_video(
            chat_id=TARGET_CHAT_ID,
            video=video.file_id,
            caption=caption
        )
        
        # Option B: Uncomment below if you prefer forwarding instead of posting fresh
        # await update.message.forward(chat_id=TARGET_CHAT_ID)

        await update.message.reply_text("✅ Video successfully posted!")
        
    except Exception as e:
        logging.error(f"Failed to send video: {e}")
        await update.message.reply_text(f"❌ Failed to post video. Error: {e}")

def main() -> None:
    """Start the bot."""
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
