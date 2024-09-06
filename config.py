import os
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.environ.get("TG_TOKEN", "")
YAM_TOKEN = os.environ.get("YAM_TOKEN", "")
DUMP_CHAT_ID = os.environ.get("DUMP_CHAT_ID", "")
DB_PATH = os.environ.get("DB_PATH", "./data/bot.db")
