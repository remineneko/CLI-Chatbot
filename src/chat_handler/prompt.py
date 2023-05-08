from dataclasses import dataclass
from typing import List, Union, Dict

@dataclass
class CompletionPrompt:
    model: str              
    prompt: str
    max_tokens: int
    temperature: float
    top_p: float
    n: int
    stream: bool
    logprobs: int
    echo: bool
    stop: Union[List, str]
    presence_penalty: float
    frequency_penalty: float
    best_of: int
    logit_bias: Dict
    user: str

    @classmethod
    def from_dict(cls, prompt_dict: Dict):
        return cls(**prompt_dict)
    
    @property
    def user_prompt(self):
        return self.prompt


@dataclass
class ChatCompletionPrompt:
    model: str              
    messages: List[Dict[str, str]]
    max_tokens: int
    temperature: float
    top_p: float
    n: int
    stream: bool
    logprobs: int
    echo: bool
    stop: Union[List, str]
    presence_penalty: float
    frequency_penalty: float
    best_of: int
    logit_bias: Dict
    user: str

    @classmethod
    def from_dict(cls, prompt_dict: Dict):
        return cls(**prompt_dict)
    
    @property
    def user_prompt(self):
        return self.messages[0]['content']