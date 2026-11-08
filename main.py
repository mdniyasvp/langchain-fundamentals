
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# 1. Create prompt template
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an experienced AI engineer. "
        "Explain technical concepts clearly with examples."
    ),
    (
        "human",
        "Explain {topic} at {level} level."
    )
])

# 2. Initialize local chat model
model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

# 3. Create output parser
output_parser = StrOutputParser()

# 4. Build LCEL chain
chain = prompt | model | output_parser



# 5. Execute chain
try:
    #experiment A: invoke()
    """response = chain.invoke({
        "topic": "Neural Networks",
        "level": "intermediate"
    })
    print("\nAI RESPONSE:\n")
    print(response)"""

    #Experiment B:batch()
    """inputs = [
        {"topic": "RAG", "level": "beginner"},
        {"topic": "LoRA", "level": "intermediate"},
        {"topic": "Transformers", "level": "advanced"}
    ]

    responses = chain.batch(inputs)

    for i, response in enumerate(responses, start=1):
        print(f"\n--- RESPONSE {i} ---")
        print(response)"""
    #Experiment C: stream()
    """for chunk in chain.stream({
        "topic": "Large Language Models",
        "level": "intermediate"
    }):
        print(chunk, end="", flush=True)"""

    topic = input("Enter a technical topic: ")
    level = input("Enter difficulty level: ")

    response = chain.invoke({
        "topic": topic,
        "level": level
    })

    print("\nAI RESPONSE:\n")
    print(response)

except Exception as e:
    print(f"Error executing chain: {e}")
