from src.base_objects import ChatOutput, InputStream, LLMModel
from src.constants import CHATBOT_API_TOKEN
from src.logger import ChatbotLogger
from src.exceptions import InvalidAPIKey, InvalidPrompt

import openai
from typing import Union, List, Dict, Any, Optional


class OpenAIChatOutput(ChatOutput):
    @property
    def answer(self):
        choices = self.output['choices'][0]
        if 'message' in choices:
            return choices['message']['content']
        else:
            return choices['text']
        
    @property
    def token_usage(self) -> int:
        """ Gets the total token usage of the last prompt + answer combination.
        """
        return self.output['usage']['total_tokens']
        


class OpenAI(LLMModel):
    CHAT_COMPLETION_MODELS = [
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301",
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-32k",
        "gpt-4-32k-0314"
    ]   
    def __init__(
        self, 
        api_key: str = CHATBOT_API_TOKEN,
        api_base: str = None,
        organization: str = None,
        model_name: str = 'text-davinci-003', 
        temperature: float = 0.7,
        max_tokens: int = 256,
        top_p: float = 1,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
        n: int = 1,
        best_of: int = 1,
        log_probs: int = None,
        max_retries: int = 6,
        streaming: bool = False,
        stop: Union[str, List[str]] = None,
        logit_bias: Optional[Dict[str, float]] = None,
        logger = ChatbotLogger()
    ):
        super().__init__(model=model_name)
        self.logger = logger
        try:
            openai.api_key = api_key
            openai.api_base = api_base if api_base else "https://api.openai.com/v1"
            openai.organization = organization if organization else None
            openai.Model.list()
        except openai.OpenAIError:
            self._logger.critical("Invalid OpenAI API Key provided.")
            raise InvalidAPIKey("The API Key provided is invalid. Please double check your key.")
        
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.n = n
        self.best_of = best_of
        self.max_retries = max_retries
        self.streaming = streaming
        self.stop = stop
        self.logit_bias = logit_bias
        self.logprobs = log_probs

    def generate(
            self, 
            prompt: Union[str, InputStream, List[str], List[Dict[str, str]]], 
            suffix:str = None, 
            echo: bool = False, 
            stop: Union[str, List[str]] = None
        ) -> ChatOutput:
        if not prompt:
            raise InvalidPrompt("The given prompt is invalid")
        if isinstance(prompt, InputStream):
            prompt = prompt.prompt
        num_prompts = 1 if isinstance(prompt, str) else len(prompt)
        self.logger.info(f"Number of prompts given: {num_prompts}")

        for i in len(num_prompts):
            if isinstance(prompt, str):
                self.logger.info(f"Prompt {i+1}: {prompt}")
            else:
                self.logger.info(f"Prompt {i+1}: {prompt[0]}")

        if self.model in self.CHAT_COMPLETION_MODELS:
            if isinstance(prompt, str):
                prompt = [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            elif isinstance(prompt, list) and isinstance(prompt[0], str):
                prompt = [
                    {
                        'role': 'user',
                        'content': i
                    }
                    for i in prompt
                ]
            generated = OpenAIChatOutput(openai.ChatCompletion(
                model = self.model,
                prompt = prompt,
                suffix = suffix,
                max_tokens = self.max_tokens,
                temperature = self.temperature,
                top_p = self.top_p,
                n = self.n,
                stream = self.streaming,
                logprobs = self.logprobs,
                echo = echo,
                stop = stop,
                presence_penalty = self.presence_penalty,
                frequency_penalty = self.frequency_penalty,
                best_of = self.best_of,
                logit_bias=self.logit_bias,
            ))
        else:
            generated = OpenAIChatOutput(openai.Completion(
                model = self.model,
                prompt = prompt,
                suffix = suffix,
                max_tokens = self.max_tokens,
                temperature = self.temperature,
                top_p = self.top_p,
                n = self.n,
                stream = self.streaming,
                logprobs = self.logprobs,
                echo = echo,
                stop = stop,
                presence_penalty = self.presence_penalty,
                frequency_penalty = self.frequency_penalty,
                best_of = self.best_of,
                logit_bias=self.logit_bias,
            ))
        
        token_usage = generated.token_usage
        
        self.logger.info(f"Generated content: {generated.answer}")
        self.logger.info(f"Used {token_usage} for the given prompt and generated content.")

        return generated
        
    