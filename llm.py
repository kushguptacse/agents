import json
from config import API_URL, CHAT_COMPLETIONS_API_KEY, LLM_MODEL_NAME, LLM_TEMPERATURE, MAX_TOKEN
import openai

openai.api_key = CHAT_COMPLETIONS_API_KEY
openai.base_url = API_URL

def call_chat_api(messages, disable_reasoning=True):
    """
    Calls the LLM API with tools for function calling using OpenAI library.
    Returns the message object that may contain tool calls.
    """
    p = json.dumps(messages)
    print("DEBUG", f"Prompt Length: {len(p)}")
    extra_body: dict = {
    }
    if disable_reasoning:
        extra_body['reasoning_effort'] = 'none'
    try:
        response = openai.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=messages,
            temperature=LLM_TEMPERATURE,
            max_tokens=MAX_TOKEN,
            extra_body= extra_body
        )
        
        usage = getattr(response, 'usage', None)
        if usage:
            print("DEBUG", f"Usage of LLM API: {usage}")
        
        return response
        
    except Exception as e:
        print("ERROR", f"Error calling LLM API with tools: {e}")
        print("ERROR", f"The prompt seems too long.")
        return None
