from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.models.book import Book
from app.schemas.category import CategoryCreate, CategoryOut
from app.dependencies.auth import get_current_user
from app.models.user import User
from typing import List

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryOut)
def create_category(
        category: CategoryCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden crear categorías")

    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="La categoría ya existe")

    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.post("/assign")
def assign_category_to_book(
        book_id: int,
        category_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden asignar categorías")

    book = db.query(Book).filter(Book.id == book_id).first()
    category = db.query(Category).filter(Category.id == category_id).first()

    if not book or not category:
        raise HTTPException(status_code=404, detail="Libro o categoría no encontrados")

    if category in book.categories:
        raise HTTPException(status_code=400, detail="Categoría ya asignada al libro")

    book.categories.append(category)
    db.commit()
    return {"detail": "Categoría asignada al libro"}
