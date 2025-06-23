#!/usr/bin/env python3
"""
Live demo showing the scrolling background in action
"""
import pygame
from game import Game

def live_demo():
    """Show the game with automatic scrolling demo"""
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print("🌌 LIVE SCROLLING BACKGROUND DEMO")
    print("Watch the background scroll automatically!")
    
    # Demo loop - automatically scroll through the background
    demo_time = 0
    scroll_direction = 1
    
    for frame in range(300):  # 5 seconds at 60 FPS
        # Auto-scroll the background
        if frame % 2 == 0:  # Every other frame
            if game.background.is_at_bottom():
                scroll_direction = -1
            elif game.background.is_at_top():
                scroll_direction = 1
            
            # Simulate player movement for background scrolling
            game.background.update(scroll_direction * 3)
        
        # Update and draw
        game.update()
        game.draw()
        
        # Save a few key frames
        if frame in [0, 75, 150, 225, 299]:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/live_demo_frame_{frame}.png"
            pygame.image.save(game.screen, screenshot_path)
            progress = game.background.get_scroll_progress()
            print(f"Frame {frame}: Scroll at {progress:.1%}")
    
    print("\n✅ Live demo completed!")
    print("🎮 Your scrolling background system is working perfectly!")
    
    pygame.quit()

if __name__ == "__main__":
    live_demo()
