from fastapi import Depends, FastAPI, HTTPException
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from api.events.router import router as events_router
from api.users.models import User
from api.users.schemas import UserCreate, UserResponse
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Events and Users API")
password_hash = PasswordHash.recommended()

app.include_router(events_router)


@app.get("/users", response_model=list[UserResponse], tags=["users"])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    tags=["users"],
)
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
        contrasena_hash=password_hash.hash(data.contrasena.get_secret_value()),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.put(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["users"],
)
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
    user.contrasena_hash = password_hash.hash(data.contrasena.get_secret_value())

    db.commit()
    db.refresh(user)

    return user


@app.delete("/users/{user_id}", tags=["users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
