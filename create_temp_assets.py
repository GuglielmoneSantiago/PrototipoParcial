#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear assets temporales del videojuego
Crea imágenes y sonidos básicos para testing
"""

import pygame
import os
import random

def create_temp_assets():
    """Crear assets temporales para testing"""
    
    # Crear directorios si no existen
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/sounds", exist_ok=True)
    
    # Crear imágenes temporales
    create_temp_images()
    print("Assets temporales creados en assets/")
    print("Puedes reemplazar estos archivos con tus propias imágenes y sonidos")

def create_temp_images():
    """Crear imágenes temporales básicas"""
    
    # Personaje
    create_player_images()
    
    # Fondos
    create_background_images()
    
    # Enemigos
    create_enemy_images()
    
    # Construcciones
    create_building_images()
    
    # Items
    create_item_images()

def create_player_images():
    """Crear imágenes del personaje basadas en la referencia"""
    
    # Player Idle - Personaje en reposo
    surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    # Cabeza (cuadrada, piel rosada)
    pygame.draw.rect(surface, (255, 200, 150), (12, 4, 8, 8))  # Cabeza
    
    # Cabello (marrón oscuro)
    pygame.draw.rect(surface, (101, 67, 33), (10, 2, 12, 6))  # Cabello principal
    pygame.draw.rect(surface, (101, 67, 33), (8, 4, 2, 4))    # Oreja izquierda
    pygame.draw.rect(surface, (101, 67, 33), (22, 4, 2, 4))  # Oreja derecha
    
    # Sonrisa (blanca)
    pygame.draw.rect(surface, (255, 255, 255), (13, 8, 6, 2))  # Sonrisa
    
    # Cuello/corbata (marrón)
    pygame.draw.rect(surface, (101, 67, 33), (14, 12, 4, 2))  # Cuello
    
    # Torso (azul brillante)
    pygame.draw.rect(surface, (0, 100, 255), (10, 14, 12, 8))  # Camisa/chaqueta
    
    # Brazos (azul, en reposo a los lados)
    pygame.draw.rect(surface, (0, 100, 255), (6, 16, 4, 4))   # Brazo izquierdo
    pygame.draw.rect(surface, (0, 100, 255), (22, 16, 4, 4))  # Brazo derecho
    
    # Manos (piel rosada)
    pygame.draw.rect(surface, (255, 200, 150), (4, 18, 2, 2))  # Mano izquierda
    pygame.draw.rect(surface, (255, 200, 150), (26, 18, 2, 2)) # Mano derecha
    
    # Piernas (marrón oscuro)
    pygame.draw.rect(surface, (101, 67, 33), (12, 22, 4, 6))  # Pierna izquierda
    pygame.draw.rect(surface, (101, 67, 33), (16, 22, 4, 6))  # Pierna derecha
    
    # Pies (marrón oscuro)
    pygame.draw.rect(surface, (101, 67, 33), (10, 28, 3, 2))  # Pie izquierdo
    pygame.draw.rect(surface, (101, 67, 33), (19, 28, 3, 2))  # Pie derecho
    
    pygame.image.save(surface, "assets/images/player_idle.png")
    
    # Player Walk - Personaje caminando (brazos balanceándose)
    surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    # Cabeza (cuadrada, piel rosada)
    pygame.draw.rect(surface, (255, 200, 150), (12, 4, 8, 8))  # Cabeza
    
    # Cabello (marrón oscuro)
    pygame.draw.rect(surface, (101, 67, 33), (10, 2, 12, 6))  # Cabello principal
    pygame.draw.rect(surface, (101, 67, 33), (8, 4, 2, 4))    # Oreja izquierda
    pygame.draw.rect(surface, (101, 67, 33), (22, 4, 2, 4))  # Oreja derecha
    
    # Sonrisa (blanca)
    pygame.draw.rect(surface, (255, 255, 255), (13, 8, 6, 2))  # Sonrisa
    
    # Cuello/corbata (marrón)
    pygame.draw.rect(surface, (101, 67, 33), (14, 12, 4, 2))  # Cuello
    
    # Torso (azul brillante)
    pygame.draw.rect(surface, (0, 100, 255), (10, 14, 12, 8))  # Camisa/chaqueta
    
    # Brazos balanceándose (uno arriba, uno abajo)
    pygame.draw.rect(surface, (0, 100, 255), (6, 14, 4, 6))   # Brazo izquierdo (arriba)
    pygame.draw.rect(surface, (0, 100, 255), (22, 18, 4, 6))  # Brazo derecho (abajo)
    
    # Manos (piel rosada)
    pygame.draw.rect(surface, (255, 200, 150), (4, 12, 2, 2))  # Mano izquierda (arriba)
    pygame.draw.rect(surface, (255, 200, 150), (26, 22, 2, 2))  # Mano derecha (abajo)
    
    # Piernas en movimiento (una adelante, una atrás)
    pygame.draw.rect(surface, (101, 67, 33), (10, 22, 4, 6))  # Pierna izquierda (adelante)
    pygame.draw.rect(surface, (101, 67, 33), (18, 22, 4, 6))  # Pierna derecha (atrás)
    
    # Pies (marrón oscuro)
    pygame.draw.rect(surface, (101, 67, 33), (8, 28, 3, 2))   # Pie izquierdo (adelante)
    pygame.draw.rect(surface, (101, 67, 33), (21, 28, 3, 2))  # Pie derecho (atrás)
    
    pygame.image.save(surface, "assets/images/player_walk.png")
    
    # Player Run - Personaje corriendo (brazos más arriba, piernas más separadas)
    surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    # Cabeza (cuadrada, piel rosada)
    pygame.draw.rect(surface, (255, 200, 150), (12, 4, 8, 8))  # Cabeza
    
    # Cabello (marrón oscuro)
    pygame.draw.rect(surface, (101, 67, 33), (10, 2, 12, 6))  # Cabello principal
    pygame.draw.rect(surface, (101, 67, 33), (8, 4, 2, 4))    # Oreja izquierda
    pygame.draw.rect(surface, (101, 67, 33), (22, 4, 2, 4))  # Oreja derecha
    
    # Sonrisa (blanca)
    pygame.draw.rect(surface, (255, 255, 255), (13, 8, 6, 2))  # Sonrisa
    
    # Cuello/corbata (marrón)
    pygame.draw.rect(surface, (101, 67, 33), (14, 12, 4, 2))  # Cuello
    
    # Torso (azul brillante)
    pygame.draw.rect(surface, (0, 100, 255), (10, 14, 12, 8))  # Camisa/chaqueta
    
    # Brazos corriendo (ambos arriba)
    pygame.draw.rect(surface, (0, 100, 255), (6, 12, 4, 8))   # Brazo izquierdo (arriba)
    pygame.draw.rect(surface, (0, 100, 255), (22, 12, 4, 8))  # Brazo derecho (arriba)
    
    # Manos (piel rosada)
    pygame.draw.rect(surface, (255, 200, 150), (4, 10, 2, 2))  # Mano izquierda (arriba)
    pygame.draw.rect(surface, (255, 200, 150), (26, 10, 2, 2)) # Mano derecha (arriba)
    
    # Piernas corriendo (más separadas)
    pygame.draw.rect(surface, (101, 67, 33), (8, 22, 4, 6))   # Pierna izquierda
    pygame.draw.rect(surface, (101, 67, 33), (20, 22, 4, 6))  # Pierna derecha
    
    # Pies (marrón oscuro)
    pygame.draw.rect(surface, (101, 67, 33), (6, 28, 3, 2))   # Pie izquierdo
    pygame.draw.rect(surface, (101, 67, 33), (23, 28, 3, 2)) # Pie derecho
    
    pygame.image.save(surface, "assets/images/player_run.png")

def create_background_images():
    """Crear fondos temporales - todo suelo sin cielo"""
    
    # Día - Campo verde brillante en toda la pantalla
    surface = pygame.Surface((1200, 800), pygame.SRCALPHA)
    surface.fill((144, 238, 144))  # Verde claro base
    
    # Crear patrón de hierba en toda la pantalla
    for y in range(0, 800, 2):
        for x in range(0, 1200, 2):
            if random.random() < 0.4:  # 40% de probabilidad de hierba verde clara
                pygame.draw.rect(surface, (144, 238, 144), (x, y, 2, 2))
            elif random.random() < 0.2:  # 20% de probabilidad de hierba verde oscura
                pygame.draw.rect(surface, (34, 139, 34), (x, y, 2, 2))
            elif random.random() < 0.1:  # 10% de probabilidad de tierra marrón
                pygame.draw.rect(surface, (139, 69, 19), (x, y, 2, 2))
    
    # Agregar flores rojas dispersas por toda la pantalla
    for _ in range(80):
        x = random.randint(0, 1200)
        y = random.randint(0, 800)
        # Flor roja con centro amarillo
        pygame.draw.rect(surface, (255, 0, 0), (x, y, 2, 2))
        pygame.draw.rect(surface, (255, 255, 0), (x+1, y+1, 1, 1))
    
    pygame.image.save(surface, "assets/images/background_day.png")
    
    # Noche - Campo oscuro en toda la pantalla
    surface = pygame.Surface((1200, 800), pygame.SRCALPHA)
    surface.fill((0, 50, 0))  # Verde muy oscuro base
    
    # Crear patrón de hierba oscura en toda la pantalla
    for y in range(0, 800, 2):
        for x in range(0, 1200, 2):
            if random.random() < 0.3:  # 30% de probabilidad de hierba oscura
                pygame.draw.rect(surface, (0, 50, 0), (x, y, 2, 2))
            elif random.random() < 0.1:  # 10% de probabilidad de hierba muy oscura
                pygame.draw.rect(surface, (0, 25, 0), (x, y, 2, 2))
            elif random.random() < 0.05:  # 5% de probabilidad de tierra oscura
                pygame.draw.rect(surface, (50, 25, 0), (x, y, 2, 2))
    
    # Agregar algunas flores rojas oscuras (menos visibles)
    for _ in range(30):
        x = random.randint(0, 1200)
        y = random.randint(0, 800)
        pygame.draw.rect(surface, (100, 0, 0), (x, y, 2, 2))
    
    pygame.image.save(surface, "assets/images/background_night.png")
    
    # Amanecer - Campo con tonos rosados en toda la pantalla
    surface = pygame.Surface((1200, 800), pygame.SRCALPHA)
    surface.fill((200, 150, 150))  # Rosa claro base
    
    # Crear patrón de hierba con tonos rosados en toda la pantalla
    for y in range(0, 800, 2):
        for x in range(0, 1200, 2):
            if random.random() < 0.3:  # 30% de probabilidad de hierba verde
                pygame.draw.rect(surface, (144, 238, 144), (x, y, 2, 2))
            elif random.random() < 0.2:  # 20% de probabilidad de hierba rosada
                pygame.draw.rect(surface, (200, 150, 150), (x, y, 2, 2))
            elif random.random() < 0.1:  # 10% de probabilidad de tierra rosada
                pygame.draw.rect(surface, (180, 120, 120), (x, y, 2, 2))
    
    # Agregar flores rojas
    for _ in range(70):
        x = random.randint(0, 1200)
        y = random.randint(0, 800)
        pygame.draw.rect(surface, (255, 0, 0), (x, y, 2, 2))
        pygame.draw.rect(surface, (255, 255, 0), (x+1, y+1, 1, 1))
    
    pygame.image.save(surface, "assets/images/background_dawn.png")
    
    # Atardecer - Campo con tonos naranjas en toda la pantalla
    surface = pygame.Surface((1200, 800), pygame.SRCALPHA)
    surface.fill((200, 150, 100))  # Naranja claro base
    
    # Crear patrón de hierba con tonos naranjas en toda la pantalla
    for y in range(0, 800, 2):
        for x in range(0, 1200, 2):
            if random.random() < 0.3:  # 30% de probabilidad de hierba verde
                pygame.draw.rect(surface, (144, 238, 144), (x, y, 2, 2))
            elif random.random() < 0.2:  # 20% de probabilidad de hierba naranja
                pygame.draw.rect(surface, (200, 150, 100), (x, y, 2, 2))
            elif random.random() < 0.1:  # 10% de probabilidad de tierra naranja
                pygame.draw.rect(surface, (180, 130, 80), (x, y, 2, 2))
    
    # Agregar flores rojas
    for _ in range(75):
        x = random.randint(0, 1200)
        y = random.randint(0, 800)
        pygame.draw.rect(surface, (255, 0, 0), (x, y, 2, 2))
        pygame.draw.rect(surface, (255, 255, 0), (x+1, y+1, 1, 1))
    
    pygame.image.save(surface, "assets/images/background_dusk.png")

def create_enemy_images():
    """Crear imágenes de enemigos"""
    # Enemigo sombra - Estilo consistente con la criatura
    surface = pygame.Surface((24, 24), pygame.SRCALPHA)
    
    # Contorno negro grueso
    pygame.draw.rect(surface, (0, 0, 0), (2, 2, 20, 20))  # Contorno exterior
    
    # Cuerpo sombra con gradientes oscuros
    pygame.draw.rect(surface, (40, 40, 40), (4, 4, 16, 16))  # Gris oscuro base
    pygame.draw.rect(surface, (20, 20, 20), (4, 4, 16, 8))   # Gris más oscuro (sombra)
    pygame.draw.rect(surface, (60, 60, 60), (4, 4, 16, 4))   # Gris claro (iluminación)
    
    # Cabeza cuadrada grande
    pygame.draw.rect(surface, (40, 40, 40), (6, 2, 12, 8))  # Cabeza gris
    pygame.draw.rect(surface, (20, 20, 20), (6, 2, 12, 4))  # Sombra en cabeza
    
    # Cabello negro
    pygame.draw.rect(surface, (0, 0, 0), (6, 0, 12, 4))     # Cabello principal
    pygame.draw.rect(surface, (0, 0, 0), (4, 2, 2, 2))      # Cabello lado izquierdo
    pygame.draw.rect(surface, (0, 0, 0), (18, 2, 2, 2))     # Cabello lado derecho
    
    # Ojos rojos brillantes
    pygame.draw.rect(surface, (255, 0, 0), (8, 4, 3, 2))     # Ojo izquierdo rojo
    pygame.draw.rect(surface, (255, 0, 0), (13, 4, 3, 2))   # Ojo derecho rojo
    pygame.draw.rect(surface, (0, 0, 0), (8, 4, 3, 2), 1)   # Contorno ojo izquierdo
    pygame.draw.rect(surface, (0, 0, 0), (13, 4, 3, 2), 1)  # Contorno ojo derecho
    
    # Boca pequeña oscura
    pygame.draw.rect(surface, (0, 0, 0), (10, 6, 4, 1))     # Boca
    
    # Torso musculoso
    pygame.draw.rect(surface, (40, 40, 40), (6, 10, 12, 8))  # Torso
    pygame.draw.rect(surface, (20, 20, 20), (6, 10, 12, 4)) # Sombra torso
    
    # Brazos gruesos
    pygame.draw.rect(surface, (40, 40, 40), (4, 12, 3, 6))  # Brazo izquierdo
    pygame.draw.rect(surface, (40, 40, 40), (17, 12, 3, 6)) # Brazo derecho
    pygame.draw.rect(surface, (20, 20, 20), (4, 12, 3, 3))  # Sombra brazo izquierdo
    pygame.draw.rect(surface, (20, 20, 20), (17, 12, 3, 3))  # Sombra brazo derecho
    
    # Manos simples
    pygame.draw.rect(surface, (40, 40, 40), (3, 16, 2, 2))  # Mano izquierda
    pygame.draw.rect(surface, (40, 40, 40), (19, 16, 2, 2)) # Mano derecha
    
    # Piernas cortas y gruesas
    pygame.draw.rect(surface, (40, 40, 40), (8, 18, 3, 4))  # Pierna izquierda
    pygame.draw.rect(surface, (40, 40, 40), (13, 18, 3, 4)) # Pierna derecha
    pygame.draw.rect(surface, (20, 20, 20), (8, 18, 3, 2))  # Sombra pierna izquierda
    pygame.draw.rect(surface, (20, 20, 20), (13, 18, 3, 2)) # Sombra pierna derecha
    
    # Pies simples
    pygame.draw.rect(surface, (40, 40, 40), (7, 22, 2, 1))  # Pie izquierdo
    pygame.draw.rect(surface, (40, 40, 40), (15, 22, 2, 1)) # Pie derecho
    
    # Sombra gris debajo
    pygame.draw.rect(surface, (80, 80, 80), (6, 23, 12, 1)) # Sombra proyectada
    
    pygame.image.save(surface, "assets/images/enemy_shadow.png")
    
    # Criatura hostil - Basada en la referencia verde monstruosa
    surface = pygame.Surface((24, 24), pygame.SRCALPHA)
    
    # Contorno negro grueso
    pygame.draw.rect(surface, (0, 0, 0), (2, 2, 20, 20))  # Contorno exterior
    
    # Cuerpo verde con gradientes
    pygame.draw.rect(surface, (100, 150, 50), (4, 4, 16, 16))  # Verde base
    pygame.draw.rect(surface, (80, 120, 40), (4, 4, 16, 8))   # Verde más oscuro (sombra)
    pygame.draw.rect(surface, (120, 180, 60), (4, 4, 16, 4))  # Verde claro (iluminación)
    
    # Cabeza cuadrada grande
    pygame.draw.rect(surface, (100, 150, 50), (6, 2, 12, 8))  # Cabeza verde
    pygame.draw.rect(surface, (80, 120, 40), (6, 2, 12, 4))   # Sombra en cabeza
    
    # Cabello marrón oscuro/púrpura
    pygame.draw.rect(surface, (60, 30, 80), (6, 0, 12, 4))   # Cabello principal
    pygame.draw.rect(surface, (60, 30, 80), (4, 2, 2, 2))    # Cabello lado izquierdo
    pygame.draw.rect(surface, (60, 30, 80), (18, 2, 2, 2))   # Cabello lado derecho
    
    # Ojos blancos rectangulares
    pygame.draw.rect(surface, (255, 255, 255), (8, 4, 3, 2))  # Ojo izquierdo
    pygame.draw.rect(surface, (255, 255, 255), (13, 4, 3, 2)) # Ojo derecho
    pygame.draw.rect(surface, (0, 0, 0), (8, 4, 3, 2), 1)     # Contorno ojo izquierdo
    pygame.draw.rect(surface, (0, 0, 0), (13, 4, 3, 2), 1)    # Contorno ojo derecho
    
    # Boca pequeña oscura
    pygame.draw.rect(surface, (0, 0, 0), (10, 6, 4, 1))       # Boca
    
    # Torso musculoso
    pygame.draw.rect(surface, (100, 150, 50), (6, 10, 12, 8))  # Torso
    pygame.draw.rect(surface, (80, 120, 40), (6, 10, 12, 4))  # Sombra torso
    
    # Brazos gruesos
    pygame.draw.rect(surface, (100, 150, 50), (4, 12, 3, 6))   # Brazo izquierdo
    pygame.draw.rect(surface, (100, 150, 50), (17, 12, 3, 6))  # Brazo derecho
    pygame.draw.rect(surface, (80, 120, 40), (4, 12, 3, 3))   # Sombra brazo izquierdo
    pygame.draw.rect(surface, (80, 120, 40), (17, 12, 3, 3))  # Sombra brazo derecho
    
    # Manos simples
    pygame.draw.rect(surface, (100, 150, 50), (3, 16, 2, 2))   # Mano izquierda
    pygame.draw.rect(surface, (100, 150, 50), (19, 16, 2, 2))  # Mano derecha
    
    # Piernas cortas y gruesas
    pygame.draw.rect(surface, (100, 150, 50), (8, 18, 3, 4))   # Pierna izquierda
    pygame.draw.rect(surface, (100, 150, 50), (13, 18, 3, 4))  # Pierna derecha
    pygame.draw.rect(surface, (80, 120, 40), (8, 18, 3, 2))   # Sombra pierna izquierda
    pygame.draw.rect(surface, (80, 120, 40), (13, 18, 3, 2))  # Sombra pierna derecha
    
    # Pies simples
    pygame.draw.rect(surface, (100, 150, 50), (7, 22, 2, 1))   # Pie izquierdo
    pygame.draw.rect(surface, (100, 150, 50), (15, 22, 2, 1))  # Pie derecho
    
    # Sombra gris debajo
    pygame.draw.rect(surface, (100, 100, 100), (6, 23, 12, 1)) # Sombra proyectada
    
    pygame.image.save(surface, "assets/images/enemy_creature.png")

def create_building_images():
    """Crear imágenes de construcciones"""
    # Muro
    surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.rect(surface, (139, 69, 19), (0, 0, 40, 40))
    pygame.draw.rect(surface, (101, 67, 33), (5, 5, 30, 30))
    pygame.image.save(surface, "assets/images/wall.png")
    
    # Puerta
    surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.rect(surface, (101, 67, 33), (0, 0, 40, 40))
    pygame.draw.rect(surface, (139, 69, 19), (10, 10, 20, 30))
    pygame.image.save(surface, "assets/images/door.png")
    
    # Piso
    surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.rect(surface, (160, 82, 45), (0, 0, 40, 40))
    pygame.draw.rect(surface, (139, 69, 19), (5, 5, 30, 30))
    pygame.image.save(surface, "assets/images/floor.png")
    
    # Techo
    surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.rect(surface, (105, 105, 105), (0, 0, 40, 40))
    pygame.draw.rect(surface, (64, 64, 64), (5, 5, 30, 30))
    pygame.image.save(surface, "assets/images/roof.png")
    
    # Fuego
    surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(surface, (255, 69, 0), (20, 20), 15)
    pygame.draw.circle(surface, (255, 140, 0), (20, 20), 10)
    pygame.draw.circle(surface, (255, 255, 0), (20, 20), 5)
    pygame.image.save(surface, "assets/images/fire.png")

def create_item_images():
    """Crear imágenes de items"""
    # Antorcha
    surface = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.rect(surface, (139, 69, 19), (8, 12, 4, 8))  # Palo
    pygame.draw.circle(surface, (255, 69, 0), (10, 10), 6)  # Fuego
    pygame.image.save(surface, "assets/images/torch.png")
    
    # Madera
    surface = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.draw.rect(surface, (139, 69, 19), (4, 2, 8, 12))
    pygame.draw.rect(surface, (101, 67, 33), (6, 4, 4, 8))
    pygame.image.save(surface, "assets/images/wood.png")
    
    # Piedra
    surface = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.draw.circle(surface, (128, 128, 128), (8, 8), 6)
    pygame.draw.circle(surface, (96, 96, 96), (8, 8), 4)
    pygame.image.save(surface, "assets/images/stone.png")
    
    # Hierba
    surface = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.draw.rect(surface, (34, 139, 34), (6, 8, 4, 8))
    pygame.draw.rect(surface, (0, 100, 0), (7, 6, 2, 10))
    pygame.image.save(surface, "assets/images/grass.png")
    
    # Hueso
    surface = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.draw.rect(surface, (255, 255, 255), (6, 4, 4, 8))
    pygame.draw.rect(surface, (200, 200, 200), (7, 5, 2, 6))
    pygame.image.save(surface, "assets/images/bone.png")

if __name__ == "__main__":
    pygame.init()
    create_temp_assets()
    pygame.quit()
