#!/usr/bin/env python3
"""
Demo the floating power-up system with containers spawning from screen edges
"""
import pygame
from game import Game
from powerup import PowerUp
from constants import *

def demo_floating_powerups():
    """Demo power-ups floating from screen edges"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🎁 FLOATING POWER-UP SYSTEM DEMO")
    print("Testing containers spawning from screen edges and floating naturally")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Reduce player health for HP testing
    game.player.health_system.current_health = 50
    game.player.health_system.health_bar.current_health = 50
    
    # Create test power-ups from different screen edges
    test_powerups = [
        ("health", -30, 150, "left", "HP Container from left edge"),
        ("energy", SCREEN_WIDTH + 30, 250, "right", "Energy Container from right edge"),
        ("health", 200, -30, "top", "HP Container from top edge"),
        ("energy", 600, SCREEN_HEIGHT + 30, "bottom", "Energy Container from bottom edge"),
        ("health", -30, 400, "left", "Another HP Container from left"),
        ("energy", SCREEN_WIDTH + 30, 100, "right", "Another Energy Container from right"),
    ]
    
    print(f"\nPlayer starts with {game.player.health_system.current_health}/100 HP")
    print("Creating floating power-ups from screen edges:")
    
    for powerup_type, x, y, spawn_side, description in test_powerups:
        powerup = PowerUp(x, y, powerup_type, spawn_side)
        game.powerups.add(powerup)
        game.all_sprites.add(powerup)
        print(f"  {powerup_type} from {spawn_side} at ({x}, {y}) - {description}")
    
    print(f"\nPlayer positioned at center: ({game.player.rect.centerx}, {game.player.rect.centery})")
    print("🎁 Floating Power-up Features:")
    print("  🌊 Natural floating movement with gentle up/down bobbing")
    print("  ➡️ Containers drift across screen from spawn edges")
    print("  🎯 Can be collected by moving into their path")
    print("  🌪️ Will drift off-screen if not collected")
    print("  ⏱️ 20-second lifetime before expiring")
    
    print("\n🎮 Controls:")
    print("  WASD/Arrow Keys - Move to intercept floating power-ups")
    print("  Q/E - Shoot")
    print("  R - Restart")
    print("  ESC - Quit")
    print("  Watch power-ups float naturally across the screen!")
    
    # Run demo
    for frame in range(1200):  # 20 seconds
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
                    # Primary weapon
                    shot_data = game.player.shoot("primary")
                    if shot_data:
                        from projectile import Projectile
                        x, y, proj_type, direction = shot_data
                        projectile = Projectile(x, y, proj_type, direction)
                        game.projectiles.add(projectile)
                        game.all_sprites.add(projectile)
        
        game.update()
        game.draw()
        
        # Capture key frames showing floating movement
        if frame in [0, 200, 400, 600, 800, 1000]:
            screenshot_path = f"assets/images/floating_powerup_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            player_health = game.player.health_system.current_health
            powerups_remaining = len(game.powerups)
            powerups_collected = game.collision_stats['powerups_collected']
            has_energy = game.player.has_energy_effect()
            
            print(f"\nFrame {frame}:")
            print(f"  Player Health: {player_health}/100 HP")
            print(f"  Power-ups Floating: {powerups_remaining}")
            print(f"  Power-ups Collected: {powerups_collected}")
            print(f"  Energy Effect Active: {has_energy}")
            print(f"  Screenshot: {screenshot_path}")
            
            if powerups_collected > 0:
                print("  🎁 Power-up collection working!")
            if has_energy:
                print("  ⚡ ENERGY BOOST ACTIVE!")
    
    print("\n✅ Floating power-up system demo completed!")
    print("🌊 Floating Movement Features:")
    print("   ➡️ Power-ups spawn from screen edges (left, right, top, bottom)")
    print("   🌊 Natural drift movement across screen")
    print("   🎈 Gentle floating animation with up/down bobbing")
    print("   🎯 Players must intercept them as they float by")
    print("   🌪️ Containers drift off-screen if not collected")
    print("   ⏱️ 20-second lifetime for collection opportunity")
    print("🎮 Creates dynamic, organic power-up collection gameplay!")
    print("🚀 Power-ups now feel like natural floating objects in space!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_floating_powerups()
