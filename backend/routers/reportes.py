from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from auth import get_current_user, require_admin
import models

router = APIRouter()


@router.get("/resumen")
def resumen(
    db: Session = Depends(get_db),
    _=Depends(require_admin)
):
    total_don  = db.query(models.Donacion).count()
    valor      = db.query(func.sum(models.Donacion.valor_total)).scalar() or 0
    hogares    = db.query(models.Donacion.beneficiario_id).distinct().count()
    empresas   = db.query(models.Donacion.empresa_id).distinct().count()
    pendientes = db.query(models.Donacion).filter_by(estado="Pendiente").count()

    return {
        "total_donaciones":  total_don,
        "valor_total":       float(valor),
        "hogares_atendidos": hogares,
        "empresas_activas":  empresas,
        "pendientes":        pendientes
    }


@router.get("/por-mes")
def por_mes(
    anio: int = Query(default=2026),
    db: Session = Depends(get_db),
    _=Depends(require_admin)
):
    rows = (
        db.query(
            func.substr(models.Donacion.fecha, 1, 7).label("mes"),
            func.count(models.Donacion.id).label("cantidad"),
            func.sum(models.Donacion.valor_total).label("valor")
        )
        .filter(models.Donacion.fecha.like(f"{anio}%"))
        .group_by("mes")
        .order_by("mes")
        .all()
    )
    return [
        {"mes": r.mes, "cantidad": r.cantidad, "valor": float(r.valor or 0)}
        for r in rows
    ]


@router.get("/por-categoria")
def por_categoria(
    db: Session = Depends(get_db),
    _=Depends(require_admin)
):
    rows = (
        db.query(
            models.ItemDonacion.categoria,
            func.sum(models.ItemDonacion.valor_est).label("valor")
        )
        .group_by(models.ItemDonacion.categoria)
        .order_by(func.sum(models.ItemDonacion.valor_est).desc())
        .all()
    )
    return [
        {"categoria": r.categoria or "Sin categoría", "valor": float(r.valor or 0)}
        for r in rows
    ]


@router.get("/top-empresas")
def top_empresas(
    limit: int = Query(default=5),
    db: Session = Depends(get_db),
    _=Depends(require_admin)
):
    rows = (
        db.query(
            models.Empresa.razon_social,
            func.count(models.Donacion.id).label("donaciones"),
            func.sum(models.Donacion.valor_total).label("valor")
        )
        .join(models.Donacion, models.Empresa.id == models.Donacion.empresa_id)
        .group_by(models.Empresa.id)
        .order_by(func.sum(models.Donacion.valor_total).desc())
        .limit(limit)
        .all()
    )
    return [
        {"empresa": r.razon_social, "donaciones": r.donaciones, "valor": float(r.valor or 0)}
        for r in rows
    ]


@router.get("/por-ciudad")
def por_ciudad(
    db: Session = Depends(get_db),
    _=Depends(require_admin)
):
    rows = (
        db.query(
            models.AdultoMayor.ciudad,
            func.count(models.Donacion.beneficiario_id).label("hogares")
        )
        .join(models.Donacion, models.AdultoMayor.id == models.Donacion.beneficiario_id)
        .group_by(models.AdultoMayor.ciudad)
        .order_by(func.count(models.Donacion.beneficiario_id).desc())
        .all()
    )
    return [
        {"ciudad": r.ciudad or "Sin ciudad", "hogares": r.hogares}
        for r in rows
    ]


@router.get("/urgencia-beneficiarios")
def urgencia_beneficiarios(
    db: Session = Depends(get_db),
    _=Depends(require_admin)
):
    rows = (
        db.query(
            models.AdultoMayor.urgencia,
            func.count(models.AdultoMayor.id).label("total")
        )
        .filter_by(activo=1)
        .group_by(models.AdultoMayor.urgencia)
        .all()
    )
    return [{"urgencia": r.urgencia, "total": r.total} for r in rows]