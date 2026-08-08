import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID"))  # sirf aapki Telegram user ID

SOURCE_CHAT_IDS_RAW = os.getenv("SOURCE_CHAT_IDS", "")
SOURCE_CHAT_IDS = set(int(x.strip()) for x in SOURCE_CHAT_IDS_RAW.split(",") if x.strip())

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bot active hai.")

async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/post <message ya link> — sirf admin use kar sakta hai, target group mein bhejta hai."""
    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("❌ Aapko ye command use karne ki permission nahi hai.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /post <message ya link>")
        return

    text_to_send = " ".join(context.args)

    try:
        await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=text_to_send)
        await update.message.reply_text("✅ Target group mein bhej diya.")
    except Exception as e:
        logging.error(f"Failed to send: {e}")
        await update.message.reply_text(f"❌ Error: {e}")

async def handle_media_and_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message

    if msg.chat_id not in SOURCE_CHAT_IDS:
        return

    caption = msg.caption or ""

    try:
        if msg.video:
            await context.bot.send_video(chat_id=TARGET_CHAT_ID, video=msg.video.file_id, caption=caption)
        elif msg.photo:
            await context.bot.send_photo(chat_id=TARGET_CHAT_ID, photo=msg.photo[-1].file_id, caption=caption)
        elif msg.document:
            await context.bot.send_document(chat_id=TARGET_CHAT_ID, document=msg.document.file_id, caption=caption)
        elif msg.text:
            await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=msg.text)
    except Exception as e:
        logging.error(f"Failed to forward message from {msg.chat_id}: {e}")

def main() -> None:
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set")
    if not TARGET_CHAT_ID:
        raise ValueError("TARGET_CHAT_ID environment variable not set")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post_command))

    media_filter = filters.VIDEO | filters.PHOTO | filters.Document.ALL | filters.TEXT
    app.add_handler(MessageHandler(media_filter & ~filters.COMMAND, handle_media_and_text))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
