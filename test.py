import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
key = os.getenv("GEMINI_API_KEY")

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

data = {
    "contents": [
        {
            "parts": [{"text": "Write a simple Dockerfile for a Python Flask app"}]
        }
    ]
}

headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": key
}
r = requests.post(url, headers=headers, json=data)
print(r.status_code)
print(r.json())
