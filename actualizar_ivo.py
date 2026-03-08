#!/usr/bin/env python
"""Script rápido para actualizar la imagen de Ivo"""

from sqlmodel import Session, select
from database import engine
from models import Jugador

# Buscar a Ivo y actualizar su imagen
with Session(engine) as session:
    statement = select(Jugador).where(Jugador.nombre == "Ivo")
    ivo = session.exec(statement).first()

    if ivo:
        ivo.imagen = "/jugadores/ivo_perfil.png"
        session.add(ivo)
        session.commit()
        print(f"✅ Imagen actualizada para {ivo.nombre} '{ivo.apodo}'")
        print(f"   Ruta: {ivo.imagen}")
    else:
        print("❌ No se encontró el jugador Ivo")
