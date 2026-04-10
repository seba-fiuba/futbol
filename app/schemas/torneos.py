from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TorneoCreate(BaseModel):
    nombre: str
    estado: str = "abierto"


class TorneoUpdate(BaseModel):
    nombre: Optional[str] = None
    estado: Optional[str] = None


class TorneoRead(BaseModel):
    id: int
    nombre: str
    fecha_creacion: datetime
    estado: str


class EquipoTorneoCreate(BaseModel):
    torneo_id: int
    nombre: str


class EquipoTorneoUpdate(BaseModel):
    nombre: Optional[str] = None


class EquipoTorneoRead(BaseModel):
    id: int
    torneo_id: int
    nombre: str


class JugadorTorneoCreate(BaseModel):
    equipo_torneo_id: int
    usuario_id: int


class JugadorTorneoUpdate(BaseModel):
    equipo_torneo_id: Optional[int] = None


class JugadorTorneoRead(BaseModel):
    id: int
    equipo_torneo_id: int
    usuario_id: int


class PartidoTorneoCreate(BaseModel):
    torneo_id: int
    local_id: int
    visitante_id: int
    fase: str = "liga"


class PartidoTorneoUpdate(BaseModel):
    goles_local: Optional[int] = None
    goles_visitante: Optional[int] = None
    fase: Optional[str] = None
    jugado: Optional[bool] = None


class PartidoTorneoRead(BaseModel):
    id: int
    torneo_id: int
    local_id: int
    visitante_id: int
    goles_local: Optional[int]
    goles_visitante: Optional[int]
    fase: str
    jugado: bool
