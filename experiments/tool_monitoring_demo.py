import json
import logging
import time
import uuid

from datetime import datetime, timezone
from langchain_core.tools import tool


# 1. Configure JSON logging
class JSONFormatter(logging.Formatter):

    def format(self, record):

        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "event": record.getMessage(),
            "request_id": getattr(record, "request_id", None),
            "tool_name": getattr(record, "tool_name", None),
            "status": getattr(record, "status", None),
            "execution_time": getattr(
                record, "execution_time", None
            ),
            "error": getattr(record, "error", None),
        }

        return json.dumps(log_data)


logger = logging.getLogger("agent_monitor")

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    "agent_audit.log",
    encoding="utf-8"
)

file_handler.setFormatter(JSONFormatter())

logger.addHandler(file_handler)


# 2. Create monitored calculator tool
@tool
def monitored_calculator(expression: str) -> str:
    """Calculate a basic arithmetic expression.

    Supported operations: addition, subtraction,
    multiplication and division.
    """

    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    logger.info(
        "Tool execution started",
        extra={
            "request_id": request_id,
            "tool_name": "monitored_calculator",
            "status": "started",
        }
    )

    try:

        # Simple controlled demonstration
        allowed = set("0123456789+-*/(). ")

        if not expression or not set(expression) <= allowed:
            raise ValueError("Invalid expression.")

        # Use the existing safe calculator instead of eval
        from experiments.calculator_tool import calculator

        result = calculator.invoke({
            "expression": expression
        })


        result = calculator.invoke({
            "expression": expression
        })
        print("DEBUG CALCULATOR RESULT:", repr(result))
        
        
        if (
            isinstance(result, str)
            and result.lower().startswith("calculation error:")
        ):
            raise ValueError(result)

        
        elapsed = round(
            time.perf_counter() - start_time, 4
        )

        logger.info(
            "Tool execution completed",
            extra={
                "request_id": request_id,
                "tool_name": "monitored_calculator",
                "status": "success",
                "execution_time": elapsed,
            }
        )

        return str(result)

    except Exception as error:

        elapsed = round(
            time.perf_counter() - start_time, 4
        )

        logger.error(
            "Tool execution failed",
            extra={
                "request_id": request_id,
                "tool_name": "monitored_calculator",
                "status": "error",
                "execution_time": elapsed,
                "error": type(error).__name__,
            }
        )

        raise


# 3. Test tool execution
if __name__ == "__main__":

    print("TEST 1: Successful calculation")

    try:
        result = monitored_calculator.invoke({
            "expression": "125 * 48"
        })
        print("RESULT:", result)

    except Exception as error:
        print("ERROR:", error)

    print("\nTEST 2: Invalid calculation")

    try:
        result = monitored_calculator.invoke({
            "expression": "10 / 0"
        })
        print("RESULT:", result)

    except Exception as error:
        print("ERROR:", error)

    print("\nCheck agent_audit.log for execution logs.")