from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.favorite import Favorite
from app.models.book import Book
from app.schemas.favorite import FavoriteCreate, FavoriteOut
from app.database import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.post("/", response_model=FavoriteOut)
def add_favorite(fav_data: FavoriteCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == fav_data.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    fav = db.query(Favorite).filter_by(user_id=current_user.id, book_id=book.id).first()
    if fav:
        raise HTTPException(status_code=400, detail="Ya está en favoritos")

    new_fav = Favorite(user_id=current_user.id, book_id=book.id)
    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)
    return new_fav


@router.delete("/{book_id}", status_code=204)
def remove_favorite(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fav = db.query(Favorite).filter_by(user_id=current_user.id, book_id=book_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")

    db.delete(fav)
    db.commit()
    return


@router.get("/", response_model=List[FavoriteOut])
def get_my_favorites(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Favorite).filter_by(user_id=current_user.id).all()
