"""
Basic RAG example
Implements retrieval-augmented generation (RAG) using OpenAI embeddings and FAISS.
Retrieves relevant documents and generates responses.
Author: tdiprima
"""

import os

from langchain.chains import RetrievalQA
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents.base import Document
# from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

api_key = os.getenv("OPENAI_API_KEY")  # Returns None if not set

if api_key is None:
    raise ValueError(
        "OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable."
    )

llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, api_key=api_key)

# Define some documents (like classified files)
documents = [
    Document(page_content="The nuclear codes are hidden in the vault."),
    Document(page_content="Agent X was last seen in Paris."),
    Document(
        page_content="The formula for the secret serum is stored on a secure server."
    ),
]

# Convert text into vector embeddings
# Initialize embeddings with retry parameters to handle newer SDK correctly
try:
    embeddings = OpenAIEmbeddings(
        api_key=api_key, model="text-embedding-ada-002", max_retries=5
    )
    print("Embeddings initialized successfully!")
except Exception as e:
    print(f"Error initializing OpenAIEmbeddings: {e}")

try:
    vector_db = FAISS.from_documents(documents, embeddings)
    print("FAISS database initialized successfully!")
except Exception as e:
    print(f"Error initializing FAISS: {e}")

retriever = vector_db.as_retriever()

query = "Where is Agent X?"
retrieved_docs = retriever.invoke(query)

for doc in retrieved_docs:
    print(doc.page_content)  # Output: "Agent X was last seen in Paris."

# "stuff" directly appends retrieved data
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

response = qa_chain.invoke({"query": "Tell me about the nuclear codes."})
print(response["result"])  # AI will generate a response based on retrieved data.
