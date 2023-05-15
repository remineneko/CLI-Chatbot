from abc import abstractmethod, ABC


class InputStream(ABC):
    def __init__(self, input_stream):
        self.input_stream = input_stream

    @property
    @abstractmethod
    def prompt(self):
        """
        The prompt to put into the chatbot. 
        """
        pass

    @classmethod
    def from_dict(cls, dict_: dict):
        prompt = dict_.pop("prompt")
        return cls(prompt, **dict_)

    def to_dict(self):
        pre_return = {"prompt": self.prompt}
        pre_return.update({i for i in self.__dict__ if i != "input_stream"})
        return pre_return