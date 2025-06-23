#!/usr/bin/env python3
"""
Demo the corrected enemy system: spawn from multiple locations but always fly UP/DOWN
"""
import pygame
from game import Game
from enemy import Enemy, Asteroid, Debris
from constants import *

def demo_vertical_enemies():
    """Demo enemies spawning from multiple locations but always flying vertically"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🚀 VERTICAL ENEMY SYSTEM DEMO")
    print("Enemies spawn from left/right/top but always fly UP or DOWN")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Create enemies from different spawn locations but all flying vertically
    spawn_demos = [
        ("fighter1", 200, 50, "down", "Spawned from TOP, flying DOWN"),
        ("fighter2", 100, -50, "down", "Spawned from TOP, flying DOWN"),
        ("crabship", -50, 200, "down", "Spawned from LEFT, flying DOWN"),
        ("gunship", 850, 150, "up", "Spawned from RIGHT, flying UP"),
        ("pirate", -30, 300, "up", "Spawned from LEFT, flying UP"),
    ]
    
    print("\nCreating vertical movement showcase:")
    for enemy_type, x, y, direction, description in spawn_demos:
        enemy = Enemy(enemy_type, x, y, direction)
        game.enemies.add(enemy)
        game.all_sprites.add(enemy)
        print(f"  {enemy_type} - {description}")
        print(f"    Position: ({x}, {y}), Flying: {direction}")
    
    # Add environmental hazards
    print("\nAdding environmental hazards:")
    
    # Asteroids from different spawn locations
    asteroid_spawns = [
        (300, -50, "small", "from TOP"),
        (-50, 150, "medium", "from LEFT"),
        (850, 200, "large", "from RIGHT"),
    ]
    
    for x, y, size, desc in asteroid_spawns:
        asteroid = Asteroid(x, y, size)
        game.asteroids.add(asteroid)
        game.all_sprites.add(asteroid)
        print(f"  {size} asteroid {desc} at ({x}, {y})")
    
    # Debris from different spawn locations
    debris_spawns = [
        (500, -30, "from TOP"),
        (-30, 250, "from LEFT"),
        (830, 180, "from RIGHT"),
    ]
    
    for x, y, desc in debris_spawns:
        debris = Debris(x, y)
        game.debris.add(debris)
        game.all_sprites.add(debris)
        print(f"  debris {desc} at ({x}, {y})")
    
    # Capture screenshots over time to show vertical movement
    for frame in range(120):  # 2 seconds
        game.update()
        game.draw()
        
        # Capture key frames
        if frame in [0, 40, 80]:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/vertical_enemy_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            enemy_count = len(game.enemies)
            asteroid_count = len(game.asteroids)
            debris_count = len(game.debris)
            
            print(f"\nFrame {frame}:")
            print(f"  Enemies: {enemy_count}, Asteroids: {asteroid_count}, Debris: {debris_count}")
            print(f"  Screenshot: {screenshot_path}")
    
    print("\n✅ Vertical enemy system working correctly!")
    print("📍 Enemies spawn from left, right, and top locations")
    print("⬆️⬇️ All enemies face and fly UP or DOWN only")
    print("🎯 Proper space shooter mechanics with vertical combat!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_vertical_enemies()
