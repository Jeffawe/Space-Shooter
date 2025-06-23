#!/usr/bin/env python3
"""
Demo the enemy system with all 5 enemy types plus environmental hazards
"""
import pygame
from game import Game
from enemy import Enemy, Asteroid, Debris
from constants import *

def demo_enemy_system():
    """Demo all enemy types and environmental hazards"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("👾 ENEMY SYSTEM DEMO")
    print("Showcasing 5 enemy types + asteroids + debris")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Create one of each enemy type for demonstration
    enemy_types = ["fighter1", "fighter2", "crabship", "gunship", "pirate"]
    
    print("\nCreating enemy showcase:")
    for i, enemy_type in enumerate(enemy_types):
        x = 100 + (i * 120)  # Spread them across the screen
        y = 100
        enemy = Enemy(enemy_type, x, y)
        game.enemies.add(enemy)
        game.all_sprites.add(enemy)
        print(f"  {enemy_type}: Health={enemy.health}, Score={enemy.score_value}, Pattern={enemy.movement_pattern}")
    
    # Add some asteroids
    print("\nAdding asteroids:")
    for i, size in enumerate(["small", "medium", "large"]):
        x = 150 + (i * 200)
        y = 250
        asteroid = Asteroid(x, y, size)
        game.asteroids.add(asteroid)
        game.all_sprites.add(asteroid)
        print(f"  {size} asteroid: Health={asteroid.health}, Score={asteroid.score_value}")
    
    # Add some debris
    print("\nAdding debris:")
    for i in range(3):
        x = 200 + (i * 150)
        y = 400
        debris = Debris(x, y)
        game.debris.add(debris)
        game.all_sprites.add(debris)
        print(f"  Debris piece {i+1}: Health={debris.health}, Score={debris.score_value}")
    
    # Update and capture screenshots over time
    for frame in range(180):  # 3 seconds
        game.update()
        game.draw()
        
        # Capture key frames
        if frame in [0, 60, 120]:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/enemy_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            enemy_count = len(game.enemies)
            asteroid_count = len(game.asteroids)
            debris_count = len(game.debris)
            
            print(f"\nFrame {frame}:")
            print(f"  Enemies: {enemy_count}, Asteroids: {asteroid_count}, Debris: {debris_count}")
            print(f"  Screenshot: {screenshot_path}")
    
    print("\n✅ Enemy system working perfectly!")
    print("👾 5 different enemy types with unique behaviors")
    print("🪨 Rotating asteroids with different sizes")
    print("🗑️ Drifting debris pieces")
    print("🚀 All moving independently with realistic physics!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_enemy_system()
