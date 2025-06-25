#!/usr/bin/env python3
"""
Debug the dialogue to wave transition issue
"""
import pygame
from game import Game
from constants import *

def debug_transition():
    """Debug why waves don't start after dialogue"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🔍 DEBUGGING DIALOGUE TO WAVE TRANSITION")
    print("Investigating why waves don't start after dialogue ends")
    
    # Fast-forward through dialogue
    frame_count = 0
    dialogue_ended_frame = None
    
    while game.running and frame_count < 1200:  # 20 seconds max
        # Fast advance through dialogue
        if game.dialogue_system.is_active() and frame_count % 30 == 0:  # Every 0.5 seconds
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
        
        # Handle events
        game.handle_events()
        
        # Check transition conditions before update
        if dialogue_ended_frame is None and not game.dialogue_system.is_active() and game.game_started:
            dialogue_ended_frame = frame_count
            print(f"\n🎬 DIALOGUE ENDED at frame {frame_count}")
            print(f"   Story mode: {game.story_mode}")
            print(f"   Game started: {game.game_started}")
            print(f"   Dialogue active: {game.dialogue_system.is_active()}")
            print(f"   Wave info before update: {game.wave_manager.get_wave_info()}")
            
            # Check the exact transition condition
            condition1 = game.story_mode
            condition2 = game.game_started
            condition3 = not game.dialogue_system.is_active()
            condition4 = not game.wave_manager.get_wave_info()
            
            print(f"\n🔍 TRANSITION CONDITIONS:")
            print(f"   story_mode: {condition1}")
            print(f"   game_started: {condition2}")
            print(f"   not dialogue_active: {condition3}")
            print(f"   not wave_info: {condition4}")
            print(f"   ALL CONDITIONS MET: {condition1 and condition2 and condition3 and condition4}")
        
        game.update()
        game.draw()
        
        # Monitor after dialogue ends
        if dialogue_ended_frame is not None:
            frames_since_end = frame_count - dialogue_ended_frame
            wave_info = game.wave_manager.get_wave_info()
            
            if frames_since_end % 60 == 0:  # Every second after dialogue ends
                print(f"\n⏱️ {frames_since_end//60}s after dialogue ended:")
                print(f"   Wave info: {wave_info}")
                print(f"   Story mode: {game.story_mode}")
                print(f"   Game started: {game.game_started}")
                print(f"   Dialogue active: {game.dialogue_system.is_active()}")
                
                if wave_info:
                    print("   ✅ Wave started!")
                    break
                else:
                    print("   ❌ Still no wave...")
        
        frame_count += 1
    
    print("\n🔍 DEBUG COMPLETE")
    
    final_wave_info = game.wave_manager.get_wave_info()
    if final_wave_info:
        print("✅ Wave eventually started:")
        print(f"   {final_wave_info}")
    else:
        print("❌ Wave never started - investigating wave manager...")
        
        # Let's check the wave manager state
        print(f"\nWave Manager Debug:")
        print(f"   Current wave: {getattr(game.wave_manager, 'current_wave', 'Not found')}")
        print(f"   Wave active: {getattr(game.wave_manager, 'wave_active', 'Not found')}")
        print(f"   Wave intro active: {getattr(game.wave_manager, 'wave_intro_active', 'Not found')}")
    
    pygame.quit()

if __name__ == "__main__":
    debug_transition()
