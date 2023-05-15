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


if __name__ == "__main__":
    test_prefix = ">>"
    from click_repl import register_repl
    
    @click.group()
    def cli():
        pass

    CoreCommands().setup(cli)

    register_repl(cli) # CTRL + D to exit session
    cli()