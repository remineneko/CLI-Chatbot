import logging
import openai
from .exceptions import InvalidAPIKey
from .models import supported_models
from .response import ChatResponse
from typing import List, Dict, Union


class ChatHandler:
    def __init__(self, api_key: str, logger: logging.Logger):
        self._logger = logger
        try:
            openai.api_key = api_key
            openai.Model.list()
        except openai.OpenAIError:
            self._logger.critical("Invalid OpenAI API Key provided.")
            raise InvalidAPIKey("The API Key provided is invalid. Please double check your key.")
        
    def respond(self, query: Union[str, List[Dict[str, str]]], model: str, temperature=None, max_tokens=None):
        if model in supported_models:
            return ChatResponse(openai.ChatCompletion.create(
                model=model,
                messages=query
            ))
        else:
            return ChatResponse(openai.Completion.create(
                model=model,
                prompt=query,
                temperature=temperature,
                max_tokens=max_tokens
            ))
