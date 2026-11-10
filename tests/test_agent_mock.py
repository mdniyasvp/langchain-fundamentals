
from unittest.mock import patch

from ai_agent.agent.runner import run_agent


class FakeAgent:
    def __init__(self, response):
        self.response = response
        self.called = False

    def invoke(self, *args, **kwargs):
        self.called = True
        return self.response


def test_agent_returns_final_response():
    fake_agent = FakeAgent({
        "messages": [
            type(
                "FakeMessage",
                (),
                {
                    "name": None,
                    "content": "Hello! How can I help you?"
                }
            )()
        ]
    })

    with patch(
        "ai_agent.agent.runner.build_agent",
        return_value=fake_agent
    ):
        response = run_agent("Say hello")

    assert response == "Hello! How can I help you?"
    assert fake_agent.called is True


def test_agent_without_tools_returns_final_response():
    expected = "I can help explain machine learning."

    fake_agent = FakeAgent({
        "messages": [
            type(
                "FakeMessage",
                (),
                {
                    "name": None,
                    "content": expected
                }
            )()
        ]
    })

    with patch(
        "ai_agent.agent.runner.build_agent",
        return_value=fake_agent
    ):
        response = run_agent("What can you do?")

    assert response == expected


def test_agent_receives_user_question():
    fake_agent = FakeAgent({
        "messages": [
            type(
                "FakeMessage",
                (),
                {
                    "name": None,
                    "content": "Test response"
                }
            )()
        ]
    })

    with patch(
        "ai_agent.agent.runner.build_agent",
        return_value=fake_agent
    ):
        run_agent("Explain RAG")

    assert fake_agent.called is True
