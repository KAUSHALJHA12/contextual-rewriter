# Placeholder for rewriting logic
# backend/rewriter.py

import openai
from utils import chunk_text, format_prompt

openai.api_key = "YOUR_OPENAI_API_KEY"

def rewrite_chunk(chunk: str, context: str) -> str:
    prompt = format_prompt(chunk, context)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful rewriting assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()

def rewrite_text(text: str, context: str, chunked: bool = False) -> str:
    if not chunked:
        return rewrite_chunk(text, context)
    
    chunks = chunk_text(text)
    rewritten = [rewrite_chunk(c, context) for c in chunks]
    return "\n\n".join(rewritten)
