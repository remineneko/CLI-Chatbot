from pathlib import Path
from typing import Union, List
from src.chat_handler.prompt import ChatCompletionPrompt, CompletionPrompt
from src.chat_handler.response import ChatResponse
from pygpt4all import GPT4All, GPT4All_J
from src.history import ChatHistory

def parse_history(history_file: Union[Path, str], model: Union[GPT4All_J, GPT4All]):
    """
    Parse the past history for the model to continue the conversation.

    Args:
        history_file (Union[Path, str]): The file containing the chat history.

    Returns:
        str: The parsed history that is convenient for the chatbot to work with.
    """

    history = ChatHistory(history_file)
    past_interactions: List[ChatCompletionPrompt, CompletionPrompt, ChatResponse] = history.history
    user_prefix = "Me: "
    bot_prefix = "B: "

    for interaction in past_interactions:
        if type(interaction) in [ChatCompletionPrompt, CompletionPrompt]:
            convo += user_prefix + interaction.user_prompt + "\n"
        elif type(interaction) == ChatResponse:
            convo += bot_prefix + interaction.answer + "\n"

    generation = [s for s in model.generate(starter_prompt + convo)]
    
    history.summary = generation

    history.save(history_file) 

    return generation