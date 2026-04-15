# Below scripts perform the following functions:

# 1. Be able to ask an LLM to evaluate an answer
# 2. Be able to rerun if the answer fails evaluation
# 3. Put this together into 1 workflow

from os import name
import json
from pydantic import BaseModel
from llm import call_chat_api
from prompt import (
    get_linkedin_virtual_assistant_evaluator,
    get_evaluator_user_prompt,
    get_linkedin_virtual_assistant,
)
from util import get_text_from_file, extract_text_from_pdf
import gradio as gr


class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str


linkedin = extract_text_from_pdf("me/linkedin.pdf")
name = "Kush Gupta"
summary = get_text_from_file("me/summary.txt")

linkedin_VA_system_prompt = get_linkedin_virtual_assistant(name, summary, linkedin)


def evaluate(answer, question, history):
    evaluator_system_prompt = get_linkedin_virtual_assistant_evaluator(
        name, summary, linkedin
    )
    user_prompt = get_evaluator_user_prompt(answer, question, history)
    response = call_chat_api(
        messages=[
            {"role": "system", "content": evaluator_system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    try:
        eval_resp_json  = response.choices[0].message.content
        data = json.loads(eval_resp_json)
        evaluation = Evaluation(**data)

        print(f"Is acceptable: {evaluation.is_acceptable}")
        print(f"Feedback: {evaluation.feedback}")
        return evaluation
    except Exception as e:
        print("Error parsing evaluation response:", e)
        return Evaluation(is_acceptable=False, feedback="Failed to parse evaluation response.")

def rerun(reply, message, history, feedback):
    updated_system_prompt = linkedin_VA_system_prompt + "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
    updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
    updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
    messages = [{"role": "system", "content": updated_system_prompt}] + history + [{"role": "user", "content": message}]
    response = call_chat_api( messages=messages)
    return response.choices[0].message.content

def chat(message, history):
    print("Received message:", message)
    system = linkedin_VA_system_prompt
    # if "aws" in message:
    #     system = system + "\n\nEverything in your reply needs to be in pig latin - \
    #           it is mandatory that you respond only and entirely in pig latin"
        
    messages = (
        [{"role": "system", "content": system}]
        + history
        + [{"role": "user", "content": message}]
    )
    response = call_chat_api(messages=messages)
    answer = response.choices[0].message.content
    print("Initial answer: ", answer)

    evaluation = evaluate(answer, message, history)
    if evaluation.is_acceptable:
        print("Passed evaluation - returning reply")
    else:
        print("Failed evaluation - retrying")
        answer = rerun(answer, message, history, evaluation.feedback)
        print("New answer after rerun: ", answer)
    return answer



if __name__ == "__main__":
    gr.ChatInterface(chat).launch()
