from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, delete, select

from app.core.database import get_session
from app.models.entities import EstadisticaPartido, Partido
from app.schemas.common import PartidoCreate

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


@router.put("/{partido_id}")
def modificar_partido(
    partido_id: int,
    partido_data: PartidoCreate,
    session: Session = Depends(get_session),
):
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    partido.fecha = partido_data.fecha
    partido.equipo_local_id = partido_data.equipo_local_id
    partido.equipo_visitante_id = partido_data.equipo_visitante_id
    partido.goles_local = partido_data.goles_local
    partido.goles_visitante = partido_data.goles_visitante

    session.add(partido)

    session.exec(
        delete(EstadisticaPartido).where(EstadisticaPartido.partido_id == partido_id)
    )

    for est in partido_data.estadisticas:
        nueva_estadistica = EstadisticaPartido(
            partido_id=partido_id,
            jugador_id=est.jugador_id,
            equipo_id=est.equipo_id,
            goles=est.goles,
        )
        session.add(nueva_estadistica)

    session.commit()

    return {"mensaje": "Partido actualizado con éxito", "partido_id": partido_id}


@router.delete("/{partido_id}")
def eliminar_partido(partido_id: int, session: Session = Depends(get_session)):
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    session.exec(
        delete(EstadisticaPartido).where(EstadisticaPartido.partido_id == partido_id)
    )
    session.delete(partido)
    session.commit()

    return {"mensaje": "Partido eliminado con éxito", "partido_id": partido_id}
