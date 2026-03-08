# 🚂 Guía de Deploy en Railway

## 📋 Preparación

Tu proyecto ya está configurado para Railway. Archivos creados:

- ✅ `Procfile` - Comando de inicio
- ✅ `railway.toml` - Configuración Railway
- ✅ `nixpacks.toml` - Configuración de build
- ✅ `start.sh` - Script que ejecuta migraciones
- ✅ `runtime.txt` - Versión de Python
- ✅ Backend preparado con CORS y DATABASE_URL
- ✅ Frontend preparado con variable de entorno

---

## 🚀 Paso 1: Subir a GitHub

```bash
# Asegurate de estar en la rama correcta
git status

# Agregar todos los cambios
git add .

# Commit
git commit -m "Preparar proyecto para Railway"

# Push a GitHub
git push origin main
```

---

## 🚂 Paso 2: Crear Cuenta en Railway

1. Ve a **[railway.app](https://railway.app)**
2. Haz clic en **"Start a New Project"**
3. **Login with GitHub** (conecta tu cuenta)

---

## 🗄️ Paso 3: Crear Base de Datos PostgreSQL

1. En Railway, haz clic en **"New Project"**
2. Selecciona **"Provision PostgreSQL"**
3. Espera a que se cree (tarda ~30 segundos)
4. **¡No cierres esta ventana!** Necesitarás la DATABASE_URL

---

## 🐍 Paso 4: Deploy del Backend (FastAPI)

### Opción A: Desde el mismo proyecto

1. En el proyecto donde está PostgreSQL
2. Haz clic en **"+ New"** → **"GitHub Repo"**
3. Selecciona tu repositorio `futbol`
4. Railway detectará automáticamente que es Python

### Configurar Variables de Entorno:

1. Haz clic en tu servicio de backend
2. Ve a la pestaña **"Variables"**
3. Agrega estas variables:

```
DATABASE_URL = (se copia automáticamente desde PostgreSQL)
RAILWAY_ENVIRONMENT = production
```

**Conectar con PostgreSQL:**
1. En tu servicio backend, ve a **"Settings"**
2. En **"Service Variables"**, haz clic en **"+ New Variable"** → **"Add Reference"**
3. Selecciona `PostgreSQL` → `DATABASE_URL`

### Root Directory (Importante):

Si Railway no detecta correctamente:
1. Ve a **"Settings"** de tu servicio backend
2. En **"Root Directory"** déjalo en `/` (raíz)
3. Guarda cambios

### Deploy:

1. Railway automáticamente hará el build y deploy
2. Espera a que termine (2-5 minutos la primera vez)
3. Verás los logs: migraciones ejecutándose y servidor iniciando
4. Obtendrás una URL pública como: `https://futbol-production-xxxx.up.railway.app`

---

## 🎨 Paso 5: Deploy del Frontend (SvelteKit)

### Opción Recomendada: Vercel (Mejor para SvelteKit)

1. Ve a **[vercel.com](https://vercel.com)**
2. **"New Project"** → Importa tu repo de GitHub
3. Configuración:
   - **Framework Preset:** SvelteKit
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `.svelte-kit`

4. **Variables de Entorno en Vercel:**
   ```
   VITE_API_URL = https://tu-backend-railway.up.railway.app
   ```
   *(Usa la URL que te dio Railway en el paso 4)*

5. Haz clic en **"Deploy"**

### Alternativa: También en Railway

1. En Railway, **"New Project"** → **"GitHub Repo"**
2. Selecciona tu repo y configura:
   - **Root Directory:** `frontend`
   - **Start Command:** `npm run build && npm run preview`
3. Variables de entorno:
   ```
   VITE_API_URL = https://tu-backend-railway.up.railway.app
   ```

---

## ✅ Paso 6: Verificar Todo Funciona

1. **Backend:** Abre `https://tu-backend.up.railway.app/docs`
   - Deberías ver la documentación de FastAPI
   - Prueba un endpoint (ej: GET /Jugadores/)

2. **Frontend:** Abre tu URL de Vercel/Railway
   - La app debería cargar
   - Deberías ver jugadores, equipos, etc.

3. **PostgreSQL:** En Railway
   - Ve al servicio PostgreSQL
   - Pestaña **"Data"** para ver las tablas

---

## 🔄 Paso 7: Cargar Datos Iniciales (Opcional)

### Opción A: Desde Railway CLI

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Conectar al proyecto
railway link

# Ejecutar seed
railway run python seed.py
```

### Opción B: Desde tu computadora conectándote a Railway DB

1. En Railway, copia las credenciales de PostgreSQL
2. Actualiza tu `.env` local con esas credenciales
3. Ejecuta: `python seed.py`

---

## 🎯 Resumen de URLs

Después del deploy tendrás:

- **Backend API:** `https://futbol-production-xxxx.up.railway.app`
- **Docs API:** `https://futbol-production-xxxx.up.railway.app/docs`
- **Frontend:** `https://tu-proyecto.vercel.app`
- **PostgreSQL:** (interno en Railway)

---

## 🐛 Solución de Problemas

### Backend no inicia:

1. Ve a **"Deployments"** en Railway
2. Haz clic en el último deploy
3. Ve a **"View Logs"**
4. Busca errores en las migraciones o inicio

### Frontend no se conecta al backend:

1. Verifica que `VITE_API_URL` esté bien configurada en Vercel
2. Abre la consola del navegador (F12)
3. Verifica que las peticiones vayan a la URL correcta de Railway

### Base de datos vacía:

1. Ejecuta el seed con Railway CLI: `railway run python seed.py`
2. O conéctate directamente a la DB y ejecuta `seed.py`

### Error de CORS:

- El backend ya está configurado para permitir todos los orígenes en producción
- Si hay problemas, verifica los logs del backend en Railway

---

## 🔧 Comandos Útiles

```bash
# Ver logs en tiempo real
railway logs

# Ejecutar comando en Railway
railway run python seed.py

# Conectar a PostgreSQL directamente
railway connect

# Ver variables de entorno
railway variables
```

---

## 💰 Costos

### Railway:
- **Plan Gratuito:** $5 USD de crédito mensual (suficiente para proyectos pequeños)
- Si se acaba: ~$5-10 USD/mes para proyectos personales
- PostgreSQL incluido

### Vercel:
- **Completamente gratis** para proyectos personales
- Ilimitado

---

## 📝 Próximos Pasos

Una vez desplegado:

1. ✅ Compartí la URL con quien quieras
2. ✅ El proyecto se actualiza automáticamente al hacer push a GitHub
3. ✅ Podés ver métricas y logs en Railway/Vercel
4. ✅ Agregá un dominio personalizado (gratis en Vercel)

---

## 🆘 Ayuda

- **Railway Docs:** https://docs.railway.app
- **Vercel Docs:** https://vercel.com/docs
- **SvelteKit Deploy:** https://kit.svelte.dev/docs/adapters

¡Listo para deployar! 🚀
