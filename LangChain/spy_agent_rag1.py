"""
Agentic RAG example
Uses a retriever tool to fetch intelligence data.
Calls an external API tool to get real-time "spy network" updates.
Dynamically reasons over the retrieved information before responding.
Author: tdiprima
"""

import os

import requests
from langchain.agents import initialize_agent
from langchain.tools import tool
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Load API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError(
        "OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable."
    )

# Initialize LLM with reasoning capability
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, api_key=api_key)

# Create vector database with sample documents
documents = [
    Document(page_content="The nuclear codes are hidden in the vault."),
    Document(page_content="Agent X was last seen in Paris."),
    Document(
        page_content="The formula for the secret serum is stored on a secure server."
    ),
]
embeddings = OpenAIEmbeddings(api_key=api_key, model="text-embedding-ada-002")
vector_db = FAISS.from_documents(documents, embeddings)
retriever = vector_db.as_retriever()


# Tool: Retrieve intelligence data
@tool
def retrieve_intelligence(query: str):
    """Searches classified intelligence data based on query."""
    results = retriever.invoke(query)
    return [doc.page_content for doc in results]


# Tool: Fetch external spy network info (simulated API call)
@tool
def fetch_spy_network_update(agent_name: str):
    """Fetches latest intelligence reports on a specific agent."""
    try:
        # Simulated API call
        url = f"https://fake-spy-network-api.com/agent?name={agent_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {"error": "Could not retrieve spy network data."}
    except Exception as ex:
        print("\nAn exception occurred.", ex)
        return {"error": "Could not retrieve spy network data."}


# Initialize an agent with tools
agent = initialize_agent(
    tools=[retrieve_intelligence, fetch_spy_network_update],
    llm=llm,
    agent="conversational-react-description",
    verbose=True,
)

# Example query
query = "Where is Agent X and what is his mission?"
response = agent.invoke({"input": query, "chat_history": []})
print(response["output"])
