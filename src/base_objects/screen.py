from .components import Component

from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Any, Optional


class Source(Component):
    def __init__(self, source):
        self.source = source


class OutputSource(Source, ABC):
    def __init__(self, source):
        super().__init__(source)

    @abstractmethod
    def show(self, data: Any):
        pass


class VoiceOutput(Source, ABC):
    def __init__(self, source):
        super().__init_(source)

    @abstractmethod
    def speak(self, data_stream: Any):
        pass


class VoiceInput(Source, ABC):
    def __init__(self, source):
        super().__init_(source)

    @abstractmethod
    def listen(self, input_stream: Any):
        pass

@dataclass
class Screen(ABC):
    """
    A screen that hosts the program.
    The screen can be an application or a CLI program.
    The main logic for any screen should subclass this class.
    """

    output_source: OutputSource
    ''' The source point for the generated output to be shown '''

    voice_input: Optional[VoiceInput] = None
    ''' Where the voice will be recorded, if applicable '''

    voice_output: Optional[VoiceOutput] = None
    ''' Where the bot's voice can emit '''

    @abstractmethod
    def run(self):
        '''
        Starts the chatting program under the given Screen.
        '''
        pass