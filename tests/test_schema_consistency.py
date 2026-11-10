
import pytest
from pydantic import ValidationError

from ai_agent.tools.schemas import (
    CalculatorResult,
    SearchResult,
)


def test_calculator_success_requires_result():
    with pytest.raises(ValidationError):
        CalculatorResult(
            status="success",
            expression="25 * 4",
            result=None,
            error=None,
        )


def test_calculator_error_requires_message():
    with pytest.raises(ValidationError):
        CalculatorResult(
            status="error",
            expression="10 / 0",
            result=None,
            error=None,
        )


def test_calculator_success_cannot_have_error():
    with pytest.raises(ValidationError):
        CalculatorResult(
            status="success",
            expression="25 * 4",
            result=100,
            error="Unexpected error",
        )


def test_search_success_requires_results():
    with pytest.raises(ValidationError):
        SearchResult(
            status="success",
            query="RAG",
            results=[],
        )


def test_search_error_requires_message():
    with pytest.raises(ValidationError):
        SearchResult(
            status="error",
            query="RAG",
            results=[],
            error=None,
        )


def test_search_no_results_is_valid():
    result = SearchResult(
        status="no_results",
        query="quantum computing",
        results=[],
    )

    assert result.status == "no_results"
    assert result.results == []


def test_valid_calculator_result():
    result = CalculatorResult(
        status="success",
        expression="25 * 4",
        result=100,
        error=None,
    )

    assert result.result == 100
