# 🎯 Deploy 100% GRATIS (Sin Tarjeta, Sin Sorpresas)

## ⚠️ Importante: Railway NO es gratis ilimitado
Railway te da $5 USD/mes gratis, pero si tu app crece, **puede consumir más y cobrarte**. 

## ✅ Opciones 100% GRATIS para SIEMPRE

---

## 🥇 OPCIÓN 1: Render + Supabase (RECOMENDADO)

**✅ Ventajas:**
- 100% gratis para siempre
- No necesita tarjeta
- PostgreSQL ilimitado tiempo
- Fácil de usar

**⚠️ Limitación:**
- Backend se "duerme" después de 15 min sin uso (tarda ~30 seg en despertar)

### Backend en Render.com

1. **Crear cuenta en [render.com](https://render.com)**
   - Puedes usar GitHub para login

2. **Conectar tu repositorio**
   - New → Web Service
   - Connect tu repo de GitHub
   - Root Directory: dejar vacío (usa la raíz)

3. **Configurar el servicio**
   ```
   Name: futbol-api (o el nombre que quieras)
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: sh start.sh
   ```

4. **Variables de entorno**
   ```
   DATABASE_URL = (copiar de Supabase - paso siguiente)
   ```

5. **Plan:** Free (seleccionar el gratuito)

6. **Deploy:** Click en "Create Web Service"

### Base de Datos en Supabase

1. **Crear cuenta en [supabase.com](https://supabase.com)**
   - Gratis, no necesita tarjeta

2. **Nuevo proyecto**
   - New Project
   - Name: futbol-db
   - Database Password: (guarda esta contraseña)
   - Region: South America (más cercano)
   - Free tier

3. **Obtener DATABASE_URL**
   - Settings → Database
   - Connection string → URI
   - Copiar algo como: `postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres`

4. **Pegar en Render**
   - Volver a Render
   - Environment → DATABASE_URL → Add
   - Pegar la URL de Supabase
   - Save Changes

### Frontend en Vercel

1. **Crear cuenta en [vercel.com](https://vercel.com)**
   - Usar GitHub

2. **Import proyecto**
   - Add New → Project
   - Import tu repo
   - Root Directory: `frontend`
   - Framework Preset: SvelteKit

3. **Variable de entorno**
   ```
   VITE_API_URL = https://tu-app.onrender.com
   ```
   (Copiar la URL que te dio Render)

4. **Deploy**

### Cargar datos iniciales

```bash
# Instalar Supabase CLI (una vez)
curl -sSfL https://supabase.com/install.sh | sh

# O con npm
npm install -g supabase

# Conectar a tu proyecto
supabase link --project-ref [TU-PROJECT-REF]

# Cargar datos
PGPASSWORD=[tu-password] psql -h db.xxx.supabase.co -U postgres -d postgres -f seed.sql
```

O simplemente ejecuta localmente con la DATABASE_URL de Supabase:
```bash
export DATABASE_URL="postgresql://postgres:..."
python seed.py
```

---

## 🥈 OPCIÓN 2: Fly.io (Alternativa sin hibernación)

**✅ Ventajas:**
- Gratis para siempre (3 VMs pequeñas)
- NO se duerme (siempre activo)
- PostgreSQL incluido

**⚠️ Desventaja:**
- Requiere tarjeta (pero NO cobra si no superas límites)

### Setup Fly.io

1. **Instalar flyctl**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Crear app**
   ```bash
   fly launch
   # Responde: No a PostgreSQL por ahora
   # Selecciona región más cercana
   ```

4. **Agregar PostgreSQL**
   ```bash
   fly postgres create --name futbol-db
   fly postgres attach futbol-db
   ```

5. **Deploy**
   ```bash
   fly deploy
   ```

6. **Ver URL**
   ```bash
   fly open
   ```

### Frontend: Igual que Opción 1 (Vercel)

---

## 🥉 OPCIÓN 3: PythonAnywhere (TODO EN UNO)

**✅ Ventajas:**
- Todo en un solo lugar
- 100% gratis
- Muy simple

**⚠️ Desventajas:**
- MySQL en vez de PostgreSQL en free tier
- Menos potente
- Más limitaciones

[Ver guía oficial](https://help.pythonanywhere.com/pages/Flask/)

---

## 📊 Comparación Rápida

| Servicio | Backend | Base Datos | Hibernación | Tarjeta | Mejor Para |
|----------|---------|------------|-------------|---------|------------|
| **Render + Supabase** | ✅ Gratis | ✅ PostgreSQL 500MB | ⚠️ Sí (15 min) | ❌ No | **Apps personales** |
| **Fly.io** | ✅ Gratis | ✅ PostgreSQL 3GB | ✅ Siempre activo | ⚠️ Sí (no cobra) | **Producción seria** |
| **Railway** | ⚠️ $5/mes | ✅ PostgreSQL | ✅ Siempre activo | ⚠️ Sí | Puede cobrarte |
| **PythonAnywhere** | ✅ Gratis | ⚠️ MySQL | ✅ Siempre activo | ❌ No | Muy básico |

---

## 🎯 Mi Recomendación para Vos

### Si querés CERO riesgo de pagar:
👉 **Render + Supabase + Vercel**

Pasos resumidos:
1. Subir código a GitHub
2. Crear DB en Supabase (2 min)
3. Deploy backend en Render (5 min)
4. Deploy frontend en Vercel (2 min)
5. Cargar datos con seed.py (1 min)

**Total: ~10 minutos, $0 para siempre**

---

## 🆘 Ayuda

¿Querés que te guíe paso a paso con capturas de pantalla? Decime qué opción preferís y te armo una guía detallada.

### Links útiles:
- [Render Free Tier](https://render.com/docs/free)
- [Supabase Free Tier](https://supabase.com/pricing)
- [Vercel Free Tier](https://vercel.com/pricing)
- [Fly.io Free Tier](https://fly.io/docs/about/pricing/)
