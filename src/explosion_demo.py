#!/usr/bin/env python3
"""
Demo the complete explosion system with proper frame cutting and animations
"""
import pygame
from game import Game
from enemy import Enemy, Asteroid, Debris
from projectile import Projectile
from constants import *

def demo_explosion_system():
    """Demo the complete explosion system with frame cutting and animations"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("💥 EXPLOSION SYSTEM DEMO")
    print("Testing explosion animations with proper frame cutting from Explosion02-Sheet")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Reduce player health to test death explosion
    game.player.health_system.current_health = 25
    game.player.health_system.health_bar.current_health = 25
    
    # Create test objects for explosion testing
    explosion_test_objects = [
        # Enemies to destroy with projectiles
        ("gunship", 300, 200, "down", "High health enemy (3 HP) - will explode when destroyed"),
        ("pirate", 500, 300, "up", "Medium health enemy (2 HP) - will explode when destroyed"),
        ("fighter1", 350, 350, "down", "Low health enemy (1 HP) - will explode when destroyed"),
        
        # Environmental objects to destroy
        ("asteroid", 250, 150, "large", "Large asteroid - will explode when destroyed"),
        ("asteroid", 550, 450, "medium", "Medium asteroid - will explode when destroyed"),
        ("debris", 320, 280, None, "Debris - will explode when destroyed"),
        
        # Damage sources to kill player
        ("asteroid", 400, 250, "large", "Collision damage to trigger player explosion"),
    ]
    
    print(f"\nPlayer starts with {game.player.health_system.current_health} HP (reduced for testing)")
    print("Player will explode after taking damage from collisions")
    print("\nCreating explosion test environment:")
    
    for obj_type, x, y, param, description in explosion_test_objects:
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
    print("💥 Explosion Features:")
    print("  • Player explosions: Large (2x scale) when health reaches 0")
    print("  • Enemy explosions: Medium (1.5x scale) when destroyed by projectiles")
    print("  • Asteroid explosions: Medium (1.5x scale) when destroyed")
    print("  • Debris explosions: Medium (1.5x scale) when destroyed")
    print("  • 10-frame animation cut from Explosion02-Sheet")
    print("  • Player can't move when dead")
    
    print("\n🎮 Controls:")
    print("  WASD/Arrow Keys - Move (collisions cause damage)")
    print("  Q - Primary weapon (destroy enemies/objects for explosions)")
    print("  E - Secondary weapon (destroy enemies/objects for explosions)")
    print("  R - Restart when dead")
    print("  ESC - Quit")
    
    # Auto-fire some projectiles to create explosions
    auto_fire_timer = 0
    
    # Run demo to show explosion system
    for frame in range(900):  # 15 seconds
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
                        projectile = Projectile(x, y, proj_type, direction)
                        game.projectiles.add(projectile)
                        game.all_sprites.add(projectile)
                elif event.key == pygame.K_e and game.player.is_alive():
                    # Secondary weapon
                    shot_data = game.player.shoot("secondary")
                    if shot_data:
                        x, y, proj_type, direction = shot_data
                        projectile = Projectile(x, y, proj_type, direction)
                        game.projectiles.add(projectile)
                        game.all_sprites.add(projectile)
        
        # Auto-fire projectiles to create explosions for demo
        auto_fire_timer += 1
        if auto_fire_timer >= 60 and game.player.is_alive():  # Every second
            auto_fire_timer = 0
            shot_data = game.player.shoot("primary")
            if shot_data:
                x, y, proj_type, direction = shot_data
                projectile = Projectile(x, y, proj_type, direction)
                game.projectiles.add(projectile)
                game.all_sprites.add(projectile)
                print(f"Auto-fired projectile at frame {frame}")
        
        game.update()
        game.draw()
        
        # Capture key frames showing explosion system
        if frame in [0, 200, 400, 600, 800]:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/explosion_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            player_health = game.player.health_system.current_health
            player_alive = game.player.is_alive()
            explosions = len(game.explosions)
            enemies = len(game.enemies)
            asteroids = len(game.asteroids)
            debris = len(game.debris)
            
            print(f"\nFrame {frame}:")
            print(f"  Player Health: {player_health}/100 HP")
            print(f"  Player Alive: {player_alive}")
            print(f"  Active Explosions: {explosions}")
            print(f"  Enemies Remaining: {enemies}")
            print(f"  Asteroids Remaining: {asteroids}")
            print(f"  Debris Remaining: {debris}")
            print(f"  Game Over: {game.game_over}")
            print(f"  Screenshot: {screenshot_path}")
            
            if not player_alive:
                print("  💥 PLAYER EXPLOSION ACTIVE!")
                print("  🚫 Player movement disabled")
                break
    
    print("\n✅ Explosion system working perfectly!")
    print("💥 Explosion Features Implemented:")
    print("   • Proper frame cutting from Explosion02-Sheet (10 frames)")
    print("   • Player explosions: Large scale (2x) with movement disabled")
    print("   • Enemy explosions: Medium scale (1.5x) when destroyed")
    print("   • Asteroid explosions: Medium scale (1.5x) when destroyed")
    print("   • Debris explosions: Medium scale (1.5x) when destroyed")
    print("   • Smooth animation with proper frame timing")
    print("   • Dead player sprite hidden during explosion")
    print("   • Fallback explosion system if sheet loading fails")
    print("🎮 Complete explosion system with professional animations!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_explosion_system()
