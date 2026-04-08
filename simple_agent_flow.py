    

from llm import call_chat_api


response  = call_chat_api([{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is the capital of France?"}]   )
print(response)
answer = response.content if response else "No response from LLM API."
print(answer)