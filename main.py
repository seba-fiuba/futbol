from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import jugadores, equipos, partidos, estadisticas

app = FastAPI()

# Configurar CORS para permitir peticiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectamos las rutas al main
app.include_router(jugadores.router)
app.include_router(equipos.router)
app.include_router(partidos.router)
app.include_router(estadisticas.router)
