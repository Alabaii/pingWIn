import logging

from telegram.ext import ApplicationBuilder, CommandHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update, context):
    logging.info("Команда /start вызвана")
    await update.message.reply_text("Привет! Я бот для проверки сайтов.")

if __name__ == "__main__":
    application = ApplicationBuilder().token("7834198872:AAFdjoRNdxdWvfzOSQKDqeSg01V0oevDFSc").build()
    application.add_handler(CommandHandler("start", start))
    logging.info("Бот запущен и ожидает команды.")
    application.run_polling()
