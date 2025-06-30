#!/usr/bin/env python3
"""
Demo the starfield background with key-press scrolling
"""
import pygame
from game import Game

def demo_starfield():
    """Demo the starfield background system"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("⭐ STARFIELD BACKGROUND DEMO")
    print("Background now uses only the beautiful starfield sections!")
    print("Scrolling requires being in zone AND pressing W/S keys")
    
    # Take screenshots at different positions
    test_scenarios = [
        (400, 300, "Middle zone - no scrolling"),
        (400, 100, "Upper zone - ready for W key scrolling"),
        (400, 500, "Lower zone - ready for S key scrolling"),
    ]
    
    for i, (x, y, description) in enumerate(test_scenarios):
        # Position player
        game.player.rect.centerx = x
        game.player.rect.centery = y
        
        # Update and draw
        game.update()
        game.draw()
        
        # Save screenshot
        screenshot_path = f"assets/images/starfield_demo_{i}.png"
        pygame.image.save(game.screen, screenshot_path)
        
        print(f"Screenshot {i+1}: {description}")
        print(f"  Position: ({x}, {y})")
        print(f"  File: {screenshot_path}")
    
    print("\n✅ Starfield background system complete!")
    print("🌟 Beautiful star background with scattered white stars!")
    print("🎮 Hold W in upper zone or S in lower zone to scroll!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_starfield()
