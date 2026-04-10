"""Compatibilidad para despliegues existentes.

Nuevo entrypoint recomendado: app.main:app
"""

from app.main import app

__all__ = ["app"]
