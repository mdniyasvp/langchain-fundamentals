from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.errors import GraphRecursionError

from experiments.calculator_tool import calculator
from experiments.search_tool import mock_search


# Initialize the local model
model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

# Register tools
tools = [calculator, mock_search]

# Create agent
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
    You are a helpful technical assistant.

    Use the calculator for mathematical calculations.
    Use mock_search when the user asks about supported technical topics.
    Provide a final answer based on tool results.
    """
)

question = "Explain RAG and calculate 125 * 48."

try:
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": question}
            ]
        },
        config={
            "recursion_limit": 2
        }
    )

    print("\nFINAL RESPONSE:")
    print(result["messages"][-1].content)

except GraphRecursionError:
    print("\nERROR: Agent reached the recursion limit.")
    print("Execution stopped before the agent completed its workflow.")