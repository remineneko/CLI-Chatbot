from pydantic import BaseModel
from .screen import Screen
from typing import Dict
from abc import ABC, abstractmethod


class ChatOutput(BaseModel):
    output: Dict

    @property
    @abstractmethod
    def answer(self):
        pass

    def show_output(self, screen: Screen):
        screen.output_source.show(self.output)
