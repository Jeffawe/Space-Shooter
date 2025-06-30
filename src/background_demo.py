#!/usr/bin/env python3
"""
Demo the scrolling background system
"""
import pygame
from game import Game

def demo_background():
    """Demo the background scrolling"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    # Simulate some scrolling by moving the player up and down
    print("🌌 SCROLLING BACKGROUND DEMO")
    print("Background size:", game.background.bg_width, "x", game.background.bg_height)
    print("Max scroll distance:", game.background.max_scroll)
    
    # Take screenshots at different scroll positions
    positions = [0, 0.25, 0.5, 0.75, 1.0]
    
    for i, pos in enumerate(positions):
        # Set scroll position
        game.background.scroll_y = int(pos * game.background.max_scroll)
        
        # Update and draw
        game.update()
        game.draw()
        
        # Save screenshot
        screenshot_path = f"assets/images/background_demo_{i}.png"
        pygame.image.save(game.screen, screenshot_path)
        print(f"Screenshot {i+1}/5: Scroll {pos:.0%} - {screenshot_path}")
    
    print("\n✅ Background system working!")
    print("🎮 Use W/S or UP/DOWN arrows to scroll the background!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_background()
