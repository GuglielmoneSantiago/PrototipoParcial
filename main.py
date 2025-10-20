#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pygame
import sys
import random
import math
from enum import Enum
from typing import Tuple, List, Optional
from inventory import Inventory, CraftingSystem, InventoryUI, CraftingUI, ItemType
from building import BuildingSystem, BuildingUI, BuildingType
from assets_manager import assets
from trees import TreeManager

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    INVENTORY = "inventory"
    CRAFTING = "crafting"
    BUILDING = "building"
    CONTROLS = "controls"

class TimeOfDay(Enum):
    DAY = "day"
    NIGHT = "night"
    DAWN = "dawn"
    DUSK = "dusk"

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 3
        self.running_speed = 5
        self.is_running = False
        
        # Atributos de supervivencia
        self.health = 100
        self.max_health = 100
        self.hunger = 100
        self.thirst = 100
        self.stamina = 100
        self.max_stamina = 100
        
        # Inventario
        self.inventory = Inventory(max_size=20)
        self.crafting_system = CraftingSystem()
        self.inventory_ui = InventoryUI(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.crafting_ui = CraftingUI(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Sistema de equipamiento
        self.equipped_weapon = None  # Arma equipada (SPEAR, BOW, etc.)
        self.equipped_tool = None    # Herramienta equipada (AXE, PICKAXE, KNIFE)
        self.weapon_damage = 0       # Daño adicional del arma equipada
        
        # Sistema de ataque automático
        self.auto_attack_cooldown = 0  # Cooldown para evitar spam de ataques
        self.auto_attack_delay = 30    # Frames de espera entre ataques automáticos (0.5 segundos a 60 FPS)
        
        # Dirección de movimiento
        self.direction = 0  # 0: derecha, 1: abajo, 2: izquierda, 3: arriba
        
    def move(self, dx: int, dy: int):
        """Mover al jugador"""
        if self.is_running and self.stamina > 0:
            speed = self.running_speed
            self.stamina -= 0.5
        else:
            speed = self.speed
            
        self.x += dx * speed
        self.y += dy * speed
        
        # Mantener dentro de los límites de la pantalla
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        
        # Regenerar stamina si no está corriendo
        if not self.is_running and self.stamina < self.max_stamina:
            self.stamina += 0.2
            
    def equip_weapon(self, weapon_type: ItemType) -> bool:
        """Equipar un arma"""
        if self.inventory.has_item(weapon_type, 1):
            # Desequipar arma actual si hay una
            if self.equipped_weapon:
                self.unequip_weapon()
            
            # Equipar nueva arma
            self.equipped_weapon = weapon_type
            self.update_weapon_stats()
            print(f"Equipaste {weapon_type.value}")
            return True
        return False
        
    def equip_tool(self, tool_type: ItemType) -> bool:
        """Equipar una herramienta"""
        if self.inventory.has_item(tool_type, 1):
            # Desequipar herramienta actual si hay una
            if self.equipped_tool:
                self.unequip_tool()
            
            # Equipar nueva herramienta
            self.equipped_tool = tool_type
            print(f"Equipaste {tool_type.value}")
            return True
        return False
        
    def unequip_weapon(self):
        """Desequipar arma actual"""
        if self.equipped_weapon:
            print(f"Desequipaste {self.equipped_weapon.value}")
            self.equipped_weapon = None
            self.weapon_damage = 0
            
    def unequip_tool(self):
        """Desequipar herramienta actual"""
        if self.equipped_tool:
            print(f"Desequipaste {self.equipped_tool.value}")
            self.equipped_tool = None
            
    def update_weapon_stats(self):
        """Actualizar estadísticas del arma equipada"""
        if self.equipped_weapon:
            # Definir daño de cada arma
            weapon_damage_map = {
                ItemType.SPEAR: 25,
                ItemType.BOW: 20,
                ItemType.AXE: 15,
                ItemType.PICKAXE: 10,
                ItemType.KNIFE: 8
            }
            self.weapon_damage = weapon_damage_map.get(self.equipped_weapon, 0)
        else:
            self.weapon_damage = 0
            
    def get_total_damage(self) -> int:
        """Obtener daño total (base + arma)"""
        base_damage = 10  # Daño base del jugador
        return base_damage + self.weapon_damage
            
    def update(self):
        """Actualizar estado del jugador"""
        # Reducir hambre y sed gradualmente
        self.hunger = max(0, self.hunger - 0.01)
        self.thirst = max(0, self.thirst - 0.015)
        
        # Si hambre o sed llegan a 0, reducir salud
        if self.hunger <= 0 or self.thirst <= 0:
            self.health = max(0, self.health - 0.5)
            
        # Actualizar cooldown de ataque automático
        if self.auto_attack_cooldown > 0:
            self.auto_attack_cooldown -= 1
            
    def draw(self, screen: pygame.Surface):
        """Dibujar al jugador"""
        # Intentar usar imagen del personaje
        player_image = None
        if self.is_running:
            player_image = assets.get_image("player_run")
        else:
            player_image = assets.get_image("player_walk") or assets.get_image("player_idle")
            
        if player_image:
            # Rotar imagen según la dirección
            if self.direction == 2:  # Izquierda
                player_image = pygame.transform.flip(player_image, True, False)
            elif self.direction == 1:  # Abajo
                player_image = pygame.transform.rotate(player_image, 90)
            elif self.direction == 3:  # Arriba
                player_image = pygame.transform.rotate(player_image, -90)
                
            screen.blit(player_image, (self.x, self.y))
        else:
            # Fallback a gráficos por defecto
            color = GREEN if self.health > 50 else RED
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
            
            # Dibujar dirección
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            
            if self.direction == 0:  # Derecha
                pygame.draw.polygon(screen, WHITE, [
                    (center_x + 10, center_y),
                    (center_x + 5, center_y - 5),
                    (center_x + 5, center_y + 5)
                ])
            elif self.direction == 1:  # Abajo
                pygame.draw.polygon(screen, WHITE, [
                    (center_x, center_y + 10),
                    (center_x - 5, center_y + 5),
                    (center_x + 5, center_y + 5)
                ])
            elif self.direction == 2:  # Izquierda
                pygame.draw.polygon(screen, WHITE, [
                    (center_x - 10, center_y),
                    (center_x - 5, center_y - 5),
                    (center_x - 5, center_y + 5)
                ])
            elif self.direction == 3:  # Arriba
                pygame.draw.polygon(screen, WHITE, [
                    (center_x, center_y - 10),
                    (center_x - 5, center_y - 5),
                    (center_x + 5, center_y - 5)
                ])

class Enemy:
    def __init__(self, x: int, y: int, enemy_type: str = "shadow"):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.speed = 1.5
        self.health = 50
        self.max_health = 50
        self.damage = 20
        self.enemy_type = enemy_type
        self.is_active = True
        self.light_sensitivity = 0.8  # Sensibilidad a la luz (0-1)
        
    def update(self, player: Player, light_sources: List):
        """Actualizar enemigo"""
        if not self.is_active:
            return
            
        # Calcular distancia al jugador
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Verificar si hay luz cerca
        light_nearby = False
        for light in light_sources:
            light_distance = math.sqrt((light.x - self.x)**2 + (light.y - self.y)**2)
            if light_distance < light.radius:
                light_nearby = True
                break
                
        # Si hay luz cerca, el enemigo se aleja
        if light_nearby:
            # Moverse alejándose de la luz
            if dx != 0:
                self.x -= (dx / distance) * self.speed * 0.5
            if dy != 0:
                self.y -= (dy / distance) * self.speed * 0.5
        else:
            # Perseguir al jugador
            if distance > 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
                
        # Mantener dentro de los límites
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        
    def draw(self, screen: pygame.Surface):
        """Dibujar enemigo"""
        if not self.is_active:
            return
            
        # Usar imágenes del AssetsManager
        if self.enemy_type == "shadow":
            enemy_image = assets.get_image("enemy_shadow")
        else:  # creature
            enemy_image = assets.get_image("enemy_creature")
            
        if enemy_image:
            screen.blit(enemy_image, (self.x, self.y))
        else:
            # Fallback a gráficos por defecto
            color = DARK_GRAY if self.enemy_type == "shadow" else RED
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

class LightSource:
    def __init__(self, x: int, y: int, radius: int = 100, duration: int = 300):
        self.x = x
        self.y = y
        self.radius = radius
        self.duration = duration
        self.max_duration = duration
        self.is_active = True
        
    def update(self):
        """Actualizar fuente de luz"""
        if self.duration > 0:
            self.duration -= 1
        else:
            self.is_active = False
            
    def draw(self, screen: pygame.Surface):
        """Dibujar fuente de luz"""
        if not self.is_active:
            return
            
        # Crear superficie para el efecto de luz
        light_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        # Dibujar gradiente de luz
        for i in range(self.radius):
            alpha = int(50 * (1 - i / self.radius))
            color = (*YELLOW[:3], alpha)
            pygame.draw.circle(light_surface, color, (self.radius, self.radius), self.radius - i)
            
        screen.blit(light_surface, (self.x - self.radius, self.y - self.radius))

class Lagoon:
    def __init__(self, x: int, y: int, size: int = 60):
        self.x = x
        self.y = y
        self.size = size
        self.width = size
        self.height = size
        self.water_level = 100  # Nivel de agua (0-100)
        self.max_water_level = 100
        self.is_active = True
        
        # Temporizador para reactivar la laguna cuando se seca
        self.reactivation_timer = 0
        self.reactivation_duration = 3600  # 60 segundos a 60 FPS
        self.is_drying = False
        
    def update(self):
        """Actualizar laguna"""
        # Si la laguna está secándose, manejar el temporizador de reactivación
        if self.is_drying:
            self.reactivation_timer += 1
            if self.reactivation_timer >= self.reactivation_duration:
                # Reactivar la laguna
                self.is_active = True
                self.is_drying = False
                self.reactivation_timer = 0
                self.water_level = 20  # Empezar con un nivel bajo
                print("Una laguna se ha reactivado!")
        else:
            # Regenerar agua lentamente solo si está activa
            if self.is_active and self.water_level < self.max_water_level:
                self.water_level = min(self.max_water_level, self.water_level + 0.1)
            
    def can_drink(self) -> bool:
        """Verificar si se puede beber de la laguna"""
        return self.is_active and self.water_level > 20
        
    def drink(self) -> int:
        """Beber de la laguna y devolver cuánta sed se recupera"""
        if not self.can_drink():
            return 0
            
        # Reducir nivel de agua
        water_consumed = min(30, self.water_level - 10)  # Beber hasta 30, pero dejar mínimo 10
        self.water_level -= water_consumed
        
        # Si el nivel es muy bajo, la laguna se seca temporalmente
        if self.water_level <= 10:
            self.is_active = False
            self.is_drying = True
            self.reactivation_timer = 0
            print("Una laguna se ha secado! Se reactivará en 60 segundos.")
            
        return int(water_consumed)
        
    def is_player_nearby(self, player_x: int, player_y: int, player_width: int, player_height: int) -> bool:
        """Verificar si el jugador está cerca de la laguna"""
        # Calcular distancia entre centros
        lagoon_center_x = self.x + self.width // 2
        lagoon_center_y = self.y + self.height // 2
        player_center_x = player_x + player_width // 2
        player_center_y = player_y + player_height // 2
        
        distance = math.sqrt((lagoon_center_x - player_center_x)**2 + (lagoon_center_y - player_center_y)**2)
        return distance < 50  # Radio de interacción
        
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Dibujar laguna"""
        if not self.is_active and not self.is_drying:
            return
            
        # Crear superficie para la laguna
        lagoon_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Dibujar agua con gradiente según el nivel
        if self.is_drying:
            # Laguna secándose - mostrar como tierra seca
            water_color = (139, 69, 19)  # Marrón tierra
            pygame.draw.circle(lagoon_surface, water_color, (self.width // 2, self.height // 2), self.size // 2)
            pygame.draw.circle(lagoon_surface, (101, 67, 33), (self.width // 2, self.height // 2), self.size // 2, 3)
        else:
            # Laguna activa con agua
            water_color_intensity = int(255 * (self.water_level / self.max_water_level))
            water_color = (0, 100 + water_color_intensity // 2, 150 + water_color_intensity // 3)
            
            # Dibujar círculo de agua
            pygame.draw.circle(lagoon_surface, water_color, (self.width // 2, self.height // 2), self.size // 2)
            
            # Dibujar borde
            pygame.draw.circle(lagoon_surface, (139, 69, 19), (self.width // 2, self.height // 2), self.size // 2, 3)
            
            # Dibujar efecto de ondas si hay agua
            if self.water_level > 20:
                for i in range(3):
                    wave_radius = (self.size // 2) - 5 - (i * 3)
                    if wave_radius > 0:
                        alpha = int(50 * (1 - i / 3))
                        wave_color = (*water_color[:3], alpha)
                        pygame.draw.circle(lagoon_surface, wave_color, (self.width // 2, self.height // 2), wave_radius, 2)
        
        screen.blit(lagoon_surface, (self.x, self.y))
        
        # Dibujar indicador de nivel de agua si está baja
        if self.water_level < 100:
            # Dibujar barra de agua encima de la laguna
            bar_width = 40
            bar_height = 6
            bar_x = self.x + (self.width - bar_width) // 2
            bar_y = self.y - 15
            
            # Fondo de la barra
            pygame.draw.rect(screen, (64, 64, 64), (bar_x, bar_y, bar_width, bar_height))
            
            # Barra de agua
            water_width = int(bar_width * (self.water_level / self.max_water_level))
            pygame.draw.rect(screen, water_color, (bar_x, bar_y, water_width, bar_height))

class Stone:
    def __init__(self, x: int, y: int, size: int = 40):
        self.x = x
        self.y = y
        self.size = size
        self.width = size
        self.height = size
        self.stone_amount = random.randint(2, 5)  # Cantidad de piedra disponible
        self.max_stone = self.stone_amount
        self.is_mined = False
        self.regrowth_timer = 0
        self.regrowth_time = 2400  # 40 segundos para regenerar (a 60 FPS)
        
    def can_mine(self) -> bool:
        """Verificar si la piedra puede ser minada"""
        return not self.is_mined and self.stone_amount > 0
        
    def mine(self, player_inventory) -> int:
        """Minar piedra de la roca"""
        if not self.can_mine():
            return 0
            
        # Verificar si el jugador tiene pico equipado
        if not player_inventory.has_tool(ItemType.PICKAXE):
            return 0
            
        # Minar toda la piedra disponible de una vez
        mined_stone = self.stone_amount
        
        # Agregar piedra al inventario
        if player_inventory.add_item(ItemType.STONE, mined_stone):
            # Marcar como completamente minada (desaparecerá)
            self.is_mined = True
            self.stone_amount = 0
            return mined_stone
        return 0
        
    def update(self):
        """Actualizar piedra"""
        # Las piedras no se regeneran, desaparecen cuando se minan
        pass
                
    def is_player_nearby(self, player_x: int, player_y: int, player_width: int, player_height: int) -> bool:
        """Verificar si el jugador está cerca de la piedra"""
        # Calcular distancia entre centros
        stone_center_x = self.x + self.width // 2
        stone_center_y = self.y + self.height // 2
        player_center_x = player_x + player_width // 2
        player_center_y = player_y + player_height // 2
        
        distance = math.sqrt((stone_center_x - player_center_x)**2 + (stone_center_y - player_center_y)**2)
        return distance < 50  # Radio de interacción
        
    def draw(self, screen: pygame.Surface):
        """Dibujar piedra"""
        # Solo dibujar si no está minada (desaparece cuando se mina)
        if self.is_mined:
            return
            
        # Piedra activa
        # Dibujar forma irregular de piedra
        stone_points = [
            (self.x + 5, self.y + self.height - 5),
            (self.x + self.width - 5, self.y + self.height - 5),
            (self.x + self.width - 10, self.y + 10),
            (self.x + 10, self.y + 5),
            (self.x + 5, self.y + self.height - 5)
        ]
        
        # Color gris de piedra
        stone_color = (128, 128, 128)
        pygame.draw.polygon(screen, stone_color, stone_points)
        
        # Borde más oscuro
        pygame.draw.polygon(screen, (96, 96, 96), stone_points, 2)
        
        # Agregar textura
        for i in range(3):
            x = self.x + random.randint(5, self.width - 5)
            y = self.y + random.randint(5, self.height - 5)
            pygame.draw.circle(screen, (160, 160, 160), (x, y), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Aferdark")
        self.clock = pygame.time.Clock()
        
        # Estado del juego
        self.state = GameState.MENU
        self.time_of_day = TimeOfDay.DAY
        self.day_count = 1
        self.night_timer = 0
        self.day_timer = 0
        
        # Objetos del juego
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = []
        self.light_sources = []
        self.lagoons = []
        self.stones = []
        
        # Sistema de scroll para controles
        self.controls_scroll_offset = 0  # Offset de scroll para la lista de controles
        
        # Sistema de scroll para menús
        self.inventory_scroll_offset = 0  # Offset de scroll para el inventario
        self.crafting_scroll_offset = 0   # Offset de scroll para el crafteo
        self.building_scroll_offset = 0   # Offset de scroll para construcción
        
        # Sistemas
        self.crafting_system = CraftingSystem()
        self.inventory_ui = InventoryUI(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.crafting_ui = CraftingUI(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.building_system = BuildingSystem()
        self.building_ui = BuildingUI(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.tree_manager = TreeManager(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Fuentes
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)
        
        # Cargar assets
        assets.load_all_assets()
        
        # Generar lagunas en el mapa
        self.generate_lagoons()
        
        # Generar piedras en el mapa
        self.generate_stones()
        
    def generate_lagoons(self):
        """Generar lagunas aleatorias en el mapa"""
        num_lagoons = random.randint(3, 6)  # Entre 3 y 6 lagunas
        
        for _ in range(num_lagoons):
            # Posición aleatoria evitando los bordes
            x = random.randint(100, SCREEN_WIDTH - 160)
            y = random.randint(100, SCREEN_HEIGHT - 160)
            
            # Tamaño aleatorio
            size = random.randint(50, 80)
            
            # Verificar que no esté demasiado cerca de otras lagunas
            too_close = False
            for existing_lagoon in self.lagoons:
                distance = math.sqrt((x - existing_lagoon.x)**2 + (y - existing_lagoon.y)**2)
                if distance < 150:  # Mínimo 150 píxeles de separación
                    too_close = True
                    break
            
            if not too_close:
                self.lagoons.append(Lagoon(x, y, size))
        
    def generate_stones(self):
        """Generar piedras aleatorias en el mapa"""
        num_stones = random.randint(4, 8)  # Entre 4 y 8 piedras
        
        for _ in range(num_stones):
            # Posición aleatoria evitando los bordes
            x = random.randint(80, SCREEN_WIDTH - 120)
            y = random.randint(80, SCREEN_HEIGHT - 120)
            
            # Tamaño aleatorio
            size = random.randint(35, 50)
            
            # Verificar que no esté demasiado cerca de otras piedras o lagunas
            too_close = False
            for existing_stone in self.stones:
                distance = math.sqrt((x - existing_stone.x)**2 + (y - existing_stone.y)**2)
                if distance < 100:  # Mínimo 100 píxeles de separación
                    too_close = True
                    break
            
            # También verificar distancia con lagunas
            if not too_close:
                for lagoon in self.lagoons:
                    distance = math.sqrt((x - lagoon.x)**2 + (y - lagoon.y)**2)
                    if distance < 120:  # Mínimo 120 píxeles de separación
                        too_close = True
                        break
            
            if not too_close:
                self.stones.append(Stone(x, y, size))
        
    def spawn_enemies(self):
        """Generar enemigos durante la noche"""
        if self.time_of_day == TimeOfDay.NIGHT and len(self.enemies) < 5:
            if random.random() < 0.02:  # 2% de probabilidad por frame
                side = random.randint(0, 3)
                if side == 0:  # Arriba
                    x = random.randint(0, SCREEN_WIDTH)
                    y = -50
                elif side == 1:  # Derecha
                    x = SCREEN_WIDTH + 50
                    y = random.randint(0, SCREEN_HEIGHT)
                elif side == 2:  # Abajo
                    x = random.randint(0, SCREEN_WIDTH)
                    y = SCREEN_HEIGHT + 50
                else:  # Izquierda
                    x = -50
                    y = random.randint(0, SCREEN_HEIGHT)
                    
                self.enemies.append(Enemy(x, y))
                
    def update_time_of_day(self):
        """Actualizar ciclo día/noche"""
        if self.time_of_day == TimeOfDay.DAY:
            self.day_timer += 1
            if self.day_timer >= 1800:  # 30 segundos de día
                self.time_of_day = TimeOfDay.DUSK
                self.day_timer = 0
        elif self.time_of_day == TimeOfDay.DUSK:
            self.night_timer += 1
            if self.night_timer >= 300:  # 5 segundos de atardecer
                self.time_of_day = TimeOfDay.NIGHT
                self.night_timer = 0
        elif self.time_of_day == TimeOfDay.NIGHT:
            self.night_timer += 1
            if self.night_timer >= 1800:  # 30 segundos de noche
                self.time_of_day = TimeOfDay.DAWN
                self.night_timer = 0
                self.day_count += 1
        elif self.time_of_day == TimeOfDay.DAWN:
            self.day_timer += 1
            if self.day_timer >= 300:  # 5 segundos de amanecer
                self.time_of_day = TimeOfDay.DAY
                self.day_timer = 0
                # Limpiar enemigos al amanecer
                self.enemies.clear()
                
    def handle_input(self):
        """Manejar entrada del usuario"""
        keys = pygame.key.get_pressed()
        
        if self.state == GameState.PLAYING:
            # Movimiento
            dx = dy = 0
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy = -1
                self.player.direction = 3
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy = 1
                self.player.direction = 1
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx = -1
                self.player.direction = 2
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx = 1
                self.player.direction = 0
                
            # Correr
            self.player.is_running = keys[pygame.K_LSHIFT]
            
            # Interactuar
            if keys[pygame.K_e]:
                # Colocar antorcha
                if len(self.light_sources) < 3:
                    self.light_sources.append(LightSource(
                        self.player.x + self.player.width // 2,
                        self.player.y + self.player.height // 2
                    ))
                    
            # Recolectar recursos (espacio)
            if keys[pygame.K_SPACE]:
                self.collect_resources()
                
            # Interactuar con lagunas, farmear piedras o farmear árboles (F)
            if keys[pygame.K_f]:
                if not self.drink_from_lagoon():
                    if not self.mine_stones():
                        self.harvest_trees()
                        
            # Consumir carne (G)
            if keys[pygame.K_g]:
                self.consume_meat()
                    
            # Equipar armas con teclas numéricas
            if keys[pygame.K_1]:
                self.player.equip_weapon(ItemType.SPEAR)
            elif keys[pygame.K_2]:
                self.player.equip_weapon(ItemType.BOW)
            elif keys[pygame.K_3]:
                self.player.equip_tool(ItemType.AXE)
            elif keys[pygame.K_4]:
                self.player.equip_tool(ItemType.PICKAXE)
            elif keys[pygame.K_5]:
                self.player.equip_tool(ItemType.KNIFE)
            elif keys[pygame.K_0]:
                # Desequipar todo
                self.player.unequip_weapon()
                self.player.unequip_tool()
                
            # Actualizar vista previa de construcción
            if self.building_system.building_mode:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.building_system.update_preview(mouse_x, mouse_y)
                
            # Mover al jugador
            if dx != 0 or dy != 0:
                self.player.move(dx, dy)
                # Reproducir sonido de pasos ocasionalmente
                if random.random() < 0.1:  # 10% de probabilidad
                    assets.play_sound("footstep", 0.3)
                
    def collect_resources(self):
        """Recolectar recursos del entorno"""
        # Simular recolección aleatoria de recursos
        if random.random() < 0.3:  # 30% de probabilidad
            resource_types = [ItemType.WOOD, ItemType.STONE, ItemType.GRASS, ItemType.BONE]
            resource = random.choice(resource_types)
            quantity = random.randint(1, 3)
            
            if self.player.inventory.add_item(resource, quantity):
                print(f"Recolectaste {quantity} {resource.value}")
                assets.play_sound("collect", 0.5)
            else:
                print("Inventario lleno!")
                
    def drink_from_lagoon(self) -> bool:
        """Beber de una laguna cercana"""
        for lagoon in self.lagoons:
            if lagoon.is_player_nearby(self.player.x, self.player.y, self.player.width, self.player.height):
                if lagoon.can_drink():
                    water_restored = lagoon.drink()
                    self.player.thirst = min(100, self.player.thirst + water_restored)
                    print(f"Bebiste agua de la laguna! Sed restaurada: +{water_restored}")
                    assets.play_sound("collect", 0.4)
                    return True
                else:
                    print("La laguna está seca o no tiene suficiente agua")
                    return True  # Retornar True para evitar farmear árboles
        
        return False  # No hay lagunas cerca, se puede farmear árboles
        
    def mine_stones(self) -> bool:
        """Minar piedras cercanas"""
        for stone in self.stones:
            if stone.is_player_nearby(self.player.x, self.player.y, self.player.width, self.player.height):
                if stone.can_mine():
                    mined_amount = stone.mine(self.player.inventory)
                    if mined_amount > 0:
                        print(f"Minaste {mined_amount} piedra(s) y la roca desapareció!")
                        assets.play_sound("collect", 0.5)
                        return True
                    else:
                        print("Necesitas un pico equipado para minar piedras")
                        return True  # Retornar True para evitar farmear árboles
        
        return False  # No hay piedras cerca, se puede farmear árboles
        
    def consume_meat(self) -> bool:
        """Consumir carne para recuperar salud y hambre"""
        # Buscar carne en el inventario
        meat_item = None
        for item in self.player.inventory.items:
            if item.item_type == ItemType.MEAT:
                meat_item = item
                break
        
        if meat_item is None:
            print("No tienes carne para consumir!")
            return False
            
        # Verificar si el jugador necesita comer
        if self.player.health >= 100 and self.player.hunger >= 100:
            print("Ya estás lleno!")
            return False
            
        # Consumir la carne
        meat_item.quantity -= 1
        if meat_item.quantity <= 0:
            self.player.inventory.items.remove(meat_item)
            
        # Recuperar salud y hambre
        health_recovery = random.randint(15, 25)  # Entre 15 y 25 puntos de salud
        hunger_recovery = random.randint(20, 30)  # Entre 20 y 30 puntos de hambre
        
        self.player.health = min(100, self.player.health + health_recovery)
        self.player.hunger = min(100, self.player.hunger + hunger_recovery)
        
        print(f"Consumiste carne! +{health_recovery} salud, +{hunger_recovery} hambre")
        assets.play_sound("eat", 0.6)
        
        return True
        
    def harvest_trees(self):
        """Farmear árboles cercanos"""
        harvested = self.tree_manager.harvest_nearby_trees(
            self.player.x, self.player.y, self.player.width, self.player.height,
            self.player.inventory
        )
        
        if harvested > 0:
            print(f"Farmaste {harvested} madera de los árboles")
            assets.play_sound("collect", 0.6)
        else:
            print("No hay árboles cerca para farmear")
                    
    def player_attack(self, target_x: int, target_y: int):
        """Ataque del jugador con arma equipada"""
        if not self.player.equipped_weapon or self.player.stamina < 15:
            return
            
        # Consumir stamina
        self.player.stamina -= 15
        
        # Calcular rango de ataque según el arma
        attack_range = 50  # Rango base
        if self.player.equipped_weapon == ItemType.SPEAR:
            attack_range = 80  # Lanza tiene más alcance
        elif self.player.equipped_weapon == ItemType.BOW:
            attack_range = 120  # Arco tiene mucho alcance
        elif self.player.equipped_weapon in [ItemType.AXE, ItemType.PICKAXE, ItemType.KNIFE]:
            attack_range = 40  # Herramientas tienen menos alcance
            
        # Buscar enemigos en el rango
        for enemy in self.enemies[:]:
            distance = math.sqrt((enemy.x - target_x)**2 + (enemy.y - target_y)**2)
            if distance <= attack_range:
                damage = self.player.get_total_damage()
                enemy.health -= damage
                
                print(f"Atacaste con {self.player.equipped_weapon.value} por {damage} daño!")
                assets.play_sound("enemy_hit", 0.7)
                
                # Si el enemigo muere
                if enemy.health <= 0:
                    print(f"¡Mataste al enemigo con {self.player.equipped_weapon.value}!")
                    self.enemies.remove(enemy)
                else:
                    print(f"Enemigo herido! Vida restante: {enemy.health}")
                    
    def check_auto_attack(self, enemy):
        """Verificar si el jugador debe atacar automáticamente cuando un enemigo se acerca"""
        if not self.player.equipped_weapon or self.player.stamina < 15 or self.player.auto_attack_cooldown > 0:
            return
            
        # Calcular distancia al enemigo
        distance = math.sqrt((enemy.x - self.player.x)**2 + (enemy.y - self.player.y)**2)
        
        # Calcular rango de ataque según el arma
        attack_range = 50  # Rango base
        if self.player.equipped_weapon == ItemType.SPEAR:
            attack_range = 160  # Lanza tiene más alcance
        elif self.player.equipped_weapon == ItemType.BOW:
            attack_range = 200  # Arco tiene mucho alcance
        elif self.player.equipped_weapon in [ItemType.AXE, ItemType.PICKAXE, ItemType.KNIFE]:
            attack_range = 100  # Herramientas tienen menos alcance
            
        # Si el enemigo está en rango de ataque, atacar automáticamente
        if distance <= attack_range:
            # Verificar que no esté demasiado cerca (para evitar spam de ataques)
            if distance > 25:  # Mínimo 25 píxeles de distancia
                damage = self.player.get_total_damage()
                enemy.health -= damage
                self.player.stamina -= 15  # Consumir stamina
                self.player.auto_attack_cooldown = self.player.auto_attack_delay  # Activar cooldown
                
                print(f"Atacaste automáticamente con {self.player.equipped_weapon.value} por {damage} daño!")
                assets.play_sound("enemy_hit", 0.7)
                
                # Si el enemigo muere
                if enemy.health <= 0:
                    self.enemies.remove(enemy)
                    print("¡Enemigo eliminado!")
                    assets.play_sound("enemy_death", 0.8)
                    
                    # Dejar carne al morir
                    meat_amount = random.randint(1, 3)  # Entre 1 y 3 carnes
                    self.player.inventory.add_item(ItemType.MEAT, meat_amount)
                    print(f"El enemigo dejó {meat_amount} carne!")
                    
    def update(self):
        """Actualizar lógica del juego"""
        if self.state not in [GameState.PLAYING]:
            return
            
        # Actualizar tiempo
        self.update_time_of_day()
        
        # Cambiar música según el tiempo del día
        if self.time_of_day == TimeOfDay.DAY:
            if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
                assets.play_music("ambient_day", -1, 0.3)
        elif self.time_of_day == TimeOfDay.NIGHT:
            if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
                assets.play_music("ambient_night", -1, 0.4)
        
        # Actualizar jugador
        self.player.update()
        
        # Generar enemigos
        self.spawn_enemies()
        
        # Actualizar enemigos
        for enemy in self.enemies[:]:
            enemy.update(self.player, self.light_sources)
            
            # Verificar si el jugador debe atacar automáticamente
            self.check_auto_attack(enemy)
            
            # Verificar colisión con jugador
            if (abs(enemy.x - self.player.x) < 30 and 
                abs(enemy.y - self.player.y) < 30):
                # Calcular protección del refugio
                shelter_protection = self.building_system.get_shelter_protection(
                    self.player.x, self.player.y
                )
                
                # Reducir daño según la protección
                actual_damage = enemy.damage * (1 - shelter_protection)
                self.player.health -= actual_damage
                
                # Si el jugador tiene arma equipada, puede contraatacar
                if self.player.equipped_weapon and self.player.stamina > 10:
                    # El jugador contraataca con su arma
                    counter_damage = self.player.get_total_damage()
                    enemy.health -= counter_damage
                    self.player.stamina -= 10  # Consumir stamina al atacar
                    
                    print(f"Contraatacaste con {self.player.equipped_weapon.value} por {counter_damage} daño!")
                    assets.play_sound("enemy_hit", 0.6)
                    
                    # Si el enemigo muere por el contraataque
                    if enemy.health <= 0:
                        print(f"¡Mataste al enemigo con {self.player.equipped_weapon.value}!")
                        self.enemies.remove(enemy)
                        
                        # Dejar carne al morir
                        meat_amount = random.randint(1, 3)  # Entre 1 y 3 carnes
                        self.player.inventory.add_item(ItemType.MEAT, meat_amount)
                        print(f"El enemigo dejó {meat_amount} carne!")
                        
                        continue
                
                self.enemies.remove(enemy)
                
        # Dañar construcciones durante la noche
        if self.time_of_day == TimeOfDay.NIGHT and random.random() < 0.01:
            self.building_system.damage_buildings(5)
                
        # Actualizar fuentes de luz
        for light in self.light_sources[:]:
            light.update()
            if not light.is_active:
                self.light_sources.remove(light)
                
        # Actualizar árboles
        self.tree_manager.update()
        
        # Actualizar lagunas
        for lagoon in self.lagoons:
            lagoon.update()
            
        # Actualizar piedras
        for stone in self.stones:
            stone.update()
                
        # Verificar condiciones de derrota
        if self.player.health <= 0:
            self.state = GameState.GAME_OVER
            
    def draw_hud(self):
        """Dibujar interfaz de usuario"""
        
        # Función para renderizar texto con borde negro
        def render_text_with_border(font, text, text_color, border_color):
            # Renderizar texto con borde
            text_surface = font.render(text, True, text_color)
            border_surface = font.render(text, True, border_color)
            
            # Crear superficie más grande para el borde
            border_width = text_surface.get_width() + 4
            border_height = text_surface.get_height() + 4
            bordered_surface = pygame.Surface((border_width, border_height), pygame.SRCALPHA)
            
            # Dibujar borde (2 píxeles de grosor)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        bordered_surface.blit(border_surface, (dx + 1, dy + 1))
            
            # Dibujar texto principal encima
            bordered_surface.blit(text_surface, (1, 1))
            
            return bordered_surface
        
        # Barras de vida, hambre, sed y resistencia
        y_offset = 20
        
        # Vida
        health_width = int(200 * (self.player.health / self.player.max_health))
        pygame.draw.rect(self.screen, RED, (20, y_offset, health_width, 15))
        pygame.draw.rect(self.screen, BLACK, (20, y_offset, 200, 15), 2)
        text_surface = render_text_with_border(self.font, f"Vida: {int(self.player.health)}", WHITE, BLACK)
        self.screen.blit(text_surface, (230, y_offset))
        
        # Hambre
        y_offset += 25
        hunger_width = int(200 * (self.player.hunger / 100))
        pygame.draw.rect(self.screen, ORANGE, (20, y_offset, hunger_width, 15))
        pygame.draw.rect(self.screen, BLACK, (20, y_offset, 200, 15), 2)
        text_surface = render_text_with_border(self.font, f"Hambre: {int(self.player.hunger)}", WHITE, BLACK)
        self.screen.blit(text_surface, (230, y_offset))
        
        # Sed
        y_offset += 25
        thirst_width = int(200 * (self.player.thirst / 100))
        pygame.draw.rect(self.screen, BLUE, (20, y_offset, thirst_width, 15))
        pygame.draw.rect(self.screen, BLACK, (20, y_offset, 200, 15), 2)
        text_surface = render_text_with_border(self.font, f"Sed: {int(self.player.thirst)}", WHITE, BLACK)
        self.screen.blit(text_surface, (230, y_offset))
        
        # Resistencia
        y_offset += 25
        stamina_width = int(200 * (self.player.stamina / self.player.max_stamina))
        pygame.draw.rect(self.screen, YELLOW, (20, y_offset, stamina_width, 15))
        pygame.draw.rect(self.screen, BLACK, (20, y_offset, 200, 15), 2)
        text_surface = render_text_with_border(self.font, f"Resistencia: {int(self.player.stamina)}", WHITE, BLACK)
        self.screen.blit(text_surface, (230, y_offset))
        
        # Información del equipamiento
        y_offset += 25
        
        # Arma equipada
        if self.player.equipped_weapon:
            weapon_text = f"Arma: {self.player.equipped_weapon.value.title()} (+{self.player.weapon_damage} daño)"
            text_surface = render_text_with_border(self.font, weapon_text, GREEN, BLACK)
            self.screen.blit(text_surface, (20, y_offset))
        else:
            text_surface = render_text_with_border(self.font, "Arma: Ninguna", GRAY, BLACK)
            self.screen.blit(text_surface, (20, y_offset))
            
        # Herramienta equipada
        y_offset += 25
        if self.player.equipped_tool:
            tool_text = f"Herramienta: {self.player.equipped_tool.value.title()}"
            text_surface = render_text_with_border(self.font, tool_text, BLUE, BLACK)
            self.screen.blit(text_surface, (20, y_offset))
        else:
            text_surface = render_text_with_border(self.font, "Herramienta: Ninguna", GRAY, BLACK)
            self.screen.blit(text_surface, (20, y_offset))
        
        # Indicador de pausa cuando se abren las interfaces
        if self.state in [GameState.INVENTORY, GameState.CRAFTING, GameState.BUILDING]:
            pause_text = self.font.render("JUEGO PAUSADO", True, YELLOW)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, 50))
            self.screen.blit(pause_text, pause_rect)
        
    def draw_time_info(self):
        """Dibujar información detallada del tiempo en la parte inferior central"""
        # Calcular tiempo del día en formato de horas
        if self.time_of_day == TimeOfDay.DAY:
            hour = 6 + (self.day_timer * 12) // 1800  # 6 AM a 6 PM (12 horas)
        elif self.time_of_day == TimeOfDay.DUSK:
            hour = 18 + (self.night_timer * 6) // 300  # 6 PM a 7 PM (1 hora)
        elif self.time_of_day == TimeOfDay.NIGHT:
            hour = 19 + (self.night_timer * 11) // 1800  # 7 PM a 6 AM (11 horas)
        elif self.time_of_day == TimeOfDay.DAWN:
            hour = 6 + (self.day_timer * 6) // 300  # 6 AM a 7 AM (1 hora)
        
        # Formatear hora
        display_hour = hour % 24
        time_str = f"{display_hour:02d}:00"
        
        # Texto principal del tiempo
        time_info = f"Hora: {time_str} | Día {self.day_count} | {self.time_of_day.value.title()}"
        
        # Crear texto con borde negro
        def render_text_with_border(font, text, text_color, border_color):
            # Renderizar texto con borde
            text_surface = font.render(text, True, text_color)
            border_surface = font.render(text, True, border_color)
            
            # Crear superficie más grande para el borde
            border_width = text_surface.get_width() + 4
            border_height = text_surface.get_height() + 4
            bordered_surface = pygame.Surface((border_width, border_height), pygame.SRCALPHA)
            
            # Dibujar borde (4 píxeles de grosor)
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    if dx != 0 or dy != 0:
                        bordered_surface.blit(border_surface, (dx + 2, dy + 2))
            
            # Dibujar texto principal encima
            bordered_surface.blit(text_surface, (2, 2))
            
            return bordered_surface
        
        # Renderizar texto con borde
        time_text_surface = render_text_with_border(self.font, time_info, WHITE, BLACK)
        
        # Posicionar en la parte inferior central de la pantalla
        text_rect = time_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(time_text_surface, text_rect)
        
    def draw_menu(self):
        """Dibujar menú principal"""
        # Cargar imagen de fondo si existe
        try:
            background_image = pygame.image.load("assets/images/menu_background.png")
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(background_image, (0, 0))
        except pygame.error:
            # Si no se puede cargar la imagen, usar fondo negro
            self.screen.fill(BLACK)
        
        # El título ya está en la imagen de fondo, no necesitamos dibujarlo aquí
        
        # Texto principal
        subtitle = self.font.render("Presiona ESPACIO para comenzar", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 350))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Botón de controles
        controls_text = self.font.render("Presiona C para ver Controles", True, WHITE)
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH//2, 450))
        self.screen.blit(controls_text, controls_rect)
            
    def draw_controls(self):
        """Dibujar pantalla de controles"""
        # Cargar imagen de fondo si existe
        try:
            background_image = pygame.image.load("assets/images/menu_background.png")
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(background_image, (0, 0))
        except pygame.error:
            # Si no se puede cargar la imagen, usar fondo negro
            self.screen.fill(BLACK)
        
        # Título de controles
        title = self.big_font.render("CONTROLES", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        # Crear caja para los controles
        box_width = 500
        box_height = 400
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = 200
        
        # Dibujar fondo de la caja
        pygame.draw.rect(self.screen, (30, 30, 30), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(self.screen, WHITE, (box_x, box_y, box_width, box_height), 2)
        
        # Lista de controles (expandida para necesitar scroll)
        controls = [
            "=== MOVIMIENTO ===",
            "WASD - Movimiento",
            "SHIFT - Correr",
            "",
            "=== INTERACCIÓN ===",
            "E - Colocar antorcha",
            "ESPACIO - Recolectar recursos",
            "F - Interactuar",
            "G - Consumir carne",
            "",
            "=== EQUIPAMIENTO ===",
            "1 - Equipar lanza",
            "2 - Equipar arco",
            "3 - Equipar hacha",
            "4 - Equipar pico",
            "5 - Equipar cuchillo",
            "0 - Desequipar todo",
            "",
            "=== INTERFACES ===",
            "I - Inventario",
            "C - Crafteo",
            "B - Construcción",
            "M - Modo construcción",
            "",
            "=== SISTEMA ===",
            "ESC - Pausa",
            "ENTER - Usar item (en inventario)",
            "Flechas - Navegar (en inventario)",
            "",
            "=== COMBATE ===",
            "Click Izquierdo - Atacar (con arma)",
            "Ataque Automático - Al acercarse enemigos",
            "",
            "=== CONSTRUCCIÓN ===",
            "Click Izquierdo - Colocar estructura",
            "Click Derecho - Cancelar construcción"
        ]
        
        # Crear superficie para el contenido scrolleable
        content_height = len(controls) * 25 + 50  # Altura total del contenido
        scroll_surface = pygame.Surface((box_width - 20, content_height))
        scroll_surface.fill((30, 30, 30))
        
        # Dibujar controles en la superficie de scroll
        y_offset = 25
        for line in controls:
            if line.startswith("==="):
                # Títulos de sección
                text = self.font.render(line, True, (255, 255, 100))
            elif line == "":
                # Línea vacía
                y_offset += 15
                continue
            else:
                # Controles normales
                text = self.font.render(line, True, WHITE)
            
            text_rect = text.get_rect(center=(scroll_surface.get_width()//2, y_offset))
            scroll_surface.blit(text, text_rect)
            y_offset += 25
        
        # Aplicar scroll y dibujar contenido visible
        visible_height = box_height - 20
        scroll_y = max(0, min(self.controls_scroll_offset, content_height - visible_height))
        
        # Crear máscara para el área visible
        mask = pygame.Surface((box_width - 20, visible_height))
        mask.fill((30, 30, 30))
        
        # Dibujar la parte visible del contenido
        self.screen.blit(scroll_surface, (box_x + 10, box_y + 10), 
                        (0, scroll_y, box_width - 20, visible_height))
        
        # Dibujar indicadores de scroll si es necesario
        if content_height > visible_height:
            # Barra de scroll
            scroll_bar_width = 10
            scroll_bar_height = int((visible_height / content_height) * visible_height)
            scroll_bar_y = box_y + 10 + int((scroll_y / (content_height - visible_height)) * (visible_height - scroll_bar_height))
            
            pygame.draw.rect(self.screen, (100, 100, 100), 
                           (box_x + box_width - 15, box_y + 10, scroll_bar_width, visible_height))
            pygame.draw.rect(self.screen, WHITE, 
                           (box_x + box_width - 15, scroll_bar_y, scroll_bar_width, scroll_bar_height))
        
        # Instrucciones de navegación
        nav_text = self.font.render("Flechas para navegar | ESC para volver", True, WHITE)
        nav_rect = nav_text.get_rect(center=(SCREEN_WIDTH//2, 650))
        self.screen.blit(nav_text, nav_rect)
            
    def draw_game_over(self):
        """Dibujar pantalla de game over"""
        self.screen.fill(BLACK)
        
        game_over = self.big_font.render("LA OSCURIDAD TE ENCONTRÓ...", True, RED)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(game_over, game_over_rect)
        
        stats = f"Superviviste {self.day_count} días"
        stats_text = self.font.render(stats, True, WHITE)
        stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH//2, 400))
        self.screen.blit(stats_text, stats_rect)
        
        restart = "Presiona R para reiniciar"
        restart_text = self.font.render(restart, True, GRAY)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, 500))
        self.screen.blit(restart_text, restart_rect)
        
    def draw_lagoon_interaction_hint(self):
        """Dibujar indicador cuando el jugador está cerca de una laguna"""
        for lagoon in self.lagoons:
            if lagoon.is_player_nearby(self.player.x, self.player.y, self.player.width, self.player.height):
                if lagoon.can_drink():
                    # Dibujar texto "Presiona F para beber"
                    hint_text = self.font.render("Presiona F para beber", True, WHITE)
                    hint_rect = hint_text.get_rect(center=(lagoon.x + lagoon.width // 2, lagoon.y - 20))
                    
                    # Fondo semitransparente
                    bg_rect = hint_rect.inflate(10, 5)
                    pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)
                    
                    self.screen.blit(hint_text, hint_rect)
                else:
                    # Dibujar texto "Laguna seca"
                    hint_text = self.font.render("Laguna seca", True, RED)
                    hint_rect = hint_text.get_rect(center=(lagoon.x + lagoon.width // 2, lagoon.y - 20))
                    
                    # Fondo semitransparente
                    bg_rect = hint_rect.inflate(10, 5)
                    pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)
                    
                    self.screen.blit(hint_text, hint_rect)
                break  # Solo mostrar un indicador a la vez
        
    def draw_stone_interaction_hint(self):
        """Dibujar indicador cuando el jugador está cerca de una piedra"""
        for stone in self.stones:
            # Solo mostrar indicador si la piedra no está minada (no existe)
            if not stone.is_mined and stone.is_player_nearby(self.player.x, self.player.y, self.player.width, self.player.height):
                if stone.can_mine():
                    if self.player.inventory.has_tool(ItemType.PICKAXE):
                        # Dibujar texto "Presiona F para minar"
                        hint_text = self.font.render("Presiona F para minar", True, WHITE)
                        hint_rect = hint_text.get_rect(center=(stone.x + stone.width // 2, stone.y - 20))
                        
                        # Fondo semitransparente
                        bg_rect = hint_rect.inflate(10, 5)
                        pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)
                        
                        self.screen.blit(hint_text, hint_rect)
                    else:
                        # Dibujar texto "Necesitas un pico"
                        hint_text = self.font.render("Necesitas un pico", True, RED)
                        hint_rect = hint_text.get_rect(center=(stone.x + stone.width // 2, stone.y - 20))
                        
                        # Fondo semitransparente
                        bg_rect = hint_rect.inflate(10, 5)
                        pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)
                        
                        self.screen.blit(hint_text, hint_rect)
                break  # Solo mostrar un indicador a la vez
        
    def draw(self):
        """Dibujar todo el juego"""
        # Fondo según el tiempo del día
        background_image = None
        if self.time_of_day == TimeOfDay.DAY:
            background_image = assets.get_image("background_day")
            if not background_image:
                self.screen.fill((135, 206, 235))  # Azul cielo
        elif self.time_of_day == TimeOfDay.DUSK:
            background_image = assets.get_image("background_dusk")
            if not background_image:
                self.screen.fill((255, 140, 0))  # Naranja atardecer
        elif self.time_of_day == TimeOfDay.NIGHT:
            background_image = assets.get_image("background_night")
            if not background_image:
                self.screen.fill((25, 25, 50))  # Azul oscuro noche
        elif self.time_of_day == TimeOfDay.DAWN:
            background_image = assets.get_image("background_dawn")
            if not background_image:
                self.screen.fill((255, 192, 203))  # Rosa amanecer
                
        if background_image:
            # Escalar imagen para cubrir toda la pantalla
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(background_image, (0, 0))
            
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state in [GameState.PLAYING, GameState.INVENTORY, GameState.CRAFTING, GameState.BUILDING]:
            # Dibujar fuentes de luz
            for light in self.light_sources:
                light.draw(self.screen)
                
            # Dibujar árboles
            self.tree_manager.draw(self.screen)
            
            # Dibujar lagunas
            for lagoon in self.lagoons:
                lagoon.draw(self.screen, self.font)
                
            # Dibujar piedras
            for stone in self.stones:
                stone.draw(self.screen)
                
            # Dibujar construcciones
            self.building_system.draw(self.screen)
            
            # Dibujar enemigos
            for enemy in self.enemies:
                enemy.draw(self.screen)
                
            # Dibujar jugador
            self.player.draw(self.screen)
            
            # Dibujar vista previa de construcción
            self.building_system.draw_preview(self.screen)
            
            # Dibujar HUD
            self.draw_hud()
            
            # Dibujar información del tiempo en la parte inferior
            self.draw_time_info()
            
            # Dibujar indicadores de interacción con árboles
            self.tree_manager.draw_interaction_hint(
                self.screen, self.player.x, self.player.y, 
                self.player.width, self.player.height
            )
            
            # Dibujar indicador de interacción con lagunas
            self.draw_lagoon_interaction_hint()
            
            # Dibujar indicador de interacción con piedras
            self.draw_stone_interaction_hint()
            
            # Dibujar interfaces según el estado
            if self.state == GameState.INVENTORY:
                self.inventory_ui.draw(self.screen, self.player.inventory, self.crafting_system, self.inventory_scroll_offset)
            elif self.state == GameState.CRAFTING:
                self.crafting_ui.draw(self.screen, self.player.inventory, self.crafting_system, self.crafting_scroll_offset)
            elif self.state == GameState.BUILDING:
                self.building_ui.draw(self.screen, self.building_system, self.building_scroll_offset)
            
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.state == GameState.CONTROLS:
            self.draw_controls()
            
    def run(self):
        """Bucle principal del juego"""
        running = True
        
        while running:
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEWHEEL:
                    # Manejar scroll con rueda del mouse en controles
                    if self.state == GameState.CONTROLS:
                        self.controls_scroll_offset -= event.y * 20
                        self.controls_scroll_offset = max(0, self.controls_scroll_offset)
                    elif self.state == GameState.INVENTORY:
                        self.inventory_scroll_offset -= event.y * 20
                        self.inventory_scroll_offset = max(0, self.inventory_scroll_offset)
                    elif self.state == GameState.CRAFTING:
                        self.crafting_scroll_offset -= event.y * 20
                        self.crafting_scroll_offset = max(0, self.crafting_scroll_offset)
                    elif self.state == GameState.BUILDING:
                        self.building_scroll_offset -= event.y * 20
                        self.building_scroll_offset = max(0, self.building_scroll_offset)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == GameState.PLAYING:
                            self.state = GameState.PAUSED
                        elif self.state == GameState.PAUSED:
                            self.state = GameState.PLAYING
                        elif self.state == GameState.CONTROLS:
                            self.state = GameState.MENU
                    elif event.key == pygame.K_SPACE:
                        if self.state == GameState.MENU:
                            self.state = GameState.PLAYING
                            # Reiniciar juego
                            self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                            self.enemies.clear()
                            self.light_sources.clear()
                            self.lagoons.clear()
                            self.stones.clear()
                            self.generate_lagoons()
                            self.generate_stones()
                            self.day_count = 1
                            self.time_of_day = TimeOfDay.DAY
                    elif event.key == pygame.K_c:
                        if self.state == GameState.MENU:
                            self.state = GameState.CONTROLS
                    elif event.key == pygame.K_UP:
                        if self.state == GameState.CONTROLS:
                            self.controls_scroll_offset = max(0, self.controls_scroll_offset - 30)
                        elif self.state == GameState.INVENTORY:
                            self.inventory_scroll_offset = max(0, self.inventory_scroll_offset - 30)
                        elif self.state == GameState.CRAFTING:
                            self.crafting_scroll_offset = max(0, self.crafting_scroll_offset - 30)
                        elif self.state == GameState.BUILDING:
                            self.building_scroll_offset = max(0, self.building_scroll_offset - 30)
                    elif event.key == pygame.K_DOWN:
                        if self.state == GameState.CONTROLS:
                            self.controls_scroll_offset += 30
                        elif self.state == GameState.INVENTORY:
                            self.inventory_scroll_offset += 30
                        elif self.state == GameState.CRAFTING:
                            self.crafting_scroll_offset += 30
                        elif self.state == GameState.BUILDING:
                            self.building_scroll_offset += 30
                    elif event.key == pygame.K_r:
                        if self.state == GameState.GAME_OVER:
                            self.state = GameState.MENU
                    elif event.key == pygame.K_i:
                        # Abrir/cerrar inventario
                        if self.state == GameState.PLAYING:
                            self.inventory_ui.toggle()
                            if self.inventory_ui.is_open:
                                self.state = GameState.INVENTORY
                        elif self.state == GameState.INVENTORY:
                            self.inventory_ui.toggle()
                            self.state = GameState.PLAYING
                            
                    # Manejar entrada del inventario
                    if self.state == GameState.INVENTORY:
                        inventory_result = self.inventory_ui.handle_input(event, self.player.inventory, self.crafting_system)
                        if inventory_result:
                            if inventory_result.startswith("equip_weapon:"):
                                weapon_type = inventory_result.split(":")[1]
                                # Convertir string a ItemType
                                for item_type in ItemType:
                                    if item_type.value == weapon_type:
                                        self.player.equip_weapon(item_type)
                                        print(f"Equipaste {item_type.value} como arma!")
                                        break
                            elif inventory_result.startswith("equip_tool:"):
                                tool_type = inventory_result.split(":")[1]
                                # Convertir string a ItemType
                                for item_type in ItemType:
                                    if item_type.value == tool_type:
                                        self.player.equip_tool(item_type)
                                        print(f"Equipaste {item_type.value} como herramienta!")
                                        break
                            elif inventory_result == "craft":
                                self.state = GameState.CRAFTING
                                self.crafting_ui.toggle()
                            elif inventory_result == "close":
                                self.state = GameState.PLAYING
                                self.inventory_ui.toggle()
                    elif event.key == pygame.K_c:
                        # Abrir/cerrar crafteo
                        if self.state == GameState.PLAYING:
                            self.crafting_ui.toggle()
                            if self.crafting_ui.is_open:
                                self.state = GameState.CRAFTING
                        elif self.state == GameState.CRAFTING:
                            self.crafting_ui.toggle()
                            self.state = GameState.PLAYING
                    elif event.key == pygame.K_b:
                        # Abrir/cerrar construcción
                        if self.state == GameState.PLAYING:
                            self.building_ui.toggle()
                            if self.building_ui.is_open:
                                self.state = GameState.BUILDING
                        elif self.state == GameState.BUILDING:
                            self.building_ui.toggle()
                            self.state = GameState.PLAYING
                    elif event.key == pygame.K_m:
                        # Activar/desactivar modo construcción
                        if self.state == GameState.PLAYING:
                            self.building_system.toggle_building_mode()
                            if self.building_system.building_mode:
                                self.state = GameState.BUILDING
                        elif self.state == GameState.BUILDING:
                            self.building_system.toggle_building_mode()
                            self.state = GameState.PLAYING
                            
                # Manejar entrada de las interfaces según el estado
                if self.state == GameState.INVENTORY:
                    result = self.inventory_ui.handle_input(event, self.player.inventory, self.crafting_system)
                    if result == "close":
                        self.state = GameState.PLAYING
                    elif result == "craft":
                        self.crafting_ui.toggle()
                        if self.crafting_ui.is_open:
                            self.state = GameState.CRAFTING
                elif self.state == GameState.CRAFTING:
                    result = self.crafting_ui.handle_input(event, self.player.inventory, self.crafting_system)
                    if result == "close":
                        self.state = GameState.PLAYING
                elif self.state == GameState.BUILDING:
                    result = self.building_ui.handle_input(event, self.building_system)
                    if result == "close":
                        self.state = GameState.PLAYING
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic izquierdo
                        if self.state == GameState.BUILDING and self.building_system.building_mode:
                            mouse_x, mouse_y = event.pos
                            # Construir en la posición del mouse
                            if self.building_system.build(mouse_x, mouse_y, self.building_system.selected_building_type):
                                print(f"Construiste {self.building_system.selected_building_type.value}")
                                assets.play_sound("build", 0.7)
                            else:
                                print("No se puede construir aquí")
                        elif self.state == GameState.PLAYING and self.player.equipped_weapon and self.player.stamina > 15:
                            # Ataque con arma equipada
                            mouse_x, mouse_y = event.pos
                            self.player_attack(mouse_x, mouse_y)
                            
            # Actualizar y dibujar
            self.handle_input()
            self.update()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
