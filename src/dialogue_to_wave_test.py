#!/usr/bin/env python3
"""
Test the transition from opening dialogue to Wave 1
"""
import pygame
from game import Game
from constants import *

def test_dialogue_to_wave_transition():
    """Test that Wave 1 starts after opening dialogue completes"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🎬 DIALOGUE TO WAVE TRANSITION TEST")
    print("Testing automatic transition from opening dialogue to Wave 1")
    
    print("\n🎯 Expected Flow:")
    print("  1. Opening dialogue (23 lines)")
    print("  2. Dialogue closes automatically after last line")
    print("  3. Wave 1 intro screen appears automatically")
    print("  4. Player can press SPACE to start Wave 1")
    
    # Fast-forward through dialogue
    dialogue_completed = False
    wave_started = False
    frame_count = 0
    
    while game.running and frame_count < 1800:  # 30 seconds max
        # Fast advance through dialogue
        if game.dialogue_system.is_active() and frame_count % 30 == 0:  # Every 0.5 seconds
            # Simulate SPACE key press
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
        
        # Handle events
        game.handle_events()
        game.update()
        game.draw()
        
        # Check for dialogue completion
        if not dialogue_completed and not game.dialogue_system.is_active() and game.game_started:
            dialogue_completed = True
            print("✅ DIALOGUE COMPLETED!")
            print(f"   Frame: {frame_count}")
            print(f"   Story mode: {game.story_mode}")
            print(f"   Game started: {game.game_started}")
            print(f"   Dialogue active: {game.dialogue_system.is_active()}")
            print(f"   Wave info: {game.wave_manager.get_wave_info()}")
        
        # Check for wave start
        wave_info = game.wave_manager.get_wave_info()
        if not wave_started and wave_info:
            wave_started = True
            print("🌊 WAVE 1 INTRO STARTED!")
            print(f"   Frame: {frame_count}")
            print(f"   Wave info: {wave_info}")
            
            # Try to start the wave
            if wave_info.get('wave_intro_active', False):
                print("   Pressing SPACE to start wave...")
                space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                pygame.event.post(space_event)
        
        # Status updates
        if frame_count % 300 == 0:  # Every 5 seconds
            dialogue_active = game.dialogue_system.is_active()
            wave_info = game.wave_manager.get_wave_info()
            
            print(f"\n--- Frame {frame_count} Status ---")
            print(f"Dialogue completed: {dialogue_completed}")
            print(f"Wave started: {wave_started}")
            
            if dialogue_active:
                speaker = game.dialogue_system.get_current_speaker()
                line_num = game.dialogue_system.current_line_index + 1
                total_lines = len(game.dialogue_system.current_dialogue) if game.dialogue_system.current_dialogue else 0
                print(f"💬 DIALOGUE: {speaker} (Line {line_num}/{total_lines})")
            elif wave_info:
                if wave_info.get('wave_intro_active', False):
                    print(f"🌊 WAVE {wave_info['wave_number']} INTRO")
                elif wave_info.get('wave_active', False):
                    time_left = wave_info.get('time_remaining', 0)
                    print(f"⚔️ WAVE {wave_info['wave_number']} ACTIVE - {time_left:.1f}s remaining")
                elif wave_info.get('wave_complete', False):
                    print(f"✅ WAVE {wave_info['wave_number']} COMPLETE")
            else:
                print("🎮 WAITING FOR WAVE START...")
                print(f"   Story mode: {game.story_mode}")
                print(f"   Game started: {game.game_started}")
                print(f"   Dialogue active: {game.dialogue_system.is_active()}")
        
        frame_count += 1
    
    print("\n🎬 DIALOGUE TO WAVE TRANSITION TEST COMPLETED!")
    
    print("\n✅ Results:")
    if dialogue_completed:
        print("   💬 Opening dialogue completed successfully")
    else:
        print("   ⚠️ Opening dialogue did not complete")
    
    if wave_started:
        print("   🌊 Wave 1 intro started successfully")
        print("   ✅ Transition working correctly")
    else:
        print("   ⚠️ Wave 1 intro did not start")
        print("   🔧 Transition needs debugging")
    
    final_wave_info = game.wave_manager.get_wave_info()
    if final_wave_info:
        print(f"\n🌊 Final Wave State:")
        print(f"   Wave number: {final_wave_info.get('wave_number', 'Unknown')}")
        print(f"   Intro active: {final_wave_info.get('wave_intro_active', False)}")
        print(f"   Wave active: {final_wave_info.get('wave_active', False)}")
        print(f"   Wave complete: {final_wave_info.get('wave_complete', False)}")
    
    pygame.quit()

if __name__ == "__main__":
    test_dialogue_to_wave_transition()
