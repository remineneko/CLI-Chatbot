from typing import List
from .response import ChatResponse


class SessionHandler:
    def __init__(self, history = None):
        self._past_reponses: List[ChatResponse] = history.past_responses if history else None
        self._sesh_responses: List[ChatResponse] = []

    def save_response(self, response: ChatResponse):
        self._sesh_responses.append(response)

    def save_session(self):
        pass