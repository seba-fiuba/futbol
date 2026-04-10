"""Compatibilidad para imports existentes.

Nuevo módulo recomendado: app.core.database
"""

from app.core.database import DATABASE_URL, engine, get_session

__all__ = ["DATABASE_URL", "engine", "get_session"]
