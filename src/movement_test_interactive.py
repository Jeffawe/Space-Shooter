#!/usr/bin/env python3
"""
Interactive test for movement lockout - requires user input
"""
import pygame
from game import Game
from constants import *

def test_movement_interactive():
    """Interactive test that requires user to try moving"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🔒 INTERACTIVE MOVEMENT LOCKOUT TEST")
    print("This test requires you to actively try moving the player")
    
    print("\n🎮 TEST INSTRUCTIONS:")
    print("  1. The game will start with dialogue active")
    print("  2. Try pressing W, A, S, D or Arrow Keys to move")
    print("  3. The player should NOT move during dialogue")
    print("  4. Press SPACE to advance dialogue")
    print("  5. Try moving again during wave intro")
    print("  6. Movement should only work during active gameplay")
    
    print("\n🔍 What to watch for:")
    print("  • Player position should stay EXACTLY the same during dialogue")
    print("  • Console messages: '🔒 Player input disabled'")
    print("  • Player should only move when dialogue/transitions are complete")
    
    print("\n⌨️ Controls:")
    print("  WASD/Arrow Keys - Try to move (should be blocked)")
    print("  SPACE - Advance dialogue")
    print("  ESC - Quit test")
    
    input("\nPress ENTER to start the interactive test...")
    
    # Run interactive test
    frame_count = 0
    position_log = []
    
    while game.running and frame_count < 3600:  # 60 seconds max
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
                else:
                    # Let game handle the event
                    game.handle_events()
        
        # Also handle events through game system
        game.handle_events()
        
        # Update and draw
        game.update()
        game.draw()
        
        # Log player position changes
        current_pos = (game.player.rect.x, game.player.rect.y)
        if not position_log or position_log[-1][1] != current_pos:
            position_log.append((frame_count, current_pos))
            
            # Print position changes
            if len(position_log) > 1:
                prev_pos = position_log[-2][1]
                if prev_pos != current_pos:
                    dialogue_active = game.dialogue_system.is_active()
                    wave_info = game.wave_manager.get_wave_info()
                    
                    state = "UNKNOWN"
                    if dialogue_active:
                        state = "DIALOGUE"
                    elif wave_info:
                        if wave_info.get('wave_intro_active', False):
                            state = "WAVE_INTRO"
                        elif wave_info.get('wave_active', False):
                            state = "WAVE_ACTIVE"
                        elif wave_info.get('wave_complete', False):
                            state = "WAVE_COMPLETE"
                    
                    if state in ["DIALOGUE", "WAVE_INTRO", "WAVE_COMPLETE"]:
                        print(f"⚠️ MOVEMENT DURING LOCKOUT! {prev_pos} → {current_pos} (State: {state})")
                    else:
                        print(f"✅ Movement allowed: {prev_pos} → {current_pos} (State: {state})")
        
        # Status update every 10 seconds
        if frame_count % 600 == 0:
            dialogue_active = game.dialogue_system.is_active()
            wave_info = game.wave_manager.get_wave_info()
            
            print(f"\n--- Status Update (Frame {frame_count}) ---")
            print(f"Player Position: {current_pos}")
            print(f"Position Changes: {len(position_log)}")
            
            if dialogue_active:
                speaker = game.dialogue_system.get_current_speaker()
                print(f"State: DIALOGUE ACTIVE ({speaker})")
                print("🔒 Movement should be COMPLETELY BLOCKED")
            elif wave_info:
                if wave_info.get('wave_intro_active', False):
                    print(f"State: WAVE {wave_info['wave_number']} INTRO")
                    print("🔒 Movement should be BLOCKED")
                elif wave_info.get('wave_active', False):
                    print(f"State: WAVE {wave_info['wave_number']} ACTIVE")
                    print("🏃 Movement should be ALLOWED")
                elif wave_info.get('wave_complete', False):
                    print(f"State: WAVE {wave_info['wave_number']} COMPLETE")
                    print("🔒 Movement should be BLOCKED")
            
            print("Try pressing WASD or Arrow Keys now!")
        
        frame_count += 1
    
    print("\n🔒 INTERACTIVE TEST COMPLETED!")
    print(f"Total position changes recorded: {len(position_log)}")
    
    if len(position_log) <= 1:
        print("✅ PERFECT LOCKOUT - Player never moved!")
    else:
        print("\n📍 Position Change Log:")
        for i, (frame, pos) in enumerate(position_log[:10]):
            print(f"   Frame {frame}: {pos}")
        if len(position_log) > 10:
            print(f"   ... and {len(position_log) - 10} more position changes")
    
    pygame.quit()

if __name__ == "__main__":
    test_movement_interactive()
