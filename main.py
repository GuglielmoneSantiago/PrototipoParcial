#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Videojuego de Supervivencia Nocturna
Basado en la documentación Game Treatment Mata-Guglielmone

Un juego de supervivencia donde el jugador debe resistir las noches
contra criaturas hostiles, construyendo refugios y gestionando recursos.
"""

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
            
    def update(self):
        """Actualizar estado del jugador"""
        # Reducir hambre y sed gradualmente
        self.hunger = max(0, self.hunger - 0.01)
        self.thirst = max(0, self.thirst - 0.015)
        
        # Si hambre o sed llegan a 0, reducir salud
        if self.hunger <= 0 or self.thirst <= 0:
            self.health = max(0, self.health - 0.5)
            
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

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Supervivencia Nocturna")
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
                
            # Farmear árboles (F)
            if keys[pygame.K_f]:
                self.harvest_trees()
                
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
                
        # Verificar condiciones de derrota
        if self.player.health <= 0:
            self.state = GameState.GAME_OVER
            
    def draw_hud(self):
        """Dibujar interfaz de usuario"""
        # Fondo del HUD
        hud_rect = pygame.Rect(10, 10, 300, 120)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), hud_rect)
        
        # Barras de vida, hambre, sed y resistencia
        y_offset = 20
        
        # Vida
        health_width = int(200 * (self.player.health / self.player.max_health))
        pygame.draw.rect(self.screen, RED, (20, y_offset, health_width, 15))
        pygame.draw.rect(self.screen, WHITE, (20, y_offset, 200, 15), 2)
        text = self.font.render(f"Vida: {int(self.player.health)}", True, WHITE)
        self.screen.blit(text, (230, y_offset))
        
        # Hambre
        y_offset += 25
        hunger_width = int(200 * (self.player.hunger / 100))
        pygame.draw.rect(self.screen, ORANGE, (20, y_offset, hunger_width, 15))
        pygame.draw.rect(self.screen, WHITE, (20, y_offset, 200, 15), 2)
        text = self.font.render(f"Hambre: {int(self.player.hunger)}", True, WHITE)
        self.screen.blit(text, (230, y_offset))
        
        # Sed
        y_offset += 25
        thirst_width = int(200 * (self.player.thirst / 100))
        pygame.draw.rect(self.screen, BLUE, (20, y_offset, thirst_width, 15))
        pygame.draw.rect(self.screen, WHITE, (20, y_offset, 200, 15), 2)
        text = self.font.render(f"Sed: {int(self.player.thirst)}", True, WHITE)
        self.screen.blit(text, (230, y_offset))
        
        # Resistencia
        y_offset += 25
        stamina_width = int(200 * (self.player.stamina / self.player.max_stamina))
        pygame.draw.rect(self.screen, YELLOW, (20, y_offset, stamina_width, 15))
        pygame.draw.rect(self.screen, WHITE, (20, y_offset, 200, 15), 2)
        text = self.font.render(f"Resistencia: {int(self.player.stamina)}", True, WHITE)
        self.screen.blit(text, (230, y_offset))
        
        # Información del tiempo
        time_text = f"Día {self.day_count} - {self.time_of_day.value.upper()}"
        text = self.font.render(time_text, True, WHITE)
        self.screen.blit(text, (20, y_offset + 30))
        
        # Indicador de pausa cuando se abren las interfaces
        if self.state in [GameState.INVENTORY, GameState.CRAFTING, GameState.BUILDING]:
            pause_text = self.font.render("JUEGO PAUSADO", True, YELLOW)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, 50))
            self.screen.blit(pause_text, pause_rect)
        
    def draw_menu(self):
        """Dibujar menú principal"""
        self.screen.fill(BLACK)
        
        title = self.big_font.render("SUPERVIVENCIA NOCTURNA", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font.render("Presiona ESPACIO para comenzar", True, GRAY)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(subtitle, subtitle_rect)
        
        controls = [
            "Controles:",
            "WASD - Movimiento",
            "SHIFT - Correr",
            "E - Colocar antorcha",
            "ESPACIO - Recolectar recursos",
            "F - Farmear árboles",
            "I - Inventario",
            "C - Crafteo",
            "B - Construcción",
            "M - Modo construcción",
            "ESC - Pausa"
        ]
        
        y_offset = 400
        for line in controls:
            text = self.font.render(line, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH//2 - 100, y_offset))
            y_offset += 30
            
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
            
            # Dibujar indicadores de interacción con árboles
            self.tree_manager.draw_interaction_hint(
                self.screen, self.player.x, self.player.y, 
                self.player.width, self.player.height
            )
            
            # Dibujar interfaces según el estado
            if self.state == GameState.INVENTORY:
                self.inventory_ui.draw(self.screen, self.player.inventory, self.crafting_system)
            elif self.state == GameState.CRAFTING:
                self.crafting_ui.draw(self.screen, self.player.inventory, self.crafting_system)
            elif self.state == GameState.BUILDING:
                self.building_ui.draw(self.screen, self.building_system)
            
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
            
    def run(self):
        """Bucle principal del juego"""
        running = True
        
        while running:
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == GameState.PLAYING:
                            self.state = GameState.PAUSED
                        elif self.state == GameState.PAUSED:
                            self.state = GameState.PLAYING
                    elif event.key == pygame.K_SPACE:
                        if self.state == GameState.MENU:
                            self.state = GameState.PLAYING
                            # Reiniciar juego
                            self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                            self.enemies.clear()
                            self.light_sources.clear()
                            self.day_count = 1
                            self.time_of_day = TimeOfDay.DAY
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
                    if event.button == 1 and self.state == GameState.BUILDING and self.building_system.building_mode:  # Clic izquierdo
                        mouse_x, mouse_y = event.pos
                        # Construir en la posición del mouse
                        if self.building_system.build(mouse_x, mouse_y, self.building_system.selected_building_type):
                            print(f"Construiste {self.building_system.selected_building_type.value}")
                            assets.play_sound("build", 0.7)
                        else:
                            print("No se puede construir aquí")
                            
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
