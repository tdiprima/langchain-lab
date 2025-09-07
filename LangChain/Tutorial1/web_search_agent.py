"""
An AI-powered web search agent using LangChain and OpenAI.
Integrates TavilySearch for retrieving online results and
executes search queries via a chatbot interface.
Author: tdiprima
"""

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

# Initialize the Tavily search tool
search_tool = TavilySearchResults(max_results=3)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that uses web search to answer questions.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Initialize the language model
llm = ChatOpenAI(temperature=0)

# Create the agent
tools = [search_tool]
functions = [format_tool_to_openai_function(t) for t in tools]
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def process_query(query: str) -> str:
    """
    Process a search query using the Tavily search tool and return results
    """
    result = agent_executor.invoke({"input": query, "chat_history": []})
    return result["output"]


if __name__ == "__main__":
    # Example usage
    query = "What are the latest developments in quantum computing?"
    print("\nQuery:", query)
    print("\nResults:", process_query(query))
