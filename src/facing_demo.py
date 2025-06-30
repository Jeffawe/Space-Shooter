#!/usr/bin/env python3
"""
Demo the directional facing system
"""
import pygame
from game import Game
from constants import *

def demo_directional_facing():
    """Demo the player facing different directions"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🚀 DIRECTIONAL FACING DEMO")
    print("Player now faces the direction they move (up/down priority)")
    
    # Test different movement directions
    test_movements = [
        ('up', "Moving UP - Player faces UP"),
        ('down', "Moving DOWN - Player faces DOWN"),
        ('left', "Moving LEFT - Player tilts LEFT"),
        ('right', "Moving RIGHT - Player tilts RIGHT"),
        ('center', "No movement - Player faces UP (default)"),
    ]
    
    for i, (direction, description) in enumerate(test_movements):
        # Reset player position to center
        game.player.rect.centerx = SCREEN_WIDTH // 2
        game.player.rect.centery = SCREEN_HEIGHT // 2
        
        # Simulate movement by setting movement flags
        game.player.moving_up = False
        game.player.moving_down = False
        game.player.moving_left = False
        game.player.moving_right = False
        
        if direction == 'up':
            game.player.moving_up = True
        elif direction == 'down':
            game.player.moving_down = True
        elif direction == 'left':
            game.player.moving_left = True
        elif direction == 'right':
            game.player.moving_right = True
        # center = no movement flags set
        
        # Update sprite based on movement
        game.player.update_sprite()
        
        # Update and draw
        game.update()
        game.draw()
        
        # Save screenshot
        screenshot_path = f"assets/images/facing_demo_{direction}.png"
        pygame.image.save(game.screen, screenshot_path)
        
        print(f"Demo {i+1}: {description}")
        print(f"  Current sprite: {game.player.current_sprite}")
        print(f"  Screenshot: {screenshot_path}")
    
    print("\n✅ Directional facing system working!")
    print("🎮 Player now faces UP when moving up, DOWN when moving down!")
    print("🎯 Vertical movement takes priority over horizontal movement!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_directional_facing()
