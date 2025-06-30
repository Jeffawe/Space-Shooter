#!/usr/bin/env python3
"""
Create a screenshot of the game for demo purposes
"""
import pygame
import sys
from game import Game

def create_screenshot():
    """Create a screenshot of the game"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    # Run a few update cycles to position everything
    for _ in range(5):
        game.update()
    
    # Draw the current state
    game.draw()
    
    # Save screenshot
    screenshot_path = "assets/images/game_screenshot.png"
    pygame.image.save(game.screen, screenshot_path)
    print(f"Screenshot saved to: {screenshot_path}")
    
    # Show game info
    print("\n🎮 SPACE SHOOTER - CURRENT STATUS:")
    print("✅ Player ship with tilt animations")
    print("✅ Smooth WASD/Arrow key movement")
    print("✅ Screen boundary collision")
    print("✅ 60 FPS gameplay")
    print("✅ Professional sprite system")
    print("\n🎯 READY FOR: Shooting, Enemies, Backgrounds!")
    
    pygame.quit()

if __name__ == "__main__":
    create_screenshot()
