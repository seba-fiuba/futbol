# ⚽ Fútbol Manager - Frontend

Frontend web desarrollado con SvelteKit para gestionar partidos, equipos y jugadores de fútbol.

## 🚀 Características

- 📊 **Dashboard** - Vista general con estadísticas
- 👥 **Jugadores** - Lista y búsqueda de jugadores
- 🏆 **Equipos** - Tabla de posiciones actualizada
- ⚽ **Partidos** - Registro y edición de partidos con goleadores
- 🎯 **Goleadores** - Tabla de máximos anotadores con podio

## 🛠️ Tecnologías

- **SvelteKit** - Framework web
- **Tailwind CSS** - Estilos
- **Vite** - Build tool

## 📋 Requisitos

- Node.js 18+ 
- npm o pnpm

## ⚙️ Instalación

```bash
# Instalar dependencias
npm install

# Modo desarrollo
npm run dev

# Build para producción
npm run build

# Preview de producción
npm run preview
```

## 🔗 Configuración

El frontend se conecta al backend en `http://localhost:8000` por defecto.

Para cambiar la URL del API, edita el archivo `src/lib/api.js`:

```javascript
const API_BASE = 'http://tu-backend:puerto';
```

## 📱 Páginas

- `/` - Inicio con accesos rápidos
- `/jugadores` - Lista de jugadores
- `/equipos` - Tabla de posiciones
- `/partidos` - Lista de partidos
- `/partidos/nuevo` - Registrar nuevo partido
- `/goleadores` - Tabla de goleadores

## 🎨 Personalización

Los colores y estilos están configurados en:
- `tailwind.config.js` - Configuración de Tailwind
- `src/app.css` - Estilos globales

## 📝 Notas

- Asegúrate de que el backend esté corriendo antes de iniciar el frontend
- El backend debe tener CORS habilitado para aceptar peticiones del frontend
