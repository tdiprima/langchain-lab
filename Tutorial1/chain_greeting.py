"""
Chains: Greeting Chain
Builds a simple chain to greet someone funnily.
"""
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Build a prompt (the instruction)
prompt = PromptTemplate.from_template("Say hello to {name} in a fun way!")

# Pick an AI model (our worker)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Snap them together into a chain
chain = prompt | llm

# Run it!
response = chain.invoke({"name": "Bear"})
print(response.content)  # Hey there, Bear! Ready for some roaring good times?
