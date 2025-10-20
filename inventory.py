#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Inventario y Crafteo
Para el videojuego de Supervivencia Nocturna
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
import pygame

class ItemType(Enum):
    # Materiales básicos
    WOOD = "wood"
    STONE = "stone"
    GRASS = "grass"
    BONE = "bone"
    
    # Herramientas
    AXE = "axe"
    PICKAXE = "pickaxe"
    KNIFE = "knife"
    
    # Armas
    SPEAR = "spear"
    BOW = "bow"
    ARROW = "arrow"
    
    # Consumibles
    FOOD = "food"
    WATER = "water"
    MEDICINE = "medicine"
    MEAT = "meat"  # Carne de enemigos
    
    # Construcción
    WALL = "wall"
    DOOR = "door"
    TORCH = "torch"
    FIRE = "fire"

class Item:
    def __init__(self, item_type: ItemType, quantity: int = 1, durability: int = 100):
        self.item_type = item_type
        self.quantity = quantity
        
        # Solo las armas y herramientas tienen durabilidad
        if self.is_weapon_or_tool():
            self.durability = durability
            self.max_durability = durability
        else:
            self.durability = None
            self.max_durability = None
        
    def is_weapon_or_tool(self) -> bool:
        """Verificar si el item es un arma o herramienta"""
        weapons_and_tools = [
            ItemType.SPEAR, ItemType.BOW, ItemType.AXE, 
            ItemType.PICKAXE, ItemType.KNIFE
        ]
        return self.item_type in weapons_and_tools
        
    def use(self):
        """Usar el objeto (reduce durabilidad solo si es arma/herramienta)"""
        if self.is_weapon_or_tool():
            if self.durability and self.durability > 0:
                self.durability -= 10
                return True
            return False
        else:
            # Para consumibles y otros items, solo reducir cantidad
            if self.quantity > 0:
                self.quantity -= 1
                return True
            return False
        
    def is_broken(self):
        """Verificar si el objeto está roto (solo para armas/herramientas)"""
        if self.is_weapon_or_tool():
            return self.durability is not None and self.durability <= 0
        return False
        
    def repair(self, amount: int = 20):
        """Reparar el objeto (solo para armas/herramientas)"""
        if self.is_weapon_or_tool() and self.durability is not None:
            self.durability = min(self.max_durability, self.durability + amount)

class Recipe:
    def __init__(self, result: ItemType, materials: Dict[ItemType, int], tool_required: Optional[ItemType] = None):
        self.result = result
        self.materials = materials
        self.tool_required = tool_required
        
    def can_craft(self, inventory: 'Inventory') -> bool:
        """Verificar si se puede craftear con el inventario actual"""
        # Verificar materiales
        for material, quantity in self.materials.items():
            if not inventory.has_item(material, quantity):
                return False
                
        # Verificar herramienta requerida
        if self.tool_required and not inventory.has_tool(self.tool_required):
            return False
            
        return True

class Inventory:
    def __init__(self, max_size: int = 20):
        self.items: List[Item] = []
        self.max_size = max_size
        
    def add_item(self, item_type: ItemType, quantity: int = 1) -> bool:
        """Agregar item al inventario"""
        if len(self.items) >= self.max_size:
            return False
            
        # Buscar si ya existe el item
        for item in self.items:
            if item.item_type == item_type:
                item.quantity += quantity
                return True
                
        # Crear nuevo item
        self.items.append(Item(item_type, quantity))
        return True
        
    def remove_item(self, item_type: ItemType, quantity: int = 1) -> bool:
        """Remover item del inventario"""
        for item in self.items:
            if item.item_type == item_type:
                if item.quantity >= quantity:
                    item.quantity -= quantity
                    if item.quantity <= 0:
                        self.items.remove(item)
                    return True
        return False
        
    def has_item(self, item_type: ItemType, quantity: int = 1) -> bool:
        """Verificar si tiene suficiente cantidad de un item"""
        for item in self.items:
            if item.item_type == item_type and item.quantity >= quantity:
                return True
        return False
        
    def has_tool(self, tool_type: ItemType) -> bool:
        """Verificar si tiene una herramienta específica no rota"""
        for item in self.items:
            if item.item_type == tool_type and not item.is_broken():
                return True
        return False
        
    def get_item_count(self, item_type: ItemType) -> int:
        """Obtener cantidad de un item específico"""
        for item in self.items:
            if item.item_type == item_type:
                return item.quantity
        return 0
        
    def get_total_items(self) -> int:
        """Obtener total de items en el inventario"""
        return sum(item.quantity for item in self.items)

