
from langchain_core.tools import tool

from ai_agent.tools.schemas import SearchResult, SearchItem


KNOWLEDGE_BASE = {
    "rag": (
        "Retrieval-Augmented Generation (RAG) combines "
        "information retrieval with language generation. "
        "It retrieves relevant external information and "
        "provides it as context to an LLM."
    ),

    "lora": (
        "Low-Rank Adaptation (LoRA) is a parameter-efficient "
        "fine-tuning technique. It introduces trainable "
        "low-rank matrices while keeping most original "
        "model parameters frozen."
    ),

    "transformers": (
        "Transformers are neural network architectures "
        "based on attention mechanisms. They are widely "
        "used in NLP and modern large language models."
    ),

    "langchain": (
        "LangChain is a framework for building applications "
        "powered by large language models. It provides "
        "components for prompts, models, tools, agents "
        "and retrieval workflows."
    )
}


@tool
def search_knowledge(query: str) -> str:
    """
    Search the local knowledge base for supported AI topics.
    """

    query_lower = query.lower()

    results = []

    for topic, content in KNOWLEDGE_BASE.items():

        if topic in query_lower:

            results.append(
                SearchItem(
                    topic=topic,
                    content=content
                )
            )

    if results:

        response = SearchResult(
            status="success",
            query=query,
            results=results
        )

    else:

        response = SearchResult(
            status="no_results",
            query=query,
            results=[]
        )

    return response.model_dump_json(indent=2)
