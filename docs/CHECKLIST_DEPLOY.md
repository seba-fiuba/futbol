# ✅ Checklist: Deploy

⚠️ **IMPORTANTE:** Railway puede cobrarte si superas $5/mes. Para opciones **100% GRATIS**, lee [DEPLOY_GRATIS_100.md](DEPLOY_GRATIS_100.md)

## Deploy a Railway (Puede tener costos)

Antes de deployar, verifica que tengas todo:

## 📦 Archivos Necesarios (Ya creados ✅)

- [x] `Procfile` - Comando de inicio
- [x] `railway.toml` - Config de Railway
- [x] `nixpacks.toml` - Config de build
- [x] `start.sh` - Script de migraciones
- [x] `runtime.txt` - Python 3.14
- [x] `requirements.txt` - Dependencias
- [x] `.env.example` - Ejemplo de variables
- [x] `frontend/.env.example` - Variables del frontend

## 🔧 Código Preparado (Ya listo ✅)

- [x] `database.py` - Maneja DATABASE_URL de Railway
- [x] `main.py` - CORS configurado para producción
- [x] `frontend/src/lib/api.js` - Variables de entorno
- [x] `.gitignore` - Archivos ignorados correctamente

## 📝 Pasos para Deploy

1. **Subir a GitHub**
   ```bash
   git add .
   git commit -m "Preparar para Railway"
   git push origin main
   ```

2. **Railway - PostgreSQL**
   - Crear proyecto en railway.app
   - Provisionar PostgreSQL
   - Copiar DATABASE_URL

3. **Railway - Backend**
   - Deploy desde GitHub
   - Conectar PostgreSQL (Add Reference)
   - Esperar build (~3 min)
   - Obtener URL pública

4. **Vercel - Frontend**
   - Deploy desde GitHub
   - Root Directory: `frontend`
   - Variable: `VITE_API_URL` = URL de Railway
   - Deploy automático

5. **Cargar Datos**
   ```bash
   railway run python seed.py
   ```

6. **✅ ¡Listo!**
   - Compartí tu URL
   - Probá todas las funciones

## 📖 Guía Completa

Lee [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md) para instrucciones detalladas paso a paso.

## 🆘 ¿Problemas?

- **Backend no inicia:** Revisa logs en Railway → Deployments
- **Frontend no conecta:** Verifica `VITE_API_URL` en Vercel
- **DB vacía:** Ejecuta `railway run python seed.py`
- **CORS errors:** Ya está configurado, revisa logs del backend

## 💰 Costos

- Railway: $5 USD/mes gratis, **pero puede cobrar más si creces** ⚠️
- Vercel: 100% gratis para siempre
- **Total: Potencialmente NO GRATIS**

### ✅ Alternativa 100% Gratis
Lee [DEPLOY_GRATIS_100.md](DEPLOY_GRATIS_100.md) para opciones que NUNCA cobran
