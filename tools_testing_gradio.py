from prompt import get_linkedin_virtual_assistant_with_tools
from pushover import push
from tools import record_user_details_json, record_unknown_question_json
import json
from llm import call_chat_api
from util import extract_text_from_pdf, get_text_from_file
import gradio as gr

def record_user_details(email:str, name:str="Name not provided", notes:str="not provided")-> dict:
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "record_user_details_ok"}

def record_unknown_question(question:str)-> dict:
    push(f"Recording {question} asked that I couldn't answer")
    return {"recorded": "record_unknown_question_ok"} 

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]

def handle_tool_call(tool_calls)-> dict:
    results=[]
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        if tool_name == "record_user_details":
            result = record_user_details(**arguments)
        elif tool_name == "record_unknown_question":
            result = record_unknown_question(**arguments)
        else:
            raise ValueError(f"Unknown tool {tool_name}")
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return {"results": results}

linkedin = extract_text_from_pdf("me/linkedin.pdf")
name = "Kush Gupta"
summary = get_text_from_file("me/summary.txt")


def chat(message, history):
    print("Received message:", message)
    system_prompt = get_linkedin_virtual_assistant_with_tools(name, summary, linkedin)
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    done = False
    while not done:

        response = call_chat_api(messages=messages, tools=tools, disable_reasoning=True)
        finish_reason = response.choices[0].finish_reason
        
        if finish_reason=="tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_call(tool_calls)
            #messages.append(message)
            messages.extend(results["results"])
        else:
            done = True
    return response.choices[0].message.content
    

if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown("## 💬 Chat Assistant")
        gr.ChatInterface(fn=chat)

    demo.launch()