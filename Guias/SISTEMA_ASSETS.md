# Guía Completa de Assets - Supervivencia Nocturna

## 📁 Estructura de Carpetas

```
PrototipoParcial/
├── assets/
│   ├── images/          # Todas las imágenes del juego
│   ├── sounds/          # Todos los sonidos y música
│   └── README.md        # Documentación de assets
├── main.py              # Juego principal
├── assets_manager.py    # Gestor de assets
├── create_temp_assets.py # Script para crear assets temporales
└── ...
```

## 🎨 Cómo Agregar tus Propios Assets

### 1. **Imágenes del Personaje**
Coloca en `assets/images/`:
- `player_idle.png` - Personaje en reposo con brazos a los lados (32x32)
- `player_walk.png` - Personaje caminando con brazos balanceándose (32x32)  
- `player_run.png` - Personaje corriendo con brazos arriba (32x32)

### 2. **Fondos del Juego**
Coloca en `assets/images/`:
- `background_day.png` - Campo verde brillante completo (1200x800)
- `background_night.png` - Campo oscuro completo (1200x800)
- `background_dawn.png` - Campo con tonos rosados completo (1200x800)
- `background_dusk.png` - Campo con tonos naranjas completo (1200x800)

### 3. **Enemigos**
Coloca en `assets/images/`:
- `enemy_shadow.png` - Enemigo sombra gris con ojos rojos (24x24)
- `enemy_creature.png` - Criatura verde monstruosa con ojos blancos (24x24)

### 4. **Construcciones**
Coloca en `assets/images/`:
- `wall.png` - Muro (40x40)
- `door.png` - Puerta (40x40)
- `floor.png` - Piso (40x40)
- `roof.png` - Techo (40x40)
- `fire.png` - Fuego (40x40)

### 5. **Items y Recursos**
Coloca en `assets/images/`:
- `torch.png` - Antorcha (20x20)
- `wood.png` - Madera (16x16)
- `stone.png` - Piedra (16x16)
- `grass.png` - Hierba (16x16)
- `bone.png` - Hueso (16x16)

## 🎵 Cómo Agregar Sonidos y Música

### Efectos de Sonido
Coloca en `assets/sounds/`:
- `footstep.wav` - Pasos del personaje
- `collect.wav` - Recolección de recursos
- `build.wav` - Construcción
- `enemy_hit.wav` - Golpe de enemigo
- `player_hurt.wav` - Personaje herido

### Música de Fondo
Coloca en `assets/sounds/`:
- `ambient_day.ogg` - Música ambiente del día
- `ambient_night.ogg` - Música ambiente de la noche
- `menu.ogg` - Música del menú

## 🛠️ Crear Assets Temporales

Si quieres probar el juego inmediatamente, ejecuta:

```bash
python create_temp_assets.py
```

Esto creará imágenes temporales básicas para que puedas probar todas las funcionalidades.

## 📋 Especificaciones Técnicas

### Imágenes
- **Formato**: PNG (con transparencia)
- **Profundidad**: 32 bits
- **Estilo**: Pixel art recomendado
- **Transparencia**: Usar canal alpha para fondos transparentes

### Sonidos
- **Efectos**: WAV (mejor calidad)
- **Música**: OGG (mejor compresión)
- **Frecuencia**: 44.1 kHz
- **Canales**: Estéreo para música, mono para efectos
- **Duración**: Efectos cortos (1-3 segundos), música larga

## 🎮 Cómo Funciona el Sistema

### Carga Automática
El juego carga automáticamente todos los assets al iniciar. Si falta algún archivo, usará gráficos por defecto.

### Fallback System
- Si no hay imagen del personaje → usa rectángulo verde
- Si no hay fondo → usa colores sólidos
- Si no hay sonido → no reproduce nada (sin errores)

### Optimización
- Las imágenes se cargan una sola vez al inicio
- Los sonidos se cargan bajo demanda
- La música se cambia automáticamente según el tiempo del día

## 🔧 Personalización Avanzada

### Cambiar Tamaños
Edita `assets_manager.py` para cambiar las dimensiones:

```python
self.load_image("player_idle", "player_idle.png", (64, 64))  # Más grande
```

### Agregar Nuevos Assets
1. Agrega el archivo a la carpeta correspondiente
2. Modifica `assets_manager.py` en el método `load_all_assets()`
3. Usa `assets.get_image("nombre")` en el código

### Cambiar Volúmenes
Modifica los volúmenes en `main.py`:

```python
assets.play_sound("footstep", 0.5)  # 50% de volumen
assets.play_music("ambient_day", -1, 0.3)  # 30% de volumen
```

## 🎯 Consejos para Assets

### Personaje
- Estilo pixel art cuadrado y simple
- Paleta de colores: azul brillante, marrón oscuro, piel rosada, blanco
- Animaciones diferenciadas: reposo, caminar, correr
- Brazos expresivos según el movimiento
- Sonrisa característica

### Fondos
- Usa colores atmosféricos naturales
- Campo de hierba con flores rojas como base
- Diferencia clara entre día y noche
- Resolución recomendada 1200x800
- Sin elementos astronómicos (sol/luna)
- Cobertura completa de pantalla (sin cielo)

### Enemigos
- Estilo pixel art cuadrado y robusto
- Paleta de colores: verde/gris con gradientes, negro para contornos
- Ojos diferenciados: blancos (criatura) o rojos (sombra)
- Aspecto musculoso y monstruoso
- Contorno negro grueso para definición
- Diseño consistente entre ambos tipos

### Sonidos
- Efectos cortos y claros
- Música ambiental y relajante
- Volúmenes balanceados

¡El juego está listo para recibir tus assets personalizados!
