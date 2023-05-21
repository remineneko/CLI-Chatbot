from langchain.llms import GPT4All
from langchain.schema import Generation, LLMResult
from langchain.callbacks.manager import Callbacks

from typing import Union, List
from pathlib import Path

from src.utils.config import Config


class GPT4AllModel_(GPT4All):
    @classmethod
    def from_cfg(cls, cfg_file: Union[Path, str]):
        return cls(**Config.from_file(cfg_file).cfg.model)
    
    def answer(self, prompt: Union[str, List[str]], stops: List[str]=None, callbacks: Callbacks=None):
        if isinstance(prompt, str):
            prompt = [prompt]
        generated: List[Generation] = self.generate(prompt, stops, callbacks)
        return generated.generations[0][0].text