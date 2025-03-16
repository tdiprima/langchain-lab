"""
Agents: Agent with a Tool
Creates an agent with a fake search tool.
"""
from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI


# Step 1: Make a fake tool (pretend it searches the web)
def fake_search(query):
    return f"I found: {query} is awesome!"


tools = [Tool(name="Search", func=fake_search, description="Searches stuff")]

# Step 2: Create an agent
llm = ChatOpenAI(model="gpt-3.5-turbo")
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description")

# Step 3: Ask it something
response = agent.invoke({"input": "Tell me about cats!"})
print(response['output'])  # Cats are both interesting and awesome animals!
