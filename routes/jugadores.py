from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Jugador, JugadorCreate

router = APIRouter(prefix="/Jugadores", tags=["Jugadores"])


@router.get("/")
def obtener_jugadores(session: Session = Depends(get_session)):
    statement = select(Jugador)
    jugadores = session.exec(statement).all()
    return jugadores


@router.post("/")
def cargar_jugadores(
    jugador_data: JugadorCreate, session: Session = Depends(get_session)
):
    nuevo_jugador = Jugador(
        nombre=jugador_data.nombre,
        apodo=jugador_data.apodo,
        imagen=jugador_data.imagen_url,
    )

    session.add(nuevo_jugador)
    session.commit()
    session.refresh(nuevo_jugador)

    return {"mensaje": "Jugador registrado con exito", "jugador_id": nuevo_jugador.id}


@router.put("/{jugador_id}")
def editar_jugador(
    jugador_id: int,
    jugador_data: JugadorCreate,
    session: Session = Depends(get_session),
):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    jugador.nombre = jugador_data.nombre
    jugador.apodo = jugador_data.apodo
    jugador.imagen = jugador_data.imagen_url

    session.add(jugador)
    session.commit()
    session.refresh(jugador)

    return {"mensaje": "Jugador actualizado con exito", "jugador_id": jugador.id}
