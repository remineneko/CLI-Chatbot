class ModelCreator:
    """
    A class to create new classes for models dynamically. 
    Code adapted from https://stackoverflow.com/questions/21060073/dynamic-inheritance-in-python
    """
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        return self.memo.setdefault(args, self.f(*args))
    

@ModelCreator
def create_model(model_name, *base):
    new_model = type(model_name, tuple(base), {})

    
