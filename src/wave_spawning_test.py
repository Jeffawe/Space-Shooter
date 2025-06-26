#!/usr/bin/env python3
"""
Test wave spawning to identify why enemies stop spawning
"""
import pygame
from game import Game
from constants import *

def test_wave_spawning():
    """Test continuous enemy spawning throughout wave duration"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🌊 WAVE SPAWNING TEST")
    print("Testing continuous enemy spawning throughout wave duration")
    
    print("\n🎯 Testing Wave 2 Spawning:")
    print("  Expected: Enemies spawn every 1.67s (±0.83s) for 75 seconds")
    print("  Issue: Enemies stop spawning near end of wave")
    
    # Fast-forward to Wave 2
    print("\n⏩ Fast-forwarding through opening dialogue...")
    frame_count = 0
    wave_2_started = False
    spawn_events = []
    
    while game.running and frame_count < 3600:  # 60 seconds max
        # Fast advance through dialogue
        if game.dialogue_system.is_active() and frame_count % 30 == 0:
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
        
        # Auto-start waves
        wave_info = game.wave_manager.get_wave_info()
        if wave_info:
            if wave_info.get('wave_intro_active', False) and frame_count % 60 == 0:
                space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                pygame.event.post(space_event)
            elif wave_info.get('wave_complete', False) and frame_count % 60 == 0:
                # Advance to next wave
                space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                pygame.event.post(space_event)
        
        # Handle events
        game.handle_events()
        game.update()
        game.draw()
        
        # Track Wave 2 specifically
        if wave_info and wave_info['wave_number'] == 2:
            if not wave_2_started and wave_info.get('wave_active', False):
                wave_2_started = True
                print(f"\n🌊 WAVE 2 STARTED at frame {frame_count}")
                print(f"   Duration: {wave_info.get('time_remaining', 0):.1f}s")
                print(f"   Spawn rate: Every 1.67s (±0.83s)")
            
            if wave_2_started and wave_info.get('wave_active', False):
                current_enemies = len(game.enemies)
                time_remaining = wave_info.get('time_remaining', 0)
                
                # Track spawning events
                if frame_count % 60 == 0:  # Every second
                    spawn_events.append({
                        'frame': frame_count,
                        'time_remaining': time_remaining,
                        'enemies_count': current_enemies,
                        'enemies_spawned': game.wave_manager.enemies_spawned,
                        'spawn_timer': game.wave_manager.spawn_timer,
                        'spawn_interval': game.wave_manager.spawn_interval
                    })
                    
                    print(f"⏱️ Wave 2 - {time_remaining:.1f}s left: {current_enemies} enemies, spawned: {game.wave_manager.enemies_spawned}")
                    
                    # Check for spawning issues
                    if time_remaining > 10 and current_enemies == 0:
                        print(f"⚠️ NO ENEMIES with {time_remaining:.1f}s remaining!")
                        print(f"   Spawn timer: {game.wave_manager.spawn_timer}")
                        print(f"   Spawn interval: {game.wave_manager.spawn_interval}")
                        print(f"   Max enemies: {game.wave_manager.max_enemies_on_screen}")
            
            # Wave 2 completed
            if wave_2_started and wave_info.get('wave_complete', False):
                print(f"\n✅ WAVE 2 COMPLETED at frame {frame_count}")
                break
        
        frame_count += 1
    
    print("\n🌊 WAVE 2 SPAWNING ANALYSIS:")
    print(f"Total spawn events tracked: {len(spawn_events)}")
    
    if spawn_events:
        print("\n📊 Spawning Timeline:")
        for i, event in enumerate(spawn_events[-10:]):  # Show last 10 events
            print(f"   {event['time_remaining']:.1f}s left: {event['enemies_count']} enemies (spawned: {event['enemies_spawned']})")
        
        # Analyze spawning gaps
        zero_enemy_periods = [e for e in spawn_events if e['enemies_count'] == 0 and e['time_remaining'] > 5]
        if zero_enemy_periods:
            print(f"\n⚠️ SPAWNING ISSUES DETECTED:")
            print(f"   Periods with 0 enemies: {len(zero_enemy_periods)}")
            for period in zero_enemy_periods:
                print(f"   - {period['time_remaining']:.1f}s remaining: 0 enemies (spawn timer: {period['spawn_timer']})")
        else:
            print("\n✅ No major spawning gaps detected")
    
    print("\n🔧 SPAWNING SYSTEM DEBUG:")
    if hasattr(game.wave_manager, 'spawn_timer'):
        print(f"   Final spawn timer: {game.wave_manager.spawn_timer}")
        print(f"   Final spawn interval: {game.wave_manager.spawn_interval}")
        print(f"   Max enemies on screen: {game.wave_manager.max_enemies_on_screen}")
    
    pygame.quit()

if __name__ == "__main__":
    test_wave_spawning()
