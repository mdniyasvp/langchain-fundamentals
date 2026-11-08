\# LangChain Fundamentals



A hands-on learning project covering the fundamentals of \*\*LangChain and Generative AI application development\*\*, using Python and locally hosted LLMs through Ollama.



This project explores prompt engineering, chat models, LangChain Expression Language (LCEL), document loading, conversation handling, structured outputs, and document-based question answering.



\## Learning Objectives



\- Understand LangChain architecture and core components.

\- Build reusable prompt templates.

\- Work with chat models and local LLMs.

\- Construct chains using LangChain Expression Language (LCEL).

\- Understand `invoke()`, `batch()`, and `stream()`.

\- Load and process text and PDF documents.

\- Implement a basic document question-answering workflow.

\- Explore structured outputs and conversation history.



\## Project Structure



```text

langchain-fundamentals/

│

├── data/

│   └── company\_policy.txt

│

├── experiments/

│   ├── chat\_model\_demo.py

│   ├── conversation\_demo.py

│   ├── document\_loader\_demo.py

│   ├── document\_qa.py

│   ├── pdf\_loader\_demo.py

│   └── structured\_output\_demo.py

│

├── main.py

├── pyproject.toml

├── uv.lock

├── .gitignore

└── README.md

```



\## Technologies Used



\- Python

\- LangChain

\- LangChain Core

\- LangChain Ollama

\- Ollama

\- PyPDF

\- Pydantic

\- uv



\## Local LLM



This project uses Ollama to run language models locally, avoiding the need for paid API calls.



The primary model used is:



`llama3.2:3b`



Install Ollama and download the model:



```bash

ollama pull llama3.2:3b

```



Make sure the Ollama service is running before executing the application.



\## Setup Instructions



\### 1. Clone the repository



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd langchain-fundamentals

```



\### 2. Install uv



```bash

pip install uv

```



\### 3. Install project dependencies



```bash

uv sync

```



\### 4. Download the Ollama model



```bash

ollama pull llama3.2:3b

```



\### 5. Run the main application



```bash

uv run python main.py

```



Enter a technical topic and difficulty level to receive an explanation from the local LLM.



\## Practical Experiments



| File | Description |

|---|---|

| `chat\_model\_demo.py` | Exploring LangChain chat models |

| `conversation\_demo.py` | Working with conversational messages and history |

| `document\_loader\_demo.py` | Loading text documents |

| `document\_qa.py` | Basic document question-answering |

| `pdf\_loader\_demo.py` | Loading PDF documents |

| `structured\_output\_demo.py` | Exploring structured model outputs |

| `main.py` | LCEL-based prompt and model chain |



\## Key Concepts Practiced



\*\*Prompt Templates:\*\* Creating reusable prompts with dynamic variables.



\*\*Chat Models:\*\* Interacting with locally hosted LLMs.



\*\*LCEL:\*\* Composing prompts, models, and output parsers using the pipe operator.



\*\*Output Parsers:\*\* Converting model responses into usable formats.



\*\*Document Loaders:\*\* Loading text and PDF documents into LangChain Document objects.



\*\*Document Q\&A:\*\* Using document content as context for answering questions.



\*\*Chain Execution:\*\* Understanding synchronous invocation, batch processing, and streaming.



\## Future Improvements



\- Tool-based agents

\- ReAct agent workflows

\- Multimodal LLM applications

\- FastAPI deployment

\- Retrieval-Augmented Generation (RAG)

\- Production-oriented GenAI application development



\## Learning Progress



\- \[x] Day 1 — LangChain Fundamentals

\- \[ ] Day 2 — Tool-Based Agents

\- \[ ] Day 3 — Multimodal LLMs

\- \[ ] Day 4 — Deployment with FastAPI

\- \[ ] Day 5 — RAG System Architecture



\---



\*\*Purpose:\*\* Practical learning and experimentation with LangChain, local LLMs, and Generative AI application development.

