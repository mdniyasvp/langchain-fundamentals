
from langchain_core.tools import tool
from langchain_core.tools import ToolException


@tool
def divide_numbers(a: float, b: float) -> float:
    """
    Divide two numbers.
    """

    if b == 0:
        raise ToolException(
            "Division by zero is not permitted."
        )

    return a / b


# Test successful execution
try:
    result = divide_numbers.invoke({
        "a": 100,
        "b": 4
    })

    print("SUCCESS:", result)

except ToolException as error:
    print("TOOL ERROR:", error)


# Test failed execution
try:
    result = divide_numbers.invoke({
        "a": 100,
        "b": 0
    })

    print("SUCCESS:", result)

except ToolException as error:
    print("TOOL ERROR:", error)
