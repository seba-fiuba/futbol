"""Compatibilidad para imports existentes.

Nuevo módulo recomendado: app.schemas.common
"""

from app.schemas.common import (
    EquipoCreate,
    EstadisticaCreate,
    JugadorCreate,
    PartidoCreate,
)

__all__ = ["EstadisticaCreate", "PartidoCreate", "JugadorCreate", "EquipoCreate"]
