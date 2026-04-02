from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from routes import jugadores, equipos, partidos, estadisticas

app = FastAPI(title="Fútbol Manager API", version="1.0.0")

# Configurar CORS
# En desarrollo permite localhost, en producción permite cualquier origen
is_production = (
    os.getenv("RAILWAY_ENVIRONMENT") is not None or os.getenv("RENDER") is not None
)

if is_production:
    # En producción, permite todos los orígenes (puedes restringir después)
    allowed_origins = ["*"]
else:
    # En desarrollo, solo localhost
    allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectamos las rutas al main para mantener la API sincronizada en despliegues
# comentario
app.include_router(jugadores.router)
app.include_router(equipos.router)
app.include_router(partidos.router)
app.include_router(estadisticas.router)

# Archivos subidos (imagenes de jugadores)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
