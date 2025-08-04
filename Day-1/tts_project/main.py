from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

MURF_API_KEY = os.getenv("MURF_API_KEY")

app = FastAPI(
    title="Murf TTS API",
    description="Send text and receive generated voice audio using Murf.ai",
    version="1.0.0"
)

class TextRequest(BaseModel):
    text: str

class TTSResponse(BaseModel):
    message: str
    audio_url: str

@app.post("/tts", response_model=TTSResponse)
async def generate_tts(request: TextRequest):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "apikey": MURF_API_KEY
    }

    payload = {
        "text": request.text,
        "voice": "en-US-Wavenet-D",  # Change as per Murf's supported voices
        "format": "mp3"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.murf.ai/v1/speech/generate",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return {
                "message": "Audio generated successfully!",
                "audio_url": data.get("audio_url", "No URL returned.")
            }
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Error calling Murf API: {str(e)}")
