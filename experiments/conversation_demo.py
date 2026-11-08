
from langchain_ollama import ChatOllama
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

# Initial conversation
messages = [
    SystemMessage(
        content="You are an experienced GenAI engineer."
    )
]

# First question
messages.append(
    HumanMessage(content="What is RAG?")
)

response1 = model.invoke(messages)

print("AI:", response1.content)

# Save AI response in conversation history
messages.append(response1)

# Second question
messages.append(
    HumanMessage(content="What are its advantages?")
)

response2 = model.invoke(messages)

print("\nAI:", response2.content)
