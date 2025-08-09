from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import json
import requests
import os
import subprocess

load_dotenv()

client = OpenAI()

def run_command(cmd: str):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return f"Command executed successfully. Output: {result.stdout}"
        else:
            return f"Command failed with error: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Command timed out"
    except Exception as e:
        return f"Error executing command: {str(e)}"

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    
    return "Something went wrong"

def create_file(params):
    """Handle file creation with dictionary parameters"""
    try:
        if isinstance(params, dict):
            filename = params.get('filename')
            content = params.get('content')
        else:
            # If it's a string, treat as filename with empty content
            filename = params
            content = ""
            
        if not filename:
            return "Error: filename is required"
            
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"File {filename} created successfully"
    except Exception as e:
        return f"Error creating file: {str(e)}"

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command,
    "create_file": create_file
}

with open('./prompting/weather-agent.md', 'r', encoding='utf-8') as file:
    prompt = file.read()
    messages = [{"role": "system", "content": prompt}]

while True:
    query = input("> ")
    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=messages
        )

        messages.append({"role": "assistant", "content": response.choices[0].message.content})
        
        try:
            parsed_response = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            print("❌: Failed to parse JSON response")
            break

        if parsed_response.get("step") == "plan":
            print(f"🧠: {parsed_response.get('content')}")
            continue

        if parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            print(f"🛠️: Calling Tool:{tool_name} with input {tool_input}")

            if tool_name in available_tools:
                output = available_tools[tool_name](tool_input)
                messages.append({"role": "user", "content": json.dumps({"step": "observe", "output": output})})
                continue
            else:
                print(f"❌: Tool '{tool_name}' not found")
                break
        
        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get('content')}")
            break
