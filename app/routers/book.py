from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app.models.book import Book
from app.models.category import Category
from app.models.user import User
from app.schemas.book import BookCreate, BookOut
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

    if book.category_ids:
        categories = db.query(Category).filter(Category.id.in_(book.category_ids)).all()
        missing_ids = set(book.category_ids) - {c.id for c in categories}

        if not categories:
            raise HTTPException(status_code=404, detail="Categorías no encontradas")

        new_book.categories.extend(categories)

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).options(joinedload(Book.categories)).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book


@router.get("/", response_model=List[BookOut])
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Book).offset(skip).limit(limit).all()
