from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from pydantic import BaseModel


# Define the state - this is what flows between steps
class State(BaseModel):
    input: str = ""
    answer: str = ""


# Create a GPT-4 model (or gpt-3.5)
llm = ChatOpenAI(model="gpt-4", temperature=0)


# Node 1: Ask a question (simulate user input)
def ask_question(state: State) -> State:
    return State(
        input="What's your favorite programming language?", answer=state.answer
    )


# Node 2: Analyze the answer with GPT
def analyze_input(state: State) -> State:
    response = llm.invoke(f"User said: {state.input}. What can we infer from that?")
    return State(input=state.input, answer=response.content)


# Build graph
builder = StateGraph(State)

builder.add_node("ask", RunnableLambda(ask_question))
builder.add_node("analyze", RunnableLambda(analyze_input))

builder.set_entry_point("ask")
builder.add_edge("ask", "analyze")
builder.add_edge("analyze", END)

graph = builder.compile()

# Run it!
result = graph.invoke(State().model_dump())
print(result)
