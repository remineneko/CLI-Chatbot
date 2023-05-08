import json
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

    def _load_file(self, file):
        with open(file, 'r') as f:
            return edict(json.load(f))
        
    def save(self, file):
        with open(file, 'w') as f:
            return json.dump(self._past_data, f)
        
    @property
    def past_interactions(self):
        return self._past_data.chat_data
    
    @past_interactions.setter
    def past_interactions(self, new_data):
        self._past_data.chat_data = new_data
    
    @property
    def title(self):
        return self._past_data.title
    
    @property
    def file_name(self):
        return self._past_data.filename
    
    @property
    def summary(self):
        return self._past_data.summary
    
    @summary.setter
    def summary(self, new_summary):
        self._past_data.summary = new_summary
    
    @property
    def file_name_no_ext(self):
        return os.path.splitext(self._past_data.filename)[0]