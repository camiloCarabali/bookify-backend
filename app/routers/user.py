from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.role import Role
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.database import get_db
from app.utils.security import hash_password
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_pwd = hash_password(user.password)

    role = db.query(Role).filter(Role.name == (user.role_name or "user")).first()
    if not role:
        raise HTTPException(status_code=400, detail=f"Rol '{user.role_name}' no existe")

    new_user = User(
        email=user.email,
        username=user.username,
        password=hashed_pwd,
        role_id=role.id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[UserOut])
def get_users(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return db.query(User).all()


@router.get("/me", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
