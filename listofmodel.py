import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("Available Models:\n")

for model in genai.list_models():
    print(f"Model Name : {model.name}")
    print(f"Display Name : {model.display_name}")
    print(f"Description : {model.description}")
    print(f"Supported Methods : {model.supported_generation_methods}")
    print("-" * 80)