#!/usr/bin/env python3
"""
Test actual player movement lockout during dialogue
"""
import pygame
from game import Game
from constants import *

def test_movement_lockout():
    """Test that player actually cannot move during dialogue"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🔒 MOVEMENT LOCKOUT TEST")
    print("Testing actual player movement prevention during dialogue")
    
    print("\n🎮 Instructions:")
    print("  Try pressing WASD or Arrow Keys during dialogue")
    print("  Player should NOT move at all")
    print("  Press SPACE to advance dialogue and test different states")
    
    # Run test
    frame_count = 0
    last_position = None
    movement_attempts = 0
    successful_movements = 0
    
    while game.running and frame_count < 1800:  # 30 seconds
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                # Let game handle dialogue progression
                game.handle_events()
                
                # Track movement key presses
                if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,
                               pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]:
                    movement_attempts += 1
                    current_pos = (game.player.rect.x, game.player.rect.y)
                    
                    if last_position is not None and current_pos != last_position:
                        successful_movements += 1
                        print(f"⚠️ MOVEMENT DETECTED! From {last_position} to {current_pos}")
                    else:
                        print(f"✅ Movement blocked - player stayed at {current_pos}")
                    
                    last_position = current_pos
        
        # Update and draw
        game.update()
        game.draw()
        
        # Track player position
        current_pos = (game.player.rect.x, game.player.rect.y)
        if last_position is None:
            last_position = current_pos
        
        # Check for unexpected movement
        if current_pos != last_position:
            print(f"🚨 UNEXPECTED MOVEMENT: {last_position} → {current_pos}")
            last_position = current_pos
        
        # Status update every 5 seconds
        if frame_count % 300 == 0:
            dialogue_active = game.dialogue_system.is_active()
            wave_info = game.wave_manager.get_wave_info()
            
            print(f"\n--- Frame {frame_count} Status ---")
            print(f"Player Position: {current_pos}")
            print(f"Dialogue Active: {dialogue_active}")
            print(f"Movement Attempts: {movement_attempts}")
            print(f"Successful Movements: {successful_movements}")
            
            if dialogue_active:
                print("🔒 DIALOGUE ACTIVE - Movement should be BLOCKED")
            elif wave_info:
                if wave_info.get('wave_intro_active', False):
                    print("🔒 WAVE INTRO - Movement should be BLOCKED")
                elif wave_info.get('wave_active', False):
                    print("🏃 WAVE ACTIVE - Movement should be ALLOWED")
                elif wave_info.get('wave_complete', False):
                    print("🔒 WAVE COMPLETE - Movement should be BLOCKED")
            else:
                print("🏃 FREE STATE - Movement should be ALLOWED")
        
        frame_count += 1
    
    print("\n🔒 MOVEMENT LOCKOUT TEST RESULTS:")
    print(f"   Total Movement Attempts: {movement_attempts}")
    print(f"   Successful Movements: {successful_movements}")
    print(f"   Blocked Movements: {movement_attempts - successful_movements}")
    
    if successful_movements == 0 and movement_attempts > 0:
        print("   ✅ PERFECT LOCKOUT - No movement during restricted states")
    elif successful_movements > 0:
        print(f"   ⚠️ LOCKOUT FAILED - {successful_movements} movements got through")
    else:
        print("   ℹ️ No movement attempts detected during test")
    
    pygame.quit()

if __name__ == "__main__":
    test_movement_lockout()
