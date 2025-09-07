# Based on: https://smith.langchain.com/onboarding
import openai
from langsmith import traceable
from langsmith.wrappers import wrap_openai

# Auto-trace LLM calls in-context
client = wrap_openai(openai.Client())


@traceable  # Auto-trace this function
def pipeline(user_input: str):
    result = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}], model="gpt-3.5-turbo"
    )
    return result.choices[0].message.content


# pipeline("What's the best pizza topping?")
print(pipeline("What's the best pizza topping?"))
