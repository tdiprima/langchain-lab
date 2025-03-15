from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# Create a prompt template. This is the blueprint of the prompt the LLM will see.
template = "You are a friendly assistant. Respond to the user by name.\nUser: {user_input}\nAssistant:"
prompt = PromptTemplate(template=template, input_variables=["user_input"])

# Initialize the LLM
llm = OpenAI(temperature=0.7)  # temperature=0.7 for a bit of creativity

# Create the chain using RunnableSequence
chain = prompt | llm

# Run the chain with some input
user_name = "Bear"
question = f"My name is {user_name}. Can you greet me?"
response = chain.invoke({"user_input": question})

print(response)  # Hello Bear, it's nice to meet you! How can I assist you today?
