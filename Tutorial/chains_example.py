"""
AI Chatbot greeting user
Author: tdiprima
"""
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# Prompt template instructs the assistant to respond in a friendly manner and address the user by name
template = "You are a friendly assistant. Respond to the user by name.\nUser: {user_input}\nAssistant:"
prompt = PromptTemplate(template=template, input_variables=["user_input"])

llm = OpenAI(temperature=0.7)  # 0.7 for creativity

# LangChain pipeline processes the user's input and passes it to the OpenAI language model with a set temperature
chain = prompt | llm

# Construct a user query
user_name = "Bear"
question = f"My name is {user_name}. Can you greet me?"

# Execute the pipeline
response = chain.invoke({"user_input": question})

print(response)  # Hello Bear, it's nice to meet you! How can I assist you today?
