import json

from ai_agent.tools.search import search_knowledge


test_queries = [
    "What is RAG?",
    "Explain LoRA",
    "What are Transformers?",
    "What is LangChain?",
    "Explain quantum computing"
]

for query in test_queries:

    result = search_knowledge.invoke({
        "query": query
    })

    data = json.loads(result)

    print("\nQUESTION:", query)
    print("STATUS:", data["status"])

    for item in data["results"]:
        print("TOPIC:", item["topic"])
        print("CONTENT:", item["content"])