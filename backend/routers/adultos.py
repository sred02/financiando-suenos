from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

# GET /adultos → listar todos
@router.get("/")
def listar_adultos(db: Session = Depends(get_db)):
    return db.query(models.AdultoMayor).filter_by(activo=1).all()

# GET /adultos/{id} → obtener uno
@router.get("/{adulto_id}")
def obtener_adulto(adulto_id: int, db: Session = Depends(get_db)):
    adulto = db.query(models.AdultoMayor).filter_by(id=adulto_id).first()
    if not adulto:
        raise HTTPException(status_code=404, detail="No encontrado")
    return adulto

# POST /adultos → crear
@router.post("/")
def crear_adulto(datos: dict, db: Session = Depends(get_db)):
    adulto = models.AdultoMayor(**datos)
    db.add(adulto)
    db.commit()
    db.refresh(adulto)
    return adulto

# PUT /adultos/{id} → actualizar
@router.put("/{adulto_id}")
def actualizar_adulto(adulto_id: int, datos: dict, db: Session = Depends(get_db)):
    adulto = db.query(models.AdultoMayor).filter_by(id=adulto_id).first()
    if not adulto:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in datos.items():
        setattr(adulto, key, value)
    db.commit()
    return adulto