"""
Tools: Tool with LangChain
Uses tools to solve math problems.
Author: tdiprima
"""

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()


@tool
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """Subtract the second number from the first"""
    return a - b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together"""
    return a * b


@tool
def divide(a: int, b: int) -> float:
    """Divide the first number by the second"""
    return a / b


# Create a list of tools
tools = [add, subtract, multiply, divide]

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful math assistant. Use the available tools to solve math problems.",
        ),
        ("human", "{input}"),
        ("ai", "{agent_scratchpad}"),
    ]
)

# Create the agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Example usage
if __name__ == "__main__":
    result = agent_executor.invoke(
        {"input": "What is 15 multiplied by 5, then divided by 3?"}
    )
    print("Result:", result["output"])
