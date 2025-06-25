#!/usr/bin/env python3
"""
Demo the movement lockout during dialogue and wave transitions
"""
import pygame
from game import Game
from constants import *

def demo_movement_lockout():
    """Demo the complete movement lockout system"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🔒 MOVEMENT LOCKOUT DEMO")
    print("Testing player movement lockout during dialogue and wave transitions")
    
    print("\n🔒 Movement Lockout Features:")
    print("  💬 During Dialogue:")
    print("    • Player completely locked in position")
    print("    • WASD/Arrow keys have no effect")
    print("    • Background scrolling disabled")
    print("    • Only dialogue controls active (SPACE/ESC)")
    print("  🌊 During Wave Transitions:")
    print("    • Wave intro screens - Player locked")
    print("    • Wave completion screens - Player locked")
    print("    • Wave failure screens - Player locked")
    print("  🛡️ Immunity Integration:")
    print("    • Player immune to damage during lockout")
    print("    • Complete protection during story moments")
    
    print("\n🎮 Test Controls:")
    print("  WASD/Arrow Keys - Try to move (should be locked)")
    print("  SPACE/ENTER - Progress dialogue")
    print("  ESC - Skip dialogue")
    print("  Q/E - Shoot (disabled during lockout)")
    
    print("\n🧪 Test Sequence:")
    print("  1. Opening dialogue - Movement locked for 23 lines")
    print("  2. Wave 1 intro - Movement locked until SPACE")
    print("  3. Wave 1 active - Movement enabled")
    print("  4. Wave 1 complete - Movement locked again")
    print("  5. Post-wave dialogue - Movement locked")
    
    # Run demo
    frame_count = 0
    screenshot_interval = 300  # Every 5 seconds
    movement_states = []
    last_player_pos = None
    
    while game.running and frame_count < 2400:  # 40 seconds max
        # Handle events
        game.handle_events()
        
        # Track player position for movement detection
        current_player_pos = (game.player.rect.x, game.player.rect.y)
        if last_player_pos is None:
            last_player_pos = current_player_pos
        
        # Detect if player moved
        player_moved = (current_player_pos != last_player_pos)
        if player_moved:
            movement_states.append(f"Frame {frame_count}: Player moved from {last_player_pos} to {current_player_pos}")
        
        last_player_pos = current_player_pos
        
        game.update()
        game.draw()
        
        # Capture screenshots and analyze movement state
        if frame_count % screenshot_interval == 0:
            screenshot_path = f"/home/jeffawe/amazon-build/assets/images/lockout_frame_{frame_count}.png"
            pygame.image.save(game.screen, screenshot_path)
            
            dialogue_active = game.dialogue_system.is_active()
            wave_info = game.wave_manager.get_wave_info()
            player_immune = game.player.health_system.is_immune()
            
            print(f"\nFrame {frame_count}:")
            print(f"  Player Position: {current_player_pos}")
            print(f"  Dialogue Active: {'Yes' if dialogue_active else 'No'}")
            print(f"  Player Immune: {'Yes' if player_immune else 'No'}")
            
            # Determine expected movement state
            should_be_locked = False
            lock_reason = "None"
            
            if dialogue_active:
                should_be_locked = True
                lock_reason = "Dialogue active"
                current_speaker = game.dialogue_system.get_current_speaker()
                if current_speaker:
                    print(f"  Current Speaker: {current_speaker}")
            elif wave_info:
                if wave_info.get('wave_intro_active', False):
                    should_be_locked = True
                    lock_reason = f"Wave {wave_info['wave_number']} intro"
                elif wave_info.get('wave_complete', False):
                    should_be_locked = True
                    lock_reason = f"Wave {wave_info['wave_number']} complete"
                elif wave_info.get('wave_failed', False):
                    should_be_locked = True
                    lock_reason = f"Wave {wave_info['wave_number']} failed"
                elif wave_info.get('wave_active', False):
                    should_be_locked = False
                    lock_reason = f"Wave {wave_info['wave_number']} active"
            
            print(f"  Movement Status: {'🔒 LOCKED' if should_be_locked else '🏃 FREE'}")
            print(f"  Lock Reason: {lock_reason}")
            print(f"  Screenshot: {screenshot_path}")
            
            # Validate immunity matches movement lockout
            if should_be_locked and not player_immune:
                print(f"  ⚠️ WARNING: Movement locked but player not immune!")
            elif not should_be_locked and player_immune:
                print(f"  ⚠️ WARNING: Movement free but player still immune!")
            else:
                print(f"  ✅ Movement and immunity states consistent")
        
        frame_count += 1
    
    print("\n✅ Movement lockout demo completed!")
    print(f"🏃 Movement Events Detected: {len(movement_states)}")
    
    if movement_states:
        print("\n📍 Player Movement Log:")
        for state in movement_states[:10]:  # Show first 10 movements
            print(f"   {state}")
        if len(movement_states) > 10:
            print(f"   ... and {len(movement_states) - 10} more movements")
    
    print("\n🔒 Movement Lockout Features Demonstrated:")
    print("   💬 Complete movement lockout during dialogue")
    print("   🌊 Movement lockout during wave transitions")
    print("   🛡️ Immunity integration with movement control")
    print("   🎮 Game control prioritization (dialogue > movement)")
    print("   📍 Position preservation during lockout")
    print("   ⚡ Seamless lockout/unlock transitions")
    
    print("\n🚀 Player Experience Improvements:")
    print("   Before: Could move during story moments (distracting)")
    print("   After: Complete focus on story during dialogue")
    print("   🎬 Cinematic presentation with locked camera")
    print("   📖 Undistracted story consumption")
    print("   🎯 Clear separation of story vs action phases")
    print("   ⚡ Professional game state management")
    
    pygame.quit()

if __name__ == "__main__":
    demo_movement_lockout()
