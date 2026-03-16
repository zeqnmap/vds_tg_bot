import aiosqlite
from utils.logger_conf import setup_logger
from typing import Optional
from .models import User

logger = setup_logger(__name__)

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def create_tables(self):
        async with aiosqlite.connect(self.db_path) as db:

            await db.execute('PRAGMA journal_mode=WAL')
            await db.execute('PRAGMA synchronous=NORMAL')
            await db.execute('PRAGMA cache_size=10000')
            await db.execute('PRAGMA temp_store=MEMORY')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.commit()
            logger.info("Database tables created/verified")

    async def add_user(self, user_id: int, username: Optional[str] = None) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    INSERT OR REPLACE INTO users (user_id, username)
                    VALUES (?, ?)
                ''', (user_id, username))
                await db.commit()
                logger.info(f"User {user_id} ({username}) added/updated")
                return True
        except Exception as e:
            logger.error(f"Error adding user: {e}")
            return False

    async def get_user(self, user_id: int) -> Optional[User]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                'SELECT user_id, username FROM users WHERE user_id = ?',
                (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return User(user_id=row['user_id'], username=row['username'])
                return None

    async def get_all_users(self):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT user_id, username FROM users') as cursor:
                rows = await cursor.fetchall()
                return [User(user_id=row['user_id'], username=row['username']) for row in rows]

    async def user_exists(self, user_id: int) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT 1 FROM users WHERE user_id = ?',
                (user_id,)
            ) as cursor:
                return await cursor.fetchone() is not None

    async def delete_user(self, user_id: int) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
                await db.commit()
                logger.info(f"User {user_id} deleted")
                return True
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return False