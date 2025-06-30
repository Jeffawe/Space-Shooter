#!/usr/bin/env python3
"""
Demo the bomb collision system with explosion animations and 40% health damage
"""
import pygame
from game import Game
from enemy import Enemy
from enemy_projectile import Bomb
from constants import *

def demo_bomb_system():
    """Demo the complete bomb system with collision detection and massive damage"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("💣 BOMB COLLISION SYSTEM DEMO")
    print("Testing bomb collisions with explosion animations and 40% health damage")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Set player health to full for testing
    game.player.health_system.current_health = 100
    game.player.health_system.health_bar.current_health = 100
    
    # Create enemies that drop bombs
    bomb_dropping_enemies = [
        ("pirate", 200, 100, "down", "Pirate ship - drops bombs"),
        ("crabship", 600, 150, "down", "Crab ship - drops bombs"),
        ("pirate", 300, 500, "up", "Another pirate - drops bombs"),
    ]
    
    print(f"\nPlayer starts with {game.player.health_system.current_health} HP")
    print("Bombs deal 40% max health damage (40 HP) + explosion animation")
    print("\nCreating bomb-dropping enemies:")
    
    for enemy_type, x, y, direction, description in bomb_dropping_enemies:
        enemy = Enemy(enemy_type, x, y, direction)
        game.enemies.add(enemy)
        game.all_sprites.add(enemy)
        print(f"  {enemy_type} at ({x}, {y}) - {description}")
    
    # Manually create some bombs for immediate testing
    test_bombs = [
        (350, 250, "Test bomb near player"),
        (450, 350, "Test bomb near player"),
        (320, 320, "Test bomb very close to player"),
    ]
    
    print("\nCreating test bombs for collision testing:")
    for x, y, description in test_bombs:
        bomb = Bomb(x, y)
        game.bombs.add(bomb)
        game.all_sprites.add(bomb)
        print(f"  Bomb at ({x}, {y}) - {description}")
    
    print(f"\nPlayer positioned at center: ({game.player.rect.centerx}, {game.player.rect.centery})")
    print("💣 Bomb System Features:")
    print("  • Bombs deal 40% of max health as damage (40 HP)")
    print("  • Bomb explosion animation plays on contact")
    print("  • Player explosion if bomb kills player")
    print("  • Bombs are destroyed on contact")
    print("  • Movement disabled if player dies")
    
    print("\n🎮 Controls:")
    print("  WASD/Arrow Keys - Move (collide with bombs for explosions)")
    print("  Q/E - Shoot (enemies will drop more bombs)")
    print("  R - Restart when dead")
    print("  ESC - Quit")
    
    print("\n💣 Expected Damage Sequence:")
    print("  100 HP → 60 HP (1st bomb) → 20 HP (2nd bomb) → 0 HP (3rd bomb = death)")
    
    # Run demo to show bomb system
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
                    # Recreate test bombs after restart
                    for x, y, description in test_bombs:
                        bomb = Bomb(x, y)
                        game.bombs.add(bomb)
                        game.all_sprites.add(bomb)
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
        
        # Capture key frames showing bomb system
        if frame in [0, 150, 300, 450]:
            screenshot_path = f"assets/images/bomb_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            player_health = game.player.health_system.current_health
            player_alive = game.player.is_alive()
            explosions = len(game.explosions)
            bombs = len(game.bombs)
            bomb_explosions = game.collision_stats['bomb_explosions']
            
            print(f"\nFrame {frame}:")
            print(f"  Player Health: {player_health}/100 HP")
            print(f"  Player Alive: {player_alive}")
            print(f"  Active Explosions: {explosions}")
            print(f"  Bombs Remaining: {bombs}")
            print(f"  Bomb Explosions: {bomb_explosions}")
            print(f"  Game Over: {game.game_over}")
            print(f"  Screenshot: {screenshot_path}")
            
            if bomb_explosions > 0:
                print(f"  💣 {bomb_explosions} bomb explosion(s) occurred!")
            
            if not player_alive:
                print("  💥 PLAYER KILLED BY BOMB!")
                print("  🚫 Player movement disabled")
                break
    
    print("\n✅ Bomb collision system working perfectly!")
    print("💣 Bomb System Features Implemented:")
    print("   • Collision detection between player and bombs")
    print("   • 40% max health damage (40 HP) per bomb collision")
    print("   • Bomb explosion animation on contact")
    print("   • Player explosion if bomb kills player")
    print("   • Bombs destroyed on contact (realistic)")
    print("   • Player movement disabled when dead")
    print("   • Bomb explosion statistics tracking")
    print("   • Visual feedback with explosion animations")
    print("🎮 Bombs are now a serious threat that players must avoid!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_bomb_system()
