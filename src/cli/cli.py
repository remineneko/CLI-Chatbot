import sys

from langchain.utilities import GoogleSearchAPIWrapper
from langchain.vectorstores import VectorStore
from langchain.llms.base import LLM
from langchain.agents import Tool, LLMSingleActionAgent, AgentExecutor, initialize_agent, AgentType
from langchain import LLMChain

from constants import (
    DEFAULT_CHATBOT_PROMPT,
    CHATBOT_NAME,
    DEFAULT_USER_NAME
)

from src.base_objects import Screen, OutputSource
from src.utils.custom_memory import ConversationMemory, save_message
from src.utils.custom_output import CustomOutputParser
from src.utils.custom_prompt_template import CustomPromptTemplate


class StandardOutput(OutputSource):
    def __init__(self, source=sys.stdout):
        super().__init__(source)
    
    def show(self, data):
        self.source.write(data)


class CLI(Screen):
    def __init__(self, output_source=StandardOutput, voice_output=None, voice_input=None, verbose=False):
        super().__init__(output_source, voice_input, voice_output)
        self._verbose = verbose

    def _cli(self, model: LLM, vector_db: VectorStore, memory: ConversationMemory):
        retrieval_tool = Tool(
            name='Memory',
            description=f"Contains past conversations between the user and {CHATBOT_NAME} and information from various documents that {CHATBOT_NAME} has read.",
            func=vector_db.similarity_search
        )

        search = GoogleSearchAPIWrapper()
        search_tool = Tool(
                name = "Internet",
                description=f"Tool to look up answers that {CHATBOT_NAME} does not know.",
                func=search.run
            )

        tools = [retrieval_tool, search_tool]
    
        chatbot_prompt = CustomPromptTemplate(
            input_variables=['input', 'chat_history', 'intermediate_steps'], 
            template = DEFAULT_CHATBOT_PROMPT,
            tools=tools
        )

        llm_chain = LLMChain(llm=model, prompt=chatbot_prompt, verbose=self._verbose)

        output_parser = CustomOutputParser()
        tools_names = [tool.name for tool in tools]
        agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=output_parser,
            stop=["\nObservation"],     #  kind of required if I want the chatbot to output something at all.
            allowed_tools=tools_names,
            verbose=self._verbose
        )

        chat_agent = AgentExecutor.from_agent_and_tools(
            agent=agent, 
            tools=tools, 
            verbose=self._verbose,
            memory=memory
        )

        while True:
            query = input("\nUser: ")
            if query == "exit" or not query:
                break

            save_message(query, DEFAULT_USER_NAME, vector_db)
            # Get the answer from the chain
            res = chat_agent.run(query)    
            if res:
                save_message(res, CHATBOT_NAME, vector_db)

            print(f"{CHATBOT_NAME}: {res}")

    def run(self, **kwargs):
        model_ = kwargs.get('model')
        vector_db = kwargs.get('vector_db')
        memory = kwargs.get('memory')
        self._cli(model_, vector_db, memory)