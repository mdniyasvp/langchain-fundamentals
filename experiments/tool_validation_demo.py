from pydantic import BaseModel, Field
from langchain_core.tools import tool


# 1. Define input schema
class TransferInput(BaseModel):

    amount: float = Field(
        gt=0,
        le=100000,
        description="Transfer amount. Must be greater than 0 and at most 100000."
    )

    account_number: str = Field(
        min_length=10,
        max_length=16,
        description="Destination account number."
    )


# 2. Create validated tool
@tool(args_schema=TransferInput)
def transfer_money(
    amount: float,
    account_number: str
) -> str:
    """Transfer money to a destination bank account."""

    return (
        f"Transfer request accepted: "
        f"₹{amount} to account {account_number}"
    )


# 3. Test valid input
print("\nVALID INPUT:")

try:
    result = transfer_money.invoke({
        "amount": 5000,
        "account_number": "1234567890"
    })

    print(result)

except Exception as error:
    print("VALIDATION ERROR:", error)


# 4. Test invalid amount
print("\nINVALID AMOUNT:")

try:
    result = transfer_money.invoke({
        "amount": -5000,
        "account_number": "1234567890"
    })

    print(result)

except Exception as error:
    print("VALIDATION ERROR:", error)


# 5. Test invalid account number
print("\nINVALID ACCOUNT:")

try:
    result = transfer_money.invoke({
        "amount": 5000,
        "account_number": "123"
    })

    print(result)

except Exception as error:
    print("VALIDATION ERROR:", error)