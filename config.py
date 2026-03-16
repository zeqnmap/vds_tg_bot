import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(CURR_DIR, 'logs')

DATABASE_PATH = 'vds_database.db'


