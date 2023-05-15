from base_commands import Command
import click


class CoreCommands(Command):
    @staticmethod
    @click.command()
    def hello():
        click.echo("Hello")

    def _get_commands(self):
        return [
            "hello"
        ]