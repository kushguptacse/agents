# agents
some solutions and learning related to ai agents


## Project File Overview

- **config.py**: Stores configuration variables such as API URLs, model names, and keys.
- **llm.py**: Contains the logic to call the LLM (Qwen3/OpenAI-compatible) API.
- **api.py**: Exposes the LLM as a REST API endpoint using FastAPI and Uvicorn, compatible with OpenAI payloads.
- **simple_agent_flow.py**: Demonstrates a multi-step agentic workflow by calling the REST API endpoint and processing responses.
- **README.md**: Project overview and file descriptions (this file).
