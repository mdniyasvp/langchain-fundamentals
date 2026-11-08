
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama

# Define expected output schema
class Candidate(BaseModel):
    name: str = Field(description="Candidate name")
    skills: list[str] = Field(description="Technical skills")
    experience_level: str = Field(
        description="Experience level"
    )

# Initialize model
model = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

# Create structured-output model
structured_model = model.with_structured_output(
    Candidate
)

# Execute
response = structured_model.invoke(
    "Analyze this candidate: John knows Python, "
    "SQL and Machine Learning. He has intermediate skills."
)

print(response)
print("\nCandidate name:", response.name)
print("Skills:", response.skills)
print("Experience:", response.experience_level)
