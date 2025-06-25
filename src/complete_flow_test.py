#!/usr/bin/env python3
"""
Test the complete flow from dialogue to wave gameplay
"""
import pygame
from game import Game
from constants import *

def test_complete_flow():
    """Test the complete flow from opening dialogue through wave gameplay"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🎬 COMPLETE FLOW TEST")
    print("Testing: Opening Dialogue → Wave 1 Intro → Wave 1 Active → Wave 1 Complete")
    
    print("\n🎯 Expected Complete Flow:")
    print("  1. Opening dialogue (23 lines)")
    print("  2. Automatic transition to Wave 1 intro")
    print("  3. Press SPACE to start Wave 1")
    print("  4. Wave 1 runs for 60 seconds")
    print("  5. Wave 1 completes automatically")
    print("  6. Post-wave 1 dialogue appears")
    
    # Track the complete flow
    flow_events = []
    frame_count = 0
    
    while game.running and frame_count < 2400:  # 40 seconds max
        # Auto-advance dialogue
        if game.dialogue_system.is_active() and frame_count % 60 == 0:  # Every 1 second
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
        
        # Auto-start waves
        wave_info = game.wave_manager.get_wave_info()
        if wave_info and wave_info.get('wave_intro_active', False) and frame_count % 120 == 0:
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
            flow_events.append(f"Frame {frame_count}: Started Wave {wave_info['wave_number']}")
        
        # Handle events
        game.handle_events()
        game.update()
        game.draw()
        
        # Track flow events
        dialogue_active = game.dialogue_system.is_active()
        
        # Status updates every 5 seconds
        if frame_count % 300 == 0:
            print(f"\n--- Frame {frame_count} ({frame_count//60}s) ---")
            
            if dialogue_active:
                speaker = game.dialogue_system.get_current_speaker()
                line_num = game.dialogue_system.current_line_index + 1
                total_lines = len(game.dialogue_system.current_dialogue) if game.dialogue_system.current_dialogue else 0
                print(f"💬 DIALOGUE: {speaker} (Line {line_num}/{total_lines})")
                flow_events.append(f"Frame {frame_count}: Dialogue active ({speaker})")
            elif wave_info:
                if wave_info.get('wave_intro_active', False):
                    print(f"🌊 WAVE {wave_info['wave_number']} INTRO")
                    flow_events.append(f"Frame {frame_count}: Wave {wave_info['wave_number']} intro")
                elif wave_info.get('wave_active', False):
                    time_left = wave_info.get('time_remaining', 0)
                    enemies_count = len(game.enemies)
                    print(f"⚔️ WAVE {wave_info['wave_number']} ACTIVE - {time_left:.1f}s left, {enemies_count} enemies")
                    if frame_count % 300 == 0:  # Only log every 5 seconds
                        flow_events.append(f"Frame {frame_count}: Wave {wave_info['wave_number']} active ({time_left:.1f}s left)")
                elif wave_info.get('wave_complete', False):
                    print(f"✅ WAVE {wave_info['wave_number']} COMPLETE")
                    flow_events.append(f"Frame {frame_count}: Wave {wave_info['wave_number']} complete")
                elif wave_info.get('wave_failed', False):
                    print(f"❌ WAVE {wave_info['wave_number']} FAILED")
                    flow_events.append(f"Frame {frame_count}: Wave {wave_info['wave_number']} failed")
            else:
                print("🎮 TRANSITION STATE")
        
        frame_count += 1
    
    print("\n🎬 COMPLETE FLOW TEST FINISHED!")
    print(f"Total flow events: {len(flow_events)}")
    
    print("\n📋 Flow Events Log:")
    for i, event in enumerate(flow_events):
        print(f"   {i+1}. {event}")
    
    # Analyze the flow
    dialogue_events = [e for e in flow_events if 'Dialogue' in e]
    wave_intro_events = [e for e in flow_events if 'intro' in e]
    wave_active_events = [e for e in flow_events if 'active' in e]
    wave_complete_events = [e for e in flow_events if 'complete' in e]
    
    print("\n✅ Flow Analysis:")
    print(f"   💬 Dialogue events: {len(dialogue_events)}")
    print(f"   🌊 Wave intro events: {len(wave_intro_events)}")
    print(f"   ⚔️ Wave active events: {len(wave_active_events)}")
    print(f"   ✅ Wave complete events: {len(wave_complete_events)}")
    
    if len(dialogue_events) > 0 and len(wave_intro_events) > 0:
        print("   🎬 ✅ Dialogue → Wave transition working!")
    else:
        print("   🎬 ❌ Dialogue → Wave transition failed")
    
    if len(wave_intro_events) > 0 and len(wave_active_events) > 0:
        print("   🌊 ✅ Wave intro → Active transition working!")
    else:
        print("   🌊 ❌ Wave intro → Active transition failed")
    
    if len(wave_active_events) > 0:
        print("   ⚔️ ✅ Wave gameplay functioning!")
    else:
        print("   ⚔️ ❌ Wave gameplay not detected")
    
    pygame.quit()

if __name__ == "__main__":
    test_complete_flow()
