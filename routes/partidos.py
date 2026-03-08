from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import Partido, EstadisticaPartido, PartidoCreate

router = APIRouter(prefix="/partidos", tags=["Partidos"])


@router.get("/")
def obtener_partidoss(session: Session = Depends(get_session)):
    statement = select(Partido)
    partidos = session.exec(statement).all()
    return partidos


@router.post("/")
def cargar_partidos(
    partido_data: PartidoCreate, session: Session = Depends(get_session)
):
    nuevo_partido = Partido(
        fecha=partido_data.fecha,
        equipo_local_id=partido_data.equipo_local_id,
        equipo_visitante_id=partido_data.equipo_visitante_id,
        goles_local=partido_data.goles_local,
        goles_visitante=partido_data.goles_visitante,
    )

    session.add(nuevo_partido)
    session.commit()
    session.refresh(nuevo_partido)

    for est in partido_data.estadisticas:
        nueva_estadistica = EstadisticaPartido(
            partido_id=nuevo_partido.id,
            jugador_id=est.jugador_id,
            equipo_id=est.equipo_id,
            goles=est.goles,
        )
        session.add(nueva_estadistica)

    session.commit()

    return {"mensaje": "Partido registrado con éxito", "partido_id": nuevo_partido.id}
