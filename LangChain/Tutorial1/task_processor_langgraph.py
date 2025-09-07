"""
A simple LangGraph example that demonstrates state management and flow control.
Demonstrates a task processing workflow with state management.
Type your task and the system will analyze it and provide both an analysis and
a detailed solution. Type 'quit' when you want to exit.
Author: tdiprima
"""

import json
from typing import Sequence, TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph


# Define our state
class AgentState(TypedDict):
    messages: Sequence[str]
    next_step: str
    task_status: dict


# Initialize LLM
llm = ChatOpenAI()


# Node functions
def analyze_task(state: AgentState) -> dict:
    """Analyze the task and determine next steps"""
    messages = state["messages"]
    response = llm.invoke(
        [
            HumanMessage(
                content=f"""
            Analyze this task and determine the next step. Respond with a JSON object with two fields:
            - next_step: either 'process' if task needs work or 'complete' if finished
            - analysis: brief analysis of the task
            
            Task: {messages[-1]}
            """
            )
        ]
    )

    result = json.loads(response.content)
    state["next_step"] = result["next_step"]
    state["task_status"]["analysis"] = result["analysis"]
    return state


def process_task(state: AgentState) -> dict:
    """Process the task and update status"""
    messages = state["messages"]
    response = llm.invoke(
        [
            HumanMessage(
                content=f"""
            Process this task and provide a solution. Current status: {state['task_status']['analysis']}
            Task: {messages[-1]}
            """
            )
        ]
    )

    state["task_status"]["solution"] = response.content
    state["next_step"] = "complete"
    return state


def should_process(state: AgentState) -> bool:
    """Determine if we should process the task"""
    return state["next_step"] == "process"


def should_end(state: AgentState) -> bool:
    """Determine if we should end"""
    return state["next_step"] == "complete"


# Define the state graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("analyze", analyze_task)
workflow.add_node("process", process_task)

# Add edges with conditional routing
workflow.set_entry_point("analyze")
workflow.add_conditional_edges("analyze", should_process, {True: "process", False: END})
workflow.add_edge("process", END)

# Compile the graph
app = workflow.compile()

if __name__ == "__main__":
    print("Task Processing System (type 'quit' to exit)")
    print("Enter tasks and the system will analyze and process them.\n")

    while True:
        # Get user input
        task = input("\nEnter a task: ")
        if task.lower() == "quit":
            break

        # Initialize state
        initial_state = {"messages": [task], "next_step": "analyze", "task_status": {}}

        # Run the workflow
        print("\nProcessing task...")
        result = app.invoke(initial_state)

        print("\nWorkflow Results:")
        print("Analysis:", result["task_status"]["analysis"])
        if "solution" in result["task_status"]:
            print("\nSolution:", result["task_status"]["solution"])

"""
Ideas:
Build a simple web application
Design a user authentication system
Create a data visualization dashboard
Implement a REST API for a blog
"""
