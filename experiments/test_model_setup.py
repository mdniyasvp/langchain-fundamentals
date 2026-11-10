from langchain_core.messages import SystemMessage, HumanMessage

from ai_agent.models import get_chat_model

model = get_chat_model()

messages = [
    SystemMessage(
        content=(
            "You are a Python AI engineering tutor. "
            "Answer accurately and concisely. "
            "If uncertain, say so. "
            "Do not invent facts."
        )
    ),
    HumanMessage(
        content=(
            "In Python AI development, what is LangChain? "
            "Explain its purpose in one sentence."
        )
    )
]

response = model.invoke(messages)

print("\nMODEL RESPONSE:")
print(response.content)