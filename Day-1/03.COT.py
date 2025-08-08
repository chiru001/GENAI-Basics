from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI()

# Load your chain-of-thought prompt (examples should include "🧠 Think:")
with open('./prompting/chain-of-thought.md', 'r', encoding='utf-8') as file:
    prompt = file.read()

messages = [
    {"role": "system", "content": prompt}
]

while True:
    query = input("> ")
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )

    reply = response.choices[0].message.content
    print("🤖", reply)

    # Optionally keep appending for an ongoing conversation
    messages.append({"role": "assistant", "content": reply})


