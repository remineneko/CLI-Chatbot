from constants.exceptions import *
import os
import logging

OPENAI_KEY = 'OPENAI_API_KEY'
DB_NAME = "DB_NAME"
DB_USERNAME = "DB_USERNAME"
DB_PASSWORD = "DB_PASSWORD"

class ChatbotConfig:
    """
    Sets up basic configurations for the bot.
    """
    def __init__(self, logger: logging.Logger):
        self._config_logger = logger   
        self._config_logger.info("Setting up the bot... Please wait a moment.")

    def __check_existence(self, key):
        if key in os.environ:
            self._config_logger.info(f"Environment variable {key} has been found.")
            return os.environ[key]
        else:
            self._config_logger.critical(f"Environment variable {key} does not exist.")
            raise EnvironmentVariableNotFoundException("The environment variables must be manually set before using this program.")

    @property
    def api_token(self):
        return self.__check_existence(OPENAI_KEY)
    
    @property
    def db_host(self):
        return self.__check_existence(DB_NAME)
    
    @property
    def db_username(self):
        return self.__check_existence(DB_USERNAME)
    
    @property
    def db_password(self):
        return self.__check_existence(DB_PASSWORD)
        


