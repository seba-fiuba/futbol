#!/usr/bin/env python
"""
Script para actualizar imágenes de jugadores.

Uso:
    python actualizar_imagenes.py
"""

from sqlmodel import Session, select
from database import engine
from models import Jugador


def listar_jugadores():
    """Muestra todos los jugadores con sus imágenes actuales."""
    with Session(engine) as session:
        statement = select(Jugador)
        jugadores = session.exec(statement).all()

        print("\n📋 JUGADORES REGISTRADOS:")
        print("-" * 80)
        for j in jugadores:
            imagen_info = j.imagen if j.imagen else "Sin imagen"
            print(
                f"ID: {j.id:3d} | {j.nombre:20s} | {j.apodo or 'Sin apodo':20s} | {imagen_info}"
            )
        print("-" * 80)
        print(f"Total: {len(jugadores)} jugadores\n")


def actualizar_imagen(jugador_id: int, ruta_imagen: str):
    """Actualiza la imagen de un jugador.

    Args:
        jugador_id: ID del jugador
        ruta_imagen: Ruta de la imagen (ej: "/jugadores/nombre.jpg")
    """
    with Session(engine) as session:
        jugador = session.get(Jugador, jugador_id)

        if not jugador:
            print(f"❌ No se encontró jugador con ID {jugador_id}")
            return False

        jugador.imagen = ruta_imagen
        session.add(jugador)
        session.commit()

        print(f"✅ Imagen actualizada para {jugador.nombre}: {ruta_imagen}")
        return True


def actualizar_multiples():
    """Actualiza imágenes de múltiples jugadores.

    Modifica el diccionario 'actualizaciones' con los IDs y rutas de imagen.
    """
    # ⚠️ CONFIGURA AQUÍ TUS ACTUALIZACIONES
    actualizaciones = {
        # ID: ruta_imagen
        # Ejemplos:
        # 1: "/jugadores/juampy.jpg",
        # 2: "/jugadores/bianca.jpg",
        # 3: "/jugadores/santi.jpg",
    }

    if not actualizaciones:
        print("⚠️  No hay actualizaciones configuradas.")
        print("   Edita el diccionario 'actualizaciones' en este script.")
        return

    with Session(engine) as session:
        for jugador_id, ruta in actualizaciones.items():
            jugador = session.get(Jugador, jugador_id)

            if jugador:
                jugador.imagen = ruta
                session.add(jugador)
                print(f"✓ {jugador.nombre} → {ruta}")
            else:
                print(f"✗ No se encontró jugador con ID {jugador_id}")

        session.commit()
        print("\n✅ Actualizaciones completadas")


def menu():
    """Menú interactivo para gestionar imágenes."""
    while True:
        print("\n🖼️  GESTIÓN DE IMÁGENES DE JUGADORES")
        print("=" * 50)
        print("1. Listar todos los jugadores")
        print("2. Actualizar imagen de un jugador")
        print("3. Actualizar múltiples imágenes (configurado en script)")
        print("0. Salir")
        print("=" * 50)

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "0":
            print("👋 ¡Hasta luego!")
            break

        elif opcion == "1":
            listar_jugadores()

        elif opcion == "2":
            listar_jugadores()
            try:
                jugador_id = int(input("ID del jugador: ").strip())
                print("\nEjemplos de rutas:")
                print("  - /jugadores/nombre.jpg  (imagen local)")
                print("  - https://ejemplo.com/imagen.jpg  (URL externa)")
                print("  - (dejar vacío para sin imagen)")
                ruta = input("Ruta de la imagen: ").strip()

                if ruta == "":
                    ruta = None

                actualizar_imagen(jugador_id, ruta)
            except ValueError:
                print("❌ ID inválido")

        elif opcion == "3":
            actualizar_multiples()

        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    print(
        """
    📸 GESTIÓN DE IMÁGENES DE JUGADORES
    
    PASOS:
    1. Guarda las imágenes en: frontend/static/jugadores/
    2. Usa este script para relacionarlas con los jugadores
    3. La ruta debe ser: /jugadores/nombre-archivo.jpg
    
    Ejemplo:
      - Guardas: frontend/static/jugadores/messi.jpg
      - Ingresas: /jugadores/messi.jpg
    """
    )

    menu()
