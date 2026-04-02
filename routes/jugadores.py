from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlmodel import Session, select
from database import get_session
from models import Jugador, JugadorCreate

router = APIRouter(prefix="/Jugadores", tags=["Jugadores"])

UPLOAD_DIR = Path("uploads/jugadores")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

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
async def upload_imagen_jugador(request: Request, archivo: UploadFile = File(...)):
    if archivo.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Formato no permitido. Usa JPG, PNG o WEBP",
        )

    extension = Path(archivo.filename or "").suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
        extension = ".jpg"

    filename = f"jugador_{uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / filename

    content = await archivo.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="La imagen supera 5MB")

    file_path.write_bytes(content)

    image_url = f"{request.base_url}uploads/jugadores/{filename}"
    return {"url": image_url}


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
