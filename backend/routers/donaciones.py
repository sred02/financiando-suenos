from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import DonacionCreate, DonacionUpdate, DonacionOut
from auth import get_current_user
import models

router = APIRouter()


def _generar_folio(db: Session) -> str:
    from datetime import datetime
    anio  = datetime.now().year
    total = db.query(models.Donacion).count()
    return f"CF-{anio}-{str(total + 1).zfill(3)}"


@router.get("/", response_model=List[DonacionOut])
def listar_donaciones(
    empresa_id:      int = Query(default=None),
    beneficiario_id: int = Query(default=None),
    estado:          str = Query(default=None),
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    q = db.query(models.Donacion)

    if current_user.rol == "empresa":
        mi_empresa = db.query(models.Empresa).filter_by(
            usuario_id=current_user.id
        ).first()
        if mi_empresa:
            q = q.filter_by(empresa_id=mi_empresa.id)
    else:
        if empresa_id:
            q = q.filter_by(empresa_id=empresa_id)

    if beneficiario_id:
        q = q.filter_by(beneficiario_id=beneficiario_id)
    if estado:
        q = q.filter_by(estado=estado)

    return q.order_by(models.Donacion.id.desc()).all()


@router.get("/{donacion_id}", response_model=DonacionOut)
def obtener_donacion(
    donacion_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    don = db.query(models.Donacion).filter_by(id=donacion_id).first()
    if not don:
        raise HTTPException(status_code=404, detail="Donación no encontrada")
    return don


@router.post("/", response_model=DonacionOut, status_code=201)
def crear_donacion(
    datos: DonacionCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    empresa = db.query(models.Empresa).filter_by(id=datos.empresa_id, activo=1).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    beneficiario = db.query(models.AdultoMayor).filter_by(
        id=datos.beneficiario_id, activo=1
    ).first()
    if not beneficiario:
        raise HTTPException(status_code=404, detail="Beneficiario no encontrado")

    valor_total = sum(item.valor_est or 0 for item in datos.items)

    donacion = models.Donacion(
        folio=_generar_folio(db),
        empresa_id=datos.empresa_id,
        beneficiario_id=datos.beneficiario_id,
        fecha=datos.fecha,
        modalidad=datos.modalidad,
        observaciones=datos.observaciones,
        valor_total=valor_total,
        estado="Registrada"
    )
    db.add(donacion)
    db.flush()

    for item in datos.items:
        db.add(models.ItemDonacion(
            donacion_id=donacion.id,
            **item.model_dump()
        ))

    db.commit()
    db.refresh(donacion)
    return donacion


@router.put("/{donacion_id}", response_model=DonacionOut)
def actualizar_donacion(
    donacion_id: int,
    datos: DonacionUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    don = db.query(models.Donacion).filter_by(id=donacion_id).first()
    if not don:
        raise HTTPException(status_code=404, detail="Donación no encontrada")

    for campo, valor in datos.model_dump(exclude_none=True).items():
        setattr(don, campo, valor)

    db.commit()
    db.refresh(don)
    return don


@router.delete("/{donacion_id}")
def eliminar_donacion(
    donacion_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    don = db.query(models.Donacion).filter_by(id=donacion_id).first()
    if not don:
        raise HTTPException(status_code=404, detail="Donación no encontrada")
    db.delete(don)
    db.commit()
    return {"ok": True}
