"""
An AI-powered search agent using LangChain and OpenAI.
Includes a fake search function with predefined responses and an agent
for handling search queries via a chat-based interface.
Author: tdiprima
"""

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI


def fake_search(query: str) -> str:
    """Use this tool when you need to search for information about any topic.

    Args:
        query: The search query or topic to search for
    Returns:
        Information found about the topic
    """
    responses = {
        "meaning of life": "According to various sources, it's 42!",
        "weather": "It's always sunny in the digital world!",
        "food": "The most popular food is pizza, according to my fake data.",
    }

    # Try to match query with predefined responses, or give a default
    for key in responses:
        if key in query.lower():
            return responses[key]
    return f"Based on my fake search: {query} is a fascinating topic!"


# Initialize the model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Define tools
tools = [
    Tool(
        name="search",
        func=fake_search,
        description="Search for information about any topic",
    )
]

# Create prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI assistant with access to a search tool. You must ONLY use the information returned by the search tool in your responses - do not add any additional information or ask follow-up questions about location, time, or other specifics. Simply relay what the search tool tells you.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Create the agent
agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)

# Create the executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # This will show the agent's thinking process
)

# Initialize an empty chat history
chat_history = []

# Interactive loop
while True:
    user_input = input("\nUser (type 'quit' to exit): ")

    if user_input.lower() == "quit":
        break

    response = agent_executor.invoke(
        {"input": user_input, "chat_history": chat_history}
    )
    print("\nAssistant:", response["output"])

"""
Try asking questions about:

- The meaning of life
- The weather
- Food
- Or any other topic (it will give a generic response)
"""
