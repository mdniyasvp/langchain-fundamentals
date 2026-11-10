
import json
from types import SimpleNamespace
from unittest.mock import patch

from ai_agent.agent.runner import run_agent


class FakeAgent:

    def __init__(self, messages):
        self.messages = messages

    def invoke(self, *args, **kwargs):
        return {"messages": self.messages}


def fake_message(name, content):
    return SimpleNamespace(
        name=name,
        content=content
    )


def execute_with_messages(messages, question="Test question"):

    with patch(
        "ai_agent.agent.runner.build_agent",
        return_value=FakeAgent(messages)
    ):
        return run_agent(question)


def test_invalid_calculator_json():

    messages = [
        fake_message("calculator", "not valid JSON")
    ]

    response = execute_with_messages(messages)

    assert response == "Invalid calculator tool response."


def test_invalid_search_json():

    messages = [
        fake_message("search_knowledge", "not valid JSON")
    ]

    response = execute_with_messages(messages)

    assert response == "Invalid search tool response."


def test_calculator_execution_error():

    error_result = {
        "status": "error",
        "expression": "10 / 0",
        "result": None,
        "error": "division by zero"
    }

    messages = [
        fake_message(
            "calculator",
            json.dumps(error_result)
        )
    ]

    response = execute_with_messages(messages)

    assert "Calculation failed" in response
    assert "division by zero" in response


def test_search_no_results():

    search_result = {
        "status": "no_results",
        "query": "quantum computing",
        "results": []
    }

    messages = [
        fake_message(
            "search_knowledge",
            json.dumps(search_result)
        )
    ]

    response = execute_with_messages(messages)

    assert "couldn't find information" in response.lower()


def test_search_empty_success():

    search_result = {
        "status": "success",
        "query": "RAG",
        "results": []
    }

    messages = [
        fake_message(
            "search_knowledge",
            json.dumps(search_result)
        )
    ]

    response = execute_with_messages(messages)

    assert response == "Invalid search tool response."


def test_calculator_and_failed_search():

    calculator_result = {
        "status": "success",
        "expression": "25 * 4",
        "result": 100,
        "error": None
    }

    search_result = {
        "status": "no_results",
        "query": "quantum computing",
        "results": []
    }

    messages = [
        fake_message(
            "calculator",
            json.dumps(calculator_result)
        ),
        fake_message(
            "search_knowledge",
            json.dumps(search_result)
        )
    ]

    response = execute_with_messages(messages)

    assert "25 * 4 = 100" in response
    assert "No matching information found" in response
