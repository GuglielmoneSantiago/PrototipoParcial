# Supervivencia Nocturna

Un videojuego de supervivencia basado en la documentación Game Treatment Mata-Guglielmone.

## Descripción

Un juego de supervivencia donde el jugador debe resistir las noches contra criaturas hostiles, construyendo refugios y gestionando recursos. El objetivo es sobrevivir el mayor número de noches posible.

## Características Implementadas

- **Personaje principal** con sistema de vida, hambre, sed y resistencia
- **Ciclo día/noche** con mecánicas diferentes para cada momento
- **Sistema de enemigos** que aparecen durante la noche
- **Sistema de iluminación** para repeler enemigos
- **Sistema de inventario y crafteo** completo
- **Sistema de construcción de refugio** con múltiples tipos
- **Recolección de recursos** del entorno
- **Protección del refugio** contra enemigos
- **Interfaz minimalista** con barras de estado
- **Controles intuitivos** (WASD, correr, interactuar)

## Instalación

1. Asegúrate de tener Python 3.7+ instalado
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Controles

- **WASD** - Movimiento
- **SHIFT** - Correr (consume resistencia)
- **E** - Colocar antorcha (máximo 3)
- **ESPACIO** - Recolectar recursos
- **I** - Inventario
- **C** - Crafteo
- **B** - Construcción
- **M** - Modo construcción
- **ESC** - Pausa/Reanudar
- **R** - Reiniciar (en pantalla de game over)

## Mecánicas del Juego

### Supervivencia
- **Vida**: Se reduce por daño de enemigos
- **Hambre**: Se reduce gradualmente, afecta la salud si llega a 0
- **Sed**: Se reduce más rápido que el hambre
- **Resistencia**: Se consume al correr, se regenera al caminar

### Ciclo Día/Noche
- **Día**: Tiempo seguro para explorar y recolectar
- **Noche**: Aparecen enemigos hostiles
- **Amanecer**: Los enemigos desaparecen

### Enemigos
- Aparecen solo durante la noche
- Son sensibles a la luz (se alejan de las antorchas)
- Persiguen al jugador en la oscuridad

### Iluminación
- Las antorchas repelen a los enemigos
- Máximo 3 antorchas activas
- Las antorchas se consumen con el tiempo

## Objetivo

Sobrevive el mayor número de noches posible. Cada noche es más desafiante que la anterior.

## Estado del Proyecto

✅ **Completado:**
- Sistema básico de jugador
- Ciclo día/noche
- Enemigos nocturnos
- Sistema de iluminación
- Sistema de inventario y crafteo
- Construcción de refugios
- Recolección de recursos
- Protección del refugio
- Interfaz de usuario

🔄 **Pendiente:**
- Música y efectos de sonido

## Tecnologías Utilizadas

- **Python 3.7+**
- **Pygame 2.5.2**
- **NumPy 1.24.3**

## Estructura del Proyecto

```
PrototipoParcial/
├── main.py              # Archivo principal del juego
├── inventory.py         # Sistema de inventario y crafteo
├── building.py          # Sistema de construcción
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Documentación
├── INSTRUCCIONES.md    # Guía de juego
└── Game Treatment Mata-Guglielmone.pdf  # Documentación original
```

## Contribuciones

Este es un prototipo basado en la documentación proporcionada. Las mejoras y nuevas características son bienvenidas.

## Licencia

Proyecto educativo desarrollado como prototipo de videojuego.
