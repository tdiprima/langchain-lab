from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.runnables import RunnableLambda
from typing import TypedDict


# --------- STEP 1: Define State Schema ---------
class State(TypedDict):
    question: str
    thought: str
    calculation_result: str
    summary: str


# --------- STEP 2: Define LLM ---------
llm = ChatOpenAI(model="gpt-4", temperature=0)


# --------- STEP 3: Define Nodes ---------

# 1. Receive question
def receive_question(state: State) -> dict[str, str]:
    return {"question": "What's 24 * (365 + 1) + 42?"}  # simulate user input


# 2. Think step
def think_step(state: State) -> dict[str, str]:
    response = llm.invoke(f"User asked: {state['question']}. Think step-by-step.")
    return {"thought": response.content}


# 3. Tool use (Calculator)
@tool
def calculator(expr: str) -> str:
    """
    Evaluates a mathematical expression and returns the result as a string.
    
    Args:
        expr (str): A string containing a valid mathematical expression to evaluate.
        
    Returns:
        str: The result of the evaluated expression as a string, or an error message if evaluation fails.
    """
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Error: {e}"


def use_calculator(state: State) -> dict[str, str]:
    # Extract expression using GPT
    extract_expr = llm.invoke(
        f"Extract a math expression from this: {state['thought']}. Only return the expression."
    )
    result = calculator.invoke(extract_expr.content)
    return {"calculation_result": result}


# 4. Summarize final answer
def summarize(state: State) -> dict[str, str]:
    summary = llm.invoke(
        f"Original question: {state['question']}\n"
        f"Thoughts: {state['thought']}\n"
        f"Calculation result: {state['calculation_result']}\n"
        f"Summarize everything into a final answer."
    )
    return {"summary": summary.content}


# --------- STEP 4: Build the Graph ---------
# Build the graph
builder = StateGraph(State)

# Add nodes
builder.add_node("receive", RunnableLambda(receive_question))
builder.add_node("think", RunnableLambda(think_step))
builder.add_node("calculate", RunnableLambda(use_calculator))
builder.add_node("summarize", RunnableLambda(summarize))

# Add edges
builder.add_edge("receive", "think")
builder.add_edge("think", "calculate")
builder.add_edge("calculate", "summarize")
builder.add_edge("summarize", END)

# Set entry point
builder.set_entry_point("receive")

# Compile
graph = builder.compile()

# Initialize with empty state values
initial_state = {
    "question": "",
    "thought": "",
    "calculation_result": "",
    "summary": ""
}

# --------- STEP 5: Run It ---------
result = graph.invoke(initial_state)
print(result["summary"])
