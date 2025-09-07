"""
A Minimal "Calculator" Tool Using LangGraph
Converted from LangChain example by tdiprima
"""

from typing import TypedDict

from langchain_openai import OpenAI
from langgraph.graph import END, StateGraph


# Define the state that will be maintained throughout the graph
class AgentState(TypedDict):
    input: str  # User's input question
    output: str  # Final response


# Define our calculator function (same as original)
def add_numbers(input_str: str) -> str:
    try:
        a, b = input_str.split()
        return str(float(a) + float(b))
    except Exception as ex:
        print(ex)
        return "Error: Please pass two numbers separated by a space."


# Define the tool node
def tool_node(state: AgentState) -> AgentState:
    # Simple parsing to extract numbers from the input
    # In a more complex scenario, you might use an LLM to parse this
    words = (
        state["input"]
        .lower()
        .replace("what is", "")
        .replace("plus", "")
        .replace("?", "")
        .strip()
    )
    result = add_numbers(words)
    return {"input": "", "output": result}


# Initialize the LLM (same as original)
llm = OpenAI(temperature=0)

# Create the graph
workflow = StateGraph(AgentState)

# Add nodes to the graph
workflow.add_node("calculator", tool_node)

# Set the entry point
workflow.set_entry_point("calculator")

# Set the finish point
workflow.add_edge("calculator", END)

# Compile the graph
app = workflow.compile()


# Use it
def run_calculator(query: str) -> str:
    result = app.invoke({"input": query, "output": ""})
    return result["output"]


# Test it
if __name__ == "__main__":
    response = run_calculator("What is 2 plus 7?")
    print(response)  # Should output "9"
