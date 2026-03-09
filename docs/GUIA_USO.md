# 🚀 Guía de Uso - Fútbol Manager

## ⚙️ Instalación

### Backend (FastAPI)

El backend ya está configurado. Solo asegúrate de tener las dependencias instaladas:

```bash
# Desde la raíz del proyecto
pip install -r requirements.txt
```

### Frontend (SvelteKit)

Para instalar Node.js en Fedora:

```bash
# Instalar Node.js y npm
sudo dnf install nodejs npm

# Verificar instalación
node --version
npm --version
```

Luego instala las dependencias del frontend:

```bash
# Ir a la carpeta frontend
cd frontend

# Instalar dependencias
npm install
```

## 🏃 Ejecutar el Proyecto

### 1. Iniciar el Backend

Desde la raíz del proyecto:

```bash
# Activar el entorno virtual si lo tienes
source .venv/bin/activate

# Iniciar el servidor FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: `http://localhost:8000`
Documentación API: `http://localhost:8000/docs`

### 2. Iniciar el Frontend

En otra terminal, desde la carpeta `frontend`:

```bash
cd frontend
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

## 📖 Uso de la Aplicación

### 1. Página de Inicio
- Vista general del sistema
- Accesos rápidos a las funciones principales
- Estadísticas generales

### 2. Jugadores (`/jugadores`)
- Lista de todos los jugadores registrados
- Búsqueda por nombre o apodo
- Vista de tarjetas con fotos e información

### 3. Equipos (`/equipos`)
- **Tabla de posiciones** completa
- Estadísticas de cada equipo:
  - Partidos jugados, ganados, empatados, perdidos
  - Goles a favor y en contra
  - Diferencia de goles
  - Puntos (victoria = 3 pts, empate = 1 pt)
- Ordenamiento automático por puntos y diferencia de goles

### 4. Partidos (`/partidos`)
- Lista de todos los partidos registrados
- Ordenados por fecha (más recientes primero)
- Vista clara del resultado y equipos

#### Registrar Nuevo Partido (`/partidos/nuevo`)
1. Seleccionar fecha del partido
2. Elegir equipo local y equipo visitante
3. Ingresar goles de cada equipo
4. **Asignar goles a los jugadores:**
   - Usar botones "+ Gol Local" o "+ Gol Visitante"
   - Seleccionar el jugador que marcó
   - Especificar cantidad de goles (si hizo más de uno)
   - Los goles asignados deben coincidir con el resultado
5. Guardar partido

**Importante:** La suma de goles asignados a jugadores debe ser igual al resultado del partido.

### 5. Goleadores (`/goleadores`)
- **Podio con top 3 goleadores**
- Tabla completa con todos los goleadores
- Estadísticas:
  - Total de goles
  - Partidos en los que anotó
  - Promedio de goles por partido
- Ordenamiento por cantidad de goles

## 🎯 Flujo de Trabajo Recomendado

1. **Cargar Jugadores y Equipos** (via API o seed.py)
2. **Registrar Partidos** con sus goleadores
3. **Consultar Estadísticas:**
   - Ver tabla de posiciones en `/equipos`
   - Ver goleadores en `/goleadores`
   - Ver jugadores en `/jugadores`

## 📝 Cargar Datos Iniciales

Si necesitas cargar datos de prueba, usa el script seed.py:

```bash
python seed.py
```

## 🐛 Solución de Problemas

### Error de conexión entre frontend y backend
- Verifica que el backend esté corriendo en el puerto 8000
- Verifica que el frontend esté corriendo en el puerto 5173
- Revisa la consola del navegador para ver errores

### Error de CORS
- Ya está configurado en `main.py` para los puertos 5173 y 8000
- Si usas otros puertos, actualiza `allow_origins` en `main.py`

### Frontend no carga datos
- Abre las DevTools del navegador (F12)
- Ve a la pestaña "Network" para ver las peticiones
- Verifica que las respuestas del backend sean correctas

## 🔧 Desarrollo

### Modificar estilos
- Los estilos globales están en `frontend/src/app.css`
- La configuración de Tailwind está en `frontend/tailwind.config.js`

### Agregar nuevas páginas
- Crea archivos `.svelte` en `frontend/src/routes/`
- La estructura de carpetas define las rutas automáticamente

### Modificar la API
- Edita los archivos en `routes/` para modificar los endpoints
- Actualiza `models.py` para cambiar la estructura de datos

## 📚 Recursos

- [Documentación SvelteKit](https://kit.svelte.dev/docs)
- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Documentación Tailwind CSS](https://tailwindcss.com/docs)
