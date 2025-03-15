from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import OpenAI

# Initialize the LLM for the agent (we'll use the same OpenAI GPT-3 model)
llm = OpenAI(temperature=0)
print("Model:", llm.model_name)

# Load the tools the agent can use. We'll give it a calculator tool (LLM math).
tools = load_tools(["llm-math"], llm=llm)
# "llm-math" is a built-in tool that uses the LLM plus python for math.

# Initialize the agent with the tools and LLM.
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Ask a math question
query = "What is 2 raised to the 5th power, divided by 7?"
result = agent.invoke({"input": query})
print(f"Final Answer: {result['output']}")
