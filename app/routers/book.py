from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.book import BookCreate, BookOut
from app.models.book import Book, AudioBook
from app.models.user import User
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Crear el libro
    new_book = Book(
        title=book.title,
        author=book.author,
        description=book.description,
        uploaded_by=current_user.id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    if book.audio_url:
        audio = AudioBook(
            audio_url=book.audio_url,
            book_id=new_book.id
        )
        db.add(audio)
        db.commit()
        db.refresh(audio)

    return new_book


@router.get("/", response_model=List[BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book
