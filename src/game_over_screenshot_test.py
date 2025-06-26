#!/usr/bin/env python3
"""
Capture screenshot of game over screen with failure dialogue
"""
import pygame
from game import Game
from constants import *

def capture_game_over_screenshot():
    """Capture a screenshot of the game over screen with dialogue"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("📸 GAME OVER SCREENSHOT CAPTURE")
    print("Automatically capturing game over screen with failure dialogue")
    
    # Force game over state with dialogue
    print("\n🎮 Setting up game over state...")
    
    # Set up game over state
    game.game_over = True
    game.player_death_timer = 0  # Ready for restart
    
    # Start failure dialogue
    game.dialogue_system.start_dialogue('wave_failed')
    print("💬 Failure dialogue started")
    
    # Add some fake statistics
    game.collision_stats['enemies_destroyed'] = 15
    game.collision_stats['projectile_hits'] = 42
    
    print("📊 Game statistics set")
    
    # Capture screenshot
    screenshot_count = 0
    
    for i in range(5):  # Capture a few frames
        game.update()
        game.draw()
        
        screenshot_path = f"/home/jeffawe/amazon-build/assets/images/game_over_dialogue_{i}.png"
        pygame.image.save(game.screen, screenshot_path)
        print(f"📸 Screenshot {i+1} saved: {screenshot_path}")
        
        # Advance dialogue for next screenshot
        if i < 4:  # Don't advance on last iteration
            game.dialogue_system.advance_dialogue()
    
    print(f"\n✅ Game Over Screen Screenshots Captured!")
    print(f"📁 Location: /home/jeffawe/amazon-build/assets/images/")
    print(f"🖼️ Files: game_over_dialogue_0.png through game_over_dialogue_4.png")
    
    print(f"\n🎬 Screenshot Features:")
    print(f"   • Game over screen with semi-transparent overlay")
    print(f"   • 'GAME OVER' text in red at top")
    print(f"   • Player statistics (enemies destroyed, hits)")
    print(f"   • Failure dialogue box at bottom with red border")
    print(f"   • Duke's farewell message with proper text wrapping")
    print(f"   • 'Press SPACE to continue' instruction")
    print(f"   • 'Press R to Restart or ESC to Quit' when dialogue complete")
    
    pygame.quit()

if __name__ == "__main__":
    capture_game_over_screenshot()
