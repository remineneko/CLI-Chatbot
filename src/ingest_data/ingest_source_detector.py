import re
import os

from typing import Union
from pathlib import Path
from enum import Enum
from urllib.parse import urlparse

from src.exceptions import UnsupportedIngestSource



class IngestSource(Enum):
    FILE = 0
    DIRECTORY = 1
    URL = 2


class IngestSourceDetector:
    def __init__(self, source: Union[Path, str]):
        self._source = source

    @property
    def source(self):
        return self._classifying_source()

    def _classifying_source(self):
        if os.path.isfile(self._source):
            return IngestSource.FILE
        elif os.path.isdir(self._source):
            return IngestSource.DIRECTORY
        elif self._is_url(self._source):
            return IngestSource.URL
        else:
            raise UnsupportedIngestSource("The provided source is either unsupported or has incorrect format.")

    @staticmethod
    def _is_url(url):
        try:
            url_result = urlparse(url)
            return all([url_result.scheme, url_result.netloc])
        except ValueError:
            return False
        

class IngestURLIdentifier:
    # note: This is terrible design. Will fix when more links are needed to be supported.

    SUPPORTED_SITES = [
        'readthedocs',
        'youtube'
    ]

    YOUTUBE_REGEX = r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'

    def __init__(self, url: str):
        self._url = url

    def _get_url_type(self):
        if self._is_valid_youtube_link():
            return 'youtube'
        elif self._is_valid_readthedocs_link():
            return 'readthedocs'

    def _is_valid_youtube_link(self):
        return bool(re.search(self._YOUTUBE_REGEX, self._url))

    def _is_valid_readthedocs_link(self):
        # this is by no means the way to do this, but really, I can't be bothered to craft a regex right now.
        if 'readthedocs' in self._url:
            return True
        return False
    