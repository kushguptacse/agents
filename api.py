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
    tools = payload.get("tools", [])
    
    response = call_chat_api(messages, tools=tools)
    if response is None:
        return JSONResponse(status_code=500, content={"error": "LLM call failed"})
    # Return OpenAI-compatible response structure
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
