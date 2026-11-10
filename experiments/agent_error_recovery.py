from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.errors import GraphRecursionError


# 1. Create a tool that can fail
@tool
def divide_numbers(a: float, b: float) -> float:
    """Divide the first number by the second number."""

    if b == 0:
        raise ValueError("Division by zero is not allowed.")

    return a / b


# 2. Intercept tool execution errors
@wrap_tool_call
def handle_tool_errors(request, handler):
    try:
        return handler(request)

    except (ValueError, ZeroDivisionError) as error:
        print(f"\nTOOL ERROR CAUGHT: {error}")

        return ToolMessage(
            content=(
                f"Tool execution failed: {error}. "
                "Do not invent a calculation result. "
                "Explain the error to the user."
            ),
            tool_call_id=request.tool_call["id"]
        )


# 3. Initialize model
model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# 4. Create agent with middleware
agent = create_agent(
    model=model,
    tools=[divide_numbers],
    middleware=[handle_tool_errors],
    system_prompt="""
    You are a mathematical assistant.

    Use divide_numbers for division.
    If a tool reports an error, never fabricate a result.
    Explain the error clearly.
    """
)


# 5. Execute agent
question = "Use the division tool to calculate 100 divided by 0."

try:
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": question}
            ]
        },
        config={"recursion_limit": 10}
    )

    print("\nFINAL RESPONSE:")
    print(result["messages"][-1].content)

except GraphRecursionError:
    print("\nAGENT ERROR: Recursion limit reached.")

except Exception as error:
    print(f"\nAPPLICATION ERROR: {type(error).__name__}: {error}")