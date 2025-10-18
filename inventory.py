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
    
    # Construcción
    WALL = "wall"
    DOOR = "door"
    TORCH = "torch"
    FIRE = "fire"

class Item:
    def __init__(self, item_type: ItemType, quantity: int = 1, durability: int = 100):
        self.item_type = item_type
        self.quantity = quantity
        self.durability = durability
        self.max_durability = durability
        
    def use(self):
        """Usar el objeto (reduce durabilidad)"""
        if self.durability > 0:
            self.durability -= 10
            return True
        return False
        
    def is_broken(self):
        """Verificar si el objeto está roto"""
        return self.durability <= 0
        
    def repair(self, amount: int = 20):
        """Reparar el objeto"""
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
        recipes.append(Recipe(ItemType.AXE, {ItemType.WOOD: 2, ItemType.STONE: 1}))
        recipes.append(Recipe(ItemType.PICKAXE, {ItemType.WOOD: 2, ItemType.STONE: 2}))
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
        
    def handle_input(self, event: pygame.event.Event, inventory: Inventory, crafting_system: CraftingSystem) -> Optional[ItemType]:
        """Manejar entrada del usuario en el inventario"""
        if not self.is_open:
            return None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_slot = max(0, self.selected_slot - 1)
            elif event.key == pygame.K_RIGHT:
                self.selected_slot = min(len(inventory.items) - 1, self.selected_slot + 1)
            elif event.key == pygame.K_RETURN:
                # Usar item seleccionado
                if 0 <= self.selected_slot < len(inventory.items):
                    item = inventory.items[self.selected_slot]
                    if item.use():
                        if item.is_broken():
                            inventory.items.remove(item)
                        return item.item_type
            elif event.key == pygame.K_c:
                # Abrir menú de crafteo
                return "craft"
            elif event.key == pygame.K_ESCAPE:
                # Cerrar inventario
                self.is_open = False
                return "close"
                
        return None
        
    def draw(self, screen: pygame.Surface, inventory: Inventory, crafting_system: CraftingSystem):
        """Dibujar interfaz del inventario"""
        if not self.is_open:
            return
            
        # Fondo semi-transparente
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Panel del inventario
        panel_width = 600
        panel_height = 400
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2
        
        pygame.draw.rect(screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (255, 255, 255), (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Título
        title = self.font.render("INVENTARIO", True, (255, 255, 255))
        screen.blit(title, (panel_x + 20, panel_y + 20))
        
        # Items del inventario
        y_offset = panel_y + 60
        for i, item in enumerate(inventory.items):
            color = (100, 100, 255) if i == self.selected_slot else (200, 200, 200)
            
            # Nombre del item
            item_name = f"{item.item_type.value.title()} x{item.quantity}"
            text = self.font.render(item_name, True, color)
            screen.blit(text, (panel_x + 20, y_offset))
            
            # Durabilidad si aplica
            if item.durability < item.max_durability:
                durability_text = f"Durabilidad: {item.durability}/{item.max_durability}"
                durability_color = (255, 255, 0) if item.durability > 50 else (255, 0, 0)
                durability_surface = self.small_font.render(durability_text, True, durability_color)
                screen.blit(durability_surface, (panel_x + 20, y_offset + 25))
                
            y_offset += 50
            
        # Información de controles
        controls = [
            "Controles:",
            "Flechas - Navegar",
            "ENTER - Usar item",
            "C - Crafteo",
            "I - Cerrar inventario"
        ]
        
        y_offset = panel_y + 20
        for control in controls:
            text = self.small_font.render(control, True, (200, 200, 200))
            screen.blit(text, (panel_x + 300, y_offset))
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
        
    def draw(self, screen: pygame.Surface, inventory: Inventory, crafting_system: CraftingSystem):
        """Dibujar interfaz de crafteo"""
        if not self.is_open:
            return
            
        # Fondo semi-transparente
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # Panel de crafteo
        panel_width = 500
        panel_height = 300
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2
        
        pygame.draw.rect(screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (255, 255, 255), (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Título
        title = self.font.render("CRAFTEO", True, (255, 255, 255))
        screen.blit(title, (panel_x + 20, panel_y + 20))
        
        # Recetas disponibles
        available_recipes = crafting_system.get_available_recipes(inventory)
        
        if available_recipes:
            y_offset = panel_y + 60
            for i, recipe in enumerate(available_recipes):
                color = (100, 100, 255) if i == self.selected_recipe else (200, 200, 200)
                
                # Nombre del resultado
                result_name = recipe.result.value.title()
                text = self.font.render(result_name, True, color)
                screen.blit(text, (panel_x + 20, y_offset))
                
                # Materiales requeridos
                materials_text = "Materiales: "
                for material, quantity in recipe.materials.items():
                    materials_text += f"{material.value.title()}({quantity}) "
                    
                materials_surface = self.small_font.render(materials_text, True, (150, 150, 150))
                screen.blit(materials_surface, (panel_x + 20, y_offset + 25))
                
                y_offset += 60
        else:
            no_recipes = self.font.render("No hay recetas disponibles", True, (255, 0, 0))
            screen.blit(no_recipes, (panel_x + 20, panel_y + 60))
            
        # Controles
        controls = [
            "Flechas - Navegar",
            "ENTER - Craftear",
            "ESC - Cerrar"
        ]
        
        y_offset = panel_y + 20
        for control in controls:
            text = self.small_font.render(control, True, (200, 200, 200))
            screen.blit(text, (panel_x + 300, y_offset))
            y_offset += 20
