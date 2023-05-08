from dataclasses import dataclass
from easydict import EasyDict as edict
from typing import Union
from pathlib import Path
import os

'''
Vision: load the model from different types of files and inputs.
'''

@dataclass
class BaseLoader:
    fp: Union[Path, str]

    def load(self):
        pass


class PyLoader(BaseLoader):
    def load(self):
        pass