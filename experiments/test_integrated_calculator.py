from ai_agent.tools.calculator import calculator

test_cases = [
    "25 + 15",
    "100 - 35",
    "12 * 8",
    "144 / 12",
    "2 ** 5",
    "17 % 5",
    "10 / 0",
    "2 ** 20",
    "100 + 200 * 3",
]

for expression in test_cases:

    result = calculator.invoke({
        "expression": expression
    })

    print(f"{expression} = {result}")