import os
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
CHROMA_DEFAULT_COLLECTION_NAME = os.environ.get('CHROMA_DEFAULT_COLLECTION_NAME')
CHATBOT_NAME = os.environ.get('CHATBOT_NAME')
DEFAULT_USER_NAME = os.environ.get("USER_DEFAULT_NAME")

ROOT_FOLDER = os.path.dirname(os.path.realpath(__file__))

PERSIST_DB_FOLDER = os.path.join(ROOT_FOLDER, 'chromadb')
if not os.path.isdir(PERSIST_DB_FOLDER):
    os.makedirs(PERSIST_DB_FOLDER, mode=0o777)

SRC_FOLDER = os.path.join(ROOT_FOLDER, 'src')
CONFIG_FOLDER = os.path.join(SRC_FOLDER, 'configs')
DEFAULT_GPT4ALL_CONFIG = os.path.join(CONFIG_FOLDER, 'default_gpt4all_config.py')
DEFAULT_CHATBOT_CONFIG = os.path.join(CONFIG_FOLDER, 'default_chatbot_config.py')

CHROMA_DEFAULT_SETTINGS = Settings(
        chroma_db_impl='duckdb+parquet',
        persist_directory=PERSIST_DB_FOLDER,
        anonymized_telemetry=False
    )

HUGGING_FACE_DEFAULT_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

with open(os.environ.get("PROMPT_FILE")) as f:
    DEFAULT_CHATBOT_PROMPT = f.read()