from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import date


class Jugador(SQLModel, table=True):
    __tablename__ = "jugadores"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apodo: Optional[str] = None
    imagen: Optional[str] = None


class Equipo(SQLModel, table=True):
    __tablename__ = "equipos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str


class Partido(SQLModel, table=True):
    __tablename__ = "partidos"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: date
    equipo_local_id: int = Field(foreign_key="equipos.id")
    equipo_visitante_id: int = Field(foreign_key="equipos.id")
    goles_local: int = Field(default=0)
    goles_visitante: int = Field(default=0)


class EstadisticaPartido(SQLModel, table=True):
    __tablename__ = "estadisticas_partidos"

    id: Optional[int] = Field(default=None, primary_key=True)
    partido_id: int = Field(foreign_key="partidos.id")
    jugador_id: int = Field(foreign_key="jugadores.id")
    equipo_id: int = Field(foreign_key="equipos.id")
    goles: int = Field(default=0)
