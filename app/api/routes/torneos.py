from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.torneos import EquipoTorneo, JugadorTorneo, PartidoTorneo, Torneo
from app.schemas.torneos import (
    EquipoTorneoCreate,
    EquipoTorneoRead,
    EquipoTorneoUpdate,
    JugadorTorneoCreate,
    JugadorTorneoRead,
    JugadorTorneoUpdate,
    PartidoTorneoCreate,
    PartidoTorneoRead,
    PartidoTorneoUpdate,
    TorneoCreate,
    TorneoRead,
    TorneoUpdate,
)

router = APIRouter(prefix="/torneos", tags=["Torneos"])


@router.get("/", response_model=list[TorneoRead])
def listar_torneos(session: Session = Depends(get_session)):
    torneos = session.exec(select(Torneo)).all()
    return [
        TorneoRead(
            id=t.id,
            nombre=t.nombre,
            fecha_creacion=t.fecha_creacion,
            estado=t.estado,
        )
        for t in torneos
    ]


@router.post("/", response_model=TorneoRead)
def crear_torneo(data: TorneoCreate, session: Session = Depends(get_session)):
    torneo = Torneo(
        nombre=data.nombre,
        estado=data.estado,
        fecha_creacion=datetime.utcnow(),
    )
    session.add(torneo)
    session.commit()
    session.refresh(torneo)

    return TorneoRead(
        id=torneo.id,
        nombre=torneo.nombre,
        fecha_creacion=torneo.fecha_creacion,
        estado=torneo.estado,
    )


@router.put("/{torneo_id}", response_model=TorneoRead)
def editar_torneo(
    torneo_id: int,
    data: TorneoUpdate,
    session: Session = Depends(get_session),
):
    torneo = session.get(Torneo, torneo_id)
    if not torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")

    if data.nombre is not None:
        torneo.nombre = data.nombre
    if data.estado is not None:
        torneo.estado = data.estado

    session.add(torneo)
    session.commit()
    session.refresh(torneo)

    return TorneoRead(
        id=torneo.id,
        nombre=torneo.nombre,
        fecha_creacion=torneo.fecha_creacion,
        estado=torneo.estado,
    )


@router.delete("/{torneo_id}")
def eliminar_torneo(torneo_id: int, session: Session = Depends(get_session)):
    torneo = session.get(Torneo, torneo_id)
    if not torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")

    existe_equipo = session.exec(
        select(EquipoTorneo.id).where(EquipoTorneo.torneo_id == torneo_id)
    ).first()
    if existe_equipo:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el torneo porque tiene equipos asociados",
        )

    existe_partido = session.exec(
        select(PartidoTorneo.id).where(PartidoTorneo.torneo_id == torneo_id)
    ).first()
    if existe_partido:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el torneo porque tiene partidos asociados",
        )

    session.delete(torneo)
    session.commit()
    return {"mensaje": "Torneo eliminado con exito", "torneo_id": torneo_id}


@router.get("/equipos", response_model=list[EquipoTorneoRead])
def listar_equipos_torneo(session: Session = Depends(get_session)):
    equipos = session.exec(select(EquipoTorneo)).all()
    return [
        EquipoTorneoRead(id=e.id, torneo_id=e.torneo_id, nombre=e.nombre)
        for e in equipos
    ]


@router.get("/{torneo_id}/equipos", response_model=list[EquipoTorneoRead])
def listar_equipos_de_torneo(torneo_id: int, session: Session = Depends(get_session)):
    equipos = session.exec(
        select(EquipoTorneo).where(EquipoTorneo.torneo_id == torneo_id)
    ).all()
    return [
        EquipoTorneoRead(id=e.id, torneo_id=e.torneo_id, nombre=e.nombre)
        for e in equipos
    ]


@router.post("/equipos", response_model=EquipoTorneoRead)
def crear_equipo_torneo(
    data: EquipoTorneoCreate,
    session: Session = Depends(get_session),
):
    torneo = session.get(Torneo, data.torneo_id)
    if not torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")

    equipo = EquipoTorneo(torneo_id=data.torneo_id, nombre=data.nombre)
    session.add(equipo)
    session.commit()
    session.refresh(equipo)

    return EquipoTorneoRead(
        id=equipo.id, torneo_id=equipo.torneo_id, nombre=equipo.nombre
    )


