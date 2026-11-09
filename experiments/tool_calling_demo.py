from langchain_ollama import ChatOllama
from experiments.calculator_tool import calculator
from experiments.search_tool import mock_search

model = ChatOllama(model="llama3.2:3b",
                   temperature=0)
tools = [calculator, mock_search]
model_with_tools = model.bind_tools(tools)
questions = [
    "calculate 250 multiplied by 48.",
    "search for information about RAG."
]
for question in questions:
    print("\nUSER:",question)
    response = model_with_tools.invoke(question)
    print("TOOL CALLS:")
    print(response.tool_calls)
    print("NORMAL RESPONSE:")
    print(response.content)