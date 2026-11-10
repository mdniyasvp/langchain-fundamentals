import json

def validate_agent_response(response):
    """
    Validate the final AI message.
    """

    if not isinstance(response, str):
        return {
            "valid": False,
            "reason": "Response is not a string"
        }

    if not response.strip():
        return {
            "valid": False,
            "reason": "Empty response"
        }

    try:
        parsed = json.loads(response)

        if (
            isinstance(parsed, dict)
            and "name" in parsed
            and "parameters" in parsed
        ):
            return {
                "valid": False,
                "reason": "Malformed tool-call-like response"
            }

    except json.JSONDecodeError:
        pass

    return {
        "valid": True,
        "reason": "Response format accepted"
    }


if __name__ == "__main__":

    examples = [
        "Hello! How can I help you?",
        "",
        '{"name": "", "parameters": {}}',
        "The answer is 100."
    ]

    for example in examples:
        print(validate_agent_response(example))
