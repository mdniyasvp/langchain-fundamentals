import os
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# Read configuration
APP_ENV = os.getenv("APP_ENV", "development")

APP_NAME = os.getenv(
    "APP_NAME",
    "AI Application"
)

DEMO_SECRET = os.getenv("DEMO_SECRET")


# Display non-sensitive configuration
print("Application:", APP_NAME)
print("Environment:", APP_ENV)

# Never print the actual secret
print(
    "Demo secret loaded:",
    DEMO_SECRET is not None
)