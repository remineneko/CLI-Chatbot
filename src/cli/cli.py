from src.base_objects import Screen, OutputSource
from commands.base_commands import Command
import sys
import click


class StandardOutput(OutputSource):
    def __init__(self, source=sys.stdout):
        super().__init__(source)
    
    def show(self, data):
        self.source.write(data)


class CLI(Screen, Command):
    def __init__(self, output_source=StandardOutput, voice_output=None, voice_input=None):
        super().__init__(output_source, voice_input, voice_output)
    
    @click.group()
    def main_cli():
        pass

    def run(self):
        self.main_cli()

    