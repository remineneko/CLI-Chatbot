import openai
from .exceptions import InvalidAPIKey
from .models import supported_models
from .response import ChatResponse


class ChatHandler:
    def __init__(self, api_key: str):
        try:
            openai.api_key = api_key
            openai.Model.list()
        except openai.OpenAIError:
            raise InvalidAPIKey("The API Key provided is invalid. Please double check your key.")
        
    def respond(self, query: str, model: str, temperature=None, max_tokens=None):
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
