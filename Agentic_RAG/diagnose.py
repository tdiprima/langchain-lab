"""
Clinical Symptom Analysis Tool with Diagnosis Hypothesis Generation
1) retrieve guidelines, 2) query the API for disease matches, 3) combine both into a hypothesis with the LLM.
Note: Requires OPENAI_API_KEY for LLM functionality
Author: tdiprima
"""
import os
import requests
import logging
from langchain.agents import initialize_agent
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from langchain.tools import tool

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("langchain")
logger.setLevel(logging.INFO)

# Load OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OpenAI API key is not set.")

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, openai_api_key=api_key)

# Sample medical documents
documents = [
    Document(page_content="Common causes of excessive thirst include diabetes mellitus, dehydration, or hypercalcemia."),
    Document(page_content="Fatigue and weight loss can indicate metabolic disorders such as diabetes or thyroid dysfunction."),
    Document(page_content="Standard tests for unexplained weight loss include blood glucose, thyroid function tests, and kidney function tests.")
]
embeddings = OpenAIEmbeddings(openai_api_key=api_key, model="text-embedding-ada-002")
vector_db = FAISS.from_documents(documents, embeddings)
retriever = vector_db.as_retriever()


# Tool: Retrieve medical knowledge
@tool
def retrieve_medical_knowledge(query: str):
    """Step 1: Fetch relevant medical guidelines from local knowledge base to inform diagnosis."""
    results = retriever.invoke(query)
    return [doc.page_content for doc in results]


# Tool: Query symptom-disease database
@tool
def check_symptom_disease_database(symptoms: str):
    """Step 2: Query an external API for possible disease matches after retrieving guidelines."""
    try:
        url = f"https://fake-medical-api.com/symptoms?query={symptoms}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return {"error": "Could not retrieve medical data."}
    except Exception as ex:
        print("\nAn exception occurred.", ex)
        return {"error": "Could not retrieve medical data."}


# Initialize agent
agent = initialize_agent(
    tools=[retrieve_medical_knowledge, check_symptom_disease_database],
    llm=llm,
    agent="conversational-react-description",
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs={
        "system_message": "Always start by retrieving medical guidelines with `retrieve_medical_knowledge` before querying external APIs."
    }
)

# Query
query = "A 55-year-old male presents with fatigue, weight loss, and excessive thirst. What could be the cause?"
chat_history = []
response = agent.run(input=query, chat_history=chat_history)

print("\nFinal Response:")
print(response)
