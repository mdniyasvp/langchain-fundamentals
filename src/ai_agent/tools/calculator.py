
import ast
import math
import operator

from langchain_core.tools import tool

from ai_agent.tools.schemas import CalculatorResult



OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate_expression(expression: str) -> float:

    if len(expression) > 200:
        raise ValueError("Expression is too long.")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        raise ValueError("Invalid mathematical expression.")

    def evaluate(node):

        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Only numeric values are allowed.")

            if abs(node.value) > 1_000_000_000:
                raise ValueError("Number exceeds allowed magnitude.")

            return node.value

        if isinstance(node, ast.BinOp):
            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported mathematical operator.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent exceeds allowed limit.")

            result = operation(left, right)

            if isinstance(result, complex):
                raise ValueError("Complex results are not supported.")

            if not math.isfinite(result):
                raise ValueError("Result is not finite.")

            if abs(result) > 1_000_000_000:
                raise ValueError("Result exceeds allowed magnitude.")

            return result

        if isinstance(node, ast.UnaryOp):
            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported unary operator.")

            result = operation(evaluate(node.operand))

            if not math.isfinite(result):
                raise ValueError("Result is not finite.")

            return result

        raise ValueError("Unsupported expression.")

    return evaluate(tree)



@tool
def calculator(expression: str) -> str:
    """Safely evaluate a mathematical expression."""

    try:
        value = evaluate_expression(expression)

        response = CalculatorResult(
            status="success",
            expression=expression,
            result=value
        )

    except (ValueError, ZeroDivisionError, OverflowError) as error:

        response = CalculatorResult(
            status="error",
            expression=expression,
            error=str(error)
        )

    return response.model_dump_json()
