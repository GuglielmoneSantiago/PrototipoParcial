# Sistema de Pausa Automática - Supervivencia Nocturna

## 🎮 **Características del Sistema**

### **Pausa Automática**
El juego se pausa automáticamente cuando se abren las siguientes interfaces:
- **Inventario** (Tecla I)
- **Crafteo** (Tecla C)  
- **Construcción** (Tecla B)
- **Modo Construcción** (Tecla M)

### **Estados del Juego**
- `PLAYING` - Juego normal en progreso
- `INVENTORY` - Inventario abierto (juego pausado)
- `CRAFTING` - Crafteo abierto (juego pausado)
- `BUILDING` - Construcción abierta (juego pausado)
- `MENU` - Menú principal
- `GAME_OVER` - Pantalla de fin de juego

## 🎯 **Funcionalidades**

### **Pausa Inteligente**
- **Tiempo detenido**: El ciclo día/noche se pausa
- **Enemigos pausados**: Los enemigos no se mueven ni atacan
- **Recursos pausados**: No se consumen hambre, sed o resistencia
- **Árboles pausados**: Los árboles no se regeneran

### **Indicador Visual**
- **"JUEGO PAUSADO"** aparece en pantalla cuando está pausado
- **Color amarillo** para destacar el estado
- **Posición central** para máxima visibilidad

### **Controles Simplificados**
- **Tecla I**: Abrir/cerrar inventario (pausa automática)
- **Tecla C**: Abrir/cerrar crafteo (pausa automática)
- **Tecla B**: Abrir/cerrar construcción (pausa automática)
- **Tecla M**: Activar/desactivar modo construcción (pausa automática)
- **Tecla ESC**: Cerrar cualquier interfaz desde dentro (desactiva pausa automáticamente)

## 🔧 **Implementación Técnica**

### **Sistema de Estados**
```python
class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    INVENTORY = "inventory"
    CRAFTING = "crafting"
    BUILDING = "building"
```

### **Lógica de Pausa**
- **Update**: Solo se ejecuta cuando `state == PLAYING`
- **Draw**: Se adapta según el estado actual
- **Input**: Manejo específico para cada interfaz

### **Interfaces Inteligentes**
- **Una a la vez**: Solo una interfaz puede estar abierta
- **Estado específico**: Cada interfaz tiene su propio estado
- **Transiciones suaves**: Cambio automático entre estados

## 🎮 **Experiencia de Usuario**

### **Ventajas**
1. **Planificación sin presión**: Puedes pensar tranquilamente
2. **Gestión segura**: No pierdes recursos mientras organizas
3. **Construcción precisa**: Puedes construir sin prisa
4. **Crafteo relajado**: Experimenta con recetas sin presión

### **Flujo de Juego**
1. **Explora y recolecta** en modo normal
2. **Abre inventario** para organizar recursos
3. **Juego se pausa** automáticamente
4. **Organiza tranquilamente** sin perder tiempo
5. **Presiona ESC** o **cierra inventario** para reanudar automáticamente

## 🎯 **Casos de Uso**

### **Gestión de Recursos**
- Abre inventario para organizar items
- Juego pausado = no consumes hambre/sed
- Tiempo para planificar qué craftear

### **Construcción Segura**
- Abre construcción para planificar
- Juego pausado = enemigos no atacan
- Construye sin presión de tiempo

### **Crafteo Experimental**
- Abre crafteo para probar recetas
- Juego pausado = recursos seguros
- Experimenta sin consecuencias

## 🚀 **Beneficios del Sistema**

### **Para el Jugador**
- **Menos estrés**: No hay presión de tiempo
- **Mejor planificación**: Puedes pensar estratégicamente
- **Gestión eficiente**: Organiza recursos sin prisa
- **Construcción precisa**: Coloca estructuras cuidadosamente

### **Para el Juego**
- **Mejor balance**: Evita pérdida accidental de recursos
- **Experiencia fluida**: Transiciones suaves entre modos
- **Interfaz clara**: Estados bien definidos
- **Control total**: El jugador decide cuándo pausar

## 🎮 **Controles Actualizados**

### **Navegación**
- **I** - Inventario (pausa automática)
- **C** - Crafteo (pausa automática)
- **B** - Construcción (pausa automática)
- **M** - Modo construcción (pausa automática)
- **ESC** - Cerrar interfaz actual (desactiva pausa automáticamente)

### **Indicadores Visuales**
- **"JUEGO PAUSADO"** - Cuando está en interfaces
- **Interfaces específicas** - Solo la activa se muestra
- **HUD completo** - Información siempre visible

¡El sistema de pausa automática hace el juego mucho más manejable y estratégico!
