
import json
import re

from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from experiments.calculator_tool import calculator
from experiments.search_tool import mock_search


# ============================================================
# 1. CONFIGURATION
# ============================================================

MODEL_NAME = "llama3.2:3b"

model = ChatOllama(
    model=MODEL_NAME,
    temperature=0
)

tools = [
    calculator,
    mock_search
]


# ============================================================
# 2. SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a reliable AI assistant.

AVAILABLE TOOLS:

1. calculator:
   Use for mathematical calculations.

2. mock_search:
   Search the knowledge base for RAG, LoRA,
   Transformers and LangChain.

TOOL SELECTION RULES:

- Use calculator for mathematical operations.
- Use mock_search for supported knowledge topics.
- Never use tools for greetings or casual conversation.
- Use multiple tools when the request contains
  multiple independent tasks.
- Do not call tools unnecessarily.

ERROR HANDLING:

- If calculator returns an error, report the error.
- Never invent or estimate a result after calculation failure.
- If mock_search returns no results, acknowledge this.
- Do not invent missing retrieval results.

ANSWER GENERATION:

- Examine every tool result.
- Address every part of the user's request.
- Combine relevant results from multiple tools.
- Do not ignore successful tool results.
- Do not output raw tool-call JSON.
- Prioritize accuracy and completeness.
"""


# ============================================================
# 3. CREATE AGENT
# ============================================================

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)


# ============================================================
# 4. DETERMINISTIC GREETING ROUTER
# ============================================================

def is_simple_greeting(question: str) -> bool:

    greetings = {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    }

    normalized = question.lower().strip()

    normalized = re.sub(
        r"[!.?,]+$",
        "",
        normalized
    )

    return normalized in greetings


# ============================================================
# 5. FINAL RESPONSE VALIDATION
# ============================================================

def validate_response(response: str) -> dict:

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
            and (
                "name" in parsed
                or "parameters" in parsed
            )
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


# ============================================================
# 6. TEST CASES
# ============================================================

test_cases = [

    # Calculator tests
    "Calculate 25 * 40",

    "What is 100 / 4?",

    "Calculate 2 ** 8",

    # Knowledge retrieval tests
    "Explain RAG",

    "What is LoRA?",

    "Explain Transformers",

    "What is LangChain?",

    # Multiple tool tests
    "Search for RAG and calculate 20 * 5",

    "What is 10 + 15?",

    # Greeting test
    "Hello, how are you?",

    # Additional evaluation tests
    "Explain RAG and calculate 15 * 12",

    "What is the difference between RAG and LoRA?",

    "Calculate 50 / 5 and explain Transformers",

    "Good morning! What can you do?",

    "Search for information about quantum computing",

    # Failure handling tests
    "Calculate 100 / 0",

    "Calculate 2 ** 1000000",

    "Search for quantum computing",

    "Hello!",

    "Explain RAG and calculate 12 * 12"
]


# ============================================================
# 7. EXECUTE EVALUATION
# ============================================================

for index, question in enumerate(test_cases, start=1):

    print("\n" + "=" * 65)
    print(f"TEST CASE {index}")
    print("=" * 65)

    print("\nQUESTION:")
    print(question)

    try:

        # ----------------------------------------------------
        # A. DETERMINISTIC GREETING ROUTING
        # ----------------------------------------------------

        if is_simple_greeting(question):

            print("\nROUTER:")
            print("Greeting detected. No tools required.")

            final_answer = "Hello! How can I help you today?"

            print("\nFINAL ANSWER:")
            print(final_answer)

            print("\nVALIDATION:")
            print(validate_response(final_answer))

            continue

        # ----------------------------------------------------
        # B. INVOKE AGENT
        # ----------------------------------------------------

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            },
            config={
                "recursion_limit": 12
            }
        )

        # ----------------------------------------------------
        # C. INSPECT AGENT EXECUTION
        # ----------------------------------------------------

        print("\nTOOL EXECUTION:")

        tool_was_used = False

        for message in result["messages"]:

            # AI-generated tool calls
            if message.type == "ai" and message.tool_calls:

                for call in message.tool_calls:

                    tool_was_used = True

                    print("\nSelected tool:", call["name"])

                    print(
                        "Tool arguments:",
                        call["args"]
                    )

            # Tool execution results
            elif message.type == "tool":

                print(
                    "Tool result:",
                    message.content
                )

        if not tool_was_used:

            print("No tools were selected.")

        # ----------------------------------------------------
        # D. EXTRACT FINAL RESPONSE
        # ----------------------------------------------------

        final_message = result["messages"][-1]

        final_answer = final_message.content

        # ----------------------------------------------------
        # E. VALIDATE FINAL RESPONSE
        # ----------------------------------------------------

        validation = validate_response(final_answer)

        if not validation["valid"]:

            final_answer = (
                "I couldn't generate a valid response. "
                "Please try again."
            )

        # ----------------------------------------------------
        # F. DISPLAY RESULTS
        # ----------------------------------------------------

        print("\nFINAL ANSWER:")
        print(final_answer)

        print("\nRESPONSE VALIDATION:")
        print(validation)

    except Exception as error:

        print("\nTEST FAILED:")

        print(type(error).__name__, ":", str(error))


# ============================================================
# 8. EVALUATION COMPLETED
# ============================================================

print("\n" + "=" * 65)
print("AGENT EVALUATION COMPLETED")
print("=" * 65)
