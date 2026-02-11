import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
if key:
    print(f"Key found! Length: {len(key)}")
    print(f"Key starts with: {key[:10]}")
    print(f"Key ends with: {key[-4:]}")
else:
    print("NO OPENAI_API_KEY FOUND IN ENVIRONMENT")
