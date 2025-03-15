"""
Memory: Chat with Memory
Shows how to make an AI remember your name or preferences.
"""
from langchain_core.messages import HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI

# Create a memory bank
memory = ChatMessageHistory()

# Add some convo
memory.add_user_message("Hi, I'm Bear!")
memory.add_ai_message("Hey Bear, nice to meet you!")

# Set up the AI
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Ask it something with memory
messages = memory.messages + [HumanMessage("What's my name?")]
response = llm.invoke(messages)
print(response.content)  # Your name is Bear!
