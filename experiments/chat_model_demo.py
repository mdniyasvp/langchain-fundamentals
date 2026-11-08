
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# Initialize model
model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

# Create structured messages
messages = [
    SystemMessage(
        content="You are an experienced GenAI engineer."
    ),
    HumanMessage(
        content="Explain the difference between RAG and fine-tuning."
    )
]

# Invoke model
response = model.invoke(messages)

print("AI RESPONSE:\n")
print(response.content)

print("\nRESPONSE TYPE:")
print(type(response))
