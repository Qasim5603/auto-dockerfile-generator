import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
key = os.getenv("GEMINI_API_KEY")

if not key:
    print("No API key found!")
    exit(1)

print(f"Using API key: {key[:10]}...")

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

data = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Explain how AI works in a few words"
                }
            ]
        }
    ]
}

headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": key
}

print("Making request...")
print(f"URL: {url}")
print(f"Headers: {headers}")
print(f"Data: {data}")

try:
    r = requests.post(url, headers=headers, json=data)
    print(f"Status code: {r.status_code}")
    print(f"Response: {r.json()}")
except Exception as e:
    print(f"Error: {e}") 