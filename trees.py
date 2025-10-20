#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Árboles para el Videojuego de Supervivencia Nocturna
Permite farmear madera de los árboles
"""

import pygame
import random
import math
from typing import List, Tuple, Optional
from inventory import ItemType

class Tree:
    def __init__(self, x: int, y: int, tree_type: str = "oak"):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.tree_type = tree_type
        self.wood_amount = random.randint(4, 6)  # Cantidad de madera disponible
        self.max_wood = self.wood_amount
        self.is_chopped = False
        self.regrowth_timer = 0
        self.regrowth_time = 6000  # 100 segundos para regenerar (a 60 FPS)
        
        # Diferentes tipos de árboles
        self.tree_colors = {
            "oak": (34, 139, 34),      # Verde bosque
            "pine": (0, 100, 0),       # Verde oscuro
            "birch": (245, 245, 220),     # Blanco hueso
            "cherry": (255, 20, 147)    # Rosa profundo
        }
        
        self.trunk_colors = {
            "oak": (139, 69, 19),      # Marrón
            "pine": (101, 67, 33),     # Marrón oscuro
            "birch": (255, 255, 255),  # Blanco
            "cherry": (160, 82, 45)     # Marrón claro
        }
        
    def can_harvest(self) -> bool:
        """Verificar si el árbol puede ser farmeado"""
        return not self.is_chopped and self.wood_amount > 0
        
    def harvest(self, player_inventory) -> int:
        """Farmear madera del árbol"""
        if not self.can_harvest():
            return 0
            
        # Calcular cuánta madera se puede obtener (1-2 por click)
        harvest_amount = min(random.randint(1, 2), self.wood_amount)
        
        # Agregar madera al inventario
        if player_inventory.add_item(ItemType.WOOD, harvest_amount):
            self.wood_amount -= harvest_amount
            if self.wood_amount <= 0:
                self.is_chopped = True
                self.regrowth_timer = 0
                # El árbol desaparece completamente cuando se farmea todo
                print(f"¡Árbol completamente farmeado! (+{harvest_amount} madera)")
                return harvest_amount
            return harvest_amount
        else:
            return 0
            
    def update(self):
        """Actualizar estado del árbol"""
        if self.is_chopped:
            self.regrowth_timer += 1
            if self.regrowth_timer >= self.regrowth_time:
                # Regenerar el árbol
                self.is_chopped = False
                self.wood_amount = self.max_wood
                self.regrowth_timer = 0
                
    def draw(self, screen: pygame.Surface):
        """Dibujar el árbol"""
        if self.is_chopped:
            # El árbol desaparece completamente cuando se farmea todo
            return
            
        # Color del árbol según el tipo
        tree_color = self.tree_colors.get(self.tree_type, (34, 139, 34))
        trunk_color = self.trunk_colors.get(self.tree_type, (139, 69, 19))
        
        # Dibujar tronco
        pygame.draw.rect(screen, trunk_color, (self.x + 15, self.y + 30, 10, 30))
        
        # Dibujar copa del árbol
        pygame.draw.circle(screen, tree_color, (self.x + 20, self.y + 25), 15)
        pygame.draw.circle(screen, tree_color, (self.x + 15, self.y + 20), 12)
        pygame.draw.circle(screen, tree_color, (self.x + 25, self.y + 20), 12)
        
        # Indicador de madera disponible
        if self.wood_amount > 0:
            # Dibujar barra de madera disponible
            bar_width = int(30 * (self.wood_amount / self.max_wood))
            pygame.draw.rect(screen, (139, 69, 19), (self.x + 5, self.y - 10, bar_width, 4))
            pygame.draw.rect(screen, (255, 255, 255), (self.x + 5, self.y - 10, 30, 4), 1)
            
    def get_rect(self) -> pygame.Rect:
        """Obtener rectángulo de colisión del árbol"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def is_near_player(self, player_x: int, player_y: int, player_width: int, player_height: int) -> bool:
        """Verificar si el jugador está cerca del árbol"""
        tree_rect = self.get_rect()
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        
        # Expandir el área de interacción
        interaction_distance = 50
        expanded_tree_rect = tree_rect.inflate(interaction_distance, interaction_distance)
        
        return expanded_tree_rect.colliderect(player_rect)

class TreeManager:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.trees: List[Tree] = []
        self.max_trees = 7
        
    def spawn_trees(self):
        """Generar árboles en el mapa"""
        if len(self.trees) < self.max_trees:
            if random.random() < 0.01:  # 1% de probabilidad por frame
                # Posición aleatoria
                x = random.randint(50, self.screen_width - 50)
                y = random.randint(50, self.screen_height - 50)
                
                # Verificar que no esté muy cerca de otros árboles
                too_close = False
                for tree in self.trees:
                    distance = math.sqrt((tree.x - x)**2 + (tree.y - y)**2)
                    if distance < 80:  # Mínimo 80 píxeles de separación
                        too_close = True
                        break
                        
                if not too_close:
                    tree_type = random.choice(["oak", "pine", "birch", "cherry"])
                    self.trees.append(Tree(x, y, tree_type))
                    
    def get_nearby_trees(self, player_x: int, player_y: int, player_width: int, player_height: int) -> List[Tree]:
        """Obtener árboles cerca del jugador que se pueden farmear"""
        nearby_trees = []
        for tree in self.trees:
            if tree.is_near_player(player_x, player_y, player_width, player_height) and tree.can_harvest():
                nearby_trees.append(tree)
        return nearby_trees
        
    def harvest_nearby_trees(self, player_x: int, player_y: int, player_width: int, player_height: int, player_inventory) -> int:
        """Farmear árboles cerca del jugador"""
        nearby_trees = self.get_nearby_trees(player_x, player_y, player_width, player_height)
        total_harvested = 0
        
        for tree in nearby_trees:
            if tree.can_harvest():
                harvested = tree.harvest(player_inventory)
                total_harvested += harvested
                
        return total_harvested
        
    def update(self):
        """Actualizar todos los árboles"""
        for tree in self.trees[:]:  # Usar slice para evitar problemas al modificar la lista
            tree.update()
            
        # Generar nuevos árboles ocasionalmente
        self.spawn_trees()
        
    def draw(self, screen: pygame.Surface):
        """Dibujar todos los árboles"""
        for tree in self.trees:
            tree.draw(screen)
            
    def draw_interaction_hint(self, screen: pygame.Surface, player_x: int, player_y: int, player_width: int, player_height: int):
        """Dibujar indicador de interacción con árboles"""
        nearby_trees = self.get_nearby_trees(player_x, player_y, player_width, player_height)
        
        for tree in nearby_trees:
            # Dibujar indicador visual
            hint_x = tree.x + tree.width // 2
            hint_y = tree.y - 20
            
            # Texto "F para farmear"
            font = pygame.font.Font(None, 20)
            text = font.render("F para farmear", True, (255, 255, 255))
            text_rect = text.get_rect(center=(hint_x, hint_y))
            
            # Fondo del texto
            bg_rect = text_rect.inflate(10, 5)
            pygame.draw.rect(screen, (0, 0, 0, 128), bg_rect)
            pygame.draw.rect(screen, (255, 255, 255), bg_rect, 1)
            
            screen.blit(text, text_rect)
