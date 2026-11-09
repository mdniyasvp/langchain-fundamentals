from experiments.calculator_tool import calculator
from experiments.search_tool import mock_search

tools = [calculator, mock_search]
for tool in tools:
    print("\nTOOL NAME:",tool.name)
    print("DESCRIPTION:",tool.description)
    print("ARGUMENT SCHEMA:",tool.args)