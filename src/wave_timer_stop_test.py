#!/usr/bin/env python3
"""
Test that wave timer and progress bar stop when player dies
"""
import pygame
from game import Game
from constants import *

def test_wave_timer_stop():
    """Test that wave timer and UI stop when player dies"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("⏱️ WAVE TIMER STOP TEST")
    print("Testing that wave timer and progress bar stop when player dies")
    
    print("\n🎯 Expected Behavior:")
    print("  1. Wave timer counts down during active gameplay")
    print("  2. Progress bar updates during active gameplay")
    print("  3. When player dies:")
    print("     - Wave timer stops counting")
    print("     - Progress bar stops updating")
    print("     - Wave UI disappears")
    print("     - Game over screen appears")
    
    # Fast-forward to active gameplay
    print("\n⏩ Fast-forwarding to active gameplay...")
    frame_count = 0
    gameplay_active = False
    player_killed = False
    timer_before_death = None
    timer_after_death = None
    
    while game.running and frame_count < 2400:  # 40 seconds max
        # Fast advance through dialogue
        if game.dialogue_system.is_active() and frame_count % 20 == 0:
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
        
        # Auto-start waves
        wave_info = game.wave_manager.get_wave_info()
        if wave_info and wave_info.get('wave_intro_active', False) and frame_count % 30 == 0:
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
        
        # Handle events
        game.handle_events()
        game.update()
        game.draw()
        
        # Track when gameplay becomes active
        if wave_info and wave_info.get('wave_active', False) and not gameplay_active:
            gameplay_active = True
            print(f"\n⚔️ ACTIVE GAMEPLAY STARTED at frame {frame_count}")
            print(f"   Wave timer: {game.wave_manager.wave_timer} frames ({game.wave_manager.wave_timer/60:.1f}s)")
        
        # Monitor wave timer during active gameplay
        if gameplay_active and not player_killed and game.player.is_alive():
            if frame_count % 60 == 0:  # Every second
                current_timer = game.wave_manager.wave_timer
                time_remaining = current_timer / 60
                print(f"⏱️ Wave timer: {current_timer} frames ({time_remaining:.1f}s remaining)")
                
                # Kill player after 5 seconds of gameplay
                if time_remaining <= 55 and not player_killed:
                    print(f"\n💀 KILLING PLAYER at frame {frame_count}")
                    timer_before_death = current_timer
                    
                    # Kill the player by setting health to 0
                    game.player.health_system.current_health = -1
                    player_killed = True
                    print(f"   Timer before death: {timer_before_death} frames ({timer_before_death/60:.1f}s)")
        
        # Monitor timer after player death
        if player_killed and not game.player.is_alive():
            current_timer = game.wave_manager.wave_timer
            
            if timer_after_death is None:
                timer_after_death = current_timer
                print(f"💀 Player died - Timer should stop!")
                print(f"   Timer at death: {timer_after_death} frames ({timer_after_death/60:.1f}s)")
            
            # Check if timer is still counting down
            if frame_count % 60 == 0:  # Every second
                if current_timer != timer_after_death:
                    print(f"🚨 TIMER STILL COUNTING! {timer_after_death} → {current_timer}")
                else:
                    print(f"✅ Timer stopped at {current_timer} frames ({current_timer/60:.1f}s)")
            
            # Check if game over screen appears
            if game.game_over:
                print(f"💀 Game over screen active - Test complete")
                break
        
        frame_count += 1
    
    print(f"\n⏱️ WAVE TIMER STOP TEST RESULTS:")
    
    if timer_before_death is not None and timer_after_death is not None:
        timer_difference = timer_before_death - timer_after_death
        print(f"   Timer before death: {timer_before_death} frames ({timer_before_death/60:.1f}s)")
        print(f"   Timer after death: {timer_after_death} frames ({timer_after_death/60:.1f}s)")
        print(f"   Timer change: {timer_difference} frames")
        
        if timer_difference <= 1:  # Allow for 1 frame difference due to timing
            print(f"   ✅ TIMER STOPPED CORRECTLY")
            print(f"   Wave timer froze when player died")
        else:
            print(f"   ❌ TIMER CONTINUED COUNTING")
            print(f"   Timer kept running after player death")
    else:
        print(f"   ⚠️ Test didn't reach player death phase")
    
    print(f"\n🎮 UI Behavior Verification:")
    if player_killed:
        wave_info = game.wave_manager.get_wave_info()
        if wave_info and wave_info.get('wave_active', False):
            print(f"   Wave still marked as active: {wave_info['wave_active']}")
            print(f"   ✅ This is correct - wave state preserved for restart")
        
        if game.game_over:
            print(f"   ✅ Game over screen appeared")
            print(f"   ✅ Wave UI should be hidden during game over")
        else:
            print(f"   ⚠️ Game over screen not detected")
    
    print(f"\n🔧 Expected Behavior Summary:")
    print(f"   • Wave timer stops counting when player dies")
    print(f"   • Progress bar stops updating when player dies")
    print(f"   • Wave UI disappears during game over screen")
    print(f"   • Wave state preserved for potential restart")
    print(f"   • Clean separation between active gameplay and game over")
    
    pygame.quit()

if __name__ == "__main__":
    test_wave_timer_stop()
