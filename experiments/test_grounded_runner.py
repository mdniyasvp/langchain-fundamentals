
from ai_agent.agent.runner import run_agent


questions = [
    "Explain RAG",

    "Explain LoRA",

    "Calculate 250 * 48",

    "Calculate 100 + 200 * 3 and explain RAG",

    "Explain quantum computing"
]


for index, question in enumerate(questions, start=1):

    print("\n" + "=" * 60)
    print("TEST:", index)
    print("QUESTION:", question)
    print("=" * 60)

    response = run_agent(question)

    print("\nFINAL RESPONSE:")
    print(response)
