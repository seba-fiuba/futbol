# ⚽ Fútbol Manager

Sistema completo de gestión de partidos de fútbol con API REST y aplicación web moderna.

## 📋 Descripción

Aplicación full-stack para gestionar partidos de fútbol, equipos, jugadores y estadísticas. Incluye:
- Backend API REST con FastAPI
- Frontend web interactivo con SvelteKit
- Base de datos PostgreSQL
- Sistema de migraciones con Alembic

## 🛠️ Tecnologías

### Backend
- **FastAPI** - Framework web de alto rendimiento
- **SQLModel** - ORM (SQLAlchemy + Pydantic)
- **PostgreSQL** - Base de datos relacional
- **Alembic** - Migraciones de base de datos
- **python-dotenv** - Gestión de variables de entorno

### Frontend
- **SvelteKit** - Framework web moderno
- **Tailwind CSS** - Framework de estilos
- **Vite** - Build tool y dev server

## 📋 Requisitos

- Python 3.14+
- PostgreSQL 14+
- Node.js 18+ y npm (para el frontend)

## 🚀 Instalación

### 1. Backend (FastAPI)

```bash
# Clona el repositorio
git clone <url-del-repo>
cd futbol

# Crea y activa el entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instala las dependencias
pip install -r requirements.txt

# Configura PostgreSQL
sudo -u postgres psql
CREATE DATABASE futbol_db;
ALTER USER postgres WITH PASSWORD 'tu_contraseña';
\q

# Configura las variables de entorno
cp .env.example .env
# Edita .env con tus credenciales de PostgreSQL

# Ejecuta las migraciones
alembic upgrade head

# (Opcional) Carga datos de prueba
python seed.py
```

### 2. Frontend (SvelteKit)

```bash
# Instala Node.js si no lo tienes (Fedora)
sudo dnf install nodejs npm

# Navega a la carpeta del frontend
cd frontend

# Instala las dependencias
npm install
```

## 🏃 Ejecutar el Proyecto

### Backend

```bash
# Activa el entorno virtual
source .venv/bin/activate

# Inicia el servidor (desde la raíz del proyecto)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en:
- API: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs

### Frontend

```bash
# En otra terminal, desde la carpeta frontend
cd frontend
npm run dev
```

La aplicación web estará disponible en: http://localhost:5173

## 📁 Estructura del Proyecto

```
futbol/
├── alembic/              # Migraciones de base de datos
│   └── versions/
├── routes/               # Endpoints de la API
│   ├── jugadores.py
│   ├── equipos.py
│   ├── partidos.py
│   └── estadisticas.py
├── frontend/             # Aplicación web SvelteKit
│   ├── src/
│   │   ├── routes/      # Páginas de la aplicación
│   │   └── lib/         # Utilidades y componentes
│   ├── static/
│   └── package.json
├── models.py             # Modelos SQLModel
├── database.py           # Configuración de la base de datos
├── main.py              # Punto de entrada de FastAPI
├── seed.py              # Script para cargar datos de prueba
├── alembic.ini          # Configuración de Alembic
├── requirements.txt     # Dependencias de Python
├── .env                 # Variables de entorno (no versionado)
└── README.md
```

## 📊 Modelos de Datos

- **Jugador**: Información de jugadores (nombre, apodo, imagen)
- **Equipo**: Equipos de fútbol
- **Partido**: Partidos entre equipos con fecha y resultado
- **EstadisticaPartido**: Goles de jugadores en cada partido

## 🌐 API Endpoints

### Jugadores
- `GET /Jugadores/` - Lista de jugadores
- `POST /Jugadores/` - Crear jugador

### Equipos
- `GET /equipos/` - Lista de equipos
- `POST /equipos/` - Crear equipo

### Partidos
- `GET /partidos/` - Lista de partidos
- `POST /partidos/` - Crear partido con estadísticas
- `PUT /partidos/{id}` - Actualizar partido

### Estadísticas
- `GET /estadisticas/` - Todas las estadísticas

## 💻 Características del Frontend

- 🏠 **Dashboard** - Vista general con estadísticas
- 👥 **Jugadores** - Lista y búsqueda de jugadores
- 🏆 **Equipos** - Tabla de posiciones actualizada automáticamente
- ⚽ **Partidos** - Registro y gestión de partidos con goleadores
- 🎯 **Goleadores** - Ranking con podio de los top 3

## 🔧 Comandos Útiles

### Migraciones

```bash
# Crear una nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

### Base de datos

```bash
# Conectar a PostgreSQL
psql -U postgres -d futbol_db -h localhost

# Ver tablas
\dt

# Ver contenido de una tabla
SELECT * FROM jugadores;
```

### Frontend

```bash
cd frontend

# Desarrollo
npm run dev

# Build producción
npm run build

# Preview producción
npm run preview
```

## 🐛 Solución de Problemas

### Error de conexión entre frontend y backend
- Verifica que el backend esté corriendo en el puerto 8000
- Verifica que el frontend esté corriendo en el puerto 5173
- CORS está configurado automáticamente para esos puertos

### Error de base de datos
- Verifica que PostgreSQL esté corriendo
- Verifica las credenciales en el archivo `.env`
- Asegúrate de haber ejecutado las migraciones

## 📚 Documentación Adicional

- [GUIA_USO.md](GUIA_USO.md) - Guía detallada de uso de la aplicación
- [IMAGENES.md](IMAGENES.md) - Cómo agregar y gestionar imágenes de jugadores
- [frontend/README.md](frontend/README.md) - Documentación específica del frontend
- [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md) - Guía completa de deployment a Railway
- [CHECKLIST_DEPLOY.md](CHECKLIST_DEPLOY.md) - Checklist rápido antes de deployar

## 📝 Notas de Desarrollo

- El backend incluye documentación interactiva en `/docs` (Swagger UI)
- El frontend usa proxy para las peticiones a `/api`
- Las imágenes de jugadores se guardan en `frontend/static/jugadores/`
- Los puntos se calculan automáticamente: Victoria = 3, Empate = 1, Derrota = 0

## 📄 Licencia

Este proyecto es de uso personal y educativo.
