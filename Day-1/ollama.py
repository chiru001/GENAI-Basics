import re
from Prompting import one_shot_prompt
import requests

OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"


def build_ollama_messages():
    return [
        {"role": "system", "content": one_shot_prompt()},
        {"role": "user",   "content": "hey, my name is chiru"},
        {"role": "user",   "content": "how to make tea "},
    ]

def chat_with_ollama(model, messages):
    payload = {
        "model": model,                 
        "messages": messages,
        "stream": False
    }
    res = requests.post(OLLAMA_API_URL, json=payload)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]
    
if __name__ == "__main__":
    answer = chat_with_ollama("qwen3:14b", build_ollama_messages())
    print(answer)



