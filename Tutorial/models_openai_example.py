from langchain.llms import OpenAI

# Initialize the OpenAI LLM
openai_llm = OpenAI(temperature=0.9)

prompt = "Tell me a short joke about chickens."
response = openai_llm(prompt)
print(response)
