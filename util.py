from pypdf import PdfReader
from rich.console import Console

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_text_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def print_pretty(text):
    try:
        Console().print(text)
    except Exception:
        print(text)