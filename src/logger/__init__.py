from .bot_handler import ChatbotHandler
import logging

def setup_logger():
    new_logger = logging.getLogger(__name__)
    new_logger.setLevel(logging.INFO)
    new_logger.addHandler(ChatbotHandler())

    return new_logger