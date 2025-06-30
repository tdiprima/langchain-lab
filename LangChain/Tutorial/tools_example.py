"""
AI Agent that uses tools to answer questions
Author: tdiprima
"""
import warnings

warnings.filterwarnings("ignore")  # Suppress warnings for cleaner output

from langchain_openai import OpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import Tool
from datetime import datetime


# Define the current time tool
def get_current_time(unused_input=None):
    """Returns the current time as a string."""
    return datetime.now().strftime("%H:%M:%S")


# Create the tool list
tools = [
    Tool(
        name="Current Time",
        func=get_current_time,
        description="Get the current time in HH:MM:SS format"
    )
]

# Initialize the LLM
llm = OpenAI(temperature=0)

# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Ask the agent a question that requires the tool
question = "What is the current time?"

# Run the agent using invoke with a dictionary input
response = agent.invoke({"input": question})

# Print the final answer
print(f"Agent's answer: {response['output']}")

"""
> Entering new AgentExecutor chain...
 I should use the Current Time tool to get the current time
Action: Current Time
Action Input: None
Observation: 12:55:00
Thought: I now know the final answer
Final Answer: 12:55:00

> Finished chain.
Agent's answer: 12:55:00
"""
