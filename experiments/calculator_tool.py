import ast
import operator
from langchain_core.tools import tool

#supported mathematical operations
OPERATORS ={
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}

def safe_calculate(node):
    if isinstance(node,ast.Constant):
        if type(node.value) not in (int,float):
            raise ValueError("Only numeric values are allowed.")
        return node.value

    if isinstance(node, ast.BinOp):
        operation = OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported mathematical operation.")
        left = safe_calculate(node.left)
        right = safe_calculate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Exponent is too large.")
        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported unary operation.")
        return operation(safe_calculate(node.operand))
    raise ValueError("Invalid mathematical expression.")

@tool
def calculator(expression: str) ->str:
    """
    calculate mathematical expressions involving addition, substraction, multiplication, division, exponential and modulo.
    """
    try:
        if len(expression) > 200:
            return "Error: Expression is too long."
        tree = ast.parse(expression, mode="eval")
        result = safe_calculate(tree.body)
        return str(result)
    except(ValueError, TypeError,ZeroDivisionError, OverflowError, SyntaxError) as error:
        return f"calculation error: {error}"

if __name__=="__main__":
    print(calculator.invoke({"expression":"250*48"}))
    print(calculator.invoke({"expression":"100/4"}))
    print(calculator.invoke({"expression":"2**5"}))
    