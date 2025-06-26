#!/usr/bin/env python3
"""
Test the failure dialogue on game over screen
"""
import pygame
from game import Game
from constants import *

def test_game_over_dialogue():
    """Test that failure dialogue appears on game over screen"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("💀 GAME OVER DIALOGUE TEST")
    print("Testing failure dialogue integration with game over screen")
    
    print("\n🎯 Expected Behavior:")
    print("  1. Player dies during story mode")
    print("  2. Game over screen appears with statistics")
    print("  3. Failure dialogue appears at bottom of screen")
    print("  4. Duke's farewell message: 'They got through the defenses...'")
    print("  5. Player can press SPACE to advance dialogue")
    print("  6. After dialogue, player can press R to restart")
    
    # Fast-forward to gameplay and simulate player death
    print("\n⏩ Fast-forwarding to gameplay...")
    frame_count = 0
    gameplay_reached = False
    player_killed = False
    
    while game.running and frame_count < 2400:  # 40 seconds max
        # Fast advance through dialogue
        if game.dialogue_system.is_active() and frame_count % 30 == 0:
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
        
        # Auto-start waves
        wave_info = game.wave_manager.get_wave_info()
        if wave_info and wave_info.get('wave_intro_active', False) and frame_count % 60 == 0:
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
            gameplay_reached = True
            print("🎮 Gameplay reached - simulating player death...")
        
        # Simulate player death after reaching gameplay
        if gameplay_reached and not player_killed and frame_count % 120 == 0:
            # Kill the player by setting health to 0
            game.player.health_system.current_health = 0
            game.player.health_system.health_bar.current_health = 0
            
            # Trigger player death
            if game.player.is_alive():
                # Force player death
                game.player.health_system.current_health = -1
                print("💀 Simulating player death...")
            
            player_killed = True
        
        # Handle events
        game.handle_events()
        game.update()
        game.draw()
        
        # Monitor game over state
        if game.game_over:
            dialogue_active = game.dialogue_system.is_active()
            
            if frame_count % 60 == 0:  # Every second
                print(f"\n💀 Game Over State (Frame {frame_count}):")
                print(f"   Game over: {game.game_over}")
                print(f"   Player death timer: {game.player_death_timer}")
                print(f"   Dialogue active: {dialogue_active}")
                
                if dialogue_active:
                    speaker = game.dialogue_system.get_current_speaker()
                    text = game.dialogue_system.get_current_text()
                    print(f"   Current dialogue: {speaker}")
                    print(f"   Text preview: {text[:50]}..." if text else "   No text")
                    
                    # Test dialogue advancement
                    if frame_count % 180 == 0:  # Every 3 seconds
                        print("   🎮 Advancing dialogue...")
                        space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                        pygame.event.post(space_event)
                
                # Break after testing dialogue
                if not dialogue_active and game.player_death_timer <= 0:
                    print("   ✅ Dialogue completed - ready for restart")
                    break
        
        frame_count += 1
    
    print("\n💀 GAME OVER DIALOGUE TEST COMPLETED!")
    
    # Final state check
    final_dialogue_active = game.dialogue_system.is_active()
    final_game_over = game.game_over
    
    print(f"\n📊 Final Test Results:")
    print(f"   Game over state: {final_game_over}")
    print(f"   Dialogue active: {final_dialogue_active}")
    print(f"   Player death timer: {game.player_death_timer}")
    
    if final_game_over:
        print("   ✅ Game over screen successfully triggered")
    else:
        print("   ❌ Game over screen not triggered")
    
    print(f"\n🎬 Expected Failure Dialogue:")
    print(f"   Speaker: Duke")
    print(f"   Message: 'They got through the defenses. The fleet is coming close.'")
    print(f"   Full text: 'PILOT! You fought a good fight! but it wasn't enough.'")
    print(f"   Ending: 'Fly away and live to fly another day. Juvar will be in the hands'")
    print(f"   Final: 'of the enemies by Dusk but the Empire will live on and fight.'")
    print(f"   Farewell: 'Fight forever. Goodbye Pilot. Take care of the ship!'")
    
    print(f"\n🎮 Integration Features:")
    print(f"   • Failure dialogue appears at bottom of game over screen")
    print(f"   • Red border and styling for dramatic effect")
    print(f"   • SPACE to advance dialogue, R to restart after completion")
    print(f"   • Seamless integration with existing game over functionality")
    
    pygame.quit()

if __name__ == "__main__":
    test_game_over_dialogue()
