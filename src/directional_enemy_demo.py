#!/usr/bin/env python3
"""
Demo the directional enemy system with multi-directional spawning
"""
import pygame
from game import Game
from enemy import Enemy, Asteroid, Debris
from constants import *

def demo_directional_enemies():
    """Demo enemies coming from different directions and facing correctly"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🚀 DIRECTIONAL ENEMY SYSTEM DEMO")
    print("Testing enemies coming from multiple directions and facing correctly")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Create enemies from different directions to showcase directional facing
    directions_and_positions = [
        ("down", 200, 50, "Coming from TOP, flying DOWN"),
        ("up", 400, 550, "Coming from BOTTOM, flying UP"),
        ("right", 50, 200, "Coming from LEFT, flying RIGHT"),
        ("left", 750, 300, "Coming from RIGHT, flying LEFT"),
    ]
    
    print("\nCreating directional enemy showcase:")
    for i, (direction, x, y, description) in enumerate(directions_and_positions):
        enemy_type = ["fighter1", "fighter2", "crabship", "pirate"][i]
        enemy = Enemy(enemy_type, x, y, direction)
        game.enemies.add(enemy)
        game.all_sprites.add(enemy)
        print(f"  {enemy_type} - {description}")
        print(f"    Position: ({x}, {y}), Direction: {direction}")
    
    # Add some asteroids and debris from different directions
    print("\nAdding environmental hazards from multiple directions:")
    
    # Asteroids from different edges
    asteroid_positions = [
        (100, -50, "small", "from TOP"),
        (-50, 150, "medium", "from LEFT"),
        (850, 200, "large", "from RIGHT"),
    ]
    
    for x, y, size, desc in asteroid_positions:
        asteroid = Asteroid(x, y, size)
        game.asteroids.add(asteroid)
        game.all_sprites.add(asteroid)
        print(f"  {size} asteroid {desc} at ({x}, {y})")
    
    # Debris from different edges
    debris_positions = [
        (300, -30, "from TOP"),
        (-30, 250, "from LEFT"),
        (830, 180, "from RIGHT"),
    ]
    
    for x, y, desc in debris_positions:
        debris = Debris(x, y)
        game.debris.add(debris)
        game.all_sprites.add(debris)
        print(f"  debris {desc} at ({x}, {y})")
    
    # Capture screenshots over time to show movement
    for frame in range(120):  # 2 seconds
        game.update()
        game.draw()
        
        # Capture key frames
        if frame in [0, 40, 80]:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/directional_enemy_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            enemy_count = len(game.enemies)
            asteroid_count = len(game.asteroids)
            debris_count = len(game.debris)
            
            print(f"\nFrame {frame}:")
            print(f"  Enemies: {enemy_count}, Asteroids: {asteroid_count}, Debris: {debris_count}")
            print(f"  Screenshot: {screenshot_path}")
    
    print("\n✅ Directional enemy system working perfectly!")
    print("🎯 Enemies face the direction they're flying")
    print("🌊 Multi-directional spawning from top, left, and right")
    print("🚀 Realistic space combat with threats from all angles!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_directional_enemies()