class CraftingSystem:
    def __init__(self):
        self.recipes = self._initialize_recipes()
        
    def _initialize_recipes(self) -> List[Recipe]:
        """Inicializar todas las recetas de crafteo"""
        recipes = []
        
        # Herramientas básicas
        recipes.append(Recipe(ItemType.AXE, {ItemType.WOOD: 10}))
        recipes.append(Recipe(ItemType.PICKAXE, {ItemType.WOOD: 10}))
        recipes.append(Recipe(ItemType.KNIFE, {ItemType.WOOD: 1, ItemType.STONE: 1}))
        
        # Armas
        recipes.append(Recipe(ItemType.SPEAR, {ItemType.WOOD: 3, ItemType.STONE: 1}))
        recipes.append(Recipe(ItemType.BOW, {ItemType.WOOD: 3, ItemType.GRASS: 2}))
        recipes.append(Recipe(ItemType.ARROW, {ItemType.WOOD: 1, ItemType.STONE: 1}))
        
        # Construcción
        recipes.append(Recipe(ItemType.WALL, {ItemType.WOOD: 4, ItemType.STONE: 2}))
        recipes.append(Recipe(ItemType.DOOR, {ItemType.WOOD: 3}))
        recipes.append(Recipe(ItemType.TORCH, {ItemType.WOOD: 1, ItemType.GRASS: 2}))
        
        # Consumibles
        recipes.append(Recipe(ItemType.FOOD, {ItemType.GRASS: 3}))
        recipes.append(Recipe(ItemType.MEDICINE, {ItemType.GRASS: 5, ItemType.BONE: 1}))
        
        return recipes
        
    def get_available_recipes(self, inventory: Inventory) -> List[Recipe]:
        """Obtener recetas que se pueden craftear"""
        available = []
        for recipe in self.recipes:
            if recipe.can_craft(inventory):
                available.append(recipe)
        return available
        
    def craft_item(self, recipe: Recipe, inventory: Inventory) -> bool:
        """Craftear un item usando una receta"""
        if not recipe.can_craft(inventory):
            return False
            
        # Remover materiales
        for material, quantity in recipe.materials.items():
            inventory.remove_item(material, quantity)
            
        # Agregar resultado
        return inventory.add_item(recipe.result, 1)

