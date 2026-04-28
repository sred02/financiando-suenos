from auth import hash_password
from database import SessionLocal, engine
import models


models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ── USUARIOS ──────────────────────────────────────────────────────────────────
admin = models.Usuario(
    nombre="Administrador Unbound",
    correo="admin@unbound.org.co",
    password_hash=hash_password("Admin2026"),
    rol="admin"
)
u_empresa = models.Usuario(
    nombre="Andrés Felipe Ruiz",
    correo="empresa@materiales.com",
    password_hash=hash_password("Empresa2026"),
    rol="empresa"
)
db.add_all([admin, u_empresa])
db.flush()

# ── EMPRESAS ──────────────────────────────────────────────────────────────────
empresa1 = models.Empresa(
    usuario_id=u_empresa.id,
    razon_social="Materiales y Acabados del Norte S.A.S.",
    nit="900.456.123-7",
    sector="Construcción y materiales",
    representante="Andrés Felipe Ruiz",
    cargo="Gerente de RSE",
    telefono="601 345 8900",
    direccion="Calle 80 #45-22, Bogotá D.C."
)
db.add(empresa1)

u2 = models.Usuario(nombre="Sandra Gómez", correo="sandra@xyz.com", password_hash=hash_password("Empresa2026"), rol="empresa")
db.add(u2); db.flush()
empresa2 = models.Empresa(usuario_id=u2.id, razon_social="Ferreterías XYZ Ltda.", nit="800.123.456-1", representante="Sandra Milena Gómez", cargo="Directora Comercial")
db.add(empresa2)

u3 = models.Usuario(nombre="Luis Prado", correo="luis@techcorp.com", password_hash=hash_password("Empresa2026"), rol="empresa")
db.add(u3); db.flush()
empresa3 = models.Empresa(usuario_id=u3.id, razon_social="Cerámicas TechCorp S.A.", nit="901.234.567-3", representante="Luis Alberto Prado", cargo="Gerente General")
db.add(empresa3)

u4 = models.Usuario(nombre="Camila Torres", correo="camila@electrohogar.com", password_hash=hash_password("Empresa2026"), rol="empresa")
db.add(u4); db.flush()
empresa4 = models.Empresa(usuario_id=u4.id, razon_social="Electrohogar Dist. S.A.", nit="700.987.654-2", representante="Camila Torres Ruiz", cargo="Jefe de RSE")
db.add(empresa4)

db.flush()

# ── ADULTOS MAYORES ───────────────────────────────────────────────────────────
adultos = [
    models.AdultoMayor(nombre="María Inés Torres Salcedo", identificacion="25431987", fecha_nac="1948-04-12", genero="Femenino", ciudad="Bogotá", barrio="Los Cedritos", direccion="Cra 15 #42-10", telefono="3104557892", acudiente="Carlos Torres – 3156782341", necesidades="Cubierta y tejas,Cemento y barillas,Pintura", descripcion="Techo con filtraciones y grietas en paredes exteriores. Requiere reparación urgente antes de temporada de lluvias.", urgencia="Alta", tipo_vivienda="Casa propia"),
    models.AdultoMayor(nombre="Jorge Ernesto Ríos", identificacion="13887204", fecha_nac="1943-07-20", genero="Masculino", ciudad="Bogotá", barrio="Kennedy", direccion="Calle 38 Sur #72-15", necesidades="Cama y colchón,Muebles de sala,Televisor", descripcion="Duerme en una cama deteriorada sin colchón adecuado. La sala no tiene mobiliario básico.", urgencia="Media", tipo_vivienda="Arriendo"),
    models.AdultoMayor(nombre="Lucía Amparo Castaño", identificacion="41205339", fecha_nac="1951-11-03", genero="Femenino", ciudad="Bogotá", barrio="Chapinero", necesidades="Baldosas y pisos,Electrodomésticos,Pintura", descripcion="Piso en tierra y paredes sin pintar desde hace más de 10 años. Sin nevera ni estufa funcional.", urgencia="Alta", tipo_vivienda="Casa propia"),
    models.AdultoMayor(nombre="Pedro Manuel Vargas", identificacion="7654321", fecha_nac="1955-03-14", genero="Masculino", ciudad="Medellín", barrio="Belén", necesidades="Pintura y acabados", descripcion="Ventanas en mal estado y paredes sin pintar interior y exterior.", urgencia="Media", tipo_vivienda="Casa propia"),
    models.AdultoMayor(nombre="Rosa Elena Muñoz", identificacion="31876543", fecha_nac="1946-09-28", genero="Femenino", ciudad="Cali", barrio="El Jardín", acudiente="Vecina – 3178901234", necesidades="Electrodomésticos,Cama y colchón,Cubierta y tejas", descripcion="Techo de zinc deteriorado y sin nevera. Vive sola, requiere intervención urgente.", urgencia="Alta", tipo_vivienda="Casa propia"),
    models.AdultoMayor(nombre="Hernando Gómez Salas", identificacion="8123456", fecha_nac="1940-02-11", genero="Masculino", ciudad="Bucaramanga", barrio="Cabecera", acudiente="Hermano – 3155678901", necesidades="Muebles y sala,Televisor,Pisos y baldosas", descripcion="Requiere mejoras en el área social. Pisos desgastados y sin mobiliario en la sala.", urgencia="Baja", tipo_vivienda="Casa propia"),
]
db.add_all(adultos)
db.flush()

