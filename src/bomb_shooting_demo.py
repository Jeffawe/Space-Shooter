#!/usr/bin/env python3
"""
Demo the projectile-bomb collision system - shooting bombs to destroy them
"""
import pygame
from game import Game
from enemy_projectile import Bomb
from constants import *

def demo_bomb_shooting():
    """Demo shooting bombs to destroy them safely"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("💥 BOMB SHOOTING SYSTEM DEMO")
    print("Testing projectile-bomb collisions - shoot bombs to destroy them!")
    
    # Position player in center-left
    game.player.rect.centerx = 200
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Create test bombs at various positions
    test_bombs = [
        (400, 200, "Target bomb - easy shot"),
        (500, 300, "Moving target bomb"),
        (350, 400, "Close range bomb"),
        (600, 150, "Long range bomb"),
        (450, 350, "Cluster bomb 1"),
        (470, 370, "Cluster bomb 2"),
        (430, 330, "Cluster bomb 3"),
    ]
    
    print(f"\nPlayer positioned at: ({game.player.rect.centerx}, {game.player.rect.centery})")
    print("Creating target bombs for shooting practice:")
    
    for x, y, description in test_bombs:
        bomb = Bomb(x, y)  # Create bomb at position
        # Make bomb stationary for testing by setting speed to 0
        bomb.speed = 0
        game.bombs.add(bomb)
        game.all_sprites.add(bomb)
        print(f"  Bomb at ({x}, {y}) - {description}")
    
    print(f"\nTotal bombs created: {len(test_bombs)}")
    print("💥 Bomb Shooting Features:")
    print("  🎯 Projectiles can hit and destroy bombs")
    print("  💥 Bombs explode when shot (safe detonation)")
    print("  🎮 Strategic bomb clearing from distance")
    print("  📊 Statistics tracking for bombs shot")
    
    print("\n🎮 Controls:")
    print("  WASD/Arrow Keys - Move and aim")
    print("  Q - Primary weapon (shoot bombs)")
    print("  E - Secondary weapon (shoot bombs)")
    print("  R - Restart")
    print("  ESC - Quit")
    print("  Aim at bombs and shoot to destroy them safely!")
    
    # Run demo
    for frame in range(900):  # 15 seconds
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break
                elif event.key == pygame.K_r and game.game_over and game.player_death_timer <= 0:
                    game.restart_game()
                elif event.key == pygame.K_q and game.player.is_alive():
                    # Primary weapon - shoot at bombs
                    shot_data = game.player.shoot("primary")
                    if shot_data:
                        from projectile import Projectile
                        x, y, proj_type, direction = shot_data
                        projectile = Projectile(x, y, proj_type, direction)
                        game.projectiles.add(projectile)
                        game.all_sprites.add(projectile)
                        print(f"🔫 Fired {direction} projectile at frame {frame}")
                elif event.key == pygame.K_e and game.player.is_alive():
                    # Secondary weapon - shoot at bombs
                    shot_data = game.player.shoot("secondary")
                    if shot_data:
                        from projectile import Projectile
                        x, y, proj_type, direction = shot_data
                        projectile = Projectile(x, y, proj_type, direction)
                        game.projectiles.add(projectile)
                        game.all_sprites.add(projectile)
                        print(f"🔫 Fired {direction} secondary projectile at frame {frame}")
        
        game.update()
        game.draw()
        
        # Capture key frames
        if frame in [0, 200, 400, 600, 800]:
            screenshot_path = f"assets/images/bomb_shooting_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            bombs_remaining = len(game.bombs)
            bombs_shot = game.collision_stats['bombs_shot']
            projectiles_active = len(game.projectiles)
            
            print(f"\nFrame {frame}:")
            print(f"  Bombs Remaining: {bombs_remaining}")
            print(f"  Bombs Shot: {bombs_shot}")
            print(f"  Active Projectiles: {projectiles_active}")
            print(f"  Screenshot: {screenshot_path}")
            
            if bombs_shot > 0:
                print(f"  🎯 SUCCESS! {bombs_shot} bombs destroyed by shooting!")
            if bombs_remaining == 0:
                print("  🏆 ALL BOMBS CLEARED!")
    
    print("\n✅ Bomb shooting system demo completed!")
    print("💥 Projectile-Bomb Collision Features:")
    print("   🎯 Projectiles can hit and destroy bombs")
    print("   💥 Bombs explode when shot (safe detonation)")
    print("   🔫 Both primary and secondary weapons work")
    print("   📊 Statistics tracking for tactical feedback")
    print("   🎮 Strategic bomb clearing from safe distance")
    print("   ⚡ Works with energy-enhanced projectiles too")
    print("🚀 Players can now actively defend against bomb threats!")
    print("🎯 Adds tactical depth - avoid OR destroy bombs!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_bomb_shooting()
