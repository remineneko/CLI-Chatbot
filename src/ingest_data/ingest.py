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

from typing import Union, List
from pathlib import Path

from src.ingest_data.ingest_source_detector import IngestSource, IngestSourceDetector, IngestURLIdentifier, IngestURLType
from constants import PERSIST_DB_FOLDER, CHROMA_DEFAULT_SETTINGS, HUGGING_FACE_DEFAULT_MODEL, CHROMA_DEFAULT_COLLECTION_NAME


class BaseIngest:
    def __init__(self, source: Union[Path, str], source_type = None):
        self._source = source
        self._type = IngestSourceDetector(self._source).source if not source_type else source_type


class Ingest:
    _INGEST_DICT = {
        IngestSource.FILE: 'IngestFile',
        IngestSource.DIRECTORY: 'IngestFile',
        IngestSource.URL: 'IngestURL'
    }

    def __call__(self, source: Union[Path, str]):
        source_type = IngestSourceDetector(source).source
        data: List[Document] = getattr(sys.modules[__name__], self._INGEST_DICT[source_type])(source).extract_data()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splitted_data = text_splitter.split_documents(data)

        embeddings = HuggingFaceEmbeddings(model_name=HUGGING_FACE_DEFAULT_MODEL)

        db = Chroma.from_documents(
            splitted_data, 
            embeddings, 
            persist_directory=PERSIST_DB_FOLDER, 
            client_settings=CHROMA_DEFAULT_SETTINGS,
            collection_name=CHROMA_DEFAULT_COLLECTION_NAME
        )

        db.persist()
        db = None

        print(f"Completed ingesting data from {source}")
        

class IngestFile(BaseIngest):
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


class IngestURL(BaseIngest):
    # For now, only readthedocs is supported because im trying to figure out what exactly i want to do for YouTube.
    _LINK_MAPPING = {
        IngestURLType.READTHEDOCS: (ReadTheDocsLoader, {})
    }

    def __init__(self, source: Union[Path, str]):
        super().__init__(source)

    def extract_data(self):
        func, args = self._LINK_MAPPING[self._type]
        return func(self._source, **args)
    