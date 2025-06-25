#!/usr/bin/env python3
"""
Test the complete dialogue flow and wave progression
"""
import pygame
from game import Game
from constants import *

def test_dialogue_flow():
    """Test the complete dialogue flow from start to waves"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("💬 COMPLETE DIALOGUE FLOW TEST")
    print("Testing dialogue sequence and wave progression")
    
    print("\n🎬 Expected Flow:")
    print("  1. Opening dialogue (23 lines) - Operator, Pilot, Duke conversation")
    print("  2. Wave 1 intro screen - 'Press SPACE to begin wave'")
    print("  3. Wave 1 active gameplay")
    print("  4. Wave 1 complete - Post-wave dialogue")
    print("  5. Continue through waves with dialogue at waves 7 and 10")
    print("  6. Failure dialogue if any wave fails")
    
    print("\n🎮 Controls:")
    print("  SPACE - Advance dialogue / Start waves")
    print("  ESC - Skip dialogue")
    print("  Q/E - Shoot during active waves")
    
    # Track dialogue and wave progression
    dialogue_events = []
    wave_events = []
    frame_count = 0
    
    while game.running and frame_count < 3600:  # 60 seconds max
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
                elif event.key == pygame.K_SPACE:
                    # Track SPACE presses for dialogue/wave progression
                    dialogue_active = game.dialogue_system.is_active()
                    wave_info = game.wave_manager.get_wave_info()
                    
                    if dialogue_active:
                        speaker = game.dialogue_system.get_current_speaker()
                        text = game.dialogue_system.get_current_text()
                        dialogue_events.append(f"Advanced: {speaker} - {text[:30]}...")
                        print(f"💬 Dialogue advanced: {speaker}")
                    elif wave_info:
                        if wave_info.get('wave_intro_active', False):
                            wave_events.append(f"Started Wave {wave_info['wave_number']}")
                            print(f"🌊 Wave {wave_info['wave_number']} started!")
                        elif wave_info.get('wave_complete', False):
                            wave_events.append(f"Completed Wave {wave_info['wave_number']}")
                            print(f"✅ Wave {wave_info['wave_number']} completed!")
        
        # Let game handle events
        game.handle_events()
        game.update()
        game.draw()
        
        # Track state changes
        if frame_count % 300 == 0:  # Every 5 seconds
            dialogue_active = game.dialogue_system.is_active()
            wave_info = game.wave_manager.get_wave_info()
            
            print(f"\n--- Frame {frame_count} Status ---")
            
            if dialogue_active:
                speaker = game.dialogue_system.get_current_speaker()
                line_num = game.dialogue_system.current_line_index + 1
                total_lines = len(game.dialogue_system.current_dialogue) if game.dialogue_system.current_dialogue else 0
                print(f"💬 DIALOGUE: {speaker} (Line {line_num}/{total_lines})")
                print("🔒 Player movement locked during dialogue")
            elif wave_info:
                if wave_info.get('wave_intro_active', False):
                    print(f"🌊 WAVE {wave_info['wave_number']} INTRO")
                    print("🔒 Player movement locked - Press SPACE to start")
                elif wave_info.get('wave_active', False):
                    time_left = wave_info.get('time_remaining', 0)
                    print(f"⚔️ WAVE {wave_info['wave_number']} ACTIVE - {time_left:.1f}s remaining")
                    print("🏃 Player can move and fight")
                elif wave_info.get('wave_complete', False):
                    print(f"✅ WAVE {wave_info['wave_number']} COMPLETE")
                    print("🔒 Player movement locked - Press SPACE to continue")
                elif wave_info.get('wave_failed', False):
                    print(f"❌ WAVE {wave_info['wave_number']} FAILED")
                    print("💬 Failure dialogue should be active")
            else:
                print("🎮 PRE-GAME STATE")
                print("💬 Waiting for opening dialogue to complete")
            
            print(f"Dialogue Events: {len(dialogue_events)}")
            print(f"Wave Events: {len(wave_events)}")
        
        frame_count += 1
    
    print("\n💬 DIALOGUE FLOW TEST COMPLETED!")
    print(f"Total Dialogue Events: {len(dialogue_events)}")
    print(f"Total Wave Events: {len(wave_events)}")
    
    print("\n🎬 Dialogue Events Log:")
    for i, event in enumerate(dialogue_events[:10]):
        print(f"   {i+1}. {event}")
    if len(dialogue_events) > 10:
        print(f"   ... and {len(dialogue_events) - 10} more dialogue events")
    
    print("\n🌊 Wave Events Log:")
    for i, event in enumerate(wave_events):
        print(f"   {i+1}. {event}")
    
    print("\n✅ Flow Verification:")
    if len(dialogue_events) > 0:
        print("   💬 Dialogue system active and responsive")
    else:
        print("   ⚠️ No dialogue progression detected")
    
    if len(wave_events) > 0:
        print("   🌊 Wave progression working")
    else:
        print("   ⚠️ No wave progression detected")
    
    print("\n🎯 Expected Dialogue Triggers:")
    print("   📖 Opening dialogue: 23 lines (Operator → Pilot → Duke)")
    print("   🌊 After Wave 1: Victory celebration")
    print("   🌊 After Wave 7: Strategic update")
    print("   🌊 After Wave 10: Final battle preparation")
    print("   💀 Wave failure: Dramatic farewell")
    
    pygame.quit()

if __name__ == "__main__":
    test_dialogue_flow()
