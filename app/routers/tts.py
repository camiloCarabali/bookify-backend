import os
from fastapi import APIRouter, HTTPException, Query
from gtts import gTTS
from fastapi.responses import FileResponse

router = APIRouter(prefix="/tts", tags=["Text-to-Speech"])

TTS_DIR = os.path.join("app", "uploads", "tts")
os.makedirs(TTS_DIR, exist_ok=True)


@router.get("/", response_class=FileResponse)
def text_to_speech(text: str = Query(..., min_length=5, max_length=1000)):
    try:
        tts = gTTS(text=text, lang="es")
        file_path = os.path.join(TTS_DIR, "tts_output.mp3")
        tts.save(file_path)
        return FileResponse(file_path, media_type="audio/mpeg", filename="tts_output.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
