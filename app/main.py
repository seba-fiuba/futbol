import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db_and_tables, engine
from app.api.routes import equipos, estadisticas, jugadores, partidos, torneos

app = FastAPI(title="Fútbol Manager API", version="1.0.0")

is_production = (
    os.getenv("RAILWAY_ENVIRONMENT") is not None or os.getenv("RENDER") is not None
)

if is_production:
    allowed_origins = ["*"]
else:
    allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jugadores.router)
app.include_router(equipos.router)
app.include_router(partidos.router)
app.include_router(estadisticas.router)
app.include_router(torneos.router)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    try:
        with engine.connect() as connection:
            connection.exec_driver_sql("SELECT 1")
        return {"status": "ready"}
    except Exception as exc:
        raise HTTPException(
            status_code=503, detail=f"Database not ready: {exc}"
        ) from exc


@app.on_event("startup")
def on_startup() -> None:
    # En producción, Alembic ya corre en start.sh.
    # Evitamos trabajo extra en startup para reducir timeouts y 502 por cold start.
    if not is_production:
        create_db_and_tables()
