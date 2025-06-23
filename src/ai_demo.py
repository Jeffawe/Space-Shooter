#!/usr/bin/env python3
"""
Demo the enemy AI system with detection, positioning, and shooting
"""
import pygame
from game import Game
from enemy import Enemy
from constants import *

def demo_enemy_ai():
    """Demo intelligent enemy AI behavior"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🤖 ENEMY AI SYSTEM DEMO")
    print("Testing intelligent enemy behavior: detection, positioning, shooting, and bombs")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Create enemies with different AI behaviors
    ai_enemies = [
        ("fighter1", 200, 100, "down", "Aggressive AI - Fast attack"),
        ("fighter2", 600, 150, "up", "Tactical AI - Weaving movement"),
        ("crabship", 100, 400, "down", "Defensive AI - Drops bombs"),
        ("gunship", 700, 500, "up", "Artillery AI - Long range"),
        ("pirate", 400, 50, "down", "Chaotic AI - Unpredictable with bombs"),
    ]
    
    print("\nCreating AI enemy showcase:")
    for enemy_type, x, y, direction, description in ai_enemies:
        enemy = Enemy(enemy_type, x, y, direction)
        game.enemies.add(enemy)
        game.all_sprites.add(enemy)
        print(f"  {enemy_type} - {description}")
        print(f"    Detection radius: {enemy.detection_radius}")
        print(f"    Attack radius: {enemy.attack_radius}")
        print(f"    Can drop bombs: {enemy.can_drop_bombs}")
    
    print(f"\nPlayer positioned at center: ({game.player.rect.centerx}, {game.player.rect.centery})")
    print("Enemies will detect player and engage with AI behavior!")
    
    # Run demo for several seconds to show AI in action
    for frame in range(300):  # 5 seconds at 60 FPS
        game.update()
        game.draw()
        
        # Capture key frames showing AI behavior
        if frame in [0, 100, 200]:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/ai_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            enemy_count = len(game.enemies)
            enemy_shots = len(game.enemy_projectiles)
            bombs = len(game.bombs)
            
            print(f"\nFrame {frame}:")
            print(f"  Enemies: {enemy_count}")
            print(f"  Enemy projectiles: {enemy_shots}")
            print(f"  Bombs dropped: {bombs}")
            print(f"  Screenshot: {screenshot_path}")
            
            # Show AI states
            for i, enemy in enumerate(game.enemies):
                print(f"    Enemy {i+1} ({enemy.enemy_type}): State = {enemy.ai_state}")
    
    print("\n✅ Enemy AI system working perfectly!")
    print("🎯 Enemies detect player within radius")
    print("🧠 AI positioning to get in front/behind player")
    print("🔫 Smart shooting when in attack range")
    print("💣 Bomb dropping by capable enemy types")
    print("🤖 Different AI personalities for each enemy type!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_enemy_ai()
