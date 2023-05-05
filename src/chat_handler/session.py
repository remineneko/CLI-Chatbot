from typing import List, Union, Dict
from .response import ChatResponse
from .prompt import CompletionPrompt, ChatCompletionPrompt

from src.history import ChatHistory
from src.database import DBSession

import openai
import json
from secrets import token_urlsafe
import logging

class SessionHandler:
    def __init__(self, database: DBSession, logger: logging.Logger, history: ChatHistory = None):
        self._history = history
        self._past_interactions: List[Union[CompletionPrompt, ChatCompletionPrompt, ChatResponse]] = history.past_interactions if history else None
        self._sesh_responses: List[Union[CompletionPrompt, ChatCompletionPrompt, ChatResponse]] = []
        self._db_sesh = database
        self._logger = logger

    def save_response(self, response: ChatResponse):
        self._sesh_responses.append(response)

    def save_prompt(self, prompt: Union[ChatCompletionPrompt, ChatCompletionPrompt]):
        self._sesh_responses.append(prompt)
    
    def _gen_title(self, first_input: str):
        """
        Generates the title for the chat session.
        
        Args:
            first_input (str): The first input that is given by the user.

        Returns:
            _type_: _description_
        """
        system_role = {
            "role": "system", 
            "content": "You are given a text input from a user, and you will summarize the content of the input, maximum 4,5 word of length."
        }
        user_role = {
            "role": "user",
            "content": first_input
        }
        messages = [system_role, user_role]
        response = ChatResponse(openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        ))
        return response.answer

    def _gen_file_name():
        fn_length = 20
        return ''.join([c for c in token_urlsafe(fn_length) if c not in '#%&{}\\<>*?/ $!\'\":@+`|='])

    def _save_to_file(self, chat_data: List[Union[ChatResponse, ChatCompletionPrompt, CompletionPrompt]], history: ChatHistory = None, title = None):
        if history:
            self._logger.info(f"History is used, saving to history id {history.file_name_no_ext}.")
            history.past_interactions = chat_data
            history.save()
            self._logger.info("Saved to history.")
            self._db_sesh.update_history(history.file_name_no_ext)
            self._logger.info("Database has updated the history.")
        else:
            self._logger.info("No history has been used, creating new entry.")
            fn_no_ext = self._gen_file_name()
            file_name = fn_no_ext + ".json"
            with open(file_name, 'w') as f:
                saving_dict = {
                    "title": title,
                    "past_interactions": chat_data,
                    "filename": file_name
                }
                json.dump(saving_dict, f)
            self._logger.info(f"History id {fn_no_ext} has been created.")
            self._db_sesh.save_session(fn_no_ext)
            self._logger.info(f"History has been saved to the database.")

    def save_session(self, title):
        if self._history:
            self._past_interactions.extend(self._sesh_responses)
            self._save_to_file(self._past_interactions, self._history)
        else:
            self._save_to_file(self._sesh_responses, title)
        