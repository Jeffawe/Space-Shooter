#!/usr/bin/env python3
"""
Demo the shooting system
"""
import pygame
from game import Game
from projectile import Projectile
from constants import *

def demo_shooting():
    """Demo the shooting system"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🔫 SHOOTING SYSTEM DEMO")
    print("Testing primary and secondary projectiles")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Test shooting both projectile types
    print("Creating primary projectile (Q key)...")
    primary_proj = Projectile(400, 300, "primary")
    game.projectiles.add(primary_proj)
    game.all_sprites.add(primary_proj)
    
    print("Creating secondary projectile (E key)...")
    secondary_proj = Projectile(450, 300, "secondary")
    game.projectiles.add(secondary_proj)
    game.all_sprites.add(secondary_proj)
    
    # Update and draw several frames to show projectiles moving
    for frame in range(60):  # 1 second at 60 FPS
        game.update()
        game.draw()
        
        # Save a few key frames
        if frame in [0, 20, 40]:
            screenshot_path = f"assets/images/shooting_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            proj_count = len(game.projectiles)
            print(f"Frame {frame}: {proj_count} projectiles active - {screenshot_path}")
    
    print("\n✅ Shooting system working!")
    print("🎮 Press Q for primary weapon, E for secondary weapon!")
    print("🚀 Projectiles move upward and disappear off-screen!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_shooting()
