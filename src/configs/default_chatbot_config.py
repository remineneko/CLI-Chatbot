from constants import (
    DEFAULT_GPT4ALL_CONFIG,
    PERSIST_DB_FOLDER,
    HUGGING_FACE_DEFAULT_MODEL, 
    CHROMA_DEFAULT_COLLECTION_NAME, 
    CHROMA_DEFAULT_SETTINGS,
    DEFAULT_CHATBOT_PROMPT,
    CHATBOT_NAME
)
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings


config = dict(
    chat_option = 'cli',
    model_name = 'gpt4all',
    model_config_file = DEFAULT_GPT4ALL_CONFIG,
    model_vector_db = Chroma(
        persist_directory=PERSIST_DB_FOLDER, 
        embedding_function=HuggingFaceEmbeddings(
            model_name=HUGGING_FACE_DEFAULT_MODEL
            ), 
        client_settings=CHROMA_DEFAULT_SETTINGS, 
        collection_name=CHROMA_DEFAULT_COLLECTION_NAME
    )
)