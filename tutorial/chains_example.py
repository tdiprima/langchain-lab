# chains_example.py

# 1. Import necessary classes
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
import os

# 2. Set your OpenAI API key (if not set as environment variable already)
os.environ["OPENAI_API_KEY"] = "YOUR-OPENAI-API-KEY-HERE"

# 3. Create a prompt template. This is the blueprint of the prompt the LLM will see.
template = "You are a friendly assistant. Respond to the user by name.\nUser: {user_input}\nAssistant:"
prompt = PromptTemplate(template=template, input_variables=["user_input"])

# 4. Initialize the LLM (OpenAI GPT-3 in this case)
llm = OpenAI(temperature=0.7)  # temperature=0.7 for a bit of creativity in the output

# 5. Create the chain by combining the prompt and the LLM
chain = LLMChain(prompt=prompt, llm=llm)

# 6. Run the chain with some input
user_name = "Alex"
question = f"My name is {user_name}. Can you greet me?"
response = chain.run(user_input=question)

print(response)
