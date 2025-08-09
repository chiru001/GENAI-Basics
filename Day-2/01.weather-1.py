from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
load_dotenv()
client = OpenAI()

date = datetime.now()
print(f'Current date: {date}')
SYSTEM_PROMPT= """
You are a helpful AI Assistant.

IMPORTANT: The actual current date and time is {date.strftime("%A, %B %d, %Y at %I:%M %p")}.
You must ONLY use this date when asked about today's date. 
Do NOT use any other date from your training data.

tirupati Weather is 32 degress
"""
response = client.responses.create(
    model="gpt-4.1",
    input=[
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role":"user", "content": "what is the weather in tirupati"},
        ]
)

print(response.output_text)