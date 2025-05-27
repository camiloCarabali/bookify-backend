from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.review import Review
from app.models.book import Book
from app.schemas.review import ReviewCreate, ReviewOut
from app.dependencies.auth import get_current_user
from app.models.user import User
from typing import List
from sqlalchemy import func

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewOut)
def create_review(
        review: ReviewCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == review.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    existing_review = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.book_id == review.book_id
    ).first()

    if existing_review:
        raise HTTPException(
            status_code=400,
            detail="Ya has enviado una reseña para este libro"
        )

    new_review = Review(
        comentario=review.comentario,
        calificacion=review.calificacion,
        user_id=current_user.id,
        book_id=review.book_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.get("/book/{book_id}", response_model=List[ReviewOut])
def get_reviews_for_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.book_id == book_id).all()


@router.put("/{review_id}", response_model=ReviewOut)
def update_review(
        review_id: int,
        updated_data: ReviewCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review no encontrado")

    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este review")

    review.comentario = updated_data.comentario
    review.calificacion = updated_data.calificacion
    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}")
def delete_review(
        review_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review no encontrado")

    if review.user_id != current_user.id and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta reseña")

    db.delete(review)
    db.commit()
    return {"detail": "Review eliminado correctamente"}


@router.get("/book/{book_id}/rating")
def get_average_rating(book_id: int, db: Session = Depends(get_db)):
    promedio = db.query(func.avg(Review.calificacion)) \
        .filter(Review.book_id == book_id).scalar()

    if promedio is None:
        raise HTTPException(status_code=404, detail="Este libro no tiene reviews")

    return {"book_id": book_id, "average_rating": round(promedio, 2)}


@router.get("/book/{book_id}/stats")
def get_review_stats(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    avg_rating, total_reviews = db.query(
        func.avg(Review.calificacion),
        func.count(Review.id)
    ).filter(Review.book_id == book_id).first()

    return {
        "book_id": book_id,
        "titulo": book.title,
        "promedio_calificacion": round(avg_rating, 2) if avg_rating else 0,
        "total_reviews": total_reviews
    }
