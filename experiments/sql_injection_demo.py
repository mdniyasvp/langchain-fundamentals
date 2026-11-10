import sqlite3


# 1. Create an in-memory database
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()


# 2. Create users table
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
)
""")


# 3. Insert sample users
cursor.executemany(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    [
        ("alice", "password123"),
        ("bob", "mypassword456")
    ]
)

connection.commit()


# 4. Vulnerable login function
def vulnerable_login(username, password):

    query = f"""
    SELECT username FROM users
    WHERE username = '{username}'
    AND password = '{password}'
    """

    print("\nGenerated vulnerable SQL:")
    print(query)

    cursor.execute(query)

    return cursor.fetchone()


# 5. Secure login function
def secure_login(username, password):

    query = """
    SELECT username FROM users
    WHERE username = ?
    AND password = ?
    """

    print("\nExecuting parameterized SQL.")

    cursor.execute(query, (username, password))

    return cursor.fetchone()


# 6. Normal login
print("========== NORMAL LOGIN ==========")

result = vulnerable_login("alice", "password123")

print("Result:", result)


# 7. SQL injection attempt
print("\n========== SQL INJECTION ATTACK ==========")

malicious_username = "' OR '1'='1' --"

result = vulnerable_login(
    malicious_username,
    "wrongpassword"
)

print("Attack result:", result)


# 8. Test the same attack against secure query
print("\n========== PARAMETERIZED QUERY ==========")

result = secure_login(
    malicious_username,
    "wrongpassword"
)

print("Secure result:", result)


connection.close()