@router.put("/equipos/{equipo_torneo_id}", response_model=EquipoTorneoRead)
def editar_equipo_torneo(
    equipo_torneo_id: int,
    data: EquipoTorneoUpdate,
    session: Session = Depends(get_session),
):
    equipo = session.get(EquipoTorneo, equipo_torneo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo de torneo no encontrado")

    if data.nombre is not None:
        equipo.nombre = data.nombre

    session.add(equipo)
    session.commit()
    session.refresh(equipo)

    return EquipoTorneoRead(
        id=equipo.id, torneo_id=equipo.torneo_id, nombre=equipo.nombre
    )


@router.delete("/equipos/{equipo_torneo_id}")
def eliminar_equipo_torneo(
    equipo_torneo_id: int,
    session: Session = Depends(get_session),
):
    equipo = session.get(EquipoTorneo, equipo_torneo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo de torneo no encontrado")

    tiene_jugadores = session.exec(
        select(JugadorTorneo.id).where(
            JugadorTorneo.equipo_torneo_id == equipo_torneo_id
        )
    ).first()
    if tiene_jugadores:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el equipo porque tiene jugadores asociados",
        )

    tiene_partidos = session.exec(
        select(PartidoTorneo.id).where(
            (PartidoTorneo.local_id == equipo_torneo_id)
            | (PartidoTorneo.visitante_id == equipo_torneo_id)
        )
    ).first()
    if tiene_partidos:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el equipo porque tiene partidos asociados",
        )

    session.delete(equipo)
    session.commit()
    return {
        "mensaje": "Equipo de torneo eliminado con exito",
        "equipo_torneo_id": equipo_torneo_id,
    }


@router.get("/jugadores", response_model=list[JugadorTorneoRead])
def listar_jugadores_torneo(session: Session = Depends(get_session)):
    jugadores = session.exec(select(JugadorTorneo)).all()
    return [
        JugadorTorneoRead(
            id=j.id,
            equipo_torneo_id=j.equipo_torneo_id,
            usuario_id=j.usuario_id,
        )
        for j in jugadores
    ]


@router.get(
    "/equipos/{equipo_torneo_id}/jugadores", response_model=list[JugadorTorneoRead]
)
def listar_jugadores_de_equipo(
    equipo_torneo_id: int,
    session: Session = Depends(get_session),
):
    jugadores = session.exec(
        select(JugadorTorneo).where(JugadorTorneo.equipo_torneo_id == equipo_torneo_id)
    ).all()
    return [
        JugadorTorneoRead(
            id=j.id,
            equipo_torneo_id=j.equipo_torneo_id,
            usuario_id=j.usuario_id,
        )
        for j in jugadores
    ]


