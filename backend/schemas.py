from pydantic import BaseModel
from typing import Optional, List


# ── AUTH ──────────────────────────────────────────────────────────────────────
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


# ── EMPRESA ───────────────────────────────────────────────────────────────────
class EmpresaCreate(BaseModel):
    razon_social:  str
    nit:           str
    sector:        Optional[str] = None
    tamano:        Optional[str] = None
    representante: Optional[str] = None
    cargo:         Optional[str] = None
    telefono:      Optional[str] = None
    direccion:     Optional[str] = None
    correo:        str
    password:      str

class EmpresaOut(BaseModel):
    id:            int
    razon_social:  str
    nit:           str
    sector:        Optional[str] = None
    representante: Optional[str] = None
    cargo:         Optional[str] = None
    telefono:      Optional[str] = None
    direccion:     Optional[str] = None
    activo:        int

    model_config = {"from_attributes": True}


# ── ADULTO MAYOR ──────────────────────────────────────────────────────────────
class AdultoCreate(BaseModel):
    nombre:         str
    identificacion: str
    fecha_nac:      Optional[str] = None
    genero:         Optional[str] = None
    direccion:      Optional[str] = None
    ciudad:         Optional[str] = None
    barrio:         Optional[str] = None
    telefono:       Optional[str] = None
    acudiente:      Optional[str] = None
    necesidades:    Optional[str] = None
    descripcion:    Optional[str] = None
    urgencia:       Optional[str] = "Media"
    tipo_vivienda:  Optional[str] = None

class AdultoUpdate(BaseModel):
    nombre:        Optional[str] = None
    fecha_nac:     Optional[str] = None
    genero:        Optional[str] = None
    direccion:     Optional[str] = None
    ciudad:        Optional[str] = None
    barrio:        Optional[str] = None
    telefono:      Optional[str] = None
    acudiente:     Optional[str] = None
    necesidades:   Optional[str] = None
    descripcion:   Optional[str] = None
    urgencia:      Optional[str] = None
    tipo_vivienda: Optional[str] = None
    activo:        Optional[int] = None

class AdultoOut(BaseModel):
    id:             int
    nombre:         str
    identificacion: str
    fecha_nac:      Optional[str] = None
    genero:         Optional[str] = None
    direccion:      Optional[str] = None
    ciudad:         Optional[str] = None
    barrio:         Optional[str] = None
    telefono:       Optional[str] = None
    acudiente:      Optional[str] = None
    necesidades:    Optional[str] = None
    descripcion:    Optional[str] = None
    urgencia:       str = "Media"
    tipo_vivienda:  Optional[str] = None
    activo:         int

    model_config = {"from_attributes": True}


# ── DONACIÓN ──────────────────────────────────────────────────────────────────
class ItemCreate(BaseModel):
    categoria:   Optional[str] = None
    descripcion: Optional[str] = None
    cantidad:    Optional[int] = 1
    unidad:      Optional[str] = None
    valor_est:   Optional[float] = 0

class ItemOut(BaseModel):
    id:          int
    categoria:   Optional[str] = None
    descripcion: Optional[str] = None
    cantidad:    Optional[int] = None
    unidad:      Optional[str] = None
    valor_est:   Optional[float] = None

    model_config = {"from_attributes": True}

class DonacionCreate(BaseModel):
    empresa_id:      int
    beneficiario_id: int
    fecha:           str
    modalidad:       Optional[str] = None
    observaciones:   Optional[str] = None
    items:           List[ItemCreate] = []

class DonacionUpdate(BaseModel):
    estado:        Optional[str] = None
    observaciones: Optional[str] = None

class DonacionOut(BaseModel):
    id:              int
    folio:           str
    empresa_id:      int
    beneficiario_id: int
    fecha:           str
    modalidad:       Optional[str] = None
    observaciones:   Optional[str] = None
    valor_total:     float
    estado:          str
    items:           List[ItemOut] = []
    empresa:         Optional[EmpresaOut] = None
    beneficiario:    Optional[AdultoOut] = None

    model_config = {"from_attributes": True}


# ── REPORTES ──────────────────────────────────────────────────────────────────
class ResumenReporte(BaseModel):
    total_donaciones:  int
    valor_total:       float
    hogares_atendidos: int
    empresas_activas:  int
    pendientes:        int