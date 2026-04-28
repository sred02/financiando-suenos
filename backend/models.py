from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class AdultoMayor(Base):
    __tablename__ = "adultos_mayores"

    id            = Column(Integer, primary_key=True, index=True)
    nombre        = Column(String, nullable=False)
    identificacion = Column(String, unique=True, nullable=False)
    fecha_nac     = Column(String)
    genero        = Column(String)
    ciudad        = Column(String)
    barrio        = Column(String)
    direccion     = Column(String)
    telefono      = Column(String)
    acudiente     = Column(String)
    necesidades   = Column(Text)   
    descripcion   = Column(Text)
    urgencia      = Column(String)
    tipo_vivienda = Column(String)
    activo        = Column(Integer, default=1)

    donaciones = relationship("Donacion", back_populates="beneficiario")


class Empresa(Base):
    __tablename__ = "empresas"

    id             = Column(Integer, primary_key=True, index=True)
    usuario_id     = Column(Integer, ForeignKey("usuarios.id"))
    razon_social   = Column(String, nullable=False)
    nit            = Column(String, unique=True, nullable=False)
    sector         = Column(String)
    representante  = Column(String)
    cargo          = Column(String)
    correo         = Column(String, unique=True)
    telefono       = Column(String)
    direccion      = Column(String)
    activo         = Column(Integer, default=1)

    donaciones = relationship("Donacion", back_populates="empresa")


class Donacion(Base):
    __tablename__ = "donaciones"

    id              = Column(Integer, primary_key=True, index=True)
    folio           = Column(String, unique=True)
    empresa_id      = Column(Integer, ForeignKey("empresas.id"))
    beneficiario_id = Column(Integer, ForeignKey("adultos_mayores.id"))
    fecha           = Column(String)
    modalidad       = Column(String)
    observaciones   = Column(Text)
    valor_total     = Column(Float, default=0)
    estado          = Column(String, default="Registrada")

    empresa      = relationship("Empresa", back_populates="donaciones")
    beneficiario = relationship("AdultoMayor", back_populates="donaciones")
    items        = relationship("ItemDonacion", back_populates="donacion")


class ItemDonacion(Base):
    __tablename__ = "items_donacion"

    id           = Column(Integer, primary_key=True, index=True)
    donacion_id  = Column(Integer, ForeignKey("donaciones.id"))
    categoria    = Column(String)
    descripcion  = Column(String)
    cantidad     = Column(Integer)
    unidad       = Column(String)
    valor_est    = Column(Float, default=0)

    donacion = relationship("Donacion", back_populates="items")


class Usuario(Base):
    __tablename__ = "usuarios"

    id            = Column(Integer, primary_key=True, index=True)
    nombre        = Column(String, nullable=False)
    correo        = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    rol           = Column(String, nullable=False)  # 'admin' o 'empresa'
    activo        = Column(Integer, default=1)