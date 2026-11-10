
import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "LangChain AI Agent")
APP_ENV = os.getenv("APP_ENV", "development")

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")

MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "12"))

TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))

print(f"Application: {APP_NAME}")
print(f"Environment: {APP_ENV}")
