from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

import os
api_key = os.getenv("OPENAI_API_KEY")

# Store for chat histories (in-memory for this example)
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Retrieve or create a chat history for the given session."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def create_conversation():
    # Initialize the language model
    llm = ChatOpenAI(temperature=0.7)
    
    # Create a custom prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant with knowledge up to March 2025."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    # Create the runnable chain with history
    chain = prompt | llm
    
    # Wrap the chain with message history
    conversation = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    
    return conversation


def main():
    # Create the conversation instance
    convo = create_conversation()
    session_id = "user_session"  # Simple session ID for this example
    
    # Example conversation loop
    print("Start chatting! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
            
        # Invoke the conversation with the input and session ID
        response = convo.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        print(f"AI: {response.content}")


if __name__ == "__main__":
    main()
