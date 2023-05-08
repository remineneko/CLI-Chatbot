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
    past_interactions: List[ChatCompletionPrompt, CompletionPrompt, ChatResponse] = history_file.past_interactions

    # with the past interactions, I will tell a LLM model to summarize this for me.
    # not gpt-3.5-turbo though, OpenAI doesn't allow it to do that kind of job, I think.
    # so now, I would rely on a... hopefully decent model for the job.

    starter_prompt = """
    I will provide you a chain of exchanges between me and another person ("Me" for me and "B" for the other person) and/or a summary of conclusions that have been drawn from our previous conversations.
    From the summary (if given, which will be denoted by a "Summary" word) and the exchanges, please give me a new summary of conclusions that can be drawn.\n
    Limit the conclusions to 15 words.\n
    """

    convo = ''

    summary_prefix = "Summary: "
    user_prefix = "Me: "
    bot_prefix = "B: "

    if history.summary:
        convo += summary_prefix + history.summary + "\n"
    
    for interaction in past_interactions:
        if type(interaction) in [ChatCompletionPrompt, CompletionPrompt]:
            convo += user_prefix + interaction.user_prompt + "\n"
        elif type(interaction) == ChatResponse:
            convo += bot_prefix + interaction.answer + "\n"

    generation = [s for s in model.generate(starter_prompt + convo)]
    
    history.summary = generation

    history.save(history_file) 

    return generation
