
from pydantic import ValidationError

from ai_agent.agent.factory import build_agent
from ai_agent.tools.schemas import (
    CalculatorResult,
    SearchResult
)


NO_RESULTS_MESSAGE = (
    "I couldn't find information about this topic "
    "in the available knowledge base."
)


def run_agent(question: str) -> str:

    agent = build_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        config={"recursion_limit": 12}
    )

    messages = result["messages"]

    calculator_results = []
    search_results = []

    search_was_called = False

    for message in messages:

        tool_name = getattr(message, "name", None)

        if tool_name == "calculator":

            try:
                data = CalculatorResult.model_validate_json(
                    message.content
                )

            except (ValidationError, TypeError):
                return "Invalid calculator tool response."

            if data.status == "success":

                if data.result is None:
                    return "Calculator returned a missing result."

                calculator_results.append(
                    f"{data.expression} = {data.result:g}"
                )

            else:

                calculator_results.append(
                    f"Calculation failed: {data.error}"
                )

        elif tool_name == "search_knowledge":

            search_was_called = True

            try:
                data = SearchResult.model_validate_json(
                    message.content
                )

            except (ValidationError, TypeError):
                return "Invalid search tool response."

            if data.status == "success":

                if not data.results:
                    return "Search returned an empty success response."

                for item in data.results:

                    search_results.append({
                        "topic": item.topic,
                        "content": item.content
                    })

            elif data.status != "no_results":

                return "Search returned an unrecognized status."

    response_parts = []

    if calculator_results:

        response_parts.append("CALCULATION RESULTS:")

        for calculation in calculator_results:
            response_parts.append(calculation)

    if search_results:

        response_parts.append("\nKNOWLEDGE BASE RESULTS:")

        for item in search_results:

            response_parts.append(
                f"\nTopic: {item['topic']}\n"
                f"{item['content']}"
            )

    if search_was_called and not search_results:

        if not calculator_results:
            return NO_RESULTS_MESSAGE

        response_parts.append(
            "\nKNOWLEDGE BASE: No matching information found."
        )

    if response_parts:
        return "\n".join(response_parts)

    return messages[-1].content
