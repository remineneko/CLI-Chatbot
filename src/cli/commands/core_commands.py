from .base_commands import Command
import click
from typing import Union
from pathlib import Path
from src.ingest_data.ingest import Ingest



class CoreCommands(Command):
    @staticmethod
    @click.command()
    def hello():
        click.echo("Hello")

    @staticmethod
    @click.command()
    @click.option('--file', '-f', default=None, help='Ingests a file, a path to file, an entire folder, or an url. Currently only supports ReadTheDocs urls.')
    def ingest(file: Union[str, Path]):
        if not file:
            click.echo("A file must be included to ingest.")
            exit()
        else:
            click.echo(f"Ingesting data from {file}")
            Ingest(file).ingest()

    def _get_commands(self):
        return [
            "hello",
            "ingest"
        ]