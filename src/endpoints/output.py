from pydantic import BaseModel
from .screen import Screen


class ChatOutput(BaseModel):
    output: str

    def show_output(self, screen: Screen):
        screen.output_source.show(self.output)
