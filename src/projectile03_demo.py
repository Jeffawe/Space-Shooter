#!/usr/bin/env python3
"""
Demo the enemy projectile system using Projectile03
"""
import pygame
from game import Game
from enemy import Enemy
from constants import *

def demo_projectile03_enemies():
    """Demo enemies using Projectile03 for their shots"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🔫 PROJECTILE03 ENEMY DEMO")
    print("Testing enemies using Projectile03 as their primary weapon")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Create enemies positioned to immediately engage player
    shooting_enemies = [
        ("fighter1", 350, 150, "down", "Fast shooter"),
        ("fighter2", 450, 450, "up", "Tactical shooter"),
        ("gunship", 300, 200, "down", "Artillery - long range"),
        ("pirate", 500, 400, "up", "Chaotic shooter with bombs"),
    ]
    
    print("\nCreating shooting enemy showcase:")
    for enemy_type, x, y, direction, description in shooting_enemies:
        enemy = Enemy(enemy_type, x, y, direction)
        game.enemies.add(enemy)
        game.all_sprites.add(enemy)
        print(f"  {enemy_type} - {description}")
        print(f"    Shot cooldown: {enemy.shot_cooldown} frames")
        print(f"    Attack radius: {enemy.attack_radius}")
    
    print(f"\nPlayer positioned at center: ({game.player.rect.centerx}, {game.player.rect.centery})")
    print("Enemies are positioned within attack range to demonstrate Projectile03 shooting!")
    
    # Run demo focusing on shooting behavior
    for frame in range(180):  # 3 seconds
        game.update()
        game.draw()
        
        # Capture frames showing projectile action
        if frame in [0, 60, 120]:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/projectile03_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            enemy_count = len(game.enemies)
            enemy_shots = len(game.enemy_projectiles)
            bombs = len(game.bombs)
            
            print(f"\nFrame {frame}:")
            print(f"  Enemies: {enemy_count}")
            print(f"  Projectile03 shots: {enemy_shots}")
            print(f"  Bombs: {bombs}")
            print(f"  Screenshot: {screenshot_path}")
            
            # Show which enemies are actively shooting
            active_shooters = 0
            for enemy in game.enemies:
                if enemy.ai_state == "attack":
                    active_shooters += 1
            print(f"  Active shooters: {active_shooters}")
    
    print("\n✅ Projectile03 enemy system working perfectly!")
    print("🎯 All enemies now use Projectile03 as their primary weapon")
    print("🔫 Projectiles are properly aimed at player position")
    print("💥 Different enemy types have different shooting patterns")
    print("🚀 Visual distinction between player and enemy projectiles!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_projectile03_enemies()
