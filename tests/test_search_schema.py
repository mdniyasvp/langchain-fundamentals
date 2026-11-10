
import pytest

from pydantic import ValidationError

from ai_agent.tools.search import search_knowledge
from ai_agent.tools.schemas import SearchResult


def test_successful_search_schema():

    raw = search_knowledge.invoke({
        "query": "What is RAG?"
    })

    result = SearchResult.model_validate_json(raw)

    assert result.status == "success"
    assert result.query == "What is RAG?"
    assert result.results[0].topic == "rag"


def test_unsupported_search_schema():

    raw = search_knowledge.invoke({
        "query": "Explain quantum computing"
    })

    result = SearchResult.model_validate_json(raw)

    assert result.status == "no_results"
    assert result.results == []


def test_invalid_search_status():

    with pytest.raises(ValidationError):

        SearchResult(
            status="invalid",
            query="RAG",
            results=[]
        )


def test_search_result_content():

    raw = search_knowledge.invoke({
        "query": "Explain LoRA"
    })

    result = SearchResult.model_validate_json(raw)

    assert len(result.results) == 1
    assert "parameter-efficient" in (
        result.results[0].content
    )
