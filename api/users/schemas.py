from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr


class UserCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr
    contrasena: SecretStr = Field(
        alias="contraseña",
        min_length=8,
        max_length=128,
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: EmailStr
