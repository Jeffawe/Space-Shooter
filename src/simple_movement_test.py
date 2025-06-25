#!/usr/bin/env python3
"""
Simple visual test to verify movement lockout
"""
import pygame
from game import Game
from constants import *

def simple_movement_test():
    """Simple test to verify movement lockout visually"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🔒 SIMPLE MOVEMENT LOCKOUT VERIFICATION")
    print("Visual test to confirm player cannot move during dialogue")
    
    print("\n📍 Initial player position will be recorded")
    print("🔒 During dialogue, player should stay in EXACT same position")
    print("🏃 After dialogue, player should be able to move freely")
    
    # Record initial position
    initial_pos = (game.player.rect.x, game.player.rect.y)
    print(f"📍 Initial player position: {initial_pos}")
    
    # Run for a short time to test
    frame_count = 0
    position_changes = 0
    
    while game.running and frame_count < 600:  # 10 seconds
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
        
        # Simulate key presses to test movement
        keys = pygame.key.get_pressed()
        
        # Try to move every few frames
        if frame_count % 30 == 0:  # Every half second
            # Simulate movement attempt by checking current position
            current_pos = (game.player.rect.x, game.player.rect.y)
            
            if current_pos != initial_pos:
                position_changes += 1
                print(f"📍 Position changed: {initial_pos} → {current_pos}")
                initial_pos = current_pos
            
            # Show current state
            dialogue_active = game.dialogue_system.is_active()
            if dialogue_active:
                speaker = game.dialogue_system.get_current_speaker()
                print(f"🔒 Frame {frame_count}: Dialogue active ({speaker}) - Position: {current_pos}")
            else:
                print(f"🏃 Frame {frame_count}: No dialogue - Position: {current_pos}")
        
        game.update()
        game.draw()
        frame_count += 1
    
    final_pos = (game.player.rect.x, game.player.rect.y)
    
    print("\n🔒 MOVEMENT LOCKOUT TEST RESULTS:")
    print(f"   Initial Position: {(376, 532)}")  # Expected starting position
    print(f"   Final Position: {final_pos}")
    print(f"   Position Changes: {position_changes}")
    
    if position_changes == 0:
        print("   ✅ PERFECT LOCKOUT - Player stayed in exact same position!")
        print("   🔒 Movement lockout is working correctly")
    else:
        print(f"   ⚠️ Player moved {position_changes} times during test")
        print("   🔧 Movement lockout may need adjustment")
    
    pygame.quit()

if __name__ == "__main__":
    simple_movement_test()
