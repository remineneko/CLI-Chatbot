from .base_commands import Command
import click
from typing import Union
from pathlib import Path



class CoreCommands(Command):
    @staticmethod
    @click.command()
    def hello():
        click.echo("Hello")

    @staticmethod
    @click.command()
    @click.option('--file', '-f', default=None, help='Ingests a file, or a path to file, or an entire folder.')
    def ingest(file: Union[str, Path]):
        if not file:
            click.echo("A file must be included to ingest.")
            exit()
        else:
            pass

    def _get_commands(self):
        return [
            "hello",
            "ingest"
        ]