@router.post("/jugadores", response_model=JugadorTorneoRead)
def crear_jugador_torneo(
    data: JugadorTorneoCreate,
    session: Session = Depends(get_session),
):
    equipo = session.get(EquipoTorneo, data.equipo_torneo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo de torneo no encontrado")

    jugador = JugadorTorneo(
        equipo_torneo_id=data.equipo_torneo_id,
        usuario_id=data.usuario_id,
    )
    session.add(jugador)
    session.commit()
    session.refresh(jugador)

    return JugadorTorneoRead(
        id=jugador.id,
        equipo_torneo_id=jugador.equipo_torneo_id,
        usuario_id=jugador.usuario_id,
    )


@router.put("/jugadores/{jugador_torneo_id}", response_model=JugadorTorneoRead)
def editar_jugador_torneo(
    jugador_torneo_id: int,
    data: JugadorTorneoUpdate,
    session: Session = Depends(get_session),
):
    jugador = session.get(JugadorTorneo, jugador_torneo_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador de torneo no encontrado")

    if data.equipo_torneo_id is not None:
        equipo = session.get(EquipoTorneo, data.equipo_torneo_id)
        if not equipo:
            raise HTTPException(
                status_code=404, detail="Equipo de torneo no encontrado"
            )
        jugador.equipo_torneo_id = data.equipo_torneo_id

    session.add(jugador)
    session.commit()
    session.refresh(jugador)

    return JugadorTorneoRead(
        id=jugador.id,
        equipo_torneo_id=jugador.equipo_torneo_id,
        usuario_id=jugador.usuario_id,
    )


@router.delete("/jugadores/{jugador_torneo_id}")
def eliminar_jugador_torneo(
    jugador_torneo_id: int,
    session: Session = Depends(get_session),
):
    jugador = session.get(JugadorTorneo, jugador_torneo_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador de torneo no encontrado")

    session.delete(jugador)
    session.commit()
    return {
        "mensaje": "Jugador de torneo eliminado con exito",
        "jugador_torneo_id": jugador_torneo_id,
    }


@router.get("/partidos", response_model=list[PartidoTorneoRead])
def listar_partidos_torneo(session: Session = Depends(get_session)):
    partidos = session.exec(select(PartidoTorneo)).all()
    return [
        PartidoTorneoRead(
            id=p.id,
            torneo_id=p.torneo_id,
            local_id=p.local_id,
            visitante_id=p.visitante_id,
            goles_local=p.goles_local,
            goles_visitante=p.goles_visitante,
            fase=p.fase,
            jugado=p.jugado,
        )
        for p in partidos
    ]


@router.get("/{torneo_id}/partidos", response_model=list[PartidoTorneoRead])
def listar_partidos_de_torneo(torneo_id: int, session: Session = Depends(get_session)):
    partidos = session.exec(
        select(PartidoTorneo).where(PartidoTorneo.torneo_id == torneo_id)
    ).all()
    return [
        PartidoTorneoRead(
            id=p.id,
            torneo_id=p.torneo_id,
            local_id=p.local_id,
            visitante_id=p.visitante_id,
            goles_local=p.goles_local,
            goles_visitante=p.goles_visitante,
            fase=p.fase,
            jugado=p.jugado,
        )
        for p in partidos
    ]


@router.post("/partidos", response_model=PartidoTorneoRead)
def crear_partido_torneo(
    data: PartidoTorneoCreate,
    session: Session = Depends(get_session),
):
    if data.local_id == data.visitante_id:
        raise HTTPException(
            status_code=400, detail="Local y visitante no pueden ser el mismo"
        )

    torneo = session.get(Torneo, data.torneo_id)
    if not torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")

    local = session.get(EquipoTorneo, data.local_id)
    visitante = session.get(EquipoTorneo, data.visitante_id)
    if not local or not visitante:
        raise HTTPException(
            status_code=404, detail="Equipo local o visitante no encontrado"
        )

    partido = PartidoTorneo(
        torneo_id=data.torneo_id,
        local_id=data.local_id,
        visitante_id=data.visitante_id,
        fase=data.fase,
    )
    session.add(partido)
    session.commit()
    session.refresh(partido)

    return PartidoTorneoRead(
        id=partido.id,
        torneo_id=partido.torneo_id,
        local_id=partido.local_id,
        visitante_id=partido.visitante_id,
        goles_local=partido.goles_local,
        goles_visitante=partido.goles_visitante,
        fase=partido.fase,
        jugado=partido.jugado,
    )


@router.put("/partidos/{partido_torneo_id}", response_model=PartidoTorneoRead)
def editar_partido_torneo(
    partido_torneo_id: int,
    data: PartidoTorneoUpdate,
    session: Session = Depends(get_session),
):
    partido = session.get(PartidoTorneo, partido_torneo_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido de torneo no encontrado")

    if data.goles_local is not None:
        partido.goles_local = data.goles_local
    if data.goles_visitante is not None:
        partido.goles_visitante = data.goles_visitante
    if data.fase is not None:
        partido.fase = data.fase
    if data.jugado is not None:
        partido.jugado = data.jugado

    session.add(partido)
    session.commit()
    session.refresh(partido)

    return PartidoTorneoRead(
        id=partido.id,
        torneo_id=partido.torneo_id,
        local_id=partido.local_id,
        visitante_id=partido.visitante_id,
        goles_local=partido.goles_local,
        goles_visitante=partido.goles_visitante,
        fase=partido.fase,
        jugado=partido.jugado,
    )


@router.delete("/partidos/{partido_torneo_id}")
def eliminar_partido_torneo(
    partido_torneo_id: int,
    session: Session = Depends(get_session),
):
    partido = session.get(PartidoTorneo, partido_torneo_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido de torneo no encontrado")

    session.delete(partido)
    session.commit()
    return {
        "mensaje": "Partido de torneo eliminado con exito",
        "partido_torneo_id": partido_torneo_id,
    }
