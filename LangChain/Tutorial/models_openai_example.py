"""
OpenAI Joke Generation
Author: tdiprima
"""
from langchain_openai import OpenAI

openai_llm = OpenAI(temperature=0.9)

prompt = "Tell me a short joke about chickens."
response = openai_llm(prompt)
print(response)
