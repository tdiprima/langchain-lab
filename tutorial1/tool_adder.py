"""
Tools: Tool with LangChain
Uses a custom tool to add numbers.
"""
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate

# Define the tool
@tool
def add_numbers(a: int, b: int):
    """Adds two numbers"""
    print(f"DEBUG - Tool called: add_numbers({a}, {b})")
    result = a + b
    print(f"DEBUG - Tool result: {result}")
    return result

# Create a simple system prompt
system_prompt = """You are a helpful assistant that uses tools when appropriate.
When asked to perform calculations, you should use the add_numbers tool rather than doing the calculation yourself."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("ai", "{agent_scratchpad}")
])

# Set up the AI
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# Create an agent with proper tool integration
tools = [add_numbers]
agent = create_openai_tools_agent(llm, tools, prompt)

# AgentExecutor is specifically designed to handle tool calls properly
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run the agent
print("\nRunning agent...")
result = agent_executor.invoke({"input": "Add 5 and 3. You must use the add_numbers tool."})

print("\nFINAL RESULT:")
print(result["output"])
