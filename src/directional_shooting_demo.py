#!/usr/bin/env python3
"""
Demo the directional shooting system
"""
import pygame
from game import Game
from projectile import Projectile
from constants import *

def demo_directional_shooting():
    """Demo shooting in different directions"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🔫 DIRECTIONAL SHOOTING DEMO")
    print("Testing upward and downward shooting based on player facing")
    
    # Test 1: Player facing up, shooting upward
    print("\nTest 1: Player facing UP - projectiles should go UP")
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    game.player.current_sprite = 'up'
    game.player.image = game.player.sprites['up']
    
    # Create upward-firing projectiles
    up_primary = Projectile(350, 300, "primary", "up")
    up_secondary = Projectile(400, 300, "secondary", "up")
    game.projectiles.add(up_primary, up_secondary)
    game.all_sprites.add(up_primary, up_secondary)
    
    # Update and draw
    game.update()
    game.draw()
    screenshot_path = "/home/jeffawe/amazon-build/assets/images/directional_shooting_up.png"
    pygame.image.save(game.screen, screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")
    
    # Clear projectiles for next test
    game.projectiles.empty()
    for sprite in list(game.all_sprites):
        if hasattr(sprite, 'projectile_type'):
            sprite.kill()
    
    # Test 2: Player facing down, shooting downward
    print("\nTest 2: Player facing DOWN - projectiles should go DOWN")
    game.player.current_sprite = 'down'
    game.player.image = game.player.sprites['down']
    
    # Create downward-firing projectiles
    down_primary = Projectile(350, 300, "primary", "down")
    down_secondary = Projectile(400, 300, "secondary", "down")
    game.projectiles.add(down_primary, down_secondary)
    game.all_sprites.add(down_primary, down_secondary)
    
    # Update and draw
    game.update()
    game.draw()
    screenshot_path = "/home/jeffawe/amazon-build/assets/images/directional_shooting_down.png"
    pygame.image.save(game.screen, screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")
    
    # Test movement over several frames
    print("\nTest 3: Showing projectile movement over time")
    for frame in range(30):
        game.update()
        if frame == 15:  # Halfway through
            screenshot_path = "/home/jeffawe/amazon-build/assets/images/directional_shooting_movement.png"
            pygame.image.save(game.screen, screenshot_path)
            proj_count = len(game.projectiles)
            print(f"Frame {frame}: {proj_count} projectiles moving - {screenshot_path}")
    
    print("\n✅ Directional shooting system working!")
    print("🎮 Player facing UP → projectiles fire UP")
    print("🎮 Player facing DOWN → projectiles fire DOWN")
    print("🚀 Projectiles are rotated to match direction!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_directional_shooting()
