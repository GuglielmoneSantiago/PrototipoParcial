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
        
    def draw(self, screen: pygame.Surface, building_system: BuildingSystem, scroll_offset: int = 0):
        """Dibujar interfaz de construcción"""
        if not self.is_open:
            return
            
        # Fondo semi-transparente
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Panel de construcción con caja
        panel_width = 600
        panel_height = 500
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2
        
        # Dibujar fondo de la caja
        pygame.draw.rect(screen, (30, 30, 30), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (255, 255, 255), (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Título
        title = self.font.render("CONSTRUCCIÓN", True, (255, 255, 255))
        screen.blit(title, (panel_x + 20, panel_y + 20))
        
        # Tipos de construcción
        building_types = list(BuildingType)
        
        # Crear superficie para el contenido scrolleable
        content_height = len(building_types) * 60 + 100
        scroll_surface = pygame.Surface((panel_width - 40, content_height))
        scroll_surface.fill((30, 30, 30))
        
        # Dibujar tipos de construcción en la superficie de scroll
        y_offset = 20
        for i, building_type in enumerate(building_types):
            color = (100, 100, 255) if i == self.selected_building else (200, 200, 200)
            
            # Nombre del tipo de construcción
            building_name = building_type.value.title()
            text = self.font.render(building_name, True, color)
            text_rect = text.get_rect(center=(scroll_surface.get_width()//2, y_offset))
            scroll_surface.blit(text, text_rect)
            
            # Descripción
            descriptions = {
                BuildingType.WALL: "Protección básica contra enemigos",
                BuildingType.DOOR: "Entrada segura al refugio",
                BuildingType.FLOOR: "Base sólida para construcción",
                BuildingType.ROOF: "Protección superior contra elementos",
                BuildingType.FIRE: "Fuente de calor y luz"
            }
            
            desc_text = descriptions.get(building_type, "")
            desc_surface = self.small_font.render(desc_text, True, (150, 150, 150))
            desc_rect = desc_surface.get_rect(center=(scroll_surface.get_width()//2, y_offset + 25))
            scroll_surface.blit(desc_surface, desc_rect)
            
            y_offset += 60
        
        # Aplicar scroll y dibujar contenido visible
        visible_height = panel_height - 100
        scroll_y = max(0, min(scroll_offset, content_height - visible_height))
        
        # Dibujar la parte visible del contenido
        screen.blit(scroll_surface, (panel_x + 20, panel_y + 60), 
                   (0, scroll_y, panel_width - 40, visible_height))
        
        # Dibujar indicadores de scroll si es necesario
        if content_height > visible_height:
            # Barra de scroll
            scroll_bar_width = 10
            scroll_bar_height = int((visible_height / content_height) * visible_height)
            scroll_bar_y = panel_y + 60 + int((scroll_y / (content_height - visible_height)) * (visible_height - scroll_bar_height))
            
            pygame.draw.rect(screen, (100, 100, 100), 
                           (panel_x + panel_width - 25, panel_y + 60, scroll_bar_width, visible_height))
            pygame.draw.rect(screen, (255, 255, 255), 
                           (panel_x + panel_width - 25, scroll_bar_y, scroll_bar_width, scroll_bar_height))
            
        # Controles
        controls = [
            "Flechas - Navegar",
            "ENTER - Seleccionar",
            "ESC - Cerrar"
        ]
        
        y_offset = panel_y + panel_height - 80
        for control in controls:
            text = self.small_font.render(control, True, (200, 200, 200))
            screen.blit(text, (panel_x + 20, y_offset))
            y_offset += 20
