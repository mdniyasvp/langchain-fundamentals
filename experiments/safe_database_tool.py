import sqlite3

from pydantic import BaseModel, Field
from langchain_core.tools import tool


# 1. Create sample database
connection = sqlite3.connect(
    ":memory:",
    check_same_thread=False
)

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE employees (
    employee_id TEXT PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER
)
""")

cursor.executemany(
    """
    INSERT INTO employees
    (employee_id, name, department, salary)
    VALUES (?, ?, ?, ?)
    """,
    [
        ("E101", "Alice", "Engineering", 60000),
        ("E102", "Bob", "HR", 45000),
        ("E103", "Charlie", "Finance", 55000)
    ]
)

connection.commit()


# 2. Define validated tool arguments
class EmployeeInput(BaseModel):

    employee_id: str = Field(
        pattern=r"^E\d{3}$",
        description="Employee ID such as E102."
    )


# 3. Create safe database tool
@tool(args_schema=EmployeeInput)
def get_employee_details(employee_id: str) -> str:
    """Retrieve an employee's name and department using employee ID.

    Salary information is not available through this tool.
    """

    query = """
    SELECT employee_id, name, department
    FROM employees
    WHERE employee_id = ?
    """

    cursor = connection.execute(
        query,
        (employee_id,)
    )

    employee = cursor.fetchone()

    if employee is None:
        return "No employee found."

    return (
        f"Employee ID: {employee['employee_id']}\n"
        f"Name: {employee['name']}\n"
        f"Department: {employee['department']}"
    )


# 4. Test normal input
if __name__ == "__main__":

    print("\nNORMAL REQUEST:")

    result = get_employee_details.invoke({
        "employee_id": "E102"
    })

    print(result)

    print("\nINVALID INPUT:")

    try:
        result = get_employee_details.invoke({
            "employee_id": "' OR '1'='1' --"
        })

        print(result)

    except Exception as error:
        print("VALIDATION ERROR:", error)

    connection.close()