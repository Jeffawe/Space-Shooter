#!/usr/bin/env python3
"""
Demo the layered background system showing depth effect
"""
import pygame
from game import Game

def demo_layered_background():
    """Demo the layered background with depth"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🌌 LAYERED BACKGROUND DEMO")
    print("Showing background/foreground separation with depth!")
    
    # Demo different scroll positions to show the layering effect
    scroll_positions = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    
    for i, pos in enumerate(scroll_positions):
        # Set scroll position
        game.background.scroll_y = int(pos * game.background.max_scroll)
        
        # Update and draw
        game.update()
        game.draw()
        
        # Save screenshot
        screenshot_path = f"assets/images/layered_demo_{i}.png"
        pygame.image.save(game.screen, screenshot_path)
        
        scroll_percent = game.background.get_scroll_progress()
        print(f"Screenshot {i+1}/6: Scroll {scroll_percent:.1%} - {screenshot_path}")
    
    print("\n✅ Layered background system complete!")
    print("🎮 Background and foreground layers now properly separated!")
    print("🌟 Player flies behind nebula clouds for depth effect!")
    
    pygame.quit()

if __name__ == "__main__":
    demo_layered_background()
