from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class EstadisticaCreate(BaseModel):
    jugador_id: int
    equipo_id: int
    goles: int


class PartidoCreate(BaseModel):
    fecha: date
    equipo_local_id: int
    equipo_visitante_id: int
    goles_local: int
    goles_visitante: int
    estadisticas: List[EstadisticaCreate]


class JugadorCreate(BaseModel):
    nombre: str
    apodo: Optional[str] = None
    imagen_url: Optional[str] = None


class EquipoCreate(BaseModel):
    nombre: str
