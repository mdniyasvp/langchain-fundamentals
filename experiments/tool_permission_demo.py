from langchain_core.tools import tool


# Simulated application user
CURRENT_USER = {
    "user_id": "USER001",
    "role": "admin"
}


# Permission checker
def has_permission(user, required_role):
    return user["role"] == required_role


# Tool requiring admin permission
@tool
def delete_customer_record(customer_id: str) -> str:
    """Delete a customer record. Requires admin permission."""

    if not has_permission(CURRENT_USER, "admin"):
        return "ACCESS DENIED: Admin permission required."

    # Simulated deletion only
    return f"Customer record {customer_id} deleted successfully."


# Test
result = delete_customer_record.invoke({
    "customer_id": "CUST100"
})

print(result)