
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class CalculatorResult(BaseModel):
    status: Literal["success", "error"]
    expression: str = Field(min_length=1)
    result: float | None = None
    error: str | None = None

    @model_validator(mode="after")
    def validate_result_consistency(self):
        if self.status == "success":
            if self.result is None:
                raise ValueError(
                    "Successful calculation must contain a result."
                )

            if self.error is not None:
                raise ValueError(
                    "Successful calculation cannot contain an error."
                )

        elif self.status == "error":
            if self.result is not None:
                raise ValueError(
                    "Failed calculation cannot contain a result."
                )

            if not self.error:
                raise ValueError(
                    "Failed calculation must contain an error."
                )

        return self


class SearchItem(BaseModel):
    topic: str
    content: str


class SearchResult(BaseModel):
    status: Literal["success", "no_results", "error"]
    query: str = Field(min_length=1)
    results: list[SearchItem] = Field(default_factory=list)
    error: str | None = None

    @model_validator(mode="after")
    def validate_search_consistency(self):
        if self.status == "success":
            if not self.results:
                raise ValueError(
                    "Successful search must contain results."
                )

            if self.error is not None:
                raise ValueError(
                    "Successful search cannot contain an error."
                )

        elif self.status == "no_results":
            if self.results:
                raise ValueError(
                    "No-results response cannot contain results."
                )

            if self.error is not None:
                raise ValueError(
                    "No-results response cannot contain an error."
                )

        elif self.status == "error":
            if self.results:
                raise ValueError(
                    "Failed search cannot contain results."
                )

            if not self.error:
                raise ValueError(
                    "Failed search must contain an error."
                )

        return self
