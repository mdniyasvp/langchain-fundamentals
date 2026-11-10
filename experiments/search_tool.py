
import json

from langchain_core.tools import tool

KNOWLEDGE_BASE = {
    "rag": """
    Retrieval-Augmented Generation (RAG) combines
    information retrieval with generative AI.

    It retrieves relevant information from external
    knowledge sources and supplies it to an LLM
    to generate context-aware responses.
    """,

    "lora": """
    LoRA stands for Low-Rank Adaptation.

    It is a parameter-efficient fine-tuning technique
    that introduces trainable low-rank matrices
    while keeping original model weights frozen.
    """,

    "transformers": """
    Transformers are neural network architectures
    based on attention mechanisms.

    They are widely used in modern NLP and LLMs.
    """,

    "langchain": """
    LangChain is a framework for developing
    applications powered by language models.

    It provides components for prompts, models,
    tools, retrieval and agent workflows.
    """
}

@tool
def mock_search(query: str) -> str:
    """
    Search the local knowledge base for a specific
    topic explicitly requested by the user.

    Supported topics:
    - RAG
    - LoRA
    - Transformers
    - LangChain

    Do not use this tool for greetings, casual
    conversation or unrelated questions.

    The query should contain the actual topic
    requested by the user, not this tool description.
    """

    query_lower = query.lower()

    results = []

    for keyword, content in KNOWLEDGE_BASE.items():

        if keyword in query_lower:
            results.append({
                "topic": keyword,
                "content": content.strip()
            })

    if not results:
        return json.dumps({
            "status": "no_results",
            "query": query,
            "results": []
        })

    return json.dumps({
        "status": "success",
        "query": query,
        "results": results
    }, indent=2)


if __name__ == "__main__":

    print(mock_search.invoke({
        "query": "Explain RAG"
    }))
