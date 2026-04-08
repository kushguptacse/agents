from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from llm import call_chat_api
import uvicorn
from config import LLM_MODEL_NAME, PORT

app = FastAPI()

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    payload = await request.json()
    messages = payload.get("messages", [])
    # Optionally pass through other OpenAI-compatible params
    response = call_chat_api(messages)
    if response is None:
        return JSONResponse(status_code=500, content={"error": "LLM call failed"})
    # Return OpenAI-compatible response structure
    return JSONResponse(content={
        "id": "chatcmpl-xxx",
        "object": "chat.completion",
        "created": 0,
        "model": LLM_MODEL_NAME,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response.content if hasattr(response, "content") else str(response)
                },
                "finish_reason": "stop"
            }
        ],
        "usage": getattr(response, 'usage', None)
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
