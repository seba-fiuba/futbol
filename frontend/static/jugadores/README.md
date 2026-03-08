# 📸 Imágenes de Jugadores

Esta carpeta contiene las fotos de los jugadores.

## 📋 Formato de Nombres

Guarda las imágenes con un nombre descriptivo, por ejemplo:
- `jugador-1.jpg` o `jugador-1.png`
- `lionel-messi.jpg`
- `cristiano-ronaldo.png`

## 🖼️ Cómo usar las imágenes

### 1. Guardar la imagen aquí

Copia la imagen del jugador a esta carpeta:
```bash
cp /ruta/a/tu/imagen.jpg frontend/static/jugadores/
```

### 2. En la base de datos

Al crear o actualizar un jugador, usa la ruta relativa:
```
/jugadores/nombre-archivo.jpg
```

**Ejemplo:**
```json
{
  "nombre": "Lionel Messi",
  "apodo": "La Pulga",
  "imagen": "/jugadores/messi.jpg"
}
```

### 3. Desde el frontend

Las imágenes se acceden automáticamente desde la raíz:
```html
<img src="/jugadores/messi.jpg" alt="Messi" />
```

## 💡 Consejos

- **Formato:** Usa JPG o PNG
- **Tamaño:** Recomendado 400x400px o similar (cuadrado)
- **Peso:** Máximo 500KB por imagen
- **Nombres:** Sin espacios ni caracteres especiales (usa guiones)

## 🔧 Redimensionar imágenes (opcional)

Si necesitas redimensionar imágenes desde la terminal:

```bash
# Instalar ImageMagick
sudo dnf install ImageMagick

# Redimensionar una imagen a 400x400
convert imagen-original.jpg -resize 400x400^ -gravity center -extent 400x400 jugadores/imagen-final.jpg
```
