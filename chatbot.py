import chromadb
import click
import logging
import os
import warnings
import random

from chromadb.config import Settings
from colorama import Fore
from click_repl import register_repl
from gpt4all import GPT4All
from pathlib import Path
from pydantic.error_wrappers import ValidationError
from typing import Union

from constants import (
    DEFAULT_CHATBOT_CONFIG, 
    CHROMA_DEFAULT_COLLECTION_NAME,
    PERSIST_DB_FOLDER
)
from src.cli.cli import CLI
from src.ingest_data.ingest import Ingest
from src.models.model_picker import get_model
from src.utils.config import Config
from src.utils.custom_memory import ConversationMemory


def load_config(config_file: Union[Path, str]):
    config = Config.from_file(config_file).cfg.config
    model_name = config.model_name
    model_config_file = config.model_config_file
    model_vector_db = config.model_vector_db
    chat_type = config.chat_option
    return model_name, model_config_file, model_vector_db, chat_type


SEED_RANDOM_LIMIT = 10**10


@click.group()
def main():
    pass


@main.command()
@click.option('--config_file', '-cf', default=DEFAULT_CHATBOT_CONFIG, help='A premade config file for the chatbot.')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Check if the chatbot should be verbose or not.')
@click.option('--silence-logger', is_flag=True, default=False, help='Whether to silence the default logger or not.')
@click.option('--silence-level', '-sl', type=click.Choice(['debug','info','warning','critical','error'], case_sensitive=True), default='warning', help='The minimum level of logging that is being silenced. Requires --silence-logger to work.')
@click.option('--seed', '-s', default='-1', help='Select a seed for the chatbot. -1 for random seed.')
def start(config_file: Union[Path, str], verbose, silence_logger, silence_level, seed: str):
    logger_level_mapping = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'critical': logging.CRITICAL,
        'error': logging.ERROR
    }

    # param setups
    v = True if verbose else False
    logger_silenced = True if silence_logger else False
    logger_level = logger_level_mapping[silence_level]
    try:
        seed = int(seed)
        seed = seed if seed >= -1 else -1
    except ValueError:
        warnings.warn("Illegal value for seed detected. Defaulting seed value to -1.")
        seed = -1

    if seed == -1:
        seed = random.randint(0, SEED_RANDOM_LIMIT)
    if logger_silenced:
        logging.disable(logger_level)

    model_name, model_config_file, model_vector_db, chat_type = load_config(config_file)
    load_model = lambda: get_model(model_name).from_cfg(model_config_file)
    
    try:
        model = load_model()
    except ValidationError:
        if model_name == 'gpt4all':
            print("Pretrained model has not been downloaded. Attempting to download the pretrained model.")
            os.system('python3 chatbot.py load-model')
        model = load_model()
    if model.__dict__.__contains__('seed'):
        model.__setattr__('seed', seed)
        print(f"Running the chatbot with seed {seed}.")
    else:
        print("Specified model does not support seeds.")
    if chat_type == "cli":
        CLI(verbose=v).run(model=model, vector_db=model_vector_db, memory = ConversationMemory(memory_key='chat_history'))


@main.command()
@click.option('--config-file', '-cf', default=DEFAULT_CHATBOT_CONFIG, help='A premade config file for the chatbot.')
def load_model(config_file: Union[Path, str]):
    model_name, model_config_file, _, _ = load_config(config_file)
    if model_name == 'gpt4all':
        model_config = Config.from_file(model_config_file)
        pretrained_model = model_config.cfg.model.model
        GPT4All(pretrained_model)


@main.command()
@click.option('--file', '-f', default=None, help='Ingests a file, a path to file, an entire folder, or an url. Currently only supports ReadTheDocs urls.')
def ingest(file: Union[str, Path]):
    if not file:
        click.echo("A file must be included to ingest.")
    else:
        click.echo(f"Ingesting data from {file}")
        ingest = Ingest()
        ingest(file)


@main.command()
@click.option('--chroma-db-impl', '-impl', default='duckdb+parquet', type=click.Choice(['duckdb+parquet', 'duckdb', 'clickhouse'], case_sensitive=True), help='The implementation used for the Chroma database.')
@click.option('--persist-dir', '-p', default=PERSIST_DB_FOLDER, help="The persist directory for the Chroma database.")
@click.option('--anonymized-telemetry', '-a', is_flag=True, default=False, help='Whether to capture anonymous data usage or not.')
@click.option('--collection-name', '-c', default=CHROMA_DEFAULT_COLLECTION_NAME, help = "The name of the collection that will be cleared.")
def clear_history(chroma_db_impl, persist_dir, anonymized_telemetry, collection_name):
    print(f'Checking the vector database collection {collection_name} at {persist_dir}.')
    chroma_db_settings = Settings(
        chroma_db_impl=chroma_db_impl,
        persist_directory=persist_dir,
        anonymized_telemetry=anonymized_telemetry
    )

    client = chromadb.Client(chroma_db_settings)
    print(f"Connected to client at {persist_dir}.")
    print(f"Looking into collection {collection_name}")

    # before deleting, we have to make sure that the collection exists first.
    try:
        collection = client.get_collection(collection_name)
        print(f"Collection {collection_name} found.")
    except ValueError:
        print(f"Collection {collection_name} does not exist. Process cancelled.")
        exit()

    will_delete = _confirm_deletion()
    if will_delete:
        client.delete_collection(collection_name)
        print(f"Collection {collection_name} has been deleted.")
    else:
        print("Process cancelled.")


def _confirm_deletion():
    user_input_mappings = {
        'y': True,
        'yes': True,
        'no': False,
        'n': False
    }
    print(f"{Fore.RED}WARNING:{Fore.RESET} This will delete your {Fore.RED}ENTIRE MEMORY COLLECTION{Fore.RESET}.")
    print(f"This action is {Fore.RED}IRREVERSIBLE{Fore.RESET}!")
    user_input = input("Are you sure you want to continue? (Y/N/Yes/No): ")

    lower_user_input = user_input.lower()
    if lower_user_input in user_input_mappings:
        return user_input_mappings[lower_user_input]
    else:
        while lower_user_input not in user_input_mappings:
            new_user_input = input("Invalid input. Please try again (Y/N/Yes/No): ")
            lower_user_input = new_user_input.lower()

        return user_input_mappings[lower_user_input]


if __name__ == "__main__":
    register_repl(main)
    main()
