import os
import warnings
import sys

from langchain.document_loaders import (
    CSVLoader,
    PDFMinerLoader,
    TextLoader,
    UnstructuredEPubLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader,
    PythonLoader,
    ReadTheDocsLoader
)

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

from chromadb.config import Settings

from typing import Union, List
from pathlib import Path

from src.ingest_data.ingest_source_detector import IngestSource, IngestSourceDetector, IngestURLIdentifier
from src.constants import PERSIST_DB_FOLDER


class Ingest:
    _INGEST_DICT = {
        IngestSource.FILE: 'IngestFile',
        IngestSource.DIRECTORY: 'IngestFile',
        IngestSource.URL: 'IngestURL'
    }
    def __init__(self, source: Union[Path, str]):
        self._source = source
        self._type = IngestSourceDetector(self._source).source

    def ingest(self):
        data: List[Document] = getattr(sys.modules[__name__], self._INGEST_DICT[self._type])(self._source).extract_data()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splitted_data = text_splitter.split_documents(data)

        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

        db = Chroma.from_documents(
            splitted_data, 
            embeddings, 
            persist_directory=PERSIST_DB_FOLDER, 
            client_settings={
                Settings(
                    chroma_db_impl='duckdb+parquet',
                    persist_directory=PERSIST_DB_FOLDER,
                    anonymized_telemetry=False
                )
            }
        )

        db.persist()
        db = None
        

class IngestFile(Ingest):
    _FILE_EXT_MAPPING = {
        ".csv": (CSVLoader, {}),
        ".docx": (UnstructuredWordDocumentLoader, {}),
        ".epub": (UnstructuredEPubLoader, {}),
        ".md": (UnstructuredMarkdownLoader, {}),
        ".pdf": (PDFMinerLoader, {}),
        ".txt": (TextLoader, {"encoding": "utf8"}),
        ".py": (PythonLoader, {})
    }

    def __init__(self, source: Union[Path, str]):
        super().__init__(source)

    def extract_data(self):
        if self._type == IngestSource.FILE:
            return [self._single_file_load(self._source)]
        else:
            return [i for i in self._folder_load(self._source)]
        
    def _single_file_load(self, file):
        file_name, file_ext = os.path.splitext(file)
        if file_ext not in self._FILE_EXT_MAPPING:
            warnings.warn(f"File {file} cannot be loaded - unsupported extension.")
        else:
            loader, args = self._FILE_EXT_MAPPING[file_ext]
            return loader(file, **args).load()[0]
    
    def _folder_load(self, folder):
        for file in os.listdir(folder):
            yield self._single_file_load(os.path.join(folder, file))


