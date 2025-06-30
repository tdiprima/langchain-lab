# Friendly LangChain & LangGraph Tutorial

**Date:** March 15, 2025  
**Versions:** LangChain 0.3.20, LangGraph 0.3.5  
**Goal:** Learn the big 4—Chains, Memory, Agents, Tools—fast, with code you can run!

---

## Setup (Do This First!)
Let's get the boring stuff out of the way. Run this in your Python environment (e.g., Jupyter or Colab):

```bash
pip install langchain==0.3.20 langgraph==0.3.5 langchain-openai
```

Set up your OpenAI API key (get one from [OpenAI](https://platform.openai.com/)):

```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

Ready? Let's roll!

---

## 1. Chains: The LEGO Blocks of AI
**What's a Chain?** Think of it like stacking LEGO pieces: you connect a prompt to an AI model to get an answer. Simple, reusable, awesome.

### Quick Example: Greeting Chain
```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Step 1: Build a prompt (the instruction)
prompt = PromptTemplate.from_template("Say hello to {name} in a fun way!")

# Step 2: Pick an AI model (our worker)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Step 3: Snap them together into a chain
chain = prompt | llm

# Step 4: Run it!
response = chain.invoke({"name": "Alex"})
print(response.content)
```

**Try It!**

- Run the code. Expect something like: "Hey Alex, you rockstar, hello from the AI side!"
- Change "Alex" to your name. What happens?

**Why It's Cool:** Chains let you reuse prompts and models like a recipe. No mess, just results!

---

## 2. Memory: AI That Remembers You
**What's Memory?** Normally, AI forgets everything after each chat. Memory fixes that—it's like giving your AI a sticky note.

### Quick Example: Chat with Memory
```python
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ChatMessageHistory
from langchain_openai import ChatOpenAI

# Step 1: Create a memory bank
memory = ChatMessageHistory()

# Step 2: Add some convo
memory.add_user_message("Hi, I'm Sam!")
memory.add_ai_message("Hey Sam, nice to meet you!")

# Step 3: Set up the AI
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Step 4: Ask it something with memory
messages = memory.messages + [HumanMessage("What's my name?")]
response = llm.invoke(messages)
print(response.content)
```

**Try It!**

- Run it. It should say something like: "Your name is Sam!"
- Add more messages to `memory` (e.g., "I like pizza"). Then ask: "What do I like?" See if it remembers!

**Why It's Cool:** Memory makes your AI feel like a friend, not a stranger every time.

---

## 3. Agents: AI That Thinks and Acts
**What's an Agent?** Chains are dumb—they just follow orders. Agents are smarter: they decide what to do next, like a mini-robot assistant.

### Quick Example: Agent with a Tool
```python
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool

# Step 1: Make a fake tool (pretend it searches the web)
def fake_search(query):
    return f"I found: {query} is awesome!"

tools = [Tool(name="Search", func=fake_search, description="Searches stuff")]

# Step 2: Create an agent
llm = ChatOpenAI(model="gpt-3.5-turbo")
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description")

# Step 3: Ask it something
response = agent.run("Tell me about cats!")
print(response)
```

**Try It!**

- Run it. You'll get something like: "I found: cats is awesome!"
- Change "cats" to "dogs" or anything else. Does it adapt?

**Why It's Cool:** Agents think for themselves—perfect for tasks where you don't know every step ahead of time.

---

## 4. Tools: Giving AI Superpowers
**What's a Tool?** Tools are like gadgets for your AI—think Batman's utility belt. They let it do more than just talk (e.g., search, calculate).

### Quick Example: Tool with LangGraph
```python
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# Step 1: Define a tool
@tool
def add_numbers(a: int, b: int):
    "Adds two numbers"
    return a + b

# Step 2: Set up the AI
llm = ChatOpenAI(model="gpt-3.5-turbo").bind_tools([add_numbers])

# Step 3: Define a simple state
class State(dict):
    messages = []

# Step 4: Create a graph (LangGraph magic!)
graph = StateGraph(State)
def agent(state):
    response = llm.invoke(state["messages"])
    state["messages"].append(response)
    return state

graph.add_node("agent", agent)
graph.add_edge("agent", END)
graph.set_entry_point("agent")
app = graph.compile()

# Step 5: Run it!
response = app.invoke({"messages": ["Add 5 and 3"]})
print(response["messages"][-1].content)
```

**Try It!**

- Run it. It should say something like: "8" or explain the tool call.
- Try "Add 10 and 20". Does it work?

**Why It's Cool:** Tools + LangGraph = AI that can act, not just chat. LangGraph adds flow control, making it super flexible.

---

## Putting It All Together: A Mini Chatbot
Let's combine everything into a tiny chatbot with memory, tools, and agent-like smarts!

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END

# Memory
memory = ChatMessageHistory()

# Tool
@tool
def shout(text: str):
    "Shouts your text"
    return text.upper() + "!!!"

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a fun assistant with memory and tools!"),
    ("human", "{input}")
])

# AI with tools
llm = ChatOpenAI(model="gpt-3.5-turbo").bind_tools([shout])
chain = prompt | llm

# LangGraph setup
class State(dict):
    messages = []

graph = StateGraph(State)
def agent(state):
    # Add memory to state
    state["messages"] = memory.messages + [state["messages"][0]]
    response = chain.invoke({"input": state["messages"][-1].content})
    memory.add_ai_message(response.content)
    state["messages"].append(response)
    return state

graph.add_node("agent", agent)
graph.add_edge("agent", END)
graph.set_entry_point("agent")
app = graph.compile()

# Chat!
response = app.invoke({"messages": ["Hi, I'm Zoe!"]})
print(response["messages"][-1].content)
response = app.invoke({"messages": ["Shout my name!"]})
print(response["messages"][-1].content)
```

**Try It!**

- Run it. First output: "Hi Zoe, nice to meet you!" Second: "ZOE!!!"
- Ask: "What's my name?" See if it remembers!

**Why It's Cool:** You've got memory, tools, and a smart flow—all in one!

---

## Recap (Quick Bites!)
- **Chains:** Stack prompts + AI. Simple, fast.
- **Memory:** Sticky notes for AI. Remembers stuff.
- **Agents:** Thinkers that choose actions. Smarter than chains.
- **Tools:** Gadgets for AI. Do more than talk.

**Next Steps:**

- Add real tools (e.g., web search with `langchain_community.tools.tavily_search`).
- Play with LangGraph's loops for fancier flows!

<br>
