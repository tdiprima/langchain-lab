"""
LLM Math Agent
Author: tdiprima
"""

from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import OpenAI

llm = OpenAI(temperature=0)
print("Model:", llm.model_name)

tools = load_tools(["llm-math"], llm=llm)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

query = "What is 2 raised to the 5th power, divided by 7?"
result = agent.invoke({"input": query})
print(f"Final Answer: {result['output']}")  # Final Answer: 4.571428571428571
