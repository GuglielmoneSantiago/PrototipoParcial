#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Assets para el Videojuego de Supervivencia Nocturna
Maneja la carga de imágenes, sonidos y música
"""

import pygame
import os
from typing import Dict, Optional

class AssetsManager:
    def __init__(self):
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_files: Dict[str, str] = {}
        
        # Inicializar mixer para sonidos
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
    def load_image(self, name: str, filename: str, scale: Optional[tuple] = None) -> bool:
        """
        Cargar una imagen desde el archivo
        
        Args:
            name: Nombre interno de la imagen
            filename: Nombre del archivo (debe estar en assets/images/)
            scale: Tupla (width, height) para redimensionar la imagen
            
        Returns:
            bool: True si se cargó correctamente, False en caso contrario
        """
        try:
            filepath = os.path.join("assets", "images", filename)
            if not os.path.exists(filepath):
                print(f"Advertencia: No se encontró la imagen {filepath}")
                return False
                
            image = pygame.image.load(filepath).convert_alpha()
            
            if scale:
                image = pygame.transform.scale(image, scale)
                
            self.images[name] = image
            print(f"Imagen cargada: {name} desde {filename}")
            return True
            
        except pygame.error as e:
            print(f"Error al cargar imagen {filename}: {e}")
            return False
            
    def load_sound(self, name: str, filename: str) -> bool:
        """
        Cargar un sonido desde el archivo
        
        Args:
            name: Nombre interno del sonido
            filename: Nombre del archivo (debe estar en assets/sounds/)
            
        Returns:
            bool: True si se cargó correctamente, False en caso contrario
        """
        try:
            filepath = os.path.join("assets", "sounds", filename)
            if not os.path.exists(filepath):
                print(f"Advertencia: No se encontró el sonido {filepath}")
                return False
                
            sound = pygame.mixer.Sound(filepath)
            self.sounds[name] = sound
            print(f"Sonido cargado: {name} desde {filename}")
            return True
            
        except pygame.error as e:
            print(f"Error al cargar sonido {filename}: {e}")
            return False
            
    def load_music(self, name: str, filename: str) -> bool:
        """
        Registrar un archivo de música
        
        Args:
            name: Nombre interno de la música
            filename: Nombre del archivo (debe estar en assets/sounds/)
            
        Returns:
            bool: True si se registró correctamente, False en caso contrario
        """
        try:
            filepath = os.path.join("assets", "sounds", filename)
            if not os.path.exists(filepath):
                print(f"Advertencia: No se encontró la música {filepath}")
                return False
                
            self.music_files[name] = filepath
            print(f"Música registrada: {name} desde {filename}")
            return True
            
        except Exception as e:
            print(f"Error al registrar música {filename}: {e}")
            return False
            
    def get_image(self, name: str) -> Optional[pygame.Surface]:
        """Obtener una imagen cargada"""
        return self.images.get(name)
        
    def get_sound(self, name: str) -> Optional[pygame.mixer.Sound]:
        """Obtener un sonido cargado"""
        return self.sounds.get(name)
        
    def get_music_path(self, name: str) -> Optional[str]:
        """Obtener la ruta de un archivo de música"""
        return self.music_files.get(name)
        
    def play_sound(self, name: str, volume: float = 1.0) -> bool:
        """
        Reproducir un sonido
        
        Args:
            name: Nombre del sonido
            volume: Volumen (0.0 a 1.0)
            
        Returns:
            bool: True si se reprodujo correctamente
        """
        sound = self.get_sound(name)
        if sound:
            sound.set_volume(volume)
            sound.play()
            return True
        return False
        
    def play_music(self, name: str, loops: int = -1, volume: float = 0.5) -> bool:
        """
        Reproducir música de fondo
        
        Args:
            name: Nombre de la música
            loops: Número de repeticiones (-1 para infinito)
            volume: Volumen (0.0 a 1.0)
            
        Returns:
            bool: True si se reprodujo correctamente
        """
        music_path = self.get_music_path(name)
        if music_path:
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loops)
                return True
            except pygame.error as e:
                print(f"Error al reproducir música {name}: {e}")
        return False
        
    def stop_music(self):
        """Detener la música de fondo"""
        pygame.mixer.music.stop()
        
    def pause_music(self):
        """Pausar la música de fondo"""
        pygame.mixer.music.pause()
        
    def unpause_music(self):
        """Reanudar la música de fondo"""
        pygame.mixer.music.unpause()
        
    def load_all_assets(self):
        """Cargar todos los assets del juego"""
        print("Cargando assets del juego...")
        
        # Cargar imágenes del personaje
        self.load_image("player_idle", "player_idle.png", (32, 32))
        self.load_image("player_walk", "player_walk.png", (32, 32))
        self.load_image("player_run", "player_run.png", (32, 32))
        
        # Cargar fondos
        self.load_image("background_day", "background_day.png")
        self.load_image("background_night", "background_night.png")
        self.load_image("background_dawn", "background_dawn.png")
        self.load_image("background_dusk", "background_dusk.png")
        
        # Cargar enemigos
        self.load_image("enemy_shadow", "enemy_shadow.png", (24, 24))
        self.load_image("enemy_creature", "enemy_creature.png", (24, 24))
        
        # Cargar construcciones
        self.load_image("wall", "wall.png", (40, 40))
        self.load_image("door", "door.png", (40, 40))
        self.load_image("floor", "floor.png", (40, 40))
        self.load_image("roof", "roof.png", (40, 40))
        self.load_image("fire", "fire.png", (40, 40))
        
        # Cargar items
        self.load_image("torch", "torch.png", (20, 20))
        self.load_image("wood", "wood.png", (16, 16))
        self.load_image("stone", "stone.png", (16, 16))
        self.load_image("grass", "grass.png", (16, 16))
        self.load_image("bone", "bone.png", (16, 16))
        
        # Cargar sonidos
        self.load_sound("footstep", "footstep.wav")
        self.load_sound("collect", "collect.wav")
        self.load_sound("build", "build.wav")
        self.load_sound("enemy_hit", "enemy_hit.wav")
        self.load_sound("player_hurt", "player_hurt.wav")
        
        # Cargar música
        self.load_music("ambient_day", "ambient_day.ogg")
        self.load_music("ambient_night", "ambient_night.ogg")
        self.load_music("menu", "menu.ogg")
        
        print("Assets cargados correctamente!")

# Instancia global del gestor de assets
assets = AssetsManager()
