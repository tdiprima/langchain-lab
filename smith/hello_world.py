# Based on https://smith.langchain.com/onboarding
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
# llm = ChatOpenAI(verbose=True)
# llm.invoke("Hello! Who are you?")
response = llm.invoke("Hello! Who are you?")
print(response.content)
