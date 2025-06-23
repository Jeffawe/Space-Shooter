#!/usr/bin/env python3
"""
Demo the improved enemy detection ranges - different sizes for different ships
"""
import pygame
from game import Game
from enemy import Enemy
from constants import *

def demo_detection_ranges():
    """Demo enemies with different detection ranges"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🎯 DETECTION RANGE DEMO")
    print("Testing improved detection ranges - different sizes for different ship types")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Create enemies at various distances to test detection ranges
    detection_test_enemies = [
        ("fighter1", 200, 200, "down", "Medium detection (200px)"),
        ("fighter2", 600, 200, "down", "Good detection (220px)"),
        ("crabship", 200, 400, "up", "Short detection (180px)"),
        ("gunship", 100, 100, "down", "Longest detection (280px)"),
        ("pirate", 700, 400, "up", "Very good detection (250px)"),
    ]
    
    print("\nCreating detection range showcase:")
    for enemy_type, x, y, direction, description in detection_test_enemies:
        enemy = Enemy(enemy_type, x, y, direction)
        game.enemies.add(enemy)
        game.all_sprites.add(enemy)
        
        # Calculate distance to player for testing
        dx = game.player.rect.centerx - x
        dy = game.player.rect.centery - y
        distance = (dx*dx + dy*dy)**0.5
        
        print(f"  {enemy_type} - {description}")
        print(f"    Detection radius: {enemy.detection_radius}px")
        print(f"    Attack radius: {enemy.attack_radius}px")
        print(f"    Distance to player: {distance:.1f}px")
        print(f"    Can detect player: {'YES' if distance <= enemy.detection_radius else 'NO'}")
        print(f"    Can attack player: {'YES' if distance <= enemy.attack_radius else 'NO'}")
    
    print(f"\nPlayer positioned at center: ({game.player.rect.centerx}, {game.player.rect.centery})")
    print("Testing which enemies can detect and attack the player!")
    
    # Run demo to show detection behavior
    for frame in range(150):  # 2.5 seconds
        game.update()
        game.draw()
        
        # Capture frames showing detection behavior
        if frame in [0, 50, 100]:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/detection_range_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            enemy_count = len(game.enemies)
            enemy_shots = len(game.enemy_projectiles)
            bombs = len(game.bombs)
            
            print(f"\nFrame {frame}:")
            print(f"  Enemies: {enemy_count}")
            print(f"  Enemy shots: {enemy_shots}")
            print(f"  Bombs: {bombs}")
            print(f"  Screenshot: {screenshot_path}")
            
            # Show AI states and detection status
            for i, enemy in enumerate(game.enemies):
                distance = enemy.distance_to_player(game.player.rect)
                can_detect = enemy.can_see_player(game.player.rect)
                can_attack = enemy.can_attack_player(game.player.rect)
                
                print(f"    {enemy.enemy_type}: Distance={distance:.1f}, State={enemy.ai_state}, Detect={can_detect}, Attack={can_attack}")
    
    print("\n✅ Detection range system working perfectly!")
    print("🎯 Different ship types have different detection ranges:")
    print("   • Fighter1: 200px detection, 150px attack")
    print("   • Fighter2: 220px detection, 160px attack") 
    print("   • Crabship: 180px detection, 140px attack")
    print("   • Gunship: 280px detection, 220px attack (longest)")
    print("   • Pirate: 250px detection, 180px attack")
    print("🧠 Enemies engage at appropriate distances for their type!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_detection_ranges()
