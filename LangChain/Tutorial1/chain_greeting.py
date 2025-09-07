"""
Chains: Greeting Chain
Builds a simple chain to greet someone.
Author: tdiprima
"""

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

prompt = PromptTemplate.from_template(
    "You are a cheerful assistant.  Say hello to {name}"
)

chain = prompt | llm

response = chain.invoke({"name": "Bear"})

print(
    response.content
)  # Hello, Bear! 🌟 It's so nice to meet you! How are you doing today?
