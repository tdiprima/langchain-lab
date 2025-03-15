import os
from langchain_openai import ChatOpenAI

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "your-api-key"
os.environ["LANGSMITH_PROJECT"] = "test-project-123"

llm = ChatOpenAI()
response = llm.invoke("Am I awesome?")
print(response.content)
# Yes, you are awesome!
