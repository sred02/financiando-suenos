from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financiando Sueños API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers.auth_router  import router as auth_router
from routers.adultos      import router as adultos_router
from routers.empresas     import router as empresas_router
from routers.donaciones   import router as donaciones_router
from routers.reportes     import router as reportes_router
from routers.certificados import router as cert_router

app.include_router(auth_router,       prefix="/auth",         tags=["Autenticación"])
app.include_router(adultos_router,    prefix="/adultos",      tags=["Adultos Mayores"])
app.include_router(empresas_router,   prefix="/empresas",     tags=["Empresas"])
app.include_router(donaciones_router, prefix="/donaciones",   tags=["Donaciones"])
app.include_router(reportes_router,   prefix="/reportes",     tags=["Reportes"])
app.include_router(cert_router,       prefix="/certificados", tags=["Certificados"])


@app.get("/ping")
def ping():
    return {"status": "ok", "app": "Financiando Sueños"}