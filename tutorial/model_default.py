from langchain_community.llms import OpenAI

# Initialize OpenAI with default settings
openai_llm = OpenAI(temperature=0.9)
# openai_llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.9)

# Print the default model being used
print(f"The default model is: {openai_llm.model_name}")
# The default model is: gpt-3.5-turbo-instruct
