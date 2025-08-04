
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from tts_api import app as tts_app

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/tts_api", tts_app)

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")
