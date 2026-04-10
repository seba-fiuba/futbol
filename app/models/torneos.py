from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Torneo(SQLModel, table=True):
    __tablename__ = "torneos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    estado: str = Field(default="abierto", max_length=20)
    equipos: List["EquipoTorneo"] = Relationship(back_populates="torneo")
    partidos: List["PartidoTorneo"] = Relationship(back_populates="torneo")


class EquipoTorneo(SQLModel, table=True):
    __tablename__ = "equipos_torneo"

    id: Optional[int] = Field(default=None, primary_key=True)
    torneo_id: int = Field(foreign_key="torneos.id")
    nombre: str = Field(max_length=100)

    torneo: Optional[Torneo] = Relationship(back_populates="equipos")
    jugadores: List["JugadorTorneo"] = Relationship(back_populates="equipo")


class JugadorTorneo(SQLModel, table=True):
    __tablename__ = "jugadores_torneo"

    id: Optional[int] = Field(default=None, primary_key=True)
    equipo_torneo_id: int = Field(foreign_key="equipos_torneo.id")
    usuario_id: int = Field(index=True)

    equipo: Optional[EquipoTorneo] = Relationship(back_populates="jugadores")


class PartidoTorneo(SQLModel, table=True):
    __tablename__ = "partidos_torneo"

    id: Optional[int] = Field(default=None, primary_key=True)
    torneo_id: int = Field(foreign_key="torneos.id")
    local_id: int = Field(foreign_key="equipos_torneo.id")
    visitante_id: int = Field(foreign_key="equipos_torneo.id")

    goles_local: Optional[int] = Field(default=None)
    goles_visitante: Optional[int] = Field(default=None)
    fase: str = Field(default="liga", max_length=50)
    jugado: bool = Field(default=False)

    torneo: Optional[Torneo] = Relationship(back_populates="partidos")

    local: Optional[EquipoTorneo] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "PartidoTorneo.local_id==EquipoTorneo.id"
        }
    )
    visitante: Optional[EquipoTorneo] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "PartidoTorneo.visitante_id==EquipoTorneo.id"
        }
    )
