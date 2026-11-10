
import pytest

from ai_agent.tools.calculator import evaluate_expression


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("25 + 15", 40),
        ("100 - 35", 65),
        ("12 * 8", 96),
        ("144 / 12", 12),
        ("2 ** 5", 32),
        ("17 % 5", 2),
        ("100 + 200 * 3", 700),
    ]
)
def test_valid_calculations(expression, expected):

    result = evaluate_expression(expression)

    assert result == expected


@pytest.mark.parametrize(
    "expression",
    [
        "10 / 0",
        "2 ** 20",
        "1000000001 + 1",
        "invalid expression",
        "__import__('os').system('dir')",
    ]
)
def test_invalid_calculations(expression):

    with pytest.raises((ValueError, ZeroDivisionError)):
        evaluate_expression(expression)
