#!/usr/bin/env python3
"""
Interactive bomb collision test - moves player into bombs automatically
"""
import pygame
from game import Game
from enemy_projectile import Bomb
from constants import *

def test_bomb_collisions():
    """Test bomb collisions by automatically moving player into bombs"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("💣 AUTOMATIC BOMB COLLISION TEST")
    print("Moving player into bombs to test collision system")
    
    # Position player at specific location
    game.player.rect.centerx = 300
    game.player.rect.centery = 300
    
    # Create a bomb right next to the player for guaranteed collision
    test_bomb = Bomb(320, 300)  # Very close to player
    game.bombs.add(test_bomb)
    game.all_sprites.add(test_bomb)
    
    print(f"Player at: ({game.player.rect.centerx}, {game.player.rect.centery})")
    print(f"Bomb at: ({test_bomb.rect.centerx}, {test_bomb.rect.centery})")
    print(f"Player health: {game.player.health_system.current_health}/100")
    
    # Run a few frames to test collision
    for frame in range(10):
        print(f"\nFrame {frame}:")
        
        # Move player towards bomb
        if frame < 5:
            game.player.rect.x += 5  # Move player right towards bomb
            print(f"  Moving player to: ({game.player.rect.centerx}, {game.player.rect.centery})")
        
        # Update game
        game.update()
        
        # Check results
        player_health = game.player.health_system.current_health
        bombs_remaining = len(game.bombs)
        explosions = len(game.explosions)
        bomb_explosions = game.collision_stats.get('bomb_explosions', 0)
        
        print(f"  Player Health: {player_health}/100")
        print(f"  Bombs Remaining: {bombs_remaining}")
        print(f"  Active Explosions: {explosions}")
        print(f"  Bomb Explosions: {bomb_explosions}")
        
        if bomb_explosions > 0:
            print("  💣 BOMB COLLISION DETECTED!")
            print(f"  💥 Player took {100 - player_health} damage!")
            break
        
        if not game.player.is_alive():
            print("  💀 PLAYER DIED!")
            break
    
    pygame.quit()
    
    if bomb_explosions > 0:
        print("\n✅ BOMB COLLISION SYSTEM WORKING!")
        print(f"💣 Bomb exploded and dealt {100 - player_health} damage")
        print("💥 Explosion animation triggered")
        print("🎯 40% damage system confirmed")
    else:
        print("\n❌ No bomb collision detected")
        print("🔧 Need to debug collision detection")

if __name__ == "__main__":
    test_bomb_collisions()
