# Sistema de Lagunas - Documentación

## Descripción General

El sistema de lagunas permite al jugador beber agua para restaurar su sed, añadiendo una mecánica de supervivencia importante al juego. Las lagunas aparecen aleatoriamente en el mapa y proporcionan una fuente renovable de agua.

## Características Principales

### 🌊 Clase Lagoon

La clase `Lagoon` representa una laguna individual con las siguientes propiedades:

- **Posición**: Coordenadas (x, y) en el mapa
- **Tamaño**: Radio variable entre 50-80 píxeles
- **Nivel de agua**: Valor de 0-100 que determina cuánta agua contiene
- **Estado activo**: Indica si la laguna está disponible para beber

### 💧 Sistema de Agua

#### Regeneración Natural
- Las lagunas se regeneran lentamente (0.1 puntos por frame)
- El nivel máximo de agua es 100
- Las lagunas nunca se agotan completamente

#### Consumo de Agua
- Al beber, se consume entre 10-30 puntos de agua
- Se mantiene un mínimo de 10 puntos para evitar que se seque completamente
- Si el nivel baja demasiado, la laguna se desactiva temporalmente

### 🎮 Interacción del Jugador

#### Tecla F - Sistema de Prioridad
La tecla F funciona con un sistema de prioridad inteligente:

1. **Primera prioridad**: Si hay una laguna cerca → Beber agua
2. **Segunda prioridad**: Si no hay lagunas cerca → Farmear árboles

#### Detección de Proximidad
- Radio de interacción: 50 píxeles desde el centro de la laguna
- Solo se puede interactuar con una laguna a la vez
- El sistema detecta automáticamente la laguna más cercana

#### Restauración de Sed
- Restaura entre 10-30 puntos de sed según el agua disponible
- La sed del jugador no puede exceder 100 puntos
- Se reproduce un sonido de recolección al beber

## Generación de Lagunas

### 🗺️ Distribución en el Mapa

#### Cantidad
- Se generan entre 3-6 lagunas por partida
- La cantidad es aleatoria para variar la experiencia

#### Posicionamiento
- Evita los bordes del mapa (margen de 100 píxeles)
- Separación mínima de 150 píxeles entre lagunas
- Tamaño aleatorio entre 50-80 píxeles de radio

#### Regeneración
- Las lagunas se regeneran al reiniciar el juego
- Cada nueva partida tiene una distribución diferente

## Interfaz Visual

### 🎨 Apariencia de las Lagunas

#### Diseño Base
- Forma circular con gradiente de color
- Color del agua varía según el nivel (más intenso = más agua)
- Borde marrón para simular tierra

#### Efectos Visuales
- **Ondas**: Se muestran cuando hay suficiente agua (>20 puntos)
- **Gradiente**: El color se intensifica con el nivel de agua
- **Transparencia**: Efectos de ondas con alpha variable

#### Indicadores de Estado
- **Barra de agua**: Aparece cuando el nivel está bajo (<50)
- **Color de la barra**: Refleja el nivel actual de agua
- **Posición**: Encima de la laguna

### 💬 Indicadores de Interacción

#### Mensajes Contextuales
- **"Presiona F para beber"**: Cuando hay agua disponible
- **"Laguna seca"**: Cuando no se puede beber
- **Fondo semitransparente**: Para mejor legibilidad

#### Prioridad Visual
- Solo se muestra un indicador a la vez
- Se prioriza la laguna más cercana al jugador

## Integración con el Juego

### 🔄 Actualización del Sistema

#### En el Loop Principal
```python
# Actualizar lagunas
for lagoon in self.lagoons:
    lagoon.update()
```

#### En el Dibujado
```python
# Dibujar lagunas
for lagoon in self.lagoons:
    lagoon.draw(self.screen)
```

### 🎵 Efectos de Sonido
- Se utiliza el sonido "collect" con volumen reducido (0.4)
- Proporciona feedback auditivo al beber

### 📋 Controles Actualizados
El menú principal ahora muestra:
```
F - Beber de laguna / Farmear árboles
```

## Métodos Principales

### Clase Lagoon

#### `__init__(x, y, size)`
Inicializa una nueva laguna en la posición especificada.

#### `update()`
Regenera el agua lentamente si está por debajo del máximo.

#### `can_drink() -> bool`
Verifica si la laguna tiene suficiente agua para beber.

#### `drink() -> int`
Consume agua y devuelve la cantidad restaurada de sed.

#### `is_player_nearby(player_x, player_y, player_width, player_height) -> bool`
Verifica si el jugador está dentro del radio de interacción.

#### `draw(screen)`
Dibuja la laguna con todos sus efectos visuales.

### Clase Game

#### `generate_lagoons()`
Genera lagunas aleatorias en el mapa respetando las restricciones de distancia.

#### `drink_from_lagoon() -> bool`
Maneja la interacción de beber, retorna True si se interactuó con una laguna.

#### `draw_lagoon_interaction_hint()`
Dibuja los indicadores de interacción cuando el jugador está cerca.

## Balance del Juego

### ⚖️ Consideraciones de Diseño

#### Regeneración vs Consumo
- **Regeneración lenta**: Evita que las lagunas sean demasiado poderosas
- **Consumo moderado**: Permite múltiples usos antes de agotarse
- **Mínimo de agua**: Previene que las lagunas se sequen completamente

#### Distribución Estratégica
- **Separación mínima**: Evita clusters de lagunas
- **Cantidad variable**: Añade incertidumbre a cada partida
- **Tamaños diferentes**: Variedad visual y de capacidad

#### Interacción Intuitiva
- **Prioridad clara**: Las lagunas tienen prioridad sobre los árboles
- **Feedback visual**: Indicadores claros de disponibilidad
- **Radio generoso**: Fácil interacción sin precisión exacta

## Posibles Mejoras Futuras

### 🔮 Extensiones Potenciales

#### Calidad del Agua
- Diferentes tipos de agua (limpia, contaminada, etc.)
- Efectos secundarios según la calidad

#### Contaminación
- Las lagunas podrían contaminarse con el tiempo
- Requerir purificación antes de beber

#### Estaciones
- Las lagunas podrían congelarse en invierno
- Niveles de agua que varían con las estaciones

#### Construcción
- Permitir crear pozos o cisternas
- Sistema de almacenamiento de agua

#### Animales
- Criaturas que también beben de las lagunas
- Competencia por los recursos

## Conclusión

El sistema de lagunas añade una capa importante de gestión de recursos al juego, proporcionando una fuente renovable de agua que requiere planificación estratégica. La implementación prioriza la usabilidad y la claridad visual, asegurando que los jugadores entiendan fácilmente cómo interactuar con el sistema.

La mecánica se integra perfectamente con los sistemas existentes, especialmente con el sistema de sed del jugador y la interacción con árboles, creando un ecosistema de supervivencia más completo y envolvente.
