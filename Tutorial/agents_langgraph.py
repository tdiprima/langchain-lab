"""
Same thing, but using LangGraph
Author: tdiprima
"""
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langgraph.prebuilt import create_react_agent

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

tools = load_tools(["llm-math"], llm=llm)

agent = create_react_agent(llm, tools)

query = "What is 2 raised to the 5th power, divided by 7?"
result = agent.invoke({"messages": [{"role": "human", "content": query}]})
print(f"Final Answer: {result['messages'][-1].content}")

"""
1. `result['messages']` gets the list of messages
2. `[-1]` gets the last message (an AIMessage object)
3. `.content` accesses the content attribute of the AIMessage object
"""
