from src.base_objects import Screen, OutputSource
from commands import CoreCommands
from click_repl import register_repl
import sys
import click


class StandardOutput(OutputSource):
    def __init__(self, source=sys.stdout):
        super().__init__(source)
    
    def show(self, data):
        self.source.write(data)


class CLI(Screen):
    def __init__(self, output_source=StandardOutput, voice_output=None, voice_input=None):
        super().__init__(output_source, voice_input, voice_output)
    
    @staticmethod
    @click.group()
    def _cli():
        pass

    def run(self):
        CoreCommands().setup(self.main_cli)
        register_repl(self.main_cli)
        self._cli()