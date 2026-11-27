from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.users.models import User
from api.users.schemas import UserCreate, UserResponse
from api.users.security import hash_password
from database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.correo == data.correo).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user = User(
        nombre=data.nombre,
        correo=data.correo,
        contrasena_hash=hash_password(data.contrasena.get_secret_value()),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserCreate,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    duplicated = db.query(User).filter(
        User.correo == data.correo,
        User.id != user_id,
    ).first()

    if duplicated:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user.nombre = data.nombre
    user.correo = data.correo
    user.contrasena_hash = hash_password(data.contrasena.get_secret_value())

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
