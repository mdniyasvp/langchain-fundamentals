
from langchain_core.tools import tool

# Small mock knowledge collection
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
    while keeping the original model weights frozen.
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
    Search the local mock knowledge base for
    information about RAG, LoRA, Transformers
    or LangChain.
    """

    query_lower = query.lower()
    results = []
    for keyword, content in KNOWLEDGE_BASE.items():
        if keyword in query_lower:
            results.append(content.strip())

    if not results:
        return (
            "No relevant information found "
            "in the mock knowledge base."
        )

    return "\n\n".join(results)


if __name__ == "__main__":
    result = mock_search.invoke({
        "query": "Explain RAG"
    })
    print(result)
