#!/usr/bin/env python3
"""
Visual test of game over screen with failure dialogue
"""
import pygame
from game import Game
from constants import *

def visual_game_over_test():
    """Visual test to see the game over screen with dialogue"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("👁️ VISUAL GAME OVER SCREEN TEST")
    print("Manual test to see the failure dialogue on game over screen")
    
    print("\n🎮 Instructions:")
    print("  1. Game will start in story mode")
    print("  2. Press SPACE to advance through opening dialogue quickly")
    print("  3. Press SPACE to start Wave 1")
    print("  4. Let enemies kill the player (don't move or shoot)")
    print("  5. Observe the game over screen with failure dialogue")
    print("  6. Press SPACE to advance the failure dialogue")
    print("  7. Press R to restart or ESC to quit")
    
    print("\n🔍 What to Look For:")
    print("  • Game over screen with statistics")
    print("  • Red-bordered dialogue box at bottom")
    print("  • Duke's failure message about defenses falling")
    print("  • Proper text wrapping and formatting")
    print("  • SPACE to advance dialogue functionality")
    
    print("\nPress ENTER to start the visual test...")
    input()
    
    # Run the game normally for manual testing
    frame_count = 0
    dialogue_shown = False
    
    while game.running:
        # Handle events normally
        game.handle_events()
        game.update()
        game.draw()
        
        # Monitor for game over with dialogue
        if game.game_over and game.dialogue_system.is_active() and not dialogue_shown:
            dialogue_shown = True
            speaker = game.dialogue_system.get_current_speaker()
            text = game.dialogue_system.get_current_text()
            print(f"\n💀 GAME OVER DIALOGUE DETECTED!")
            print(f"   Speaker: {speaker}")
            print(f"   Text: {text[:100]}...")
            print(f"   Full message length: {len(text)} characters")
            print(f"   🎮 You should see the dialogue at the bottom of the game over screen!")
        
        # Provide status updates
        if frame_count % 600 == 0:  # Every 10 seconds
            if not game.game_over:
                wave_info = game.wave_manager.get_wave_info()
                dialogue_active = game.dialogue_system.is_active()
                
                if dialogue_active:
                    print(f"📖 Opening dialogue in progress...")
                elif wave_info:
                    if wave_info.get('wave_intro_active', False):
                        print(f"🌊 Wave {wave_info['wave_number']} intro - Press SPACE to start")
                    elif wave_info.get('wave_active', False):
                        time_left = wave_info.get('time_remaining', 0)
                        print(f"⚔️ Wave {wave_info['wave_number']} active - {time_left:.1f}s left")
                else:
                    print(f"🎮 Ready for gameplay...")
            else:
                dialogue_active = game.dialogue_system.is_active()
                if dialogue_active:
                    print(f"💀 Game over with failure dialogue active")
                else:
                    print(f"💀 Game over - Press R to restart")
        
        frame_count += 1
    
    print("\n👁️ Visual test completed!")
    pygame.quit()

if __name__ == "__main__":
    visual_game_over_test()
