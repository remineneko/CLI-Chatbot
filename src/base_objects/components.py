from abc import abstractmethod, ABC


class Component(ABC):

    @abstractmethod
    def load(self):
        pass