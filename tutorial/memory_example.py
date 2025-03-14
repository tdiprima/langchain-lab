from langchain_openai import OpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Initialize the LLM
llm = OpenAI(temperature=0)

# Create an in-memory chat history store
chat_history_store = {}  # Dictionary to store session histories


# Function to get or create chat history for a session
def get_chat_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in chat_history_store:
        chat_history_store[session_id] = InMemoryChatMessageHistory()
    return chat_history_store[session_id]


# Define a prompt template that includes history and input
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant. Use the conversation history to answer questions."),
    MessagesPlaceholder(variable_name="history"),  # Placeholder for chat history
    ("human", "{input}")  # User's input
])

# Create a chain with prompt and LLM
chain = prompt | llm

# Wrap the chain with message history
conversation = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_chat_history,
    input_messages_key="input",  # Key for the input message
    history_messages_key="history"  # Key for the history messages
)

# Simulate a conversation with a session ID
session_id = "user_bear_session"
config = {"configurable": {"session_id": session_id}}

# First message
print("User: Hi, my name is Bear.")
reply = conversation.invoke({"input": "Hi, my name is Bear."}, config=config)
print(f"Assistant: {reply}")

# Second message
print("\nUser: What's my name?")
reply = conversation.invoke({"input": "What's my name?"}, config=config)
print(f"Assistant: {reply}")

"""
User: Hi, my name is Bear.
Assistant:  Hello Bear, it's nice to meet you! My name is AI and I am an artificial intelligence designed to assist and communicate with humans. I am constantly learning and evolving, so I may not have all the answers, but I will do my best to help you. What can I assist you with today?

User: What's my name?
Assistant:  Your name is Bear. I know this because you introduced yourself as such at the beginning of our conversation. Is there anything else you would like to know about yourself?
"""
