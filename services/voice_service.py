import requests
import os
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

def speech_to_text(audio_path):

    url = "https://api.sarvam.ai/speech-to-text"

    headers = {
        "api-subscription-key": SARVAM_API_KEY
    }

    with open(audio_path, "rb") as audio_file:

        files = {
            "file": (
                os.path.basename(audio_path),
                audio_file,
                "audio/wav"
            )
        }

        data = {
            "language_code": "en-IN",
            "model": "saarika:v2.5"
        }

        response = requests.post(
            url,
            headers=headers,
            files=files,
            data=data
        )

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    try:
        result = response.json()
    except Exception:
        return None

    if "transcript" in result:
        return result["transcript"]

    return None