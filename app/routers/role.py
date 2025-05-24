from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleOut

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RoleOut)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.name == role.name).first()
    if db_role:
        raise HTTPException(status_code=400, detail="El rol ya existe")
    new_role = Role(name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


@router.get("/", response_model=List[RoleOut])
def list_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()
