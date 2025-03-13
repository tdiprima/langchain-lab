import os
from langchain_openai import OpenAIEmbeddings

api_key = os.getenv("OPENAI_API_KEY")  # Returns None if not set

try:
    embeddings = OpenAIEmbeddings(
        openai_api_key=api_key,
        model="text-embedding-ada-002",
        max_retries=5
    )
    print("Embeddings initialized successfully!")
except Exception as e:
    print(f"Error initializing OpenAIEmbeddings: {e}")

from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document

documents = [
    Document(page_content="The nuclear codes are hidden in the vault."),
    Document(page_content="Agent X was last seen in Paris."),
    Document(page_content="The formula for the secret serum is stored on a secure server.")
]

try:
    vector_db = FAISS.from_documents(documents, embeddings)
    print("FAISS database initialized successfully!")
except Exception as e:
    print(f"Error initializing FAISS: {e}")
