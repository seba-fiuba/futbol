from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import Equipo

router = APIRouter(prefix="/equipos", tags=["Equipos"])


@router.get("/")
def obtener_equipos(session: Session = Depends(get_session)):
    statement = select(Equipo)
    equipos = session.exec(statement).all()
    return equipos


@router.post("/")
def cargar_equipos(session: Session = Depends(get_session)): ...
