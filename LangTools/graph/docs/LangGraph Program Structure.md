## LangGraph for dummies, ground floor edition.

I'll break down the basic structure of a LangGraph program for you, focusing on the order of components and what goes where.

## Core Structure (In Order)

**1. Define Your State**
First, you create a TypedDict that holds all the data your graph will work with:

```python
from typing import TypedDict

class GraphState(TypedDict):
    messages: list
    user_input: str
    result: str
```

**2. Create Your Nodes (Functions)**
These are the actual functions that do work. Each takes the state and returns updated state:

```python
def process_input(state: GraphState):
    # Do something with state
    return {"messages": state["messages"] + ["Processing..."]}

def generate_response(state: GraphState):
    # Generate output
    return {"result": "Here's your answer"}
```

**3. Build the Graph**
This is where you wire everything together:

```python
from langgraph.graph import StateGraph

# Create graph with your state schema
workflow = StateGraph(GraphState)

# Add nodes (give them names)
workflow.add_node("process", process_input)
workflow.add_node("respond", generate_response)

# Add edges (connect nodes)
workflow.add_edge("process", "respond")

# Set entry point
workflow.set_entry_point("process")

# Set finish point
workflow.set_finish_point("respond")

# Compile it
app = workflow.compile()
```

## Key Parameters to Remember

- **StateGraph()** - Takes your state schema as parameter
- **add_node()** - Takes (name, function)
- **add_edge()** - Takes (from_node, to_node)
- **add_conditional_edges()** - Takes (from_node, decision_function, routing_map)

## Simple Complete Example

```python
from typing import TypedDict
from langgraph.graph import StateGraph

# 1. State
class State(TypedDict):
    count: int

# 2. Nodes
def increment(state):
    return {"count": state["count"] + 1}

def double(state):
    return {"count": state["count"] * 2}

# 3. Build
graph = StateGraph(State)
graph.add_node("inc", increment)
graph.add_node("dbl", double)
graph.add_edge("inc", "dbl")
graph.set_entry_point("inc")
graph.set_finish_point("dbl")

# 4. Use
app = graph.compile()
result = app.invoke({"count": 5})
# Result: {"count": 12} (5+1=6, 6*2=12)
```

The key insight is that LangGraph is really just:
1. Define what data flows through (State)
2. Define what happens to that data (Nodes/Functions)
3. Define the order things happen (Edges)
4. Compile and run

Think of it like a recipe: ingredients (state), steps (nodes), and the order you do them (edges).

<br>