# ── DONACIONES ────────────────────────────────────────────────────────────────
donaciones_data = [
    {
        "folio":"CF-2026-001","empresa_id":empresa1.id,"beneficiario_id":adultos[0].id,
        "fecha":"2026-03-24","modalidad":"Entrega directa en el domicilio",
        "observaciones":"La empresa aportó transporte y descargue.","valor_total":815000,"estado":"Registrada",
        "items":[
            {"categoria":"Materiales de construcción","descripcion":"Cemento gris Argos 50kg","cantidad":10,"unidad":"Bultos","valor_est":280000},
            {"categoria":"Cubierta y tejas","descripcion":"Tejas fibrocemento 1.00x0.50m","cantidad":20,"unidad":"Unidades","valor_est":340000},
            {"categoria":"Materiales de construcción","descripcion":"Barilla corrugada 3/8 x 6m","cantidad":15,"unidad":"Unidades","valor_est":195000},
        ]
    },
    {
        "folio":"CF-2026-002","empresa_id":empresa2.id,"beneficiario_id":adultos[1].id,
        "fecha":"2026-03-22","modalidad":"Entrega con instalación","observaciones":"Muebles acomodados en el espacio indicado.","valor_total":1200000,"estado":"Registrada",
        "items":[
            {"categoria":"Cama y colchón","descripcion":"Cama doble con colchón ortopédico Cannon","cantidad":1,"unidad":"Unidad","valor_est":750000},
            {"categoria":"Muebles","descripcion":"Juego de sala 3+2 puestos en tela","cantidad":1,"unidad":"Juego","valor_est":450000},
        ]
    },
    {
        "folio":"CF-2026-003","empresa_id":empresa3.id,"beneficiario_id":adultos[2].id,
        "fecha":"2026-03-20","modalidad":"Entrega en domicilio","observaciones":"Incluye pegante y boquilla.","valor_total":680000,"estado":"Registrada",
        "items":[
            {"categoria":"Pisos y baldosas","descripcion":"Baldosa porcelanato 60x60cm blanco","cantidad":30,"unidad":"m2","valor_est":680000},
        ]
    },
    {
        "folio":"CF-2026-004","empresa_id":empresa1.id,"beneficiario_id":adultos[3].id,
        "fecha":"2026-03-18","modalidad":"Entrega en domicilio","observaciones":"","valor_total":320000,"estado":"En verificación",
        "items":[
            {"categoria":"Pintura y acabados","descripcion":"Pintura exterior Viniltex blanco","cantidad":4,"unidad":"Galones","valor_est":320000},
        ]
    },
    {
        "folio":"CF-2026-005","empresa_id":empresa4.id,"beneficiario_id":adultos[4].id,
        "fecha":"2026-03-15","modalidad":"Entrega con instalación","observaciones":"Técnicos instalaron TV y verificaron nevera.","valor_total":2100000,"estado":"Registrada",
        "items":[
            {"categoria":"Televisor","descripcion":"Televisor Samsung 43 Smart TV 4K","cantidad":1,"unidad":"Unidad","valor_est":1200000},
            {"categoria":"Electrodomésticos","descripcion":"Nevera LG 220L No Frost","cantidad":1,"unidad":"Unidad","valor_est":900000},
        ]
    },
    {
        "folio":"CF-2026-006","empresa_id":empresa2.id,"beneficiario_id":adultos[5].id,
        "fecha":"2026-03-10","modalidad":"Entrega en domicilio","observaciones":"Falta soporte fotográfico.","valor_total":1450000,"estado":"Pendiente",
        "items":[
            {"categoria":"Electrodomésticos","descripcion":"Estufa 4 hornillas + horno","cantidad":1,"unidad":"Unidad","valor_est":850000},
            {"categoria":"Electrodomésticos","descripcion":"Lavadora semiautomática 9kg","cantidad":1,"unidad":"Unidad","valor_est":600000},
        ]
    },
]

for d in donaciones_data:
    items = d.pop("items")
    don = models.Donacion(**d)
    db.add(don)
    db.flush()
    for it in items:
        db.add(models.ItemDonacion(donacion_id=don.id, **it))

db.commit()
print("✅ Base de datos inicializada con datos de demostración.")
print("   Admin:   admin@unbound.org.co  / Admin2026")
print("   Empresa: empresa@materiales.com / Empresa2026")
db.close()
