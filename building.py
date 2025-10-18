#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Construcción de Refugio
Para el videojuego de Supervivencia Nocturna
"""

import pygame
import math
from enum import Enum
from typing import List, Tuple, Optional
from inventory import ItemType

class BuildingType(Enum):
    WALL = "wall"
    DOOR = "door"
    FLOOR = "floor"
    ROOF = "roof"
    FIRE = "fire"

class Building:
    def __init__(self, x: int, y: int, building_type: BuildingType, health: int = 100):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.building_type = building_type
        self.health = health
        self.max_health = health
        self.is_destroyed = False
        
    def take_damage(self, damage: int):
        """Recibir daño"""
        self.health -= damage
        if self.health <= 0:
            self.is_destroyed = True
            
    def repair(self, amount: int = 20):
        """Reparar construcción"""
        self.health = min(self.max_health, self.health + amount)
        
    def draw(self, screen: pygame.Surface):
        """Dibujar construcción"""
        if self.is_destroyed:
            return
            
        # Color según el tipo de construcción
        if self.building_type == BuildingType.WALL:
            color = (139, 69, 19)  # Marrón
        elif self.building_type == BuildingType.DOOR:
            color = (101, 67, 33)  # Marrón oscuro
        elif self.building_type == BuildingType.FLOOR:
            color = (160, 82, 45)  # Marrón claro
        elif self.building_type == BuildingType.ROOF:
            color = (105, 105, 105)  # Gris
        elif self.building_type == BuildingType.FIRE:
            color = (255, 69, 0)  # Rojo fuego
        else:
            color = (128, 128, 128)  # Gris por defecto
            
        # Dibujar construcción
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
        # Dibujar borde según la salud
        if self.health > self.max_health * 0.7:
            border_color = (0, 255, 0)  # Verde
        elif self.health > self.max_health * 0.3:
            border_color = (255, 255, 0)  # Amarillo
        else:
            border_color = (255, 0, 0)  # Rojo
            
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 2)
        
        # Dibujar barra de salud
        health_width = int(self.width * (self.health / self.max_health))
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 8, health_width, 4))

class BuildingSystem:
    def __init__(self):
        self.buildings: List[Building] = []
        self.building_mode = False
        self.selected_building_type = BuildingType.WALL
        self.preview_x = 0
        self.preview_y = 0
        
    def toggle_building_mode(self):
        """Activar/desactivar modo construcción"""
        self.building_mode = not self.building_mode
        
    def set_building_type(self, building_type: BuildingType):
        """Establecer tipo de construcción"""
        self.selected_building_type = building_type
        
    def update_preview(self, x: int, y: int):
        """Actualizar posición de vista previa"""
        self.preview_x = x
        self.preview_y = y
        
    def can_build_at(self, x: int, y: int) -> bool:
        """Verificar si se puede construir en la posición"""
        # Verificar si hay otra construcción en la misma posición
        for building in self.buildings:
            if (abs(building.x - x) < 50 and abs(building.y - y) < 50 and 
                not building.is_destroyed):
                return False
        return True
        
    def build(self, x: int, y: int, building_type: BuildingType) -> bool:
        """Construir en la posición especificada"""
        if not self.can_build_at(x, y):
            return False
            
        # Crear nueva construcción
        new_building = Building(x, y, building_type)
        self.buildings.append(new_building)
        return True
        
    def get_building_at(self, x: int, y: int) -> Optional[Building]:
        """Obtener construcción en la posición"""
        for building in self.buildings:
            if (building.x <= x <= building.x + building.width and
                building.y <= y <= building.y + building.height and
                not building.is_destroyed):
                return building
        return None
        
    def damage_buildings(self, damage: int = 10):
        """Dañar todas las construcciones (por enemigos)"""
        for building in self.buildings:
            if not building.is_destroyed:
                building.take_damage(damage)
                
    def repair_building(self, building: Building, amount: int = 20):
        """Reparar construcción específica"""
        if not building.is_destroyed:
            building.repair(amount)
            
    def get_shelter_protection(self, player_x: int, player_y: int) -> float:
        """Calcular protección del refugio para el jugador"""
        protection = 0.0
        for building in self.buildings:
            if building.is_destroyed:
                continue
                
            # Calcular distancia al jugador
            distance = math.sqrt((building.x - player_x)**2 + (building.y - player_y)**2)
            
            # Si está cerca del refugio, obtener protección
            if distance < 100:  # Radio de protección
                if building.building_type == BuildingType.WALL:
                    protection += 0.3
                elif building.building_type == BuildingType.DOOR:
                    protection += 0.2
                elif building.building_type == BuildingType.ROOF:
                    protection += 0.4
                    
        return min(1.0, protection)  # Máximo 100% de protección
        
    def draw(self, screen: pygame.Surface):
        """Dibujar todas las construcciones"""
        for building in self.buildings:
            building.draw(screen)
            
    def draw_preview(self, screen: pygame.Surface):
        """Dibujar vista previa de construcción"""
        if not self.building_mode:
            return
            
        # Color de vista previa
        if self.can_build_at(self.preview_x, self.preview_y):
            preview_color = (0, 255, 0, 128)  # Verde transparente
        else:
            preview_color = (255, 0, 0, 128)  # Rojo transparente
            
        # Crear superficie para vista previa
        preview_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        preview_surface.fill(preview_color)
        
        # Dibujar vista previa
        screen.blit(preview_surface, (self.preview_x, self.preview_y))

class BuildingUI:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_open = False
        self.selected_building = 0
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
    def toggle(self):
        """Abrir/cerrar menú de construcción"""
        self.is_open = not self.is_open
        
    def handle_input(self, event: pygame.event.Event, building_system: BuildingSystem) -> bool:
        """Manejar entrada del usuario en construcción"""
        if not self.is_open:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_building = max(0, self.selected_building - 1)
            elif event.key == pygame.K_DOWN:
                building_types = list(BuildingType)
                self.selected_building = min(len(building_types) - 1, self.selected_building + 1)
            elif event.key == pygame.K_RETURN:
                # Seleccionar tipo de construcción
                building_types = list(BuildingType)
                if 0 <= self.selected_building < len(building_types):
                    building_system.set_building_type(building_types[self.selected_building])
                    building_system.toggle_building_mode()
                    return True
            elif event.key == pygame.K_ESCAPE:
                self.is_open = False
                return "close"
                
        return False
        
    def draw(self, screen: pygame.Surface, building_system: BuildingSystem):
        """Dibujar interfaz de construcción"""
        if not self.is_open:
            return
            
        # Fondo semi-transparente
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Panel de construcción
        panel_width = 400
        panel_height = 300
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2
        
        pygame.draw.rect(screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (255, 255, 255), (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Título
        title = self.font.render("CONSTRUCCIÓN", True, (255, 255, 255))
        screen.blit(title, (panel_x + 20, panel_y + 20))
        
        # Tipos de construcción
        building_types = list(BuildingType)
        y_offset = panel_y + 60
        
        for i, building_type in enumerate(building_types):
            color = (100, 100, 255) if i == self.selected_building else (200, 200, 200)
            
            # Nombre del tipo de construcción
            building_name = building_type.value.title()
            text = self.font.render(building_name, True, color)
            screen.blit(text, (panel_x + 20, y_offset))
            
            # Descripción
            descriptions = {
                BuildingType.WALL: "Protección básica",
                BuildingType.DOOR: "Entrada al refugio",
                BuildingType.FLOOR: "Base sólida",
                BuildingType.ROOF: "Protección superior",
                BuildingType.FIRE: "Calor y luz"
            }
            
            desc_text = descriptions.get(building_type, "")
            desc_surface = self.small_font.render(desc_text, True, (150, 150, 150))
            screen.blit(desc_surface, (panel_x + 20, y_offset + 25))
            
            y_offset += 50
            
        # Controles
        controls = [
            "Flechas - Navegar",
            "ENTER - Seleccionar",
            "ESC - Cerrar"
        ]
        
        y_offset = panel_y + 20
        for control in controls:
            text = self.small_font.render(control, True, (200, 200, 200))
            screen.blit(text, (panel_x + 250, y_offset))
            y_offset += 20
