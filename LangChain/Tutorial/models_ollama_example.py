"""
Llama3 Fact-Generating Agent
Author: tdiprima
"""
from langchain_ollama import OllamaLLM

# Initialize Llama3 using Ollama locally
llm = OllamaLLM(model="llama3.2:latest")

# Ask Llama3 a fun question
prompt = "Tell me an interesting fact about space 🚀."
response = llm.invoke(prompt)

print(f"Llama3 says: {response}")

"""
Llama3 says: Did you know that there is a giant storm on Jupiter that has been raging for at least 187 years?
The Great Red Spot, as it's called, is a persistent anticyclonic storm on Jupiter, which means it's a high-pressure region 
with clockwise rotation. It's so large that three Earths could fit inside it, and it's still visible from Earth with the help of telescopes!
"""
