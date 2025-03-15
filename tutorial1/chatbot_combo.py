"""
Putting It All Together: A Mini Chatbot
Combines chains, memory, and tools into a mini chatbot.
"""
from operator import itemgetter

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


# Tool
@tool
def shout(text: str):
    """Shouts your text"""
    return text.upper() + "!!!"


# Memory
memory = ChatMessageHistory()

# Prompt
prompt = ChatPromptTemplate.from_messages([("system", """You're a fun assistant with memory and tools! 
    
IMPORTANT: ONLY use the 'shout' tool when a user EXPLICITLY asks you to shout something.
For regular conversation, do NOT use the shout tool even if the word "shout" appears in a different context.

TOOL USAGE INSTRUCTIONS:
1. ONLY use the shout tool when specifically asked to shout something
2. The shout tool takes a text parameter and returns that text in uppercase with exclamation marks
3. For all other conversation, respond normally without using tools
4. Do NOT attempt to simulate shouting by using uppercase text yourself

Examples of CORRECT usage:

Example 1 (Normal conversation):
Human: Hi there! What can you do?
Assistant: Hello! I'm a fun assistant that can help answer questions, have conversations, and I have a special ability to shout text when you ask me to. Just ask me to shout something if you'd like to see it in action!

Example 2 (Proper tool usage):
Human: Please shout "Hello world"
Assistant: I'll shout that for you!
<tool>shout(text="Hello world")</tool>

Example 3 (Do NOT use tool for this):
Human: People sometimes shout when they're excited.
Assistant: That's true! People do tend to raise their voice when excited. It's a natural expression of enthusiasm.

REMEMBER: ONLY use the shout tool when explicitly asked to shout something specific."""),
    MessagesPlaceholder(variable_name="history"), ("human", "{input}") ])

# AI with tools
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
llm_with_tools = llm.bind_tools([shout], tool_choice="auto")

# Create LangChain chain
chain = ({"input": itemgetter("input"), "history": lambda _: memory.messages} | prompt | llm_with_tools)


# Chat function
def chat(user_input):
    # Add the user message to history
    memory.add_user_message(user_input)

    # Invoke the chain
    response = chain.invoke({"input": user_input})

    # Extract response content
    content = ""
    if hasattr(response, "content"):
        content = response.content
    elif isinstance(response, str):
        content = response

    # Check if the response has tool calls and execute them
    if hasattr(response, "additional_kwargs") and "tool_calls" in response.additional_kwargs:
        # Print initial assistant response without tool text
        # Clean up the content by removing any <tool> tags
        clean_content = content.split("<tool>")[0].strip()
        print(f"Assistant: {clean_content}")

        # Process each tool call
        for tool_call in response.additional_kwargs["tool_calls"]:
            # Extract tool name and arguments
            tool_name = tool_call["function"]["name"]
            tool_args = tool_call["function"]["arguments"]

            # Parse JSON arguments
            import json
            try:
                parsed_args = json.loads(tool_args)
            except json.JSONDecodeError:
                print(f"Error parsing tool arguments: {tool_args}")
                continue

            if tool_name == "shout":
                # Execute the shout tool using invoke method
                result = shout.invoke(parsed_args)
                print(f"Tool {tool_name}: {result}")

                # Add tool response to the content
                tool_response = f"\nResult: {result}"
                content = clean_content + tool_response

        # Add the assistant's response with tool results to history
        memory.add_ai_message(content)
        return content
    else:
        # Extract content for regular responses
        content = response.content if hasattr(response, "content") else str(response)

        # Clean up the content by removing any <tool> or <function> tags that might appear
        if "<tool>" in content:
            content = content.split("<tool>")[0].strip()

        # Add the assistant's response to history
        memory.add_ai_message(content)

        print(f"Assistant: {content}")
        return content


# Test conversations
print("\n--- TESTING CHATBOT FUNCTIONALITY ---")

print("\nStarting conversation...")
chat("Hi, I'm Zelda!")

print("\nTesting simple question-answer...")
chat("What can you do to help me?")

print("\nTesting shout functionality...")
chat("I introduced myself earlier.  Please shout my name.")

print("\nTesting memory consistency...")
chat("What was the word you shouted for me earlier?")

print("\nTesting another shout request...")
chat("Now shout 'Awesome Code' please!")

print("\nTesting conversation wrap-up...")
chat("Thank you for demonstrating your capabilities!")
