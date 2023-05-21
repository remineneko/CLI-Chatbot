from langchain.schema import Generation
from langchain.callbacks.manager import Callbacks

from typing import Union, List
from pathlib import Path

from src.utils.config import Config


class ModelMixin:
    @classmethod
    def from_cfg(cls, cfg_file: Union[Path, str]):
        return cls(**Config.from_file(cfg_file).cfg.model)
    
    def answer(self, prompt: Union[str, List[str]], stops: List[str]=None, callbacks: Callbacks=None):
        if isinstance(prompt, str):
            prompt = [prompt]
        generated: List[Generation] = self.generate(prompt, stops, callbacks)
        return generated.generations[0][0].text