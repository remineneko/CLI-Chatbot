import click

from typing import Union
from pathlib import Path
from click_repl import register_repl
from pydantic.error_wrappers import ValidationError

from constants import DEFAULT_CHATBOT_CONFIG
from src.utils.config import Config
from src.utils.custom_memory import ConversationMemory
from src.models.model_picker import get_model
from src.cli.cli import CLI
from src.ingest_data.ingest import Ingest

def load_config(config_file: Union[Path, str]):
    config = Config.from_file(config_file).cfg.config
    model_name = config.model_name
    model_config_file = config.model_config_file
    model_vector_db = config.model_vector_db
    chat_type = config.chat_option
    return model_name, model_config_file, model_vector_db, chat_type

@click.group()
def main():
    pass

@main.command()
@click.option('--config_file', '-cf', default=DEFAULT_CHATBOT_CONFIG, help='A premade config file for the chatbot.')
def start(config_file: Union[Path, str]):
    model_name, model_config_file, model_vector_db, chat_type = load_config(config_file)
    model = get_model(model_name).from_cfg(model_config_file)
    if chat_type == "cli":
        CLI().run(model=model, vector_db=model_vector_db, memory = ConversationMemory(memory_key='chat_history'))


@main.command()
@click.option('--file', '-f', default=None, help='Ingests a file, a path to file, an entire folder, or an url. Currently only supports ReadTheDocs urls.')
def ingest(file: Union[str, Path]):
    if not file:
        click.echo("A file must be included to ingest.")
    else:
        click.echo(f"Ingesting data from {file}")
        Ingest(file).ingest()


if __name__ == "__main__":
    register_repl(main)
    main()