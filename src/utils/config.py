import os.path as osp
import shutil
import sys
import tempfile
from importlib import import_module
from easydict import EasyDict
from pathlib import Path
from typing import Union, Dict


class Config:
    def __init__(self, cfg_dict: Dict=None, cfg_text: str=None, filename: Union[str, Path]=None):
        self._cfg_dict = EasyDict(cfg_dict)
        self._filename = filename
        if cfg_text:
            text = cfg_text
        elif filename:
            with open(filename, 'r') as f:
                text = f.read()
        else:
            text = ''
        self._text = text

    @classmethod
    def from_file(cls, filename: Union[str, Path]):
        filename = str(filename)
        if filename.endswith('.py'):
            with tempfile.TemporaryDirectory() as temp_config_dir:
                shutil.copyfile(filename,
                                osp.join(temp_config_dir, '_tempconfig.py'))
                sys.path.insert(0, temp_config_dir)
                mod = import_module('_tempconfig')
                sys.path.pop(0)
                cfg_dict = {name: value for name, value in mod.__dict__.items() if not name.startswith('__')}
                # delete imported module
                del sys.modules['_tempconfig']
        else:
            raise IOError('Only .py type are supported now!')
        cfg_text = filename + '\n'
        with open(filename, 'r') as f:
            cfg_text += f.read()

        return cls(cfg_dict=cfg_dict, cfg_text=cfg_text, filename=filename)


    @property
    def filename(self):
        return self._filename

    @property
    def text(self):
        return self._text
    
    @property
    def cfg(self):
        return self._cfg_dict

    def __repr__(self):
        return 'Config (path: {}): {}'.format(self.filename,
                                              self._cfg_dict.__repr__())

    def __getattr__(self, name):
        return getattr(self._cfg_dict, name)