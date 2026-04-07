    
from llm import call_chat_api


ans  = call_chat_api([{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is the capital of France?"}]   )

print(ans)