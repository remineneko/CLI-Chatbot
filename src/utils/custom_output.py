from langchain.agents import AgentOutputParser
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish


class CustomOutputParser(AgentOutputParser):
    
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        output = llm_output.split("Final Answer:")[-1].strip() if "Final Answer" in llm_output else llm_output
        
        return AgentFinish(
            return_values={
                "output": output
            },
            log=llm_output
        )