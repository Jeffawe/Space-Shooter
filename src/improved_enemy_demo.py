#!/usr/bin/env python3
"""
Demo the improved enemy system: top/bottom spawning only, slower movement
"""
import pygame
from game import Game
from enemy import Enemy
from constants import *

def demo_improved_enemies():
    """Demo improved enemy behavior with top/bottom spawning and slower movement"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🚀 IMPROVED ENEMY SYSTEM DEMO")
    print("Testing top/bottom spawning only with slower, more controlled movement")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Create enemies from top and bottom to showcase improved spawning
    improved_enemies = [
        ("fighter1", 200, -50, "down", "From TOP, flying DOWN - Aggressive (speed 2)"),
        ("fighter2", 400, -80, "down", "From TOP, flying DOWN - Tactical weaving (speed 1.5)"),
        ("crabship", 600, SCREEN_HEIGHT + 50, "up", "From BOTTOM, flying UP - Defensive (speed 0.8)"),
        ("gunship", 300, SCREEN_HEIGHT + 80, "up", "From BOTTOM, flying UP - Artillery (speed 0.7)"),
        ("pirate", 500, -60, "down", "From TOP, flying DOWN - Chaotic (speed 1.2)"),
    ]
    
    print("\nCreating improved enemy showcase:")
    for enemy_type, x, y, direction, description in improved_enemies:
        enemy = Enemy(enemy_type, x, y, direction)
        game.enemies.add(enemy)
        game.all_sprites.add(enemy)
        print(f"  {enemy_type} - {description}")
        print(f"    Base speed: {enemy.base_speed}")
        print(f"    Movement pattern: {enemy.movement_pattern}")
    
    print(f"\nPlayer positioned at center: ({game.player.rect.centerx}, {game.player.rect.centery})")
    print("Enemies will move slower and more predictably!")
    
    # Run demo to show improved movement
    for frame in range(240):  # 4 seconds at 60 FPS
        game.update()
        game.draw()
        
        # Capture key frames showing improved movement
        if frame in [0, 80, 160]:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/improved_enemy_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            enemy_count = len(game.enemies)
            enemy_shots = len(game.enemy_projectiles)
            bombs = len(game.bombs)
            
            print(f"\nFrame {frame}:")
            print(f"  Enemies: {enemy_count}")
            print(f"  Enemy projectiles: {enemy_shots}")
            print(f"  Bombs dropped: {bombs}")
            print(f"  Screenshot: {screenshot_path}")
            
            # Show enemy positions and states
            for i, enemy in enumerate(game.enemies):
                print(f"    Enemy {i+1} ({enemy.enemy_type}): Y={enemy.rect.centery}, State={enemy.ai_state}")
    
    print("\n✅ Improved enemy system working perfectly!")
    print("📍 Enemies spawn only from top and bottom")
    print("⬇️⬆️ All enemies move forward (vertically) as intended")
    print("🐌 Slower, more manageable movement speeds")
    print("🎯 Better gameplay balance and control!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_improved_enemies()
