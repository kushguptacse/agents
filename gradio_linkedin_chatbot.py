import gradio as gr
from pypdf import PdfReader
from prompt import get_linkedin_virtual_assistant
from llm import call_chat_api   

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

with open("me/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

linkedin = extract_text_from_pdf("me/linkedin.pdf")

name = "Kush Gupta"

system_prompt = get_linkedin_virtual_assistant(name, summary, linkedin)

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = call_chat_api(messages=messages)
    if response is None:
        return "Sorry, I could not get a response from the LLM."

    choices = getattr(response, "choices", None)
    if not choices:
        return "Sorry, I could not get a valid response from the LLM."

    return choices[0].message.content

if __name__ == "__main__":
    gr.ChatInterface(chat).launch()