#!/usr/bin/env python3
"""
Test the spawn position and frequency fixes
"""
import pygame
from game import Game
from constants import *

def test_spawn_fixes():
    """Test the fixed spawn positions and progressive difficulty"""
    pygame.init()
    
    # Create game instance in story mode
    game = Game()
    
    print("🔧 SPAWN FIXES TEST")
    print("Testing fixed spawn positions and progressive difficulty")
    
    print("\n✅ Fixes Applied:")
    print("  1. Spawn positions: Closer to screen edges (-50/+50 instead of -60/+60)")
    print("  2. Safer spawn margins: 50px from edges instead of 100px")
    print("  3. Progressive max enemies: 12 + wave bonus (up to 20 enemies)")
    print("  4. Aggressive spawn frequency scaling")
    
    # Fast-forward to Wave 2 for testing
    print("\n⏩ Fast-forwarding to Wave 2...")
    frame_count = 0
    wave_2_started = False
    spawn_positions = []
    
    while game.running and frame_count < 2400:  # 40 seconds max
        # Keep player alive
        if game.player.health_system.current_health < 50:
            game.player.health_system.current_health = 100
            game.player.health_system.health_bar.current_health = 100
        
        # Fast advance through dialogue
        if game.dialogue_system.is_active() and frame_count % 15 == 0:
            space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            pygame.event.post(space_event)
        
        # Auto-start waves
        wave_info = game.wave_manager.get_wave_info()
        if wave_info:
            if wave_info.get('wave_intro_active', False) and frame_count % 30 == 0:
                space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                pygame.event.post(space_event)
            elif wave_info.get('wave_complete', False) and frame_count % 30 == 0:
                space_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                pygame.event.post(space_event)
        
        # Track enemy spawns
        enemies_before = len(game.enemies)
        
        # Handle events
        game.handle_events()
        game.update()
        game.draw()
        
        # Check for new spawns
        enemies_after = len(game.enemies)
        if enemies_after > enemies_before:
            for enemy in game.enemies:
                pos = (enemy.rect.x, enemy.rect.y)
                if pos not in [sp['pos'] for sp in spawn_positions]:
                    spawn_info = {
                        'pos': pos,
                        'type': enemy.enemy_type,
                        'direction': enemy.direction,
                        'on_screen': (0 <= enemy.rect.x <= SCREEN_WIDTH and 0 <= enemy.rect.y <= SCREEN_HEIGHT),
                        'near_screen': (-100 <= enemy.rect.x <= SCREEN_WIDTH + 100 and 
                                      -100 <= enemy.rect.y <= SCREEN_HEIGHT + 100)
                    }
                    spawn_positions.append(spawn_info)
        
        # Track Wave 2 specifically
        if wave_info and wave_info['wave_number'] == 2:
            if not wave_2_started and wave_info.get('wave_active', False):
                wave_2_started = True
                print(f"\n🌊 WAVE 2 STARTED at frame {frame_count}")
                print(f"   Spawn interval: {game.wave_manager.spawn_interval} frames ({game.wave_manager.spawn_interval/60:.2f}s)")
            
            if wave_2_started and wave_info.get('wave_active', False):
                # Monitor every 3 seconds
                if frame_count % 180 == 0:
                    current_enemies = len(game.enemies)
                    time_remaining = wave_info.get('time_remaining', 0)
                    
                    # Calculate dynamic max enemies for wave 2
                    base_max = 12
                    wave_bonus = min(2 - 1, 8)  # Wave 2 bonus
                    expected_max = base_max + wave_bonus
                    
                    print(f"\n📊 Wave 2 Status - {time_remaining:.1f}s left:")
                    print(f"   Enemies on screen: {current_enemies}/{expected_max}")
                    print(f"   Total spawned: {game.wave_manager.enemies_spawned}")
                    
                    # Check spawn positions
                    recent_spawns = spawn_positions[-10:] if len(spawn_positions) >= 10 else spawn_positions
                    on_screen = sum(1 for s in recent_spawns if s['on_screen'])
                    near_screen = sum(1 for s in recent_spawns if s['near_screen'])
                    
                    print(f"   Recent spawn success: {on_screen}/{len(recent_spawns)} on screen, {near_screen}/{len(recent_spawns)} near screen")
            
            # Wave 2 completed
            if wave_2_started and wave_info.get('wave_complete', False):
                print(f"\n✅ WAVE 2 COMPLETED at frame {frame_count}")
                break
        
        frame_count += 1
    
    print(f"\n🔧 SPAWN FIXES TEST RESULTS:")
    print(f"Total spawn positions tracked: {len(spawn_positions)}")
    
    if spawn_positions:
        # Analyze spawn success rate
        on_screen_spawns = sum(1 for s in spawn_positions if s['on_screen'])
        near_screen_spawns = sum(1 for s in spawn_positions if s['near_screen'])
        
        print(f"\n📊 Spawn Position Analysis:")
        print(f"   On-screen spawns: {on_screen_spawns}/{len(spawn_positions)} ({on_screen_spawns/len(spawn_positions)*100:.1f}%)")
        print(f"   Near-screen spawns: {near_screen_spawns}/{len(spawn_positions)} ({near_screen_spawns/len(spawn_positions)*100:.1f}%)")
        
        # Show recent spawn positions
        print(f"\n📍 Recent Spawn Positions (last 10):")
        for spawn in spawn_positions[-10:]:
            status = "✅ ON" if spawn['on_screen'] else ("🟡 NEAR" if spawn['near_screen'] else "❌ FAR")
            print(f"   {spawn['type']} at {spawn['pos']} moving {spawn['direction']} - {status}")
        
        # Analyze spawn distribution
        spawn_sides = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}
        for spawn in spawn_positions:
            x, y = spawn['pos']
            if x < 0:
                spawn_sides['left'] += 1
            elif x > SCREEN_WIDTH:
                spawn_sides['right'] += 1
            elif y < 0:
                spawn_sides['top'] += 1
            elif y > SCREEN_HEIGHT:
                spawn_sides['bottom'] += 1
        
        print(f"\n🎯 Spawn Side Distribution:")
        for side, count in spawn_sides.items():
            print(f"   {side.capitalize()}: {count} spawns")
        
        # Success evaluation
        success_rate = near_screen_spawns / len(spawn_positions) * 100
        if success_rate >= 95:
            print(f"\n✅ SPAWN FIXES SUCCESSFUL!")
            print(f"   {success_rate:.1f}% of enemies spawn near screen")
        elif success_rate >= 80:
            print(f"\n🟡 SPAWN FIXES MOSTLY WORKING")
            print(f"   {success_rate:.1f}% success rate (target: 95%+)")
        else:
            print(f"\n❌ SPAWN FIXES NEED MORE WORK")
            print(f"   Only {success_rate:.1f}% success rate")
    
    print(f"\n🚀 Progressive Difficulty Features:")
    print(f"   Wave 1: 12 max enemies, 2.0s spawn interval")
    print(f"   Wave 2: 13 max enemies, 1.5s spawn interval")
    print(f"   Wave 3: 14 max enemies, 1.25s spawn interval")
    print(f"   Wave 10: 20 max enemies, 0.5s spawn interval")
    print(f"   🎯 Exponential difficulty increase!")
    
    pygame.quit()

if __name__ == "__main__":
    test_spawn_fixes()
