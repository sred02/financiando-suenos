from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import AdultoCreate, AdultoUpdate, AdultoOut
from auth import get_current_user
import models

router = APIRouter()


@router.get("/", response_model=List[AdultoOut])
def listar_adultos(
    ciudad:   Optional[str] = None,
    urgencia: Optional[str] = None,
    activo:   int = 1,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    q = db.query(models.AdultoMayor).filter_by(activo=activo)
    if ciudad:
        q = q.filter(models.AdultoMayor.ciudad == ciudad)
    if urgencia:
        q = q.filter(models.AdultoMayor.urgencia == urgencia)
    return q.order_by(models.AdultoMayor.id.desc()).all()


@router.get("/{adulto_id}", response_model=AdultoOut)
def obtener_adulto(
    adulto_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    adulto = db.query(models.AdultoMayor).filter_by(id=adulto_id).first()
    if not adulto:
        raise HTTPException(status_code=404, detail="Beneficiario no encontrado")
    return adulto


@router.post("/", response_model=AdultoOut, status_code=201)
def crear_adulto(
    datos: AdultoCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    existe = db.query(models.AdultoMayor).filter_by(
        identificacion=datos.identificacion
    ).first()
    if existe:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un beneficiario con la identificación {datos.identificacion}"
        )
    try:
        adulto = models.AdultoMayor(**datos.model_dump())
        db.add(adulto)
        db.commit()
        db.refresh(adulto)
        return adulto
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{adulto_id}", response_model=AdultoOut)
def actualizar_adulto(
    adulto_id: int,
    datos: AdultoUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    adulto = db.query(models.AdultoMayor).filter_by(id=adulto_id).first()
    if not adulto:
        raise HTTPException(status_code=404, detail="Beneficiario no encontrado")
    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(adulto, campo, valor)
    db.commit()
    db.refresh(adulto)
    return adulto


@router.delete("/{adulto_id}")
def eliminar_adulto(
    adulto_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    adulto = db.query(models.AdultoMayor).filter_by(id=adulto_id).first()
    if not adulto:
        raise HTTPException(status_code=404, detail="Beneficiario no encontrado")
    db.delete(adulto)
    db.commit()
    return {"ok": True, "mensaje": "Beneficiario eliminado"}