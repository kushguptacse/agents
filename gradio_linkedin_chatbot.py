import gradio as gr
from prompt import get_linkedin_virtual_assistant
from llm import call_chat_api
from util import get_text_from_file, extract_text_from_pdf


linkedin = extract_text_from_pdf("me/linkedin.pdf")

name = "Kush Gupta"

summary = get_text_from_file("me/summary.txt")

system_prompt = get_linkedin_virtual_assistant(name, summary, linkedin)


def chat(message, history):
    messages = (
        [{"role": "system", "content": system_prompt}]
        + history
        + [{"role": "user", "content": message}]
    )
    response = call_chat_api(messages=messages)
    if response is None:
        return "Sorry, I could not get a response from the LLM."

    choices = getattr(response, "choices", None)
    if not choices:
        return "Sorry, I could not get a valid response from the LLM."

    return choices[0].message.content


if __name__ == "__main__":
    gr.ChatInterface(chat).launch()
