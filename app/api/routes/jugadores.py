import base64

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.entities import EstadisticaPartido, Jugador
from app.schemas.common import JugadorCreate

router = APIRouter(prefix="/Jugadores", tags=["Jugadores"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


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


@router.post("/upload-imagen")
async def upload_imagen_jugador(archivo: UploadFile = File(...)):
    if archivo.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Formato no permitido. Usa JPG, PNG o WEBP",
        )

    content = await archivo.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="La imagen supera 5MB")

    base64_content = base64.b64encode(content).decode("utf-8")
    media_type = archivo.content_type or "image/jpeg"
    image_data_url = f"data:{media_type};base64,{base64_content}"
    return {"url": image_data_url}


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


@router.delete("/{jugador_id}")
def eliminar_jugador(jugador_id: int, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    participacion = session.exec(
        select(EstadisticaPartido.id).where(EstadisticaPartido.jugador_id == jugador_id)
    ).first()
    if participacion:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el jugador porque participo en partidos",
        )

    session.delete(jugador)
    session.commit()

    return {"mensaje": "Jugador eliminado con exito", "jugador_id": jugador_id}
