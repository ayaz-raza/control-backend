import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("Gemini Key Loaded:", GEMINI_API_KEY)

genai.configure(
    api_key=GEMINI_API_KEY
)

# Load Model
model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

def get_ai_diagnosis(pcode):

    prompt = f"""
    You are an expert EV diagnostic assistant.

    Return ONLY valid JSON.

    Format:

    {{
      "description": "",
      "causes": "",
      "vehicle_reaction": "",
      "remedies": ""
    }}

    P-Code: {pcode}

    Keep the response concise and relevant.
    """
    print("Calling Gemini for:", pcode)

    try:
        response = model.generate_content(prompt)
        print("Gemini Response:")
        print(response.text)
    except Exception as e:
        print("Gemini Error:", e)
        raise

    text = response.text.strip()

    # Remove markdown code blocks if Gemini returns them
    if text.startswith("```json"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)