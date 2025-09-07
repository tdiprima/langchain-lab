"""
Hugging Face Text Generation
Author: tdiprima
"""

import os

from langchain_community.llms import HuggingFaceHub

# Set your Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "YOUR-HUGGINGFACE-API-TOKEN-HERE"

# Initialize the Hugging Face model
# Using google/flan-t5-small as an example - it's a smaller, faster model
llm = HuggingFaceHub(
    repo_id="google/flan-t5-small", model_kwargs={"temperature": 0.7, "max_length": 64}
)

# Create a prompt
prompt = "Translate this to French: 'Hello, how are you?'"

# Generate the response
response = llm.invoke(prompt)
print(f"Prompt: {prompt}")
print(f"Response: {response}")
