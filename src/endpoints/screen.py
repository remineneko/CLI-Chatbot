from abc import abstractmethod, ABC
from pydantic import BaseModel
from typing import Any, Optional


class Source(BaseModel):
    source: Any


class OutputSource(Source, ABC):
    def __init__(self, source, **kwargs):
        super(OutputSource).__init__(source)
        self.__dict__.update(kwargs)

    @abstractmethod
    def show(self, data: Any):
        pass


class VoiceOutput(Source, ABC):
    def __init__(self, source, **kwargs):
        super(VoiceOutput).__init__(source)
        self.__dict__.update(kwargs)

    @abstractmethod
    def speak(self, data_stream: Any):
        pass


class VoiceInput(Source, ABC):
    def __init__(self, source, **kwargs):
        super(VoiceInput).__init_(source)
        self.__dict__.update(kwargs)

    @abstractmethod
    def listen(self, input_stream: Any):
        pass


class Screen(BaseModel, ABC):
    output_source: OutputSource
    ''' The source point for the generated output to be shown '''

    voice_input: Optional[VoiceInput]
    ''' Where the voice will be recorded, if applicable '''

    voice_output: Optional[VoiceOutput]
    ''' Where the bot's voice can emit '''

    @abstractmethod
    def run(self):
        pass