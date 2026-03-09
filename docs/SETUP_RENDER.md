# 🎯 Guía Paso a Paso: Render + Supabase

## ✅ Tu Código Ya Está Listo

No necesitas cambiar nada en el código. Ya está preparado para:
- ✅ Detectar automáticamente Render como producción
- ✅ Usar DATABASE_URL de Supabase
- ✅ Ejecutar migraciones automáticamente al iniciar
- ✅ CORS configurado para producción

---

## 📋 PASO 1: Configurar Supabase (Base de Datos)

### 1.1. Obtener la URL de conexión

Ya creaste el proyecto en Supabase. Ahora necesitas la URL:

1. Ve a tu proyecto en [supabase.com](https://supabase.com)
2. Click en **Settings** (⚙️) en el sidebar izquierdo
3. Click en **Database**
4. Busca la sección **Connection string**
5. Click en **URI** (no en Session pooling)
6. Verás algo como:
   ```
   postgresql://postgres.xxxxx:[YOUR-PASSWORD]@xxxxx.supabase.co:5432/postgres
   ```
7. **Reemplaza `[YOUR-PASSWORD]`** con la contraseña que creaste al crear el proyecto
8. **Copia esta URL completa** (la vas a necesitar en el siguiente paso)

📝 **Ejemplo de URL correcta:**
```
postgresql://postgres.abcdefghijk:tu_contraseña_aqui@db.abcdefghijk.supabase.co:5432/postgres
```

---

## 📋 PASO 2: Configurar Render (Backend)

Ya creaste el proyecto en Render. Ahora configúralo:

### 2.1. Configurar el Build y Start

1. Ve a tu servicio en [render.com](https://dashboard.render.com)
2. Click en tu servicio (futbol-backend o como lo hayas llamado)
3. Ve a **Settings** → **Build & Deploy**
4. Configura:

   **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```

   **Start Command:**
   ```bash
   sh start.sh
   ```

   ⚠️ **IMPORTANTE:** Usar `start.sh` ejecuta automáticamente las migraciones de Alembic antes de iniciar el servidor.

### 2.2. Agregar la Variable de Entorno DATABASE_URL

1. En el mismo servicio, ve a **Environment**
2. Click en **Add Environment Variable**
3. Agrega:
   - **Key:** `DATABASE_URL`
   - **Value:** (pega la URL que copiaste de Supabase en el PASO 1)

   Ejemplo:
   ```
   DATABASE_URL = postgresql://postgres.xxxxx:tu_password@db.xxxxx.supabase.co:5432/postgres
   ```

4. Click en **Save Changes**

### 2.3. Deploy Manual (primera vez)

1. Ve a la pestaña **Manual Deploy**
2. Click en **Deploy latest commit**
3. Espera ~2-3 minutos mientras:
   - Instala las dependencias
   - Ejecuta las migraciones de Alembic
   - Inicia el servidor

### 2.4. Verificar que funcionó

1. Ve a **Logs** en tu servicio
2. Deberías ver:
   ```
   🚀 Ejecutando migraciones de Alembic...
   ✅ Migraciones completadas
   🌟 Iniciando servidor FastAPI...
   Application startup complete.
   ```

3. Copia la **URL de tu servicio** (algo como `https://futbol-backend-xxxx.onrender.com`)
4. Prueba abriendo en tu navegador:
   ```
   https://tu-url.onrender.com/docs
   ```
   Deberías ver la documentación de FastAPI (Swagger UI)

---

## 📋 PASO 3: Cargar Datos Iniciales

Ahora que tu backend está funcionando, carga los datos de prueba:

### Opción A: Desde tu PC (Recomendado)

```bash
# En tu terminal, en la carpeta del proyecto
export DATABASE_URL="postgresql://postgres.xxxxx:tu_password@db.xxxxx.supabase.co:5432/postgres"
python seed.py
```

Deberías ver:
```
Limpiando datos existentes...
Creando equipos...
Creando jugadores...
✅ Seed completado: 2 equipos y 20 jugadores creados.
```

### Opción B: Usar psql directamente

```bash
# Si prefieres SQL directo
psql "postgresql://postgres.xxxxx:tu_password@db.xxxxx.supabase.co:5432/postgres" -f seed.sql
```

---

## 📋 PASO 4: Deploy del Frontend en Vercel

### 4.1. Conectar GitHub

1. Ve a [vercel.com](https://vercel.com)
2. Click en **Add New...** → **Project**
3. Busca tu repositorio de GitHub
4. Click en **Import**

### 4.2. Configurar el proyecto

**Root Directory:**
```
frontend
```

**Framework Preset:**
```
SvelteKit
```

**Build Command:** (dejar por defecto)
```
npm run build
```

**Output Directory:** (dejar por defecto)
```
.svelte-kit
```

### 4.3. Variables de Entorno

Click en **Environment Variables** y agrega:

**Key:**
```
VITE_API_URL
```

**Value:** (tu URL de Render del PASO 2.4)
```
https://futbol-backend-xxxx.onrender.com
```

⚠️ **SIN barra final** (sin `/` al final)

### 4.4. Deploy

1. Click en **Deploy**
2. Espera ~1-2 minutos
3. ¡Listo! Te dará una URL como `https://futbol-xxxx.vercel.app`

---

## 🎉 PASO 5: Probar Todo

1. **Abre tu frontend en Vercel:** `https://futbol-xxxx.vercel.app`
2. **Navega por las páginas:**
   - ✅ Inicio → Deberías ver las estadísticas
   - ✅ Jugadores → Deberías ver los 20 jugadores del seed
   - ✅ Equipos → Deberías ver "Negro" y "Color"
   - ✅ Partidos → Página vacía (normal, no hay partidos aún)
   - ✅ Goleadores → Página vacía (normal, no hay goles aún)

3. **Crear un partido de prueba:**
   - Ve a "Partidos" → "Nuevo Partido"
   - Selecciona equipos
   - Agrega algunos goles
   - Guarda
   - ¡Verifica que aparezca en la tabla de partidos y goleadores!

---

## 🔧 Troubleshooting

### ❌ Backend no inicia en Render

**Ver logs:**
1. Ve a tu servicio en Render
2. Click en **Logs**
3. Busca errores rojos

**Errores comunes:**
- `relation "jugador" does not exist` → Las migraciones no corrieron. Verifica que el Start Command sea `sh start.sh`
- `could not connect to server` → DATABASE_URL incorrecta. Verifica la contraseña en Supabase
- `ImportError: No module named 'X'` → Falta una dependencia. Verifica `requirements.txt`

### ❌ Frontend no conecta con Backend

**Verificar:**
1. Ve a Vercel → Tu proyecto → Settings → Environment Variables
2. Verifica que `VITE_API_URL` tenga la URL correcta de Render
3. Si la cambiaste, necesitas **Redeploy:**
   - Vercel → Tu proyecto → Deployments → Latest → ⋮ → Redeploy

**Probar la API directamente:**
```bash
curl https://tu-backend.onrender.com/jugadores
# Debería devolver JSON con jugadores
```

### ❌ CORS Error en el frontend

**Verificar logs del backend:**
- El código ya maneja CORS automáticamente
- En producción permite todos los orígenes (`*`)
- Si ves errores, verifica que `RENDER=true` esté seteado (Render lo hace automáticamente)

### ❌ Base de datos vacía

**Cargar datos:**
```bash
export DATABASE_URL="tu-url-de-supabase"
python seed.py
```

**Verificar en Supabase:**
1. Ve a Table Editor en Supabase
2. Deberías ver las tablas: jugador, equipo, partido, estadisticapartido
3. Click en cada tabla para ver los datos

---

## 📊 Verificación Final

✅ **Backend funcionando:**
- [ ] `https://tu-backend.onrender.com/docs` muestra Swagger UI
- [ ] `https://tu-backend.onrender.com/jugadores` devuelve JSON

✅ **Base de datos poblada:**
- [ ] Supabase Table Editor muestra datos en las tablas
- [ ] API `/jugadores` devuelve 20 jugadores

✅ **Frontend funcionando:**
- [ ] `https://tu-frontend.vercel.app` carga correctamente
- [ ] Página de Jugadores muestra los 20 jugadores
- [ ] Página de Equipos muestra "Negro" y "Color"

✅ **Funcionalidad completa:**
- [ ] Puedes crear un partido nuevo
- [ ] Los goles se registran correctamente
- [ ] La tabla de goleadores se actualiza

---

## 📝 Resumen de URLs y Credenciales

**Guarda esta info:**

```
🗄️ Supabase (Base de Datos):
   URL: https://app.supabase.com/project/[tu-project-id]
   DATABASE_URL: postgresql://postgres.xxxxx:[pass]@db.xxxxx.supabase.co:5432/postgres

🖥️ Render (Backend):
   Dashboard: https://dashboard.render.com
   API URL: https://futbol-backend-xxxx.onrender.com
   Docs: https://futbol-backend-xxxx.onrender.com/docs

🌐 Vercel (Frontend):
   Dashboard: https://vercel.com/dashboard
   App URL: https://futbol-xxxx.vercel.app
```

---

## 🎯 Próximos Pasos

Ya tienes todo funcionando 100% gratis. Ahora puedes:

1. **Agregar más jugadores** usando el script `actualizar_imagenes.py`
2. **Subir imágenes de jugadores** a `frontend/static/jugadores/`
3. **Crear partidos** y ver estadísticas en tiempo real
4. **Compartir tu app** con tus amigos (la URL de Vercel es pública)
5. **Personalizar el diseño** editando los archivos en `frontend/src/routes/`

---

## 💡 Tips

- **Render se duerme** después de 15 minutos sin uso (plan gratis)
- La primera petición después de dormir tarda ~30 segundos
- Las siguientes son instantáneas
- Vercel NUNCA se duerme (siempre rápido)
- Supabase tiene límite de 500MB en plan gratis (más que suficiente para tu app)

---

## 🆘 ¿Necesitas ayuda?

Si algo no funciona, revisa los logs:
- **Render:** Dashboard → Tu servicio → Logs
- **Vercel:** Dashboard → Tu proyecto → Deployments → Latest → View Function Logs
- **Supabase:** Database → Query Editor (para ejecutar SQL)

¡Todo listo! 🎉
