from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/company_policy.pdf")

documents = loader.load()

print("Total pages:", len(documents))

for i, document in enumerate(documents):
    print(f"\n--- PAGE {i + 1} ---")
    print(document.page_content[:500])
    print("Metadata:", document.metadata)