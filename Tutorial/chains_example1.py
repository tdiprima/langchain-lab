"""
Multi-Chain: chain multiple processing steps together
Author: tdiprima
"""
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# First Chain: Summarization Step
summarization_template = "Summarize this input concisely:\n{user_input}"
summarization_prompt = PromptTemplate(template=summarization_template, input_variables=["user_input"])
llm = OpenAI(temperature=0.5)

summarization_chain = summarization_prompt | llm  # First chain: summarization

# Second Chain: Response Generation
response_template = "You are a friendly assistant. Respond to this summary:\nSummary: {summary}\nAssistant:"
response_prompt = PromptTemplate(template=response_template, input_variables=["summary"])

response_chain = response_prompt | llm  # Second chain: response generation

# Example Input
user_input = "Hello, my name is Bear. I was wondering if you could give me a friendly greeting and maybe tell me something interesting about the world."

# Run the chains
summary = summarization_chain.invoke({"user_input": user_input})
summary = summary.strip()
response = response_chain.invoke({"summary": summary})

# Output
print("Summary:", summary)  # Bear wants a friendly greeting and to learn something interesting about the world.
print("Assistant's Response:", response)
"""
Hello Bear! Did you know that the Great Barrier Reef is the largest living structure on Earth and is home to thousands of different species?
It's truly a fascinating and diverse place in our world.
"""
