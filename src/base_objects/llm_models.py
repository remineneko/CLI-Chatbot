from abc import ABC, abstractmethod
from .source import InputStream
from .output import ChatOutput
from typing import Union

class LLMModel(ABC):
    def __init__(self, model):
        """
        Initialize the LLMModel class.

        Args:
            model_name (_type_): _description_
            required_imports (tuple, optional): _description_. Defaults to (None, None).
        """
        self.model = model

    @abstractmethod
    def generate(self, prompt: Union[str,InputStream]) -> ChatOutput:
        pass