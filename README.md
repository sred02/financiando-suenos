# 🏠 Financiando Sueños

> Plataforma web de gestión de donaciones de materiales para mejoras del hogar,
> desarrollada para la ONG **Unbound Colombia**.

---

##  Contexto del proyecto

Financiando Sueños es un sistema que conecta **empresas donantes** con
**adultos mayores beneficiarios** que necesitan materiales para mejorar
sus viviendas. La plataforma es gestionada por el equipo administrativo
de Unbound Colombia.

Las donaciones son exclusivamente en especie — materiales físicos como:
cemento, pintura, baldosas, tejas, barillas, camas, televisores,
muebles y electrodomésticos. No se gestionan donaciones en efectivo.

Este proyecto fue desarrollado como parte del programa académico de
Ingeniería de Software — Semillero de investigación SISE, con enfoque en
tecnología para comunidades vulnerables.

---

##  Roles del sistema

| Rol | Descripción |
|-----|-------------|
| **Administrador (Unbound)** | Gestiona beneficiarios, donaciones, empresas y reportes globales |
| **Empresa Donante** | Registra donaciones, ve sus propios certificados y los perfiles de beneficiarios |

---

##  Pantallas del sistema

| Pantalla | Descripción |
|----------|-------------|
| `login.html` | Inicio de sesión con selector de rol |
| `dashboard.html` | Panel de inicio adaptativo según rol |
| `adultos.html` | Gestión y visualización de beneficiarios |
| `donaciones.html` | Registro y seguimiento de donaciones |
| `empresas.html` | Gestión de empresas donantes |
| `reportes.html` | Estadísticas, gráficas y exportación |
| `certificado.html` | Generación y descarga de certificados contables |

---

##  Tecnologías utilizadas

### Backend
- **Python 3.11**
- **FastAPI** — framework web para la API REST
- **SQLAlchemy** — ORM para manejo de base de datos
- **SQLite** — base de datos local
- **Pydantic v2** — validación de datos
- **python-jose** — generación y verificación de tokens JWT
- **passlib + bcrypt** — hashing seguro de contraseñas

### Frontend
- **HTML5 / CSS3 / JavaScript** puro (sin frameworks)
- **Chart.js** — gráficas y visualización de datos
- **Google Fonts** — tipografía (Nunito + Merriweather)

---

---

##  Instalación y ejecución local

### Requisitos previos
- Python 3.10 o superior → https://www.python.org/downloads/
- Visual Studio Code → https://code.visualstudio.com/
- Extensión **Live Server** en VS Code

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/financiando-suenos.git
cd financiando-suenos
```

### 2. Crear y activar el entorno virtual

```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac / Linux:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos con datos de prueba

```bash
python seed.py
```

### 5. Arrancar el servidor

```bash
uvicorn main:app --reload
```

El servidor corre en: http://localhost:8000

La documentación de la API está en: http://localhost:8000/docs

### 6. Abrir el frontend

En VS Code, clic derecho sobre `frontend/dashboard.html` →
**Open with Live Server**

Se abre en: http://127.0.0.1:5500/dashboard.html

---

## Credenciales de prueba

| Perfil | Correo | Contraseña |
|--------|--------|------------|
| Administrador Unbound | admin@unbound.org.co | Admin2026 |
| Empresa Donante | empresa@materiales.com | Empresa2026 |

---

##  Endpoints principales de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/auth/login` | Iniciar sesión → devuelve JWT |
| GET | `/adultos/` | Listar beneficiarios |
| POST | `/adultos/` | Crear beneficiario |
| PUT | `/adultos/{id}` | Actualizar beneficiario |
| GET | `/empresas/` | Listar empresas donantes |
| POST | `/empresas/` | Registrar empresa (público) |
| GET | `/donaciones/` | Listar donaciones |
| POST | `/donaciones/` | Registrar donación con ítems |
| GET | `/reportes/resumen` | KPIs globales del sistema |
| GET | `/reportes/por-mes` | Donaciones agrupadas por mes |
| GET | `/certificados/{id}` | HTML del certificado de donación |

---

##  Seguridad

- Autenticación mediante **JWT (JSON Web Tokens)**
- Contraseñas hasheadas con **bcrypt**
- Control de acceso por rol en todos los endpoints sensibles
- Los datos de la base de datos local **no se suben al repositorio**

---

##  Licencia

Proyecto académico desarrollado para Unbound Colombia.
Uso educativo y sin fines de lucro.