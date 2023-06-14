from langchain.vectorstores import VectorStore, Chroma
from langchain.memory.buffer import ConversationBufferMemory
from langchain.schema import Document, HumanMessage, AIMessage, SystemMessage, ChatMessage, BaseMessage
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from typing import Any, List
from constants import (
    DEFAULT_USER_NAME, 
    CHATBOT_NAME,
    PERSIST_DB_FOLDER,
    CHROMA_DEFAULT_COLLECTION_NAME,
    CHROMA_DEFAULT_SETTINGS,
    HUGGING_FACE_DEFAULT_MODEL
)
from datetime import datetime


def buffer_string(
    messages: List[BaseMessage], human_prefix: str = "Human", ai_prefix: str = "AI"
) -> str:
    """Get buffer string of messages.
    This function bears the same signature as get_buffer_string; however, this function is meant to better support LLaMA-based models.
    """
    string_messages = []
    for m in messages:
        if isinstance(m, HumanMessage):
            role = human_prefix
        elif isinstance(m, AIMessage):
            role = ai_prefix
        elif isinstance(m, SystemMessage):
            role = "System"
        elif isinstance(m, ChatMessage):
            role = m.role
        else:
            raise ValueError(f"Got unsupported message type: {m}")
        string_messages.append(f"### {role}:\n{m.content}")
    return "\n".join(string_messages)


class ConversationMemory(ConversationBufferMemory):
    @property
    def buffer(self) -> Any:
        """String buffer of memory."""
        if self.return_messages:
            return self.chat_memory.messages
        else:
            return buffer_string(
                self.chat_memory.messages,
                human_prefix=DEFAULT_USER_NAME,
                ai_prefix=CHATBOT_NAME,
            )


def get_time():
    time = datetime.now()
    return time.strftime('%d/%m/%Y %H:%M:%S')


def message_to_document(message, prefix) -> Document:
    return Document(
        page_content=message,
        metadata={
            'source': prefix,
            'time': get_time()
        }
    )
    

def save_to_db(document: Document, v_db: Chroma):
    data = [document]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splitted_data = text_splitter.split_documents(data)

    db = v_db.from_documents(
        splitted_data,
        embedding=HuggingFaceEmbeddings(model_name=HUGGING_FACE_DEFAULT_MODEL),
        persist_directory=PERSIST_DB_FOLDER,
        client_settings=CHROMA_DEFAULT_SETTINGS,
        collection_name=CHROMA_DEFAULT_COLLECTION_NAME
    )
    db.persist()
    db = None
    # im not entirely sure for other vector dbs, so thats there for now.


def save_message(message, prefix, v_db: VectorStore):
    save_to_db(message_to_document(message, prefix), v_db)