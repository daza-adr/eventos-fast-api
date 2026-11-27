from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(320), nullable=False, unique=True, index=True)
    contrasena_hash = Column(String(255), nullable=False)
