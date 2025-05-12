import logging

from telegram import Update
from telegram.ext import ContextTypes

from database_manager import AsyncSQLiteManager, Exists
from utilities import is_valid_url

DB_PATH = 'articles.db'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает команду /start. Отправляет описание возможностей бота.

    Args:
        update (Update): Объект обновления от Telegram.
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения.
    """
    text = (
        "Привет! Я бот, который поможет не забыть прочитать статьи, найденные тобой в интернете :)\n"
        "Чтобы я запомнил статью, достаточно передать мне ссылку на нее.\n"
        "Например, https://example.com\n"
        "Чтобы получить случайную статью, вызови или напиши команду /get_article.\n"
        "Помни, отдавая тебе статью на прочтение, она больше не хранится в моей базе."
        "Так что тебе нужно ее изучить"
    )
    await update.message.reply_text(text)


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает текстовые сообщения — предполагает, что это ссылка.

    Args:
        update (Update): Объект обновления от Telegram.
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения.
    """
    url = update.message.text.strip()

    if not is_valid_url(url):
        await update.message.reply_text("❌ Неверный формат ссылки. Убедись, что это полноценный URL.")
        return

    async with AsyncSQLiteManager(DB_PATH) as db:
        try:
            await db.add_link(url)
            await update.message.reply_text("Ссылка успешно добавлена в базу данных.")
        except Exists:
            await update.message.reply_text("Вы уже сохраняли эту статью!")


async def get_article(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает команду /get_article. Отправляет случайную статью и удаляет её из базы.

    Args:
        update (Update): Объект обновления от Telegram.
        context (ContextTypes.DEFAULT_TYPE): Контекст выполнения.
    """
    async with AsyncSQLiteManager(DB_PATH) as db:
        article = await db.get_random_link_and_delete()
        if article:
            await update.message.reply_text(f"Вы хотели прочитать:\n{article}\n Самое время это сделать!")
        else:
            await update.message.reply_text("Пока что вы не сохранили ни одной статьи. "
                                            "Отправляйте мне ссылки и я сохраню их!")
