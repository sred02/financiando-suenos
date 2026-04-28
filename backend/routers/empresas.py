from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

# GET /empresas → listar todos
@router.get("/")
def listar_empresas(db: Session = Depends(get_db)):
    return db.query(models.Empresa).filter_by(activo=1).all()

# GET /empresas/{id} → obtener uno
@router.get("/{empresa_id}")
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(models.Empresa).filter_by(id=empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="No encontrado")
    return empresa

# POST /empresas → crear
@router.post("/")
def crear_empresa(datos: dict, db: Session = Depends(get_db)):
    empresa = models.Empresa(**datos)
    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    return empresa

# PUT /empresas/{id} → actualizar
@router.put("/{empresa_id}")
def actualizar_empresa(empresa_id: int, datos: dict, db: Session = Depends(get_db)):
    empresa = db.query(models.Empresa).filter_by(id=empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="No encontrado")
    for key, value in datos.items():
        setattr(empresa, key, value)
    db.commit()
    return empresa
