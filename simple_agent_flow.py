    
import requests
from config import CHAT_COMPLETIONS_API_URL

def ask_llm(question):
	payload = {"messages": [{"role": "user", "content": question}]}
	try:
		r = requests.post(CHAT_COMPLETIONS_API_URL, json=payload)
		r.raise_for_status()
		data = r.json()
		response = data["choices"][0]["message"]
		answer = response.get("content", "No content in response.")
	except Exception as e:
		print(f"Error calling REST endpoint: {e}")
		answer = "No response from REST endpoint."
	return answer

# Step 1
question1 = "pick one business area that might be worth exploring for an Agentic AI opportunity."
answer1 = ask_llm(question1)

# Step 2
question2 = f"Using below business area,present a pain-point in the industry - something challenging that might be ripe for an Agentic solution. \n {answer1}"
answer2 = ask_llm(question2)

# Step 3
question3 = f"Using below pain-point, brainstorm a potential Agentic AI solution to the pain point you identified. \n {answer2}"
answer3 = ask_llm(question3)

print("Final answer:", answer3)