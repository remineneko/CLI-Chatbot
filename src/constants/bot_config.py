from .exceptions import *
import os
from src.logger import ChatbotLogger

OPENAI_KEY = 'OPENAI_API_KEY'

class ChatbotConfig:
    """
    Sets up basic configurations for the bot.
    """
    def __init__(self, logger = ChatbotLogger()):
        self._config_logger = logger   
        self._config_logger.info("Setting up the bot... Please wait a moment.")

    def __check_existence(self, key):
        if key in os.environ:
            self._config_logger.info(f"Environment variable {key} has been found.")
            return os.environ[key]
        else:
            self._config_logger.error(f"Environment variable {key} does not exist.")
            raise EnvironmentVariableNotFoundException("The environment variables must be manually set before using this program.")

    @property
    def api_token(self):
        return self.__check_existence(OPENAI_KEY)
        


