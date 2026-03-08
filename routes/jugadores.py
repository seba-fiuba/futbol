from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import Jugador

router = APIRouter(prefix="/Jugadores", tags=["Jugadores"])


@router.get("/")
def obtener_jugadores(session: Session = Depends(get_session)):
    statement = select(Jugador)
    jugadores = session.exec(statement).all()
    return jugadores


@router.post("/")
def cargar_jugadores(session: Session = Depends(get_session)): ...
