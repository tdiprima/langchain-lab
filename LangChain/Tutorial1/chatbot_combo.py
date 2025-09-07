"""
Putting It All Together: A Mini Chatbot
Combines chains, memory, and tools into a mini chatbot.
"""

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()


@tool
def shout(text: str):
    """Shouts your text"""
    return text.upper() + "!!!"


@tool
def whisper(text: str):
    """Whispers your text"""
    return text.lower() + "..."


# Create a list of tools
tools = [shout, whisper]

# Initialize chat history
chat_history = ChatMessageHistory()

# Define the prompt template with memory and system message
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that can shout or whisper messages. Use the shout tool when the user wants emphasis or excitement, and the whisper tool for quiet or secretive messages.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Create the agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    print("Chat with the assistant (type 'quit' to exit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "quit":
            break

        # Get response from agent
        response = agent_executor.invoke(
            {"input": user_input, "chat_history": chat_history.messages}
        )

        # Add messages to chat history
        chat_history.add_message(HumanMessage(content=user_input))
        chat_history.add_message(AIMessage(content=response["output"]))

        print("Assistant:", response["output"])

"""
Hi, I'm Zelda!
Please shout my name.
quit
"""
