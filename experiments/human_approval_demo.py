from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_ollama import ChatOllama

from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command


# 1. Create a simulated sensitive tool
@tool
def delete_customer_record(customer_id: str) -> str:
    """Delete a customer record. This is a simulated operation."""

    print(f"\nEXECUTING DELETE for {customer_id}")

    # Simulation only: no actual deletion
    return f"Customer record {customer_id} deleted successfully."


# 2. Initialize local model
model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# 3. Configure human approval middleware
approval_middleware = HumanInTheLoopMiddleware(
    interrupt_on={
        "delete_customer_record": True
    }
)


# 4. Create agent with checkpointing
agent = create_agent(
    model=model,
    tools=[delete_customer_record],
    middleware=[approval_middleware],
    checkpointer=InMemorySaver(),
    system_prompt="""
    You are a customer management assistant.

    When the user requests deletion, use the
    delete_customer_record tool.

    Never claim that a record was deleted unless
    the tool actually executes successfully.
    """
)


# 5. Give this execution a unique thread ID
config = {
    "configurable": {
        "thread_id": "customer-delete-demo-001"
    }
}


# 6. Invoke the agent
question = "Delete customer record CUST100."

print("\nUSER REQUEST:")
print(question)

result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": question}
        ]
    },
    config=config
)


# 7. Check whether approval is required
interrupts = result.get("__interrupt__", ())

if interrupts:

    print("\nHUMAN APPROVAL REQUIRED")
    for item in interrupts:
        print(item.value)

    decision = input(
        "\nApprove deletion? (yes/no): "
    ).strip().lower()

    if decision == "yes":
        human_decision = {
            "type": "approve"
        }
    else:
        human_decision = {
            "type": "reject",
            "message": "Deletion rejected by human reviewer."
        }

    # 8. Resume the paused agent
    result = agent.invoke(
        Command(
            resume={
                "decisions": [human_decision]
            }
        ),
        config=config
    )

    print("\nWORKFLOW RESUMED")

else:
    print("\nNo approval interrupt was returned.")


# 9. Display final response
print("\nFINAL RESPONSE:")

for message in result["messages"]:
    if message.type == "ai" and message.content:
        print(message.content)