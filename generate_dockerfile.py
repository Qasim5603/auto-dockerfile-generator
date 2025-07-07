import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv(dotenv_path=".env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API configuration
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Files that indicate a project's tech stack
CONFIG_FILES = [
    "package.json",        # Node.js
    "requirements.txt",    # Python
    "setup.py",            # Python
    "Pipfile",             # Python
    "pom.xml",             # Java
    "go.mod",              # Go
    "Gemfile"              # Ruby
]

# Folders we should not scan
EXCLUDED_DIRS = {
    ".git", ".github", "__pycache__", "node_modules", ".venv", ".idea", ".mypy_cache",
    "venv", ".pytest_cache", ".vscode", ".DS_Store", "build", "dist"
}


def get_target_dirs(base_path="."):
    """Get top-level directories that might contain microservices"""
    return [
        name for name in os.listdir(base_path)
        if os.path.isdir(name) and name not in EXCLUDED_DIRS
    ]


def detect_config_files(service_path):
    """Find which known config files exist in the given service folder"""
    return [
        file for file in CONFIG_FILES
        if os.path.isfile(os.path.join(service_path, file))
    ]


def build_prompt(service_path, config_files):
    """Generate a strict and production-focused prompt for Gemini"""
    parts = [f"""
You are a DevOps expert.

Generate a **production-grade Dockerfile** for the project located at `{service_path}` based on the following configuration file(s).

---
🎯 Output Requirements:
- **Detect** whether the project is a Node.js frontend (like React, Vue) or a Python Flask backend.
- **Do NOT ask questions. Do NOT explain.** Just output the final Dockerfile.
- Use **multi-stage builds** when needed.
- Ensure:
    - **Non-root user** in final image
    - **HEALTHCHECK**
    - **gunicorn** for Python apps
    - **nginx** for frontend static builds
- Output **only** the Dockerfile. No markdown or explanations.

📦 Configuration Files:
"""]

    for file in config_files:
        parts.append(f"\n# {file}\n")
        with open(os.path.join(service_path, file), "r", encoding="utf-8") as f:
            parts.append(f.read())

    return "\n".join(parts)


def call_gemini(prompt):
    """Send prompt to Gemini API and return Dockerfile text"""
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]


def write_dockerfile(service_path, dockerfile_content):
    """Write Dockerfile into the service folder, overwrite if exists"""
    output_path = os.path.join(service_path, "Dockerfile")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(dockerfile_content.strip() + "\n")
    print(f"[✅] Dockerfile written to: {output_path}")


def main():
    print("🔍 Scanning for services...")
    service_dirs = get_target_dirs()
    if not service_dirs:
        print("⚠️ No valid service directories found.")
        return

    for service in service_dirs:
        print(f"\n📁 Processing: {service}")
        config_files = detect_config_files(service)
        if not config_files:
            print(f"⚠️ No recognizable config files found in: {service}")
            continue
        prompt = build_prompt(service, config_files)
        try:
            dockerfile_content = call_gemini(prompt)
            write_dockerfile(service, dockerfile_content)
        except Exception as e:
            print(f"❌ Failed to generate Dockerfile for {service}: {e}")


if __name__ == "__main__":
    main()
