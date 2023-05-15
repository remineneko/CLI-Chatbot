from dataclasses import dataclass
from .screen import Screen
from typing import Dict
from abc import ABC, abstractmethod


@dataclass
class ChatOutput:
    output: Dict

    @property
    @abstractmethod
    def answer(self):
        pass

    def show_output(self, screen: Screen):
        screen.output_source.show(self.output)
