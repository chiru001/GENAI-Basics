from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv(override=True)

# Initialize GPT-4 client
client_gpt = OpenAI()  # Uses OPENAI_API_KEY from .env

# Initialize DeepSeek client
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
client_deepseek = OpenAI(
    api_key=deepseek_api_key,
    base_url="https://api.deepseek.com"
)

# Load your chain-of-thought prompt
with open('./prompting/chain-of-thought.md', 'r', encoding='utf-8') as file:
    prompt = file.read()

while True:
    query = input("> ").strip()
    if not query:
        continue

    # ---- STEP 1: GPT-4: Analyse, Think, Outpt ----
    gpt_messages = [
        {"role": "system", "content": prompt + "\nFor this query, ONLY provide Analyse, Think, and Outpt steps (not Validate or Result)."},
        {"role": "user", "content": query}
    ]
    response_gpt4_steps = client_gpt.chat.completions.create(
        model="gpt-4.1",
        messages=gpt_messages
    )
    partial_gpt = response_gpt4_steps.choices[0].message.content
    print("\n🤖 GPT-4 (Analyse, Think, Outpt):\n", partial_gpt.strip())

    # ---- STEP 2: DeepSeek: Validate ----
    deepseek_messages = [
        {"role": "system", "content": prompt + "\nFor the following, ONLY perform the 🧠 Validate step (no other steps)."},
        {"role": "user", "content": query},
        {"role": "assistant", "content": partial_gpt}
    ]
    response_deepseek = client_deepseek.chat.completions.create(
        model="deepseek-reasoner",  # or "deepseek-chat"
        messages=deepseek_messages
    )
    deepseak_validate = response_deepseek.choices[0].message.content
    print("\n🌊 Deepseak Validate:\n", deepseak_validate.strip())

    # ---- STEP 3: GPT-4: Result ----
    gpt_messages_final = [
        {"role": "system", "content": prompt + "\nNow, ONLY provide the Result step (given previous steps and validation)."},
        {"role": "user", "content": query},
        {"role": "assistant", "content": partial_gpt},
        {"role": "assistant", "content": deepseak_validate}
    ]
    response_gpt4_final = client_gpt.chat.completions.create(
        model="gpt-4.1",
        messages=gpt_messages_final
    )
    final_result = response_gpt4_final.choices[0].message.content
    print("\n🤖 GPT-4 (Result):\n", final_result.strip())

    print("\n" + "-"*40 + "\n")
