from app.schemas.common import (
    EquipoCreate,
    EstadisticaCreate,
    JugadorCreate,
    PartidoCreate,
)
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

__all__ = [
    "EstadisticaCreate",
    "PartidoCreate",
    "JugadorCreate",
    "EquipoCreate",
    "TorneoCreate",
    "TorneoUpdate",
    "TorneoRead",
    "EquipoTorneoCreate",
    "EquipoTorneoUpdate",
    "EquipoTorneoRead",
    "JugadorTorneoCreate",
    "JugadorTorneoUpdate",
    "JugadorTorneoRead",
    "PartidoTorneoCreate",
    "PartidoTorneoUpdate",
    "PartidoTorneoRead",
]
