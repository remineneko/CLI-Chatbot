from src.base_objects import ChatOutput, InputStream, LLMModel
from src.constants import CHATBOT_API_TOKEN
from src.logger import ChatbotLogger
from src.exceptions import InvalidAPIKey, InvalidPrompt

from gpt4all import GPT4All
from typing import Union, List, Dict, Any, Optional


class GPT4AllOutput(ChatOutput):
    @property
    def answer(self):
        return self.output
    

class GPT4All_Model(LLMModel):
    def __init__(
            self,
            model_name = "gpt4all",
            pretrained_file = None
        ):
        pass