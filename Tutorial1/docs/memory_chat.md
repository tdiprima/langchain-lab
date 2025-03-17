In this implementation, the `ConversationBufferMemory` is automatically handling the chat history for us. When we use `ConversationChain`, it:

1. Takes the user input
2. Combines it with the history stored in memory
3. Sends it to the LLM
4. Automatically saves the new interaction (both the input and response) to memory

The `ConversationBufferMemory` class handles all of this behind the scenes, which is why we don't need to manually manage the chat history like we did in other examples.

This is one of the nice features of using `ConversationChain` - it integrates the memory management automatically. Each time you make a request:

1. The memory is retrieved
2. Added to the prompt
3. he new interaction is stored
4. And it's all ready for the next interaction

That's why we didn't need to explicitly pass a `chat_history` parameter - the `ConversationChain` handles all that for us!

```python
memory = ConversationBufferMemory()

chain = ConversationChain(
    llm=llm,
    memory=memory
)

response = chain.invoke({"input": user_input})
```

# 🆚

```py
response = agent_executor.invoke({"input": user_input, "chat_history": chat_history})
```

<br>
