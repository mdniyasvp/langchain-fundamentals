
import json

from ai_agent.tools.search import search_knowledge


def test_rag_search():

    result = search_knowledge.invoke({
        "query": "What is RAG?"
    })

    data = json.loads(result)

    assert data["status"] == "success"
    assert data["results"][0]["topic"] == "rag"


def test_lora_search():

    result = search_knowledge.invoke({
        "query": "Explain LoRA"
    })

    data = json.loads(result)

    assert data["status"] == "success"
    assert data["results"][0]["topic"] == "lora"


def test_unsupported_topic():

    result = search_knowledge.invoke({
        "query": "Explain quantum computing"
    })

    data = json.loads(result)

    assert data["status"] == "no_results"
    assert data["results"] == []


def test_multiple_supported_topics():

    result = search_knowledge.invoke({
        "query": "Explain RAG and LoRA"
    })

    data = json.loads(result)

    assert data["status"] == "success"

    topics = [
        item["topic"]
        for item in data["results"]
    ]

    assert "rag" in topics
    assert "lora" in topics
