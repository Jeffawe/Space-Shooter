#!/usr/bin/env python3
"""
Demo the complete power-up system with HP and Energy containers
"""
import pygame
from game import Game
from powerup import PowerUp
from enemy import Enemy
from constants import *

def demo_powerup_system():
    """Demo the complete power-up system with area effects"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🎁 POWER-UP SYSTEM DEMO")
    print("Testing HP Container (healing) and Energy Container (area destruction)")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Reduce player health for HP testing
    game.player.health_system.current_health = 40
    game.player.health_system.health_bar.current_health = 40
    
    # Create test power-ups
    test_powerups = [
        ("health", 350, 200, "HP Container - heals 30 HP"),
        ("energy", 450, 200, "Energy Container - enhanced projectiles"),
        ("health", 300, 350, "Another HP Container"),
        ("energy", 500, 350, "Another Energy Container"),
    ]
    
    print(f"\nPlayer starts with {game.player.health_system.current_health}/100 HP")
    print("Creating test power-ups:")
    
    for powerup_type, x, y, description in test_powerups:
        powerup = PowerUp(x, y, powerup_type)
        game.powerups.add(powerup)
        game.all_sprites.add(powerup)
        print(f"  {powerup_type} at ({x}, {y}) - {description}")
    
    # Create enemies for energy effect testing
    test_enemies = [
        ("gunship", 200, 150, "down", "Target for energy effects"),
        ("pirate", 300, 150, "down", "Horizontal line target"),
        ("fighter1", 400, 150, "down", "Horizontal line target"),
        ("fighter2", 500, 150, "down", "Horizontal line target"),
        ("crabship", 350, 100, "down", "Vertical line target"),
        ("gunship", 350, 200, "down", "Vertical line target"),
        ("pirate", 350, 250, "down", "Vertical line target"),
        ("fighter1", 250, 100, "down", "Diagonal target"),
        ("fighter2", 450, 200, "down", "Diagonal target"),
    ]
    
    print("\nCreating enemies for energy effect testing:")
    for enemy_type, x, y, direction, description in test_enemies:
        enemy = Enemy(enemy_type, x, y, direction)
        game.enemies.add(enemy)
        game.all_sprites.add(enemy)
        print(f"  {enemy_type} at ({x}, {y}) - {description}")
    
    print(f"\nPlayer positioned at center: ({game.player.rect.centerx}, {game.player.rect.centery})")
    print("🎁 Power-up System Features:")
    print("  💖 HP Container: Heals 30 HP instantly")
    print("  ⚡ Energy Container: Enhanced projectiles for 5 seconds")
    print("    - 40% chance: Horizontal destruction")
    print("    - 30% chance: Vertical destruction") 
    print("    - 25% chance: Diagonal destruction")
    print("    - 5% chance: Screen clear (all enemies!)")
    
    print("\n🎮 Controls:")
    print("  WASD/Arrow Keys - Move to collect power-ups")
    print("  Q/E - Shoot (energy effect triggers on enemy hits)")
    print("  R - Restart")
    print("  ESC - Quit")
    
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
                elif event.key == pygame.K_e and game.player.is_alive():
                    # Secondary weapon
                    shot_data = game.player.shoot("secondary")
                    if shot_data:
                        from projectile import Projectile
                        x, y, proj_type, direction = shot_data
                        projectile = Projectile(x, y, proj_type, direction)
                        game.projectiles.add(projectile)
                        game.all_sprites.add(projectile)
        
        game.update()
        game.draw()
        
        # Capture key frames
        if frame in [0, 300, 600, 900]:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/powerup_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            player_health = game.player.health_system.current_health
            powerups_remaining = len(game.powerups)
            powerups_collected = game.collision_stats['powerups_collected']
            enemies_remaining = len(game.enemies)
            has_energy = game.player.has_energy_effect()
            energy_time = game.player.get_energy_time_remaining()
            
            print(f"\nFrame {frame}:")
            print(f"  Player Health: {player_health}/100 HP")
            print(f"  Power-ups Remaining: {powerups_remaining}")
            print(f"  Power-ups Collected: {powerups_collected}")
            print(f"  Enemies Remaining: {enemies_remaining}")
            print(f"  Energy Effect Active: {has_energy}")
            if has_energy:
                print(f"  Energy Time Remaining: {energy_time:.1f}s")
            print(f"  Screenshot: {screenshot_path}")
            
            if powerups_collected > 0:
                print("  🎁 Power-ups working!")
            if has_energy:
                print("  ⚡ ENERGY BOOST ACTIVE - Enhanced projectiles!")
    
    print("\n✅ Power-up system demo completed!")
    print("🎁 Power-up Features Implemented:")
    print("   💖 HP Container: Instant healing (30 HP)")
    print("   ⚡ Energy Container: Enhanced projectiles with area effects")
    print("   🎯 Area Effect Patterns:")
    print("     - Horizontal: Destroys enemies in horizontal line")
    print("     - Vertical: Destroys enemies in vertical line")
    print("     - Diagonal: Destroys enemies on diagonal lines")
    print("     - Screen Clear: Destroys ALL enemies (rare!)")
    print("   ⏱️ Timed Effects: Energy boost lasts 5 seconds")
    print("   🎮 Automatic Spawning: Power-ups spawn randomly during gameplay")
    print("🚀 Complete power-up system with strategic gameplay elements!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_powerup_system()
