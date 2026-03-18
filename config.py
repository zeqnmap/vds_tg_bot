import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(CURR_DIR, 'logs')

DATABASE_PATH = 'vds_database.db'

NOTIFICATION_CHAT_ID = os.getenv('NOTIFICATION_CHAT_ID')  # id чата или группы
NOTIFICATION_INTERVAL = int(os.getenv('NOTIFICATION_INTERVAL', 5)) # секунд между проверками

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(CURR_DIR, 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)