from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import tempfile

from services.pdf_service import generate_pdf
from services.database import (
    get_pcode_details,
    get_ftb_list,
    get_pcode_ftb_details
)
from services.ai_service import get_ai_diagnosis
from services.voice_service import speech_to_text
from pydub import AudioSegment
from pydub.utils import which
import os

# Automatically find FFmpeg installed on the server
AudioSegment.converter = "ffmpeg"


app = FastAPI(
    title="Acontrol Diagnostic API"
)

@app.get("/")
def home():
    return {
        "message": "Acontrol API Running"
    }

@app.get("/ftb/{pcode}")
def get_ftbs(pcode):

    ftbs = get_ftb_list(pcode)

    return {
        "pcode": pcode.upper(),
        "ftbs": ftbs
    }

@app.get("/search/{pcode}/{ftb}")
def search_fault_by_ftb(pcode, ftb):

    result = get_pcode_ftb_details(pcode, ftb)

    if result:
        return {
            "source": "database",
            "data": result
        }

    return {
        "error": "No record found"
    }


@app.get("/search/{pcode}")
def search_fault(pcode):

    result = get_pcode_details(pcode)

    if result:
        return {
            "source": "database",
            "data": result
        }

    ai_result = get_ai_diagnosis(pcode)

    return {
        "source": "gemini_ai",
        "data": ai_result
    }


@app.post("/voice-search")
async def voice_search(audio: UploadFile = File(...)):

    # Save uploaded audio temporarily
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temp_file:

        content = await audio.read()


        temp_file.write(content)

        temp_path = temp_file.name

    wav_path = temp_path + ".wav"


    AudioSegment.from_file(temp_path).export(
        wav_path,
        format="wav"
    )


    transcript = speech_to_text(wav_path)

    os.remove(wav_path)
    

    if not transcript:
        return {
            "error": "Could not detect speech"
        }

    import re

    text = transcript.upper()

    # Convert spoken numbers to digits
    text = text.replace("ZERO", "0")
    text = text.replace("ONE", "1")
    text = text.replace("TWO", "2")
    text = text.replace("THREE", "3")
    text = text.replace("FOUR", "4")
    text = text.replace("FIVE", "5")
    text = text.replace("SIX", "6")
    text = text.replace("SEVEN", "7")
    text = text.replace("EIGHT", "8")
    text = text.replace("NINE", "9")

    # Remove commas, spaces and periods
    text = re.sub(r'[^A-Z0-9]', '', text)

    # If transcript starts with digits, assume it is a P-Code
    if text and text[0].isdigit():
        pcode = "P" + text
    else:
        pcode = text


    result = get_pcode_details(pcode)

    if result:
        return {
            "source": "database",
            "detected_code": pcode,
            "data": result
        }

    ai_result = get_ai_diagnosis(pcode)

    return {
        "source": "gemini_ai",
        "detected_code": pcode,
        "data": ai_result
    }

@app.get("/generate-report/{pcode}")
def generate_report(pcode):

    result = get_pcode_details(pcode)

    if result:

        pdf_file = generate_pdf(
            pcode,
            result
        )

        return FileResponse(
            path=pdf_file,
            filename=pdf_file,
            media_type="application/pdf"
        )

    ai_result = get_ai_diagnosis(pcode)

    pdf_file = generate_pdf(
        pcode,
        ai_result
    )

    return FileResponse(
        path=pdf_file,
        filename=pdf_file,
        media_type="application/pdf"
    )
