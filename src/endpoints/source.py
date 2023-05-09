from abc import abstractmethod, ABC


class Source(ABC):
    def __init__(self, input_stream, **kwargs):
        self.input_stream = input_stream
        self.__dict__.update(kwargs)

    @property
    @abstractmethod
    def prompt(self):
        """
        The prompt to put into the chatbot. 
        """
        pass