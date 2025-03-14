from langchain_openai import ChatOpenAI  # Use ChatOpenAI instead of OpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langgraph.prebuilt import create_react_agent

# Initialize the LLM (chat model) for the agent
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")  # Specify a chat model

# Load the tools the agent can use
tools = load_tools(["llm-math"], llm=llm)

# Create a ReAct agent with LangGraph
agent = create_react_agent(llm, tools)

# Ask a math question
query = "What is 2 raised to the 5th power, divided by 7?"
result = agent.invoke({"messages": [{"role": "human", "content": query}]})
print(f"Final Answer: {result['messages'][-1].content}")

"""
1. `result['messages']` gets the list of messages
2. `[-1]` gets the last message (an AIMessage object)
3. `.content` accesses the content attribute of the AIMessage object
"""

"""
> Entering new AgentExecutor chain...
 I should use a calculator to solve this problem.
Action: Calculator
Action Input: 2 ** 5 / 7
Observation: Answer: 4.571428571428571
Thought: I now know the final answer.
Final Answer: 4.571428571428571

> Finished chain.
Final Answer: 4.571428571428571
"""
