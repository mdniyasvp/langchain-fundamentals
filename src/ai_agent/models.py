
from langchain_ollama import ChatOllama

from ai_agent.config import MODEL_NAME, TEMPERATURE


def get_chat_model():

    model = ChatOllama(
        model=MODEL_NAME,
        temperature=TEMPERATURE
    )

    return model
