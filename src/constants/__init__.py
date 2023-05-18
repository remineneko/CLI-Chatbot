import os

from .bot_config import ChatbotConfig
from dir_constants import ROOT_FOLDER

config = ChatbotConfig()

CHATBOT_API_TOKEN = config.api_token
DATABASE_HOST = config.db_host
DATABASE_USERNAME = config.db_username
DATABASE_PASSWORD = config.db_password

PERSIST_DB_FOLDER = os.path.join(ROOT_FOLDER, 'chromadb')
if not os.path.isdir(PERSIST_DB_FOLDER):
    os.makedirs(PERSIST_DB_FOLDER, mode=0o777)
