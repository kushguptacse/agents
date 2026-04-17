from prompt import get_linkedin_virtual_assistant_with_tools
from pushover import push
import json
from llm import loop_llm_call
from util import extract_text_from_pdf, get_text_from_file
import gradio as gr

def record_user_details(email:str, name:str="Name not provided", notes:str="not provided")-> dict:
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "record_user_details_ok"}

def record_unknown_question(question:str)-> dict:
    push(f"Recording {question} asked that I couldn't answer")
    return {"recorded": "record_unknown_question_ok"} 

linkedin = extract_text_from_pdf("me/linkedin.pdf")
name = "Kush Gupta"
summary = get_text_from_file("me/summary.txt")

from tools import TOOL_REGISTRY, record_user_details_json, record_unknown_question_json
tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]
TOOL_REGISTRY["record_user_details"] = record_user_details
TOOL_REGISTRY["record_unknown_question"] = record_unknown_question

def chat(message, history):
    print("Received message:", message)
    system_prompt = get_linkedin_virtual_assistant_with_tools(name, summary, linkedin)
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    return loop_llm_call(messages, tools)

if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown("## 💬 Chat Assistant")
        gr.ChatInterface(fn=chat)

    demo.launch()