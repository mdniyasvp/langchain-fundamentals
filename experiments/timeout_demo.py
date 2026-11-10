
import time
from concurrent.futures import (
    ThreadPoolExecutor,
    TimeoutError
)


def slow_tool():
    """Simulate a slow external API."""

    print("Tool execution started...")

    time.sleep(5)

    return "External API response received."


with ThreadPoolExecutor(max_workers=1) as executor:

    future = executor.submit(slow_tool)

    try:
        result = future.result(timeout=2)

        print("SUCCESS:", result)

    except TimeoutError:
        print("ERROR: Tool execution timed out.")

