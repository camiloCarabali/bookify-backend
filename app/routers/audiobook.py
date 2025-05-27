import os
from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
from app.database import get_db
from app.models.audiobook import Audiobook
from app.models.book import Book
from app.schemas.audiobook import AudiobookOut
from app.dependencies.security import validate_audio_file, get_current_admin

router = APIRouter(prefix="/audiobooks", tags=["Audiobooks"])

UPLOAD_DIR = os.path.join("app", "uploads", "audio")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=AudiobookOut)
def upload_audiobook(
        book_id: int = Form(...),
        file: UploadFile = Depends(validate_audio_file),
        db: Session = Depends(get_db),
        _: dict = Depends(get_current_admin)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    existing_audio = db.query(Audiobook).filter(Audiobook.book_id == book_id).first()
    if existing_audio:
        raise HTTPException(status_code=400, detail="Este libro ya tiene un audiolibro")

    filename = f"{book_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    audio = Audiobook(file_path=file_path, book_id=book_id)
    db.add(audio)
    db.commit()
    db.refresh(audio)
    return audio


@router.get("/", response_model=list[AudiobookOut])
def list_audiobooks(db: Session = Depends(get_db)):
    return db.query(Audiobook).all()


@router.get("/{audiobook_id}", response_model=AudiobookOut)
def get_audiobook(audiobook_id: int, db: Session = Depends(get_db)):
    audio = db.query(Audiobook).filter(Audiobook.id == audiobook_id).first()
    if not audio:
        raise HTTPException(status_code=404, detail="Audiolibro no encontrado")
    return audio


@router.get("/{audiobook_id}/audio")
def get_audiobook_file(audiobook_id: int, db: Session = Depends(get_db)):
    audio = db.query(Audiobook).filter(Audiobook.id == audiobook_id).first()
    if not audio or not os.path.exists(audio.file_path):
        raise HTTPException(status_code=404, detail="Archivo de audio no encontrado")

    return FileResponse(path=audio.file_path, media_type="audio/mpeg", filename=os.path.basename(audio.file_path))
