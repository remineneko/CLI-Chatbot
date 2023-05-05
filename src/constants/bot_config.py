import configparser
from typing import Union
from pathlib import Path
from src.logger import ChatbotHandler
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
    def __init__(self):
        self._config_logger = logging.getLogger(__name__)
        self._config_logger.setLevel(logging.INFO)
        self._config_logger.addHandler(ChatbotHandler())
        
        self._config_logger.info("Setting up the bot... Please wait a moment.")

    def __check_existence(self, key):
        if key in os.environ:
            return os.environ[key]
        else:
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
        


