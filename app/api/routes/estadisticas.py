from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.entities import EstadisticaPartido

router = APIRouter(prefix="/estadisticas", tags=["Estadisticas"])


@router.get("/")
def obtener_estadisticas(session: Session = Depends(get_session)):
    statement = select(EstadisticaPartido)
    estadisticas = session.exec(statement).all()
    return estadisticas


@router.post("/")
def cargar_estadisticas(session: Session = Depends(get_session)): ...
