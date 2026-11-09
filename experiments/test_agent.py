
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from experiments.calculator_tool import calculator
from experiments.search_tool import mock_search


model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

tools = [calculator, mock_search]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
    You are a tool-using AI assistant.

    Use calculator for mathematical operations.
    Use mock_search for knowledge retrieval.
    You may use both tools if required.
    Answer simple greetings directly.
    Do not invent tool results.
    """
)


test_cases = [
    "Calculate 25 * 40",
    "What is 100 / 4?",
    "Calculate 2 ** 8",
    "Explain RAG",
    "What is LoRA?",
    "Explain Transformers",
    "What is LangChain?",
    "Search for RAG and calculate 20 * 5",
    "What is 10 + 15?",
    "Hello, how are you?"
]


for index, question in enumerate(test_cases, start=1):

    print("\n" + "=" * 60)
    print(f"TEST CASE {index}")
    print("=" * 60)

    print("QUESTION:", question)

    try:

        result = agent.invoke(
            {
                "messages": [
                    {"role": "user", "content": question}
                ]
            },
            config={"recursion_limit": 12}
        )

        print("\nTOOL EXECUTION:")

        for message in result["messages"]:

            if message.type == "ai" and message.tool_calls:

                for call in message.tool_calls:
                    print("Selected tool:", call["name"])

            elif message.type == "tool":
                print("Tool result:", message.content)

        print("\nFINAL ANSWER:")
        print(result["messages"][-1].content)

    except Exception as error:

        print("TEST FAILED:", error)
