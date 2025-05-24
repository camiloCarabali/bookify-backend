import os
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.audiobook import Audiobook
from app.models.book import Book
from app.schemas.audiobook import AudiobookOut
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/audiobooks", tags=["Audiobooks"])

UPLOAD_DIR = "uploads/audio"

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
