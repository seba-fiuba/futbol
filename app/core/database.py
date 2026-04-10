import os
from importlib import import_module

from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./futbol.db"

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

is_production = (
    os.getenv("RAILWAY_ENVIRONMENT") is not None or os.getenv("RENDER") is not None
)
engine = create_engine(DATABASE_URL, echo=not is_production)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables() -> None:
    # Importa modelos para registrar metadata antes del create_all
    import_module("app.models.entities")
    import_module("app.models.torneos")

    SQLModel.metadata.create_all(engine)
