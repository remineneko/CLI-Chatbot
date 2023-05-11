import pickle
from pathlib import Path
from typing import Union
import os
from easydict import EasyDict as edict


class ChatHistory:
    def __init__(self, history_file: Union[Path, str]):
        """ Loads the previous chat sessions with the chatbot.

        Args:
            history_file (Union[Path, str]): The path to the file containing past interactions with the chatbot.
        """
        self._past_data = self._load_file(history_file)
        self.file = history_file

    def _load_file(self, file):
        with open(file, 'r') as f:
            return pickle.load(f)
        
    def save(self, data):
        with open(self.file, 'w') as f:
            return pickle.dump(data, f)
        
    @property
    def history(self):
        return self._past_data