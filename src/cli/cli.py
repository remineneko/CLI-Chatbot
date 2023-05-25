import sys

from langchain.utilities import GoogleSearchAPIWrapper
from langchain.vectorstores import VectorStore
from langchain.llms.base import LLM
from langchain.agents import Tool, LLMSingleActionAgent, AgentExecutor, initialize_agent, AgentType
from langchain import LLMChain

from constants import (
    DEFAULT_CHATBOT_PROMPT,
    CHATBOT_NAME
)

from src.base_objects import Screen, OutputSource
from src.utils.custom_memory import ConversationMemory
from src.utils.custom_output import CustomOutputParser
from src.utils.custom_prompt_template import CustomPromptTemplate


class StandardOutput(OutputSource):
    def __init__(self, source=sys.stdout):
        super().__init__(source)
    
    def show(self, data):
        self.source.write(data)


class CLI(Screen):
    def __init__(self, output_source=StandardOutput, voice_output=None, voice_input=None):
        super().__init__(output_source, voice_input, voice_output)

    @staticmethod
    def _cli(model: LLM, vector_db: VectorStore, memory: ConversationMemory):
        retrieval_tool = Tool(
            name='Core Memory',
            description=f"Contains completed conversations between the user and {CHATBOT_NAME} in the past and information from various documents.",
            func=vector_db.similarity_search
        )

        search = GoogleSearchAPIWrapper()
        search_tool = Tool(
                name = "Google Search",
                description="Search Google for recent results.",
                func=search.run
            )

        tools = [retrieval_tool, search_tool]
    
        chatbot_prompt = CustomPromptTemplate(
            input_variables=['input', 'chat_history', 'intermediate_steps'], 
            template = DEFAULT_CHATBOT_PROMPT,
            tools=tools
        )

        cqa = LLMChain(llm=model, prompt=chatbot_prompt, verbose=False)

        output_parser = CustomOutputParser()
        tools_names = [tool.name for tool in tools]
        agent = LLMSingleActionAgent(
            llm_chain=cqa,
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=tools_names
        )

        chat_agent = AgentExecutor.from_agent_and_tools(
            agent=agent, 
            tools=tools, 
            verbose=False,
            memory=memory,
        )

        cont_chatting = True
        while cont_chatting:
            query = input("\nUser: ")
            if query == "exit":
                cont_chatting = False
                memory.save_to_db(v_db=vector_db, ai_prefix=CHATBOT_NAME)
            
            # Get the answer from the chain
            res = chat_agent.run(query)    

            print(f"{CHATBOT_NAME}:{res}")

    def run(self, **kwargs):
        model_ = kwargs.get('model')
        vector_db = kwargs.get('vector_db')
        memory = kwargs.get('memory')
        self._cli(model_, vector_db, memory)