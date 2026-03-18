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

            await db.execute('''
                        CREATE TABLE IF NOT EXISTS document_requests (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            doc_type TEXT,
                            fullname TEXT,
                            purpose TEXT,
                            period TEXT,
                            organization TEXT,
                            attachment TEXT,
                            attachment_name TEXT,
                            attachment_type TEXT,
                            child_fullname TEXT,
                            child_birth TEXT,
                            copy_type TEXT,
                            vacation_type TEXT,
                            ref_type TEXT,
                            petition_topic TEXT,
                            doc_name TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS app_state (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            await db.execute(
                'INSERT OR IGNORE INTO app_state (key, value) VALUES ("last_notification_id", "0")'
            )

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

    async def save_document_request(
            self,
            user_id,
            doc_type,
            fullname,
            purpose=None,
            period=None,
            organization=None,
            attachment=None,
            attachment_name=None,
            attachment_type=None,
            child_fullname=None,
            child_birth=None,
            copy_type=None,
            vacation_type=None,
            ref_type=None,
            petition_topic=None,
            doc_name=None
    ):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO document_requests (
                    user_id, doc_type, fullname, purpose, period, organization,
                    attachment, attachment_name, attachment_type,
                    child_fullname, child_birth, copy_type, vacation_type,
                    ref_type, petition_topic, doc_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, doc_type, fullname, purpose, period, organization,
                attachment, attachment_name, attachment_type,
                child_fullname, child_birth, copy_type, vacation_type,
                ref_type, petition_topic, doc_name
            ))
            await db.commit()


    async def get_last_processed_notification_id(self) -> int:
        """Возвращает последний ID заявки, по которой было отправлено уведомление"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                    'SELECT value FROM app_state WHERE key = "last_notification_id"'
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return int(row[0])
                await db.execute(
                    'INSERT OR IGNORE INTO app_state (key, value) VALUES ("last_notification_id", "0")'
                )
                await db.commit()
                return 0

    async def update_last_processed_notification_id(self, last_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'UPDATE app_state SET value = ? WHERE key = "last_notification_id"',
                (str(last_id),)
            )
            await db.commit()

    async def get_new_document_requests(self, last_id: int):
        """Возвращает список заявок с ID > last_id, отсортированных по возрастанию"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                    'SELECT * FROM document_requests WHERE id > ? ORDER BY id ASC',
                    (last_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]