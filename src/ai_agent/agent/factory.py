
from langchain.agents import create_agent

from ai_agent.models import get_chat_model

from ai_agent.tools.calculator import calculator
from ai_agent.tools.search import search_knowledge


SYSTEM_PROMPT = """
You are a helpful AI assistant specializing in
mathematics and AI engineering.

You have access to two tools:

1. calculator:
   Use this tool for mathematical calculations.

2. search_knowledge:
   Use this tool for questions about RAG, LoRA,
   Transformers and LangChain.

IMPORTANT RULES:

1. Use the calculator for calculations.
   Never invent calculation results.

2. Use search_knowledge for supported AI topics.

3. If the search tool returns no_results,
   clearly explain that the requested topic
   is not available in the knowledge base.

4. Never fabricate search results.

5. If a tool returns an error, explain the error.
   Never pretend that the operation succeeded.

6. For questions requiring multiple operations,
   use all relevant tools.

7. Provide clear and concise answers.

8. If you do not know something, acknowledge it.
"""


def build_agent():

    model = get_chat_model()

    tools = [
        calculator,
        search_knowledge
    ]

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )

    return agent
