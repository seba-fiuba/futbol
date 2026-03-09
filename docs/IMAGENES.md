# 📸 Guía: Cómo Agregar Imágenes a los Jugadores

## 🎯 Resumen Rápido

Las imágenes se guardan en: **`frontend/static/jugadores/`**

En la base de datos guardas la ruta: **`/jugadores/nombre-imagen.jpg`**

---

## 📝 Métodos para Relacionar Imágenes

### Opción 1: Imágenes Locales (Recomendada)

#### Paso 1: Guarda la imagen en el frontend

```bash
# Copia tu imagen a la carpeta static
cp foto-jugador.jpg frontend/static/jugadores/messi.jpg
```

#### Paso 2: Crea el jugador con la ruta

**Usando Python (seed.py o script):**

```python
from models import Jugador
from database import get_session

with get_session() as session:
    jugador = Jugador(
        nombre="Lionel Messi",
        apodo="La Pulga",
        imagen="/jugadores/messi.jpg"  # ← Ruta desde la raíz del frontend
    )
    session.add(jugador)
    session.commit()
```

**Usando la API (POST con curl):**

```bash
curl -X POST "http://localhost:8000/Jugadores/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Lionel Messi",
    "apodo": "La Pulga",
    "imagen_url": "/jugadores/messi.jpg"
  }'
```

**Usando la API docs (http://localhost:8000/docs):**

```json
{
  "nombre": "Lionel Messi",
  "apodo": "La Pulga",
  "imagen_url": "/jugadores/messi.jpg"
}
```

---

### Opción 2: URLs Externas

Simplemente usa una URL completa:

```python
jugador = Jugador(
    nombre="Cristiano Ronaldo",
    apodo="CR7",
    imagen="https://ejemplo.com/cr7.jpg"
)
```

---

## 🖼️ Estructura de Archivos

```
futbol/
├── frontend/
│   └── static/
│       └── jugadores/           ← Aquí van las imágenes
│           ├── messi.jpg
│           ├── ronaldo.jpg
│           └── neymar.png
│
└── seed.py                      ← Script para cargar datos
```

---

## 💻 Ejemplo Completo: Script para Cargar Jugadores con Imágenes

Crea un archivo `cargar_jugadores.py`:

```python
from sqlmodel import Session, select
from database import get_session
from models import Jugador

# Lista de jugadores con sus imágenes
jugadores_data = [
    {
        "nombre": "Lionel Messi",
        "apodo": "La Pulga",
        "imagen": "/jugadores/messi.jpg"
    },
    {
        "nombre": "Cristiano Ronaldo",
        "apodo": "CR7", 
        "imagen": "/jugadores/ronaldo.jpg"
    },
    {
        "nombre": "Neymar Jr",
        "apodo": "Ney",
        "imagen": "/jugadores/neymar.jpg"
    },
]

with get_session() as session:
    for data in jugadores_data:
        # Verifica si ya existe
        statement = select(Jugador).where(Jugador.nombre == data["nombre"])
        jugador_existe = session.exec(statement).first()
        
        if not jugador_existe:
            jugador = Jugador(**data)
            session.add(jugador)
            print(f"✓ Agregado: {data['nombre']}")
        else:
            print(f"○ Ya existe: {data['nombre']}")
    
    session.commit()
    print("\n✅ Jugadores cargados correctamente")
```

**Ejecutar:**

```bash
source .venv/bin/activate
python cargar_jugadores.py
```

---

## 🔄 Actualizar Imagen de un Jugador Existente

```python
from sqlmodel import select
from database import get_session
from models import Jugador

with get_session() as session:
    # Buscar el jugador
    statement = select(Jugador).where(Jugador.nombre == "Lionel Messi")
    jugador = session.exec(statement).first()
    
    if jugador:
        jugador.imagen = "/jugadores/messi-nueva.jpg"
        session.add(jugador)
        session.commit()
        print(f"✓ Imagen actualizada para {jugador.nombre}")
```

---

## 🗄️ Actualizar Directamente en PostgreSQL

```sql
-- Conectar a la base de datos
psql -U postgres -d futbol_db

-- Actualizar imagen de un jugador
UPDATE jugadores 
SET imagen = '/jugadores/messi.jpg' 
WHERE nombre = 'Lionel Messi';

-- Ver todos los jugadores y sus imágenes
SELECT id, nombre, apodo, imagen FROM jugadores;
```

---

## 🎨 Consejos de Optimización

### 1. Redimensionar Imágenes

Las imágenes grandes hacen lenta la aplicación. Redimensiónalas:

```bash
# Con ImageMagick
sudo dnf install ImageMagick
convert original.jpg -resize 400x400^ -gravity center -extent 400x400 jugadores/optimizada.jpg

# Con Python (Pillow)
pip install Pillow

python << EOF
from PIL import Image

img = Image.open('original.jpg')
img = img.resize((400, 400), Image.Resampling.LANCZOS)
img.save('frontend/static/jugadores/optimizada.jpg', quality=85, optimize=True)
EOF
```

### 2. Nombres de Archivo

- ✅ Bien: `lionel-messi.jpg`, `cr7.jpg`, `jugador-10.jpg`
- ❌ Mal: `Lionel Messi.jpg`, `cr7 (1).jpg`, `foto final.JPG`

### 3. Formato y Peso

- **Formato:** JPG para fotos, PNG para logos con transparencia
- **Peso máximo:** 500KB por imagen
- **Dimensiones:** 400x400px (cuadrado) o 300x400px (retrato)

---

## 🚀 Forma Rápida: Descargar Imágenes de Internet

```bash
# Ir a la carpeta de imágenes
cd frontend/static/jugadores

# Descargar con wget
wget -O messi.jpg "https://url-de-la-imagen.com/messi.jpg"

# O con curl
curl -o ronaldo.jpg "https://url-de-la-imagen.com/ronaldo.jpg"
```

Luego actualiza la base de datos con `/jugadores/messi.jpg`

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo usar imágenes de URLs externas?**  
R: Sí, solo pon la URL completa en el campo imagen: `https://ejemplo.com/foto.jpg`

**P: ¿Las imágenes se guardan en la base de datos?**  
R: No, solo se guarda la ruta o URL. Las imágenes están en `frontend/static/jugadores/`

**P: ¿Qué pasa si no pongo imagen?**  
R: El frontend mostrará un emoji de usuario por defecto 👤

**P: ¿Puedo cambiar la carpeta de las imágenes?**  
R: Sí, pero debes actualizar todas las rutas en la base de datos
