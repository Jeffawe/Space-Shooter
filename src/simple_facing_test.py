#!/usr/bin/env python3
"""
Simple test to verify directional facing works
"""
import pygame
from game import Game
from constants import *

def test_facing():
    """Test the facing system by checking sprite changes"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🚀 TESTING DIRECTIONAL FACING")
    
    # Position player in center
    game.player.rect.centerx = SCREEN_WIDTH // 2
    game.player.rect.centery = SCREEN_HEIGHT // 2
    
    # Test 1: Default state
    game.update()
    game.draw()
    screenshot_path = "assets/images/facing_test_default.png"
    pygame.image.save(game.screen, screenshot_path)
    print(f"Default: Current sprite = {game.player.current_sprite}")
    
    # Test 2: Check if we have the down sprite
    print(f"Available sprites: {list(game.player.sprites.keys())}")
    
    # Test 3: Manually set sprite to down to verify it exists
    game.player.current_sprite = 'down'
    game.player.image = game.player.sprites['down']
    game.draw()
    screenshot_path = "assets/images/facing_test_down.png"
    pygame.image.save(game.screen, screenshot_path)
    print("Manually set to down sprite - screenshot saved")
    
    pygame.quit()

if __name__ == "__main__":
    test_facing()
