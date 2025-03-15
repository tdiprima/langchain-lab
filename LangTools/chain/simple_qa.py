"""
Basic LLM-based Q&A system with a static prompt.
Just a direct query-response system.
Author: tdiprima
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

import os
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"
api_key = os.getenv("OPENAI_API_KEY")


def ask_question(question):
    # Initialize the language model
    llm = ChatOpenAI(temperature=0.7)
    
    # Create a simple prompt template
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful AI assistant. Answer this: {question}"
    )
    
    # Format the prompt with the question
    formatted_prompt = prompt.format_prompt(question=question)
    
    # Get the response
    response = llm.invoke(formatted_prompt.to_messages())
    return response.content


# Example usage
question = "What is Python?"
response = ask_question(question)
print(f"AI: {response}")
