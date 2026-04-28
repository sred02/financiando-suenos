from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from auth import verify_password, create_token
import models

router = APIRouter()


class LoginRequest(BaseModel):
    correo:   str
    password: str
    rol:      str


class LoginResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    rol:          str
    nombre:       str
    correo:       str


@router.post("/login", response_model=LoginResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario por correo
    user = db.query(models.Usuario).filter(
        models.Usuario.correo == datos.correo,
        models.Usuario.activo == 1
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    if not verify_password(datos.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    if user.rol != datos.rol:
        raise HTTPException(
            status_code=403,
            detail="El perfil seleccionado no corresponde a este usuario"
        )

    token = create_token({"sub": user.correo, "rol": user.rol})

    return LoginResponse(
        access_token=token,
        rol=user.rol,
        nombre=user.nombre,
        correo=user.correo
    )


@router.post("/recovery")
def recovery(body: dict, db: Session = Depends(get_db)):
    return {
        "ok": True,
        "mensaje": "Si el correo existe, recibirás un enlace de recuperación."
    }