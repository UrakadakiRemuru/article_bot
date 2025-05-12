import aiosqlite
import random
from typing import Optional, Tuple

class Exists(Exception):
    """Исключение, поднимаемое при попытке вставить уже существующую ссылку в базу данных."""
    pass


class AsyncSQLiteManager:
    """Асинхронный контекстный менеджер для работы с SQLite базой данных."""

    def __init__(self, db_path):
        """
        Инициализация менеджера.

        Args:
            db_path (str): Путь к базе данных.
        """
        self.db_path = db_path
        self.connection: Optional[aiosqlite.Connection] = None

    async def __aenter__(self):
        """
        Вход в контекст. Открывает соединение и создаёт таблицу при необходимости.

        Returns:
            AsyncSQLiteManager: Текущий экземпляр менеджера.
        """
        self.connection = await aiosqlite.connect(self.db_path)
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL
            )
        ''')
        await self.connection.commit()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Выход из контекста. Закрывает соединение с базой данных.
        """
        await self.connection.close()

    async def add_link(self, url: str):
        """
        Добавляет новую ссылку в базу данных.

        Args:
            url (str): Ссылка на статью.

        Raises:
            Exists: Если такая ссылка уже есть в базе данных.
        """
        try:
            await self.connection.execute(
                'INSERT INTO articles (url) VALUES (?)',
                (url,)
            )
            await self.connection.commit()
        except aiosqlite.IntegrityError:
            raise Exists(f"Ссылка уже существует: {url}")

    async def get_random_link_and_delete(self) -> Optional[str]:
        """
        Получает случайную ссылку и удаляет её из базы.

        Returns:
            Optional[str]: Ссылка на статью, если найдена. Иначе — None.
        """
        async with self.connection.execute('SELECT id, url FROM articles') as cursor:
            rows = await cursor.fetchall()
            if not rows:
                return None
            row = random.choice(rows)
            await self.connection.execute('DELETE FROM articles WHERE id = ?', (row[0],))
            await self.connection.commit()
            return row[1]
