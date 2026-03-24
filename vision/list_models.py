from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY", "").strip()
client = genai.Client(api_key=key)

print("--- Available Models ---")
try:
    for model in client.models.list():
        # Correctly check for generation capabilities in the new SDK
        print(f"- {model.name}")
except Exception as e:
    print(f"Error: {e}")
