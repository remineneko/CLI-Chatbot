import langchain.llms
import importlib
import inspect

from copy import deepcopy

from src.exceptions import UnsupportedModel
from .model_mixins import ModelMixin


def get_models_from_langchain():
    model_dict = {}

    for i in inspect.getmembers(langchain.llms, inspect.ismodule):
        module_name = i[0]
        class_name_lowercase = module_name.replace("_","")
        if module_name == 'base' or module_name == 'utils': # unnecessary files to consider
            continue
        module = importlib.import_module(f'langchain.llms.{module_name}')
        class_name = [i[0] for i in inspect.getmembers(module, inspect.isclass)]

        # avoid any accidents
        dup_class_name = deepcopy(class_name)
        lc_class_name = list(map(lambda x: x.lower(), dup_class_name))
        
        if class_name_lowercase in lc_class_name:
            actual_class_name = class_name[lc_class_name.index(class_name_lowercase)]
        else:
            actual_class_name = None
        
        if actual_class_name:
            model_dict[module_name] = getattr(module, actual_class_name)
        
    return model_dict

MODELS = get_models_from_langchain()


def get_model(name):
    obtained_model = MODELS.get(name, None)
    if obtained_model:
        return type(f'{obtained_model.__name__}Model', (obtained_model, ModelMixin), {})
    else:
        raise UnsupportedModel("Given model is not supported by LangChain for the time being.")
