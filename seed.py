from sqlmodel import Session
from database import engine
from models import Jugador, Equipo


def seed_equipos():
    """Carga equipos iniciales en la base de datos."""
    equipos_data = [
        {"nombre": "Negro"},
        {"nombre": "Color"},
    ]

    with Session(engine) as session:
        # Verificar si ya hay equipos
        equipos_existentes = session.query(Equipo).count()
        if equipos_existentes > 0:
            print(
                f"Ya hay {equipos_existentes} equipos en la base de datos. Saltando seed de equipos."
            )
            return

        # Crear equipos
        for equipo_dict in equipos_data:
            equipo = Equipo(**equipo_dict)
            session.add(equipo)

        session.commit()
        print(f"✅ {len(equipos_data)} equipos cargados exitosamente.")


def seed_jugadores():
    """Carga jugadores iniciales en la base de datos.

    NOTAS SOBRE IMÁGENES:
    - Las imágenes se guardan en: frontend/static/jugadores/
    - En la BD se guarda la ruta: "/jugadores/nombre-archivo.jpg"
    - También podes usar URLs externas: "https://..."
    - Si es None, el frontend muestra un emoji por defecto 👤

    Ejemplos:
        {"nombre": "Juan", "apodo": "Pepe", "imagen": "/jugadores/juan.jpg"}
        {"nombre": "María", "apodo": "Mary", "imagen": "https://example.com/maria.jpg"}
        {"nombre": "Pedro", "apodo": "Pete", "imagen": None}
    """
    jugadores_data = [
        {"nombre": "Juampy", "apodo": "La Hiena", "imagen": None},
        {"nombre": "Bianca", "apodo": "EL Bicho", "imagen": None},
        {"nombre": "Santi", "apodo": "Chicho", "imagen": None},
        {"nombre": "Cande", "apodo": "La Chispa", "imagen": None},
        {"nombre": "Cindy", "apodo": "La Araña", "imagen": None},
        {"nombre": "Cami", "apodo": "La Pesadilla", "imagen": None},
        {"nombre": "Rodri", "apodo": "El Fuego", "imagen": None},
        {"nombre": "Jorge", "apodo": "El Curioso", "imagen": None},
        {"nombre": "Fran", "apodo": "El Francotirador", "imagen": None},
        {"nombre": "Nahue", "apodo": "El tanque", "imagen": None},
        {"nombre": "Valen", "apodo": "La Bala", "imagen": None},
        {"nombre": "Giuli", "apodo": "La Guille", "imagen": None},
        {"nombre": "Ivo", "apodo": "El Vivo", "imagen": None},
        {"nombre": "Seba", "apodo": "El Zezozo", "imagen": None},
        {"nombre": "Juan Cruz", "apodo": "Garnacho", "imagen": None},
        {"nombre": "Enzo", "apodo": "Primo", "imagen": None},
        {"nombre": "Alvarito", "apodo": "La Maquina", "imagen": None},
        {"nombre": "Mile", "apodo": "La Prodigio", "imagen": None},
        {"nombre": "Seba", "apodo": "Amigo de Chicho", "imagen": None},
        {"nombre": "Gonza", "apodo": "Hermano de Giu", "imagen": None},
    ]

    with Session(engine) as session:
        # Verificar si ya hay jugadores
        jugadores_existentes = session.query(Jugador).count()
        if jugadores_existentes > 0:
            print(
                f"Ya hay {jugadores_existentes} jugadores en la base de datos. Saltando seed de jugadores."
            )
            return

        # Crear jugadores
        for jugador_dict in jugadores_data:
            jugador = Jugador(**jugador_dict)
            session.add(jugador)

        session.commit()
        print(f"✅ {len(jugadores_data)} jugadores cargados exitosamente.")


def seed_all():
    """Ejecuta todas las funciones de seed."""
    print("🌱 Iniciando seed de la base de datos...\n")

    seed_equipos()
    seed_jugadores()

    print("\n🎉 Seed completado exitosamente!")


if __name__ == "__main__":
    seed_all()
