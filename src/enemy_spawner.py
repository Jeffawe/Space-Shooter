"""
Basic Enemy Spawner for Retro Space Shooter
TODO: Enhance this system later for story mode and advanced gameplay
"""
import pygame
import random
from enemy import Enemy, Asteroid, Debris
from constants import *

class EnemySpawner:
    def __init__(self):
        """Initialize the enemy spawner"""
        self.spawn_timer = 0
        self.enemy_spawn_rate = 120  # Frames between enemy spawns (2 seconds at 60 FPS)
        self.asteroid_spawn_rate = 180  # 3 seconds
        self.debris_spawn_rate = 240  # 4 seconds
        
        # Spawn probabilities for different enemy types
        self.enemy_types = ["fighter1", "fighter2", "crabship", "gunship", "pirate"]
        self.enemy_weights = [30, 25, 20, 15, 10]  # Fighter1 most common, Gunship least
        
        # Environmental spawn settings
        self.max_asteroids = 3  # Maximum asteroids on screen
        self.max_debris = 5     # Maximum debris pieces
        
        print("🚀 Basic Enemy Spawner initialized")
        print("TODO: Enhance spawner system for story mode")
        
    def update(self, enemy_group, asteroid_group, debris_group, all_sprites):
        """Update spawner and create new enemies/hazards"""
        self.spawn_timer += 1
        
        # Spawn enemies
        if self.spawn_timer % self.enemy_spawn_rate == 0:
            self.spawn_enemy(enemy_group, all_sprites)
            
        # Spawn asteroids
        if (self.spawn_timer % self.asteroid_spawn_rate == 0 and 
            len(asteroid_group) < self.max_asteroids):
            self.spawn_asteroid(asteroid_group, all_sprites)
            
        # Spawn debris
        if (self.spawn_timer % self.debris_spawn_rate == 0 and 
            len(debris_group) < self.max_debris):
            self.spawn_debris(debris_group, all_sprites)
    
    def spawn_enemy(self, enemy_group, all_sprites):
        """Spawn a random enemy ship from top or bottom only"""
        # Choose enemy type based on weights
        enemy_type = random.choices(self.enemy_types, weights=self.enemy_weights)[0]
        
        # Choose spawn location (only top or bottom)
        spawn_location = random.choice(["top", "bottom"])
        
        if spawn_location == "top":
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(-100, -50)
            flight_direction = "down"  # Coming from top, flying down
        else:  # bottom
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(SCREEN_HEIGHT + 50, SCREEN_HEIGHT + 100)
            flight_direction = "up"  # Coming from bottom, flying up
        
        # Create enemy with vertical flight direction
        enemy = Enemy(enemy_type, x, y, flight_direction)
        enemy_group.add(enemy)
        all_sprites.add(enemy)
        
        print(f"Spawned {enemy_type} from {spawn_location} at ({x}, {y}) flying {flight_direction}")
    
    def spawn_asteroid(self, asteroid_group, all_sprites):
        """Spawn an asteroid from top or bottom"""
        # Random size
        size = random.choice(["small", "medium", "large"])
        
        # Choose spawn location (only top or bottom)
        spawn_location = random.choice(["top", "bottom"])
        
        if spawn_location == "top":
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(-100, -50)
        else:  # bottom
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(SCREEN_HEIGHT + 50, SCREEN_HEIGHT + 100)
        
        # Create asteroid
        asteroid = Asteroid(x, y, size)
        asteroid_group.add(asteroid)
        all_sprites.add(asteroid)
        
        print(f"Spawned {size} asteroid from {spawn_location} at ({x}, {y})")
    
    def spawn_debris(self, debris_group, all_sprites):
        """Spawn debris from top or bottom"""
        # Choose spawn location (only top or bottom)
        spawn_location = random.choice(["top", "bottom"])
        
        if spawn_location == "top":
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(-50, -20)
        else:  # bottom
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 50)
        
        # Create debris
        debris = Debris(x, y)
        debris_group.add(debris)
        all_sprites.add(debris)
        
        print(f"Spawned debris from {spawn_location} at ({x}, {y})")
    
    def set_difficulty(self, level):
        """Adjust spawn rates based on difficulty (for future enhancement)"""
        # TODO: Implement difficulty scaling
        # This is a placeholder for future story mode enhancement
        base_enemy_rate = 120
        base_asteroid_rate = 180
        
        # Increase spawn rate with difficulty
        self.enemy_spawn_rate = max(30, base_enemy_rate - (level * 10))
        self.asteroid_spawn_rate = max(60, base_asteroid_rate - (level * 15))
        
        print(f"TODO: Difficulty set to level {level} - enhance this system!")
    
    def spawn_wave(self, wave_type, enemy_group, all_sprites):
        """Spawn a specific wave of enemies (for future story mode)"""
        # TODO: Implement wave-based spawning for story mode
        print(f"TODO: Implement wave spawning - {wave_type}")
        
        # Placeholder: spawn 3 enemies of the same type
        enemy_type = random.choice(self.enemy_types)
        for i in range(3):
            x = 100 + (i * 150)
            y = -50 - (i * 30)
            enemy = Enemy(enemy_type, x, y)
            enemy_group.add(enemy)
            all_sprites.add(enemy)
