
from ai_agent.agent.factory import build_agent


agent = build_agent()

question = (
    "Calculate 100 + 200 * 3 "
    "and explain what RAG means."
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    },
    config={"recursion_limit": 12}
)

print("\nQUESTION:")
print(question)

print("\nEXECUTION TRACE:")

for message in result["messages"]:

    print("\nMESSAGE TYPE:", type(message).__name__)

    if getattr(message, "tool_calls", None):
        print("TOOL CALLS:")

        for tool_call in message.tool_calls:
            print("Tool:", tool_call["name"])
            print("Arguments:", tool_call["args"])

    if getattr(message, "name", None):
        print("TOOL NAME:", message.name)

    if message.content:
        print("CONTENT:", message.content)

print("\nFINAL RESPONSE:")
print(result["messages"][-1].content)
