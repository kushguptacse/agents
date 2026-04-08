# agents
Project covers basic agentic flow example using qwen3 LLM and exposes LLM endpoint for further usage

1. AI agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.

2. AI agentic solutions have some characterstics - Multiple LLM calls, LLM uses tools, autonomous decision making.

## Project File Overview

- **config.py**: Stores configuration variables such as API URLs, model names, and keys.
- **llm.py**: Contains the logic to call the LLM (Qwen3/OpenAI-compatible) API.
- **api.py**: Exposes the LLM as a REST API endpoint using FastAPI and Uvicorn, compatible with OpenAI payloads.
- **simple_agent_flow.py**: Demonstrates a multi-step agentic workflow by calling the REST API endpoint and processing responses.
- **README.md**: Project overview and file descriptions (this file).
