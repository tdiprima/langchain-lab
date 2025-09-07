"""
Clinical Decision Support Tool for Diabetes Medication Selection
Note: Requires SERPAPI_API_KEY and OPENAI_API_KEY
Author: tdiprima
"""

import requests
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_community.utilities import SerpAPIWrapper
from langchain_openai import ChatOpenAI


# Define a function to fetch drug contraindications
def check_drug_contraindications(medication, condition):
    """Fetch drug contraindications based on a condition."""
    url = f"https://api.fda.gov/drug/label.json?search={medication}+AND+{condition}"
    response = requests.get(url)
    if response.status_code == 200:
        return (
            response.json()
            .get("results", [{}])[0]
            .get("warnings", "No warnings found.")
        )
    return "No data available"


# Define an agent tool for checking contraindications
def contraindication_checker(input_str: str):
    """Check if a medication is safe for a condition.

    Input should be in the format: 'medication,condition'
    """
    try:
        parts = input_str.split(",")
        medication = parts[0].strip()
        condition = parts[1].strip()
        return check_drug_contraindications(medication, condition)
    except (IndexError, ValueError):
        return "Please provide input in the format: 'medication,condition'"


search = SerpAPIWrapper()


# Define an agent tool for retrieving diabetes treatment guidelines
def retrieve_medical_guidelines(query: str):
    """Searches medical guidelines using a web search API."""
    return search.run(query)


# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create an agent with memory
# Create properly formatted tools
tools = [
    Tool(
        name="retrieve_medical_guidelines",
        func=retrieve_medical_guidelines,
        description="Searches medical guidelines using a web search API.",
    ),
    Tool(
        name="contraindication_checker",
        func=contraindication_checker,
        description="Check if a medication is safe for a condition. Input should be in the format: 'medication,condition'",
    ),
]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
)

# Query: Find the best medication for diabetes with kidney disease
query = "What is the best medication for a diabetic patient with kidney disease?"
response = agent.run(query)

print(response)
