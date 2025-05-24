import os
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.audiobook import Audiobook
from app.models.book import Book
from app.schemas.audiobook import AudiobookOut
from app.dependencies.auth import get_current_user
from app.models.user import User
from fastapi.responses import FileResponse
from typing import List

router = APIRouter(prefix="/audiobooks", tags=["Audiobooks"])

UPLOAD_DIR = os.path.join("app", "uploads", "audio")

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=AudiobookOut)
def upload_audiobook(
        book_id: int = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden subir audiolibros")

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    filename = f"{book_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    audio = Audiobook(file_path=file_path, book_id=book_id)
    db.add(audio)
    db.commit()
    db.refresh(audio)
    return audio


@router.get("/", response_model=List[AudiobookOut])
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
