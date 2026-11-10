import chromadb


# 1. Create an in-memory ChromaDB client
client = chromadb.EphemeralClient()

collection = client.create_collection(
    name="company_documents"
)


# 2. Insert documents from two companies
documents = [
    "Company A provides 20 annual leave days.",
    "Company A employee salary information.",
    "Company B provides 25 annual leave days.",
    "Company B confidential financial report."
]

metadatas = [
    {
        "tenant_id": "company_A",
        "access_level": "public"
    },
    {
        "tenant_id": "company_A",
        "access_level": "confidential"
    },
    {
        "tenant_id": "company_B",
        "access_level": "public"
    },
    {
        "tenant_id": "company_B",
        "access_level": "confidential"
    }
]

ids = ["DOC1", "DOC2", "DOC3", "DOC4"]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)


# 3. Simulated authenticated user
# In production, obtain this identity from
# a verified server-side authentication session.
authenticated_user = {
    "user_id": "USER001",
    "tenant_id": "company_A",
    "role": "employee"
}


# 4. Define permissions
ROLE_PERMISSIONS = {
    "employee": ["public"],
    "manager": ["public", "confidential"]
}


# 5. Secure retrieval function
def retrieve_documents(user):

    tenant_id = user["tenant_id"]
    role = user["role"]

    if role not in ROLE_PERMISSIONS:
        raise PermissionError("Unknown user role.")

    allowed_levels = ROLE_PERMISSIONS[role]

    results = collection.get(
        where={
            "$and": [
                {"tenant_id": tenant_id},
                {"access_level": {"$in": allowed_levels}}
            ]
        }
    )

    return results["documents"]


# 6. Test employee access
print("\nEMPLOYEE ACCESS:")

employee_results = retrieve_documents(
    authenticated_user
)

for document in employee_results:
    print("-", document)


# 7. Test manager access
print("\nMANAGER ACCESS:")

manager = {
    **authenticated_user,
    "role": "manager"
}

manager_results = retrieve_documents(manager)

for document in manager_results:
    print("-", document)