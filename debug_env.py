import os
from dotenv import load_dotenv

print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir("."))

# Try to load .env
load_dotenv(dotenv_path=".env")
key = os.getenv("GEMINI_API_KEY")

print(f"API Key loaded: {key}")
print(f"API Key length: {len(key) if key else 0}")
print(f"API Key starts with: {key[:10] if key else 'None'}")

# Also try without explicit path
load_dotenv()
key2 = os.getenv("GEMINI_API_KEY")
print(f"API Key (without path): {key2}") 