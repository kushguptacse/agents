
## Project File Overview

- **config.py**: Stores configuration variables such as API URLs, model names, and keys.
- **llm.py**: Contains the logic to call the LLM (Qwen3/OpenAI-compatible) API.
- **api.py**: Exposes the LLM as a REST API endpoint using FastAPI and Uvicorn, compatible with OpenAI payloads.
- **simple_agent_flow.py**: Demonstrates a multi-step agentic workflow by calling the REST API endpoint and processing responses.
- **prompt.py**: Contains prompt templates and prompt management utilities for various agent workflows.
- **tools.py**: Defines custom tools and functions available to agents for task execution.
- **util.py**: Utility functions and helper methods used across the project.
- **gradio_linkedin_chatbot.py**: Implements a LinkedIn-focused chatbot interface using Gradio for user interaction.
- **evaluator_optmizer_pattern_linkedin_agent.py**: Implements evaluation and optimization patterns for LinkedIn agents.
- **todo_list_performer.py**: Agent implementation for managing and performing tasks from a todo list.
- **tools_testing_gradio.py**: Gradio-based interface for testing and demonstrating available tools.
- **pushover.py**: Integration module for Pushover notifications and alerts.
- **agents_llm_api.postman_collection.json**: Postman collection for testing and documenting API endpoints.
- **me/summary.txt**: User profile or project summary information.


# agents
Project covers basic agentic flow example using qwen3 LLM and exposes LLM endpoint for further usage

1. AI agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.

2. AI agentic solutions have some characterstics - Multiple LLM calls, LLM uses tools, autonomous decision making.


# Design Patterns in Agentic Application

---

## 1. Prompt Chaining

### Definition
**Prompt Chaining** is a design pattern where the output of one LLM call becomes the input to another LLM call.  
This process can continue across multiple steps until the final output is produced.

### When to Use
Use this pattern when a task can be broken into **sequential stages**.

### Common Use Cases
- Extract → Classify → Summarize

### Example
User asks for contract analysis:
1. First LLM extracts important clauses
2. Second LLM identifies risks
3. Third LLM generates a summary

### Benefits
- Easy to design and debug
- Improves control over complex tasks
- Allows step-by-step validation

### Limitation
- Higher latency due to multiple sequential LLM calls

---

## 2. Routing

### Definition
**Routing** is a design pattern where the incoming user request is analyzed first, and then directed to the most suitable **model, tool, workflow, or agent**.

### When to Use
Use this pattern when your system supports **multiple capabilities** and not every request should go through the same path.

### Common Use Cases
- Send coding questions to code workflow
- Send SQL requests to database tool
- Send summarization requests to document pipeline
- Send general questions to chat model

### Example
A user query is first analyzed:
- If it is a coding question → use coding model
- If it is a math question → use reasoning flow
- If it requires database access → use SQL tool

### Benefits
- Better accuracy by choosing the right path
- Reduces unnecessary tool/model usage
- Improves efficiency and cost optimization

### Limitation
- Incorrect routing can lead to poor final answers

> **Note:** Routing can be done using an **LLM** or **programmatic rules**.

---

## 3. Parallelization

### Definition
**Parallelization** is a design pattern where a task is divided into multiple **independent subtasks**, and those subtasks are executed **concurrently**.  
Once all subtasks are completed, their outputs are combined to produce the final result.

### Typical Flow
1. **Coordinator (programmatic code)** breaks the task into subtasks
2. Multiple LLM calls run in parallel
3. **Aggregator (programmatic code)** combines the outputs

### When to Use
Use this pattern when subtasks are **independent** and do not depend on each other’s outputs.

### Common Use Cases
- Summarizing large documents chunk by chunk
- Running sentiment, keyword extraction, and summary together
- Evaluating multiple candidate answers at once

### Example
For document analysis:
- One LLM extracts entities
- One LLM identifies risks
- One LLM creates summary
- Final code merges the outputs

### Benefits
- Faster execution
- Better scalability
- Useful for large inputs or multi-analysis workflows

### Limitation
- Not suitable if subtasks depend on previous outputs

---

## 4. Orchestrator-Worker

### Definition
**Orchestrator-Worker** is a design pattern where an LLM dynamically plans the work, creates subtasks, assigns them to worker LLMs/tools, and combines the results into a final response.

Unlike standard Parallelization, the task decomposition is handled **intelligently by an LLM**, not just fixed programmatic logic.

### Typical Flow
1. **Orchestrator (LLM)** analyzes the task
2. It decides what subtasks are needed
3. Multiple **Workers (LLMs/tools)** execute those subtasks
4. A **Synthesizer (LLM)** combines the outputs

### When to Use
Use this pattern when:
- the number of subtasks is not fixed
- the system must decide dynamically how to solve the problem
- tasks are complex and require decomposition

### Example
User asks:
> “Prepare a go-to-market plan for a new AI product”

The Orchestrator may create these workers:
- Market research worker
- Competitor analysis worker
- Pricing strategy worker
- Launch strategy worker

Then the Synthesizer combines all outputs into one final plan.

### Benefits
- Highly flexible
- Handles complex and open-ended tasks well
- Enables intelligent task planning

### Limitation
- More expensive and harder to control than fixed workflows

---

## 5. Evaluator-Optimizer

### Definition
**Evaluator-Optimizer** is a design pattern where one LLM generates an output, and another LLM evaluates it against predefined criteria.  
If the output is not good enough, feedback is provided and the output is improved iteratively.

### Typical Flow
1. **Generator LLM** produces output
2. **Evaluator LLM** checks quality, correctness, or compliance
3. If needed, feedback is sent back
4. Generator improves the output
5. Process repeats until acceptable result is achieved

### When to Use
Use this pattern when output quality matters and iterative refinement is valuable.

### Common Use Cases
- SQL generation with validation
- Code generation with review
- Policy-compliant response generation
- Report or content refinement

### Example
- Generator creates SQL query
- Evaluator checks correctness and safety
- If issues are found, feedback is sent back
- Query is regenerated until valid

### Benefits
- Improves output quality
- Reduces hallucination and formatting errors
- Useful in high-accuracy workflows

### Limitation
- Higher latency and cost due to iterative loops

---

