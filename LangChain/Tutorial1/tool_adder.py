"""
This is an example of a LangGraph that uses a tool to add two numbers.
It successfully demonstrates:
- Tool usage with the add_numbers function
- State management with TypedDict
- Proper message handling and conversation flow
Author: tdiprima
"""

import json
from typing import List, TypedDict

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph


# Define a tool
@tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers"""
    result = a + b
    print(f"Adding {a} + {b} = {result}")
    return result


# Define state
class State(TypedDict):
    messages: List
    current_step: str


# Set up the AI
llm = ChatOpenAI(model="gpt-3.5-turbo").bind_tools([add_numbers])

# Create a graph
graph = StateGraph(State)


def agent(state: State) -> State:
    messages = state["messages"]
    if isinstance(messages[-1], str):
        messages[-1] = HumanMessage(content=messages[-1])

    print(f"\nProcessing message: {messages[-1].content}")
    response = llm.invoke(messages)

    # Handle tool calls if present
    if response.additional_kwargs.get("tool_calls"):
        tool_call = response.additional_kwargs["tool_calls"][0]
        tool_name = tool_call["function"]["name"]
        tool_args = json.loads(tool_call["function"]["arguments"])

        # Execute the tool
        if tool_name == "add_numbers":
            result = add_numbers.invoke(tool_args)
            # Add the tool result as a message
            messages.append(AIMessage(content=f"The result is {result}"))
    else:
        messages.append(response)

    return state


graph.add_node("agent", agent)
graph.add_edge("agent", END)
graph.set_entry_point("agent")
app = graph.compile()

# Run it!
initial_state = {"messages": ["Add 5 and 3"], "current_step": "agent"}
print("\nStarting conversation with: Add 5 and 3")
response = app.invoke(initial_state)
print("\nFinal messages:")
for msg in response["messages"]:
    if hasattr(msg, "content"):
        print(f"- {msg.content}")
    else:
        print(f"- {msg}")
