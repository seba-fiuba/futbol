"""Punto de entrada compatible para todos los modelos.

Nuevos módulos recomendados:
- app.models.entities
- app.models.torneos
- app.schemas.common
"""

from app.models.entities import Equipo, EstadisticaPartido, Jugador, Partido
from app.models.torneos import EquipoTorneo, JugadorTorneo, PartidoTorneo, Torneo
from app.schemas.common import (
    EquipoCreate,
    EstadisticaCreate,
    JugadorCreate,
    PartidoCreate,
)

__all__ = [
    "Jugador",
    "Equipo",
    "Partido",
    "EstadisticaPartido",
    "EstadisticaCreate",
    "PartidoCreate",
    "JugadorCreate",
    "EquipoCreate",
    "Torneo",
    "EquipoTorneo",
    "JugadorTorneo",
    "PartidoTorneo",
]
