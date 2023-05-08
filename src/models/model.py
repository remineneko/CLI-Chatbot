from dataclasses import dataclass
from typing import Union
from pathlib import Path


@dataclass
class Model:
    model_name: str

    @classmethod
    def from_file(cls, fp: Union[Path, str]):
        pass