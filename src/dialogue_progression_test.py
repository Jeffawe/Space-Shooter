#!/usr/bin/env python3
"""
Test dialogue progression by simulating SPACE key presses
"""
import pygame
from game import Game
from constants import *

def test_dialogue_progression():
    """Test dialogue progression with simulated input"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("💬 DIALOGUE PROGRESSION TEST")
    print("Simulating SPACE key presses to advance dialogue")
    
    print("\n🎬 Testing Complete Flow:")
    print("  1. Opening dialogue (23 lines)")
    print("  2. Automatic transition to Wave 1 intro")
    print("  3. Wave 1 start and completion")
    print("  4. Post-wave 1 dialogue")
    
    # Track progression
    dialogue_lines_seen = []
    wave_states_seen = []
    frame_count = 0
    last_dialogue_advance = 0
    
    while game.running and frame_count < 3600:  # 60 seconds max
        # Auto-advance dialogue every 2 seconds
        if (game.dialogue_system.is_active() and 
            frame_count - last_dialogue_advance > 120):  # 2 seconds
            
            # Simulate SPACE key press
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
            last_dialogue_advance = frame_count
            
            # Record dialogue line
            speaker = game.dialogue_system.get_current_speaker()
            text = game.dialogue_system.get_current_text()
            if speaker and text:
                dialogue_lines_seen.append(f"{speaker}: {text[:50]}...")
                print(f"💬 Line {len(dialogue_lines_seen)}: {speaker}")
        
        # Auto-start waves
        wave_info = game.wave_manager.get_wave_info()
        if wave_info and wave_info.get('wave_intro_active', False):
            if frame_count % 180 == 0:  # Every 3 seconds, try to start wave
                space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                pygame.event.post(space_event)
                wave_states_seen.append(f"Started Wave {wave_info['wave_number']}")
                print(f"🌊 Auto-started Wave {wave_info['wave_number']}")
        
        # Handle events
        game.handle_events()
        game.update()
        game.draw()
        
        # Status updates
        if frame_count % 300 == 0:  # Every 5 seconds
            dialogue_active = game.dialogue_system.is_active()
            
            print(f"\n--- Frame {frame_count} Status ---")
            
            if dialogue_active:
                speaker = game.dialogue_system.get_current_speaker()
                line_num = game.dialogue_system.current_line_index + 1
                total_lines = len(game.dialogue_system.current_dialogue) if game.dialogue_system.current_dialogue else 0
                print(f"💬 DIALOGUE: {speaker} (Line {line_num}/{total_lines})")
                print(f"   Lines seen so far: {len(dialogue_lines_seen)}")
            elif wave_info:
                if wave_info.get('wave_intro_active', False):
                    print(f"🌊 WAVE {wave_info['wave_number']} INTRO")
                elif wave_info.get('wave_active', False):
                    time_left = wave_info.get('time_remaining', 0)
                    print(f"⚔️ WAVE {wave_info['wave_number']} ACTIVE - {time_left:.1f}s remaining")
                elif wave_info.get('wave_complete', False):
                    print(f"✅ WAVE {wave_info['wave_number']} COMPLETE")
                elif wave_info.get('wave_failed', False):
                    print(f"❌ WAVE {wave_info['wave_number']} FAILED")
            else:
                print("🎮 TRANSITION STATE")
                print("   Checking for wave start...")
        
        frame_count += 1
    
    print("\n💬 DIALOGUE PROGRESSION TEST COMPLETED!")
    print(f"Total dialogue lines seen: {len(dialogue_lines_seen)}")
    print(f"Wave states encountered: {len(wave_states_seen)}")
    
    print("\n📖 Dialogue Lines Captured:")
    for i, line in enumerate(dialogue_lines_seen[:10]):
        print(f"   {i+1}. {line}")
    if len(dialogue_lines_seen) > 10:
        print(f"   ... and {len(dialogue_lines_seen) - 10} more lines")
    
    print("\n🌊 Wave Progression:")
    for state in wave_states_seen:
        print(f"   • {state}")
    
    print("\n✅ Flow Verification:")
    if len(dialogue_lines_seen) >= 20:
        print("   💬 Opening dialogue progressed successfully")
    else:
        print(f"   ⚠️ Only {len(dialogue_lines_seen)} dialogue lines seen (expected ~23)")
    
    if len(wave_states_seen) > 0:
        print("   🌊 Wave progression working")
    else:
        print("   ⚠️ No wave progression detected")
    
    # Check for expected dialogue triggers
    expected_speakers = ['operator', 'pilot', 'Duke']
    speakers_seen = set()
    for line in dialogue_lines_seen:
        for speaker in expected_speakers:
            if line.startswith(speaker):
                speakers_seen.add(speaker)
    
    print(f"\n🎭 Characters in dialogue: {', '.join(speakers_seen)}")
    if len(speakers_seen) == 3:
        print("   ✅ All expected characters appeared")
    else:
        print(f"   ⚠️ Missing characters: {set(expected_speakers) - speakers_seen}")
    
    pygame.quit()

if __name__ == "__main__":
    test_dialogue_progression()
