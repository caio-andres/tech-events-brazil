import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_URL = os.getenv("DISCORD_URL")
DB_JSON_URL = os.getenv("DB_JSON_URL")
