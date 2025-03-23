from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda


class State(TypedDict, total=False):
    history: List[dict]
    intent: str
    response: str


def receive_input(state):
    # message = {"role": "user", "content": "What's the capital of France?"}
    message = {"role": "user", "content": "How are you doing this morning?"}
    history = state.get("history", [])
    history.append(message)
    return {"history": history}


llm = ChatOpenAI(model="gpt-4", temperature=0)


def route_intent(state):
    history = state["history"]
    last_msg = history[-1]["content"]
    decision = llm.invoke(
        f"Classify this message as 'qa' or 'chitchat': {last_msg}"
    )
    intent = decision.content.strip().lower().replace("'", "").replace('"', '')
    print(f"Intent classified as: '{intent}'")  # Debug line
    return {"intent": intent}


# QA path
def handle_qa(state):
    response = llm.invoke(state["history"])
    return {"response": response.content}


# Chitchat path
def handle_chitchat(state):
    # response = llm.invoke([
    #     *state["history"],
    #     # {"role": "system", "content": "You're a witty assistant, keep it light and friendly."}
    #     {"role": "system", "content": "You're a cheeky, fun assistant—crack a joke or keep it playful, no stiff answers!"}
    # ])
    last_msg = state["history"][-1]["content"]
    response = llm.invoke(
        f"Respond to '{last_msg}' with a short, witty quip—keep it light, no boring AI clichés!"
    )
    return {"response": response.content}


builder = StateGraph(State)

# Add nodes
builder.add_node("receive_input", RunnableLambda(receive_input))
builder.add_node("route", RunnableLambda(route_intent))
builder.add_node("qa", RunnableLambda(handle_qa))
builder.add_node("chitchat", RunnableLambda(handle_chitchat))

# Set entry
builder.set_entry_point("receive_input")

# Add edges
builder.add_edge("receive_input", "route")


# Conditional branching
def choose_path(state):
    intent = state["intent"]
    print(f"Intent: {intent}")
    return intent


builder.add_conditional_edges("route", choose_path, {
    "qa": "qa",
    "chitchat": "chitchat"
})

builder.add_edge("qa", END)
builder.add_edge("chitchat", END)

graph = builder.compile()

initial_state = {
    "history": []
}
result = graph.invoke(initial_state)
print(result["response"])
