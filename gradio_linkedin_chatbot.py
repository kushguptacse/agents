import gradio as gr
from pypdf import PdfReader
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

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

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