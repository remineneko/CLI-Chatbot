from dataclasses import dataclass
from .screen import Screen
from typing import Dict, Union
from abc import ABC, abstractmethod


@dataclass
class ChatOutput:
    output: Union[Dict, str]

    @property
    @abstractmethod
    def answer(self):
        pass

    def show_output(self, screen: Screen):
        screen.output_source.show(self.output)
