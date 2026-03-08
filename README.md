# Futbol API

API REST para gestión de partidos de fútbol, equipos, jugadores y estadísticas.

## Tecnologías

- **FastAPI** - Framework web
- **SQLModel** - ORM (SQLAlchemy + Pydantic)
- **PostgreSQL** - Base de datos
- **Alembic** - Migraciones de base de datos
- **python-dotenv** - Gestión de variables de entorno

## Requisitos

- Python 3.14+
- PostgreSQL 14+

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone <url-del-repo>
   cd futbol
   ```

2. **Crea y activa el entorno virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura PostgreSQL:**
   ```bash
   # Crea la base de datos
   sudo -u postgres psql
   CREATE DATABASE futbol_db;
   ALTER USER postgres WITH PASSWORD 'tu_contraseña';
   \q
   ```

5. **Configura las variables de entorno:**
   ```bash
   cp .env.example .env
   # Edita .env con tus credenciales de PostgreSQL
   ```

6. **Ejecuta las migraciones:**
   ```bash
   alembic upgrade head
   ```

## Estructura del Proyecto

```
futbol/
├── alembic/              # Migraciones de base de datos
│   └── versions/
├── models/               # Modelos (por organizar)
├── routes/               # Rutas de la API (por crear)
├── models.py             # Modelos SQLModel
├── database.py           # Configuración de la base de datos
├── alembic.ini          # Configuración de Alembic
├── requirements.txt     # Dependencias de Python
├── .env                 # Variables de entorno (no versionado)
└── .env.example         # Ejemplo de variables de entorno
```

## Modelos

- **Jugador**: Información de jugadores
- **Equipo**: Equipos de fútbol
- **Partido**: Partidos entre equipos
- **EstadisticaPartido**: Estadísticas de jugadores en partidos

## Comandos Útiles

**Migraciones:**
```bash
# Crear una nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

**Base de datos:**
```bash
# Conectar a PostgreSQL
psql -U postgres -d futbol_db -h localhost

# Ver tablas
\dt

# Ver estructura de tabla
\d jugadores
```

## Desarrollo

_Por implementar: Endpoints de la API con FastAPI_
