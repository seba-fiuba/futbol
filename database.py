from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# 1. Definimos la URL de la base de datos PostgreSQL.
# Formato: postgresql://usuario:contraseña@host:puerto/nombre_bd
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/futbol_db"
)

# 2. Creamos el motor (engine).
# echo=True hace que veas en la terminal todo el SQL que se ejecuta por detrás (ideal para aprender).
engine = create_engine(DATABASE_URL, echo=True)


# 3. Generador de sesiones (El estándar de FastAPI)
def get_session():
    with Session(engine) as session:
        yield session
