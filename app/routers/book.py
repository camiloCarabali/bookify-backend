from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app.models.book import Book
from app.models.audiobook import Audiobook
from app.schemas.book import BookCreate, BookOut
from app.models.user import User
from app.dependencies.security import get_current_admin

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookOut, status_code=201)
def create_book(
        book: BookCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_admin)
):
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
        audio = Audiobook(
            audio_url=book.audio_url,
            book_id=new_book.id
        )
        db.add(audio)
        db.commit()
        db.refresh(audio)

    return new_book


@router.get("/", response_model=List[BookOut])
def list_books(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Book).options(
        joinedload(Book.audiobooks),
        joinedload(Book.favorites),
        joinedload(Book.reviews),
        joinedload(Book.categories)
    ).offset(skip).limit(limit).all()


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).options(
        joinedload(Book.audiobooks),
        joinedload(Book.favorites),
        joinedload(Book.reviews),
        joinedload(Book.categories)
    ).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book
