from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
import asyncio
from typing import Optional

# Load environment variables
load_dotenv()

app = FastAPI(
    title="TTS Server",
    description="A FastAPI server that integrates with Murf's TTS API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str
    voice_id: Optional[str] = "en-US-Neural2-F"  # Default voice
    speed: Optional[float] = 1.0
    pitch: Optional[float] = 0.0

class TTSResponse(BaseModel):
    success: bool
    audio_url: Optional[str] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint with server information"""
    return {
        "message": "TTS Server is running!",
        "endpoints": {
            "POST /tts": "Generate TTS audio from text",
            "GET /docs": "Interactive API documentation"
        }
    }

@app.post("/tts", response_model=TTSResponse)
async def generate_tts(request: TTSRequest):
    """
    Generate TTS audio using Murf's REST API
    
    Args:
        request: TTSRequest object containing text and optional parameters
        
    Returns:
        TTSResponse with audio URL or error message
    """
    try:
        # Get API key from environment
        api_key = os.getenv("MURF_API_KEY")
        api_url = os.getenv("MURF_API_URL", "https://api.murf.ai/v1")
        
        if not api_key:
            raise HTTPException(
                status_code=500, 
                detail="MURF_API_KEY not configured in environment variables"
            )
        
        # Prepare request payload for Murf API
        payload = {
            "text": request.text,
            "voiceId": request.voice_id,
            "speed": request.speed,
            "pitch": request.pitch,
            "format": "mp3"
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Make request to Murf API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{api_url}/generate",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                audio_url = data.get("audioUrl")
                
                if audio_url:
                    return TTSResponse(
                        success=True,
                        audio_url=audio_url
                    )
                else:
                    return TTSResponse(
                        success=False,
                        error="No audio URL received from Murf API"
                    )
            else:
                error_detail = f"Murf API error: {response.status_code} - {response.text}"
                return TTSResponse(
                    success=False,
                    error=error_detail
                )
                
    except httpx.TimeoutException:
        return TTSResponse(
            success=False,
            error="Request to Murf API timed out"
        )
    except httpx.RequestError as e:
        return TTSResponse(
            success=False,
            error=f"Network error: {str(e)}"
        )
    except Exception as e:
        return TTSResponse(
            success=False,
            error=f"Unexpected error: {str(e)}"
        )

@app.post("/tts-form")
async def generate_tts_form(
    text: str = Form(...),
    voice_id: str = Form("en-US-Neural2-F"),
    speed: float = Form(1.0),
    pitch: float = Form(0.0)
):
    """
    Alternative endpoint that accepts form data instead of JSON
    Useful for testing with HTML forms or Postman
    """
    request = TTSRequest(
        text=text,
        voice_id=voice_id,
        speed=speed,
        pitch=pitch
    )
    return await generate_tts(request)

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"Starting TTS Server on {host}:{port}")
    print("Make sure to set your MURF_API_KEY in the .env file")
    print("Access the API documentation at: http://localhost:8000/docs")
    
    uvicorn.run(app, host=host, port=port) 