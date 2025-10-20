# Guía de Temporizadores - Supervivencia Nocturna

## 🕐 Tipos de Temporizadores Disponibles

### 1. **Temporizador Simple (Countdown)**
Para eventos que ocurren una sola vez después de un tiempo específico.

### 2. **Temporizador Recurrente (Interval)**
Para eventos que se repiten cada cierto tiempo.

### 3. **Temporizador de Duración**
Para efectos que duran un tiempo limitado.

### 4. **Temporizador de Cooldown**
Para habilidades que tienen tiempo de recarga.

## 📝 Implementación de Temporizadores

### **Temporizador Simple (Countdown)**

```python
class SimpleTimer:
    def __init__(self, duration_frames: int):
        self.duration = duration_frames
        self.current_time = duration_frames
        self.is_active = False
        
    def start(self):
        """Iniciar el temporizador"""
        self.current_time = self.duration
        self.is_active = True
        
    def update(self):
        """Actualizar el temporizador"""
        if self.is_active and self.current_time > 0:
            self.current_time -= 1
            if self.current_time <= 0:
                self.is_active = False
                return True  # Temporizador terminado
        return False
        
    def is_finished(self) -> bool:
        """Verificar si el temporizador terminó"""
        return self.current_time <= 0 and self.is_active
        
    def get_progress(self) -> float:
        """Obtener progreso del temporizador (0.0 a 1.0)"""
        if self.duration == 0:
            return 1.0
        return 1.0 - (self.current_time / self.duration)
        
    def reset(self):
        """Reiniciar el temporizador"""
        self.current_time = self.duration
        self.is_active = False
```

### **Temporizador Recurrente (Interval)**

```python
class IntervalTimer:
    def __init__(self, interval_frames: int):
        self.interval = interval_frames
        self.current_time = 0
        self.is_active = False
        
    def start(self):
        """Iniciar el temporizador"""
        self.current_time = 0
        self.is_active = True
        
    def update(self):
        """Actualizar el temporizador"""
        if self.is_active:
            self.current_time += 1
            if self.current_time >= self.interval:
                self.current_time = 0
                return True  # Intervalo completado
        return False
        
    def stop(self):
        """Detener el temporizador"""
        self.is_active = False
        
    def get_progress(self) -> float:
        """Obtener progreso del intervalo (0.0 a 1.0)"""
        if self.interval == 0:
            return 1.0
        return self.current_time / self.interval
```

### **Temporizador de Duración**

```python
class DurationTimer:
    def __init__(self, duration_frames: int):
        self.duration = duration_frames
        self.remaining_time = 0
        self.is_active = False
        
    def activate(self):
        """Activar el efecto por la duración especificada"""
        self.remaining_time = self.duration
        self.is_active = True
        
    def update(self):
        """Actualizar el temporizador"""
        if self.is_active and self.remaining_time > 0:
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                self.is_active = False
                return True  # Efecto terminado
        return False
        
    def is_active(self) -> bool:
        """Verificar si el efecto está activo"""
        return self.is_active and self.remaining_time > 0
        
    def get_remaining_time(self) -> int:
        """Obtener tiempo restante en frames"""
        return max(0, self.remaining_time)
        
    def get_progress(self) -> float:
        """Obtener progreso del efecto (0.0 a 1.0)"""
        if self.duration == 0:
            return 1.0
        return 1.0 - (self.remaining_time / self.duration)
```

### **Temporizador de Cooldown**

```python
class CooldownTimer:
    def __init__(self, cooldown_frames: int):
        self.cooldown = cooldown_frames
        self.current_cooldown = 0
        self.is_on_cooldown = False
        
    def trigger(self):
        """Activar el cooldown"""
        if not self.is_on_cooldown:
            self.current_cooldown = self.cooldown
            self.is_on_cooldown = True
            return True  # Acción ejecutada
        return False  # En cooldown
        
    def update(self):
        """Actualizar el cooldown"""
        if self.is_on_cooldown and self.current_cooldown > 0:
            self.current_cooldown -= 1
            if self.current_cooldown <= 0:
                self.is_on_cooldown = False
                
    def can_use(self) -> bool:
        """Verificar si se puede usar la habilidad"""
        return not self.is_on_cooldown
        
    def get_cooldown_progress(self) -> float:
        """Obtener progreso del cooldown (0.0 a 1.0)"""
        if self.cooldown == 0:
            return 1.0
        return 1.0 - (self.current_cooldown / self.cooldown)
```


