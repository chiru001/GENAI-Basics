from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI()

# Load your persona prompt
with open('./prompting/persona.md', 'r', encoding='utf-8') as file:
    prompt = file.read()



while True:
    query = input("You: ").strip()
    if not query:
        continue

    # Use only the system prompt and the latest user message (trim chat history!)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": query}
    ]

    response = client.chat.completions.create(
        model="gpt-4.1",  # or use a smaller model if you prefer
        messages=messages
    )

    reply = response.choices[0].message.content
    print("GF:", reply)
