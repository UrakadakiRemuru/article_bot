def main():
    """
    Инициализирует Telegram-бота и запускает polling.
    """
    import os
    from dotenv import load_dotenv
    from telegram.ext import ApplicationBuilder
    from telegram.ext import MessageHandler
    from telegram.ext import CommandHandler
    from telegram.ext import filters
    from telegram_bot import start, get_article, handle_link
    load_dotenv()

    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise RuntimeError("Переменная окружения BOT_TOKEN не установлена.")

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_article", get_article))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    application.run_polling()


if __name__ == '__main__':
    main()
