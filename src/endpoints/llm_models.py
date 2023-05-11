from abc import ABC, abstractmethod
from .source import Source
from .output import ChatOutput


class LLMModel(ABC):
    def __init__(self, model, **kwargs):
        """
        Initialize the LLMModel class.

        Args:
            model_name (_type_): _description_
            required_imports (tuple, optional): _description_. Defaults to (None, None).
        """
        self.model = model
        self.__dict__.update(kwargs)

    @abstractmethod
    def generate(self, prompt: Source) -> ChatOutput:
        pass