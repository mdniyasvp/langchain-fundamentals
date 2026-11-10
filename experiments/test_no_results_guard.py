
from ai_agent.agent.runner import run_agent


questions = [
    "Explain quantum computing",
    "What is RAG?",
    "Explain LoRA"
]

for question in questions:

    print("\n" + "=" * 60)
    print("QUESTION:", question)
    print("=" * 60)

    response = run_agent(question)

    print("\nRESPONSE:")
    print(response)
