import logging
import os
from typing import Union, List


class ChatbotHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        fmt = '%(asctime)-18s %(levelname)-8s: %(message)s'
        fmt_date = '%Y-%m-%d %T'
        formatter = logging.Formatter(fmt, fmt_date)
        self.setFormatter(formatter)


class ChatbotLogger:
    def __init__(self):
        cur_working_dir = os.path.dirname(__file__)
        log_dir = os.path.join(cur_working_dir, "../logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = 'activity.log'
        error_file = 'error.log'

        fmt = '%(asctime)-18s %(levelname)-8s: %(message)s'
        fmt_date = '%Y-%m-%d %T'
        formatter = logging.Formatter(fmt, fmt_date)


        self.file_handler = logging.FileHandler(
            os.path.join(log_dir, log_file), "a", "utf-8"
        )
        self.file_handler.setLevel(logging.DEBUG)
        
        self.file_handler.setFormatter(formatter)

        self.error_handler = logging.FileHandler(
            os.path.join(log_dir, error_file), "a", "utf-8"
        )
        self.error_handler.setLevel(logging.ERROR)
        
        self.error_handler.setFormatter(formatter)

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ChatbotHandler())
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.error_handler)
        self.logger.setLevel(logging.DEBUG)

    def debug(self, message, title=""):
        self._log(title, message, logging.DEBUG)

    def info(self, message, title=""):
        self._log(title, message, logging.INFO)

    def warn(self, message, title=""):
        self._log(title, message, logging.WARN)

    def error(self, title, message=""):
        self._log(title, message, logging.ERROR)

    def _log(self, title: str = "", message: Union[str, List] = "", level=logging.INFO,):
        if message:
            if isinstance(message, list):
                message = " ".join(message)
        self.logger.log(
            level, message, extra={"title": str(title)}
        )