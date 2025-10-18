# Assets del Videojuego - Supervivencia Nocturna

## Estructura de Carpetas

```
assets/
├── images/          # Todas las imágenes del juego
└── sounds/          # Todos los sonidos y música
```

## Imágenes Requeridas (assets/images/)

### Personaje
- `player_idle.png` - Personaje en reposo (32x32)
- `player_walk.png` - Personaje caminando (32x32)
- `player_run.png` - Personaje corriendo (32x32)

### Fondos
- `background_day.png` - Fondo del día
- `background_night.png` - Fondo de la noche
- `background_dawn.png` - Fondo del amanecer
- `background_dusk.png` - Fondo del atardecer

### Enemigos
- `enemy_shadow.png` - Enemigo sombra (24x24)
- `enemy_creature.png` - Criatura hostil (24x24)

### Construcciones
- `wall.png` - Muro (40x40)
- `door.png` - Puerta (40x40)
- `floor.png` - Piso (40x40)
- `roof.png` - Techo (40x40)
- `fire.png` - Fuego (40x40)

### Items
- `torch.png` - Antorcha (20x20)
- `wood.png` - Madera (16x16)
- `stone.png` - Piedra (16x16)
- `grass.png` - Hierba (16x16)
- `bone.png` - Hueso (16x16)

## Sonidos Requeridos (assets/sounds/)

### Efectos de Sonido
- `footstep.wav` - Pasos del personaje
- `collect.wav` - Recolección de recursos
- `build.wav` - Construcción
- `enemy_hit.wav` - Golpe de enemigo
- `player_hurt.wav` - Personaje herido

### Música
- `ambient_day.ogg` - Música ambiente del día
- `ambient_night.ogg` - Música ambiente de la noche
- `menu.ogg` - Música del menú

## Formatos Recomendados

### Imágenes
- **Formato**: PNG (con transparencia)
- **Profundidad**: 32 bits
- **Estilo**: Pixel art o estilo consistente

### Sonidos
- **Efectos**: WAV (mejor calidad)
- **Música**: OGG (mejor compresión)
- **Frecuencia**: 44.1 kHz
- **Canales**: Estéreo para música, mono para efectos

## Cómo Agregar Assets

1. **Coloca los archivos** en las carpetas correspondientes
2. **Mantén los nombres** exactos como se especifica arriba
3. **Ajusta las dimensiones** según las especificaciones
4. **Ejecuta el juego** - los assets se cargarán automáticamente

## Notas

- Si falta algún archivo, el juego funcionará con gráficos por defecto
- Los archivos deben estar en la carpeta correcta para ser detectados
- El juego mostrará mensajes de advertencia si no encuentra algún asset
- Puedes usar imágenes temporales mientras desarrollas el arte final
