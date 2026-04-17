from util import print_pretty
from llm import loop_llm_call
from prompt import get_todo_list_prompt

todos = []
completed = []

def create_todos(descriptions: list[str]) -> str:
    todos.extend(descriptions)
    completed.extend([False] * len(descriptions))
    return get_todo_report()

def get_todo_report() -> str:
    result = ""
    for index, todo in enumerate(todos):
        if completed[index]:
            result += f"Todo #{index + 1}: [green][strike]{todo}[/strike][/green]\n"
        else:
            result += f"Todo #{index + 1}: {todo}\n"
    print_pretty(result)
    return result

def mark_complete(index: int, completion_notes: str) -> str:
    if 1 <= index <= len(todos):
        completed[index - 1] = True
    else:
        return "No todo at this index."
    print_pretty(completion_notes)
    return get_todo_report()

# Import schemas and register after functions are defined
from tools import create_todos_json, mark_complete_json, TOOL_REGISTRY
TOOL_REGISTRY["create_todos"] = create_todos
TOOL_REGISTRY["mark_complete"] = mark_complete

user_message = """"
    A train leaves Boston at 2:00 pm traveling 60 mph.
    Another train leaves New York at 3:00 pm traveling 80 mph toward Boston.
    When do they meet?
    """
messages = [{ "role": "system", "content": get_todo_list_prompt() }, { "role": "user", "content": user_message }]

tools = [{"type": "function", "function": create_todos_json},
        {"type": "function", "function": mark_complete_json}]

print_pretty(loop_llm_call(messages, tools))