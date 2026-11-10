
import json

from ai_agent.tools.calculator import calculator
from ai_agent.tools.schemas import CalculatorResult


def test_successful_calculation():

    raw = calculator.invoke({
        "expression": "100 + 200 * 3"
    })

    result = CalculatorResult.model_validate_json(raw)

    assert result.status == "success"
    assert result.result == 700
    assert result.error is None


def test_failed_calculation():

    raw = calculator.invoke({
        "expression": "10 / 0"
    })

    result = CalculatorResult.model_validate_json(raw)

    assert result.status == "error"
    assert result.result is None
    assert "division by zero" in result.error.lower()


def test_invalid_schema_status():

    from pydantic import ValidationError
    import pytest

    with pytest.raises(ValidationError):
        CalculatorResult(
            status="unknown",
            expression="2 + 2",
            result=4
        )
