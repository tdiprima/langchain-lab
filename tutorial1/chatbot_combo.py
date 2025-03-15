"""
Putting It All Together: A Mini Chatbot
Combines chains, memory, and tools into a mini chatbot.
"""
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# Memory
memory = ChatMessageHistory()


# Tool
@tool
def shout(text: str):
    """
    Shouts your text
    """
    return text.upper() + "!!!"


# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a super fun assistant who loves to be playful! If asked to 'shout' or make something loud, use the 'shout' tool. Use memory to remember the user's name."),
    ("human", "{input}")
])

# AI with tools
llm = ChatOpenAI(model="gpt-4").bind_tools([shout])
chain = prompt | llm


# LangGraph setup
class State(dict):
    messages = []


graph = StateGraph(State)


def agent(state):
    # Convert input string to HumanMessage if it’s the first message
    if isinstance(state["messages"][0], str):
        state["messages"][0] = HumanMessage(content=state["messages"][0])
    # Add memory to state
    state["messages"] = memory.messages + [state["messages"][0]]
    # Invoke chain with the latest message content
    response = chain.invoke({"input": state["messages"][-1].content})

    # Check if the response includes a tool call
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "shout":
                # Get the text to shout
                text_to_shout = tool_call["args"]["text"]
                # If it's "my name", replace it with the actual name from memory
                if "my name" in text_to_shout.lower():
                    for msg in reversed(memory.messages):
                        if isinstance(msg, HumanMessage) and "I'm" in msg.content:
                            # Extract name (e.g., "Zelda" from "Hi, I'm Zelda!")
                            name = msg.content.split("I'm")[1].split("!")[0].strip()
                            text_to_shout = name
                            break
                # Call the shout tool with the resolved text
                shouted_text = shout.invoke({"text": text_to_shout})
                response = AIMessage(content=shouted_text)
    # Add response to memory and state
    memory.add_ai_message(response.content)
    state["messages"].append(response)
    return state


graph.add_node("agent", agent)
graph.add_edge("agent", END)
graph.set_entry_point("agent")
app = graph.compile()

# Chat!
response = app.invoke({"messages": ["Hi, I'm Zelda!"]})
print(response["messages"][-1].content)
response = app.invoke({"messages": ["Shout my name!"]})
print(response["messages"][-1].content)
"""
Hello Zelda! It's great to meet you! How can I assist you today?
Sure, I would love to, but first, could you please tell me your name?
"""
