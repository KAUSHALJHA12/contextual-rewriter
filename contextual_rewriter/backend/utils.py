# Placeholder for utility functions
import textwrap
from docx import Document

def chunk_text(text: str, max_length: int = 1000) -> list:
    return textwrap.wrap(text, width=max_length, break_long_words=False)

def format_prompt(text: str, context: str) -> str:
    return f"Rewrite the following in a {context} tone:\n\n{text}\n\nRewritten:"

def format_time(dt) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])