class InventoryUI:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_open = False
        self.selected_slot = 0
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
    def toggle(self):
        """Abrir/cerrar inventario"""
        self.is_open = not self.is_open
        
    def handle_input(self, event: pygame.event.Event, inventory: Inventory, crafting_system: CraftingSystem) -> Optional[str]:
        """Manejar entrada del usuario en el inventario"""
        if not self.is_open:
            return None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_slot = max(0, self.selected_slot - 1)
            elif event.key == pygame.K_RIGHT:
                self.selected_slot = min(len(inventory.items) - 1, self.selected_slot + 1)
            elif event.key == pygame.K_RETURN:
                # Equipar item seleccionado
                if 0 <= self.selected_slot < len(inventory.items):
                    item = inventory.items[self.selected_slot]
                    
                    # Verificar si es un arma o herramienta equipable
                    if self.is_weapon(item.item_type):
                        return f"equip_weapon:{item.item_type.value}"
                    elif self.is_tool(item.item_type):
                        return f"equip_tool:{item.item_type.value}"
                    else:
                        # Para otros items, usar normalmente
                        if item.use():
                            if item.is_broken():
                                inventory.items.remove(item)
                            return f"use:{item.item_type.value}"
            elif event.key == pygame.K_c:
                # Abrir menú de crafteo
                return "craft"
            elif event.key == pygame.K_ESCAPE:
                # Cerrar inventario
                self.is_open = False
                return "close"
                
        return None
        
    def is_weapon(self, item_type: ItemType) -> bool:
        """Verificar si un item es un arma"""
        weapons = [ItemType.SPEAR, ItemType.BOW]
        return item_type in weapons
        
    def is_tool(self, item_type: ItemType) -> bool:
        """Verificar si un item es una herramienta"""
        tools = [ItemType.AXE, ItemType.PICKAXE, ItemType.KNIFE]
        return item_type in tools
        
    def draw(self, screen: pygame.Surface, inventory: Inventory, crafting_system: CraftingSystem, scroll_offset: int = 0):
        """Dibujar interfaz del inventario"""
        if not self.is_open:
            return
            
        # Fondo semi-transparente
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Panel del inventario con caja
        panel_width = 600
        panel_height = 500
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2
        
        # Dibujar fondo de la caja
        pygame.draw.rect(screen, (30, 30, 30), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (255, 255, 255), (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Título
        title = self.font.render("INVENTARIO", True, (255, 255, 255))
        screen.blit(title, (panel_x + 20, panel_y + 20))
        
        # Crear superficie para el contenido scrolleable
        content_height = len(inventory.items) * 50 + 100
        scroll_surface = pygame.Surface((panel_width - 40, content_height))
        scroll_surface.fill((30, 30, 30))
        
        # Dibujar items en la superficie de scroll
        y_offset = 20
        for i, item in enumerate(inventory.items):
            color = (100, 100, 255) if i == self.selected_slot else (200, 200, 200)
            
            # Nombre del item
            item_name = f"{item.item_type.value.title()} x{item.quantity}"
            text = self.font.render(item_name, True, color)
            text_rect = text.get_rect(center=(scroll_surface.get_width()//2, y_offset))
            scroll_surface.blit(text, text_rect)
            
            # Durabilidad si aplica (solo para armas y herramientas)
            if item.is_weapon_or_tool() and item.durability is not None and item.durability < item.max_durability:
                durability_text = f"Durabilidad: {item.durability}/{item.max_durability}"
                durability_color = (255, 255, 0) if item.durability > 50 else (255, 0, 0)
                durability_surface = self.small_font.render(durability_text, True, durability_color)
                durability_rect = durability_surface.get_rect(center=(scroll_surface.get_width()//2, y_offset + 25))
                scroll_surface.blit(durability_surface, durability_rect)
                
            y_offset += 50
        
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
        
        # Información de controles
        controls = [
            "Flechas - Navegar",
            "ENTER - Usar item",
            "C - Crafteo",
            "I - Cerrar inventario"
        ]
        
        y_offset = panel_y + panel_height - 80
        for control in controls:
            text = self.small_font.render(control, True, (200, 200, 200))
            screen.blit(text, (panel_x + 20, y_offset))
            y_offset += 20

class CraftingUI:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_open = False
        self.selected_recipe = 0
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
    def toggle(self):
        """Abrir/cerrar menú de crafteo"""
        self.is_open = not self.is_open
        
    def handle_input(self, event: pygame.event.Event, inventory: Inventory, crafting_system: CraftingSystem) -> bool:
        """Manejar entrada del usuario en el crafteo"""
        if not self.is_open:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_recipe = max(0, self.selected_recipe - 1)
            elif event.key == pygame.K_DOWN:
                available_recipes = crafting_system.get_available_recipes(inventory)
                self.selected_recipe = min(len(available_recipes) - 1, self.selected_recipe + 1)
            elif event.key == pygame.K_RETURN:
                # Craftear receta seleccionada
                available_recipes = crafting_system.get_available_recipes(inventory)
                if 0 <= self.selected_recipe < len(available_recipes):
                    recipe = available_recipes[self.selected_recipe]
                    return crafting_system.craft_item(recipe, inventory)
            elif event.key == pygame.K_ESCAPE:
                self.is_open = False
                return "close"
                
        return False
        
    def draw(self, screen: pygame.Surface, inventory: Inventory, crafting_system: CraftingSystem, scroll_offset: int = 0):
        """Dibujar interfaz de crafteo"""
        if not self.is_open:
            return
            
        # Fondo semi-transparente
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Panel de crafteo con caja
        panel_width = 600
        panel_height = 500
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2
        
        # Dibujar fondo de la caja
        pygame.draw.rect(screen, (30, 30, 30), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (255, 255, 255), (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Título
        title = self.font.render("CRAFTEO", True, (255, 255, 255))
        screen.blit(title, (panel_x + 20, panel_y + 20))
        
        # Recetas disponibles
        available_recipes = crafting_system.get_available_recipes(inventory)
        
        if available_recipes:
            # Crear superficie para el contenido scrolleable
            content_height = len(available_recipes) * 80 + 100
            scroll_surface = pygame.Surface((panel_width - 40, content_height))
            scroll_surface.fill((30, 30, 30))
            
            # Dibujar recetas en la superficie de scroll
            y_offset = 20
            for i, recipe in enumerate(available_recipes):
                color = (100, 100, 255) if i == self.selected_recipe else (200, 200, 200)
                
                # Nombre del resultado
                result_name = recipe.result.value.title()
                text = self.font.render(result_name, True, color)
                text_rect = text.get_rect(center=(scroll_surface.get_width()//2, y_offset))
                scroll_surface.blit(text, text_rect)
                
                # Materiales requeridos
                materials_text = "Materiales: "
                for material, quantity in recipe.materials.items():
                    materials_text += f"{material.value.title()}({quantity}) "
                    
                materials_surface = self.small_font.render(materials_text, True, (150, 150, 150))
                materials_rect = materials_surface.get_rect(center=(scroll_surface.get_width()//2, y_offset + 30))
                scroll_surface.blit(materials_surface, materials_rect)
                
                y_offset += 80
            
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
        else:
            no_recipes = self.font.render("No hay recetas disponibles", True, (255, 0, 0))
            no_recipes_rect = no_recipes.get_rect(center=(panel_x + panel_width//2, panel_y + panel_height//2))
            screen.blit(no_recipes, no_recipes_rect)
            
        # Controles
        controls = [
            "Flechas - Navegar",
            "ENTER - Craftear",
            "ESC - Cerrar"
        ]
        
        y_offset = panel_y + panel_height - 80
        for control in controls:
            text = self.small_font.render(control, True, (200, 200, 200))
            screen.blit(text, (panel_x + 20, y_offset))
            y_offset += 20
