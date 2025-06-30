# LangChain Tutorial  🎉

LangChain is a framework that helps you build powerful applications with large language models (LLMs). It provides **core components** like Chains, Memory, Agents, Tools, and integrated Models to make LLMs more effective. Using an LLM by itself is cool, but the real power comes when you combine it with other sources of computation or knowledge ([langchain · PyPI](https://pypi.org/project/langchain/#:~:text=Large%20language%20models%20,sources%20of%20computation%20or%20knowledge)). LangChain makes that easier by giving you building blocks to structure prompts, remember context, call external APIs, and more.

**In this tutorial**, we'll cover the core concepts of LangChain **version 0.3.20** in a beginner-friendly way. We'll use short explanations, bullet points, and fully runnable Python examples. By the end, you'll know how to:

- **Install and set up LangChain** on your system.
- Use **Chains** to create sequences of calls (like prompts to an LLM).
- Use **Memory** to maintain context across interactions (so the AI remembers what was said).
- Use **Agents** to let an LLM decide which actions or tools to use.
- Integrate **Tools** (external functions/APIs) that an agent can use.
- Work with different **Models** in LangChain (switch between OpenAI, HuggingFace, etc).

Let's get started! 😊

## Setup and Installation

Before coding, make sure you have Python installed (Python 3.7+). Then install LangChain and the necessary dependencies:

1. **Create a virtual environment (optional)** – This keeps your project's libraries isolated. You can skip this, but it's good practice. For example:  

   ```bash
   python -m venv venv 
   source venv/bin/activate  # On Windows use "venv\\Scripts\\activate"
   ```

2. **Install LangChain v0.3.20 and dependencies** – Use pip to install the specific LangChain version and other libraries we'll use (like OpenAI API and HuggingFace for models):  

   ```bash
   pip install langchain==0.3.20 openai transformers
   ``` 

   *This will install LangChain 0.3.20, the OpenAI client, and HuggingFace Transformers.* 
3. **Get an OpenAI API Key** – Many examples use OpenAI's GPT-3. You'll need an API key from OpenAI (sign up at their website if you haven't). Once you have it, set it as an environment variable in your system, for example:  
   **On Linux/macOS:** `export OPENAI_API_KEY="YOUR-KEY-HERE"`  
   **On Windows (Powershell):** `$Env:OPENAI_API_KEY="YOUR-KEY-HERE"`  
   Or, you can set it in Python code as shown below. **Keep your key private!**

Now you're ready to use LangChain. Let's go through each core component with examples.

## 1. Chains

**What is a Chain?** In LangChain, a *Chain* is a sequence of steps or calls that can include LLMs, prompts, other chains, or utilities. Instead of a single LLM call, you can chain together a series of operations. For example, you might format user input with a prompt template, call an LLM, then post-process the result – all of that can be one chain. Chains allow you to **orchestrate complex tasks** by combining simple components in order.

Key points about Chains:

- A Chain can be as simple as "take user input, plug into a prompt, get LLM output" or as complex as a multi-step workflow.
- Chains have a standard interface: you input something and get an output. Under the hood, it might call multiple functions or LLMs.
- LangChain provides many ready-made chains (for common tasks like Q&A, summarization) and the ability to create custom chains.

**Why use Chains?** They let you reuse and organize sequences of actions. In a chain, the sequence of actions is predetermined/hardcoded in code ([Agents | LangChain](https://python.langchain.com/v0.1/docs/modules/agents/#:~:text=The%20core%20idea%20of%20agents,take%20and%20in%20which%20order)), which makes the outcome more predictable than letting an AI decide the flow (that's what Agents do, which we'll cover later). Use a chain when you know the steps you want to take every time.

### Creating and Running a Simple Chain

Let's create a simple chain that asks an LLM to generate a personalized greeting. We'll use an **LLMChain**, which is a basic chain that formats a prompt and calls an LLM. This example will use OpenAI's text model (e.g. GPT-3) for simplicity.

```python
# chains_example.py

# 1. Import necessary classes
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
import os

# 2. Set your OpenAI API key (if not set as environment variable already)
os.environ["OPENAI_API_KEY"] = "YOUR-OPENAI-API-KEY-HERE"

# 3. Create a prompt template. This is the blueprint of the prompt the LLM will see.
template = "You are a friendly assistant. Respond to the user by name.\nUser: {user_input}\nAssistant:"
prompt = PromptTemplate(template=template, input_variables=["user_input"])

# 4. Initialize the LLM (OpenAI GPT-3 in this case)
llm = OpenAI(temperature=0.7)  # temperature=0.7 for a bit of creativity in the output

# 5. Create the chain by combining the prompt and the LLM
chain = LLMChain(prompt=prompt, llm=llm)

# 6. Run the chain with some input
user_name = "Alex"
question = f"My name is {user_name}. Can you greet me?"
response = chain.run(user_input=question)

print(response)
```

**What does this code do?**  

- We define a `PromptTemplate` with a placeholder `{user_input}`. This template instructs the AI to be friendly and use the user's name in the response.
- We create an `OpenAI` LLM instance (this will use the OpenAI API under the hood). We set a `temperature` for randomness.
- We create an `LLMChain` that ties the prompt template and the LLM together.
- Finally, we run the chain by providing `user_input`. The chain fills the template with the input and calls the LLM. The result is stored in `response`.

If you run the above script, you should see the AI's greeting, for example: 

```
Hello Alex! It's nice to meet you. How can I help you today?
```

*Feel free to change `user_name` or the prompt template and run again.* The chain will consistently apply the prompt formatting and call the model.

Chains can be more complex (like multiple steps or branching logic), but this simple example shows the core idea: **structure the interaction with the LLM in a reusable way**.

## 2. Memory

**What is Memory?** Memory in LangChain is how your application **remembers previous interactions**. By default, LLMs don't recall earlier conversation turns (each call is independent). Memory modules keep track of messages or important information and feed them into the prompt of subsequent LLM calls, giving the illusion of a persistent conversation or context.

For example, if a user says "My name is Bob" and later asks "What's my name?", a memory can store that info so the LLM can answer correctly. Memory is especially useful for chatbots or multi-turn conversations.

Key points about Memory:

- **ConversationBufferMemory**: Remembers all conversation history (just stores all messages).
- **ConversationSummaryMemory**: Remembers a summarized version of the conversation (to save space).
- **ConversationBufferWindowMemory**: Remembers only the latest _N_ messages.
- Memory can be attached to Chains or Agents to carry info across calls.
- Using memory makes the interaction more dynamic and context-aware.

### Using Memory to Remember Context

Let's demonstrate memory by creating a conversational chain that remembers what was said. We'll use `ConversationBufferMemory`, which just accumulates chat history. We'll attach it to a simple conversation chain.

```python
# memory_example.py

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "YOUR-OPENAI-API-KEY-HERE"

# Initialize the conversation memory
memory = ConversationBufferMemory()  # this will store conversation history

# Initialize the LLM (OpenAI model)
llm = OpenAI(temperature=0)

# Create a ConversationChain with the LLM and the memory
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

# Simulate a conversation:
print("User: Hi, my name is Sam.")
reply = conversation.predict(input="Hi, my name is Sam.")
print(f"Assistant: {reply}")

print("\nUser: What's my name?")
reply = conversation.predict(input="What's my name?")
print(f"Assistant: {reply}")
```

**Explanation:** We use `ConversationChain` which is a ready-made chain for conversations. By giving it a `ConversationBufferMemory`, it will automatically append each user message and assistant response to the memory. When we call `conversation.predict()`, LangChain will build a prompt that includes the conversation history from memory.

- In the first user prompt, we introduce ourselves as "Sam". The assistant might reply with a greeting.
- In the second prompt, we ask **"What's my name?"**. Because we have memory, the chain will include the fact `"User: Hi, my name is Sam."` in the prompt for this question. The LLM can then answer correctly: e.g. **"Your name is Sam."**

Run the script and you should see something like:

```
User: Hi, my name is Sam.
Assistant: Hello Sam! Nice to meet you. How can I assist you today?

User: What's my name?
Assistant: You just mentioned your name is Sam.
```

Notice that the assistant remembers the name **Sam** from the earlier interaction, even though the second prompt didn't repeat it. Without memory, the model might not know who "you" refers to. Memory makes it possible to maintain context across turns.

You can keep calling `conversation.predict(input=...)` and the memory will keep growing with the conversation. This is the basis for building stateful chatbots or assistants using LangChain.

*📝 Tip: Think of memory like a chat transcript that gets prepended to each new question. It helps the AI not to forget things mentioned earlier.* 

## 3. Agents

**What is an Agent?** An *Agent* is a powerful concept in LangChain where an LLM is not just generating a direct answer, but instead **deciding a sequence of actions** to take based on the user's request ([Agents | LangChain](https://python.langchain.com/v0.1/docs/modules/agents/#:~:text=The%20core%20idea%20of%20agents,take%20and%20in%20which%20order)). An agent can choose from a set of Tools (functions or actions) to help answer a question or fulfill a task. It uses the LLM as a reasoning engine to figure out *which* tool to use, *what* input to give that tool, and *when* to stop and return an answer.

In simpler terms, **an agent = LLM + decision-making + tools.** The agent will dynamically determine the steps. This is different from a Chain where the steps are fixed in code. Use an agent when you want the AI to handle more open-ended problems that might involve multiple steps or external actions (e.g. searching the web, doing math, looking up info).

Key points about Agents:

- Agents have access to one or more Tools (we'll explain Tools next). For example, a calculator, a search engine, a database, etc.
- On each turn, the agent (the LLM behind it) receives the user question plus a list of available tools and decides:
    1. Should I use a tool? If yes, which one and with what input?
    2. Or, have I gathered enough info and I should answer now?
- The agent's reasoning is often based on a prompt (LangChain uses a ReAct framework prompt by default) which encourages the model to think step-by-step (sometimes you'll see it output "Thought: ... Action: ..." behind the scenes).
- **When to use**: If your task might require looking up information or performing intermediate calculations, agents are great. If the task is straightforward and one-step (just text in -> text out), a chain might suffice.

### Example: Math Problem Solving Agent

To illustrate agents, let's create one that can do math by using a calculator tool. Language models are notoriously bad at arithmetic, so giving the agent a calculation tool is helpful. We'll use LangChain's built-in **LLM Math tool** which lets the agent do math. 

In this example, the agent will figure out it needs to use the calculator to answer a math question.

```python
# agents_example.py

from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent

import os
os.environ["OPENAI_API_KEY"] = "YOUR-OPENAI-API-KEY-HERE"

# Initialize the LLM for the agent (we'll use the same OpenAI GPT-3 model)
llm = OpenAI(temperature=0)

# Load the tools the agent can use. We'll give it a calculator tool (LLM math).
tools = load_tools(["llm-math"], llm=llm)
# "llm-math" is a built-in tool that uses the LLM plus python for math.

# Initialize the agent with the tools and LLM.
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Ask a math question
query = "What is 2 raised to the 5th power, divided by 7?"
result = agent.run(query)
print(f"Final Answer: {result}")
```

**What's happening here?**  

- We loaded an OpenAI LLM with `temperature=0` to make it deterministic (for reliable reasoning).
- We used `load_tools(["llm-math"], llm=llm)` to get a calculator-like tool. The `"llm-math"` tool is basically a combination of an LLM and a Python evaluator: the agent can use it to do calculations.
- We initialized an agent with `initialize_agent`. We specify the agent type `"zero-shot-react-description"` which is a standard agent that uses the ReAct framework (Reason+Act) with no examples (zero-shot).
- `verbose=True` will print the agent's thought process (which is super useful to see what's going on under the hood).

When you run this, the console output will show the **agent's reasoning steps** because we set verbose mode. It might look something like:

```
> Entering new AgentExecutor chain...
 I should use a calculator to solve this problem.
Action: Calculator
Action Input: 2 ** 5 / 7
Observation: Answer: 4.571428571428571
Thought: I now know the final answer.
Final Answer: 4.571428571428571

> Finished chain.
Final Answer: 4.571428571428571
```

*(The exact format may vary, but the idea is the agent thought "I should use the calculator", then used it, then got the result and answered.)*

The final printed answer should be `4.571428571428571`. 

Notice how the agent **decided** to use the Calculator tool for the math, rather than trying to do it by itself (which an LLM might get wrong). The LLM's role here is to *choose actions* and then form the final answer. 

You could give the agent other tools (like a Wikipedia search tool) and it could then decide to search for answers to general knowledge questions. Agents shine in scenarios where the solution requires multiple steps or external information retrieval.

*In summary:* Agents = give the AI some tools and let it figure out how to solve the problem by possibly using those tools. It's like giving the AI a toolbox and the autonomy to decide which tool to pick.

## 4. Tools

We've mentioned Tools a lot – they are essential for Agents. Let's dig a bit deeper.

**What are Tools?** In LangChain, a *Tool* is essentially a function (or an external utility) that the LLM agent can use. Each tool has:

- A **name** (how the agent references it),
- A **description** (so the agent knows when to use it),
- A **function to execute** (this does the actual work, e.g. perform a calculation, call an API, etc.).

Tools can be anything from calculators, web search, databases, to your own custom functions or APIs. They allow the LLM to do more than just generate text – it can take actions like looking up information or transforming data.

**When do you use Tools?** Typically inside an Agent. You give the agent a list of tools it's allowed to use. The agent's prompt (system message) will include each tool's name and description. This way the LLM knows what capabilities it has. When the user asks something that requires one of those capabilities, the agent can invoke the tool.

LangChain comes with many pre-built tools (for example: `serpapi` for web search, `llm-math` for math, `wolfram-alpha` for advanced math, `python_repl` for running Python code, etc.). You can also integrate external APIs (like weather APIs, database queries) by wrapping them as tools.

### Creating a Custom Tool

Let's create a custom tool to demonstrate how to integrate an external function. Suppose we want the agent to be able to tell the current time (something an LLM alone doesn't know). We'll create a tool that returns the current time. This simulates integrating an external API (in this case, the system clock).

```python
# tools_example.py

from langchain.llms import OpenAI
from langchain.agents import Tool, initialize_agent
from datetime import datetime
import os

os.environ["OPENAI_API_KEY"] = "YOUR-OPENAI-API-KEY-HERE"

# Define a simple function to get current time
def get_current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")

# Create a Tool for the function
time_tool = Tool(
    name="Current Time",
    func=get_current_time,
    description="Provides the current time in HH:MM:SS format."
)

# Set up the LLM and agent with this tool
llm = OpenAI(temperature=0)
tools = [time_tool]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Ask the agent a question that requires the tool
question = "What time is it right now?"
response = agent.run(question)
print(f"Agent's answer: {response}")
```

**Explanation:** We created a Python function `get_current_time` that returns the current time as a string. Then we wrapped it in `Tool(...)` giving it a name and description. The agent will see *"Current Time: Provides the current time in HH:MM:SS format."* in its prompt, so it knows this tool can give the time.

When we run the agent on the question *"What time is it right now?"*, here's what happens internally:

- The agent thinks *"I don't know the time, but I have a tool for that."*
- It chooses the **Current Time** tool, calls `get_current_time()` (via `func`).
- The tool returns (say) `"12:48:50"`.
- The agent then uses that to formulate the final answer, e.g. *"It's currently 12:48:50."*

The console (with verbose=True) will show something like:

```
> Entering new AgentExecutor chain...
 I should use the Current Time tool to get the current time
Action: Current Time
Action Input: None
Observation: 12:48:50
Thought: I now know the final answer
Final Answer: The current time is 12:48:50.

> Finished chain.
Agent's answer: The current time is 12:48:50.
```

This demonstrates how to integrate external information via tools. You could similarly wrap an API call (e.g., a weather API) in a function and make it a tool. Then the agent could answer questions like "What's the weather in Paris?" by calling that tool.

**Tips for using tools:**

- Make sure the tool's description clearly tells the AI when to use it. The agent only knows what you tell it about the tool.
- Keep tool inputs/outputs simple (strings are easiest) because the agent communicates with tools via text. If a tool requires a complex input (like multiple parameters), you might need to adjust how the agent prompt is set up.
- Test your tools individually to ensure they work, then integrate into the agent.

## 5. Models

LangChain is **model-agnostic**. This means you can plug in different LLMs or AI models (OpenAI GPT-3, GPT-4, Anthropic's Claude, HuggingFace local models, etc.) without changing your chain/agent logic much. The *Model* in LangChain refers to the LLM or chat model that is doing the heavy lifting of text generation or reasoning.

**Using different models**: LangChain provides wrappers for many providers:

- OpenAI (e.g. `OpenAI` for text models like davinci, `ChatOpenAI` for chat models like GPT-3.5-Turbo),
- Hugging Face (both via online Hub and local pipelines),
- Cohere, AI21, Anthropic, etc.
- You can even use local models via libraries like Transformers or llama.cpp.

The core idea is you instantiate a LangChain LLM object for the model you want, and use it in your chains/agents. For example, if you switch `OpenAI` to `Anthropic()` (with appropriate API keys), the rest of your chain code can remain the same.

Let's see two examples: one with OpenAI's GPT-3 and one with a local HuggingFace model. Both will do a simple task (tell a joke) to illustrate usage.

### Example: Using OpenAI GPT-3

```python
# models_openai_example.py

from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "YOUR-OPENAI-API-KEY-HERE"

# Initialize the OpenAI LLM (text-davinci-003 by default in this version)
openai_llm = OpenAI(temperature=0.9)

prompt = "Tell me a short joke about chickens."
response = openai_llm(prompt)
print(response)
```

Here we simply create an `OpenAI` LLM instance and call it like a function with a prompt string. LangChain's `OpenAI` class is a wrapper that sends the request to OpenAI's API and returns the result. The `temperature=0.9` means the output will be quite random/funny. Running this should print a joke, for example:

```
Why did the chicken join a band? Because it had the drumsticks!
```

You can adjust parameters like `model_name='text-davinci-003'` or `max_tokens=100` if needed (LangChain's OpenAI wrapper has default values, but you can override them). Make sure your API key is set, or you'll get an authentication error.

### Example: Using a HuggingFace Transformers model (locally)

If you don't have an OpenAI key or prefer an open-source model, you can use HuggingFace models. LangChain's `HuggingFacePipeline` allows you to use a transformers pipeline as an LLM. Let's use a small model from HuggingFace for demonstration. (Note: The first time you run this, it will download the model weights, which can take time.)

```python
# models_huggingface_example.py

from transformers import pipeline
from langchain.llms import HuggingFacePipeline

# Load a text-generation pipeline from HuggingFace (using a small model)
local_pipeline = pipeline("text-generation", model="distilgpt2", max_new_tokens=50)
# Wrap the pipeline in a LangChain LLM
local_llm = HuggingFacePipeline(pipeline=local_pipeline)

# Use the local model to get a joke (distilgpt2 is not instruction-tuned, so it might just continue text)
prompt = "Tell me a short joke about chickens."
response = local_llm(prompt)
print(response)
```

Here we chose **DistilGPT-2** (a small distilled GPT-2 model) for speed. This model isn't trained to follow instructions perfectly, so the output might be a bit incoherent or just a continuation of the prompt. For example, it might output something like:

```
...chickens. The farmer said, "Looks like they're on a peck-nic!"
```

Don't worry if the joke isn't great – the point is that we successfully switched to a local model! 🎉 

If you want better results, you could try an instruction-following model such as `google/flan-t5-small` in a text2text generation pipeline, or a larger model if you have the resources. For instance:

```python
# Using an instruction-tuned model (Flan-T5) instead
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
model_name = "google/flan-t5-small"
pipe = pipeline("text2text-generation", model=model_name, tokenizer=model_name, max_new_tokens=50)
local_llm = HuggingFacePipeline(pipeline=pipe)
print(local_llm("Tell me a short joke about chickens."))
```

Flan-T5 is more likely to obey the instruction and produce a direct answer.

**Important:** When using HuggingFace models, you might need to install additional packages or ensure you have the model files. We used the Transformers pipeline which handles downloading for us. Also, local models run on your hardware (CPU/GPU), so performance will vary.

### Switching models in a Chain/Agent

You can plug these models into the chains or agents we built earlier. For example, to use a local model in our greeting chain, you'd do:

```python
llm = HuggingFacePipeline(pipeline=local_pipeline)
chain = LLMChain(prompt=prompt, llm=llm)

```
Everything else remains the same. This interchangeable design means you can prototype with a cheap local model and then switch to a more powerful one (like GPT-4) for production, or vice versa.

## Conclusion

In this tutorial, we covered the core components of LangChain:

- **Chains**: predefined sequences of steps, great for predictable workflows.
- **Memory**: add state to your chains/agents so they remember previous interactions (crucial for conversations).
- **Agents**: give your LLM the ability to decide actions and use tools, enabling more complex, interactive behavior.
- **Tools**: the actual functions or APIs an agent can use to perform tasks (from simple math to web searches or database queries).
- **Models**: different LLMs (OpenAI, HuggingFace, etc.) that LangChain can work with interchangeably.

Each section included a runnable example. You can mix and match these components to build rich applications. For instance, a chatbot might be an Agent with memory enabled and tools for searching information.

**Next steps to try:**

- Modify the examples: add another tool to the agent (maybe a dictionary lookup or a weather API) and see how to prompt the agent to use it.
- Explore LangChain's documentation for other chain types (there are chains for question answering with documents, summarization, etc.).
- Experiment with different models or tweak the prompt templates to see their effect.
- Use an agent to combine multiple tools (e.g., search + calculator) and solve more elaborate queries.

LangChain is a robust framework, but you've now seen the basics of how to use it effectively. Keep prompts clear, decide when you need memory or an agent, and have fun building with LLMs! 

Happy coding! 🎊

<br>
