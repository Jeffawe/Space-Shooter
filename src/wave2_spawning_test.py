#!/usr/bin/env python3
"""
Test Wave 2 spawning with player kept alive
"""
import pygame
from game import Game
from constants import *

def test_wave2_spawning():
    """Test Wave 2 spawning with player health maintained"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🌊 WAVE 2 SPAWNING TEST (Player Kept Alive)")
    print("Testing continuous enemy spawning throughout Wave 2 duration")
    
    # Fast-forward to Wave 2
    print("\n⏩ Fast-forwarding to Wave 2...")
    frame_count = 0
    wave_2_started = False
    spawn_timeline = []
    
    while game.running and frame_count < 4800:  # 80 seconds max
        # Keep player alive by maintaining health
        if game.player.health_system.current_health < 50:
            game.player.health_system.current_health = 100
            game.player.health_system.health_bar.current_health = 100
        
        # Fast advance through dialogue
        if game.dialogue_system.is_active() and frame_count % 20 == 0:
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
        
        # Auto-start waves and advance
        wave_info = game.wave_manager.get_wave_info()
        if wave_info:
            if wave_info.get('wave_intro_active', False) and frame_count % 30 == 0:
                space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                pygame.event.post(space_event)
            elif wave_info.get('wave_complete', False) and frame_count % 30 == 0:
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
                print(f"   Expected duration: 75 seconds")
                print(f"   Expected spawn rate: Every 1.67s (±0.83s)")
                print(f"   Enemy types: fighter1, fighter2, gunship")
            
            if wave_2_started and wave_info.get('wave_active', False):
                current_enemies = len(game.enemies)
                time_remaining = wave_info.get('time_remaining', 0)
                enemies_spawned = game.wave_manager.enemies_spawned
                
                # Record spawning data every second
                if frame_count % 60 == 0:
                    spawn_data = {
                        'time_remaining': time_remaining,
                        'enemies_count': current_enemies,
                        'enemies_spawned': enemies_spawned,
                        'spawn_timer': game.wave_manager.spawn_timer,
                        'spawn_interval': game.wave_manager.spawn_interval
                    }
                    spawn_timeline.append(spawn_data)
                    
                    print(f"⏱️ {time_remaining:.1f}s left: {current_enemies} enemies (total spawned: {enemies_spawned})")
                    
                    # Alert if no enemies with significant time left
                    if time_remaining > 5 and current_enemies == 0:
                        print(f"🚨 NO ENEMIES with {time_remaining:.1f}s remaining!")
                        print(f"   Spawn timer: {game.wave_manager.spawn_timer}/{game.wave_manager.spawn_interval}")
                        print(f"   Max enemies allowed: {game.wave_manager.max_enemies_on_screen}")
            
            # Wave 2 completed
            if wave_2_started and wave_info.get('wave_complete', False):
                print(f"\n✅ WAVE 2 COMPLETED at frame {frame_count}")
                final_spawned = game.wave_manager.enemies_spawned
                print(f"   Total enemies spawned: {final_spawned}")
                break
        
        frame_count += 1
    
    print(f"\n📊 WAVE 2 SPAWNING ANALYSIS:")
    print(f"Total timeline entries: {len(spawn_timeline)}")
    
    if spawn_timeline:
        print(f"\n⏱️ Spawning Timeline (last 15 entries):")
        for entry in spawn_timeline[-15:]:
            status = "✅" if entry['enemies_count'] > 0 else "⚠️"
            print(f"   {status} {entry['time_remaining']:.1f}s: {entry['enemies_count']} enemies (spawned: {entry['enemies_spawned']})")
        
        # Analyze for gaps
        zero_enemy_periods = [e for e in spawn_timeline if e['enemies_count'] == 0 and e['time_remaining'] > 3]
        if zero_enemy_periods:
            print(f"\n🚨 SPAWNING GAPS DETECTED:")
            for gap in zero_enemy_periods:
                print(f"   - {gap['time_remaining']:.1f}s remaining: 0 enemies (timer: {gap['spawn_timer']}/{gap['spawn_interval']})")
        
        # Check spawn rate consistency
        spawn_counts = [e['enemies_spawned'] for e in spawn_timeline]
        if len(spawn_counts) > 1:
            spawn_rate = (spawn_counts[-1] - spawn_counts[0]) / len(spawn_counts)
            expected_rate = 60 / (100/60)  # Expected spawns per second based on interval
            print(f"\n📈 Spawn Rate Analysis:")
            print(f"   Actual spawn rate: {spawn_rate:.2f} enemies/second")
            print(f"   Expected spawn rate: ~{expected_rate:.2f} enemies/second")
    
    print(f"\n🔧 Final Wave Manager State:")
    print(f"   Spawn timer: {game.wave_manager.spawn_timer}")
    print(f"   Spawn interval: {game.wave_manager.spawn_interval}")
    print(f"   Spawn variance: {getattr(game.wave_manager, 'spawn_variance', 'N/A')}")
    print(f"   Max enemies on screen: {game.wave_manager.max_enemies_on_screen}")
    
    pygame.quit()

if __name__ == "__main__":
    test_wave2_spawning()
