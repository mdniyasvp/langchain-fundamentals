from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from experiments.calculator_tool import calculator
from experiments.search_tool import mock_search

#1. Initial model
model = ChatOllama(model = "llama3.2:3b",
                   temperature=0)
#2. Register tools
tools = [calculator, mock_search]
#3. Create agent
agent = create_agent(model = model,
                     tools= tools,
                     system_prompt="""
                     You are helpful AI assistant.
                     You have access to two tools:
                     1. calculator: Use this for mathematical calculations.
                     2. mock_search: Use this to retrieve information about RAG, LoRA, Transformers and LangChain.
                     Instructions:
                     - Select tools based on the user's request.
                     - Do not invent calculartor results.
                     - Use search result when answering knowledge based questions.
                     - If a tool cannot find information, clearly acknowledge the limitation.
                     - Do not call tools unnecessarily.""" ) 
#4. Execute agent
question = "What is 250 multiplied by 48?"
result = agent.invoke(
    {"messages":[
        {"role": "user", "content":question}
    ]},
    config={"recursion_limit":12}
)
#5. Display execution
print("\nUSER:")
print(question)
print("\nAGENT EXECUTION:")
for message in result["messages"]:
    print(f"\nROLE: {message.type}")
    if message.type == "ai" and message.tool_calls:
        print("TOOL CALLS:", message.tool_calls)
    elif message.type == "tool":
        print("TOOL RESULT:", message.content)
    else:
        print("CONTENT:", message.content)