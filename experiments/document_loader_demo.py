
from langchain_community.document_loaders import TextLoader

# 1. Initialize document loader
loader = TextLoader(
    "data/company_policy.txt",
    encoding="utf-8"
)

# 2. Load document
documents = loader.load()

# 3. Inspect loaded documents
print("Number of documents:", len(documents))

# 4. Access document content
document = documents[0]

print("\nDOCUMENT CONTENT:\n")
print(document.page_content)

# 5. Access metadata
print("\nDOCUMENT METADATA:\n")
print(document.metadata)