## 🎨 Visualización de Temporizadores

### **Barra de Progreso**

```python
def draw_timer_bar(self, screen: pygame.Surface, x: int, y: int, width: int, height: int, timer, color: tuple):
    """Dibujar barra de progreso para un temporizador"""
    # Fondo de la barra
    pygame.draw.rect(screen, (64, 64, 64), (x, y, width, height))
    
    # Barra de progreso
    progress = timer.get_progress()
    bar_width = int(width * progress)
    pygame.draw.rect(screen, color, (x, y, bar_width, height))
    
    # Borde
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)
```

### **Texto de Cooldown**

```python
def draw_cooldown_text(self, screen: pygame.Surface, x: int, y: int, timer: CooldownTimer):
    """Dibujar texto de cooldown"""
    if timer.is_on_cooldown:
        seconds = timer.current_cooldown // 60
        text = self.font.render(f"Cooldown: {seconds}s", True, RED)
        screen.blit(text, (x, y))
```

## 🔧 Integración en el Juego Principal

### **En la clase Game:**

```python
class Game:
    def __init__(self):
        # ... código existente ...
        
        # Temporizadores del juego
        self.weather_timer = IntervalTimer(3600)  # Cambio de clima cada minuto
        self.enemy_spawn_timer = IntervalTimer(300)  # Spawn de enemigos cada 5 segundos
        self.resource_respawn_timer = IntervalTimer(1800)  # Respawn de recursos cada 30 segundos
        
    def update(self):
        """Actualizar lógica del juego"""
        # ... código existente ...
        
        # Actualizar temporizadores
        self.weather_timer.update()
        self.enemy_spawn_timer.update()
        self.resource_respawn_timer.update()
        
        # Efectos de los temporizadores
        if self.weather_timer.update():
            self.change_weather()
            
        if self.enemy_spawn_timer.update() and self.time_of_day == TimeOfDay.NIGHT:
            self.spawn_enemies()
            
        if self.resource_respawn_timer.update():
            self.respawn_resources()
```

## 📊 Conversión de Tiempo

### **Frames a Segundos:**
- **60 FPS**: 1 segundo = 60 frames
- **30 FPS**: 1 segundo = 30 frames

### **Ejemplos de Duración:**
- **1 segundo**: 60 frames
- **5 segundos**: 300 frames
- **30 segundos**: 1800 frames
- **1 minuto**: 3600 frames

## 🎯 Casos de Uso Comunes

1. **Invencibilidad después de recibir daño**
2. **Cooldown de habilidades especiales**
3. **Regeneración automática de recursos**
4. **Efectos temporales (velocidad, fuerza, etc.)**
5. **Spawn de enemigos en intervalos**
6. **Cambios de clima o ambiente**
7. **Duración de pociones o efectos**
8. **Temporizador de partida**

## 💡 Consejos de Implementación

1. **Usa frames en lugar de segundos** para mayor precisión
2. **Actualiza todos los temporizadores** en el método `update()`
3. **Verifica el estado** antes de usar las habilidades
4. **Proporciona feedback visual** para los temporizadores importantes
5. **Considera pausar temporizadores** cuando el juego está pausado
6. **Usa nombres descriptivos** para los temporizadores
7. **Documenta la duración** en comentarios

## 🚀 Próximos Pasos

1. **Elige el tipo de temporizador** que necesitas
2. **Copia la clase correspondiente** a tu código
3. **Integra el temporizador** en la clase apropiada
4. **Actualiza el temporizador** en el método `update()`
5. **Agrega visualización** si es necesario
6. **Prueba la funcionalidad** en el juego

¡Con estos temporizadores puedes agregar muchas mecánicas interesantes a tu juego!
