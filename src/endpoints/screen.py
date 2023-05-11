from abc import abstractmethod, ABC
from pydantic import BaseModel
from typing import Any, Optional


class Source:
    def __init__(self, source, **kwargs):
        self.source = source
        self.__dict__.update(kwargs)


class OutputSource(Source, ABC):
    def __init__(self, source, **kwargs):
        super().__init__(source, **kwargs)

    @abstractmethod
    def show(self, data: Any):
        pass


class VoiceOutput(Source, ABC):
    def __init__(self, source, **kwargs):
        super().__init_(source, **kwargs)

    @abstractmethod
    def speak(self, data_stream: Any):
        pass


class VoiceInput(Source, ABC):
    def __init__(self, source, **kwargs):
        super().__init_(source, **kwargs)

    @abstractmethod
    def listen(self, input_stream: Any):
        pass


class Screen(BaseModel, ABC):
    """
    A screen that hosts the program.
    The screen can be an application or a CLI program.
    The main logic for any screen should subclass this class.
    """
    
    output_source: OutputSource
    ''' The source point for the generated output to be shown '''

    voice_input: Optional[VoiceInput]
    ''' Where the voice will be recorded, if applicable '''

    voice_output: Optional[VoiceOutput]
    ''' Where the bot's voice can emit '''

    @abstractmethod
    def run(self):
        '''
        Starts the chatting program under the given Screen.
        '''
        pass