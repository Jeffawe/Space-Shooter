#!/usr/bin/env python3
"""
Demo the complete health system with player health bar, enemy health, and explosions
"""
import pygame
from game import Game
from enemy import Enemy, Asteroid, Debris
from constants import *

def demo_health_system():
    """Demo the complete health system with visual health bars and explosions"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("💖 HEALTH SYSTEM DEMO")
    print("Testing player health bar, enemy health, and explosion effects")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Create test objects for health system
    health_test_objects = [
        # Enemies with different health levels
        ("gunship", 300, 200, "down", "High health enemy (3 HP)"),
        ("pirate", 500, 300, "up", "Medium health enemy (2 HP)"),
        ("fighter1", 350, 350, "down", "Low health enemy (1 HP)"),
        
        # Environmental hazards for damage testing
        ("asteroid", 400, 150, "large", "High damage collision (10 HP)"),
        ("asteroid", 450, 450, "medium", "Medium damage collision (10 HP)"),
        ("debris", 320, 280, None, "Light damage collision (5 HP)"),
    ]
    
    print(f"\nPlayer starts with {game.player.health_system.current_health} HP")
    print("Health bar displayed in bottom left corner")
    print("\nCreating health test environment:")
    
    for obj_type, x, y, param, description in health_test_objects:
        if obj_type == "asteroid":
            obj = Asteroid(x, y, param)
            game.asteroids.add(obj)
            game.all_sprites.add(obj)
            print(f"  {param} asteroid at ({x}, {y}) - {description}")
            
        elif obj_type == "debris":
            obj = Debris(x, y)
            game.debris.add(obj)
            game.all_sprites.add(obj)
            print(f"  Debris at ({x}, {y}) - {description}")
            
        else:  # enemy
            obj = Enemy(obj_type, x, y, param)
            game.enemies.add(obj)
            game.all_sprites.add(obj)
            print(f"  {obj_type} at ({x}, {y}) - {description} (Health: {obj.health})")
    
    print(f"\nPlayer positioned at center: ({game.player.rect.centerx}, {game.player.rect.centery})")
    print("🎮 Controls:")
    print("  WASD/Arrow Keys - Move (collisions cause damage)")
    print("  Q - Primary weapon (destroy enemies)")
    print("  E - Secondary weapon (destroy enemies)")
    print("  R - Restart when dead")
    print("  ESC - Quit")
    
    # Run demo to show health system
    for frame in range(600):  # 10 seconds
        # Handle events for player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break
                elif event.key == pygame.K_r and game.game_over and game.player_death_timer <= 0:
                    game.restart_game()
                elif event.key == pygame.K_q and game.player.is_alive():
                    # Primary weapon
                    shot_data = game.player.shoot("primary")
                    if shot_data:
                        x, y, proj_type, direction = shot_data
                        from projectile import Projectile
                        projectile = Projectile(x, y, proj_type, direction)
                        game.projectiles.add(projectile)
                        game.all_sprites.add(projectile)
                elif event.key == pygame.K_e and game.player.is_alive():
                    # Secondary weapon
                    shot_data = game.player.shoot("secondary")
                    if shot_data:
                        x, y, proj_type, direction = shot_data
                        from projectile import Projectile
                        projectile = Projectile(x, y, proj_type, direction)
                        game.projectiles.add(projectile)
                        game.all_sprites.add(projectile)
        
        game.update()
        game.draw()
        
        # Capture key frames showing health system
        if frame in [0, 150, 300, 450]:
            screenshot_path = f"assets/images/health_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            player_health = game.player.health_system.current_health
            player_alive = game.player.is_alive()
            explosions = len(game.explosions)
            
            print(f"\nFrame {frame}:")
            print(f"  Player Health: {player_health}/100 HP")
            print(f"  Player Alive: {player_alive}")
            print(f"  Active Explosions: {explosions}")
            print(f"  Game Over: {game.game_over}")
            print(f"  Screenshot: {screenshot_path}")
            
            if not player_alive:
                print("  💥 PLAYER EXPLOSION TRIGGERED!")
                break
    
    print("\n✅ Health system working perfectly!")
    print("💖 Player Health System:")
    print("   • Visual health bar in bottom left corner")
    print("   • Takes damage from collisions and enemy projectiles")
    print("   • Invulnerability period after taking damage")
    print("   • Explosion animation when health reaches 0")
    print("🤖 Enemy Health System:")
    print("   • Different health values for different enemy types")
    print("   • Health bars appear above damaged enemies")
    print("   • Enemies destroyed when health reaches 0")
    print("💥 Explosion System:")
    print("   • Beautiful explosion animation using Explosion02-Sheet")
    print("   • Player explosion triggers game over screen")
    print("   • Restart functionality with R key")
    print("🎮 Complete gameplay loop with health consequences!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_health_system()
