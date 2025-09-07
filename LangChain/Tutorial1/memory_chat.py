"""
Memory: Chat with Memory
Shows how to make an AI remember your name or preferences.
Author: tdiprima
"""

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

memory = ConversationBufferMemory()

chain = ConversationChain(llm=llm, memory=memory)

while True:
    user_input = input("User: ")

    if user_input == "quit":
        break

    response = chain.invoke({"input": user_input})

    print("Assistant:", response["response"])
