# Sistema de Árboles - Supervivencia Nocturna

## 🌳 **Características del Sistema**

### **Tipos de Árboles**
- **Roble (Oak)**: Verde bosque, tronco marrón
- **Pino (Pine)**: Verde oscuro, tronco marrón oscuro  
- **Abedul (Birch)**: Blanco hueso, tronco blanco
- **Cerezo (Cherry)**: Rosa profundo, tronco marrón claro

### **Mecánicas de Farmeo**
- **Cantidad de madera**: 3-8 unidades por árbol
- **Farmeo por click**: 1-3 madera por vez
- **Desaparición**: Los árboles desaparecen completamente cuando se farmean
- **Regeneración**: Los árboles reaparecen después de 50 segundos
- **Indicador visual**: Barra de madera disponible sobre cada árbol

## 🎮 **Controles**

### **Farmear Árboles**
- **Tecla F**: Farmear árboles cercanos
- **Indicador visual**: "F para farmear" aparece sobre árboles cercanos
- **Distancia**: Debes estar a 50 píxeles del árbol

### **Sistema de Interacción**
- Los árboles aparecen automáticamente en el mapa
- Máximo 15 árboles simultáneos
- Separación mínima de 80 píxeles entre árboles
- Los árboles se regeneran automáticamente

## 🎯 **Estrategias de Farmeo**

### **Eficiencia**
1. **Busca grupos de árboles** para farmear múltiples a la vez
2. **Usa el indicador visual** para saber cuánta madera queda
3. **Planifica tu ruta** para optimizar el farmeo
4. **Construye cerca de árboles** para acceso rápido a madera
5. **Los árboles desaparecen** cuando se farmean completamente
6. **Espera la regeneración** para farmear el mismo lugar

### **Gestión de Recursos**
- La madera es esencial para construcción
- Los árboles se regeneran, así que no te preocupes por agotarlos
- Combina farmeo con recolección de otros recursos

## 🔧 **Implementación Técnica**

### **Archivos del Sistema**
- `trees.py` - Lógica de árboles y farmeo
- `main.py` - Integración con el juego principal

### **Clases Principales**
- `Tree`: Árbol individual con madera y regeneración
- `TreeManager`: Gestión de todos los árboles del mapa

### **Características Técnicas**
- **Colisiones**: Sistema de proximidad para interacción
- **Regeneración**: Timer automático para restaurar árboles
- **Visualización**: Indicadores de estado y interacción
- **Sonidos**: Efectos de sonido al farmear

## 🎨 **Personalización**

### **Modificar Tipos de Árboles**
Edita `trees.py` en la clase `Tree`:

```python
self.tree_colors = {
    "oak": (34, 139, 34),      # Verde bosque
    "pine": (0, 100, 0),       # Verde oscuro
    "birch": (245, 245, 220),  # Blanco hueso
    "cherry": (255, 20, 147)   # Rosa profundo
}
```

### **Cambiar Cantidad de Madera**
Modifica en `trees.py`:

```python
self.wood_amount = random.randint(5, 12)  # Más madera
self.regrowth_time = 2000  # Regeneración más rápida
```

### **Ajustar Distancia de Interacción**
Cambia en `trees.py`:

```python
interaction_distance = 80  # Mayor distancia de interacción
```

## 🎮 **Integración con el Juego**

### **Sistema de Inventario**
- La madera se agrega automáticamente al inventario
- Compatible con el sistema de crafteo existente
- Se puede usar para construir refugios

### **Sistema de Construcción**
- La madera es un recurso esencial para construcción
- Se consume al construir muros, puertas, etc.
- Los árboles proporcionan suministro constante

### **Sistema de Sonidos**
- Efecto de sonido al farmear
- Volumen ajustable
- Integrado con el sistema de assets

## 🚀 **Futuras Mejoras**

### **Posibles Expansiones**
- **Herramientas de farmeo**: Hachas que aumenten la eficiencia
- **Diferentes tipos de madera**: Madera de calidad variable
- **Árboles especiales**: Árboles raros con recursos únicos
- **Sistema de plantación**: Plantar tus propios árboles

### **Mejoras Visuales**
- **Animaciones**: Efectos de corte y regeneración
- **Partículas**: Efectos visuales al farmear
- **Sprites**: Imágenes reales de árboles
- **Estaciones**: Cambios visuales según el tiempo

¡El sistema de árboles está completamente funcional y listo para usar!
