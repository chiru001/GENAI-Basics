from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI()

#One short prompting
with open('./prompting/zero-short.md', 'r', encoding='utf-8') as file:
    prompt = file.read()
    response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages= [
        {"role":"system", "content":prompt },
        {"role": "user", "content": "hey, my name is chiru"},
        {"role": "user", "content": "why you only talk about python"},
    ]
)

answer = response.choices[0].message.content
print(answer)
