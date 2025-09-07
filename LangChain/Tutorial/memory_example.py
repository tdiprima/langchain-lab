"""
Create a simple chatbot that remembers previous messages in a conversation
Author: tdiprima
"""

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(temperature=0)
message_history = []

message = "Hi, my name is Bear."
print("User:", message)
message_history.append(HumanMessage(content=message))
reply = chat.invoke(message_history)
print(f"Assistant: {reply.content}")
message_history.append(reply)

message = "What's my name?"
print("\nUser:", message)
message_history.append(HumanMessage(content=message))
reply = chat.invoke(message_history)
print(f"Assistant: {reply.content}")

"""
User: Hi, my name is Bear.
Assistant:  Hello Bear, it's nice to meet you! My name is AI and I am an artificial intelligence designed to assist and communicate with humans. I am constantly learning and evolving, so I may not have all the answers, but I will do my best to help you. What can I assist you with today?

User: What's my name?
Assistant:  Your name is Bear. I know this because you introduced yourself as such at the beginning of our conversation. Is there anything else you would like to know about yourself?
"""
