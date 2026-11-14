import json
import os

import ollama
from dotenv import load_dotenv

load_dotenv()

# The local model Ollama will run. Change it in .env with OLLAMA_MODEL=...
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


# 1. The instruction we send with the text when we want a summary
def _summary_prompt(text):
    return (
        "Summarize the following article in simple, clear English. "
        "Write 5 to 8 short sentences that cover the main points only. "
        "Do not add any information that is not in the article.\n\n"
        f"{text}"
    )


# 2. The instruction we send with the text when we want key terms
def _key_terms_prompt(text):
    return (
        "From the following article, find 5 to 8 difficult or important terms. "
        "For each term, give one short, simple meaning in easy English. "
        "Reply ONLY as a JSON list, like this: "
        '[{"term": "inflation", "meaning": "prices going up over time"}]. '
        "Do not add any other text.\n\n"
        f"{text}"
    )


# 3. Get the full summary at once
def generate_summary(text):
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": _summary_prompt(text)}],
    )
    return response["message"]["content"].strip()


# 4. Get the summary piece by piece, as it is being written (for live streaming)
def stream_summary(text):
    stream = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": _summary_prompt(text)}],
        stream=True,
    )
    for chunk in stream:
        piece = chunk["message"]["content"]
        if piece:
            yield piece


# 5. Get the key terms with their meanings
def extract_key_terms(text):
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": _key_terms_prompt(text)}],
    )
    content = response["message"]["content"].strip()
    if content.startswith("```"):
        lines = [line for line in content.splitlines() if not line.strip().startswith("```")]
        content = "\n".join(lines).strip()
    try:
        terms = json.loads(content)
    except json.JSONDecodeError:
        return []
    if not isinstance(terms, list):
        return []
    return [
        {"term": str(item.get("term", "")), "meaning": str(item.get("meaning", ""))}
        for item in terms
        if isinstance(item, dict) and item.get("term") and item.get("meaning")
    ]
