## 🧠 What Is LangGraph?

**Analogy**: Imagine LangGraph as a **flowchart for conversations**, where each bubble (node) is a piece of logic (like calling a function, model, or API), and the arrows (edges) are how you move between those bubbles based on conditions.

It's like **state machines meets LLMs**.


### 🧱 Core Concepts

- **Node**: A function or a step (e.g., call GPT-4, fetch tool results).
- **Edge**: Conditional logic to move between nodes.
- **State**: Dict that carries data between nodes.
- **Graph**: The full pipeline (workflow engine) with nodes + edges.


### ⚡️ Simple Example: A LangGraph with Two Steps

**Goal: Ask the user a question, analyze the answer with GPT-4.**

[chat.py](chat.py)


### 📦 What Makes LangGraph Powerful?

**Memory**: State is carried automatically, so your GPT calls can remember and build up a conversation.

**Branching**: You can dynamically move to different nodes (like in a game engine).

**Tools**: Combine LangChain tools (e.g., search, DB, APIs) as nodes.


### 🧪 Want to Try a Real Use Case Next?

I can walk you through building a **multi-step agent** (e.g., reasoning + tool use + summarization), or hook LangGraph into a **chatbot with memory**.

---

## 🧠 First Up: Multi-Step Agent with Reasoning + Tool Use + Summarization

### 🧰 Tools Used
- GPT-4 for reasoning
- Calculator (simple tool)
- Final summarizer


### 📊 Use Case: User asks a question → model thinks → uses a calculator → summarizes

Here's the full code:

[mathgraph.py](mathgraph.py)

Next up 👇

---

## 🧭 Chatbot With Memory + Branching Logic

We'll:

- Maintain conversation history
- Branch based on user intent (e.g., Q&A vs. chit-chat)

Let's build a **LangGraph-powered chatbot** step by step — this one will **remember context and branch logic** based on user intent.


## 🧭 GOAL

We'll build a [chatbot](chatgraph.py) that can:

- ✅ Handle conversations across turns (memory)
- 🔀 Branch between answering questions or casual chatting
- 🧠 Use GPT to decide what to do next


### 🧱 STEP 0: Mental Model

**Analogy**: Imagine a hotel concierge bot.

- If you ask "What time is breakfast?", it **answers a factual question**.
- If you say "I love this place!", it **chats back casually**.
- Behind the scenes, it **remembers everything** you said.

That's what we're going to build.


## ✅ STEP 1: Define State Schema

This is the memory that gets passed between steps.

```python
class State(TypedDict, total=False):    history: List[dict]   # list of message dicts    intent: str           # "qa" or "chitchat"    response: str         # current response
```

**Why a list for history?**  
We'll feed it to GPT so it knows what was said before (like a running transcript).


## 💬 STEP 2: Simulate a Message + Add to History

We'll start by simulating a message like:

"What's the capital of France?"

```python
def receive_input(state):
    message = {"role": "user", "content": "What's the capital of France?"}
    history = state.get("history", [])
    history.append(message)
    return {"history": history}
```


## 🧠 STEP 3: Use GPT to Decide Intent (QA or Chitchat)

```python
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model="gpt-4", temperature=0)

def route_intent(state):
    history = state["history"]
    last_msg = history[-1]["content"]
    decision = llm.invoke(
        f"Classify this message as 'qa' or 'chitchat': {last_msg}"
    )
    intent = decision.content.strip().lower().replace("'", "").replace('"', '')
    return {"intent": intent}
```


## 🧪 STEP 4: Two Response Handlers

```python
# QA path
def handle_qa(state):
    response = llm.invoke(state["history"])
    return {"response": response.content}

# Chitchat path
def handle_chitchat(state):
    response = llm.invoke([
        *state["history"],
        {"role": "system", "content": "You're a witty assistant, keep it light and friendly."}
    ])
    return {"response": response.content}
```


## 🧠 STEP 5: Build the Graph with Branching

```python
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

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
    return state["intent"]

builder.add_conditional_edges("route", choose_path, {
    "qa": "qa",
    "chitchat": "chitchat"
})

builder.add_edge("qa", END)
builder.add_edge("chitchat", END)

graph = builder.compile()
```


## ▶️ STEP 6: Run It

```python
initial_state = {    "history": []}result = graph.invoke(initial_state)
print(result["response"])
```


You now have a chatbot that:

- Tracks the full conversation
- Decides the intent of user messages
- Branches to the right type of reply


### 👉 Next Power-Up Ideas:

- Add tools (e.g., calculator, search)
- Looping back to receive more messages
- Store history in a vector DB

Want to add a **tool**, or should we build a **looping chatbot** next?

---

**If `initial_state` is an object with a `history` that's an empty array, then when you call `result = graph.invoke(initial_state)`, how does it know to do all that other stuff?**

Hey, code ninja! 🧠 You're right: `initial_state` starts with an empty `history` array. So how does the graph kick off and do its thing? Here's the breakdown:

### The Magic Trigger
When you call `graph.invoke(initial_state)`, the LangGraph engine doesn't just sit there twiddling its thumbs—it's like hitting "Run" in your IDE. The graph starts at the **entry point** (`receive_input`) and flows from there. The `initial_state` is just the starting fuel—think of it as the blank canvas the graph paints on.

### Step-by-Step (Analogy: A Factory Line! 🏭)
1. **Entry Point: `receive_input`**  
   - Code:  

      ```python
      def receive_input(state):
          message = {"role": "user", "content": "What's the capital of France?"}
          history = state.get("history", [])
          history.append(message)
          return {"history": history}
      ```

   - What happens: Even though `initial_state` has `history: []`, this node *adds* a hardcoded message (`"What's the capital of France?"`) to `history`. It's like a worker tossing a part onto the conveyor belt—it doesn't care if the belt started empty.  
   - Output: `state` now has `history: [{"role": "user", "content": "What's the capital of France?"}]`.

2. **Next Stop: `route`**  
   - The graph follows the edge from `receive_input` to `route`. It grabs that updated `history`, classifies the intent (e.g., `"qa"`), and updates `state.intent`. It's like a sorter flipping a switch based on the part it sees.

3. **Conditional Branching: `qa` or `chitchat`**  
   - `choose_path` checks `state.intent` and routes to `qa` or `chitchat`. Think of it as a forklift picking the right path—`qa` for questions, `chitchat` for banter.

4. **Endgame: Response**  
   - The chosen node (`qa` or `chitchat`) processes `history` with the LLM and sets `state.response`. Then it hits `END`, and `invoke` hands you the final `state`. It's the factory spitting out a finished product!

### Why It Works
- The graph doesn't rely on `initial_state` having data—it's the *nodes* that build the state as they run. `receive_input` injects the question, kicking off the chain reaction.  
- Analogy: It's like a game of Mario Kart—`initial_state` is Mario in the starting block, but the track (graph) and actions (nodes) drive him to the finish line. 🏎️

### Your Case: `"how are you doing today?"`
If you tweak `receive_input` to:

```python
message = {"role": "user", "content": "how are you doing today?"}
```

It'll still work! `history` starts empty, `receive_input` adds that message, `route` tags it as `"chitchat"`, and `handle_chitchat` fires off a reply. The empty `initial_state` just means "start fresh"—the graph fills in the blanks.

### Clear Now? 🎉
It's all about the graph's flow taking over. Want to test it with a print to see `history` grow? Or got another twist to explore? 🚀

<br>
