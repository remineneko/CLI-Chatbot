from .bot_config import ChatbotConfig

config = ChatbotConfig()

CHATBOT_API_TOKEN = config.api_token
DATABASE_HOST = config.db_host
DATABASE_USERNAME = config.db_username
DATABASE_PASSWORD = config.db_password