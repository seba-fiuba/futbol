import os
from importlib import import_module

from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

load_dotenv()

raw_database_url = os.getenv("DATABASE_URL", "")
DATABASE_URL = raw_database_url.strip().replace('"', "").replace("'", "")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./futbol.db"

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

is_production = (
    os.getenv("RAILWAY_ENVIRONMENT") is not None or os.getenv("RENDER") is not None
)

engine_kwargs = {"echo": not is_production}

if DATABASE_URL.startswith("postgresql://"):
    engine_kwargs.update(
        {
            "pool_size": 10,
            "max_overflow": 20,
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "connect_args": {"connect_timeout": 10},
        }
    )

engine = create_engine(DATABASE_URL, **engine_kwargs)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables() -> None:
    # Importa modelos para registrar metadata antes del create_all
    import_module("app.models.entities")
    import_module("app.models.torneos")

    SQLModel.metadata.create_all(engine)
